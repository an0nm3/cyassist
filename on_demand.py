#!/usr/bin/env python3
"""Cyassist On-Demand — fetch exploit code from URL when needed, never cache.
Also: Watch mode that triggers Rudra bridge when relevant CVE drops."""

import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib3
from pathlib import Path
from typing import Optional
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HERE = Path(__file__).parent
USER_AGENT = "cyassist-ondemand/1.0"

try:
    from intel_db import IntelDB
except ImportError:
    IntelDB = None

try:
    from rudra_bridge import RudraBridge
except ImportError:
    RudraBridge = None


class Fmt:
    _no_color = not sys.stdout.isatty()
    @classmethod
    def _w(cls, c, s, r="0"):
        if cls._no_color or not s: return s
        return f"\033[{c}m{s}\033[{r}m"
    @classmethod
    def green(cls, s): return cls._w("32", s)
    @classmethod
    def red(cls, s): return cls._w("31", s)
    @classmethod
    def yellow(cls, s): return cls._w("33", s)
    @classmethod
    def bold(cls, s): return cls._w("1", s)
    @classmethod
    def dim(cls, s): return cls._w("2", s)
    @classmethod
    def cyan(cls, s): return cls._w("36", s)


def _fetch(url: str, timeout: int = 30) -> Optional[str]:
    try:
        import requests as _req
        r = _req.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout, verify=False)
        return r.text if r.status_code == 200 else None
    except Exception:
        pass
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


# ── Exploit-DB raw code fetch ──────────────────────────────────────────────
def fetch_exploitdb_code(edb_id: str) -> Optional[str]:
    """Fetch actual exploit code from Exploit-DB by EDB ID.
    Files are in exploits/{platform}/{type}/{id}.ext on GitLab.
    Uses HEAD probes first (cheap), then GET on candidates."""
    base = "https://gitlab.com/exploit-database/exploitdb/-/raw/main"
    _exts = [".c", ".py", ".rb", ".php", ".pl", ".txt", ".sh",
             ".md", ".java", ".go", ".rs", ".js", ".html", ".asp"]

    import requests as _req
    session = _req.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    def _head(url: str) -> bool:
        try:
            return session.head(url, timeout=5, verify=False).status_code == 200
        except Exception:
            return False

    def _get(url: str) -> Optional[str]:
        try:
            r = session.get(url, timeout=10, verify=False)
            return r.text if r.status_code == 200 and len(r.text) > 150 else None
        except Exception:
            return None

    # Root-level check
    for ext in _exts:
        if _head(f"{base}/{edb_id}{ext}"):
            return _get(f"{base}/{edb_id}{ext}")

    # Platform/type combos — HEAD check first, then GET
    _paths = [f"exploits/{p}/{t}" for p in
              ["linux", "windows", "multiple", "php", "java",
               "python", "ruby", "perl", "cgi", "aix",
               "freebsd", "solaris", "macos", "bsd", "android",
               "hardware", "nodejs", "ios"]
              for t in ["webapps", "remote", "local"]]
    for path in _paths:
        for ext in _exts:
            url = f"{base}/{path}/{edb_id}{ext}"
            if _head(url):
                code = _get(url)
                if code:
                    return code

    return None


# ── GitHub raw PoC fetch ──────────────────────────────────────────────────
def fetch_github_raw(repo_url: str) -> Optional[str]:
    """Try to fetch raw exploit code from a GitHub repo URL.
    Tries common PoC filenames, README, and scanning repo root."""
    raw_base = repo_url.replace("github.com", "raw.githubusercontent.com").rstrip("/")
    api_base = f"https://api.github.com/repos/{'/'.join(repo_url.rstrip('/').split('/')[-2:])}"

    # Common PoC filenames
    _candidates = [
        "/main/exploit.py", "/main/poc.py", "/main/exploit.sh",
        "/main/exploit.rb", "/main/exploit.php", "/main/poc.sh",
        "/main/exploit.go", "/main/exploit.rs",
        "/main/exploit.c", "/main/exploit.pl",
        "/main/exploit.js", "/main/exploit.ps1",
        "/main/CVE-*.py", "/main/PoC.py", "/main/poC.py",
        "/master/exploit.py", "/master/poc.py", "/master/exploit.sh",
    ]

    for suffix in _candidates:
        if "*" in suffix:
            continue
        code = _fetch(raw_base + suffix, timeout=10)
        if code and len(code) > 80:
            return f"# Source: {repo_url}\n# {raw_base}{suffix}\n\n{code}"

    # Try README as fallback (often has usage instructions)
    for readme in ["/main/README.md", "/master/README.md"]:
        code = _fetch(raw_base + readme, timeout=8)
        if code and len(code) > 80 and "CVE" in code:
            return f"# Source: {repo_url} (README)\n# PoC usage from README:\n\n{code[:3000]}"

    return None


# ── Nuclei run on-demand ───────────────────────────────────────────────────
def run_nuclei(target_url: str, template_ids: list[str],
               timeout: int = 60) -> list[dict]:
    """Run nuclei with specific template IDs. Returns JSON findings."""
    if not template_ids:
        return []
    try:
        result = subprocess.run(
            ["nuclei", "-u", target_url,
             "-id", ",".join(template_ids[:20]),
             "-json", "-silent",
             "-timeout", "10",
             "-disable-update-check"],
            capture_output=True, text=True, timeout=timeout
        )
        findings = []
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                try:
                    findings.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return findings
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
        return []


# ── Watch Mode with Rudra Auto-Scan ────────────────────────────────────────
def watch_mode(db: IntelDB, bridge: RudraBridge = None,
               interval: int = 300, auto_scan: bool = False,
               targets: list[dict] = None):
    """Watch for new CVEs/PoCs. Optionally auto-trigger Rudra scans."""
    print(Fmt.banner("WATCH MODE", f"checking every {interval}s, auto-scan: {auto_scan}"))
    seen_cves = set(r["id"] for r in db.db.execute(
        "SELECT id FROM cves").fetchall())
    last_check = datetime.datetime.now()

    try:
        while True:
            now = datetime.datetime.now()
            new_cves = set(r["id"] for r in db.db.execute(
                "SELECT id FROM cves WHERE updated_at > ?",
                (last_check.isoformat(),)
            ).fetchall()) - seen_cves

            if new_cves:
                ts = now.strftime("%H:%M:%S")
                print(f"\n  {Fmt.green(f'[{ts}] {len(new_cves)} new CVE(s)')}")
                for cve_id in sorted(new_cves)[:10]:
                    cve = db.get_cve(cve_id)
                    cvss = cve.get("cvss", "N/A") if cve else "N/A"
                    epss = cve.get("epss", 0) if cve else 0
                    poc = " [PoC]" if (cve and cve.get("has_poc")) else ""
                    kev = " [KEV]" if (cve and cve.get("in_kev")) else ""
                    print(f"    {Fmt.cyan(cve_id)}  CVSS:{cvss}  EPSS:{epss:.4f}{poc}{kev}")

                    # Auto-scan: check if any target matches this CVE
                    if auto_scan and bridge and targets:
                        for t in targets:
                            techs = json.loads(t.get("techs", "[]"))
                            for tech in techs:
                                cves_for_tech = bridge.get_cves_for_tech(tech)
                                if any(c.get("cve_id") == cve_id for c in cves_for_tech):
                                    url = t.get("url", "")
                                    if url:
                                        t_name = t.get("name", "")
                                        print(f"      → {Fmt.yellow(f'{t_name}: auto-scan queued')}")
                                        config = bridge.generate_scan_config(url, [tech])
                                        pc = config.get("probe_count", 0)
                                        nc = config.get("nuclei_count", 0)
                                        print(f"        {Fmt.dim(f'{pc} probes, {nc} nuclei templates')}")

                seen_cves.update(new_cves)
            else:
                ts_now = now.strftime("%H:%M:%S")
                print(f"  {Fmt.dim(f'[{ts_now}] No new CVEs')}", end="\r")

            last_check = now
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n  {Fmt.yellow('Watch mode stopped.')}")


def main():
    import argparse
    p = argparse.ArgumentParser(description="Cyassist on-demand + watch")
    p.add_argument("--fetch-exploit", metavar="URL", help="Fetch exploit code from URL (no cache)")
    p.add_argument("--fetch-cve", metavar="CVE-ID", help="Fetch exploit code for a CVE (from stored URLs)")
    p.add_argument("--nuclei", metavar="URL", help="Run nuclei templates for target")
    p.add_argument("--nuclei-cve", metavar="CVE-ID", help="Run nuclei templates matching a CVE")
    p.add_argument("--watch", action="store_true", help="Watch mode for new intel")
    p.add_argument("--watch-interval", type=int, default=300)
    p.add_argument("--auto-scan", action="store_true", help="Auto-trigger Rudra scans on relevant CVEs")
    args = p.parse_args()

    if not IntelDB:
        print("Error: intel_db.py required")
        sys.exit(1)

    db = IntelDB()

    if args.fetch_exploit:
        url = args.fetch_exploit
        code = None
        if "exploit-db" in url or "exploits/" in url:
            edb_match = re.search(r'/exploits/(\d+)', url)
            if edb_match:
                code = fetch_exploitdb_code(edb_match.group(1))
        elif "github.com" in url:
            code = fetch_github_raw(url)
        else:
            code = _fetch(url)

        if code:
            print(f"  {Fmt.green('Exploit code fetched (NOT CACHED):')}")
            print(f"  {Fmt.dim('─' * 60)}")
            print(code[:3000])
            print(f"  {Fmt.dim('─' * 60)}")
            print(f"  {Fmt.dim(f'{len(code)} characters')}")
        else:
            print(f"  {Fmt.red(f'Could not fetch exploit from: {url}')}")
            print(f"  {Fmt.dim('Visit the URL directly or check the EDB ID')}")

    elif args.fetch_cve:
        exploits = db.get_exploits_for_cve(args.fetch_cve)
        if not exploits:
            print(f"  {Fmt.yellow(f'No exploit URLs stored for {args.fetch_cve}')}")
            db.close()
            return
        print(f"  {Fmt.bold(f'{len(exploits)} exploit source(s) for {args.fetch_cve}')}")
        for ex in exploits:
            url = ex.get("url", "")
            technique = ex.get("technique", "?")
            source = ex.get("source", "?")
            print(f"  [{Fmt.cyan(source)}] {Fmt.green(technique)}  {Fmt.dim(url)}")

    elif args.nuclei:
        template_ids = []
        if args.nuclei_cve:
            templates = db.get_templates_for_cve(args.nuclei_cve)
            template_ids = [t["template_id"] for t in templates]
        print(f"  Running {len(template_ids)} nuclei templates against {args.nuclei}")
        findings = run_nuclei(args.nuclei, template_ids)
        if findings:
            print(f"  {Fmt.red(f'{len(findings)} finding(s)')}")
            for f in findings[:5]:
                print(f"    [{f.get('template-id', '?')}] {f.get('matched-at', '')}")
        else:
            print(f"  {Fmt.green('No findings')}")

    elif args.watch:
        bridge = RudraBridge(db) if RudraBridge else None
        targets = db.get_targets() if args.auto_scan else None
        watch_mode(db, bridge, args.watch_interval, args.auto_scan, targets)

    db.close()


if __name__ == "__main__":
    main()
