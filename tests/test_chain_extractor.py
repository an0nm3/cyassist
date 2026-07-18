"""Tests for cyassist/engine/chain_extractor.py — ChainPattern, ChainIndex, H1 parser."""

import tempfile

from engine.chain_extractor import (
    ChainPattern,
    ChainIndex,
    extract_chains_from_report,
    _HARDCODED_PATTERNS,
)


# ── ChainPattern Tests ─────────────────────────────────────────────────


def test_chain_pattern_defaults():
    p = ChainPattern(
        primitive_a="xss",
        primitive_b="csrf",
        impact="XSS bypasses CSRF protections",
    )
    assert p.sink_a == "xss_reflected"
    assert p.sink_b == "cors_misconfig"
    assert p.cvss_bump == 1.0
    assert p.source_platform == "seed"
    assert p.created_at != ""


def test_chain_pattern_key_order_independent():
    p1 = ChainPattern("xss", "csrf", "impact")
    p2 = ChainPattern("csrf", "xss", "impact")
    assert p1.key() == p2.key()


def test_chain_pattern_to_row_roundtrip():
    p = ChainPattern(
        primitive_a="ssrf",
        primitive_b="cloud_metadata",
        impact="SSRF to cloud metadata leaks credentials",
        conditions=["IMDSv1 enabled", "no metadata block"],
        cvss_bump=3.5,
        source_url="https://h1.com/reports/123",
        source_platform="seed",
    )
    row = p.to_row()
    assert row["primitive_a"] == "ssrf"
    assert row["cvss_bump"] == 3.5
    assert "IMDSv1 enabled" in row["conditions"]


# ── ChainIndex Tests ───────────────────────────────────────────────────


def test_chain_index_seeds_loaded():
    idx = ChainIndex(db_path=":memory:")
    assert idx.count() == len(_HARDCODED_PATTERNS)
    assert idx.count() >= 15


def test_chain_index_lookup():
    idx = ChainIndex(db_path=":memory:")
    p = idx.lookup("open_redirect", "oauth_misconfig")
    assert p is not None
    assert "OAuth" in p.impact
    assert p.cvss_bump == 3.0


def test_chain_index_lookup_order_independent():
    idx = ChainIndex(db_path=":memory:")
    p1 = idx.lookup("ssrf", "cloud_metadata")
    p2 = idx.lookup("cloud_metadata", "ssrf")
    assert p1 is not None
    assert p2 is not None
    assert p1.key() == p2.key()


def test_chain_index_lookup_by_sink():
    idx = ChainIndex(db_path=":memory:")
    results = idx.lookup_by_sink("ssrf_reflected")
    # ssrf appears in multiple chain patterns
    assert len(results) >= 2


def test_chain_index_lookup_missing():
    idx = ChainIndex(db_path=":memory:")
    p = idx.lookup("nonexistent_a", "nonexistent_b")
    assert p is None


def test_chain_index_add_new():
    idx = ChainIndex(db_path=":memory:")
    initial = idx.count()
    p = ChainPattern(
        "xss", "sqli", "Custom test chain",
        source_platform="test",
    )
    added = idx.add(p)
    assert added is True
    assert idx.count() == initial + 1


def test_chain_index_add_duplicate():
    idx = ChainIndex(db_path=":memory:")
    p = ChainPattern(
        "xss", "sqli", "Custom test chain",
        source_platform="test",
    )
    idx.add(p)
    added = idx.add(p)
    assert added is False


def test_chain_index_stats():
    idx = ChainIndex(db_path=":memory:")
    s = idx.stats()
    assert s["total"] == len(_HARDCODED_PATTERNS)
    assert "seed" in s["by_source"]


# ── H1 Report Parser Tests ─────────────────────────────────────────────


def test_extract_no_chain_signal():
    text = "This report is about a simple XSS vulnerability in the search endpoint."
    results = extract_chains_from_report(text)
    assert len(results) == 0


def test_extract_chain_from_report():
    text = """
    ## Summary
    I found a stored XSS and CSRF vulnerability that can be chained together.
    
    ## Impact
    The XSS combined with missing CSRF token on the password change endpoint
    allows an attacker to change the victim's password without their consent.
    """
    results = extract_chains_from_report(text, source_url="https://h1.com/1")
    assert len(results) >= 1
    # Should detect xss + csrf
    primitives = {r.primitive_a for r in results} | {r.primitive_b for r in results}
    assert "xss" in primitives
    assert "csrf" in primitives


def test_extract_chain_with_two_cwes():
    text = """
    This report describes CWE-79 (XSS) and CWE-918 (SSRF) chained to achieve RCE.
    The attacker can combine these vulnerabilities to execute arbitrary code.
    """
    results = extract_chains_from_report(text)
    assert len(results) >= 1


def test_extract_chain_via_escalation():
    text = """
    This IDOR vulnerability can be escalated to account takeover.
    The attacker iterates user IDs to dump all records.
    """
    results = extract_chains_from_report(text)
    # IDOR + information_disclosure should be detected
    assert len(results) >= 1


def test_add_from_report():
    idx = ChainIndex(db_path=":memory:")
    initial = idx.count()
    text = """
    Chained vulnerability: XSS with OAuth misconfig.
    The stored XSS on the profile page combined with OAuth token stored in
    localStorage allows an attacker to steal the access token.
    """
    added = idx.add_from_report(text, source_url="https://h1.com/report/1")
    assert added >= 1
    assert idx.count() == initial + added


# ── Integration: Full Persistence ──────────────────────────────────────


def test_chain_index_persistence():
    db = tempfile.mktemp(suffix=".db")
    idx = ChainIndex(db_path=db)
    assert idx.count() == len(_HARDCODED_PATTERNS)

    # Add a new pattern (unique pair not in seeds)
    p = ChainPattern(
        "nosqli", "debug_endpoints",
        "NoSQLi error messages reveal debug endpoints",
        source_platform="test",
    )
    idx.add(p)
    assert idx.count() == len(_HARDCODED_PATTERNS) + 1

    # Open new instance on same DB
    idx2 = ChainIndex(db_path=db)
    assert idx2.count() == len(_HARDCODED_PATTERNS) + 1
    assert idx2.lookup("nosqli", "debug_endpoints") is not None
