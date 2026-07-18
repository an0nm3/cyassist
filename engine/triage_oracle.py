"""Phase D3: Triage Oracle — evidence-based submission advisory.

Combines ProgramPolicy and RejectionDB to produce one of four verdicts:
  Submission Ready   — no policy conflict, evidence is clear or neutral
  Needs Manual Review — no clear policy barrier, but evidence is mixed/limited
  Policy Conflict    — program policy likely excludes this finding
  Low Confidence     — insufficient evidence to assess

The oracle NEVER suppresses a finding. All verdicts are advisory.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from engine.policy_parser import PolicyStore, ProgramPolicy
from engine.rejection_analyzer import RejectionDB, EvidenceSummary
from engine.chain_extractor import ChainIndex

logger = logging.getLogger("triage_oracle")

# Severity ordering for comparison
_SEVERITY_ORDER = ["none", "low", "medium", "high", "critical"]

# Reportable sink IDs that generally pay
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


@dataclass
class OracleVerdict:
    """Advisory verdict for a finding.

    verdict: one of Submission Ready / Needs Manual Review / Policy Conflict / Low Confidence
    reasoning: full advisory explanation
    suggestions: actionable next steps
    """

    verdict: str  # "Submission Ready", "Needs Manual Review", "Policy Conflict", "Low Confidence"
    reasoning: str = ""
    policy_issues: list[str] = field(default_factory=list)
    evidence_notes: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    evidence: Optional[EvidenceSummary] = None

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "reasoning": self.reasoning,
            "policy_issues": self.policy_issues,
            "evidence_notes": self.evidence_notes,
            "suggestions": self.suggestions,
        }

    def to_display(self) -> str:
        parts = [f"Verdict: {self.verdict}"]
        if self.reasoning:
            parts.append(f"Reasoning: {self.reasoning}")
        if self.suggestions:
            parts.append(f"Suggestions: {'; '.join(self.suggestions)}")
        return " | ".join(parts)


# ── TriageOracle ─────────────────────────────────────────────────────────


class TriageOracle:
    """Combines policy + evidence to advise on submission readiness.

    This is a non-blocking advisor. It never tells you not to submit.
    """

    def __init__(self, policy_store: Optional[PolicyStore] = None,
                 rejection_db: Optional[RejectionDB] = None,
                 chain_index: Optional[ChainIndex] = None,
                 db_path: str = ""):
        if db_path:
            self.policy_store = policy_store or PolicyStore(db_path=db_path)
            self.rejection_db = rejection_db or RejectionDB(db_path=db_path)
            self.chain_index = chain_index or ChainIndex(db_path=db_path)
        else:
            self.policy_store = policy_store or PolicyStore()
            self.rejection_db = rejection_db or RejectionDB()
            self.chain_index = chain_index or ChainIndex()

    def evaluate(self, finding_class: str, program_name: str = "",
                 severity: str = "", tech: str = "",
                 description: str = "") -> OracleVerdict:
        """Evaluate a finding and return an advisory verdict.

        Args:
            finding_class: e.g. "sqli_error", "open_redirect", "xss_reflected"
            program_name: target program name (for policy lookup)
            severity: "low", "medium", "high", "critical", or ""
            tech: technology stack hint (e.g. "python", "php")
            description: optional human-readable description

        Returns:
            OracleVerdict — always advisory, never blocking.
        """
        policy_issues: list[str] = []
        evidence_notes: list[str] = []
        suggestions: list[str] = []

        # ── 1. Check program policy ────────────────────────────────
        policy: Optional[ProgramPolicy] = None
        if program_name:
            policy = self.policy_store.lookup(program_name)

        policy_excluded = False
        if policy:
            excluded, reason = policy.matches_finding(finding_class, severity)
            if excluded:
                policy_issues.append(f"Policy may exclude: {reason}")
                policy_excluded = True

            # Additional policy flags
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
                if sev_idx < min_idx:
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

        is_high_value_finding = finding_class in _REPORTABLE_SINKS

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

        # ── 4. Determine verdict ───────────────────────────────────
        verdict, reasoning = self._compute_verdict(
            finding_class, policy_excluded, ev, is_high_value_finding,
        )

        return OracleVerdict(
            verdict=verdict,
            reasoning=reasoning,
            policy_issues=policy_issues,
            evidence_notes=evidence_notes,
            suggestions=list(dict.fromkeys(suggestions)),  # dedup preserving order
            evidence=ev,
        )

    def _compute_verdict(
        self,
        finding_class: str,
        policy_excluded: bool,
        ev: Optional[EvidenceSummary],
        is_high_value: bool,
    ) -> tuple[str, str]:
        """Determine verdict and reasoning based on all inputs."""

        # ── Policy Conflict ────────────────────────────────────────
        if policy_excluded:
            return (
                "Policy Conflict",
                "The program policy appears to exclude this finding class. "
                "You may still submit, but be aware the program has a stated "
                "exclusion. Consider whether you can demonstrate a chained "
                "exploit that avoids the exclusion clause."
            )

        # ── Check confidence from evidence ─────────────────────────
        has_clear_evidence = ev and ev.total >= 3
        has_positive_evidence = ev and ev.accepted >= ev.rejected
        has_negative_evidence = ev and ev.rejected > ev.accepted and ev.rejected >= 3

        # ── Submission Ready ────────────────────────────────────────
        if has_clear_evidence and has_positive_evidence:
            return (
                "Submission Ready",
                f"Evidence shows {ev.accepted} accepted vs {ev.rejected} rejected "
                f"similar findings (confidence: {ev.confidence}). "
                "Historical pattern favors acceptance. Prepare a high-quality "
                "report with clear impact demonstration."
            )

        if is_high_value and not has_negative_evidence:
            return (
                "Submission Ready",
                f"'{finding_class}' is a well-known vulnerability class that "
                "commonly pays bounties. No strong rejection signal from evidence. "
                "Ensure your finding demonstrates clear security impact."
            )

        # ── Needs Manual Review ────────────────────────────────────
        if has_negative_evidence:
            return (
                "Needs Manual Review",
                f"Evidence shows {ev.rejected} rejected vs {ev.accepted} accepted "
                f"similar findings (confidence: {ev.confidence}). "
                "Review the common rejection patterns and ensure your finding "
                "avoids those pitfalls. Consider building a chain to increase impact."
            )

        if has_clear_evidence and ev.rejected > ev.accepted:
            return (
                "Needs Manual Review",
                "Historical evidence for this finding class is mixed. "
                "Review why similar submissions were rejected and ensure yours "
                "demonstrates clearer impact."
            )

        # ── Low Confidence ─────────────────────────────────────────
        return (
            "Low Confidence",
            f"Not enough historical evidence for '{finding_class}' "
            f"on this program. Consider: (1) verifying the finding against "
            f"multiple targets, (2) checking program policy for exclusions, "
            f"(3) building a chain for greater impact."
        )
