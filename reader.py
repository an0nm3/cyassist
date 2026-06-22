#!/usr/bin/env python3
"""Cyassist news reader — browse security news from RSS/Telegram sources.

Usage:
  python3 reader.py --today           Today's headlines
  python3 reader.py --headlines       Quick scan titles
  python3 reader.py --summary         500-word summary
  python3 reader.py -i --today        India-relevant news only
  python3 reader.py -q "SSRF"         Search keyword
  python3 reader.py -c techniques     Browse techniques
  python3 reader.py --sources         List all sources
  python3 reader.py --tags            List all tags
  python3 reader.py --add-source myblog https://blog.example.com/rss
  python3 reader.py --fetch-custom    Fetch custom RSS sources
  python3 reader.py --list-custom     List custom sources
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


class Fmt:
    _no_color = not sys.stdout.isatty()

    @classmethod
    def _wrap(cls, code, s, reset="0"):
        if cls._no_color or not s:
            return s
        return f"\033[{code}m{s}\033[{reset}m"

    @classmethod
    def bold(cls, s): return cls._wrap("1", s)
    @classmethod
    def dim(cls, s): return cls._wrap("2", s)
    @classmethod
    def red(cls, s): return cls._wrap("31", s)
    @classmethod
    def green(cls, s): return cls._wrap("32", s)
    @classmethod
    def yellow(cls, s): return cls._wrap("33", s)
    @classmethod
    def cyan(cls, s): return cls._wrap("36", s)
    @classmethod
    def cve(cls, s): return cls._wrap("1;31", s)
    @classmethod
    def source(cls, s): return cls._wrap("2;36", s)
    @classmethod
    def tag(cls, s): return cls._wrap("35", s)
    @classmethod
    def url(cls, s): return cls._wrap("4;34", s)
    @classmethod
    def orange(cls, s): return cls._wrap("38;5;214", s)
    @classmethod
    def india_green(cls, s): return cls._wrap("38;5;34", s)
    @classmethod
    def hr(cls, char="\u2501", n=60): return cls.dim(char * n)
    @classmethod
    def banner(cls, text, sub=""):
        line = cls.hr()
        parts = [f"  {cls.bold(text)}"]
        if sub:
            parts.append(f"  {cls.dim(sub)}")
        return f"\n{line}\n{chr(10).join(parts)}\n{line}\n"

    @classmethod
    def signature(cls):
        line = cls.hr("\u2500", 50)
        name = cls.bold("4n0n0n3")
        heart = cls.bold("\u2665")
        return f"{line}\n  Made by \U0001f1ee\U0001f1f3 {name} with {heart}\n{line}"


def _figlet(text: str) -> str:
    try:
        result = subprocess.run(
            ["figlet", "-f", "digital", text],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.rstrip("\n")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return f"  {Fmt.bold(text)}"


LOGO = """
\u2584\u2580\u2580\u2580  \u2588   \u2588 \u2584\u2580\u2580\u2580\u2584 \u2584\u2580\u2580\u2580\u2580 \u2584\u2580\u2580\u2580\u2580  \u2580  \u2584\u2580\u2580\u2580\u2580 \u2580\u2580\u2588\u2580\u2580
\u2588     \u2580\u2584 \u2584\u2580 \u2588\u2580\u2580\u2580\u2588  \u2580\u2580\u2580\u2584  \u2580\u2580\u2580\u2584  \u2588   \u2580\u2580\u2580\u2584   \u2588
 \u2580\u2580\u2580    \u2588   \u2580   \u2580 \u2580\u2580\u2580\u2580  \u2580\u2580\u2580\u2580   \u2580  \u2580\u2580\u2580\u2580    \u2580
       \u2584\u2580
"""


def _compact_header(heading_text: str, india_mode: bool = False):
    logo_lines = LOGO.strip("\n").split("\n")
    for line in logo_lines:
        if india_mode:
            print(f"  {Fmt.bold(Fmt.orange(line))}")
        else:
            print(f"  {Fmt.bold(Fmt.green(line))}")
    heading = _figlet(heading_text)
    lines = heading.split("\n")
    if india_mode:
        colored = []
        for i, line in enumerate(lines):
            if i == 0:
                colored.append(Fmt.bold(Fmt.orange(line)))
            elif i == len(lines) - 1:
                colored.append(Fmt.bold(Fmt.india_green(line)))
            else:
                colored.append(Fmt.bold(line))
        heading = "\n".join(colored)
    else:
        heading = "\n".join(f"  {Fmt.bold(Fmt.green(line))}" for line in lines)
    print(heading)
    print(Fmt.signature())


NEWS_DIR = Path(__file__).parent / "news"
EXCERPT_WORDS = 150
CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "cyassist"
DATA_DIR = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "cyassist"
CUSTOM_SOURCES_FILE = CONFIG_DIR / "sources.json"
CUSTOM_NEWS_DIR = DATA_DIR / "custom"


def _meta(text: str) -> dict:
    m = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    m[k.strip()] = v.strip()
    return m


def _strip_fm(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text.strip()


INDIA_SOURCE_PATTERNS = [
    "et-ciso",
    "the-cyber-india", "the cyber india",
    "cyberblogindia",
]

INDIA_KEYWORDS = [
    # General
    "india", "indian",
    # Govt cyber bodies
    "cert-in", "nciipc", "cdac", "stqc", "nielit", "nic.in",
    "meity", "ministry of home affairs", "mha",
    # Frameworks & regulations
    "dpdp", "digital personal data protection", "it act",
    "national cyber security policy", "ncsp",
    "information technology act",
    "cyber swachhta", "i4c", "cybercrime.gov.in",
    "national cyber crime reporting",
    # Identity & fintech
    "aadhaar", "uidai", "digilocker", "upi", "bhim", "rupay",
    "pan card", "voter id", "epfo",
    # Indian companies & banks
    "tcs", "infosys", "wipro", "hcl", "tech mahindra",
    "reliance jio", "airtel", "bsnl", "vodafone idea", "vi",
    "sbi", "state bank of india", "hdfc", "icici", "rbi", "npci",
    "paytm", "phonepe", "razorpay", "bharatpe",
    "flipkart", "zomato", "swiggy", "ola", "irctc", "groww", "zerodha",
    # Threat actors targeting India
    "sidewinder", "patchwork", "transparent tribe", "apt36",
    "confucius", "white elephant", "bahamut",
    "indian cyber crime", "cyber crime india",
    # Indian govt initiatives
    "ayushman bharat", "cowin", "digiyatra", "fastag",
    "gstn", "umang",
    # States & cities
    "delhi", "mumbai", "bengaluru", "bangalore",
    "hyderabad", "chennai", "pune", "kolkata", "ahmedabad",
    "gurgaon", "noida", "jaipur", "lucknow", "chandigarh",
    # Domains
    "gov.in", "nic.in", "ac.in", "edu.in", "co.in",
]


def _matches_india(text, title, source):
    source_lower = source.lower()
    for pat in INDIA_SOURCE_PATTERNS:
        if pat in source_lower:
            return True
    combined = f"{title} {text}".lower()
    for kw in INDIA_KEYWORDS:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, combined):
            return True
    return False


def _load_custom_sources():
    if not CUSTOM_SOURCES_FILE.exists():
        return []
    try:
        return json.loads(CUSTOM_SOURCES_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return []

def _save_custom_sources(sources):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CUSTOM_SOURCES_FILE.write_text(json.dumps(sources, indent=2))

def _add_source(name, url):
    sources = _load_custom_sources()
    if any(s["name"] == name for s in sources):
        return False, f"Source '{name}' already exists"
    sources.append({"name": name, "url": url})
    _save_custom_sources(sources)
    return True, f"Added source '{name}'"

def _remove_source(name):
    sources = _load_custom_sources()
    filtered = [s for s in sources if s["name"] != name]
    if len(filtered) == len(sources):
        return False, f"Source '{name}' not found"
    _save_custom_sources(filtered)
    return True, f"Removed source '{name}'"

def _fetch_custom_sources():
    sources = _load_custom_sources()
    if not sources:
        print(f"  {Fmt.dim('No custom sources configured. Use --add-source to add one.')}")
        return
    CUSTOM_NEWS_DIR.mkdir(parents=True, exist_ok=True)
    for s in sources:
        name = s["name"]
        url = s["url"]
        print(f"  Fetching {Fmt.bold(name)} ...", end=" ")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "cyassist/1.0"})
            resp = urllib.request.urlopen(req, timeout=15)
            data = resp.read()
            root = ET.fromstring(data)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            items = []
            for item in root.iter("item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = item.findtext("description", "")
                pubdate = item.findtext("pubDate", "")
                items.append((title, link, desc, pubdate))
            for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
                title = entry.findtext("{http://www.w3.org/2005/Atom}title", "")
                link_el = entry.find("{http://www.w3.org/2005/Atom}link")
                link = link_el.get("href", "") if link_el is not None else ""
                desc_el = entry.find("{http://www.w3.org/2005/Atom}content")
                desc = desc_el.text if desc_el is not None else ""
                published = entry.findtext("{http://www.w3.org/2005/Atom}published", "")
                items.append((title, link, desc, published))
            count = 0
            for title, link, desc, pubdate in items:
                if not title:
                    continue
                uid = hashlib.md5(f"{name}:{title}:{link}".encode()).hexdigest()[:12]
                fname = CUSTOM_NEWS_DIR / f"{name}_{uid}.md"
                if fname.exists():
                    continue
                tags = "custom"
                date_str = datetime.datetime.now().strftime("%Y-%m-%d")
                content = f"""---
title: "{title}"
source: "custom/{name}"
date: "{date_str}"
category: "news"
tags: [{tags}]
url: "{link}"
---
{desc.strip()[:500]}"""
                fname.write_text(content)
                count += 1
            print(f"{Fmt.green(f'{count} new')}")
        except Exception as e:
            print(f"{Fmt.red(f'error: {e}')}")


def _collect(category: str = "news", days: int = 0, source: str = "",
             query: str = "", india_mode: bool = False):
    if days > 0:
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    else:
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
    items = []

    for base_dir in [NEWS_DIR]:
        if base_dir.exists():
            for fp in base_dir.rglob("*.md"):
                if fp.name.startswith("."):
                    continue
                if datetime.datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
                    continue
                text = fp.read_text(errors="replace")
                m = _meta(text)
                if category and m.get("category", "") != category:
                    continue
                if source and source.lower() not in m.get("source", "").lower():
                    continue
                if query and query.lower() not in text.lower():
                    continue
                title = m.get("title", fp.stem)
                in_scope = _matches_india(text, title, m.get("source", "")) if india_mode else True
                items.append((fp, text, m, in_scope))

    if CUSTOM_NEWS_DIR.exists():
        for fp in CUSTOM_NEWS_DIR.rglob("*.md"):
            if fp.name.startswith("."):
                continue
            if datetime.datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
                continue
            text = fp.read_text(errors="replace")
            m = _meta(text)
            if category and m.get("category", "") != category:
                continue
            if source and source.lower() not in m.get("source", "").lower():
                continue
            if query and query.lower() not in text.lower():
                continue
            title = m.get("title", fp.stem)
            in_scope = _matches_india(text, title, m.get("source", "")) if india_mode else True
            items.append((fp, text, m, in_scope))

    return items


TECH_TAGS = {"CVE", "Rce", "Sqli", "Xss", "Ssti", "Lfi", "Idor",
              "Bypass", "0day", "Xxe", "Injection", "Deserialization",
              "Privilege escalation", "Ato", "Authentication bypass",
              "File upload", "Race condition", "Prototype pollution",
              "Mass assignment", "Graphql introspection", "Poc", "Exploit",
              "SsrF"}


def _is_tech(m: dict) -> bool:
    tags = m.get("tags", "")
    if not tags or tags == "[]":
        return False
    for tag in tags.strip("[]").split(","):
        if tag.strip() in TECH_TAGS:
            return True
    return False


def _dedup_items(items):
    seen = set()
    unique = []
    dup_map = {}
    for item in items:
        url = item[2].get("url", "")
        if not url:
            unique.append(item)
            continue
        if url in seen:
            dup_map.setdefault(url, []).append(item[2].get("source", "?"))
            continue
        seen.add(url)
        unique.append(item)
    return unique, dup_map


def _build_entry(fp, text, m, in_scope, dup_map):
    title = m.get("title", fp.stem)
    src = m.get("source", "?")
    url = m.get("url", "")
    body = _strip_fm(text)
    cves = re.findall(r"CVE-\d{4}-\d{4,}", text)
    cve_str = f" {Fmt.cve('\u26a0 ' + ' '.join(cves[:3]))}" if cves else ""
    marker = Fmt.green("\u25cf ") if in_scope else ""
    dup_note = ""
    if url and url in dup_map:
        dup_note = f"  {Fmt.yellow(f'\u262f +{len(dup_map[url])} src')}"
    display = f"{marker}{Fmt.source(f'[{src}]')} {Fmt.bold(title)}{cve_str}{dup_note}"
    return {"fp": fp, "text": text, "meta": m, "body": body, "display": display,
            "title": title, "source": src, "url": url, "cves": cves, "in_scope": in_scope}


def _clean_body(body: str, max_words: int = 150) -> str:
    lines = body.strip().split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('**Source:**') or stripped.startswith('**Link:**'):
            continue
        if stripped.lower().startswith('read more'):
            continue
        if 'appeared first on' in stripped:
            continue
        if stripped:
            cleaned.append(stripped)
    text = ' '.join(cleaned).strip()
    words = text.split()
    if len(words) > max_words:
        text = ' '.join(words[:max_words]) + ' ...'
    return text


def _show_expanded(entry):
    cve_str = f" {Fmt.cve('\u26a0 ' + ' '.join(entry['cves'][:5]))}" if entry['cves'] else ""
    print(f"\n{Fmt.hr('\u2550', 70)}")
    print(f" {Fmt.bold(entry['title'])}{cve_str}")
    print(f" {Fmt.dim('source:')} {entry['source']}")
    print(f" {Fmt.dim('tags:')} {entry['meta'].get('tags', 'None')}")
    if entry['url']:
        print(f" {Fmt.dim('link:')} {Fmt.url(entry['url'])}")
    print(Fmt.hr('\u2550', 70))
    body = _clean_body(entry['body'])
    print(f" {body}")


def today(category: str = "news", source="", query="",
          heading_text="Cyber Global News", india_mode=False):
    items = _collect(category, source=source, query=query, india_mode=india_mode)
    if not items:
        _compact_header(heading_text, india_mode)
        print(f"  {Fmt.dim('No ' + category + ' in the last 24 hours.')}\n")
        return

    items.sort(key=lambda x: (0 if "CVE" in x[2].get("tags", "") else 1, x[2].get("source", "")))
    items, dup_map = _dedup_items(items)

    if india_mode:
        items = [x for x in items if x[3]]
        if not items:
            _compact_header(heading_text, india_mode)
            print(f"  {Fmt.dim('No India-relevant ' + category + ' in the last 24 hours.')}\n")
            return

    entries = [_build_entry(*item, dup_map) for item in items]
    total = len(entries)

    if not sys.stdout.isatty():
        _compact_header(heading_text, india_mode)
        for i, e in enumerate(entries):
            print(f"  {Fmt.bold(f'{i+1:>3}.')} {e['display']}")
        return

    highlights = [e for e in entries if e['cves']]
    news_items = [e for e in entries if not e['cves']]
    page_size = 10
    page = 0
    hl_page = 0
    hl_page_size = 10
    show_all_hl = False
    mode = "highlights" if highlights else "news"

    _compact_header(heading_text, india_mode)
    pages = max(1, (total - 1) // page_size + 1)

    while True:
        if mode == "highlights":
            hl = highlights if show_all_hl else highlights[hl_page * hl_page_size:(hl_page + 1) * hl_page_size]
            if not hl:
                mode = "news"
                continue
            hl_total = len(highlights)
            tag = f" ({len(hl)}/{hl_total})" if hl_total > hl_page_size else f" ({hl_total})"
            print(f"  {Fmt.bold(Fmt.red(' \u26a0 HIGHLIGHTS '))}{Fmt.dim(tag)}")
            for e in hl:
                idx = entries.index(e) + 1
                print(f"  {Fmt.bold(f'{idx:>3}.')} {e['display']}")
            if not show_all_hl and hl_total > hl_page_size:
                hl_pages = max(1, (hl_total - 1) // hl_page_size + 1)
                p = hl_page + 1
                print(f"  {Fmt.dim(f'  Hl page {p}/{hl_pages} \u2014 [hn] [hp] to scroll')}")
            elif show_all_hl and hl_total > hl_page_size:
                print(f"  {Fmt.dim(f'  All {hl_total} highlights shown \u2014 [m] to collapse')}")
            print()
        else:
            pages = max(1, (total - 1) // page_size + 1)
            print(f"  {Fmt.dim(f'\u2500\u2500\u2500 News {page + 1}/{pages} \u2500\u2500\u2500')}")
            start = page * page_size
            end = min(start + page_size, total)
            for i in range(start, end):
                e = entries[i]
                idx = i + 1
                src_name = e['source']
                cve_tag = ' ' + Fmt.cve('\u26a0 ' + ' '.join(e['cves'][:2])) if e['cves'] else ''
                print(f"  {Fmt.bold(f'{idx:>3}.')} {Fmt.source(f'[{src_name}]')} {Fmt.bold(e['title'])}"
                      f"{cve_tag}")
                body_preview = _clean_body(e['body'], max_words=125)[:600]
                if body_preview:
                    print(f"      {Fmt.dim(body_preview)}")
                if e['url']:
                    print(f"      {Fmt.url(e['url'])}")
            print(f"  {Fmt.dim(f'{total} items')}")

        hl_nav = f"  [{Fmt.bold('h')}]hl" if mode == "news" and highlights else f"  [{Fmt.bold('n')}]news" if mode == "highlights" else ""
        more_nav = f"  [{Fmt.bold('m')}]more" if mode == "highlights" and len(highlights) > 20 and not show_all_hl else ""
        if mode == "highlights" and show_all_hl and len(highlights) > 20:
            more_nav = f"  [{Fmt.bold('m')}]less"
        page_nav = ""
        if mode == "news":
            page_nav = f"  [{Fmt.bold('n')}]next  [{Fmt.bold('p')}]prev"
        elif mode == "highlights":
            page_nav = f"  [{Fmt.bold('hn')}]hnext  [{Fmt.bold('hp')}]hprev"

        try:
            cmd = input(f"  [{Fmt.bold('#' + str(total))}]expand{page_nav}{hl_nav}{more_nav}"
                        f"  [{Fmt.bold('/')}]search  [{Fmt.bold('q')}]uit: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if cmd == 'q':
            break
        elif cmd == 'h':
            if highlights:
                mode = "highlights"
                hl_page = 0
        elif cmd == 'n':
            if mode == "news":
                if page >= pages - 1:
                    print("  No more items")
                    continue
                page += 1
            else:
                mode = "news"
        elif cmd == 'p' and mode == "news":
            if page <= 0:
                print("  Already at first page")
                continue
            page -= 1
        elif cmd == 'hn' and mode == "highlights":
            hl_pages = max(1, (len(highlights) - 1) // hl_page_size + 1) if not show_all_hl else 1
            if hl_page >= hl_pages - 1:
                print("  No more items")
                continue
            hl_page += 1
        elif cmd == 'hp' and mode == "highlights":
            if hl_page <= 0:
                print("  Already at first page")
                continue
            hl_page -= 1
        elif cmd == 'm':
            show_all_hl = not show_all_hl
        elif cmd.startswith('/'):
            term = cmd[1:].strip()
            if term:
                matches = [(i, e) for i, e in enumerate(entries)
                           if term.lower() in e['title'].lower() or term.lower() in e['body'].lower()]
                if matches:
                    print(f"\n  {Fmt.bold(f' {len(matches)} matches for \"{term}\" ')}")
                    for idx, e in matches[:10]:
                        print(f"  {Fmt.bold(f'{idx + 1:>3}.')} {e['display']}")
                    if len(matches) > 10:
                        print(f"  {Fmt.dim(f'  ... +{len(matches) - 10} more')}")
                else:
                    print(f"  {Fmt.dim(f'No matches for \"{term}\"')}")
                input(f"  {Fmt.dim('Press Enter...')}")
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < total:
                _show_expanded(entries[idx])
                input(f"\n  {Fmt.dim('Press Enter to continue...')}")


def headlines(days: int = 1, category: str = "news",
              source="", query="", india_mode=False):
    items = _collect(category, days=days, source=source, query=query, india_mode=india_mode)
    items, dup_map = _dedup_items(items)
    by_source = {}

    if india_mode:
        items = [x for x in items if x[3]]
        if not items:
            heading = "Indian Cyber News" if india_mode else "Cyber Global News"
            _compact_header(heading, india_mode)
            print(f"  {Fmt.dim(f'No India-relevant {category} in the last {days} day(s).')}\n")
            return

    for fp, text, m, in_scope in items:
        src = m.get("source", "unknown")
        title = m.get("title", fp.stem)
        tags = m.get("tags", "")
        tag_str = f" {Fmt.tag(tags)}" if tags and tags != "[]" else ""
        marker = Fmt.green("\u25cf ") if in_scope else ""
        by_source.setdefault(src, []).append(f"    {marker}\u2022 {Fmt.bold(title)}{tag_str}")

    if not by_source:
        print(f"\n  {Fmt.dim(f'No {category} in the last {days} day(s).')}\n")
        return

    total_items = sum(len(v) for v in by_source.values())
    sub = f"{total_items} items"
    if dup_map:
        sub += f" \u00b7 {Fmt.dim(f'{len(dup_map)} merged')}"
    heading = "Indian Cyber News" if india_mode else "Cyber Global News"
    print(Fmt.banner(f"{heading}", sub))

    for src in sorted(by_source.keys()):
        print(f"  {Fmt.source('\u250c\u2500 ' + src)}")
        for line in by_source[src][:10]:
            print(line)
        if len(by_source[src]) > 10:
            print(f"    {Fmt.dim(f'... +{len(by_source[src]) - 10} more')}")
        print()


def summary(days: int = 1, category: str = "news",
            heading_text="Cyber Global News", india_mode=False):
    items = _collect(category, days=days, india_mode=india_mode)
    items, _ = _dedup_items(items)
    items.sort(key=lambda x: (0 if "CVE" in x[2].get("tags", "") else 1, x[2].get("source", "")))

    if india_mode:
        items = [x for x in items if x[3]]

    entries = []
    for fp, text, m, in_scope in items:
        cves = re.findall(r"CVE-\d{4}-\d{4,}", text)
        body = _strip_fm(text)
        entries.append({"meta": m, "body": body, "cves": cves})

    total = len(entries)
    cve_items = [e for e in entries if e['cves']]

    _compact_header(heading_text, india_mode)
    print(f"  {Fmt.dim(f'{total} items \u00b7 {len(cve_items)} with CVEs')}")
    print()

    srcs = {}
    for e in entries:
        s = e['meta'].get('source', '?')
        srcs[s] = srcs.get(s, 0) + 1
    top_sources = sorted(srcs, key=srcs.get, reverse=True)[:3]
    cve_part = f"{len(cve_items)} vulnerability disclosures" if cve_items else "no CVEs"
    print(f"  Today's security roundup: {total} articles from {len(srcs)} sources "
          f"covering {cve_part}. Leading sources: {', '.join(top_sources)}.")
    print()

    if cve_items:
        print(f"  {Fmt.bold(' TOP VULNERABILITIES ')}\n")
        for e in cve_items[:5]:
            title = e['meta'].get('title', '?')
            src = e['meta'].get('source', '?')
            cves = " ".join(e['cves'][:3])
            first_line = _clean_body(e['body'], max_words=25)[:120] if e['body'] else ""
            print(f"  {Fmt.bold(title)} [{Fmt.cve(cves)}]")
            print(f"  {Fmt.source(src)} \u2014 {Fmt.dim(first_line)}")
            print()

    shown_titles = {e['meta'].get('title', '') for e in cve_items[:5]}
    remaining = [e for e in entries if e['meta'].get('title', '') not in shown_titles]
    if remaining:
        print(f"  {Fmt.bold(' TODAY\'S HEADLINES ')}\n")
        for e in remaining[:10]:
            title = e['meta'].get('title', '?')
            src = e['meta'].get('source', '?')
            cve_str = f" [{Fmt.cve(' '.join(e['cves'][:2]))}]" if e['cves'] else ""
            tag_str = ""
            tags = e['meta'].get('tags', '')
            if tags and tags != "[]":
                tag_str = f" {Fmt.tag(tags[:40])}"
            print(f"  \u2022 {Fmt.bold(title)}{cve_str}{tag_str}")
            print(f"    {Fmt.source(src)}")
        if len(remaining) > 10:
            print(f"\n  {Fmt.dim(f'... +{len(remaining) - 10} more items (use --today for full list)')}")
    print()


def list_sources(category=""):
    sources = set()
    for fp in NEWS_DIR.rglob("*.md"):
        if fp.name.startswith("."):
            continue
        m = _meta(fp.read_text(errors="replace"))
        if category and m.get("category", "") != category:
            continue
        if m.get("source"):
            sources.add(m["source"])
    print(Fmt.banner("SOURCES", f"{len(sources)} sources"))
    for s in sorted(sources):
        print(f"  {Fmt.source(s)}")


def list_tags(category=""):
    tags = set()
    for fp in NEWS_DIR.rglob("*.md"):
        if fp.name.startswith("."):
            continue
        m = _meta(fp.read_text(errors="replace"))
        if category and m.get("category", "") != category:
            continue
        t = m.get("tags", "")
        if t.startswith("[") and t.endswith("]"):
            for tag in t[1:-1].split(","):
                tag = tag.strip()
                if tag:
                    tags.add(tag)
    print(Fmt.banner("TAGS", f"{len(tags)} tags"))
    for t in sorted(tags):
        print(f"  {Fmt.tag(t)}")


def search(query="", source="", days=0, category="",
           count_only=False, india_mode=False):
    _compact_header("Indian Cyber News" if india_mode else "Cyber Global News", india_mode)
    print()

    results = []
    now = datetime.datetime.now()

    for fp in NEWS_DIR.rglob("*.md"):
        if fp.name.startswith("."):
            continue
        text = fp.read_text(errors="replace")
        m = _meta(text)
        if category and m.get("category", "") != category:
            continue
        if source and source not in m.get("source", ""):
            continue
        if days > 0:
            if (now - datetime.datetime.fromtimestamp(fp.stat().st_mtime)).days > days:
                continue
        if query and query.lower() not in text.lower():
            continue
        title = m.get("title", fp.stem)
        in_scope = _matches_india(text, title, m.get("source", "")) if india_mode else True
        if india_mode and not in_scope:
            continue
        results.append((fp, text, m, in_scope))

    if count_only:
        print(Fmt.bold(str(len(results))))
        return

    if not results:
        print(f"  {Fmt.dim('No results.')}")
        return

    print(Fmt.banner("SEARCH", f"{len(results)} results"))

    for fp, text, m, in_scope in results:
        title = m.get("title", fp.stem)
        src = m.get("source", "?")
        cat = m.get("category", "?")
        tag_str = m.get("tags", "")
        cves = " ".join(re.findall(r"CVE-\d{4}-\d{4,}", text))
        marker = Fmt.green("\u25cf ") if in_scope else ""
        print(f"\n{Fmt.hr('\u2550', 66)}")
        print(f" {marker}{Fmt.bold(title)}")
        if cves:
            print(f"   {Fmt.cve('\u26a0 ' + cves)}")
        print(f"   {Fmt.source('source: ' + src + '  |  tags: ' + tag_str)}")
        if query:
            idx = text.lower().find(query.lower())
            if idx > 0:
                s = max(0, idx - 100)
                e = min(len(text), idx + len(query) + 100)
                snippet = text[s:e].replace(chr(10), ' ')
                print(f"   {Fmt.dim('...' + snippet + '...')}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Cyassist news reader")
    p.add_argument("--news-repo", default=str(NEWS_DIR),
                   help="Path to news repo (default: ./news)")
    p.add_argument("--tech-repo", default="",
                   help="Path to techniques repo (default: none)")

    p.add_argument("-T", "--today", action="store_true",
                   help="Interactive numbered news browser")
    p.add_argument("-H", "--headlines", action="store_true",
                   help="Quick scan titles")
    p.add_argument("--summary", action="store_true",
                   help="500-word news summary")
    p.add_argument("-c", "--category", nargs='?', const='__help__', default="",
                   choices=["news", "techniques", "", "__help__"],
                   help="Category (news|techniques)")
    p.add_argument("-q", "--query", nargs='?', const='__help__', default="",
                   help="Search keyword")
    p.add_argument("-s", "--source", nargs='?', const='__help__', default="",
                   help="Filter by source name")
    p.add_argument("-i", "--india", action="store_true",
                   help="India preset scope (cert-in, dpdp, aadhaar...)")
    p.add_argument("-n", "--count", action="store_true", help="Count only")
    p.add_argument("--sources", action="store_true", help="List sources")
    p.add_argument("--tags", action="store_true", help="List tags")
    p.add_argument("--add-source", nargs=2, metavar=("NAME", "URL"),
                   help="Add a custom RSS source")
    p.add_argument("--remove-source", metavar="NAME",
                   help="Remove a custom RSS source")
    p.add_argument("--list-custom", action="store_true",
                   help="List custom RSS sources")
    p.add_argument("--fetch-custom", action="store_true",
                   help="Fetch articles from custom sources")

    args = p.parse_args()

    if args.add_source:
        ok, msg = _add_source(args.add_source[0], args.add_source[1])
        print(msg)
        return

    if args.remove_source:
        ok, msg = _remove_source(args.remove_source)
        print(msg)
        return

    if args.list_custom:
        sources = _load_custom_sources()
        if not sources:
            print("  No custom sources configured.")
        else:
            print(f"  {Fmt.bold('Custom sources:')}")
            for s in sources:
                print(f"    {Fmt.green(s['name'])}  {Fmt.dim(s['url'])}")
        return

    if args.fetch_custom:
        _fetch_custom_sources()
        return

    india_mode = args.india
    heading_text = "Indian Cyber News" if india_mode else "Cyber Global News"

    if args.today:
        today(args.category or "news", source=args.source or "",
              query=args.query or "", heading_text=heading_text,
              india_mode=india_mode)
    elif args.headlines:
        _compact_header(heading_text, india_mode)
        print()
        headlines(days=1, category=args.category or "news",
                  source=args.source or "", query=args.query or "",
                  india_mode=india_mode)
    elif args.summary:
        summary(days=1, category=args.category or "news",
                heading_text=heading_text, india_mode=india_mode)
    elif args.sources:
        _compact_header(heading_text, india_mode)
        print()
        list_sources(args.category)
    elif args.tags:
        _compact_header(heading_text, india_mode)
        print()
        list_tags(args.category)
    elif args.count:
        search(args.query or "", args.source or "",
               days=0, category=args.category or "",
               count_only=True, india_mode=india_mode)
    elif args.query:
        search(args.query or "", args.source or "",
               days=0, category=args.category or "",
               india_mode=india_mode)
    elif args.source:
        today(args.category or "news", source=args.source or "",
              heading_text=heading_text, india_mode=india_mode)
    elif india_mode:
        today(args.category or "news", heading_text=heading_text, india_mode=india_mode)
    else:
        today(args.category or "news", heading_text=heading_text, india_mode=india_mode)
