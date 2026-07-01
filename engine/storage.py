"""Minimal metadata store for bug bounty reports (<2MB for 10K reports).

Uses shelve for key-value storage with automatic deduplication via hash keys.
Stores only indexed metadata - never full report bodies.
"""

import hashlib
import shelve
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ReportMeta:
    """Minimal report metadata - never stores body text."""
    id: str  # Hash of URL or report_id
    url: str
    source: str  # "h1", "immunefi", "medium"
    title: str
    cwe: Optional[str] = None
    cve: Optional[str] = None
    platform: Optional[str] = None
    vulnerability_type: Optional[str] = None
    timestamp: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class MetadataStore:
    """In-memory + shelve-backed metadata store."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = ".engine_metadata"
        self.db_path = Path(db_path)
        self._cache: Dict[str, ReportMeta] = {}
        self._load()
    
    def _load(self):
        """Load existing metadata from shelve."""
        if self.db_path.exists():
            with shelve.open(str(self.db_path)) as db:
                for key, value in db.items():
                    self._cache[key] = ReportMeta(**value)
    
    def _save(self):
        """Persist cache to shelve."""
        with shelve.open(str(self.db_path)) as db:
            for key, meta in self._cache.items():
                db[key] = asdict(meta)
    
    def _hash_key(self, url: str) -> str:
        """Generate consistent hash key from URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    def add(self, url: str, source: str, title: str, **kwargs) -> str:
        """Add report metadata. Returns hash key."""
        key = self._hash_key(url)
        
        # Skip if already exists (dedup)
        if key in self._cache:
            return key
        
        meta = ReportMeta(
            id=key,
            url=url,
            source=source,
            title=title,
            **kwargs
        )
        self._cache[key] = meta
        return key
    
    def get(self, key: str) -> Optional[ReportMeta]:
        """Get report by hash key."""
        return self._cache.get(key)
    
    def get_by_url(self, url: str) -> Optional[ReportMeta]:
        """Get report by URL."""
        key = self._hash_key(url)
        return self._cache.get(key)
    
    def list_all(self) -> List[ReportMeta]:
        """List all stored reports."""
        return list(self._cache.values())
    
    def count(self) -> int:
        """Total report count."""
        return len(self._cache)
    
    def size_mb(self) -> float:
        """Estimate storage size in MB."""
        if not self.db_path.exists():
            return 0.0
        return self.db_path.stat().st_size / (1024 * 1024)
    
    def search(self, cwe: Optional[str] = None, 
               vuln_type: Optional[str] = None,
               source: Optional[str] = None) -> List[ReportMeta]:
        """Search reports by metadata fields."""
        results = []
        for meta in self._cache.values():
            if cwe and meta.cwe != cwe:
                continue
            if vuln_type and meta.vulnerability_type != vuln_type:
                continue
            if source and meta.source != source:
                continue
            results.append(meta)
        return results
    
    def close(self):
        """Persist and close."""
        self._save()