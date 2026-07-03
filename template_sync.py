#!/usr/bin/env python3
"""Cyassist Template Sync — indexes nuclei template metadata from local nuclei-templates.
No template YAML files downloaded. Stores only template IDs, CVE refs, severity, technique.
Uses nuclei's own template index for CVEs → template ID mapping."""

import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent
USER_AGENT = "cyassist-template-sync/1.0"

try:
    from intel_db import IntelDB
except ImportError:
    IntelDB = None


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


# ── Nuclei template paths ──────────────────────────────────────────────────
NUCLEI_TEMPLATES_DIRS = [
    Path("/root/nuclei-templates"),
    Path.home() / "nuclei-templates",
    Path(os.environ.get("NUCLEI_TEMPLATES_PATH", "")),
]

CVE_YEAR_PATTERN = re.compile(r"cves/(\d{4})")
TEMPLATE_CVE = re.compile(r"CVE-\d{4}-\d{4,}")
TEMPLATE_META = re.compile(
    r"id:\s*(\S+)\s*\n.*?info:\s*\n(.*?)(?=\n\s*\w+:|\Z)",
    re.DOTALL
)


def find_nuclei_dir() -> Optional[Path]:
    for d in NUCLEI_TEMPLATES_DIRS:
        if d and d.exists():
            return d
    try:
        result = subprocess.run(
            ["nuclei", "-ut", "--disable-update-check"],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.split("\n"):
            if "templates" in line.lower() and "/" in line:
                path = line.strip().split()[-1]
                p = Path(path)
                if p.exists():
                    return p
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass
    return None


def scan_template_file(fp: Path, db: IntelDB) -> int:
    """Scan single YAML template, extract CVE + metadata, store to DB."""
    try:
        text = fp.read_text(errors="replace")
    except (OSError, UnicodeDecodeError):
        return 0

    cves = TEMPLATE_CVE.findall(text)
    if not cves:
        return 0

    # Extract template ID
    id_m = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
    template_id = id_m.group(1) if id_m else fp.stem

    # Extract severity
    sev_m = re.search(r"severity:\s*(\w+)", text)
    severity = sev_m.group(1) if sev_m else "unknown"

    # Extract technique tags from tags field or info
    tags_m = re.search(r"tags:\s*(.+?)(?:\n\S|\Z)", text, re.DOTALL)
    tags = []
    if tags_m:
        tags = [t.strip() for t in tags_m.group(1).split(",") if t.strip()]

    # Classify technique from tags
    technique = classify_from_tags(tags)

    # Build nuclei command
    nuclei_cmd = f"nuclei -id {template_id}"

    count = 0
    for cve_id in cves:
        try:
            db.add_template(cve_id=cve_id, template_id=template_id,
                          template_name=fp.name, severity=severity,
                          technique=technique, tags=tags,
                          nuclei_cmd=nuclei_cmd, url=str(fp))
            count += 1
        except Exception:
            pass
    return count


def classify_from_tags(tags: list[str]) -> str:
    tag_text = " ".join(tags).lower()
    technique_map = {
        "xss": "xss", "sqli": "sqli", "ssrf": "ssrf",
        "rce": "rce", "lfi": "lfi", "ssti": "ssti",
        "idor": "idor", "xxe": "xxe", "cmd-exec": "rce",
        "os-cmd": "rce", "command-execution": "rce",
        "path-traversal": "path_traversal", "dir-traversal": "path_traversal",
        "open-redirect": "open_redirect", "redirect": "open_redirect",
        "file-upload": "file_upload", "upload": "file_upload",
        "prototype-pollution": "prototype_pollution",
        "race-condition": "race_condition",
        "auth-bypass": "auth_bypass", "oauth": "oauth_misconfig",
        "jwt": "jwt_attack", "nosqli": "nosqli",
        "graphql": "graphql", "injection": "generic_injection",
        "debug": "debug_endpoint", "exposure": "exposure",
        "disclosure": "information_disclosure",
        "takeover": "subdomain_takeover",
        "cors": "cors_misconfig",
    }
    for keyword, technique in technique_map.items():
        if keyword in tag_text:
            return technique
    return "generic"


def sync_all_templates(db: IntelDB, verbose: bool = True) -> int:
    """Scan all nuclei template files for CVE-referencing templates."""
    nuclei_dir = find_nuclei_dir()
    if not nuclei_dir:
        if verbose:
            print(f"  {Fmt.yellow('nuclei-templates not found locally')}")
            print(f"  {Fmt.dim('Install: nuclei -ut  or  git clone https://github.com/projectdiscovery/nuclei-templates')}")
        return 0

    if verbose:
        print(f"  {Fmt.dim(f'nuclei-templates: {nuclei_dir}')}")

    # Only scan CVE directories (most storage-efficient approach)
    cve_dirs = []
    for year_dir in nuclei_dir.glob("**/cves"):
        if year_dir.is_dir():
            cve_dirs.append(year_dir)

    if not cve_dirs:
        if verbose:
            print(f"  {Fmt.yellow('No CVE template directories found')}")
        return 0

    total = 0
    for cve_dir in cve_dirs:
        yaml_files = list(cve_dir.rglob("*.yaml"))
        for fp in yaml_files:
            count = scan_template_file(fp, db)
            total += count
        if verbose:
            rel = cve_dir.relative_to(nuclei_dir) if cve_dir != nuclei_dir else cve_dir
            print(f"  {Fmt.dim(f'  {rel}: {len(yaml_files)} files, {total} CVE mappings so far')}")

    return total


# ── Metasploit module index (via module paths) ──────────────────────────────
MSF_PATHS = [
    Path("/usr/share/metasploit-framework/modules"),
    Path("/opt/metasploit-framework/modules"),
]

MSF_MODULE_CVE = re.compile(r"CVE-\d{4}-\d{4,}")

def sync_metasploit(db: IntelDB, verbose: bool = True) -> int:
    count = 0
    msf_dir = None
    for p in MSF_PATHS:
        if p.exists():
            msf_dir = p
            break
    if not msf_dir:
        if verbose:
            print(f"  {Fmt.dim('Metasploit not found locally')}")
        return 0

    if verbose:
        print(f"  {Fmt.dim(f'Scanning Metasploit modules: {msf_dir}')}")

    for rb_file in msf_dir.rglob("*.rb"):
        try:
            text = rb_file.read_text(errors="replace")[:5000]
        except (OSError, UnicodeDecodeError):
            continue
        cves = MSF_MODULE_CVE.findall(text)
        if not cves:
            continue

        name_m = re.search(r"'Name'\s*=>\s*'([^']+)'", text)
        module_name = name_m.group(1) if name_m else rb_file.stem
        sev_m = re.search(r"'Rank'\s*=>\s*(\d+)", text)
        severity = {"0": "manual", "1": "low", "2": "low", "3": "medium",
                    "4": "medium", "5": "high"}.get(sev_m.group(1) if sev_m else "", "unknown")

        # Classify technique from module path
        technique = "generic"
        path_lower = str(rb_file).lower()
        for kw, tech in [("exploit", "rce"), ("auxiliary", "generic"),
                          ("post", "post_exploit"), ("payload", "payload"),
                          ("nop", "nop"), ("encoder", "encoder"),
                          ("sqli", "sqli"), ("xss", "xss"),
                          ("ssrf", "ssrf"), ("scanner", "scanner")]:
            if kw in path_lower:
                technique = tech
                break

        for cve_id in cves[:3]:
            try:
                db.add_exploit(cve_id=cve_id, source="metasploit",
                              title=f"MSF: {module_name}", url=f"msf:{rb_file}",
                              technique=technique,
                              sink_type=SINK_TYPE_MAP.get(technique, "generic"),
                              target_software=extract_msf_target(text),
                              tags=["Metasploit", "Module"])
                count += 1
            except Exception:
                pass
    return count


SINK_TYPE_MAP = {
    "sqli": "sql_injection", "xss": "reflected_xss", "ssrf": "ssrf",
    "rce": "command_injection", "lfi": "lfi", "path_traversal": "path_traversal",
    "ssti": "ssti", "xxe": "xxe", "idor": "idor",
    "open_redirect": "open_redirect", "file_upload": "file_upload",
    "prototype_pollution": "prototype_pollution",
    "race_condition": "race_condition", "generic": "generic",
}


def extract_msf_target(text: str) -> str:
    m = re.search(r"'Platform'\s*=>\s*'([^']+)'", text)
    if m:
        return m.group(1)
    m = re.search(r"'Targets'\s*=>\s*\[(.*?)\]", text, re.DOTALL)
    if m:
        return m.group(1)[:100]
    return ""


def sync_all(db: IntelDB, verbose: bool = True) -> dict[str, int]:
    results = {}

    if verbose:
        print(f"  {Fmt.bold('Nuclei templates')} ...")
    nuc_count = sync_all_templates(db, verbose)
    results["nuclei"] = nuc_count
    if verbose:
        print(f"  {Fmt.green(f'  {nuc_count} CVE→template mappings')}")

    if verbose:
        print(f"  {Fmt.bold('Metasploit modules')} ...", end=" ", flush=True)
    msf_count = sync_metasploit(db, verbose)
    results["metasploit"] = msf_count
    if verbose:
        print(f"  {Fmt.green(str(msf_count)) if msf_count else Fmt.dim('0')}")

    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Cyassist template sync")
    p.add_argument("--check", action="store_true", help="Check if nuclei-templates exists")
    args = p.parse_args()

    if not IntelDB:
        print("Error: intel_db.py required")
        sys.exit(1)

    if args.check:
        d = find_nuclei_dir()
        if d:
            print(f"  {Fmt.green(f'nuclei-templates: {d}')}")
        else:
            print(f"  {Fmt.yellow('nuclei-templates not found')}")
        msf = [p for p in MSF_PATHS if p.exists()]
        if msf:
            print(f"  {Fmt.green(f'Metasploit: {msf[0]}')}")
        else:
            print(f"  {Fmt.yellow('Metasploit not found')}")
    else:
        db = IntelDB()
        print(f"  {Fmt.bold('Template sync')}")
        before = db.size_mb()
        results = sync_all(db)
        total = sum(results.values())
        after = db.size_mb()
        print(f"  {Fmt.green(f'{total} template mappings')}  "
              f"{Fmt.dim(f'DB: {before:.2f}MB → {after:.2f}MB')}")
        db.close()
