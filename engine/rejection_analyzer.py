"""Phase D2: Rejection Pattern Analyzer — evidence tracking.

Tracks historical outcomes for finding classes across programs.
Outputs evidence summaries with raw counts, not predictions.

Seeded with known patterns from bug bounty experience.
Extendable via add_record() / add_rejection() / add_acceptance().

Storage: SQLite table `rejection_records`, indexed by (finding_class, program).
"""

import logging
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger("rejection_analyzer")


# ── Data Model ──────────────────────────────────────────────────────────


@dataclass
class RejectionRecord:
    """One historical outcome for a finding class on a program."""

    finding_class: str
    program: str
    reason: str = ""
    accepted: bool = False     # True = was accepted (counter-example)
    source: str = "manual"     # "manual", "triage_import", "seed"
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class EvidenceSummary:
    """Evidence-based summary for a (finding_class, program) pair.

    Never outputs probabilities. Always shows raw counts.
    """

    finding_class: str
    program: str
    total: int = 0
    accepted: int = 0
    rejected: int = 0
    common_reasons: list[str] = None
    confidence: str = "none"  # "none", "low", "medium", "high"

    def __post_init__(self):
        if self.common_reasons is None:
            self.common_reasons = []
        if self.total >= 20:
            self.confidence = "high"
        elif self.total >= 10:
            self.confidence = "medium"
        elif self.total >= 3:
            self.confidence = "low"

    @property
    def rejection_rate(self) -> Optional[float]:
        """Raw proportion (for display only). None if no data."""
        if self.total == 0:
            return None
        return round(self.rejected / self.total, 2)

    def to_display(self) -> str:
        """Human-readable summary line."""
        if self.total == 0:
            return f"Evidence: No historical data for {self.finding_class} on {self.program}"
        parts = [
            f"Evidence: {self.finding_class} on {self.program}",
            f"Records: {self.total}",
            f"Accepted: {self.accepted}",
            f"Rejected: {self.rejected}",
        ]
        if self.common_reasons:
            unique = list(dict.fromkeys(self.common_reasons))[:3]
            parts.append(f"Common reasons: {', '.join(unique)}")
        parts.append(f"Confidence: {self.confidence.title()}")
        return " | ".join(parts)

    def to_dict(self) -> dict:
        """Serializable dict with raw counts only."""
        return {
            "finding_class": self.finding_class,
            "program": self.program,
            "total": self.total,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "rejection_rate": self.rejection_rate,
            "common_reasons": self.common_reasons,
            "confidence": self.confidence,
            "display": self.to_display(),
        }


# ── Rejection Database ──────────────────────────────────────────────────


class RejectionDB:
    """SQLite-backed store for historical finding outcomes.

    Answers: "What happened when similar findings were submitted?"
    Never: "What is the probability this will be rejected?"
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS rejection_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        finding_class TEXT NOT NULL,
        program TEXT NOT NULL,
        reason TEXT DEFAULT '',
        accepted INTEGER DEFAULT 0,
        source TEXT DEFAULT 'manual',
        timestamp TEXT DEFAULT '',
        UNIQUE(finding_class, program, reason, accepted)
    );
    CREATE INDEX IF NOT EXISTS idx_rej_class ON rejection_records(finding_class);
    CREATE INDEX IF NOT EXISTS idx_rej_program ON rejection_records(program);
    CREATE INDEX IF NOT EXISTS idx_rej_class_program ON rejection_records(finding_class, program);
    """

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "vectors.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()
        self._load_seeds()

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.executescript(self.SCHEMA)
        return self._conn

    def _init_db(self):
        _ = self.conn

    def _load_seeds(self):
        for r in _SEED_RECORDS:
            self._insert(r)

    def _insert(self, record: RejectionRecord):
        try:
            existing = self.conn.execute(
                "SELECT id FROM rejection_records WHERE finding_class=? AND program=? AND reason=? AND accepted=?",
                (record.finding_class, record.program, record.reason, int(record.accepted)),
            ).fetchone()
            if existing:
                return
            self.conn.execute(
                """INSERT INTO rejection_records
                (finding_class, program, reason, accepted, source, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (record.finding_class, record.program, record.reason,
                 int(record.accepted), record.source, record.timestamp),
            )
            self.conn.commit()
        except Exception as e:
            logger.debug(f"RejectionDB insert failed: {e}")

    # ── Public API ───────────────────────────────────────────────────

    def add_rejection(self, finding_class: str, program: str,
                      reason: str = "", source: str = "manual"):
        self._insert(RejectionRecord(
            finding_class=finding_class, program=program,
            reason=reason, accepted=False, source=source,
        ))

    def add_acceptance(self, finding_class: str, program: str,
                       source: str = "manual"):
        self._insert(RejectionRecord(
            finding_class=finding_class, program=program,
            accepted=True, source=source,
        ))

    def add_record(self, finding_class: str, program: str,
                   accepted: bool, reason: str = "",
                   source: str = "manual"):
        self._insert(RejectionRecord(
            finding_class=finding_class, program=program,
            reason=reason, accepted=accepted, source=source,
        ))

    def get_evidence(self, finding_class: str = "",
                     program: str = "") -> list[EvidenceSummary]:
        """Get evidence summaries, optionally filtered.

        Returns EvidenceSummary objects (raw counts, no predictions).
        """
        where = []
        params = []
        if finding_class:
            where.append("finding_class = ?")
            params.append(finding_class)
        if program:
            where.append("program = ?")
            params.append(program)

        query = "SELECT finding_class, program FROM rejection_records"
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " GROUP BY finding_class, program"

        rows = self.conn.execute(query, params).fetchall()
        return [self._compute_evidence(r["finding_class"], r["program"]) for r in rows]

    def _compute_evidence(self, finding_class: str, program: str) -> EvidenceSummary:
        total = self.conn.execute(
            "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=? AND program=?",
            (finding_class, program)
        ).fetchone()["c"]

        accepted = self.conn.execute(
            "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=? AND program=? AND accepted=1",
            (finding_class, program)
        ).fetchone()["c"]

        rejected = total - accepted

        reason_rows = self.conn.execute(
            "SELECT reason, COUNT(*) as cnt FROM rejection_records "
            "WHERE finding_class=? AND program=? AND accepted=0 AND reason != '' "
            "GROUP BY reason ORDER BY cnt DESC LIMIT 5",
            (finding_class, program)
        ).fetchall()
        common_reasons = [r["reason"] for r in reason_rows]

        # Confidence based on sample size
        confidence = "none"
        if total >= 20:
            confidence = "high"
        elif total >= 10:
            confidence = "medium"
        elif total >= 3:
            confidence = "low"

        return EvidenceSummary(
            finding_class=finding_class,
            program=program,
            total=total,
            accepted=accepted,
            rejected=rejected,
            common_reasons=common_reasons,
            confidence=confidence,
        )

    def _aggregate_evidence_global(self, finding_class: str) -> EvidenceSummary:
        """Aggregate evidence across ALL programs for a finding class."""
        total = self.conn.execute(
            "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=?",
            (finding_class,)
        ).fetchone()["c"]

        accepted = self.conn.execute(
            "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=? AND accepted=1",
            (finding_class,)
        ).fetchone()["c"]

        rejected = total - accepted

        reason_rows = self.conn.execute(
            "SELECT reason, COUNT(*) as cnt FROM rejection_records "
            "WHERE finding_class=? AND accepted=0 AND reason != '' "
            "GROUP BY reason ORDER BY cnt DESC LIMIT 5",
            (finding_class,)
        ).fetchall()
        common_reasons = [r["reason"] for r in reason_rows]

        confidence = "none"
        if total >= 20:
            confidence = "high"
        elif total >= 10:
            confidence = "medium"
        elif total >= 3:
            confidence = "low"

        return EvidenceSummary(
            finding_class=finding_class,
            program="__all__",
            total=total,
            accepted=accepted,
            rejected=rejected,
            common_reasons=common_reasons,
            confidence=confidence,
        )

    def evidence_for(self, finding_class: str, program: str = "") -> EvidenceSummary:
        """Get evidence for a specific (class, program) or global for that class."""
        if program:
            ev = self._compute_evidence(finding_class, program)
            if ev.total > 0:
                return ev

        # Fall back to global aggregate across all programs
        return self._aggregate_evidence_global(finding_class)

    def programs_where_accepted(self, finding_class: str) -> list[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT program FROM rejection_records "
            "WHERE finding_class=? AND accepted=1",
            (finding_class,)
        ).fetchall()
        return [r["program"] for r in rows]

    def programs_where_rejected(self, finding_class: str) -> list[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT program FROM rejection_records "
            "WHERE finding_class=? AND accepted=0",
            (finding_class,)
        ).fetchall()
        return [r["program"] for r in rows]

    def all_finding_classes(self) -> list[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT finding_class FROM rejection_records ORDER BY finding_class"
        ).fetchall()
        return [r["finding_class"] for r in rows]

    def count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) as c FROM rejection_records").fetchone()
        return row["c"] if row else 0

    def stats(self) -> dict:
        fc_rows = self.conn.execute(
            "SELECT finding_class, COUNT(*) as cnt FROM rejection_records GROUP BY finding_class"
        ).fetchall()
        return {
            "total": self.count(),
            "by_finding_class": {r["finding_class"]: r["cnt"] for r in fc_rows},
        }


# ── Seed data ───────────────────────────────────────────────────────────

_SEED_RECORDS: list[RejectionRecord] = [
    RejectionRecord("open_redirect", "general", "no_security_impact", source="seed"),
    RejectionRecord("open_redirect", "cloudflare", "no_security_impact", source="seed"),
    RejectionRecord("open_redirect", "shopify", "no_security_impact", source="seed"),
    RejectionRecord("open_redirect", "paypal", "requires_chain", source="seed"),
    RejectionRecord("open_redirect", "uber", "accepted_with_chain", accepted=True, source="seed"),
    RejectionRecord("open_redirect", "facebook", "accepted_with_chain", accepted=True, source="seed"),
    RejectionRecord("open_redirect", "bugcrowd", "no_security_impact", source="seed"),
    RejectionRecord("cors_misconfig", "general", "no_credentials_exposed", source="seed"),
    RejectionRecord("cors_misconfig", "general", "requires_working_xss", source="seed"),
    RejectionRecord("cors_misconfig", "general", "curl_poc_insufficient", source="seed"),
    RejectionRecord("cors_misconfig", "paypal", "requires_browser_poc", source="seed"),
    RejectionRecord("rate_limit", "general", "informative_no_exploit", source="seed"),
    RejectionRecord("rate_limit", "general", "no_security_impact", source="seed"),
    RejectionRecord("rate_limit", "cloudflare", "intended_behavior", source="seed"),
    RejectionRecord("host_header_injection", "general", "requires_chain_to_password_reset", source="seed"),
    RejectionRecord("host_header_injection", "gitlab", "accepted_with_chain", accepted=True, source="seed"),
    RejectionRecord("path_discovery", "general", "next_data_public_by_design", source="seed"),
    RejectionRecord("path_discovery", "general", "firebase_key_public_by_design", source="seed"),
    RejectionRecord("path_discovery", "general", "datadog_rum_public_by_design", source="seed"),
    RejectionRecord("path_discovery", "general", "error_message_no_credentials", source="seed"),
    RejectionRecord("path_discovery", "general", "version_disclosure_informative", source="seed"),
    RejectionRecord("host_header_injection", "shopify", "requires_service_evidence", source="seed"),
    RejectionRecord("xss_reflected", "general", "self_xss", source="seed"),
    RejectionRecord("xss_reflected", "general", "requires_authenticated_session", source="seed"),
    RejectionRecord("debug_endpoints", "general", "stack_trace_no_credentials", source="seed"),
    RejectionRecord("debug_endpoints", "general", "informative_no_exploit", source="seed"),
    RejectionRecord("host_header_injection", "paypal", "requires_chain_to_xss", source="seed"),
    RejectionRecord("cors_misconfig", "general", "csrf_logout_informative", source="seed"),
    RejectionRecord("cors_misconfig", "general", "clickjacking_informative", source="seed"),
    RejectionRecord("ssrf_reflected", "general", "", accepted=True, source="seed"),
    RejectionRecord("ssrf_blind", "general", "", accepted=True, source="seed"),
    RejectionRecord("sqli_error", "general", "", accepted=True, source="seed"),
    RejectionRecord("sqli_time", "general", "", accepted=True, source="seed"),
    RejectionRecord("cmd_injection", "general", "", accepted=True, source="seed"),
    RejectionRecord("ssti", "general", "", accepted=True, source="seed"),
    RejectionRecord("path_discovery", "general", "", accepted=True, source="seed"),
]


# ── Evidence categorizer ─────────────────────────────────────

_REJECTION_CATEGORIES = {
    "no_security_impact": "informative",
    "intended_behavior": "informative",
    "informative_no_exploit": "informative",
    "self_xss": "informative",
    "curl_poc_insufficient": "evidence",
    "requires_browser_poc": "evidence",
    "requires_chain": "evidence",
    "requires_chain_to_password_reset": "evidence",
    "requires_chain_to_xss": "evidence",
    "requires_service_evidence": "evidence",
    "requires_authenticated_session": "evidence",
    "next_data_public_by_design": "wont_fix",
    "firebase_key_public_by_design": "wont_fix",
    "datadog_rum_public_by_design": "wont_fix",
    "error_message_no_credentials": "wont_fix",
    "version_disclosure_informative": "wont_fix",
    "stack_trace_no_credentials": "wont_fix",
    "clickjacking_informative": "wont_fix",
    "csrf_logout_informative": "wont_fix",
    "no_credentials_exposed": "evidence",
    "accepted": "accepted",
    "accepted_with_chain": "accepted",
    "accepted_with_oob_evidence": "accepted",
}


def categorize_reason(reason: str) -> str:
    normalized = reason.lower().replace("-", "_").replace(" ", "_").strip()
    return _REJECTION_CATEGORIES.get(normalized, "other")
