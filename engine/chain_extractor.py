"""Phase C1: Chain Pattern Extractor.

Extracts chain patterns from H1 disclosed reports and provides a seeded index
of known vulnerability chains. A chain combines 2+ primitives for greater impact.

Seeded with 15 known chain patterns from real bug bounty writeups.
H1 parser enriches the index over time.

Storage: SQLite table `chain_patterns` in the same VectorStore database.
"""

import json
import logging
import re
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("chain_extractor")


# ── Data Model ──────────────────────────────────────────────────────────


@dataclass
class ChainPattern:
    """One chain pattern: primitive A + primitive B = impact.

    Example:
        ChainPattern("open_redirect", "oauth_misconfig",
                      "OAuth redirect_uri bypass -> auth code theft",
                      ["OAuth flow uses redirect_uri param",
                       "redirect_uri not validated against allowlist"],
                      cvss_bump=3.0, sink_a="open_redirect", sink_b="oauth_misconfig")
    """

    primitive_a: str          # vuln class or sink_id (e.g. "open_redirect")
    primitive_b: str          # vuln class or sink_id (e.g. "oauth_misconfig")
    impact: str               # description of chain result
    conditions: list[str] = field(default_factory=list)
    cvss_bump: float = 1.0    # additional CVSS when chained
    sink_a: str = ""          # matching sink_id (inferred from primitive_a if empty)
    sink_b: str = ""
    source_url: str = ""
    source_platform: str = "seed"  # "seed", "h1", "rudra_discovery"
    evidence_count: int = 1
    created_at: str = ""

    def __post_init__(self):
        if not self.sink_a:
            self.sink_a = _primitive_to_sink(self.primitive_a)
        if not self.sink_b:
            self.sink_b = _primitive_to_sink(self.primitive_b)
        if not self.created_at:
            self.created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def key(self) -> tuple[str, str]:
        """Deterministic key for dedup: sorted(sink_a, sink_b)."""
        a, b = sorted([self.sink_a, self.sink_b])
        return (a, b)

    def to_row(self) -> dict:
        return {
            "primitive_a": self.primitive_a,
            "primitive_b": self.primitive_b,
            "sink_a": self.sink_a,
            "sink_b": self.sink_b,
            "impact": self.impact,
            "conditions": json.dumps(self.conditions),
            "cvss_bump": self.cvss_bump,
            "source_url": self.source_url,
            "source_platform": self.source_platform,
            "evidence_count": self.evidence_count,
            "created_at": self.created_at,
        }

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "ChainPattern":
        return cls(
            primitive_a=row["primitive_a"],
            primitive_b=row["primitive_b"],
            sink_a=row["sink_a"],
            sink_b=row["sink_b"],
            impact=row["impact"],
            conditions=json.loads(row["conditions"]) if row["conditions"] else [],
            cvss_bump=row["cvss_bump"],
            source_url=row["source_url"],
            source_platform=row["source_platform"],
            evidence_count=row["evidence_count"],
            created_at=row["created_at"],
        )


# ── Primitive → Sink ID Mapping ─────────────────────────────────────────

_PRIMITIVE_TO_SINK: dict[str, str] = {
    "xss": "xss_reflected",
    "sqli": "sqli_error",
    "sqli_time": "sqli_time",
    "ssrf": "ssrf_reflected",
    "ssrf_blind": "ssrf_blind",
    "ssti": "ssti",
    "cmd_injection": "cmd_injection",
    "path_discovery": "path_discovery",
    "debug_endpoints": "debug_endpoints",
    "cors_misconfig": "cors_misconfig",
    "open_redirect": "open_redirect",
    "host_header_injection": "host_header_injection",
    "path_traversal": "path_traversal",
    "nosqli": "nosqli",
    "jwt_attack": "jwt_attack",
    "jwt_confusion": "jwt_confusion",
    "oauth_misconfig": "oauth_misconfig",
    "rate_limit": "rate_limit",
    "cloud_metadata": "cloud_metadata",
    "idors": "path_discovery",
    "file_upload": "path_traversal",
    "subdomain_takeover": "host_header_injection",
    "cache_poisoning": "host_header_injection",
    "prototype_pollution": "ssti",
    "clickjacking": "cors_misconfig",
    "session_fixation": "jwt_attack",
    "csrf": "cors_misconfig",
    "information_disclosure": "path_discovery",
    "ato": "rate_limit",
    "auth_bypass": "jwt_attack",
}


def _primitive_to_sink(name: str) -> str:
    return _PRIMITIVE_TO_SINK.get(name, name)


# ── Seed Patterns ───────────────────────────────────────────────────────

_SEED_PATTERNS = [
    ChainPattern(
        "open_redirect", "oauth_misconfig",
        "OAuth redirect_uri bypass leads to auth code theft — attacker intercepts OAuth callback via open redirect",
        conditions=["OAuth flow uses redirect_uri parameter",
                     "redirect_uri not validated against allowlist",
                     "open redirect on same origin or whitelisted domain"],
        cvss_bump=3.0, source_platform="seed",
    ),
    ChainPattern(
        "idors", "rate_limit",
        "IDOR + missing rate limit enables mass data exfiltration — iterate user IDs to dump all records",
        conditions=["IDOR in list/view endpoint",
                     "no rate limiting on the endpoint",
                     "predictable or enumerable user IDs"],
        cvss_bump=2.5, source_platform="seed",
    ),
    ChainPattern(
        "ssrf", "cloud_metadata",
        "SSRF to cloud metadata service leaks cloud provider credentials (AWS IMDS / GCP metadata / Azure IMDS)",
        conditions=["outbound HTTP request to attacker-controlled URL",
                     "cloud metadata endpoint not blocked",
                     "IMDSv1 enabled (no token required)"],
        cvss_bump=3.5, source_platform="seed",
    ),
    ChainPattern(
        "xss", "csrf",
        "Stored XSS bypasses CSRF protections — attacker executes authenticated actions on victim's behalf",
        conditions=["stored XSS in user-content field",
                     "CSRF token not bound to session or missing",
                     "sensitive action endpoint accessible via XSS"],
        cvss_bump=2.0, source_platform="seed",
    ),
    ChainPattern(
        "file_upload", "path_traversal",
        "File upload with path traversal in filename overwrites system files -> RCE",
        conditions=["file upload endpoint accepts filename with ../",
                     "uploaded files stored on same filesystem as application code",
                     "web server serves uploaded files with execute permission"],
        cvss_bump=3.0, source_platform="seed",
    ),
    ChainPattern(
        "subdomain_takeover", "oauth_misconfig",
        "Subdomain takeover on OAuth redirect_uri domain enables auth code theft for any user",
        conditions=["OAuth redirect_uri points to subdomain with dangling DNS",
                     "attacker can claim the subdomain (AWS S3, GitHub Pages, Heroku, etc.)",
                     "OAuth client_id is the target application's registered client"],
        cvss_bump=3.5, source_platform="seed",
    ),
    ChainPattern(
        "rate_limit", "sqli",
        "No rate limit on login enables blind SQLi exploitation via timing-based payload repetition",
        conditions=["SQLi exists but requires many requests to extract data",
                     "no rate limiting on the vulnerable endpoint",
                     "time-based or error-based extraction feasible"],
        cvss_bump=1.0, source_platform="seed",
    ),
    ChainPattern(
        "host_header_injection", "idors",
        "Host header injection in password reset link redirects reset token to attacker -> account takeover",
        conditions=["password reset flow uses Host header to generate reset link",
                     "reset token is a one-time URL with no additional auth check",
                     "attacker can intercept the victim's reset email"],
        cvss_bump=3.0, source_platform="seed",
    ),
    ChainPattern(
        "prototype_pollution", "xss",
        "Server-side prototype pollution in Object.assign/lodash.merge enables RCE or XSS via polluted prototype reaching a sink",
        conditions=["application merges user-controlled JSON with objects",
                     "merged property reaches dangerous sink (eval, innerHTML, res.send)",
                     "Node.js or browser environment"],
        cvss_bump=3.0, source_platform="seed",
    ),
    ChainPattern(
        "cache_poisoning", "xss",
        "Web cache poisoning with XSS payload delivers persistent XSS to every user hitting the cached page",
        conditions=["CDN or reverse proxy caches responses based on request headers",
                     "unkeyed header contains XSS payload that gets reflected in cached response",
                     "no Cache-Control: no-store on dynamic pages"],
        cvss_bump=2.5, source_platform="seed",
    ),
    ChainPattern(
        "session_fixation", "jwt_attack",
        "Session fixation combined with missing re-auth on privilege escalation enables persistent ATO",
        conditions=["application accepts pre-set session ID",
                     "no session regeneration after login",
                     "attacker can force victim to use known session"],
        cvss_bump=2.5, source_platform="seed",
    ),
    ChainPattern(
        "ssrf", "ssrf_blind",
        "Blind SSRF to internal port scan maps internal network topology -> enables targeted attacks",
        conditions=["application fetches attacker-controlled URL",
                     "response timing or error messages reveal port state",
                     "internal network segments accessible from application server"],
        cvss_bump=2.0, source_platform="seed",
    ),
    ChainPattern(
        "clickjacking", "cors_misconfig",
        "Clickjacking on sensitive action endpoint combined with CORS misconfig enables data theft",
        conditions=["X-Frame-Options missing on sensitive action page",
                     "CORS allows credentialed requests from attacker origin",
                     "victim can be lured to attacker-controlled page"],
        cvss_bump=1.5, source_platform="seed",
    ),
    ChainPattern(
        "debug_endpoints", "sqli",
        "Debug endpoint leaks SQL query structure enabling precise blind SQLi payload crafting",
        conditions=["debug endpoint exposes query structure or error messages",
                     "SQLi exists but requires complex syntax to exploit",
                     "information leak narrows payload injection points"],
        cvss_bump=0.5, source_platform="seed",
    ),
    ChainPattern(
        "xss", "oauth_misconfig",
        "XSS on OAuth-authenticated app steals access tokens from localStorage or cookies -> persistent ATO",
        conditions=["OAuth access token stored in browser storage accessible via JS",
                     "XSS on same origin",
                     "no httpOnly flag on auth cookies or token in localStorage"],
        cvss_bump=2.5, source_platform="seed",
    ),
    ChainPattern(
        "nosqli", "path_discovery",
        "NoSQL injection in $where operator leaks hidden API endpoints and internal paths via error messages",
        conditions=["$where or $regex injection possible in NoSQL query",
                     "error messages or timing reveal internal endpoint names",
                     "hidden endpoints discovered expand attack surface"],
        cvss_bump=1.0, source_platform="seed",
    ),
    ChainPattern(
        "sqli", "ssrf",
        "SQLi with INTO OUTFILE / LOAD_FILE writes web shell onto application server SSRF-accessible endpoint",
        conditions=["MySQL/MariaDB with FILE privilege",
                     "writeable web directory reachable from DB server",
                     "SSRF or direct access to written file"],
        cvss_bump=3.5, source_platform="seed",
    ),
    ChainPattern(
        "ssti", "ssrf",
        "SSTI in template engine with file read capability enables SSRF to internal services using fetched credentials",
        conditions=["SSTI with file read (Jinja2 cycler, Freemarker TemplateModel)",
                     "credentials found in config files point to internal service",
                     "internal service accessible from application server"],
        cvss_bump=2.5, source_platform="seed",
    ),
]

# ── H1 Report Parser ────────────────────────────────────────────────────

# Patterns that suggest a chain is being described
_CHAIN_SIGNALS = re.compile(
    r"(chain|chained|combine|combined|escalate|escalation|"
    r"this leads? to|this allows? to|bypass both|"
    r"vulnerability chain|attack chain|step[-\s]by[-\s]step)", re.IGNORECASE
)

# CWE tags in H1 reports: "CWE-79: Cross-site Scripting" or "cwe: 79"
_CWE_TAG = re.compile(r'CWE[:\s-]*(\d{2,4})', re.IGNORECASE)

# Vulnerability class keywords mapped to primitives
_VULN_KEYWORDS: dict[str, list[str]] = {
    "xss": ["cross-site scripting", "xss", "script injection"],
    "sqli": ["sql injection", "sqli", "sql", "mysql", "postgres"],
    "ssrf": ["server-side request forgery", "ssrf", "request forgery"],
    "ssti": ["template injection", "ssti", "template"],
    "cmd_injection": ["command injection", "rce", "remote code execution", "cmd"],
    "open_redirect": ["open redirect", "redirect", "url redirect"],
    "idors": ["idor", "insecure direct object", "access control"],
    "oauth_misconfig": ["oauth", "auth code", "redirect_uri", "access token"],
    "path_traversal": ["path traversal", "directory traversal", "lfi", "file inclusion"],
    "rate_limit": ["rate limit", "no rate limit", "brute force"],
    "file_upload": ["file upload", "upload", "arbitrary file"],
    "host_header_injection": ["host header", "host injection", "password reset"],
    "cloud_metadata": ["metadata", "imds", "cloud metadata"],
    "csrf": ["csrf", "cross-site request forgery"],
    "subdomain_takeover": ["subdomain takeover", "dangling dns"],
    "cache_poisoning": ["cache poisoning", "web cache"],
    "prototype_pollution": ["prototype pollution", "proto pollution"],
    "clickjacking": ["clickjack", "clickjack", "ui redress"],
    "session_fixation": ["session fixation", "session"],
    "nosqli": ["nosql injection", "nosqli", "mongodb injection"],
    "jwt_attack": ["jwt", "json web token", "token"],
    "debug_endpoints": ["debug", "stack trace", "information disclosure"],
    "cors_misconfig": ["cors", "cross-origin"],
    "information_disclosure": ["information disclosure", "info leak", "path disclosure"],
    "ato": ["account takeover", "ato", "credential theft", "session hijack"],
    "auth_bypass": ["auth bypass", "authentication bypass", "privilege escalation"],
}

# Impact keywords for extracting the chain impact statement
_IMPACT_MARKERS = re.compile(
    r"(impact|result|consequence|this means|"
    r"attacker can|allows an attacker|leading to|resulting in)", re.IGNORECASE
)


def _detect_primitives(text: str) -> list[str]:
    """Detect vulnerability classes mentioned in report text."""
    text_lower = text.lower()
    found = []
    for prim, keywords in _VULN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(prim)
                break
    return found


def _extract_impact(text: str) -> str:
    """Extract impact statement (first sentence after an impact marker)."""
    match = _IMPACT_MARKERS.search(text)
    if match:
        start = match.end()
        end = text.find(".", start)
        if end > start:
            return text[start:end].strip()
    return ""


def extract_chains_from_report(report_text: str, source_url: str = "") -> list[ChainPattern]:
    """Parse H1 report text for chain patterns.

    Looks for:
    1. Chain signal keywords ("chain", "combined", "escalate", etc.)
    2. Multiple CWE tags or vulnerability class mentions
    3. Impact statement

    Returns list of ChainPatterns (may be empty).
    """
    if not _CHAIN_SIGNALS.search(report_text):
        return []

    primitives = _detect_primitives(report_text)
    if len(primitives) < 2:
        return []

    impact = _extract_impact(report_text)
    if not impact:
        impact = f"{primitives[0]} chained with {primitives[1]} leads to increased impact"

    results = []
    seen = set()
    for i in range(len(primitives)):
        for j in range(i + 1, len(primitives)):
            a, b = primitives[i], primitives[j]
            key = tuple(sorted([a, b]))
            if key in seen:
                continue
            seen.add(key)
            results.append(ChainPattern(
                primitive_a=a,
                primitive_b=b,
                impact=impact,
                conditions=[],
                cvss_bump=1.5,
                source_url=source_url,
                source_platform="h1",
                evidence_count=1,
            ))

    return results


# ── Chain Index ─────────────────────────────────────────────────────────


class ChainIndex:
    """Index of chain patterns, seeded + supplemented by H1 extraction.

    Backed by an in-memory dict + optional SQLite persistence.
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS chain_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        primitive_a TEXT NOT NULL,
        primitive_b TEXT NOT NULL,
        sink_a TEXT NOT NULL DEFAULT '',
        sink_b TEXT NOT NULL DEFAULT '',
        impact TEXT NOT NULL,
        conditions TEXT DEFAULT '[]',
        cvss_bump REAL DEFAULT 1.0,
        source_url TEXT DEFAULT '',
        source_platform TEXT DEFAULT 'seed',
        evidence_count INTEGER DEFAULT 1,
        created_at TEXT DEFAULT '',
        UNIQUE(sink_a, sink_b)
    );
    CREATE INDEX IF NOT EXISTS idx_chain_a ON chain_patterns(sink_a);
    CREATE INDEX IF NOT EXISTS idx_chain_b ON chain_patterns(sink_b);
    CREATE INDEX IF NOT EXISTS idx_chain_platform ON chain_patterns(source_platform);
    """

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "vectors.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        # In-memory fast lookup: (sink_a, sink_b) -> ChainPattern
        self._by_pair: dict[tuple[str, str], ChainPattern] = {}
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
        _ = self.conn  # ensure schema created

    def _load_seeds(self):
        for p in _SEED_PATTERNS:
            self._upsert(p)
        self._load_persisted()

    def _load_persisted(self):
        """Load non-seed patterns from SQLite into _by_pair."""
        rows = self.conn.execute(
            "SELECT * FROM chain_patterns WHERE source_platform != 'seed'"
        ).fetchall()
        for row in rows:
            p = ChainPattern.from_row(row)
            self._by_pair[(p.sink_a, p.sink_b)] = p
            self._by_pair[(p.sink_b, p.sink_a)] = p

    def _upsert(self, pattern: ChainPattern):
        """Insert or update a chain pattern."""
        self._by_pair[(pattern.sink_a, pattern.sink_b)] = pattern
        self._by_pair[(pattern.sink_b, pattern.sink_a)] = pattern
        try:
            row = pattern.to_row()
            self.conn.execute(
                """INSERT OR REPLACE INTO chain_patterns
                (primitive_a, primitive_b, sink_a, sink_b, impact, conditions,
                 cvss_bump, source_url, source_platform, evidence_count, created_at)
                VALUES (:primitive_a, :primitive_b, :sink_a, :sink_b, :impact, :conditions,
                        :cvss_bump, :source_url, :source_platform, :evidence_count, :created_at)""",
                row,
            )
            self.conn.commit()
        except Exception as e:
            logger.debug(f"ChainIndex upsert failed: {e}")

    # ── Public API ───────────────────────────────────────────────────

    def lookup(self, sink_a: str, sink_b: str) -> Optional[ChainPattern]:
        """Look up a chain pattern by (sink_a, sink_b) — order-independent.
        Accepts both primitive names and sink IDs.
        """
        a = _primitive_to_sink(sink_a)
        b = _primitive_to_sink(sink_b)
        key = (a, b)
        if key in self._by_pair:
            return self._by_pair[key]
        key2 = (b, a)
        return self._by_pair.get(key2)

    def lookup_by_sink(self, sink_id: str) -> list[ChainPattern]:
        """All chain patterns involving a given sink."""
        results = []
        for (a, b), p in self._by_pair.items():
            if a == sink_id and (sink_id, b) not in {(r.sink_a, r.sink_b) for r in results}:
                results.append(p)
        return results

    def add_from_report(self, report_text: str, source_url: str = "") -> int:
        """Parse and add chain patterns from an H1 report. Returns count of new patterns."""
        patterns = extract_chains_from_report(report_text, source_url)
        count = 0
        for p in patterns:
            if self.add(p):
                count += 1
        return count

    def add(self, pattern: ChainPattern) -> bool:
        """Add a single chain pattern. Returns True if new."""
        if pattern.key() in {(a, b) for a, b in self._by_pair}:
            return False
        self._upsert(pattern)
        return True

    def count(self) -> int:
        """Count unique chain patterns in the index."""
        row = self.conn.execute("SELECT COUNT(*) as c FROM chain_patterns").fetchone()
        return row["c"] if row else 0

    def all_patterns(self) -> list[ChainPattern]:
        """Return all indexed chain patterns."""
        rows = self.conn.execute("SELECT * FROM chain_patterns").fetchall()
        return [ChainPattern.from_row(r) for r in rows]

    def stats(self) -> dict:
        rows = self.conn.execute(
            "SELECT source_platform, COUNT(*) as cnt FROM chain_patterns GROUP BY source_platform"
        ).fetchall()
        return {
            "total": self.count(),
            "by_source": {r["source_platform"]: r["cnt"] for r in rows},
        }
