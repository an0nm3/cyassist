"""Phase D3: Triage Oracle — probabilistic submission advisory.

Combines ProgramPolicy and RejectionDB to produce probabilistic scores:
  expected_validity     — 0-1, how likely the finding is to be accepted
  expected_bounty       — estimated bounty tier
  duplicate_probability — 0-1
  expected_triage_time  — "Fast", "Moderate", "Slow"
  recommendation        — actionable next step

The oracle NEVER suppresses a finding. All scores are advisory.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from engine.policy_parser import PolicyStore, ProgramPolicy
from engine.rejection_analyzer import RejectionDB, EvidenceSummary
from engine.chain_extractor import ChainIndex

logger = logging.getLogger("triage_oracle")

_SEVERITY_ORDER = ["none", "low", "medium", "high", "critical"]

_REPORTABLE_SINKS = frozenset({
    "sqli_error", "sqli_time", "sqli_blind",
    "cmd_injection", "cmd_injection_time",
    "ssrf_reflected", "ssrf_blind", "ssrf_oob",
    "ssti", "ssti_blind",
    "xss_reflected", "xss_stored", "xss_dom",
    "idor",
    "auth_bypass",
    "rce",
    "file_read", "file_write",
    "xxe",
    "insecure_deserialization",
    "race_condition",
    "account_takeover",
    "no_sqli",
    "sql_injection",
})

# Base validity by sink class (starting prior before any evidence)
_BASE_VALIDITY: dict[str, float] = {
    "sqli_error": 0.85, "sqli_time": 0.80, "sqli_blind": 0.75,
    "cmd_injection": 0.80, "cmd_injection_time": 0.75,
    "ssrf_reflected": 0.85, "ssrf_blind": 0.70, "ssrf_oob": 0.75,
    "ssti": 0.80, "ssti_blind": 0.70,
    "xss_reflected": 0.65, "xss_stored": 0.80, "xss_dom": 0.55,
    "idor": 0.60, "auth_bypass": 0.75, "rce": 0.90,
    "file_read": 0.70, "file_write": 0.70,
    "xxe": 0.75, "insecure_deserialization": 0.80,
    "race_condition": 0.60, "account_takeover": 0.85,
    "no_sqli": 0.70, "sql_injection": 0.85,
}


@dataclass
class OracleVerdict:
    """Probabilistic advisory for a finding.

    All fields are advisory. The oracle never suppresses findings.
    """

    verdict: str = "Low Confidence"  # kept for backward compat; derived from scores
    expected_validity: float = 0.5
    expected_bounty: str = ""
    duplicate_probability: float = 0.0
    expected_triage_time: str = "Moderate"
    recommendation: str = "Verify Further"
    reasoning: str = ""
    policy_issues: list[str] = field(default_factory=list)
    evidence_notes: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    evidence: Optional[EvidenceSummary] = None

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "expected_validity": round(self.expected_validity, 2),
            "expected_bounty": self.expected_bounty,
            "duplicate_probability": round(self.duplicate_probability, 2),
            "expected_triage_time": self.expected_triage_time,
            "recommendation": self.recommendation,
            "reasoning": self.reasoning,
            "policy_issues": self.policy_issues,
            "evidence_notes": self.evidence_notes,
            "suggestions": self.suggestions,
        }

    def to_display(self) -> str:
        parts = [
            f"Expected validity: {self.expected_validity:.0%}",
            f"Duplicate prob: {self.duplicate_probability:.0%}",
        ]
        if self.expected_bounty:
            parts.append(f"Expected bounty: {self.expected_bounty}")
        parts.append(f"Triage time: {self.expected_triage_time}")
        parts.append(f"Recommendation: {self.recommendation}")
        if self.reasoning:
            parts.append(f"Reasoning: {self.reasoning}")
        if self.suggestions:
            parts.append(f"Suggestions: {'; '.join(self.suggestions)}")
        return " | ".join(parts)


class TriageOracle:
    """Combines policy + evidence to produce probabilistic submission scores."""

    def __init__(self, policy_store: Optional[PolicyStore] = None,
                 rejection_db: Optional[RejectionDB] = None,
                 chain_index: Optional[ChainIndex] = None,
                 db_path: str = "",
                 calibrated: bool = False):
        if db_path:
            self.policy_store = policy_store or PolicyStore(db_path=db_path)
            self.rejection_db = rejection_db or RejectionDB(db_path=db_path)
            self.chain_index = chain_index or ChainIndex(db_path=db_path)
        else:
            self.policy_store = policy_store or PolicyStore()
            self.rejection_db = rejection_db or RejectionDB()
            self.chain_index = chain_index or ChainIndex()
        self.calibrated = calibrated

    def evaluate(self, finding_class: str, program_name: str = "",
                 severity: str = "", tech: str = "",
                 description: str = "") -> OracleVerdict:
        """Evaluate a finding and return probabilistic advisory scores."""
        policy_issues: list[str] = []
        evidence_notes: list[str] = []
        suggestions: list[str] = []

        # ── 1. Check program policy ────────────────────────────────
        policy: Optional[ProgramPolicy] = None
        if program_name:
            policy = self.policy_store.lookup(program_name)

        policy_excluded = False
        policy_severity_penalty = 0.0
        if policy:
            excluded, reason = policy.matches_finding(finding_class, severity)
            if excluded:
                policy_issues.append(f"Policy may exclude: {reason}")
                policy_excluded = True

            if policy.requires_browser_poc and finding_class in (
                "cors_misconfig", "ssti", "xss_reflected", "xss_stored",
            ):
                evidence_notes.append(
                    f"Policy requires browser-based PoC for {finding_class}"
                )
                suggestions.append(
                    "Provide a browser-based PoC (DevTools console or Playwright)"
                )

            if policy.requires_account:
                suggestions.append(
                    "This program requires a test account — ensure you have "
                    "one before submitting"
                )

            if policy.minimum_severity != "none":
                sev_idx = _SEVERITY_ORDER.index(severity) if severity in _SEVERITY_ORDER else -1
                min_idx = _SEVERITY_ORDER.index(policy.minimum_severity)
                if 0 <= sev_idx < min_idx:
                    policy_severity_penalty = 0.15 * (min_idx - sev_idx)
                    evidence_notes.append(
                        f"Policy minimum severity is {policy.minimum_severity}, "
                        f"finding is {severity or 'unspecified'}"
                    )

        # ── 2. Check rejection evidence ────────────────────────────
        ev: Optional[EvidenceSummary] = None
        if policy:
            ev = self.rejection_db.evidence_for(finding_class, policy.name)
        else:
            ev = self.rejection_db.evidence_for(finding_class)

        is_high_value = finding_class in _REPORTABLE_SINKS

        if ev and ev.total > 0:
            evidence_notes.append(ev.to_display())
            if ev.rejected > 0:
                reasons_for_display = ev.common_reasons[:3]
                if reasons_for_display:
                    evidence_notes.append(
                        f"Common rejection reasons: {', '.join(reasons_for_display)}"
                    )
                suggestions.append(
                    "Review rejected patterns — ensure your finding differs "
                    "from previous submissions"
                )
        else:
            evidence_notes.append(
                f"Limited evidence for '{finding_class}' submissions on "
                f"{program_name or 'unknown program'}"
            )

        # ── 3. Check chain patterns ────────────────────────────────
        chains = self.chain_index.lookup_by_sink(finding_class) if self.chain_index else []
        chain_suggestions: list[str] = []
        for c in chains:
            label = f"{c.primitive_a} + {c.primitive_b}"
            if label not in chain_suggestions:
                chain_suggestions.append(label)
                suggestions.append(
                    f"Chain available: {c.primitive_a} + {c.primitive_b} → {c.impact}"
                )

        # ── 4. Compute probabilistic scores ────────────────────────
        return self._compute_probabilistic(
            finding_class, policy_excluded, policy_severity_penalty,
            ev, is_high_value, severity, policy_issues, evidence_notes,
            suggestions, chain_suggestions,
        )

    def _compute_probabilistic(
        self,
        finding_class: str,
        policy_excluded: bool,
        policy_severity_penalty: float,
        ev: Optional[EvidenceSummary],
        is_high_value: bool,
        severity: str,
        policy_issues: list[str],
        evidence_notes: list[str],
        suggestions: list[str],
        chain_suggestions: list[str],
    ) -> OracleVerdict:
        """Compute probabilistic scores from all available signals."""

        # ── Expected validity ──────────────────────────────────────
        base = _BASE_VALIDITY.get(finding_class, 0.5)

        # Adjust for evidence
        validity = base
        if ev and ev.total > 0:
            ratio = ev.accepted / max(ev.total, 1)
            validity = base * 0.4 + ratio * 0.6
        elif is_high_value:
            validity = max(validity, 0.65)

        # Policy penalties
        if policy_excluded:
            validity *= 0.6
        validity -= policy_severity_penalty

        # Severity boost
        if severity in ("critical", "high"):
            validity = min(1.0, validity + 0.1)

        validity = max(0.05, min(0.99, validity))

        # ── Duplicate probability ──────────────────────────────────
        dup_prob = 0.0
        if ev and ev.total > 5:
            dup_prob = ev.rejected / max(ev.total, 1) * 0.5
        if finding_class in ("xss_reflected", "open_redirect", "cors_misconfig"):
            dup_prob = max(dup_prob, 0.3)
        dup_prob = max(0.0, min(0.95, dup_prob))

        # ── Expected bounty ────────────────────────────────────────
        bounty_boost = 0
        if chain_suggestions:
            bounty_boost = 1
        bounty_map = {
            "critical": ("Critical", 2 + bounty_boost),
            "high": ("High", 1 + bounty_boost),
            "medium": ("Medium", 0 + bounty_boost),
            "low": ("Low", -1 + bounty_boost),
        }
        best = severity.lower() if severity in bounty_map else ""
        if best:
            label, _ = bounty_map[best]
        else:
            label = ""

        # ── Triage time ────────────────────────────────────────────
        if ev and ev.total >= 10:
            triage_time = "Fast"
        elif ev and ev.total >= 3:
            triage_time = "Moderate"
        else:
            triage_time = "Slow"

        # ── Recommendation ─────────────────────────────────────────
        if validity >= 0.80 and dup_prob < 0.3:
            recommendation = "Submit Immediately"
            verdict = "Submission Ready"
        elif validity >= 0.65 and dup_prob < 0.5:
            if chain_suggestions:
                recommendation = "Submit with Chain"
                verdict = "Submission Ready"
            else:
                recommendation = "Submit with Caution"
                verdict = "Submission Ready"
        elif policy_excluded:
            recommendation = "Build a Chain"
            verdict = "Policy Conflict"
        elif validity >= 0.40 or is_high_value:
            recommendation = "Verify Further"
            verdict = "Needs Manual Review"
        else:
            recommendation = "Low Confidence — Seek More Evidence"
            verdict = "Low Confidence"

        return OracleVerdict(
            verdict=verdict,
            expected_validity=validity,
            expected_bounty=label,
            duplicate_probability=dup_prob,
            expected_triage_time=triage_time,
            recommendation=recommendation,
            reasoning=f"Base validity {_BASE_VALIDITY.get(finding_class, 0.5):.0%} adjusted "
                      f"by evidence and policy constraints",
            policy_issues=policy_issues,
            evidence_notes=evidence_notes,
            suggestions=list(dict.fromkeys(suggestions)),
            evidence=ev,
        )
