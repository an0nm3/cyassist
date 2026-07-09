#!/usr/bin/env python3
"""India news backfill — fetch 2 weeks of Indian cybersecurity articles with dates."""
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
NEWS_DIR = HERE / "news" / "rss"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 cyassist-backfill/1.0"
NOW = datetime.datetime.now()

INDIA_RSS = {
    "toi-tech": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
    "indian-express-tech": "https://indianexpress.com/section/technology/feed/",
    "inc42": "https://inc42.com/feed/",
    "yourstory": "https://yourstory.com/feed",
    "medianama": "https://www.medianama.com/feed/",
    "et-ciso": "https://ciso.economictimes.indiatimes.com/rss/topstories",
    "cso-india": "https://www.csoonline.com/in/feed/",
    "k7-computing": "https://blog.k7computing.com/feed/",
    "google-news-india-cyber": "https://news.google.com/rss/search?q=cybersecurity+India&hl=en-IN&gl=IN&ceid=IN:en",
    "google-news-india-data-breach": "https://news.google.com/rss/search?q=data+breach+India&hl=en-IN&gl=IN&ceid=IN:en",
    "google-news-india-hacking": "https://news.google.com/rss/search?q=hacking+India&hl=en-IN&gl=IN&ceid=IN:en",
    "google-news-india-fintech": "https://news.google.com/rss/search?q=fintech+security+India&hl=en-IN&gl=IN&ceid=IN:en",
    "google-news-india-advisory": "https://news.google.com/rss/search?q=CERT-In+advisory&hl=en-IN&gl=IN&ceid=IN:en",
}

def fmt(s, c=0):
    if not sys.stdout.isatty():
        return s
    return f"\033[{c}m{s}\033[0m" if c else s

def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None

def save(source, title, url, body, tags, date_str):
    d = date_str or NOW.strftime("%Y-%m-%d")
    dir_path = NEWS_DIR / source / d
    dir_path.mkdir(parents=True, exist_ok=True)
    uid = hashlib.md5(f"{source}:{title}:{url}".encode()).hexdigest()[:12]
    fname = dir_path / f"{uid}.md"
    if fname.exists():
        return False
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
    return True

def parse_date(raw):
    if not raw:
        return None
    raw = raw.strip()
    # Normalize timezone names to +0000
    raw = re.sub(r"\bGMT\b", "+0000", raw)
    raw = re.sub(r"\bUTC\b", "+0000", raw)
    raw = re.sub(r"\bIST\b", "+0530", raw)
    raw = re.sub(r"\bCEST\b", "+0200", raw)
    raw = re.sub(r"\bCET\b", "+0100", raw)
    raw = re.sub(r"\bEST\b", "-0500", raw)
    raw = re.sub(r"\bEDT\b", "-0400", raw)
    raw = re.sub(r"\bPST\b", "-0800", raw)
    raw = re.sub(r"\bPDT\b", "-0700", raw)
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S",
        "%Y-%m-%d",
    ]
    for f in formats:
        try:
            return datetime.datetime.strptime(str(raw[:40]), f).strftime("%Y-%m-%d")
        except ValueError:
            continue
    m = re.search(r"(\d{4}-\d{2}-\d{2})", raw)
    return m.group(1) if m else None

def backfill_rss():
    total = 0
    for name, url in INDIA_RSS.items():
        data = fetch(url)
        if not data:
            print(f"  {fmt('✗', 31)} {name}: fetch failed")
            continue
        entries = re.findall(r"<item\b[^>]*>(.*?)</item>", data, re.DOTALL)
        if not entries:
            entries = re.findall(r"<entry\b[^>]*>(.*?)</entry>", data, re.DOTALL)
        count = 0
        for entry in entries:
            title_m = re.search(r"<title[^>]*>(.*?)</title>", entry, re.DOTALL)
            link_m = re.search(r"<link[^>]*href=\"([^\"]+)\"", entry) or \
                     re.search(r"<link[^>]*>(.*?)</link>", entry)
            pub_m = re.search(r"<published[^>]*>(.*?)</published>", entry) or \
                    re.search(r"<pubDate[^>]*>(.*?)</pubDate>", entry) or \
                    re.search(r"<dc:date[^>]*>(.*?)</dc:date>", entry) or \
                    re.search(r"<updated[^>]*>(.*?)</updated>", entry)
            desc_m = re.search(r"<description[^>]*>(.*?)</description>", entry, re.DOTALL)
            content_m = re.search(r"<content:encoded[^>]*>(.*?)</content:encoded>", entry, re.DOTALL)
            title = title_m.group(1).strip() if title_m else ""
            title = title.replace("<![CDATA[", "").replace("]]>", "")
            title = title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
            link = link_m.group(1).strip() if link_m and link_m.group(1) else ""
            link = re.sub(r"^<!\[CDATA\[", "", link)
            link = re.sub(r"\]\]>$", "", link)
            pub_raw = pub_m.group(1).strip() if pub_m else ""
            date_str = parse_date(pub_raw) or NOW.strftime("%Y-%m-%d")
            # Skip articles older than 30 days (within range, not too old)
            try:
                if date_str:
                    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    if (NOW - dt).days > 30:
                        continue
            except ValueError:
                pass
            body = ""
            raw_body = (content_m or desc_m)
            if raw_body:
                raw = raw_body.group(1)
                raw = raw.replace("<![CDATA[", "").replace("]]>", "")
                raw = re.sub(r"<[^>]+>", "", raw)
                raw = raw.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                raw = " ".join(raw.split()).strip()[:1000]
                body = raw
            cves = re.findall(r"CVE-\d{4}-\d{4,}", title + " " + body)
            tags = [name] + [f"CVE:{c}" for c in cves[:3]]
            if save(name, title, link or url, body, tags, date_str):
                count += 1
        total += count
        status = fmt(f"{count} new", 32) if count else fmt("0 new", 2)
        print(f"  {fmt('✓', 32)} {name}: {status}")
    print(f"\n  {fmt(f'RSS total: {total} new articles', 1)}")
    return total

def main():
    import argparse
    p = argparse.ArgumentParser(description="India news backfill")
    p.add_argument("--days", type=int, default=14, help="Days to go back (default: 14)")
    p.add_argument("--run-scrapers", action="store_true", help="Also run India scrapers")
    args = p.parse_args()
    
    print(f"  {fmt('India news backfill', 1)} — fetching last {args.days} days")
    print()
    total = backfill_rss()
    
    if args.run_scrapers:
        print(f"\n  {fmt('Running India scrapers...', 1)}")
        try:
            from scraper_india import scrape_all_india
            results = scrape_all_india(verbose=True)
            total += sum(results.values())
        except ImportError:
            print(f"  {fmt('scraper_india.py not found, skipping', 33)}")
        except Exception as e:
            print(f"  {fmt(f'scraper error: {e}', 31)}")
    
    print(f"\n  {fmt(f'Grand total: {total} new articles', 1)}")

if __name__ == "__main__":
    main()
