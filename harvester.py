#!/usr/bin/env python3
"""Cyassist Exploit DNA Harvester — fetches exploit metadata from Exploit-DB,
GitHub, PacketStorm. Stores only DNA (technique, sink, params, URL) to SQLite.
No exploit code stored. Rudra handles exploitation."""

import datetime
import hashlib
import json
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent
USER_AGENT = "cyassist-harvester/1.0"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GH_TOKEN", "")

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


def _fetch(url: str, timeout: int = 20, headers: dict = None) -> Optional[str]:
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    try:
        import requests as _req
        r = _req.get(url, headers=req_headers, timeout=timeout, verify=False)
        return r.text if r.status_code == 200 else None
    except Exception:
        pass
    try:
        req = urllib.request.Request(url, headers={**req_headers, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def _cves(text: str) -> list[str]:
    return list(set(re.findall(r"CVE-\d{4}-\d{4,}", text or "")))


TECHNIQUE_KEYWORDS = {
    "sql injection": "sqli", "sql_injection": "sqli", "sqli": "sqli",
    "cross site scripting": "xss", "xss": "xss", "reflected xss": "xss",
    "stored xss": "xss", "dom xss": "xss",
    "server side request forgery": "ssrf", "ssrf": "ssrf",
    "remote code execution": "rce", "rce": "rce", "code execution": "rce",
    "command injection": "rce", "cmd injection": "rce",
    "local file inclusion": "lfi", "lfi": "lfi", "path traversal": "path_traversal",
    "directory traversal": "path_traversal",
    "idor": "idor", "insecure direct object": "idor",
    "server side template injection": "ssti", "ssti": "ssti",
    "xml external entity": "xxe", "xxe": "xxe",
    "open redirect": "open_redirect",
    "csrf": "csrf_misconfig", "cross site request forgery": "csrf_misconfig",
    "prototype pollution": "prototype_pollution",
    "race condition": "race_condition",
    "file upload": "file_upload", "arbitrary file upload": "file_upload",
    "deserialization": "insecure_deserialization",
    "buffer overflow": "buffer_overflow", "boF": "buffer_overflow",
    "privilege escalation": "privilege_escalation",
    "authentication bypass": "auth_bypass", "auth bypass": "auth_bypass",
    "oauth": "oauth_misconfig",
    "jwt": "jwt_attack", "json web token": "jwt_attack",
    "nosql injection": "nosqli", "nosqli": "nosqli",
    "ldap injection": "ldapi",
    "xpath injection": "xpathi",
    "memory corruption": "memory_corruption",
    "use after free": "use_after_free", "uaf": "use_after_free",
    "integer overflow": "integer_overflow",
    "type confusion": "type_confusion",
    "dns rebinding": "dns_rebinding",
    "http smuggling": "http_smuggling", "request smuggling": "http_smuggling",
    "cache poisoning": "cache_poisoning",
    "subdomain takeover": "subdomain_takeover",
    "clickjacking": "clickjacking",
    "websocket hijacking": "websocket_hijack",
}


def classify_technique(text: str) -> tuple[str, str]:
    """Classify exploit technique and map to Rudra sink type."""
    lower = text.lower()
    for keyword, technique in sorted(TECHNIQUE_KEYWORDS.items(), key=lambda x: -len(x[0])):
        if keyword in lower:
            return technique, technique.replace("_", "-")
    return "generic", "generic"


SINK_TYPE_MAP = {
    "sqli": "sql_injection", "xss": "reflected_xss", "ssrf": "ssrf",
    "rce": "command_injection", "lfi": "lfi", "path_traversal": "path_traversal",
    "ssti": "ssti", "xxe": "xxe", "idor": "idor",
    "open_redirect": "open_redirect", "csrf_misconfig": "csrf_misconfig",
    "file_upload": "file_upload", "nosqli": "nosqli",
    "prototype_pollution": "prototype_pollution",
    "race_condition": "race_condition",
    "oauth_misconfig": "oauth_misconfig", "jwt_attack": "jwt_attack",
    "generic": "generic",
}


# ── Exploit-DB RSS ─────────────────────────────────────────────────────────
EXPLOITDB_RSS = "https://www.exploit-db.com/rss.xml"

def harvest_exploitdb(db: IntelDB, max_items: int = 50) -> int:
    count = 0
    data = _fetch(EXPLOITDB_RSS)
    if not data:
        return 0
    try:
        root = ET.fromstring(data)
        for item in list(root.iter("item"))[:max_items]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            if not title or not link:
                continue
            cve_list = _cves(f"{title} {desc}")
            cve_id = cve_list[0] if cve_list else ""
            technique, _ = classify_technique(f"{title} {desc}")
            edb_id = ""
            edb_match = re.search(r'/exploits/(\d+)', link)
            if edb_match:
                edb_id = edb_match.group(1)

            extracted_params = extract_parameters(desc)
            sink_type = SINK_TYPE_MAP.get(technique, "generic")

            if db.add_exploit(
                cve_id=cve_id, source="exploit-db", title=title, url=link,
                technique=technique, sink_type=sink_type,
                parameter_template=json.dumps(extracted_params.get("params", [])),
                payload_template=extracted_params.get("payload", ""),
                target_software=extract_software(title),
                tags=["Exploit", "PoC", f"EDB:{edb_id}"] if edb_id else ["Exploit", "PoC"]
            ):
                count += 1

            for extra_cve in cve_list[1:]:
                db.add_exploit(cve_id=extra_cve, source="exploit-db", title=title, url=link,
                               technique=technique, sink_type=sink_type, tags=["Exploit", "PoC"])
    except ET.ParseError as e:
        print(f"  {Fmt.red(f'exploit-db parse error: {e}')}", file=sys.stderr)
    return count


# ── GitHub PoC Search ──────────────────────────────────────────────────────
GITHUB_API = "https://api.github.com/search/repositories"

def harvest_github(db: IntelDB, cve_ids: list[str] = None) -> int:
    count = 0
    if not cve_ids:
        cve_ids = [r["id"] for r in db.db.execute(
            "SELECT id FROM cves ORDER BY RANDOM() LIMIT 20").fetchall()]
    for cve_id in cve_ids[:10]:
        query = urllib.parse.urlencode({"q": f"{cve_id} in:name,description,topics"})
        url = f"{GITHUB_API}?{query}&sort=stars&order=desc"
        gh_headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else None
        data = _fetch(url, headers=gh_headers)
        if not data:
            continue
        try:
            body = json.loads(data)
            for repo in body.get("items", [])[:3]:
                repo_name = repo.get("full_name", "")
                repo_url = repo.get("html_url", "")
                desc = repo.get("description", "") or ""
                technique, _ = classify_technique(
                    f"{cve_id} {repo_name} {desc} {' '.join(repo.get('topics', []))}")
                sink_type = SINK_TYPE_MAP.get(technique, "generic")
                topics = repo.get("topics", [])
                if db.add_exploit(
                    cve_id=cve_id, source="github", title=f"{cve_id} — {repo_name}",
                    url=repo_url, technique=technique, sink_type=sink_type,
                    payload_template=desc[:300],
                    target_software=extract_software(f"{repo_name} {desc}"),
                    tags=["PoC", "GitHub"] + [f"topic:{t}" for t in topics[:3]]
                ):
                    count += 1
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  {Fmt.red(f'GitHub API error for {cve_id}: {e}')}", file=sys.stderr)
        time.sleep(1.2)
    return count


# ── Parameter/Payload extraction helpers ────────────────────────────────────
PARAM_PATTERNS = [
    (re.compile(r'(?:param|parameter|variable)[:\s]*[`\"]?(\w+)[`\"]?', re.I), "param"),
    (re.compile(r'(?:id|uid|pid|sid|token|key)=[\w-]+', re.I), "param"),
    (re.compile(r'/(?:api/)?v?\d+/(\w+)(?:/\d+)?', re.I), "endpoint"),
    (re.compile(r'(?:\b)(\w+)(?:\s*=\s*)(?:[\'\"].*?[\'\"])', re.I), "assign"),
]

PAYLOAD_PATTERNS = [
    re.compile(r"(?:payload|poc|exploit)[:\s]*(.+?)(?:\.|$)", re.I),
    re.compile(r"(?:send|post|request)[:\s]*(.+?)(?:\.|$)", re.I),
    re.compile(r"'(?:<script>[^']+</script>|' OR '1'='1|../etc/passwd|\$\{|#\{)", re.I),
]

def extract_parameters(text: str) -> dict:
    params = []
    payload = ""
    for pat, ptype in PARAM_PATTERNS:
        for m in pat.finditer(text or ""):
            val = m.group(1).strip()
            if val and len(val) < 50 and val not in params:
                params.append(val)
    for pat in PAYLOAD_PATTERNS:
        m = pat.search(text or "")
        if m:
            payload = m.group(1).strip()[:200] if m.lastindex else m.group(0).strip()[:200]
            break
    return {"params": params[:5], "payload": payload}


def extract_software(text: str) -> str:
    """Extract likely target software name from exploit title/desc."""
    patterns = [
        r"(?:WordPress|WP)\s+[\w\s-]+?(?:\d[\d.]+)?",
        r"(?:Apache|Nginx|IIS|Tomcat|Jetty)\s+[\d.]+",
        r"Joomla!?\s*[\d.]*",
        r"Drupal\s*[\d.]*",
        r"PHP\s*[\d.]+",
        r"Linux Kernel\s*[\d.]+",
        r"Windows\s+(?:Server|10|11|[\d.]+)",
        r"iOS\s*[\d.]+",
        r"Android\s*[\d.]+",
        r"VMware\s+[\w\s]+?\d",
        r"Forti(?:Gate|Net|OS)\s*[\d.]*",
        r"Cisco\s+[\w\s]+?\d",
        r"Palo Alto\s+[\w]+",
    ]
    for pat in patterns:
        m = re.search(pat, text or "", re.I)
        if m:
            return m.group(0).strip()
    return ""


# ── All harvesters ─────────────────────────────────────────────────────────
def harvest_all(db: IntelDB, verbose: bool = True) -> dict[str, int]:
    results = {}

    if verbose:
        print(f"  {Fmt.bold('Exploit-DB')} ...", end=" ", flush=True)
    count = harvest_exploitdb(db)
    results["exploit-db"] = count
    if verbose:
        print(f"{Fmt.green(str(count)) if count else Fmt.dim('0')}")

    cve_ids = [r["id"] for r in db.db.execute(
        "SELECT id FROM cves ORDER BY RANDOM() LIMIT 10").fetchall()]
    if not cve_ids:
        cve_ids = []
    if cve_ids:
        if verbose:
            print(f"  {Fmt.bold('GitHub PoCs')} ...", end=" ", flush=True)
        count = harvest_github(db, cve_ids)
        results["github"] = count
        if verbose:
            print(f"{Fmt.green(str(count)) if count else Fmt.dim('0')}")

    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Cyassist exploit harvester")
    p.add_argument("--cve", metavar="CVE-ID", help="Harvest GitHub PoCs for specific CVE")
    args = p.parse_args()

    if not IntelDB:
        print("Error: intel_db.py required")
        sys.exit(1)

    db = IntelDB()
    if args.cve:
        count = harvest_github(db, [args.cve])
        print(f"  {Fmt.green(f'{count} GitHub PoCs for {args.cve}')}")
    else:
        print(f"  {Fmt.bold('Exploit DNA harvester')}")
        results = harvest_all(db)
        total = sum(results.values())
        print(f"  {Fmt.green(f'Total: {total} exploits indexed')}  "
              f"{Fmt.dim(f'(DB: {db.size_mb():.2f}MB)')}")
    db.close()
