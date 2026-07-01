"""Phase 1: Remote index ingestion from community-curated sources.

Sources:
- ajaysenr/HackerOne-Disclosed-Reports (index.json)
- sayan011/Immunefi-bug-bounty-writeups-list (README.md)
- Medium/RSS aggregators (infosec-writeups, etc.)

Never scrapes platforms directly - uses GitHub-hosted indexes only.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
import urllib.request
import urllib.error

from .storage import MetadataStore


class IndexSyncer:
    """Sync bug bounty report indexes from remote sources."""
    
    # HackerOne disclosed reports index
    H1_INDEX_URL = "https://raw.githubusercontent.com/ajaysenr/HackerOne-Disclosed-Reports/main/index.json"
    
    # Immunefi writeups (parsed from README)
    IMMUNEFI_README_URL = "https://raw.githubusercontent.com/sayan011/Immunefi-bug-bounty-writeups-list/main/README.md"
    
    # Medium/Feedly aggregators (RSS)
    MEDIUM_FEEDS = [
        "https://infosec-writeups.com/feed",
        "https://medium.com/feed/tag/hackernoon",
        "https://medium.com/feed/tag/bugbounty",
    ]
    
    def __init__(self, store: MetadataStore, verbose: bool = False):
        self.store = store
        self.verbose = verbose
    
    def _fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """Fetch URL content with error handling."""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Cyassist-Engine/1.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
            if self.verbose:
                print(f"  [!] Failed to fetch {url}: {e}", file=sys.stderr)
            return None
    
    def sync_hackerone(self) -> int:
        """Sync HackerOne disclosed reports index."""
        if self.verbose:
            print(f"[*] Syncing HackerOne index...")
        
        content = self._fetch_url(self.H1_INDEX_URL)
        if not content:
            return 0
        
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            if self.verbose:
                print("  [!] Invalid JSON in H1 index", file=sys.stderr)
            return 0
        
        added = 0
        reports = data if isinstance(data, list) else data.get("reports", [])
        for report in reports:
            url = report.get("url")
            if not url:
                continue
            
            # Extract metadata from report structure
            title = report.get("title", "Untitled")
            cwe_raw = report.get("cwe") or report.get("weakness") or ""
            if isinstance(cwe_raw, dict):
                cwe_raw = cwe_raw.get("name", "")
            cwe = str(cwe_raw) or None
            cve = None
            cve_ids = report.get("cve_ids", [])
            if cve_ids:
                cve = "; ".join(cve_ids)
            platform = report.get("program") or report.get("platform")
            vuln_type = report.get("vulnerability_type") or report.get("severity")
            if isinstance(vuln_type, dict):
                vuln_type = vuln_type.get("rating", "")
            timestamp = report.get("disclosed_at") or report.get("reported_at") or report.get("published_at")
            tags = report.get("tags", [])
            
            key = self.store.add(
                url=url,
                source="h1",
                title=title,
                cwe=cwe,
                cve=cve,
                platform=platform,
                vulnerability_type=vuln_type,
                timestamp=timestamp,
                tags=tags
            )
            added += 1
        
        if self.verbose:
            print(f"  [+] Added {added} H1 reports")
        return added
    
    def sync_immunefi(self) -> int:
        """Sync Immunefi writeups from README markdown."""
        if self.verbose:
            print(f"[*] Syncing Immunefi index...")
        
        content = self._fetch_url(self.IMMUNEFI_README_URL)
        if not content:
            return 0
        
        # Parse markdown table/link format
        # Expected format: [Title](URL) - CWE-XXX - Platform
        pattern = r'\[([^\]]+)\]\(([^)]+)\)\s*[-–]\s*(CWE-\d+)?\s*[-–]?\s*(\w+)?'
        matches = re.findall(pattern, content)
        
        added = 0
        for title, url, cwe, platform in matches:
            if not url or "immunefi" not in url.lower():
                continue
            
            key = self.store.add(
                url=url,
                source="immunefi",
                title=title.strip(),
                cwe=cwe,
                platform=platform
            )
            added += 1
        
        if self.verbose:
            print(f"  [+] Added {added} Immunefi reports")
        return added
    
    def sync_medium_feeds(self) -> int:
        """Sync Medium/RSS aggregator feeds."""
        added = 0
        
        for feed_url in self.MEDIUM_FEEDS:
            if self.verbose:
                print(f"[*] Fetching feed: {feed_url}")
            
            content = self._fetch_url(feed_url)
            if not content:
                continue
            
            # Parse RSS/Atom XML
            # Simple extraction: <title>...</title><link>...</link>
            title_pattern = r'<title[^>]*>([^<]+)</title>'
            link_pattern = r'<link[^>]*href="([^"]+)"'
            
            titles = re.findall(title_pattern, content)
            links = re.findall(link_pattern, content)
            
            for title, link in zip(titles[1:], links):  # Skip first title (feed name)
                if "medium.com" not in link:
                    continue
                
                # Extract tags from URL or content
                tags = []
                if "/tag/" in link:
                    tags = re.findall(r'/tag/([^/]+)', link)
                
                key = self.store.add(
                    url=link,
                    source="medium",
                    title=title.strip(),
                    tags=tags
                )
                added += 1
        
        if self.verbose:
            print(f"  [+] Added {added} Medium/RSS reports")
        return added
    
    def sync_all(self) -> Dict[str, int]:
        """Sync all sources."""
        if self.verbose:
            print("[*] Starting full index sync...")
            print(f"    Current store size: {self.store.count()} reports")
        
        results = {
            "hackerone": self.sync_hackerone(),
            "immunefi": self.sync_immunefi(),
            "medium": self.sync_medium_feeds(),
        }
        
        # Persist
        self.store.close()
        
        if self.verbose:
            total = sum(results.values())
            print(f"[*] Sync complete: +{total} new reports")
            print(f"    Total store size: {self.store.count()} reports")
            print(f"    Storage size: {self.store.size_mb():.2f} MB")
        
        return results