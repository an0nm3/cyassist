"""Phase A1: Feature vector schema — compact attack DNA representation.

Every disclosed bug bounty report becomes one ~500-byte vector.
Stored in SQLite, indexed by (cwe, tech, sink) for fast context-aware queries.

~500 bytes × 10,000 reports = 5MB total storage target.
"""

import hashlib
import json
import re
import sqlite3
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ── Payload Normalization ──────────────────────────────────────────────

_SQL_COMMENT = re.compile(r"--.*$|#.*$", re.MULTILINE)
_SQL_WHITESPACE = re.compile(r"\s+")
_SQL_KEYWORDS = re.compile(
    r"\b(SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|"
    r"UNION|AND|OR|NOT|INTO|VALUES|SET|SLEEP|WAITFOR|BENCHMARK)\b",
    re.IGNORECASE,
)


def normalize_payload(payload: str) -> str:
    """Normalize a payload for deduplication hashing.

    Strips SQL comments, collapses whitespace, lowercases SQL keywords.
    Returns empty string if payload is empty after normalization.
    """
    if not payload or not payload.strip():
        return ""

    # Strip SQL comments
    cleaned = _SQL_COMMENT.sub("", payload)
    # Collapse whitespace
    cleaned = _SQL_WHITESPACE.sub(" ", cleaned).strip()
    # Lowercase SQL keywords (leave rest as-is for non-SQL payloads)
    cleaned = _SQL_KEYWORDS.sub(lambda m: m.group(1).lower(), cleaned)

    return cleaned


def payload_hash(payload: str) -> str:
    """SHA-256 hash of normalized payload. First 16 hex chars for dedup key."""
    norm = normalize_payload(payload)
    if not norm:
        return ""
    return hashlib.sha256(norm.encode()).hexdigest()[:16]


# ── Tech Stack Helpers ─────────────────────────────────────────────────

_KNOWN_TECHS = {
    "python", "flask", "django", "fastapi", "python3",
    "javascript", "node", "express", "nextjs", "react", "vue", "angular",
    "php", "laravel", "symfony", "wordpress",
    "java", "spring", "tomcat", "struts",
    "ruby", "rails",
    "go", "gin",
    "csharp", "dotnet", "aspnet",
    "rust", "actix",
    "postgresql", "mysql", "mariadb", "mssql", "oracle", "sqlite",
    "mongodb", "couchdb", "dynamodb",
    "graphql", "rest", "grpc",
    "docker", "kubernetes", "aws", "gcp", "azure",
    "nginx", "apache", "caddy", "iis",
    "cloudflare", "akamai", "fastly",
}


def tech_fingerprint_headers(headers: dict) -> list[str]:
    """Extract tech stack from HTTP response headers."""
    techs = []
    headers_lower = {k.lower(): v for k, v in headers.items()}

    server = headers_lower.get("server", "")
    if "nginx" in server.lower():
        techs.append("nginx")
    if "apache" in server.lower():
        techs.append("apache")
    if "iis" in server.lower():
        techs.append("iis")
    if "caddy" in server.lower():
        techs.append("caddy")
    if "cloudflare" in server.lower():
        techs.append("cloudflare")

    x_powered = headers_lower.get("x-powered-by", "")
    if "express" in x_powered.lower():
        techs.append("express")
    if "php" in x_powered.lower():
        techs.append("php")
    if "asp.net" in x_powered.lower():
        techs.append("aspnet")

    x_frame = headers_lower.get("x-frame-options", "")
    if x_frame:
        techs.append("has_xfo")  # generic security header signal

    set_cookie = headers_lower.get("set-cookie", "")
    if "connect.sid" in set_cookie.lower():
        techs.append("express")
    if "jsessionid" in set_cookie.lower():
        techs.append("java")

    return sorted(set(techs))


def tech_fingerprint_body(body: str) -> list[str]:
    """Extract tech stack from response body content."""
    techs = []
    body_lower = body.lower()

    if "__next_data__" in body_lower:
        techs.append("nextjs")
    if "_reactroot" in body_lower or "react." in body_lower:
        techs.append("react")
    if "vue." in body_lower or "vuejs" in body_lower:
        techs.append("vue")
    if "angular." in body_lower or "ng-app" in body_lower:
        techs.append("angular")
    if "wp-content" in body_lower or "wp-includes" in body_lower:
        techs.append("wordpress")
    if "django" in body_lower and "csrf" in body_lower:
        techs.append("django")
    if "laravel" in body_lower:
        techs.append("laravel")
    if "graphql" in body_lower:
        techs.append("graphql")
    if "swagger" in body_lower or "openapi" in body_lower:
        techs.append("rest")

    return sorted(set(techs))


# ── Feature Vector ─────────────────────────────────────────────────────


@dataclass
class FeatureVector:
    """Compact representation of one vulnerability from a disclosed report.

    Storage target: ~500 bytes per vector.
    No raw report body stored — only extracted features.
    """

    # Identification
    source_url: str
    source_platform: str  # "h1", "immunefi", "medium", "rudra_feedback"
    report_title: str = ""

    # Classification
    cwe: str = ""  # CWE number (e.g., "89", "79", "918")
    tech: list[str] = field(default_factory=list)  # tech stack inferred
    sink: str = ""  # vulnerable function/pattern (e.g., "cursor.execute()")
    param_type: str = ""  # "integer", "string", "json", "file", "url"

    # Payload
    payload_class: str = ""  # "time_based", "error_based", "union", "reflected", etc.
    payload: str = ""  # the actual probe payload
    response_shape: str = ""  # "timing_delta", "error_message", "content_reflection"

    # Auth context
    auth_required: bool = False

    # Confidence / tracking
    confidence: float = 0.5  # 0.0–1.0, based on evidence quality
    evidence_count: int = 1  # how many reports produced same normalized payload
    normalized_payload_hash: str = ""  # dedup hash, computed from payload
    created_at: str = ""

    # Lifecycle (v11.15.0 — Phase B4)
    status: str = "active"  # "active" | "pending_review" | "promoted"
    rudra_session_id: str = ""  # dedup key for Rudra feedback submissions

    # Feedback outcome (Phase E — v3.2.0)
    accepted: bool = False   # True = finding was accepted by triage
    dup_of: str = ""         # Report ID if marked duplicate
    informative: bool = False  # True = marked informative/N-A
    reward: str = ""         # Bounty amount (e.g. "$500")
    notes: str = ""          # Free-text notes about outcome

    def __post_init__(self):
        if not self.normalized_payload_hash and self.payload:
            self.normalized_payload_hash = payload_hash(self.payload)
        if not self.created_at:
            self.created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_row(self) -> dict:
        """Convert to flat dict for SQLite insertion."""
        return {
            "source_url": self.source_url,
            "source_platform": self.source_platform,
            "report_title": self.report_title,
            "cwe": self.cwe,
            "tech": json.dumps(sorted(self.tech)),  # sorted for deterministic matching
            "sink": self.sink,
            "param_type": self.param_type,
            "payload_class": self.payload_class,
            "payload": self.payload,
            "response_shape": self.response_shape,
            "auth_required": int(self.auth_required),
            "confidence": self.confidence,
            "evidence_count": self.evidence_count,
            "payload_hash": self.normalized_payload_hash,
            "created_at": self.created_at,
            "status": self.status,
            "rudra_session_id": self.rudra_session_id,
            "accepted": int(self.accepted),
            "dup_of": self.dup_of,
            "informative": int(self.informative),
            "reward": self.reward,
            "notes": self.notes,
        }

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "FeatureVector":
        """Reconstruct from SQLite row."""
        return cls(
            source_url=row["source_url"],
            source_platform=row["source_platform"],
            report_title=row["report_title"],
            cwe=row["cwe"],
            tech=sorted(json.loads(row["tech"])) if row["tech"] else [],
            sink=row["sink"],
            param_type=row["param_type"],
            payload_class=row["payload_class"],
            payload=row["payload"],
            response_shape=row["response_shape"],
            auth_required=bool(row["auth_required"]),
            confidence=row["confidence"],
            evidence_count=row["evidence_count"],
            normalized_payload_hash=row["payload_hash"],
            created_at=row["created_at"],
            status=row["status"],
            rudra_session_id=row["rudra_session_id"],
            accepted=bool(row["accepted"]),
            dup_of=row["dup_of"],
            informative=bool(row["informative"]),
            reward=row["reward"],
            notes=row["notes"],
        )

    def estimated_bytes(self) -> int:
        """Rough estimate of serialized size."""
        return len(json.dumps(self.to_row()))


# ── Vector Store (SQLite) ──────────────────────────────────────────────


class VectorStore:
    """SQLite-backed storage for feature vectors.

    Indexed by (cwe, tech_json, sink) for fast querying.
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS feature_vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_url TEXT NOT NULL,
        source_platform TEXT NOT NULL DEFAULT '',
        report_title TEXT DEFAULT '',
        cwe TEXT DEFAULT '',
        tech TEXT DEFAULT '[]',          -- JSON array of tech strings
        sink TEXT DEFAULT '',
        param_type TEXT DEFAULT '',
        payload_class TEXT DEFAULT '',
        payload TEXT DEFAULT '',
        response_shape TEXT DEFAULT '',
        auth_required INTEGER DEFAULT 0,
        confidence REAL DEFAULT 0.5,
        evidence_count INTEGER DEFAULT 1,
        payload_hash TEXT DEFAULT '',
        created_at TEXT DEFAULT '',
        status TEXT DEFAULT 'active',
        rudra_session_id TEXT DEFAULT '',
        accepted INTEGER DEFAULT 0,
        dup_of TEXT DEFAULT '',
        informative INTEGER DEFAULT 0,
        reward TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        UNIQUE(payload_hash, cwe, status)
    );

    CREATE INDEX IF NOT EXISTS idx_vector_cwe ON feature_vectors(cwe);
    CREATE INDEX IF NOT EXISTS idx_vector_tech ON feature_vectors(tech);
    CREATE INDEX IF NOT EXISTS idx_vector_sink ON feature_vectors(sink);
    CREATE INDEX IF NOT EXISTS idx_vector_payload_hash ON feature_vectors(payload_hash);
    """

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "vectors.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.executescript(self.SCHEMA)
            self._migrate_schema()
        return self._conn

    def _migrate_schema(self):
        """Add columns from newer schema versions if missing."""
        existing = {r["name"] for r in self.conn.execute("PRAGMA table_info(feature_vectors)")}
        for col, col_def in [("status", "TEXT DEFAULT 'active'"),
                              ("rudra_session_id", "TEXT DEFAULT ''"),
                              ("accepted", "INTEGER DEFAULT 0"),
                              ("dup_of", "TEXT DEFAULT ''"),
                              ("informative", "INTEGER DEFAULT 0"),
                              ("reward", "TEXT DEFAULT ''"),
                              ("notes", "TEXT DEFAULT ''")]:
            if col not in existing:
                self.conn.execute(f"ALTER TABLE feature_vectors ADD COLUMN {col} {col_def}")
        # Recreate index if UNIQUE constraint changed — ignore error if exists
        try:
            self.conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_vector_unique ON feature_vectors(payload_hash, cwe, status)")
        except Exception:
            pass

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── Insert ──────────────────────────────────────────────────────────

    def insert(self, vector: FeatureVector) -> bool:
        """Insert a feature vector. Returns True if new, False if duplicate."""
        try:
            row = vector.to_row()
            cur = self.conn.execute(
                """INSERT OR IGNORE INTO feature_vectors
                (source_url, source_platform, report_title,
                 cwe, tech, sink, param_type, payload_class, payload,
                 response_shape, auth_required, confidence, evidence_count,
                 payload_hash, created_at, status, rudra_session_id,
                 accepted, dup_of, informative, reward, notes)
                VALUES (:source_url, :source_platform, :report_title,
                        :cwe, :tech, :sink, :param_type, :payload_class, :payload,
                        :response_shape, :auth_required, :confidence, :evidence_count,
                        :payload_hash, :created_at, :status, :rudra_session_id,
                        :accepted, :dup_of, :informative, :reward, :notes)""",
                row,
            )
            self.conn.commit()
            return cur.rowcount > 0
        except Exception:
            return False

    def insert_many(self, vectors: list[FeatureVector]) -> int:
        """Insert multiple vectors. Returns count of new insertions."""
        count = 0
        for v in vectors:
            if self.insert(v):
                count += 1
        return count

    # ── Pending Review (Phase B4 — Rudra Feedback) ─────────────────────

    def insert_pending(self, vector: FeatureVector, session_id: str = "") -> str:
        """Insert a Rudra-submitted finding as pending_review.

        Returns "accepted" if new, "duplicate" if already exists, "error" on failure.
        """
        vector.status = "pending_review"
        vector.source_platform = "rudra_feedback"
        vector.rudra_session_id = session_id
        try:
            row = vector.to_row()
            cur = self.conn.execute(
                """INSERT OR IGNORE INTO feature_vectors
                (source_url, source_platform, report_title,
                 cwe, tech, sink, param_type, payload_class, payload,
                 response_shape, auth_required, confidence, evidence_count,
                 payload_hash, created_at, status, rudra_session_id,
                 accepted, dup_of, informative, reward, notes)
                VALUES (:source_url, :source_platform, :report_title,
                        :cwe, :tech, :sink, :param_type, :payload_class, :payload,
                        :response_shape, :auth_required, :confidence, :evidence_count,
                        :payload_hash, :created_at, :status, :rudra_session_id,
                        :accepted, :dup_of, :informative, :reward, :notes)""",
                row,
            )
            self.conn.commit()
            if cur.rowcount > 0:
                return "accepted"
            return "duplicate"
        except Exception:
            return "error"

    def pending_count(self) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) as c FROM feature_vectors WHERE status = 'pending_review'"
        ).fetchone()
        return row["c"] if row else 0

    def promote_pending(self, payload_hash: str) -> bool:
        """Promote a pending_review vector to active status."""
        cur = self.conn.execute(
            "UPDATE feature_vectors SET status = 'promoted' WHERE payload_hash = ? AND status = 'pending_review'",
            (payload_hash,),
        )
        self.conn.commit()
        return cur.rowcount > 0

    # ── Query ────────────────────────────────────────────────────────────

    def query(
        self,
        cwe: str = "",
        tech: Optional[list[str]] = None,
        sink: str = "",
        min_confidence: float = 0.0,
        limit: int = 10,
    ) -> list[FeatureVector]:
        """Query vectors by CWE + tech + sink. Ordered by confidence desc."""
        conditions = []
        params = {}

        if cwe:
            conditions.append("cwe = :cwe")
            params["cwe"] = cwe

        if tech:
            tech_json = json.dumps(sorted(set(tech)))
            conditions.append("tech = :tech")
            params["tech"] = tech_json

        if sink:
            conditions.append("sink = :sink")
            params["sink"] = sink

        if min_confidence > 0:
            conditions.append("confidence >= :min_conf")
            params["min_conf"] = min_confidence

        where = " AND ".join(conditions) if conditions else "1=1"
        sql = f"SELECT * FROM feature_vectors WHERE {where} ORDER BY confidence DESC, evidence_count DESC LIMIT :limit"
        params["limit"] = limit

        rows = self.conn.execute(sql, params).fetchall()
        return [FeatureVector.from_row(r) for r in rows]

    def query_by_payload_hash(self, payload_hash: str) -> list[FeatureVector]:
        """Find vectors with matching payload hash (dedup check)."""
        rows = self.conn.execute(
            "SELECT * FROM feature_vectors WHERE payload_hash = ?",
            (payload_hash,),
        ).fetchall()
        return [FeatureVector.from_row(r) for r in rows]

    # ── Stats ────────────────────────────────────────────────────────────

    def count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) as c FROM feature_vectors").fetchone()
        return row["c"] if row else 0

    def count_by_cwe(self, cwe: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) as c FROM feature_vectors WHERE cwe = ?", (cwe,)
        ).fetchone()
        return row["c"] if row else 0

    def top_cwes(self, n: int = 10) -> list[tuple[str, int]]:
        rows = self.conn.execute(
            "SELECT cwe, COUNT(*) as cnt FROM feature_vectors "
            "WHERE cwe != '' GROUP BY cwe ORDER BY cnt DESC LIMIT ?",
            (n,),
        ).fetchall()
        return [(r["cwe"], r["cnt"]) for r in rows]

    def size_bytes(self) -> int:
        if self.db_path.exists():
            return self.db_path.stat().st_size
        return 0

    # ── Aggregation ──────────────────────────────────────────────────────

    def merge_duplicates(self):
        """Merge duplicate payloads: sum evidence_count, keep highest confidence.

        Run periodically (e.g., after each batch insert).
        """
        self.conn.executescript("""
            CREATE TEMP TABLE dup_merge AS
            SELECT payload_hash, cwe,
                   COUNT(*) as total_evidence,
                   MAX(confidence) as best_confidence,
                   MIN(rowid) as keep_id
            FROM feature_vectors
            WHERE payload_hash != ''
            GROUP BY payload_hash, cwe
            HAVING COUNT(*) > 1;

            UPDATE feature_vectors SET
                evidence_count = (
                    SELECT total_evidence FROM dup_merge
                    WHERE dup_merge.payload_hash = feature_vectors.payload_hash
                    AND dup_merge.cwe = feature_vectors.cwe
                ),
                confidence = (
                    SELECT best_confidence FROM dup_merge
                    WHERE dup_merge.payload_hash = feature_vectors.payload_hash
                    AND dup_merge.cwe = feature_vectors.cwe
                )
            WHERE rowid IN (
                SELECT keep_id FROM dup_merge
            );

            DELETE FROM feature_vectors WHERE rowid NOT IN (
                SELECT MIN(rowid) FROM feature_vectors
                GROUP BY payload_hash, cwe
            );

            DROP TABLE IF EXISTS dup_merge;
        """)
        self.conn.commit()


# ── Confidence Calculator ──────────────────────────────────────────────


def calculate_confidence(
    evidence_count: int,
    source_platform: str = "h1",
    has_cwe: bool = False,
    has_payload: bool = False,
    has_tech: bool = False,
    has_sink: bool = False,
) -> float:
    """Calculate confidence score for a feature vector.

    Base confidence from evidence count, then adjusted by metadata quality.
    """
    base = min(0.3 + (evidence_count - 1) * 0.05, 0.9)

    platform_boost = {"h1": 0.05, "immunefi": 0.05, "rudra_feedback": 0.1}
    base += platform_boost.get(source_platform, 0.0)

    if has_cwe:
        base += 0.05
    if has_payload:
        base += 0.1
    if has_tech:
        base += 0.05
    if has_sink:
        base += 0.05

    return min(base, 1.0)
