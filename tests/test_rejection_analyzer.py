"""Tests for rejection_analyzer.py — RejectionRecord, RejectionDB, evidence summaries."""

import tempfile

from engine.rejection_analyzer import (
    RejectionRecord,
    RejectionDB,
    EvidenceSummary,
    categorize_reason,
    _SEED_RECORDS,
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


# ── EvidenceSummary Tests ──────────────────────────────────────────────


def test_evidence_summary_empty():
    ev = EvidenceSummary(finding_class="nonexistent", program="test")
    assert ev.total == 0
    assert ev.accepted == 0
    assert ev.rejected == 0
    assert ev.rejection_rate is None


def test_evidence_summary_rate():
    ev = EvidenceSummary(
        finding_class="sqli", program="general",
        total=10, accepted=2, rejected=8,
    )
    assert ev.rejection_rate == 0.8


def test_evidence_summary_display():
    ev = EvidenceSummary(
        finding_class="open_redirect", program="shopify",
        total=5, accepted=1, rejected=4,
    )
    display = ev.to_display()
    assert "Evidence" in display
    assert "open_redirect" in display
    assert "shopify" in display
    assert "5" in display


def test_evidence_summary_dict():
    ev = EvidenceSummary(
        finding_class="sqli", program="general",
        total=10, accepted=2, rejected=8,
    )
    d = ev.to_dict()
    assert d["finding_class"] == "sqli"
    assert d["total"] == 10
    assert d["rejection_rate"] == 0.8


# ── RejectionDB Tests ──────────────────────────────────────────────────


def test_db_seeds_loaded():
    db = RejectionDB(db_path=":memory:")
    assert db.count() == len(_SEED_RECORDS)
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


def test_db_add_record():
    db = RejectionDB(db_path=":memory:")
    initial = db.count()
    db.add_record("cmd_injection", "new-program", accepted=True, source="manual")
    assert db.count() == initial + 1


def test_db_get_evidence_by_class():
    db = RejectionDB(db_path=":memory:")
    ev_list = db.get_evidence(finding_class="open_redirect")
    assert len(ev_list) >= 1
    for ev in ev_list:
        assert ev.finding_class == "open_redirect"


def test_db_get_evidence_by_program():
    db = RejectionDB(db_path=":memory:")
    ev_list = db.get_evidence(program="general")
    assert len(ev_list) >= 1
    for ev in ev_list:
        assert ev.program == "general"


def test_db_get_evidence_by_both():
    db = RejectionDB(db_path=":memory:")
    ev_list = db.get_evidence(finding_class="open_redirect", program="general")
    assert len(ev_list) >= 1
    ev = ev_list[0]
    assert ev.finding_class == "open_redirect"
    assert ev.program == "general"
    assert ev.rejected >= 1
    assert ev.total >= 1


def test_db_get_evidence_empty():
    db = RejectionDB(db_path=":memory:")
    ev_list = db.get_evidence(finding_class="nonexistent")
    assert len(ev_list) == 0


def test_db_programs_where_accepted():
    db = RejectionDB(db_path=":memory:")
    programs = db.programs_where_accepted("ssrf_reflected")
    assert len(programs) >= 1
    assert "general" in programs


def test_db_programs_where_rejected():
    db = RejectionDB(db_path=":memory:")
    programs = db.programs_where_rejected("open_redirect")
    assert len(programs) >= 3


def test_db_evidence_for():
    db = RejectionDB(db_path=":memory:")
    ev = db.evidence_for("open_redirect", "general")
    assert ev.total > 0
    assert ev.rejected >= 1


def test_db_evidence_for_fallsback_to_global():
    db = RejectionDB(db_path=":memory:")
    ev = db.evidence_for("open_redirect", "nonexistent_program")
    assert ev.total > 0  # falls back to global


def test_db_evidence_for_no_data():
    db = RejectionDB(db_path=":memory:")
    ev = db.evidence_for("nonexistent")
    assert ev.total == 0
    assert ev.confidence == "none"


def test_db_all_finding_classes():
    db = RejectionDB(db_path=":memory:")
    classes = db.all_finding_classes()
    assert "open_redirect" in classes
    assert len(classes) >= 5


def test_db_stats():
    db = RejectionDB(db_path=":memory:")
    s = db.stats()
    assert s["total"] == len(_SEED_RECORDS)
    assert "open_redirect" in s["by_finding_class"]


# ── Categorizer Tests ──────────────────────────────────────────────────


def test_categorize_reason():
    assert categorize_reason("no_security_impact") == "informative"
    assert categorize_reason("intended_behavior") == "informative"
    assert categorize_reason("requires_browser_poc") == "evidence"
    assert categorize_reason("requires_chain") == "evidence"
    assert categorize_reason("next_data_public_by_design") == "wont_fix"
    assert categorize_reason("accepted") == "accepted"
    assert categorize_reason("unknown_reason_xyz") == "other"


def test_categorize_reason_handles_variants():
    assert categorize_reason("no-security-impact") == "informative"
    assert categorize_reason("No Security Impact") == "informative"


# ── Evidence confidence ────────────────────────────────────────────────


def test_evidence_confidence_high():
    ev = EvidenceSummary(finding_class="xss", program="g", total=30)
    assert ev.confidence == "high"


def test_evidence_confidence_medium():
    ev = EvidenceSummary(finding_class="xss", program="g", total=12)
    assert ev.confidence == "medium"


def test_evidence_confidence_low():
    ev = EvidenceSummary(finding_class="xss", program="g", total=5)
    assert ev.confidence == "low"


def test_evidence_confidence_none():
    ev = EvidenceSummary(finding_class="xss", program="g", total=1)
    assert ev.confidence == "none"


# ── Integration: Full Persistence ──────────────────────────────────────


def test_rejection_db_persistence():
    db = tempfile.mktemp(suffix=".db")
    store = RejectionDB(db_path=db)
    assert store.count() == len(_SEED_RECORDS)

    store.add_rejection("test_class", "test_prog", "some_reason")
    assert store.count() == len(_SEED_RECORDS) + 1

    store2 = RejectionDB(db_path=db)
    assert store2.count() == len(_SEED_RECORDS) + 1
    ev_list = store2.get_evidence(finding_class="test_class")
    assert len(ev_list) == 1
    assert ev_list[0].program == "test_prog"
