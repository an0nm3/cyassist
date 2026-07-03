#!/usr/bin/env python3
"""Cyassist India scraper — fetch Indian cybersecurity news from CERT-In, NCIIPC, Indian media.

Scrapes sources that lack RSS feeds or need web scraping for full content.
Stores articles in the same format as reader.py expects.
"""

import datetime
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent
NEWS_DIR = HERE / "news" / "rss"

USER_AGENT = "cyassist-india-scraper/1.0"


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


def _fetch(url: str, timeout: int = 20) -> Optional[str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def _save(source: str, title: str, url: str, body: str, tags: list, date_str: str = None):
    dir_path = NEWS_DIR / source / (date_str or datetime.datetime.now().strftime("%Y-%m-%d"))
    dir_path.mkdir(parents=True, exist_ok=True)
    uid = hashlib.md5(f"{source}:{title}:{url}".encode()).hexdigest()[:12]
    fname = dir_path / f"{uid}.md"
    if fname.exists():
        return False
    d = date_str or datetime.datetime.now().strftime("%Y-%m-%d")
    tag_str = ", ".join(tags)
    content = f"""---
source: rss/{source}
title: "{title}"
url: "{url}"
date: "{d}"
item_id: "{url}"
category: news
tags: [{tag_str}]
---
{body.strip()[:2000]}"""
    fname.write_text(content)

    try:
        from intel_db import IntelDB
        _db = IntelDB()
        _db.add_news(source, url, title, tags=tags, date_str=d)
        _db.close()
    except Exception:
        pass
    return True


# ── Source: CERT-In Advisories ─────────────────────────────────────────────
CERT_IN_URL = "https://www.cert-in.org.in/sitemap.xml"
CERT_IN_ADVISORY_PATTERN = re.compile(r"/advisory/(CERT-In-\d+[^<]+)", re.I)

def scrape_cert_in() -> int:
    """Scrape CERT-In advisory pages via their sitemap."""
    count = 0
    html = _fetch("https://www.cert-in.org.in/CERT-In-Advisories.html")
    if not html:
        print(f"  {Fmt.dim('CERT-In: fetch failed')}")
        return 0
    links = re.findall(r'<a\s+href="(/advisory/[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    print(f"  {Fmt.dim(f'CERT-In: {len(links)} advisories found')}")
    for href, title_text in links[:20]:
        full_url = f"https://www.cert-in.org.in{href}"
        title = re.sub(r'<[^>]+>', '', title_text).strip()
        if not title:
            title = f"CERT-In Advisory {href.split('/')[-1]}"
        advisory_html = _fetch(full_url)
        body = ""
        if advisory_html:
            body_text = re.sub(r'<[^>]+>', ' ', advisory_html)
            body = ' '.join(body_text.split())[:1000]
        tags = ["CERT-In", "Advisory", "India"]
        cve_match = re.search(r'CVE-\d{4}-\d{4,}', f"{title} {body}")
        if cve_match:
            tags.append(f"CVE:{cve_match.group(0)}")
        if _save("cert-in", title, full_url, body, tags):
            count += 1
    return count


# ── Source: ET CISO (additional scraping for full content) ─────────────────
ECONOTIMES_CISO = "https://ciso.economictimes.indiatimes.com"

def scrape_et_ciso() -> int:
    """Scrape ET CISO (Economic Times CISO) for Indian security news."""
    count = 0
    html = _fetch(f"{ECONOTIMES_CISO}/latest-news")
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(/news/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles[:15]:
        if href in seen:
            continue
        seen.add(href)
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title or len(title) < 10:
            continue
        full_url = f"{ECONOTIMES_CISO}{href}"
        tags = ["CISO", "India", "IndianEnterprise"]
        # Check for CVEs in title
        if re.search(r'CVE-\d{4}-\d{4,}', title):
            tags.append("CVE")
        if _save("et-ciso", title, full_url, "", tags):
            count += 1
    return count


# ── Source: Quick Heal Blog ────────────────────────────────────────────────
def scrape_quickheal() -> int:
    """Scrape Quick Heal Security Blog."""
    count = 0
    html = _fetch("https://blogs.quickheal.com/")
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(https?://blogs\.quickheal\.com/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles:
        if href in seen:
            continue
        seen.add(href)
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title or len(title) < 5:
            continue
        tags = ["QuickHeal", "India"]
        if _save("quickheal-blog", title, href, "", tags):
            count += 1
    return count


# ── Source: Cyble Blog (Indian org, global threat intel) ──────────────────
CYBLE_BLOG = "https://blog.cyble.com"

def scrape_cyble() -> int:
    """Scrape Cyble blog for Indian-relevant threat intel."""
    count = 0
    html = _fetch(f"{CYBLE_BLOG}")
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(https?://blog\.cyble\.com/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles:
        if href in seen:
            continue
        seen.add(href)
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title or len(title) < 5:
            continue
        tags = ["Cyble", "India", "ThreatIntel"]
        if re.search(r'CVE-\d{4}-\d{4,}', title):
            tags.append("CVE")
        if _save("cyble-blog", title, href, "", tags):
            count += 1
    return count


# ── Source: Seqrite Blog ───────────────────────────────────────────────────
SEQRITE_BLOG = "https://www.seqrite.com/blog"

def scrape_seqrite() -> int:
    """Scrape Seqrite (Indian enterprise security) blog."""
    count = 0
    html = _fetch(SEQRITE_BLOG)
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(https?://www\.seqrite\.com/blog/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles:
        if href in seen:
            continue
        seen.add(href)
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title or len(title) < 5:
            continue
        tags = ["Seqrite", "India"]
        if _save("seqrite-blog", title, href, "", tags):
            count += 1
    return count


# ── Source: Payatu Blog ────────────────────────────────────────────────────
def scrape_payatu() -> int:
    """Scrape Payatu (Indian security research) blog."""
    count = 0
    html = _fetch("https://payatu.com/blog/")
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(https?://payatu\.com/blog/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles:
        if href in seen:
            continue
        seen.add(href)
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title or len(title) < 5:
            continue
        tags = ["Payatu", "India", "Research"]
        if _save("payatu-blog", title, href, "", tags):
            count += 1
    return count


# ── Source: CloudSEK Blog ─────────────────────────────────────────────────
def scrape_cloudsek() -> int:
    """Scrape CloudSEK (Indian cyber threat intel) blog."""
    count = 0
    html = _fetch("https://cloudsek.com/blog")
    if not html:
        return 0
    articles = re.findall(
        r'<a\s+href="(https?://cloudsek\.com/[^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    seen = set()
    for href, title_html in articles:
        if href in seen:
            continue
        seen.add(href)
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        if not title or len(title) < 5:
            continue
        tags = ["CloudSEK", "India", "ThreatIntel"]
        body = ""
        art_html = _fetch(href)
        if art_html:
            body = ' '.join(re.sub(r'<[^>]+>', ' ', art_html).split()[:300])
        if _save("cloudsek-blog", title, href, body, tags):
            count += 1
    return count


# ── Source: RBI/SEBI Advisories ────────────────────────────────────────────
def scrape_rbi_advisories() -> int:
    """Scrape RBI cybersecurity advisories and circulars."""
    count = 0
    for feed_url in [
        "https://www.rbi.org.in/rss/rssmain.aspx",
    ]:
        data = _fetch(feed_url)
        if not data:
            continue
        items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
        for item in items[:10]:
            title_m = re.search(r'<title[^>]*>(.*?)</title>', item)
            link_m = re.search(r'<link[^>]*>(.*?)</link>', item)
            desc_m = re.search(r'<description[^>]*>(.*?)</description>', item)
            title = title_m.group(1).strip() if title_m else ""
            link = link_m.group(1).strip() if link_m else ""
            desc = desc_m.group(1).strip() if desc_m else ""
            if not title:
                continue
            lower = f"{title} {desc}".lower()
            if not any(kw in lower for kw in ["cyber", "security", "fraud", "digital", "data", "it act"]):
                continue
            tags = ["RBI", "India", "Regulation"]
            if _save("rbi-advisories", title, link, desc[:500], tags):
                count += 1
    return count


# ── All India scrapers ──────────────────────────────────────────────────────
INDIA_SCRAPERS = [
    ("CERT-In", scrape_cert_in),
    ("ET CISO", scrape_et_ciso),
    ("Quick Heal", scrape_quickheal),
    ("Cyble Blog", scrape_cyble),
    ("Seqrite Blog", scrape_seqrite),
    ("Payatu Blog", scrape_payatu),
    ("CloudSEK Blog", scrape_cloudsek),
    ("RBI Advisories", scrape_rbi_advisories),
]


def scrape_all_india(verbose: bool = True) -> dict[str, int]:
    """Run all Indian news scrapers. Returns {source_name: articles_saved}."""
    results = {}
    for name, scraper_fn in INDIA_SCRAPERS:
        if verbose:
            print(f"  {Fmt.bold(name)} ...", end=" ", flush=True)
        try:
            count = scraper_fn()
            results[name] = count
            if verbose:
                if count:
                    print(f"{Fmt.green(f'{count} new')}")
                else:
                    print(f"{Fmt.dim('no new')}")
        except Exception as e:
            if verbose:
                print(f"{Fmt.red(f'error: {e}')}")
            results[name] = 0
    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Cyassist India scraper")
    p.add_argument("--list", action="store_true", help="List India scraper sources")
    args = p.parse_args()
    if args.list:
        print("India sources:")
        for name, _ in INDIA_SCRAPERS:
            print(f"  - {name}")
    else:
        print(f"  {Fmt.bold('India news scraper')}")
        results = scrape_all_india()
        total = sum(results.values())
        print(f"  {Fmt.green(f'Total: {total} new articles')}")
