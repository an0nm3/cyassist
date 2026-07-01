"""Cyassist Engine - Lean data engine for bug bounty report analysis.

Phase 1: Index Syncer (remote ingestion from community indexes)
Phase 2: On-Demand Extractor (fetch + analyze report URLs)

Usage:
    python3 engine/__init__.py sync          # Sync all indexes
    python3 engine/__init__.py filter --web2 # Filter Web2 reports
    python3 engine/__init__.py dna --all     # Export attack DNA vectors
    python3 engine/__init__.py extract <url> # Fetch single report
"""

from .storage import MetadataStore
from .index_syncer import IndexSyncer
from .tokenizer import InMemoryTokenizer
from .filter_handler import FilterHandler
from .attack_dna import AttackDNAExporter
from .extractor import OnDemandExtractor

__version__ = "1.0.0"
__all__ = [
    "MetadataStore",
    "IndexSyncer", 
    "InMemoryTokenizer",
    "FilterHandler",
    "AttackDNAExporter",
    "OnDemandExtractor",
]