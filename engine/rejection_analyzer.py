"""Phase D2: Rejection Pattern Analyzer.

Tracks what findings get N/A'd across programs, clusters rejection reasons,
and computes rejection rates per (finding_class, program).

Seeded with known rejection patterns from bug bounty experience.
Extendable via add_rejection() / import_from_log().

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
    """One rejection or acceptance event for a finding class on a program."""

    finding_class: str         # Sink ID or vuln class name
    program: str               # Program name
    reason: str = ""           # Rejection reason text
    accepted: bool = False     # True = accepted (counter-example)
    source: str = "manual"     # "manual", "triage_import", "seed"
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Rejection Database ──────────────────────────────────────────────────


class RejectionDB:
    """SQLite-backed store for rejection/acceptance records.

    Computes per-(finding_class, program) metrics:
    - rejection_rate
    - common_reasons
    - programs_where_accepted / programs_where_rejected
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
        for r in _SEED_REJECTIONS:
            self._insert(r)
        self._load_persisted()

    def _load_persisted(self):
        """No-op: records are queried directly from DB; no in-memory dedup needed."""

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
        """Record a rejection event."""
        self._insert(RejectionRecord(
            finding_class=finding_class, program=program,
            reason=reason, accepted=False, source=source,
        ))

    def add_acceptance(self, finding_class: str, program: str,
                       source: str = "manual"):
        """Record an acceptance event (counter-example)."""
        self._insert(RejectionRecord(
            finding_class=finding_class, program=program,
            accepted=True, source=source,
        ))

    def get_metrics(self, finding_class: str = "",
                    program: str = "") -> list[dict]:
        """Get rejection metrics, optionally filtered.

        Returns list of dicts:
            {finding_class, program, total, rejections, acceptances,
             rejection_rate, common_reasons}
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
        results = []
        for row in rows:
            fc, prog = row["finding_class"], row["program"]
            results.append(self._compute_metrics(fc, prog))
        return results

    def _compute_metrics(self, finding_class: str, program: str) -> dict:
        """Compute rejection metrics for a single (finding_class, program)."""
        total = self.conn.execute(
            "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=? AND program=?",
            (finding_class, program)
        ).fetchone()["c"]

        rejections = self.conn.execute(
            "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=? AND program=? AND accepted=0",
            (finding_class, program)
        ).fetchone()["c"]

        acceptances = total - rejections

        # Common rejection reasons
        reason_rows = self.conn.execute(
            "SELECT reason, COUNT(*) as cnt FROM rejection_records "
            "WHERE finding_class=? AND program=? AND accepted=0 AND reason != '' "
            "GROUP BY reason ORDER BY cnt DESC LIMIT 5",
            (finding_class, program)
        ).fetchall()
        common_reasons = [r["reason"] for r in reason_rows]

        return {
            "finding_class": finding_class,
            "program": program,
            "total": total,
            "rejections": rejections,
            "acceptances": acceptances,
            "rejection_rate": round(rejections / total, 2) if total > 0 else 0.0,
            "common_reasons": common_reasons,
        }

    def programs_where_accepted(self, finding_class: str) -> list[str]:
        """Programs where this finding class was accepted (not rejected)."""
        rows = self.conn.execute(
            "SELECT DISTINCT program FROM rejection_records "
            "WHERE finding_class=? AND accepted=1",
            (finding_class,)
        ).fetchall()
        return [r["program"] for r in rows]

    def programs_where_rejected(self, finding_class: str) -> list[str]:
        """Programs where this finding class was rejected."""
        rows = self.conn.execute(
            "SELECT DISTINCT program FROM rejection_records "
            "WHERE finding_class=? AND accepted=0",
            (finding_class,)
        ).fetchall()
        return [r["program"] for r in rows]

    def global_rejection_rate(self, finding_class: str = "") -> float:
        """Overall rejection rate, optionally filtered by finding class."""
        if finding_class:
            total = self.conn.execute(
                "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=?",
                (finding_class,)
            ).fetchone()["c"]
            rejected = self.conn.execute(
                "SELECT COUNT(*) as c FROM rejection_records WHERE finding_class=? AND accepted=0",
                (finding_class,)
            ).fetchone()["c"]
        else:
            total = self.conn.execute(
                "SELECT COUNT(*) as c FROM rejection_records"
            ).fetchone()["c"]
            rejected = self.conn.execute(
                "SELECT COUNT(*) as c FROM rejection_records WHERE accepted=0"
            ).fetchone()["c"]
        return round(rejected / total, 2) if total > 0 else 0.0

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
            "global_rejection_rate": self.global_rejection_rate(),
            "by_finding_class": {r["finding_class"]: r["cnt"] for r in fc_rows},
        }


# ── Seed data ───────────────────────────────────────────────────────────

# Seeded from AGENTS.md bug bounty lessons + never-report skill + known patterns.
# Format: (finding_class, program, reason, accepted)
_SEED_REJECTIONS: list[RejectionRecord] = [
    # -- open_redirect --
    RejectionRecord("open_redirect", "general", "no_security_impact", source="seed"),
    RejectionRecord("open_redirect", "cloudflare", "no_security_impact", source="seed"),
    RejectionRecord("open_redirect", "shopify", "no_security_impact", source="seed"),
    RejectionRecord("open_redirect", "paypal", "requires_chain", source="seed"),
    RejectionRecord("open_redirect", "uber", "accepted_with_chain", accepted=True, source="seed"),
    RejectionRecord("open_redirect", "facebook", "accepted_with_chain", accepted=True, source="seed"),
    RejectionRecord("open_redirect", "bugcrowd", "no_security_impact", source="seed"),

    # -- cors_misconfig --
    RejectionRecord("cors_misconfig", "general", "no_credentials_exposed", source="seed"),
    RejectionRecord("cors_misconfig", "general", "requires_working_xss", source="seed"),
    RejectionRecord("cors_misconfig", "general", "curl_poc_insufficient", source="seed"),
    RejectionRecord("cors_misconfig", "paypal", "requires_browser_poc", source="seed"),

    # -- rate_limit --
    RejectionRecord("rate_limit", "general", "informative_no_exploit", source="seed"),
    RejectionRecord("rate_limit", "general", "no_security_impact", source="seed"),
    RejectionRecord("rate_limit", "cloudflare", "intended_behavior", source="seed"),

    # -- host_header_injection --
    RejectionRecord("host_header_injection", "general", "requires_chain_to_password_reset", source="seed"),
    RejectionRecord("host_header_injection", "gitlab", "accepted_with_chain", accepted=True, source="seed"),

    # -- path_discovery / information_disclosure --
    RejectionRecord("path_discovery", "general", "next_data_public_by_design", source="seed"),
    RejectionRecord("path_discovery", "general", "firebase_key_public_by_design", source="seed"),
    RejectionRecord("path_discovery", "general", "datadog_rum_public_by_design", source="seed"),
    RejectionRecord("path_discovery", "general", "error_message_no_credentials", source="seed"),
    RejectionRecord("path_discovery", "general", "version_disclosure_informative", source="seed"),

    # -- subdomain_takeover --
    RejectionRecord("host_header_injection", "shopify", "requires_service_evidence", source="seed"),

    # -- xss_reflected --
    RejectionRecord("xss_reflected", "general", "self_xss", source="seed"),
    RejectionRecord("xss_reflected", "general", "requires_authenticated_session", source="seed"),

    # -- debug_endpoints --
    RejectionRecord("debug_endpoints", "general", "stack_trace_no_credentials", source="seed"),
    RejectionRecord("debug_endpoints", "general", "informative_no_exploit", source="seed"),

    # -- cache_poisoning --
    RejectionRecord("host_header_injection", "paypal", "requires_chain_to_xss", source="seed"),

    # -- csrf_logout --
    RejectionRecord("cors_misconfig", "general", "csrf_logout_informative", source="seed"),

    # -- clickjacking --
    RejectionRecord("cors_misconfig", "general", "clickjacking_informative", source="seed"),

    # -- ssrf --
    RejectionRecord("ssrf_reflected", "general", "accepted", accepted=True, source="seed"),
    RejectionRecord("ssrf_blind", "general", "accepted_with_oob_evidence", accepted=True, source="seed"),

    # -- sqli --
    RejectionRecord("sqli_error", "general", "accepted", accepted=True, source="seed"),
    RejectionRecord("sqli_time", "general", "accepted", accepted=True, source="seed"),

    # -- cmd_injection --
    RejectionRecord("cmd_injection", "general", "accepted", accepted=True, source="seed"),

    # -- ssti --
    RejectionRecord("ssti", "general", "accepted", accepted=True, source="seed"),

    # -- idor --
    RejectionRecord("path_discovery", "general", "accepted_with_scale_evidence", accepted=True, source="seed"),
]


# ── Rejection reason categorizer ────────────────────────────────────────

# Mapping from rejection reason text to categories
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
    "accepted_with_scale_evidence": "accepted",
}


def categorize_reason(reason: str) -> str:
    """Map a rejection reason to its category.

    Categories: informative, evidence, wont_fix, accepted
    """
    normalized = reason.lower().replace("-", "_").strip()
    return _REJECTION_CATEGORIES.get(normalized, "other")


def summarize_rejection_rate(rate: float) -> str:
    """Human-readable label for a rejection rate."""
    if rate >= 0.8:
        return "highly_likely_rejected"
    elif rate >= 0.5:
        return "likely_rejected"
    elif rate >= 0.2:
        return "uncertain"
    else:
        return "likely_accepted"
