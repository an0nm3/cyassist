"""Tests for cyassist/engine/policy_parser.py — ProgramPolicy, PolicyStore, exclusion detection."""

import tempfile

from engine.policy_parser import (
    ProgramPolicy,
    PolicyStore,
    _SEEDED_POLICIES,
    exclusion_to_sink,
    _EXCLUSION_CATEGORIES,
    _EXCLUSION_TO_SINK,
)


# ── ProgramPolicy Tests ────────────────────────────────────────────────


def test_policy_defaults():
    p = ProgramPolicy(name="test", platform="hackerone")
    assert p.name == "test"
    assert p.requires_poc is True
    assert p.requires_browser_poc is False
    assert p.created_at != ""
    assert p.updated_at != ""


def test_policy_to_row_roundtrip():
    p = ProgramPolicy(
        name="test-program",
        url="https://hackerone.com/test-program",
        exclusions=["self-xss", "rate-limiting", "open-redirect-without-chain"],
        score_range="$500-$5000",
        requires_browser_poc=True,
        out_of_scope=["Automated scanning without prior approval"],
        notes="Test policy",
    )
    row = p.to_row()
    assert row["name"] == "test-program"
    assert "self-xss" in row["exclusions"]
    assert row["score_range"] == "$500-$5000"
    assert row["requires_browser_poc"] == 1

    restored = ProgramPolicy.from_row(row)
    assert restored.name == p.name
    assert restored.exclusions == p.exclusions
    assert restored.score_range == p.score_range
    assert restored.requires_browser_poc is True


def test_policy_matches_finding_excluded():
    p = ProgramPolicy(
        name="test",
        exclusions=["open-redirect-without-chain"],
    )
    excluded, reason = p.matches_finding("open_redirect")
    assert excluded is True
    assert "Excluded" in reason


def test_policy_matches_finding_not_excluded():
    p = ProgramPolicy(
        name="test",
        exclusions=["self-xss", "rate-limiting"],
    )
    excluded, reason = p.matches_finding("sqli_error")
    assert excluded is False
    assert reason == ""


def test_policy_matches_finding_oos():
    p = ProgramPolicy(
        name="test",
        out_of_scope=["Automated scanning without prior approval"],
    )
    excluded, reason = p.matches_finding("automated_scanning")
    assert excluded is True
    assert "Out of scope" in reason


# ── Exclusion Mapping Tests ────────────────────────────────────────────


def test_exclusion_to_sink():
    assert exclusion_to_sink("self-xss") == "xss_reflected"
    assert exclusion_to_sink("rate_limiting") == "rate_limit"
    assert exclusion_to_sink("open-redirect-without-chain") == "open_redirect"
    assert exclusion_to_sink("next_data_leak") == "path_discovery"
    assert exclusion_to_sink("unknown_category") == "unknown_category"


def test_exclusion_categories_loaded():
    assert "self-xss" in _EXCLUSION_CATEGORIES
    assert "rate-limiting" in _EXCLUSION_CATEGORIES
    assert "open-redirect-without-chain" in _EXCLUSION_CATEGORIES
    assert len(_EXCLUSION_CATEGORIES) >= 30


def test_exclusion_to_sink_comprehensive():
    """All exclusion-to-sink mappings should have valid keys from the categories."""
    for exc_name in _EXCLUSION_TO_SINK:
        normalized = exc_name.replace("-", "_").replace(" ", "_")
        assert normalized in _EXCLUSION_CATEGORIES or exc_name in _EXCLUSION_CATEGORIES


# ── PolicyStore Tests ──────────────────────────────────────────────────


def test_store_seeds_loaded():
    store = PolicyStore(db_path=":memory:")
    assert store.count() == len(_SEEDED_POLICIES)
    assert store.count() >= 10


def test_store_lookup():
    store = PolicyStore(db_path=":memory:")
    p = store.lookup("shopify")
    assert p is not None
    assert "open-redirect-without-chain" in p.exclusions
    assert p.score_range == "$500-$10000"


def test_store_lookup_case_insensitive():
    store = PolicyStore(db_path=":memory:")
    p = store.lookup("SHOPIFY")
    assert p is not None


def test_store_lookup_partial():
    store = PolicyStore(db_path=":memory:")
    p = store.lookup("shop")  # partial match
    assert p is not None
    assert p.name == "shopify"


def test_store_lookup_missing():
    store = PolicyStore(db_path=":memory:")
    p = store.lookup("nonexistent-program-that-does-not-exist-at-all")
    assert p is None


def test_store_lookup_by_sink():
    store = PolicyStore(db_path=":memory:")
    results = store.lookup_by_sink("open_redirect")
    assert len(results) >= 5
    names = {r[0] for r in results}
    assert "shopify" in names
    assert "paypal" in names


def test_store_add_new():
    store = PolicyStore(db_path=":memory:")
    initial = store.count()
    p = ProgramPolicy(
        name="new-program",
        platform="hackerone",
        exclusions=["self-xss"],
        score_range="$1000-$5000",
    )
    added = store.add(p)
    assert added is True
    assert store.count() == initial + 1


def test_store_add_duplicate():
    store = PolicyStore(db_path=":memory:")
    p = ProgramPolicy(name="custom-prog", exclusions=["self-xss"])
    store.add(p)
    added = store.add(p)
    assert added is False


def test_store_remove():
    store = PolicyStore(db_path=":memory:")
    assert store.remove("nonexistent") is False
    p = ProgramPolicy(name="temp-prog", exclusions=[])
    store.add(p)
    assert store.remove("temp-prog") is True


def test_store_stats():
    store = PolicyStore(db_path=":memory:")
    s = store.stats()
    assert s["total"] == len(_SEEDED_POLICIES)
    assert "hackerone" in s["by_platform"]
    assert "bugcrowd" in s["by_platform"]


# ── Policy Text Parser Tests ───────────────────────────────────────────


def test_parse_policy_text_with_exclusions():
    store = PolicyStore(db_path=":memory:")
    text = """
    Out of scope: self-XSS, rate limiting, missing CSP headers.
    Bounty range: $500-$5000.
    We do not accept clickjacking or CSRF logout findings.
    """
    p = store.parse_policy_text(text, name="test-prog")
    assert p is not None
    assert p.name == "test-prog"
    exclusions_lower = [e.lower() for e in p.exclusions]
    assert any("self" in e and "xss" in e for e in exclusions_lower)
    assert p.score_range == "$500-$5000"


def test_parse_policy_text_browser_poc():
    store = PolicyStore(db_path=":memory:")
    text = """
    Browser-based proof of concept required. curl is not sufficient.
    """
    p = store.parse_policy_text(text, name="strict-prog")
    assert p is not None
    assert p.requires_browser_poc is True


def test_parse_policy_text_empty():
    store = PolicyStore(db_path=":memory:")
    p = store.parse_policy_text("", name="empty")
    assert p is None


def test_parse_policy_text_no_match():
    store = PolicyStore(db_path=":memory:")
    p = store.parse_policy_text("Just some random text about nothing relevant.")
    assert p is not None
    assert len(p.exclusions) == 0
    assert len(p.out_of_scope) == 0


# ── Integration: Full Persistence ──────────────────────────────────────


def test_policy_persistence():
    db = tempfile.mktemp(suffix=".db")
    store = PolicyStore(db_path=db)
    assert store.count() == len(_SEEDED_POLICIES)

    p = ProgramPolicy(
        name="persistent-prog",
        exclusions=["self-xss", "rate-limiting"],
        score_range="$100-$1000",
    )
    store.add(p)
    assert store.count() == len(_SEEDED_POLICIES) + 1

    store2 = PolicyStore(db_path=db)
    assert store2.count() == len(_SEEDED_POLICIES) + 1
    assert store2.lookup("persistent-prog") is not None
