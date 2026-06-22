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


def save_target(name: str, techs: list[str], keywords: list[str]):
    """Add or update a target in targets.yaml."""
    targets = load_targets()
    targets[name] = {"techs": techs, "keywords": keywords}
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

    # ── Final Brief ──
    print(f"\n{Fmt.hr('\u2550', 70)}")
    print(f"  {Fmt.bold(Fmt.red(' PRIORITY HUNTING LIST '))}")
    print(Fmt.hr('\u2550', 70))

    prioritized = []
    for cve_id in news_cves:
        priority = 0
        reasons = []
        if cve_id in active_cves:
            priority += 30
            reasons.append("ACTIVELY EXPLOITED")
        if cve_id in poc_map or cve_id in gh_results:
            priority += 20
            reasons.append("PoC AVAILABLE")
        affected_targets = [t for t, cves in target_cve_map.items() if cve_id in cves]
        if affected_targets:
            priority += 10
            reasons.append(f"TARGET: {', '.join(affected_targets)}")
        prioritized.append((priority, cve_id, reasons))

    prioritized.sort(key=lambda x: x[0], reverse=True)

    if not prioritized:
        print(f"  {Fmt.dim('No actionable CVEs today.')}")
    else:
        for pri, cve_id, reasons in prioritized:
            if pri >= 30:
                label = Fmt.red("CRITICAL")
            elif pri >= 20:
                label = Fmt.yellow("HIGH")
            elif pri >= 10:
                label = Fmt.blue("MEDIUM")
            else:
                label = Fmt.dim("LOW")
            r_str = f" [{', '.join(reasons)}]" if reasons else ""
            poc_note = ""
            if cve_id in poc_map:
                poc_note = f" {Fmt.url(poc_map[cve_id][0]['file'])}"
            elif cve_id in gh_results:
                poc_note = f" {Fmt.url(gh_results[cve_id][0]['url'])}"
            print(f"\n  [{label}] {Fmt.bold(cve_id)}{poc_note}")
            print(f"          {Fmt.dim(r_str)}")

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

    if brief_cves:
        lines.append(f"## All CVEs in Today's News ({len(brief_cves)})")
        for c in sorted(brief_cves):
            lines.append(f"- {c}")
        lines.append("")
    else:
        lines.append("_No CVEs found in today's news._")

    brief_file.write_text("\n".join(lines))
    print(f"  {Fmt.green(f'Brief saved: {brief_file}')}")


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
    p.add_argument("--target-add", nargs=3, metavar=("NAME", "TECHS", "KW"),
                   help="Add target: name, comma-separated techs, comma-separated keywords")
    p.add_argument("--news-dir", default=str(HERE / "news"),
                   help="News directory (default: cyassist/news)")

    args = p.parse_args()
    news_dir = Path(args.news_dir)
    techniques_dir = HERE.parent / "bugbounty-config" / "techniques"

    if args.target_add:
        name, techs_str, kw_str = args.target_add
        techs = [t.strip() for t in techs_str.split(",") if t.strip()]
        kw = [k.strip() for k in kw_str.split(",") if k.strip()]
        save_target(name, techs, kw)
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
