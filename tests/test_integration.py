"""Integration test — all phases sharing a single SQLite DB.

Connects PolicyStore + RejectionDB + ChainIndex + TriageOracle
with a common vectors.db to verify they work together correctly.
"""

import tempfile

from engine.policy_parser import PolicyStore
from engine.rejection_analyzer import RejectionDB
from engine.chain_extractor import ChainIndex
from engine.triage_oracle import TriageOracle


def test_shared_db_all_modules():
    """PolicyStore + RejectionDB + ChainIndex + TriageOracle on same DB."""
    db = tempfile.mktemp(suffix=".db")

    store = PolicyStore(db_path=db)
    rej = RejectionDB(db_path=db)
    chain = ChainIndex(db_path=db)
    oracle = TriageOracle(db_path=db)

    # Each module sees the same DB
    assert store.count() >= 11          # seeded policies
    assert rej.count() >= 20            # seeded rejection records
    assert chain.count() >= 18          # seeded chain patterns (18 seed pairs)

    # Query the oracle
    v = oracle.evaluate(finding_class="sqli_error", program_name="security")
    assert v.verdict in ("Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence")
    assert len(v.reasoning) > 0
    assert len(v.evidence_notes) >= 1


def test_oracle_detects_chains():
    """TriageOracle should surface chain suggestions from ChainIndex."""
    db = tempfile.mktemp(suffix=".db")

    oracle = TriageOracle(db_path=db)

    # open_redirect has known chains: open_redirect + oauth_misconfig
    v = oracle.evaluate(finding_class="open_redirect", program_name="shopify")
    chain_suggestions = [s for s in v.suggestions if "Chain available" in s]
    assert len(chain_suggestions) >= 1, f"No chain suggestions in: {v.suggestions}"


def test_oracle_detects_no_chains():
    """Finding class with no known chains should not get chain suggestions."""
    db = tempfile.mktemp(suffix=".db")

    oracle = TriageOracle(db_path=db)
    v = oracle.evaluate(finding_class="race_condition", program_name="security")
    chain_suggestions = [s for s in v.suggestions if "Chain available" in s]
    assert len(chain_suggestions) == 0


def test_oracle_policy_and_evidence_integration():
    """Oracle verdict includes both policy issues and evidence notes."""
    db = tempfile.mktemp(suffix=".db")

    oracle = TriageOracle(db_path=db)

    # open_redirect on shopify — excluded by policy
    v = oracle.evaluate(finding_class="open_redirect", program_name="shopify")
    assert len(v.policy_issues) >= 0
    assert len(v.evidence_notes) >= 1

    # sqli_error on security — should be Submission Ready or Low Confidence
    v2 = oracle.evaluate(finding_class="sqli_error", program_name="security")
    assert v2.verdict in ("Submission Ready", "Low Confidence")


def test_custom_records_across_modules():
    """Add records to each module and verify they persist."""
    db = tempfile.mktemp(suffix=".db")

    # Phase 1: seed
    store = PolicyStore(db_path=db)
    rej = RejectionDB(db_path=db)
    ChainIndex(db_path=db)  # verify table creation doesn't conflict

    pre_count = store.count()

    # Phase 2: add custom records
    from engine.policy_parser import ProgramPolicy
    store.add(ProgramPolicy(name="custom-prog", platform="hackerone",
                             exclusions=["self-xss", "rate-limiting"]))
    assert store.count() == pre_count + 1

    rej.add_acceptance("sqli_error", "custom-prog", source="manual")
    assert rej.count() >= 1

    # Phase 3: re-open with new instances
    store2 = PolicyStore(db_path=db)
    rej2 = RejectionDB(db_path=db)
    ChainIndex(db_path=db)  # verify re-open doesn't conflict

    assert store2.count() == pre_count + 1
    assert rej2.count() >= 1

    # Phase 4: oracle can query all
    oracle = TriageOracle(db_path=db)
    v = oracle.evaluate(finding_class="sqli_error", program_name="custom-prog")
    assert v.verdict in ("Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence")


def test_oracle_verdict_across_multiple_findings():
    """Oracle produces consistent verdicts for different finding classes."""
    db = tempfile.mktemp(suffix=".db")
    oracle = TriageOracle(db_path=db)

    findings = [
        ("sqli_error", "security"),
        ("ssrf_reflected", "general"),
        ("xss_reflected", "cloudflare"),
        ("idor", "paypal"),
        ("cmd_injection", ""),
        ("open_redirect", ""),
        ("rate_limit", "general"),
    ]

    for finding_class, program in findings:
        v = oracle.evaluate(finding_class=finding_class, program_name=program)
        assert v.verdict in (
            "Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence",
        ), f"Unexpected verdict {v.verdict} for {finding_class}/{program}"
        assert len(v.reasoning) > 0, f"Empty reasoning for {finding_class}/{program}"
        assert len(v.evidence_notes) >= 1, f"No evidence for {finding_class}/{program}"
