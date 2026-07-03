#!/usr/bin/env python3
"""Cyassist Web Scraper — directly scrapes security news sites beyond RSS.
Stores only metadata (title, URL, CVE refs, tags) to SQLite. No body blobs."""

import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent
USER_AGENT = "cyassist-web-scraper/1.0"

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


def _fetch(url: str, timeout: int = 20) -> Optional[str]:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def _cves(text: str) -> list[str]:
    return list(set(re.findall(r"CVE-\d{4}-\d{4,}", text or "")))


def _clean(html: str) -> str:
    return ' '.join(re.sub(r'<[^>]+>', ' ', html or '').split())


def _extract_links(html: str, base_url: str) -> list[tuple[str, str]]:
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    result = []
    for href, title_html in links:
        title = _clean(title_html)
        if not title or len(title) < 8:
            continue
        if href.startswith("/"):
            href = base_url.rstrip("/") + href
        result.append((href, title))
    return result


# ── Source: The Hacker News ────────────────────────────────────────────────
THN_URL = "https://thehackernews.com"

def scrape_thn(db: IntelDB) -> int:
    count = 0
    html = _fetch(THN_URL)
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(https?://thehackernews\.com/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles:
        if href in seen:
            continue
        seen.add(href)
        title = _clean(title_html)
        if not title or len(title) < 10:
            continue
        cve_refs = _cves(title)
        tags = ["THN"]
        if cve_refs:
            tags.append("CVE")
        if db.add_news("the-hacker-news", href, title,
                       tags=tags, cve_refs=cve_refs):
            count += 1
    return count


# ── Source: BleepingComputer ───────────────────────────────────────────────
BLEEPING_URL = "https://www.bleepingcomputer.com"

def scrape_bleeping(db: IntelDB) -> int:
    count = 0
    html = _fetch(f"{BLEEPING_URL}/")
    if not html:
        return 0
    articles = _extract_links(html, BLEEPING_URL)
    seen = set()
    for href, title in articles:
        if href in seen:
            continue
        seen.add(href)
        if not title or len(title) < 10:
            continue
        if not any(kw in href.lower() for kw in ["/news/", "/security/"]):
            continue
        cve_refs = _cves(title)
        tags = ["BleepingComputer"]
        if cve_refs:
            tags.append("CVE")
        if db.add_news("bleepingcomputer", href, title,
                       tags=tags, cve_refs=cve_refs):
            count += 1
    return count


# ── Source: GBHackers ──────────────────────────────────────────────────────
GBHACKERS_URL = "https://gbhackers.com"

def scrape_gbhackers(db: IntelDB) -> int:
    count = 0
    html = _fetch(GBHACKERS_URL)
    if not html:
        return 0
    articles = _extract_links(html, GBHACKERS_URL)
    seen = set()
    for href, title in articles:
        if href in seen:
            continue
        seen.add(href)
        if not title or len(title) < 10:
            continue
        cve_refs = _cves(title)
        tags = ["GBHackers"]
        if cve_refs:
            tags.append("CVE")
        if db.add_news("gbhackers-on-security", href, title,
                       tags=tags, cve_refs=cve_refs):
            count += 1
    return count


# ── Source: PacketStorm (as web page) ──────────────────────────────────────
PACKETSTORM_URL = "https://packetstormsecurity.com"

def scrape_packetstorm(db: IntelDB) -> int:
    count = 0
    html = _fetch(f"{PACKETSTORM_URL}/news/")
    if not html:
        return 0
    articles = _extract_links(html, PACKETSTORM_URL)
    seen = set()
    for href, title in articles:
        if href in seen:
            continue
        seen.add(href)
        if not title or len(title) < 10:
            continue
        cve_refs = _cves(title)
        tags = ["PacketStorm"]
        if cve_refs:
            tags.append("CVE")
        if db.add_news("packetstorm", href, title,
                       tags=tags, cve_refs=cve_refs):
            count += 1
    return count


# ── Source: Reddit netsec ──────────────────────────────────────────────────
REDDITS = {
    "netsec": "https://www.reddit.com/r/netsec/.rss",
    "netsecstudents": "https://www.reddit.com/r/netsecstudents/.rss",
    "hacking": "https://www.reddit.com/r/hacking/.rss",
    "cybersecurity": "https://www.reddit.com/r/cybersecurity/.rss",
    "bugbounty": "https://www.reddit.com/r/bugbounty/.rss",
}

def scrape_reddit(db: IntelDB) -> dict[str, int]:
    results = {}
    for name, rss_url in REDDITS.items():
        count = 0
        data = _fetch(rss_url)
        if not data:
            results[name] = 0
            continue
        items = re.findall(r'<entry>(.*?)</entry>', data, re.DOTALL)
        for item in items[:15]:
            title_m = re.search(r'<title[^>]*>(.*?)</title>', item)
            link_m = re.search(r'<link[^>]*href="([^"]+)"', item)
            title = title_m.group(1).strip() if title_m else ""
            link = link_m.group(1) if link_m else ""
            if not title:
                continue
            cve_refs = _cves(title)
            tags = [f"Reddit/{name}"]
            if cve_refs:
                tags.append("CVE")
            if db.add_news(f"reddit-{name}", link, title,
                           tags=tags, cve_refs=cve_refs):
                count += 1
        results[name] = count
    return results


# ── Source: Telegram Channel Scraper (via nitter/public RSS) ────────────────
TELEGRAM_FEEDS = {
    "vxunderground": "https://nitter.net/vxunderground/rss",
    "pwnallthethings": "https://nitter.net/PwnAllTheThings/rss",
    "binitamshah": "https://nitter.net/binitamshah/rss",
    "0xor0ne": "https://nitter.net/0xor0ne/rss",
}

def scrape_security_x(db: IntelDB) -> dict[str, int]:
    results = {}
    for name, rss_url in TELEGRAM_FEEDS.items():
        count = 0
        data = _fetch(rss_url, timeout=15)
        if not data:
            for fallback in ["https://nitter.poast.org", "https://nitter.1d4.us"]:
                alt = rss_url.replace("https://nitter.net", fallback)
                data = _fetch(alt, timeout=10)
                if data:
                    break
        if not data:
            results[name] = 0
            continue
        items = re.findall(r'<entry>(.*?)</entry>', data, re.DOTALL) or \
                re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
        for item in items[:15]:
            title_m = re.search(r'<title[^>]*>(.*?)</title>', item)
            link_m = re.search(r'<link[^>]*href="([^"]+)"', item)
            title = title_m.group(1).strip() if title_m else ""
            link = link_m.group(1) if link_m else ""
            if not title:
                continue
            cve_refs = _cves(title)
            tags = [f"x/{name}"]
            if cve_refs:
                tags.append("CVE")
            if db.add_news(f"x-{name}", link, title, tags=tags, cve_refs=cve_refs):
                count += 1
        results[name] = count
    return results


# ── All Web Scrapers ────────────────────────────────────────────────────────

def scrape_all_web(db: IntelDB, verbose: bool = True) -> dict[str, int]:
    results = {}

    scrapers = [
        ("The Hacker News", lambda: scrape_thn(db)),
        ("BleepingComputer", lambda: scrape_bleeping(db)),
        ("GBHackers", lambda: scrape_gbhackers(db)),
        ("PacketStorm", lambda: scrape_packetstorm(db)),
    ]
    for name, fn in scrapers:
        if verbose:
            print(f"  {Fmt.bold(name)} ...", end=" ", flush=True)
        try:
            c = fn()
            results[name] = c
            if verbose:
                print(f"{Fmt.green(f'{c} new') if c else Fmt.dim('no new')}")
        except Exception as e:
            if verbose:
                print(f"{Fmt.red(f'error: {e}')}")
            results[name] = 0

    if verbose:
        print(f"  {Fmt.bold('Reddit')} ...")
    reddit_results = scrape_reddit(db)
    for name, c in reddit_results.items():
        results[f"Reddit/{name}"] = c
        if verbose:
            print(f"    {Fmt.dim(name)}: {Fmt.green(str(c)) if c else Fmt.dim('0')}")

    if verbose:
        print(f"  {Fmt.bold('Security X/Twitter')} ...")
    x_results = scrape_security_x(db)
    for name, c in x_results.items():
        results[f"x/{name}"] = c
        if verbose:
            print(f"    {Fmt.dim(name)}: {Fmt.green(str(c)) if c else Fmt.dim('0')}")

    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Cyassist web scraper")
    p.add_argument("--list", action="store_true", help="List sources")
    args = p.parse_args()

    if not IntelDB:
        print("Error: intel_db.py required")
        sys.exit(1)

    db = IntelDB()
    if args.list:
        print("Web scraper sources:")
        print("  - The Hacker News")
        print("  - BleepingComputer")
        print("  - GBHackers")
        print("  - PacketStorm")
        print("  - Reddit (netsec, hacking, cybersecurity, bugbounty)")
        print("  - X/Twitter (vxunderground, PwnAllTheThings, binitamshah, 0xor0ne)")
    else:
        print(f"  {Fmt.bold('Web scraper')}")
        results = scrape_all_web(db)
        total = sum(results.values())
        print(f"  {Fmt.green(f'Total: {total} new articles')}  "
              f"{Fmt.dim(f'(DB: {db.size_mb():.2f}MB)')}")
    db.close()
