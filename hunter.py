#!/usr/bin/env python3
"""Cyassist hunter — PoC/exploit/KAV collection + target matching engine.

Usage:
  python3 hunter.py --hunt          Full hunting pipeline
  python3 hunter.py --poc           Show today's PoCs
  python3 hunter.py --kev           Show CISA KEV catalog
  python3 hunter.py --auto          Silent daily auto-run
  python3 hunter.py --cve CVE-2026-XXXX  Enrich a specific CVE
  python3 hunter.py --targets       List registered targets
  python3 hunter.py --target-add    Add a target
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

# ── Paths ──────────────────────────────────────────────────────────────────
HERE = Path(__file__).parent
EXPLOITS_DIR = HERE / "exploits"
KEV_DIR = HERE / "kev"
TARGETS_FILE = HERE / "targets.yaml"
CONFIG_FILE = HERE / "config.yaml"

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EXPLOITDB_RSS = "https://www.exploit-db.com/rss.xml"
PACKETSTORM_RSS = "https://packetstormsecurity.com/feed/"
GITHUB_API = "https://api.github.com/search/repositories"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GH_TOKEN", "")
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
EPSS_API = "https://api.first.org/data/v1/epss"
NVD_API_KEY = os.environ.get("NVD_API_KEY", "")

USER_AGENT = "cyassist-hunter/1.0"


# ── ANSI ────────────────────────────────────────────────────────────────────
class Fmt:
    _no_color = not sys.stdout.isatty()
    @classmethod
    def _w(cls, c, s, r="0"):
        if cls._no_color or not s: return s
        return f"\033[{c}m{s}\033[{r}m"
    @classmethod
    def bold(cls, s): return cls._w("1", s)
    @classmethod
    def dim(cls, s): return cls._w("2", s)
    @classmethod
    def red(cls, s): return cls._w("31", s)
    @classmethod
    def green(cls, s): return cls._w("32", s)
    @classmethod
    def yellow(cls, s): return cls._w("33", s)
    @classmethod
    def blue(cls, s): return cls._w("34", s)
    @classmethod
    def magenta(cls, s): return cls._w("35", s)
    @classmethod
    def cyan(cls, s): return cls._w("36", s)
    @classmethod
    def cve(cls, s): return cls._w("1;31", s)
    @classmethod
    def url(cls, s): return cls._w("4;34", s)
    @classmethod
    def hr(cls, c="\u2501", n=60): return cls.dim(c * n)
    @classmethod
    def banner(cls, t, sub=""):
        l = cls.hr()
        parts = [f"  {cls.bold(t)}"]
        if sub: parts.append(f"  {cls.dim(sub)}")
        return f"\n{l}\n{chr(10).join(parts)}\n{l}\n"


# ── Helpers ─────────────────────────────────────────────────────────────────
def _fetch_url(url: str, timeout: int = 20, headers: dict = None) -> Optional[bytes]:
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    try:
        req = urllib.request.Request(url, headers=req_headers)
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read()
    except Exception as e:
        print(f"  {Fmt.red(f'fetch failed: {url} — {e}')}", file=sys.stderr)
        return None


def _save_article(dir_path: Path, source: str, title: str, url: str,
                  body: str, tags: list, date_str: str = None, extra: dict = None):
    dir_path.mkdir(parents=True, exist_ok=True)
    uid = hashlib.md5(f"{source}:{title}:{url}".encode()).hexdigest()[:12]
    fname = dir_path / f"{uid}.md"
    if fname.exists():
        return False
    d = date_str or datetime.datetime.now().strftime("%Y-%m-%d")
    tag_str = ", ".join(tags)
    extra_fm = ""
    if extra:
        extra_fm = "\n" + "\n".join(f"{k}: {v}" for k, v in extra.items() if v)
    content = f"""---
title: "{title}"
source: "{source}"
date: "{d}"
category: "poc"
tags: [{tag_str}]
url: "{url}"{extra_fm}
---
{body.strip()[:2000]}"""
    fname.write_text(content)
    return True


def _cves_from_text(text: str) -> list[str]:
    return list(set(re.findall(r"CVE-\d{4}-\d{4,}", text)))


# ── Phase 1: Exploit-DB PoC Fetcher ───────────────────────────────────────
def fetch_exploitdb(max_items: int = 50) -> int:
    """Fetch recent exploits from exploit-db RSS. Returns count saved."""
    data = _fetch_url(EXPLOITDB_RSS)
    if not data:
        return 0
    count = 0
    try:
        root = ET.fromstring(data)
        for item in list(root.iter("item"))[:max_items]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            pubdate = item.findtext("pubDate", "")
            if not title:
                continue
            date_str = ""
            if pubdate:
                try:
                    parsed = datetime.datetime.strptime(pubdate.split("+")[0].strip(),
                                                        "%a, %d %b %Y %H:%M:%S ")
                    date_str = parsed.strftime("%Y-%m-%d")
                except ValueError:
                    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            cves = _cves_from_text(f"{title} {desc}")
            tags = ["Exploit", "PoC"] + [f"CVE:{c}" for c in cves[:3]]
            extra = {}
            if link:
                edb_match = re.search(r'/exploits/(\d+)', link)
                if edb_match:
                    extra["edb_id"] = edb_match.group(1)
            if _save_article(EXPLOITS_DIR / "exploit-db" / (date_str or "unknown"),
                            "exploit-db", title, link, desc[:500], tags, date_str, extra):
                count += 1
    except ET.ParseError as e:
        print(f"  {Fmt.red(f'exploit-db parse error: {e}')}", file=sys.stderr)
    return count


# ── Phase 1: Packet Storm PoC Fetcher ──────────────────────────────────────
def fetch_packetstorm(max_items: int = 30) -> int:
    """Fetch recent exploits from Packet Storm RSS."""
    data = _fetch_url(PACKETSTORM_RSS)
    if not data:
        return 0
    count = 0
    try:
        text_data = data.decode("utf-8", errors="replace")
        entries = re.findall(r'<entry[^>]*>(.*?)</entry>', text_data, re.DOTALL)
        for entry_xml in entries[:max_items]:
            title_m = re.search(r'<title[^>]*>(.*?)</title>', entry_xml, re.DOTALL)
            link_m = re.search(r'<link[^>]*href="([^"]+)"', entry_xml)
            pub_m = re.search(r'<published[^>]*>(.*?)</published>', entry_xml)
            title = title_m.group(1).strip() if title_m else ""
            link = link_m.group(1) if link_m else ""
            published = pub_m.group(1).strip()[:10] if pub_m else ""
            date_str = published or datetime.datetime.now().strftime("%Y-%m-%d")
            cves = _cves_from_text(title)
            tags = ["Exploit", "PoC"] + [f"CVE:{c}" for c in cves[:3]]
            if _save_article(EXPLOITS_DIR / "packetstorm" / date_str,
                            "packetstorm", title, link, "", tags, date_str):
                count += 1
    except Exception as e:
        print(f"  {Fmt.red(f'packetstorm parse error: {e}')}", file=sys.stderr)
    return count


# ── Phase 1: GitHub PoC Harvester ──────────────────────────────────────────
def fetch_github_pocs(cves: list[str]) -> dict[str, list[dict]]:
    """Search GitHub for PoC repos matching given CVEs. Returns {cve: [repo_info]}."""
    results = {}
    if not cves:
        return results
    for cve_id in cves[:10]:
        query = urllib.parse.urlencode({"q": f"{cve_id} in:name,description,topic"})
        url = f"{GITHUB_API}?{query}&sort=stars&order=desc"
        gh_headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None
        data = _fetch_url(url, headers=gh_headers)
        if not data:
            continue
        try:
            body = json.loads(data)
            repos = body.get("items", [])[:5]
            if repos:
                results[cve_id] = []
                date_str = datetime.datetime.now().strftime("%Y-%m-%d")
                for repo in repos:
                    repo_name = repo.get("full_name", "?")
                    repo_url = repo.get("html_url", "")
                    stars = repo.get("stargazers_count", 0)
                    desc = repo.get("description", "") or ""
                    topic = ",".join(repo.get("topics", [])[:5])
                    tags = ["PoC", "GitHub", f"CVE:{cve_id}"]
                    extra = {"stars": stars, "topics": topic}
                    if _save_article(EXPLOITS_DIR / "github-poc" / date_str,
                                    f"github-poc/{cve_id}", f"{cve_id} — {repo_name}",
                                    repo_url, desc[:500], tags, date_str, extra):
                        results[cve_id].append({
                            "name": repo_name, "url": repo_url,
                            "stars": stars, "desc": desc[:200]
                        })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  {Fmt.red(f'GitHub API error for {cve_id}: {e}')}", file=sys.stderr)
        time.sleep(1.2)
    return results


# ── Phase 2: CISA KEV Fetcher ──────────────────────────────────────────────
def fetch_cisa_kev() -> int:
    """Fetch and store CISA Known Exploited Vulnerabilities catalog."""
    data = _fetch_url(CISA_KEV_URL)
    if not data:
        return 0
    count = 0
    try:
        catalog = json.loads(data)
        entries = catalog.get("vulnerabilities", [])
        now = datetime.datetime.now()
        for entry in entries:
            cve_id = entry.get("cveID", "")
            date_added = entry.get("dateAdded", now.strftime("%Y-%m-%d"))
            title = f"{cve_id}: {entry.get('vulnerabilityName', '')}"
            vendor = entry.get("vendorProject", "")
            product = entry.get("product", "")
            description = entry.get("shortDescription", "")
            ransomware = entry.get("knownRansomwareCampaignUse", "Unknown")
            required_action = entry.get("requiredAction", "")
            extra = {
                "cve": cve_id,
                "vendor": vendor,
                "product": product,
                "ransomware": ransomware,
                "action": required_action,
            }
            tags = ["KEV", "KnownExploited", f"CVE:{cve_id}"]
            if ransomware.lower() == "known":
                tags.append("Ransomware")
            if _save_article(KEV_DIR / date_added,
                            "cisa-kev", title,
                            f"https://www.cisa.gov/known-exploited-vulnerabilities-catalog/{cve_id}",
                            description, tags, date_added, extra):
                count += 1
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  {Fmt.red(f'CISA KEV parse error: {e}')}", file=sys.stderr)
    return count


# ── Phase 2: Load CISA KEV for cross-referencing ───────────────────────────
def load_kev_cves(days: int = 90) -> set[str]:
    """Return set of CVE IDs in CISA KEV within last N days."""
    cves = set()
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    for fp in KEV_DIR.rglob("*.md"):
        if datetime.datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
            continue
        text = fp.read_text(errors="replace")
        cve_matches = re.findall(r"CVE-\d{4}-\d{4,}", text)
        cves.update(cve_matches)
    return cves


# ── Phase 3: Nuclei Integration ────────────────────────────────────────────
NUCLEI_TEMPLATES_DIR = Path("/root/nuclei-templates")
NUCLEI_RESULTS_DIR = HERE / "nuclei_results"


def _nuclei_has_template(cve_id: str) -> bool:
    """Check if nuclei has a template for a given CVE."""
    if not NUCLEI_TEMPLATES_DIR.exists():
        return False
    year = cve_id.split("-")[1] if cve_id.count("-") >= 2 else ""
    if not year:
        return False
    template_path = NUCLEI_TEMPLATES_DIR / "http" / "cves" / year / f"{cve_id}.yaml"
    headless_path = NUCLEI_TEMPLATES_DIR / "headless" / "cves" / year / f"{cve_id}-HEADLESS.yaml"
    return template_path.exists() or headless_path.exists()


def _nuclei_scan(target_url: str, cve_ids: list[str], timeout: int = 60) -> list[dict]:
    """Run nuclei on a target for a list of CVEs. Returns list of findings."""
    NUCLEI_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    available = [c for c in cve_ids if _nuclei_has_template(c)]
    if not available:
        return []
    template_ids = ",".join(available)
    out_file = NUCLEI_RESULTS_DIR / f"scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(target_url) % 10000}.json"
    try:
        result = subprocess.run(
            ["nuclei", "-u", target_url,
             "-id", template_ids,
             "-json", "-silent",
             "-timeout", str(timeout),
             "-o", str(out_file),
             "-disable-update-check"],
            capture_output=True, text=True, timeout=timeout + 30
        )
        findings = []
        if out_file.exists() and out_file.stat().st_size > 0:
            for line in out_file.read_text().strip().split("\n"):
                if line.strip():
                    try:
                        findings.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return findings
    except subprocess.TimeoutExpired:
        print(f"  {Fmt.yellow(f'  Nuclei scan timed out for {target_url}')}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print(f"  {Fmt.yellow('  nuclei not found in PATH')}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  {Fmt.yellow(f'  Nuclei scan error: {e}')}", file=sys.stderr)
        return []


def scan_targets(target_cve_map: dict[str, list[str]], target_urls: dict[str, str] = None) -> dict[str, list]:
    """Run nuclei scans for targets with matched CVEs."""
    if not target_cve_map:
        return {}
    print(f"\n  {Fmt.bold('Phase 6: Nuclei scanning targets...')}")
    all_findings = {}
    for tname, cves in target_cve_map.items():
        url = (target_urls or {}).get(tname, "")
        if not url:
            print(f"  {Fmt.dim(f'  {tname}: no URL configured, skipping scan')}")
            continue
        print(f"  {Fmt.cyan(f'  Scanning {tname} ({url}) for {len(cves)} CVE(s)...')}")
        findings = _nuclei_scan(url, cves)
        if findings:
            all_findings[tname] = findings
            print(f"    {Fmt.red(f'{len(findings)} finding(s)')}")
            for f in findings[:5]:
                tmpl = f.get("template-id", "?")
                matched = f.get("matched-at", "")
                print(f"      {Fmt.yellow(f'[{tmpl}]')} {Fmt.dim(matched)}")
        else:
            print(f"    {Fmt.green('No findings (or no templates available)')}")
    return all_findings


# ── Phase 3: CVE Scoring Engine (NVD + EPSS) ───────────────────────────────
SCORE_CACHE_DIR = HERE / "cve_scores"

def _nvd_batch(cve_ids: list[str]) -> dict[str, dict]:
    """Fetch CVSS scores from NVD API 2.0. Returns {cve_id: {cvss, severity, cwe, ...}}."""
    results = {}
    if not cve_ids:
        return results
    batch_size = 5
    for i in range(0, len(cve_ids), batch_size):
        batch = cve_ids[i:i + batch_size]
        cve_param = ",".join(batch)
        url = f"{NVD_API}?cveId={cve_param}"
        headers = {}
        if NVD_API_KEY:
            headers["apiKey"] = NVD_API_KEY
        data = _fetch_url(url, headers=headers)
        if data:
            try:
                body = json.loads(data)
                vulns = body.get("vulnerabilities", [])
                for vuln in vulns:
                    cve_data = vuln.get("cve", {})
                    cve_id = cve_data.get("id", "")
                    metrics = cve_data.get("metrics", {})
                    cvss_data = (metrics.get("cvssMetricV31", [{}])[0]
                                 if metrics.get("cvssMetricV31") else
                                 metrics.get("cvssMetricV30", [{}])[0]
                                 if metrics.get("cvssMetricV30") else
                                 metrics.get("cvssMetricV2", [{}])[0]
                                 if metrics.get("cvssMetricV2") else {})
                    base_score = None
                    severity = None
                    vector = None
                    if cvss_data:
                        cvss_obj = cvss_data.get("cvssData", {})
                        base_score = cvss_obj.get("baseScore")
                        severity = cvss_obj.get("baseSeverity", "")
                        vector = cvss_obj.get("vectorString", "")
                    weaknesses = cve_data.get("weaknesses", [])
                    cwes = []
                    for w in weaknesses:
                        for desc in w.get("description", []):
                            val = desc.get("value", "")
                            if val.startswith("CWE-"):
                                cwes.append(val)
                    descriptions = cve_data.get("descriptions", [])
                    desc_text = ""
                    for d in descriptions:
                        if d.get("lang") == "en":
                            desc_text = d.get("value", "")
                            break
                    results[cve_id] = {
                        "cvss": base_score,
                        "severity": severity,
                        "vector": vector or "",
                        "cwes": cwes,
                        "description": desc_text[:500],
                    }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  {Fmt.red(f'NVD parse error: {e}')}", file=sys.stderr)
        time.sleep(1.5)
    return results


def _epss_batch(cve_ids: list[str]) -> dict[str, dict]:
    """Fetch EPSS scores from FIRST.org. Returns {cve_id: {epss, percentile}}."""
    results = {}
    if not cve_ids:
        return results
    for i in range(0, len(cve_ids), 50):
        batch = cve_ids[i:i + 50]
        cve_param = ",".join(batch)
        url = f"{EPSS_API}?cve={cve_param}"
        data = _fetch_url(url)
        if data:
            try:
                body = json.loads(data)
                for item in body.get("data", []):
                    cve_id = item.get("cve", "")
                    results[cve_id] = {
                        "epss": float(item.get("epss", 0)),
                        "percentile": float(item.get("percentile", 0)),
                    }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  {Fmt.red(f'EPSS parse error: {e}')}", file=sys.stderr)
        time.sleep(0.3)
    return results


def _composite_priority(cvss: float | None, epss: float, in_kev: bool, has_poc: bool) -> tuple[int, str]:
    """Calculate composite priority score and label."""
    score = 0
    if cvss is not None:
        if cvss >= 9.0:
            score += 40
        elif cvss >= 7.0:
            score += 30
        elif cvss >= 4.0:
            score += 15
        else:
            score += 5
    if in_kev:
        score += 30
    if epss > 0.5:
        score += 25
    elif epss > 0.1:
        score += 15
    elif epss > 0.01:
        score += 5
    if has_poc:
        score += 10

    if score >= 70:
        label = "CRITICAL"
    elif score >= 50:
        label = "HIGH"
    elif score >= 30:
        label = "MEDIUM"
    elif score >= 15:
        label = "LOW"
    else:
        label = "INFO"
    return score, label


def enrich_cves(cve_ids: list[str], kev_set: set[str] = None,
                poc_set: set[str] = None) -> dict[str, dict]:
    """Full CVE enrichment pipeline: NVD → EPSS → composite score."""
    if not cve_ids:
        return {}
    unique = list(set(cve_ids))
    print(f"  {Fmt.bold('Enriching CVEs with NVD + EPSS...')}")
    print(f"  {Fmt.dim(f'  {len(unique)} unique CVEs to process')}")

    SCORE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = SCORE_CACHE_DIR / "enriched.json"
    cache = {}
    if cache_file.exists():
        try:
            cache = json.loads(cache_file.read_text())
        except (json.JSONDecodeError, OSError):
            cache = {}

    uncached = [c for c in unique if c not in cache]
    if uncached:
        nvd_data = _nvd_batch(uncached)
        epss_data = _epss_batch(uncached)
        for cve_id in uncached:
            nvd = nvd_data.get(cve_id, {})
            epss = epss_data.get(cve_id, {})
            cache[cve_id] = {
                "cvss": nvd.get("cvss"),
                "severity": nvd.get("severity", ""),
                "vector": nvd.get("vector", ""),
                "cwes": nvd.get("cwes", []),
                "description": nvd.get("description", ""),
                "epss": epss.get("epss", 0),
                "epss_percentile": epss.get("percentile", 0),
            }
        try:
            cache_file.write_text(json.dumps(cache, indent=2))
        except OSError:
            pass

    enriched = {}
    for cve_id in unique:
        info = cache.get(cve_id, {})
        has_poc = cve_id in (poc_set or set())
        in_kev = cve_id in (kev_set or set())
        pri_score, pri_label = _composite_priority(
            info.get("cvss"), info.get("epss", 0), in_kev, has_poc
        )
        enriched[cve_id] = {
            **info,
            "priority_score": pri_score,
            "priority_label": pri_label,
            "in_kev": in_kev,
            "has_poc": has_poc,
        }
    return enriched


# ── Phase 3: Target Tech Stack Registry ────────────────────────────────────
def load_targets() -> dict:
    """Load targets.yaml. Returns {name: {techs: [...], keywords: [...]}}."""
    if not TARGETS_FILE.exists():
        return {}
    try:
        import yaml
        with open(TARGETS_FILE) as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass
    try:
        text = TARGETS_FILE.read_text()
        return json.loads(text) if text.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_target(name: str, techs: list[str], keywords: list[str], url: str = ""):
    """Add or update a target in targets.yaml."""
    targets = load_targets()
    entry = {"techs": techs, "keywords": keywords}
    if url:
        entry["url"] = url
    targets[name] = entry
    try:
        import yaml
        with open(TARGETS_FILE, "w") as f:
            yaml.dump(targets, f, default_flow_style=False, sort_keys=False)
    except ImportError:
        TARGETS_FILE.write_text(json.dumps(targets, indent=2))
    print(f"  {Fmt.green(f'Saved target: {name}')}")


def list_targets():
    """Display registered targets."""
    targets = load_targets()
    if not targets:
        print(f"  {Fmt.dim('No targets registered. Use --target-add to add one.')}")
        return
    print(f"\n  {Fmt.bold(f'Registered Targets ({len(targets)})')}")
    print(Fmt.hr())
    for name, info in sorted(targets.items()):
        techs = info.get("techs", [])
        kw = info.get("keywords", [])
        t_str = ", ".join(techs) if techs else "—"
        kw_str = ", ".join(kw) if kw else "—"
        print(f"  {Fmt.green(name)}")
        print(f"    techs:    {Fmt.dim(t_str)}")
        print(f"    keywords: {Fmt.dim(kw_str)}")
    print()


# ── Phase 3: CVE → Target Matching ─────────────────────────────────────────
def match_target_cves(targets: dict, cves: list[str]) -> dict[str, list[str]]:
    """Check which CVEs affect which targets. Returns {target_name: [matching_cves]}."""
    if not targets or not cves:
        return {}
    result = {}
    for cve_id in cves:
        cve_lower = cve_id.lower()
        for tname, tinfo in targets.items():
            keywords = [k.lower() for k in tinfo.get("keywords", [])]
            techs = [k.lower() for k in tinfo.get("techs", [])]
            all_kw = keywords + techs
            if not all_kw:
                continue
            for kw in all_kw:
                if kw in cve_lower:
                    result.setdefault(tname, []).append(cve_id)
                    break
    return result


# ── Phase 3+4: Hunting Brief Generator ────────────────────────────────────
def collect_news_cves(news_dir: Path, days: int = 1) -> set[str]:
    """Extract all CVEs from news articles within N days."""
    all_cves = set()
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    for fp in news_dir.rglob("*.md"):
        if fp.name.startswith("."):
            continue
        if datetime.datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
            continue
        text = fp.read_text(errors="replace")
        all_cves.update(_cves_from_text(text))
    return all_cves


def collect_exploit_pocs(exploit_dir: Path, days: int = 7) -> dict:
    """Collect PoCs from exploit storage. Returns {cve_or_source: [poc_info]}."""
    pocs = {}
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    for fp in exploit_dir.rglob("*.md"):
        if fp.name.startswith("."):
            continue
        if datetime.datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
            continue
        text = fp.read_text(errors="replace")
        title_m = re.search(r'title:\s*"(.+)"', text)
        source_m = re.search(r'source:\s*"(.+)"', text)
        url_m = re.search(r'url:\s*"(.+)"', text)
        cves = _cves_from_text(text)
        info = {
            "file": str(fp.relative_to(exploit_dir)),
            "title": title_m.group(1) if title_m else fp.stem,
            "source": source_m.group(1) if source_m else "?",
            "url": url_m.group(1) if url_m else "",
        }
        if cves:
            for cve_id in cves:
                pocs.setdefault(cve_id, []).append(info)
        else:
            source = source_m.group(1) if source_m else "unknown"
            pocs.setdefault(source, []).append(info)
    return pocs


def load_techniques(techniques_dir: Path) -> dict[str, list[str]]:
    """Index techniques by keywords for CVE→technique linking."""
    index = {}
    if not techniques_dir.exists():
        return index
    for fp in techniques_dir.rglob("*.md"):
        text = fp.read_text(errors="replace")
        tags_match = re.search(r'tags:\s*\[(.+)\]', text)
        if not tags_match:
            continue
        tags = [t.strip().lower() for t in tags_match.group(1).split(",")]
        title = re.search(r'title:\s*"(.+)"', text)
        title_str = title.group(1) if title else fp.stem
        for tag in tags:
            index.setdefault(tag, []).append(title_str)
    return index


def generate_hunting_brief(news_dir: Path, exploit_dir: Path,
                           techniques_dir: Path = None,
                           targets: dict = None, days: int = 1):
    """Generate a prioritized hunting brief for today."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print(Fmt.banner(f"HUNTING BRIEF — {today}"))

    # Step 1: Collect news CVEs
    print(f"  {Fmt.bold('Phase 1: Scanning news for CVEs...')}")
    news_cves = collect_news_cves(news_dir, days)
    if not news_cves:
        print(f"  {Fmt.dim('  No CVEs found in recent news.')}")
    else:
        print(f"  {Fmt.green(f'  {len(news_cves)} unique CVEs found')}")

    # Step 2: Check CISA KEV (actively exploited)
    print(f"\n  {Fmt.bold('Phase 2: Cross-referencing CISA KEV...')}")
    kev_cves = load_kev_cves(days=90)
    active_cves = news_cves & kev_cves
    if active_cves:
        print(f"  {Fmt.red(f'  ⚠ {len(active_cves)} CVEs actively exploited in the wild!')}")
    else:
        print(f"  {Fmt.dim('  No news CVEs found in CISA KEV catalog.')}")

    # Step 3: Fetch PoCs for news CVEs
    print(f"\n  {Fmt.bold('Phase 3: Enriching with PoC intel...')}")
    today_cves = list(news_cves)
    gh_results = {}
    if today_cves:
        try:
            gh_results = fetch_github_pocs(today_cves)
            if gh_results:
                for cve_id, repos in gh_results.items():
                    print(f"  {Fmt.green(f'  GitHub PoCs for {cve_id}: {len(repos)} repo(s)')}")
        except Exception as e:
            print(f"  {Fmt.yellow(f'  GitHub search skipped: {e}')}")

    # Step 4: Check existing PoCs in store
    existing_pocs = collect_exploit_pocs(exploit_dir, days=7)
    poc_map = {}
    for cve_id, poc_list in existing_pocs.items():
        if cve_id in news_cves:
            poc_map[cve_id] = poc_list

    # Step 5: Target matching
    print(f"\n  {Fmt.bold('Phase 4: Target matching...')}")
    target_cve_map = {}
    if targets:
        for tname, tinfo in targets.items():
            matched = []
            for cve_id in news_cves:
                cve_lower = cve_id.lower()
                for kw in [k.lower() for k in tinfo.get("keywords", []) + tinfo.get("techs", [])]:
                    if kw in cve_lower:
                        matched.append(cve_id)
                        break
            if matched:
                target_cve_map[tname] = matched
                print(f"  {Fmt.green(f'  {tname}: {len(matched)} matching CVE(s)')}")

    # ── Enrich with NVD + EPSS ──
    print(f"\n  {Fmt.bold('Phase 5: CVE enrichment (NVD CVSS + EPSS)...')}")
    enriched = enrich_cves(list(news_cves), kev_cves,
                           set(list(poc_map.keys()) | set(gh_results.keys())))

    # ── Nuclei Scan ──
    target_urls = {}
    if targets:
        target_urls = {n: t.get("url", "") for n, t in targets.items() if t.get("url")}
    nuclei_findings = scan_targets(target_cve_map, target_urls)

    # ── Final Brief ──
    print(f"\n{Fmt.hr('\u2550', 70)}")
    print(f"  {Fmt.bold(Fmt.red(' PRIORITY HUNTING LIST '))}")
    print(Fmt.hr('\u2550', 70))

    prioritized = []
    for cve_id in news_cves:
        info = enriched.get(cve_id, {})
        score = info.get("priority_score", 0)
        label = info.get("priority_label", "INFO")
        reasons = []
        if cve_id in active_cves:
            reasons.append("ACTIVELY EXPLOITED")
        if cve_id in poc_map or cve_id in gh_results:
            reasons.append("PoC AVAILABLE")
        cvss = info.get("cvss")
        if cvss is not None:
            reasons.append(f"CVSS {cvss}")
        epss = info.get("epss", 0)
        if epss > 0.01:
            reasons.append(f"EPSS {epss:.3f}")
        affected_targets = [t for t, cves in target_cve_map.items() if cve_id in cves]
        if affected_targets:
            reasons.append(f"TARGET: {', '.join(affected_targets)}")
        prioritized.append((score, cve_id, label, reasons, info))

    prioritized.sort(key=lambda x: x[0], reverse=True)

    if not prioritized:
        print(f"  {Fmt.dim('No actionable CVEs today.')}")
    else:
        for pri, cve_id, label_str, reasons, info in prioritized:
            if label_str == "CRITICAL":
                label = Fmt.red(label_str)
            elif label_str == "HIGH":
                label = Fmt.yellow(label_str)
            elif label_str == "MEDIUM":
                label = Fmt.blue(label_str)
            elif label_str == "LOW":
                label = Fmt.dim(label_str)
            else:
                label = Fmt.dim(label_str)
            r_str = f" [{', '.join(reasons)}]" if reasons else ""
            poc_note = ""
            if cve_id in poc_map:
                poc_note = f" {Fmt.url(poc_map[cve_id][0]['file'])}"
            elif cve_id in gh_results:
                poc_note = f" {Fmt.url(gh_results[cve_id][0]['url'])}"
            desc = info.get("description", "")
            desc_short = f" — {desc[:120]}..." if desc else ""
            print(f"\n  [{label}] {Fmt.bold(cve_id)}{poc_note}")
            print(f"          Score: {pri} | CVSS: {info.get('cvss', 'N/A')} | EPSS: {info.get('epss', 0):.4f} | KEV: {info.get('in_kev', False)}")
            print(f"          {Fmt.dim(r_str)}{Fmt.dim(desc_short)}")

    # ── Generate Exploit Briefs ──
    print(f"\n  {Fmt.bold('Phase 7: Generating exploit briefs...')}")
    try:
        from gpt_briefs import generate_all_briefs
        briefed = generate_all_briefs(enriched, poc_map, nuclei_findings, target_cve_map)
        if briefed:
            print(f"  {Fmt.green(f'  {len(briefed)} exploit brief(s) generated')}")
        else:
            print(f"  {Fmt.dim('  No CVEs above threshold for briefs')}")
    except ImportError:
        print(f"  {Fmt.dim('  gpt_briefs.py not found, skipping')}")
    except Exception as e:
        print(f"  {Fmt.yellow(f'  Brief generation error: {e}')}")

    # ── Technique Links ──
    if techniques_dir and techniques_dir.exists():
        techniques = load_techniques(techniques_dir)
        print(f"\n  {Fmt.bold('Related Techniques')}")
        print(f"  {Fmt.dim('(check techniques directory for relevant writeups)')}")
        tech_tags = set()
        for cve_id in news_cves:
            parts = cve_id.split("-")
            year = parts[1] if len(parts) > 1 else ""
            for tag in techniques:
                if year and year in tag:
                    tech_tags.add(tag)
        if tech_tags:
            for tag in sorted(tech_tags)[:10]:
                print(f"    {Fmt.magenta(tag)}")

    print(f"\n{Fmt.hr('\u2550', 70)}")
    print(f"  {Fmt.dim('Run: cyassist --hunt to refresh. Use --auto for daily cron.')}")


# ── Phase 4: Auto Run ──────────────────────────────────────────────────────
def auto_run(news_dir: Path, exploit_dir: Path, techniques_dir: Path = None):
    """Silent automated pipeline for cron. Saves brief to file."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    brief_dir = HERE / "briefs"
    brief_dir.mkdir(parents=True, exist_ok=True)
    brief_file = brief_dir / f"hunting-brief-{today}.md"
    targets = load_targets()

    # Collect
    fetch_exploitdb()
    fetch_packetstorm()
    news_cves = collect_news_cves(news_dir, 1)
    gh_results = fetch_github_pocs(list(news_cves))
    brief_cves = news_cves

    # Generate markdown brief
    lines = [f"# Hunting Brief — {today}", ""]
    kev_cves = load_kev_cves(90)
    active = brief_cves & kev_cves
    if active:
        lines.append(f"## ⚠ Actively Exploited ({len(active)})")
        for c in sorted(active):
            lines.append(f"- {c}")
        lines.append("")

    existing_pocs = collect_exploit_pocs(exploit_dir, 7)
    poc_set = set(list(existing_pocs.keys()) | set(gh_results.keys()))
    with_poc = [c for c in brief_cves if c in existing_pocs or c in gh_results]
    if with_poc:
        lines.append(f"## PoC Available ({len(with_poc)})")
        for c in sorted(with_poc):
            lines.append(f"- {c}")
        lines.append("")

    target_map = match_target_cves(targets, list(brief_cves))
    if target_map:
        lines.append("## Target-Affecting CVEs")
        for tname, cves in target_map.items():
            lines.append(f"- {tname}: {', '.join(cves)}")
        lines.append("")

    enriched = enrich_cves(list(brief_cves), kev_cves, poc_set)
    if enriched:
        lines.append("## Enriched CVEs (CVSS + EPSS + Priority)")
        sorted_cves = sorted(enriched.items(), key=lambda x: x[1].get("priority_score", 0), reverse=True)
        for cve_id, info in sorted_cves:
            pri_label = info.get("priority_label", "INFO")
            cvss = info.get("cvss", "N/A")
            epss = info.get("epss", 0)
            kev = "✓" if info.get("in_kev") else ""
            desc = info.get("description", "")[:200]
            lines.append(f"- **{cve_id}** [{pri_label}] CVSS:{cvss} EPSS:{epss:.4f} KEV:{kev}")
            if desc:
                lines.append(f"  - {desc}")
        lines.append("")

    if brief_cves:
        lines.append(f"## All CVEs in Today's News ({len(brief_cves)})")
        for c in sorted(brief_cves):
            lines.append(f"- {c}")
        lines.append("")
    else:
        lines.append("_No CVEs found in today's news._")

    brief_file.write_text("\n".join(lines))
    print(f"  {Fmt.green(f'Brief saved: {brief_file}')}")

    try:
        from notifier import alert_critical
        alert_critical(enriched, target_map, str(brief_file))
    except ImportError:
        pass


# ── Phase 8: CVE Deep Research ──────────────────────────────────────────────
ADDITIONAL_FEEDS = {
    "the-hacker-news": "https://feeds.feedburner.com/TheHackersNews",
    "msrc": "https://msrc.microsoft.com/update-guide/rss",
    "project-zero": "https://googleprojectzero.blog/feed/",
    "rapid7": "https://blog.rapid7.com/feed/",
    "qualys": "https://blog.qualys.com/feed",
    "sans-newsbites": "https://www.sans.org/newsletters/newsbites/rss/",
    "portswigger": "https://portswigger.net/research/rss",
    "detectify": "https://detectify.com/blog/feed.xml",
    "assetnote": "https://assetnote.io/feed.xml",
    "projectdiscovery": "https://projectdiscovery.io/blog/rss",
}
NITTER_INSTANCE = "https://nitter.net"
X_FEEDS = {
    "x-vxunderground": f"{NITTER_INSTANCE}/vxunderground/rss",
    "x-pwntwitter": f"{NITTER_INSTANCE}/PwnAllTheThings/rss",
    "x-binitamshah": f"{NITTER_INSTANCE}/binitamshah/rss",
    "x-securityweek": f"{NITTER_INSTANCE}/SecurityWeek/rss",
    "x-thedfirreport": f"{NITTER_INSTANCE}/TheDFIRReport/rss",
    "x-0xor0ne": f"{NITTER_INSTANCE}/0xor0ne/rss",
    "x-ghostsecurity": f"{NITTER_INSTANCE}/ghost_security_/rss",
}
MEDIUM_FEEDS = {
    "medium-cybersecurity": "https://medium.com/feed/tag/cybersecurity",
    "medium-bugbounty": "https://medium.com/feed/tag/bug-bounty",
    "medium-infosec": "https://medium.com/feed/tag/infosec",
    "medium-pentest": "https://medium.com/feed/tag/penetration-testing",
    "medium-exploit": "https://medium.com/feed/tag/exploit",
    "medium-vulnerability": "https://medium.com/feed/tag/vulnerability",
    "medium-hacking": "https://medium.com/feed/tag/hacking",
}
NITTER_FALLBACK_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.1d4.us",
    "https://nitter.nl",
]
X_FEEDS_FLAT = dict(X_FEEDS)
MEDIUM_FEEDS_FLAT = dict(MEDIUM_FEEDS)
LINKEDIN_FEEDS = {
    "linkedin-cybersecurity": "https://news.google.com/rss/search?q=site:linkedin.com+cybersecurity&hl=en-US&gl=US&ceid=US:en",
    "linkedin-infosec": "https://news.google.com/rss/search?q=site:linkedin.com+infosec&hl=en-US&gl=US&ceid=US:en",
    "linkedin-bugbounty": "https://news.google.com/rss/search?q=site:linkedin.com+bug+bounty&hl=en-US&gl=US&ceid=US:en",
}
ALL_FEEDS = {**ADDITIONAL_FEEDS, **X_FEEDS_FLAT, **MEDIUM_FEEDS_FLAT, **LINKEDIN_FEEDS}


def _opencode_summarize(prompt: str, timeout: int = 60) -> Optional[str]:
    """Use opencode's LLM for AI summarization (no extra API keys needed)."""
    try:
        result = subprocess.run(
            ["opencode", "run", prompt],
            capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout or result.stderr or ""
        return output.strip() or None
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def _web_search_cve(cve_id: str) -> list[dict]:
    """Search the web for a CVE using available tools."""
    results = []
    urls_to_try = [
        f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        f"https://www.cve.org/CVERecords?id={cve_id}",
        f"https://packetstormsecurity.com/search/?q={cve_id}",
        f"https://www.exploit-db.com/search?cve={cve_id}",
    ]
    for url in urls_to_try:
        data = _fetch_url(url, timeout=10)
        if data:
            results.append({"url": url, "source": "web", "size": len(data)})
    return results


def research_cve(cve_id: str, news_dir: Path = None):
    """Deep research on a single CVE across all intel sources."""
    print(Fmt.banner(f"CVE DEEP RESEARCH", cve_id))

    # 1. NVD + EPSS
    print(f"\n  {Fmt.bold('1. NVD Enrichment')}")
    enriched = enrich_cves([cve_id])
    info = enriched.get(cve_id, {})
    if info:
        cvss = info.get("cvss", "N/A")
        severity = info.get("severity", "N/A")
        epss = info.get("epss", 0)
        cwes = info.get("cwes", [])
        desc = info.get("description", "")
        print(f"    CVSS: {Fmt.yellow(str(cvss))} ({severity})")
        print(f"    EPSS: {Fmt.yellow(f'{epss:.4f}')}")
        if cwes:
            print(f"    CWEs: {Fmt.cyan(', '.join(cwes))}")
        if desc:
            print(f"    Description: {Fmt.dim(desc[:300])}")

    # 2. CISA KEV check
    print(f"\n  {Fmt.bold('2. CISA KEV Status')}")
    kev_cves = load_kev_cves(9999)
    if cve_id in kev_cves:
        print(f"    {Fmt.red('⚠ IN CISA KEV — actively exploited in the wild')}")
        for fp in KEV_DIR.rglob("*.md"):
            if cve_id in fp.read_text():
                rw = re.search(r'ransomware:\s*(\S+)', fp.read_text())
                if rw and rw.group(1).lower() == "known":
                    print(f"    {Fmt.red('  Ransomware campaign use: KNOWN')}")
                break
    else:
        print(f"    {Fmt.dim('Not in CISA KEV catalog')}")

    # 3. GitHub PoCs
    print(f"\n  {Fmt.bold('3. GitHub PoC Repositories')}")
    gh_results = fetch_github_pocs([cve_id])
    if gh_results and cve_id in gh_results:
        for r in gh_results[cve_id]:
            print(f"    ★{r['stars']} {Fmt.green(r['name'])}  {Fmt.url(r['url'])}")
            if r['desc']:
                print(f"      {Fmt.dim(r['desc'][:200])}")
    else:
        print(f"    {Fmt.dim('No GitHub PoCs found')}")

    # 4. Local PoC storage
    print(f"\n  {Fmt.bold('4. Local PoC Storage')}")
    pocs = collect_exploit_pocs(EXPLOITS_DIR, days=999)
    if cve_id in pocs:
        for p in pocs[cve_id]:
            print(f"    {Fmt.cyan(p['source'])}  {Fmt.url(p['url'])}  {Fmt.dim(p['file'])}")
    else:
        print(f"    {Fmt.dim('No local PoCs for this CVE')}")

    # 5. News mentions
    print(f"\n  {Fmt.bold('5. News Mentions')}")
    if news_dir and news_dir.exists():
        mentions = []
        for fp in news_dir.rglob("*.md"):
            if cve_id in fp.read_text():
                title_m = re.search(r'title:\s*"(.+)"', fp.read_text(errors="replace"))
                mentions.append((fp, title_m.group(1) if title_m else fp.stem))
        if mentions:
            for fp, title in mentions[:10]:
                print(f"    {Fmt.dim(fp.parent.name)}  {title}")
        else:
            print(f"    {Fmt.dim('No news mentions')}")

    # 6. Web results
    print(f"\n  {Fmt.bold('6. Web Results')}")
    web_results = _web_search_cve(cve_id)
    for r in web_results[:5]:
        print(f"    {Fmt.url(r['url'])} ({r['size']} bytes)")

    # 7. AI summary via opencode
    print(f"\n  {Fmt.bold('7. AI Summary')}")
    desc_text = info.get("description", "")[:500]
    poc_text = ""
    if gh_results and cve_id in gh_results:
        poc_text = "\n".join(f"- {r['name']}: {r['url']} (★{r['stars']})" for r in gh_results[cve_id][:3])
    ai_prompt = f"Summarize this vulnerability for a bug bounty hunter in 3-4 sentences: CVE {cve_id}. CVSS {info.get('cvss', 'N/A')} ({info.get('severity', 'N/A')}). EPSS probability of exploitation: {info.get('epss', 0):.4f}. {'In CISA KEV (actively exploited).' if cve_id in kev_cves else ''} Description: {desc_text[:300]}. PoCs available: {poc_text[:200] or 'None found yet.'}. What should a hunter look for?"
    ai_result = _opencode_summarize(ai_prompt)
    if ai_result:
        print(f"    {Fmt.green(ai_result[:500])}")
    else:
        print(f"    {Fmt.dim('AI summary unavailable (opencode subprocess failed)')}")

    # 8. Brief write
    brief_path = BRIEFS_DIR / f"research-{cve_id}-{datetime.datetime.now().strftime('%Y%m%d')}.md"
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    brief_lines = [
        f"# CVE Research: {cve_id}",
        f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**CVSS:** {info.get('cvss', 'N/A')} ({info.get('severity', 'N/A')})",
        f"**EPSS:** {info.get('epss', 0):.4f}",
        f"**CISA KEV:** {'YES' if cve_id in kev_cves else 'No'}",
        f"**CWEs:** {', '.join(info.get('cwes', []))}",
        f"**Description:** {desc}",
        "",
        "## GitHub PoCs",
        poc_text or "None found",
        "",
        "## References",
    ]
    for r in web_results:
        brief_lines.append(f"- {r['url']}")
    brief_path.write_text("\n".join(brief_lines))
    print(f"\n  {Fmt.green(f'Brief saved: {brief_path}')}")
    return info


def firehose(news_dir: Path, days: int = 7):
    """Unfiltered intel dump — every CVE, PoC, KEV entry with no priority filtering."""
    print(Fmt.banner("INTEL FIREHOSE", f"Last {days} days — unfiltered"))

    # News CVEs
    print(f"\n  {Fmt.bold('All CVEs in News')}")
    all_cves = collect_news_cves(news_dir, days)
    if all_cves:
        for c in sorted(all_cves):
            print(f"    {Fmt.cve(c)}")
    else:
        print(f"    {Fmt.dim('No CVEs found')}")

    # All PoCs
    print(f"\n  {Fmt.bold('All PoCs')}")
    pocs = collect_exploit_pocs(EXPLOITS_DIR, days)
    if pocs:
        total = sum(len(v) for v in pocs.values())
        print(f"    {Fmt.dim(f'{total} entries across {len(pocs)} CVE/sources')}")
        seen = set()
        for key, items in sorted(pocs.items()):
            for item in items:
                if item['file'] in seen: continue
                seen.add(item['file'])
                label = Fmt.cve(key) if key.startswith("CVE") else Fmt.cyan(f"[{key}]")
                print(f"    {Fmt.bold(item['title'][:80])}")
                print(f"      {label}  {Fmt.dim(item['source'])}")
    else:
        print(f"    {Fmt.dim('No PoCs')}")

    # All KEV
    print(f"\n  {Fmt.bold('All CISA KEV Entries (last 90 days)')}")
    kev = load_kev_cves(90)
    if kev:
        for c in sorted(kev):
            print(f"    {Fmt.red(c)}")
    else:
        print(f"    {Fmt.dim('No KEV entries')}")

    # All targets matched
    print(f"\n  {Fmt.bold('Target Matches')}")
    targets = load_targets()
    if targets:
        for tname, tinfo in targets.items():
            matched = [c for c in all_cves if any(kw.lower() in c.lower() for kw in tinfo.get("keywords", []) + tinfo.get("techs", []))]
            if matched:
                print(f"    {Fmt.green(tname)}: {', '.join(matched)}")

    print(f"\n{Fmt.hr()}")


def watch_mode(news_dir: Path, interval: int = 300):
    """Continuous monitoring mode — checks for new intel every N seconds."""
    print(Fmt.banner("WATCH MODE", f"Checking every {interval}s — Ctrl+C to stop"))
    seen_cves = set()
    try:
        while True:
            cves = collect_news_cves(news_dir, days=1)
            new_cves = cves - seen_cves
            if new_cves:
                print(f"\n  {Fmt.green(f'[{datetime.datetime.now():%H:%M:%S}] {len(new_cves)} new CVE(s)')}")
                for c in sorted(new_cves):
                    print(f"    {Fmt.cve(c)}")
                    enriched = enrich_cves([c])
                    if enriched.get(c, {}).get("priority_score", 0) >= 50:
                        print(f"      {Fmt.red('⚠ HIGH PRIORITY')}")
                    seen_cves.add(c)
            else:
                print(f"  {Fmt.dim(f'[{datetime.datetime.now():%H:%M:%S}] No new CVEs')}", end="\r")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n  {Fmt.yellow('Watch mode stopped.')}")


def fetch_additional_feeds(max_items: int = 10) -> int:
    """Fetch from additional RSS sources for broader CVE coverage."""
    count = 0
    news_dir = HERE / "news" / "rss"
    for name, url in ALL_FEEDS.items():
        data = None
        if name.startswith("x-"):
            data = _fetch_url(url, timeout=15)
            if not data:
                for fallback in NITTER_FALLBACK_INSTANCES:
                    alt_url = url.replace(NITTER_INSTANCE, fallback)
                    data = _fetch_url(alt_url, timeout=10)
                    if data:
                        break
        else:
            data = _fetch_url(url, timeout=15)
        if not data:
            continue
        try:
            text_data = data.decode("utf-8", errors="replace")
            entries = re.findall(r'<entry\b[^>]*>(.*?)</entry>', text_data, re.DOTALL) or \
                      re.findall(r'<item\b[^>]*>(.*?)</item>', text_data, re.DOTALL)
            for entry_xml in entries[:max_items]:
                title_m = re.search(r'<title[^>]*>(.*?)</title>', entry_xml, re.DOTALL)
                link_m = re.search(r'<link[^>]*href="([^"]+)"', entry_xml) or \
                         re.search(r'<link[^>]*>(.*?)</link>', entry_xml)
                pub_m = re.search(r'<published[^>]*>(.*?)</published>', entry_xml) or \
                        re.search(r'<pubDate[^>]*>(.*?)</pubDate>', entry_xml)
                title = title_m.group(1).strip() if title_m else ""
                link = link_m.group(1).strip() if link_m else ""
                pub = pub_m.group(1).strip()[:10] if pub_m else ""
                date_str = pub or datetime.datetime.now().strftime("%Y-%m-%d")
                cves = _cves_from_text(title)
                tags = [name] + [f"CVE:{c}" for c in cves[:3]]
                if _save_article(news_dir / name / date_str, name, title, link, "", tags, date_str):
                    count += 1
        except Exception as e:
            print(f"  {Fmt.red(f'Feed {name} parse error: {e}')}", file=sys.stderr)
    return count


# ── CLI ─────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Cyassist hunter engine")
    p.add_argument("--hunt", action="store_true", help="Full hunting pipeline")
    p.add_argument("--poc", action="store_true", help="Show today's PoCs")
    p.add_argument("--poc-fetch", action="store_true", help="Fetch new PoCs")
    p.add_argument("--kev", action="store_true", help="Show CISA KEV catalog")
    p.add_argument("--kev-fetch", action="store_true", help="Fetch CISA KEV")
    p.add_argument("--auto", action="store_true", help="Silent daily auto-run")
    p.add_argument("--cve", metavar="CVE-ID", help="Enrich a specific CVE")
    p.add_argument("--targets", action="store_true", help="List targets")
    p.add_argument("--target-add", nargs="+", metavar="NAME TECHS KW [URL]",
                   help="Add target: NAME TECHs KEYWORDS [URL]")
    p.add_argument("--setup-telegram", nargs=2, metavar=("TOKEN", "CHAT_ID"),
                   help="Configure Telegram bot for alerts")
    p.add_argument("--setup-discord", metavar="WEBHOOK_URL",
                   help="Configure Discord webhook for alerts")
    p.add_argument("--test-alert", action="store_true",
                   help="Send a test notification")
    p.add_argument("--dashboard", action="store_true",
                   help="Launch web dashboard")
    p.add_argument("--dashboard-port", type=int, default=8080,
                   help="Dashboard port (default: 8080)")
    p.add_argument("--research", metavar="CVE-ID",
                   help="Deep research on a specific CVE across all intel sources")
    p.add_argument("--firehose", action="store_true",
                   help="Unfiltered intel dump — every CVE, PoC, KEV with no filtering")
    p.add_argument("--watch", action="store_true",
                   help="Continuous monitoring — polls for new CVEs every N seconds")
    p.add_argument("--watch-interval", type=int, default=300,
                   help="Watch mode polling interval in seconds (default: 300)")
    p.add_argument("--feeds-fetch", action="store_true",
                   help="Fetch from additional RSS sources (THN, MSRC, Project Zero, etc.)")
    p.add_argument("--brief", metavar="CVE-ID",
                   help="Generate AI-summarized exploitation brief for a CVE")
    p.add_argument("--news-dir", default=str(HERE / "news"),
                   help="News directory (default: cyassist/news)")

    args = p.parse_args()
    news_dir = Path(args.news_dir)
    techniques_dir = HERE.parent / "bugbounty-config" / "techniques"

    if args.setup_telegram:
        try:
            from notifier import setup_telegram
            setup_telegram(*args.setup_telegram)
        except ImportError:
            print(f"  {Fmt.red('notifier.py not found')}", file=sys.stderr)
        return

    if args.setup_discord:
        try:
            from notifier import setup_discord
            setup_discord(args.setup_discord)
        except ImportError:
            print(f"  {Fmt.red('notifier.py not found')}", file=sys.stderr)
        return

    if args.test_alert:
        try:
            from notifier import send_telegram, send_discord
            msg = "Cyassist test alert — hunter pipeline operational."
            tg = send_telegram(msg)
            dc = send_discord(msg)
            print(f"  Telegram: {'OK' if tg else 'SKIP'}")
            print(f"  Discord:  {'OK' if dc else 'SKIP'}")
        except ImportError:
            print(f"  {Fmt.red('notifier.py not found')}", file=sys.stderr)
        return

    if args.target_add:
        parts = args.target_add
        name = parts[0]
        techs = [t.strip() for t in parts[1].split(",") if t.strip()]
        kw = [k.strip() for k in parts[2].split(",") if k.strip()]
        url = parts[3] if len(parts) > 3 else ""
        save_target(name, techs, kw, url)
        return

    if args.targets:
        list_targets()
        return

    if args.poc_fetch:
        print(f"  Fetching exploit-db...")
        edb = fetch_exploitdb()
        print(f"  Fetching packetstorm...")
        ps = fetch_packetstorm()
        print(f"  {Fmt.green(f'Done: {edb} exploit-db, {ps} packetstorm')}")
        return

    if args.kev_fetch:
        print(f"  Fetching CISA KEV...")
        k = fetch_cisa_kev()
        print(f"  {Fmt.green(f'Done: {k} new KEV entries')}")
        return

    if args.poc:
        pocs = collect_exploit_pocs(EXPLOITS_DIR, days=7)
        if not pocs:
            print(f"  {Fmt.dim('No PoCs from last 7 days.')}")
            return
        total = sum(len(v) for v in pocs.values())
        print(Fmt.banner(f"PoC INTEL", f"{total} entries"))
        seen = set()
        for key, items in sorted(pocs.items()):
            for item in items:
                if item['file'] in seen:
                    continue
                seen.add(item['file'])
                label = Fmt.cve(key) if key.startswith("CVE") else Fmt.cyan(f"[{key}]")
                print(f"  {Fmt.bold(item['title'])}")
                print(f"    {label}  {Fmt.dim(item['source'])}  {Fmt.url(item['url']) if item['url'] else ''}")
        return

    if args.kev:
        kev = load_kev_cves(days=90)
        if not kev:
            print(f"  {Fmt.dim('No CISA KEV entries. Fetch with --kev-fetch.')}")
            return
        print(Fmt.banner("CISA KEV CATALOG", f"{len(kev)} CVEs (last 90 days)"))
        for fp in sorted(KEV_DIR.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
            text = fp.read_text(errors="replace")
            title_m = re.search(r'title:\s*"(.+)"', text)
            cve_m = re.search(r'cve:\s*(\S+)', text)
            rw_m = re.search(r'ransomware:\s*(\S+)', text)
            title = title_m.group(1) if title_m else fp.stem
            cve_id = cve_m.group(1) if cve_m else "?"
            rw = rw_m.group(1) if rw_m else ""
            rw_tag = f" {Fmt.red('[RANSOMWARE]')}" if rw and rw.lower() == "known" else ""
            print(f"  {Fmt.cve(cve_id)} {Fmt.bold(title)}{rw_tag}")
        return

    if args.cve:
        results = fetch_github_pocs([args.cve])
        if results:
            for cve_id, repos in results.items():
                print(f"\n  {Fmt.cve(cve_id)} — GitHub PoCs:")
                for r in repos:
                    print(f"    ★{r['stars']} {Fmt.bold(r['name'])}  {Fmt.url(r['url'])}")
                    if r['desc']:
                        print(f"      {Fmt.dim(r['desc'])}")
        else:
            print(f"  {Fmt.dim(f'No GitHub PoCs found for {args.cve}')}")
        return

    if args.research:
        research_cve(args.research.upper(), news_dir)
        return

    if args.firehose:
        firehose(news_dir, days=7)
        return

    if args.watch:
        watch_mode(news_dir, interval=args.watch_interval)
        return

    if args.feeds_fetch:
        print(f"  Fetching additional RSS sources...")
        n = fetch_additional_feeds()
        print(f"  {Fmt.green(f'Done: {n} new articles from {len(ALL_FEEDS)} sources')}")
        return

    if args.brief:
        enriched = enrich_cves([args.brief.upper()])
        info = enriched.get(args.brief.upper(), {})
        gh_results = fetch_github_pocs([args.brief.upper()])
        poc_repos = gh_results.get(args.brief.upper(), [])
        try:
            from gpt_briefs import generate_exploit_brief
            brief = generate_exploit_brief(args.brief.upper(), info, poc_repos=poc_repos)
        except ImportError:
            brief = f"# {args.brief.upper()} — Exploitation Brief\n\nNo AI brief module available."
        print(f"\n{brief[:2000]}")
        return

    if args.dashboard:
        try:
            from dashboard.app import run_dashboard
            run_dashboard(args.dashboard_port)
        except ImportError:
            PORT = args.dashboard_port
            print(f"  {Fmt.green(f'Launching dashboard on http://127.0.0.1:{PORT}...')}")
            sys.stdout.flush()
            os.execvp(sys.executable, [sys.executable, "-m", "dashboard.app", "--port", str(PORT)])
        return

    if args.auto:
        auto_run(news_dir, EXPLOITS_DIR, techniques_dir if techniques_dir.exists() else None)
        return

    if args.hunt:
        targets = load_targets()
        generate_hunting_brief(news_dir, EXPLOITS_DIR,
                               techniques_dir if techniques_dir.exists() else None,
                               targets, days=1)
        return

    p.print_help()


if __name__ == "__main__":
    main()
