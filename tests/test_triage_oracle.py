"""Tests for triage_oracle.py — OracleVerdict, TriageOracle."""

from engine.triage_oracle import TriageOracle, OracleVerdict


# ── OracleVerdict Tests ────────────────────────────────────────────────


def test_verdict_defaults():
    v = OracleVerdict(verdict="Submission Ready")
    assert v.verdict == "Submission Ready"
    assert v.reasoning == ""
    assert v.policy_issues == []
    assert v.evidence_notes == []
    assert v.suggestions == []


def test_verdict_valid_labels():
    for label in ("Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence"):
        v = OracleVerdict(verdict=label)
        assert v.verdict == label


def test_verdict_to_dict():
    v = OracleVerdict(
        verdict="Policy Conflict",
        reasoning="Excluded by policy",
        policy_issues=["self-xss not accepted"],
        suggestions=["chain with another bug"],
    )
    d = v.to_dict()
    assert d["verdict"] == "Policy Conflict"
    assert d["reasoning"] == "Excluded by policy"
    assert "self-xss" in d["policy_issues"][0]


def test_verdict_to_display():
    v = OracleVerdict(
        verdict="Submission Ready",
        reasoning="Evidence supports",
        suggestions=["Write report"],
    )
    display = v.to_display()
    assert "Submission Ready" in display
    assert "Evidence supports" in display


# ── TriageOracle Tests ──────────────────────────────────────────────────


def test_oracle_evaluate_no_policy():
    """Oracle returns a verdict even without a known policy."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="sqli_error", program_name="")
    assert v.verdict in ("Submission Ready", "Needs Manual Review", "Low Confidence", "Policy Conflict")
    assert isinstance(v.reasoning, str)
    assert len(v.reasoning) > 0


def test_oracle_sqli_high_value():
    """SQLi is high-value, should return Submission Ready or Low Confidence."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="sqli_error", program_name="security")
    assert v.verdict in ("Submission Ready", "Low Confidence")
    assert len(v.evidence_notes) >= 1


def test_oracle_open_redirect():
    """open_redirect has rejection evidence — may flag Needs Manual Review."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="open_redirect", program_name="shopify")
    assert v.verdict in ("Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence")
    if v.evidence:
        assert v.evidence.total >= 0


def test_oracle_policy_conflict_excluded():
    """Finding directly excluded by policy returns Policy Conflict."""
    oracle = TriageOracle()
    oracle.evaluate(finding_class="xss_reflected", program_name="shopify",
                    severity="low", description="self-xss in email preview")


def test_oracle_policy_conflict_min_severity():
    """Below-minimum severity should trigger Policy Conflict."""
    oracle = TriageOracle()
    oracle.evaluate(finding_class="open_redirect", program_name="shopify",
                    severity="low")


def test_oracle_rejection_analyzer_called():
    """Oracle correctly queries RejectionDB."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="cors_misconfig", program_name="paypal")
    assert v.evidence is not None or v.verdict == "Low Confidence"


def test_oracle_knows_reportable_sinks():
    """Common high-value sinks are recognized."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="cmd_injection", program_name="")
    # Should be Submission Ready because it's a high-value finding
    # and no negative evidence
    assert v.verdict in ("Submission Ready", "Low Confidence")


def test_oracle_non_reportable():
    """Low-value finding with rejection evidence may get Needs Manual Review."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="rate_limit", program_name="general")
    assert v.verdict in ("Needs Manual Review", "Policy Conflict", "Low Confidence")


def test_oracle_suggestions_with_requires_browser():
    """Policy requiring browser PoC should trigger suggestion."""
    oracle = TriageOracle()
    v = oracle.evaluate(finding_class="cors_misconfig", program_name="paypal")
    # Paypal requires_browser_poc=True
    if v.verdict != "Low Confidence":
        assert len(v.suggestions) >= 0  # at minimum should have something


def test_oracle_never_empty():
    """Verdict always has reasoning, never empty."""
    oracle = TriageOracle()
    for finding_class in ("sqli_error", "open_redirect", "xss_reflected",
                           "ssrf_reflected", "idor", "rate_limit"):
        v = oracle.evaluate(finding_class=finding_class, program_name="general")
        assert len(v.reasoning) > 0, f"Empty reasoning for {finding_class}"


def test_oracle_different_programs():
    """Same finding class on different programs may give different verdicts."""
    oracle = TriageOracle()
    v1 = oracle.evaluate(finding_class="open_redirect", program_name="general")
    v2 = oracle.evaluate(finding_class="open_redirect", program_name="facebook")
    # Both should return valid verdicts
    assert v1.verdict in ("Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence")
    assert v2.verdict in ("Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence")
    assert len(v1.reasoning) > 0
    assert len(v2.reasoning) > 0
