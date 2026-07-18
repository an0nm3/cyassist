"""Tests for cyassist/engine/rejection_analyzer.py — RejectionRecord, RejectionDB, categorizer."""

import tempfile

from engine.rejection_analyzer import (
    RejectionRecord,
    RejectionDB,
    categorize_reason,
    summarize_rejection_rate,
    _SEED_REJECTIONS,
)


# ── RejectionRecord Tests ──────────────────────────────────────────────


def test_record_defaults():
    r = RejectionRecord(finding_class="open_redirect", program="shopify")
    assert r.reason == ""
    assert r.accepted is False
    assert r.source == "manual"
    assert r.timestamp != ""


def test_record_accepted():
    r = RejectionRecord(
        finding_class="sqli_error", program="general",
        accepted=True, source="seed",
    )
    assert r.accepted is True
    assert r.source == "seed"


# ── RejectionDB Tests ──────────────────────────────────────────────────


def test_db_seeds_loaded():
    db = RejectionDB(db_path=":memory:")
    assert db.count() == len(_SEED_REJECTIONS)
    assert db.count() >= 20


def test_db_add_rejection():
    db = RejectionDB(db_path=":memory:")
    initial = db.count()
    db.add_rejection("open_redirect", "new-program", "no_security_impact")
    assert db.count() == initial + 1


def test_db_add_acceptance():
    db = RejectionDB(db_path=":memory:")
    initial = db.count()
    db.add_acceptance("sqli_error", "new-program")
    assert db.count() == initial + 1


def test_db_get_metrics_by_class():
    db = RejectionDB(db_path=":memory:")
    metrics = db.get_metrics(finding_class="open_redirect")
    assert len(metrics) >= 1
    for m in metrics:
        assert m["finding_class"] == "open_redirect"


def test_db_get_metrics_by_program():
    db = RejectionDB(db_path=":memory:")
    metrics = db.get_metrics(program="general")
    assert len(metrics) >= 1
    for m in metrics:
        assert m["program"] == "general"


def test_db_get_metrics_by_both():
    db = RejectionDB(db_path=":memory:")
    metrics = db.get_metrics(finding_class="open_redirect", program="cloudflare")
    assert len(metrics) == 1
    m = metrics[0]
    assert m["finding_class"] == "open_redirect"
    assert m["program"] == "cloudflare"
    assert m["rejection_rate"] == 1.0  # all rejections in seeds
    assert m["total"] >= 1
    assert len(m["common_reasons"]) >= 0


def test_db_get_metrics_empty():
    db = RejectionDB(db_path=":memory:")
    metrics = db.get_metrics(finding_class="nonexistent")
    assert len(metrics) == 0


def test_db_programs_where_accepted():
    db = RejectionDB(db_path=":memory:")
    programs = db.programs_where_accepted("ssrf_reflected")
    assert len(programs) >= 1
    assert "general" in programs


def test_db_programs_where_rejected():
    db = RejectionDB(db_path=":memory:")
    programs = db.programs_where_rejected("open_redirect")
    assert len(programs) >= 3


def test_db_global_rejection_rate():
    db = RejectionDB(db_path=":memory:")
    rate = db.global_rejection_rate()
    assert 0.0 <= rate <= 1.0


def test_db_global_rejection_rate_by_class():
    db = RejectionDB(db_path=":memory:")
    rate = db.global_rejection_rate(finding_class="open_redirect")
    assert rate >= 0.5  # most open_redirects are rejected in seed data


def test_db_all_finding_classes():
    db = RejectionDB(db_path=":memory:")
    classes = db.all_finding_classes()
    assert "open_redirect" in classes
    assert len(classes) >= 5


def test_db_stats():
    db = RejectionDB(db_path=":memory:")
    s = db.stats()
    assert s["total"] == len(_SEED_REJECTIONS)
    assert "open_redirect" in s["by_finding_class"]
    assert 0.0 <= s["global_rejection_rate"] <= 1.0


# ── Categorizer Tests ──────────────────────────────────────────────────


def test_categorize_reason():
    assert categorize_reason("no_security_impact") == "informative"
    assert categorize_reason("intended_behavior") == "informative"
    assert categorize_reason("requires_browser_poc") == "evidence"
    assert categorize_reason("requires_chain") == "evidence"
    assert categorize_reason("next_data_public_by_design") == "wont_fix"
    assert categorize_reason("accepted") == "accepted"
    assert categorize_reason("unknown_reason_xyz") == "other"


def test_summarize_rate():
    assert summarize_rejection_rate(0.9) == "highly_likely_rejected"
    assert summarize_rejection_rate(0.65) == "likely_rejected"
    assert summarize_rejection_rate(0.35) == "uncertain"
    assert summarize_rejection_rate(0.1) == "likely_accepted"


# ── Integration: Full Persistence ──────────────────────────────────────


def test_rejection_db_persistence():
    db = tempfile.mktemp(suffix=".db")
    store = RejectionDB(db_path=db)
    assert store.count() == len(_SEED_REJECTIONS)

    store.add_rejection("test_class", "test_prog", "some_reason")
    assert store.count() == len(_SEED_REJECTIONS) + 1

    store2 = RejectionDB(db_path=db)
    assert store2.count() == len(_SEED_REJECTIONS) + 1
    metrics = store2.get_metrics(finding_class="test_class")
    assert len(metrics) == 1
    assert metrics[0]["program"] == "test_prog"
