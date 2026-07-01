"""Phase 2: On-demand report extraction and attack DNA vector generation.

Fetches single report body over HTTP, tokenizes in-memory,
builds attack DNA, discards body. Never stores body text.
"""

import re
import sys
import time
import urllib.request
import urllib.error
from typing import Optional

from .storage import MetadataStore, ReportMeta
from .tokenizer import InMemoryTokenizer
from .filter_handler import FilterHandler
from .attack_dna import AttackDNAExporter


class OnDemandExtractor:
    """Fetch, tokenize, classify, and export attack DNA for a report."""

    H1_REPORT_URL = (
        "https://raw.githubusercontent.com/ajaysenr/"
        "HackerOne-Disclosed-Reports/main/reports/{id}.md"
    )

    def __init__(self, store: MetadataStore, dna_dir: str = None, verbose: bool = False):
        self.store = store
        self.verbose = verbose
        self.tokenizer = InMemoryTokenizer()
        self.filter = FilterHandler()
        self.dna = AttackDNAExporter(output_dir=dna_dir)

    def _fetch_body(self, url: str, timeout: int = 20) -> Optional[str]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Cyassist-Engine/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, urllib.error.HTTPError, Exception):
            return None

    def extract_by_url(self, url: str) -> Optional[dict]:
        """Fetch a report by URL, tokenize in-memory, build DNA vector."""
        body = self._fetch_body(url)
        if not body:
            return None
        tokenized = self.tokenizer.tokenize(body, url=url)
        u = url[:500]
        meta_dict = {"url": u, "report_id": url.rstrip("/").split("/")[-1], "source": "hackerone"}
        categories = self.filter.classify(tokenized, meta_dict)
        vector = self.dna.build_vector(meta_dict, tokenized, categories)
        self.dna.save_vector(vector)
        if self.verbose:
            cwes = "; ".join(tokenized.get("cwe_matches", [])) or "?"
            print(f"  Extracted: {cwes} | {len(tokenized.get('endpoints', []))} endpoints "
                  f"| {len(tokenized.get('parameters', []))} params")
        return vector

    def extract_by_report_id(self, report_id: str) -> Optional[dict]:
        """Fetch a report by numeric H1 ID."""
        url = self.H1_REPORT_URL.format(id=report_id)
        return self.extract_by_url(url)

    def extract_all(self, limit: int = 20) -> list[dict]:
        """Walk store, extract attack DNA for reports not yet processed."""
        vectors = []
        for meta in self.store.list_all():
            if len(vectors) >= limit:
                break
            url = meta.url
            name = self._vector_name(meta)
            dna_path = self.dna.output_dir / name
            if dna_path.exists():
                continue
            body = self._fetch_body(url)
            if not body:
                continue
            tokenized = self.tokenizer.tokenize(body, url=url)
            meta_dict = {"url": url, "report_id": self._report_id(url), "source": meta.source}
            categories = self.filter.classify(tokenized, meta_dict)
            vector = self.dna.build_vector(meta_dict, tokenized, categories)
            self.dna.save_vector(vector)
            vectors.append(vector)
            if self.verbose:
                print(f"  [{len(vectors)}] {meta.title[:50]}")
        return vectors

    def _report_id(self, url: str) -> str:
        return url.rstrip("/").split("/")[-1]

    def _vector_name(self, meta: ReportMeta) -> str:
        h = meta.id[:12]
        return f"dna_{h}.json"

    def build_catalog(self) -> str:
        vectors = self.dna.collect_all()
        if not vectors:
            vectors = self.extract_all(limit=50)
        if vectors:
            return self.dna.export_catalog(vectors)
        return ""
