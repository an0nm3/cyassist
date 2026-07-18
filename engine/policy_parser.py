"""Phase D1: Program Policy Parser — structured exclusion rules.

Parses HackerOne/Bugcrowd program policy pages into structured rules.
For the initial release, uses a seeded set of known public program policies
and manual extraction. Future: HTML scraper for live policy pages.

Schema:
    ProgramPolicy:
        name: str           # Program name
        platform: str       # "hackerone" | "bugcrowd"
        url: str            # Program page URL
        exclusions: list     # Always-rejected categories (e.g. "self-xss")
        score_range: str    # Bounty range string
        requires_poc: bool  # Must include proof of concept
        requires_browser_poc: bool  # Requires browser-based PoC (CORS, etc.)
        out_of_scope: list  # OOS statements from the policy
        notes: str          # Additional context

Storage: SQLite table `program_policies`, indexed by name.
"""

import logging
import re
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("policy_parser")


# ── Data Model ──────────────────────────────────────────────────────────


@dataclass
class ProgramPolicy:
    """Structured program policy / scope rules."""

    name: str
    platform: str = "hackerone"
    url: str = ""
    exclusions: list[str] = field(default_factory=list)
    score_range: str = ""
    requires_poc: bool = True
    requires_browser_poc: bool = False
    out_of_scope: list[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

    def to_row(self) -> dict:
        return {
            "name": self.name,
            "platform": self.platform,
            "url": self.url,
            "exclusions": _serialize_list(self.exclusions),
            "score_range": self.score_range,
            "requires_poc": int(self.requires_poc),
            "requires_browser_poc": int(self.requires_browser_poc),
            "out_of_scope": _serialize_list(self.out_of_scope),
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_row(cls, row) -> "ProgramPolicy":
        """Create from sqlite3.Row or dict."""
        if isinstance(row, dict):
            return cls(
                name=row["name"], platform=row.get("platform", "hackerone"),
                url=row.get("url", ""),
                exclusions=_deserialize_list(row.get("exclusions", "")),
                score_range=row.get("score_range", ""),
                requires_poc=bool(row.get("requires_poc", 1)),
                requires_browser_poc=bool(row.get("requires_browser_poc", 0)),
                out_of_scope=_deserialize_list(row.get("out_of_scope", "")),
                notes=row.get("notes", ""),
                created_at=row.get("created_at", ""),
                updated_at=row.get("updated_at", ""),
            )
        return cls(
            name=row["name"], platform=row["platform"],
            url=row["url"],
            exclusions=_deserialize_list(row["exclusions"]),
            score_range=row["score_range"],
            requires_poc=bool(row["requires_poc"]),
            requires_browser_poc=bool(row["requires_browser_poc"]),
            out_of_scope=_deserialize_list(row["out_of_scope"]),
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def matches_finding(self, finding_class: str) -> tuple[bool, str]:
        """Check if a finding class is excluded by this policy.

        Returns (excluded, reason).
        """
        finding_lower = finding_class.lower().replace("_", "-")
        for exc in self.exclusions:
            exc_lower = exc.lower().replace("_", "-")
            if exc_lower in finding_lower or finding_lower in exc_lower:
                return True, f"Excluded by program policy: '{exc}'"
        # Normalize OOS text: replace underscores, hyphens, and spaces with a common separator
        finding_normalized = finding_lower.replace("-", " ").replace("_", " ")
        for oos in self.out_of_scope:
            oos_normalized = oos.lower().replace("-", " ").replace("_", " ")
            # Check if finding words appear in OOS statement
            finding_words = set(finding_normalized.split())
            if finding_words and finding_words.intersection(oos_normalized.split()):
                return True, f"Out of scope: '{oos}'"
        return False, ""


# ── Serialization helpers ───────────────────────────────────────────────


def _serialize_list(items: list[str]) -> str:
    return "\n".join(items) if items else ""


def _deserialize_list(text: str) -> list[str]:
    return [s.strip() for s in text.split("\n") if s.strip()] if text else []


# ── Exclusion categories (common across programs) ───────────────────────

# These are well-known exclusion categories seen across H1/Bugcrowd programs.
# Source: never-report skill + public program policies.
_EXCLUSION_CATEGORIES = frozenset({
    "self-xss",
    "self_xss",
    "rate-limiting",
    "rate_limiting",
    "missing-csp-headers",
    "missing_csp_headers",
    "missing-security-headers",
    "missing_security_headers",
    "csrf-logout",
    "csrf_logout",
    "clickjacking",
    "click_jacking",
    "cors-misconfig-without-xss",
    "cors_misconfig_without_xss",
    "host-header-injection-without-chain",
    "host_header_injection_without_chain",
    "open-redirect-without-chain",
    "open_redirect_without_chain",
    "version-disclosure",
    "version_disclosure",
    "server-side-information-disclosure",
    "server_side_information_disclosure",
    "debug-endpoint",
    "debug_endpoint",
    "username-enumeration",
    "username_enumeration",
    "password-policy",
    "password_policy",
    "content-spoofing",
    "content_spoofing",
    "cache-poisoning-without-chain",
    "cache_poisoning_without_chain",
    "null-origin-cors",
    "null_origin_cors",
    "subdomain-takeover-without-service",
    "subdomain_takeover_without_service",
    "session-timeout",
    "session_timeout",
    "directory-listing",
    "directory_listing",
    "dangling-dns-record",
    "dangling_dns_record",
    "http-verbose",
    "http_verbose",
    "next-data-leak",
    "next_data_leak",
    "firebase-api-key-leak",
    "firebase_api_key_leak",
    "datadog-rum-token",
    "datadog_rum_token",
    "account-lockout",
    "account_lockout",
    "denial-of-service",
    "denial_of_service",
    "two-factor-authentication-bypass-without-demo",
    "two_factor_authentication_bypass_without_demo",
    "internal-ip-disclosure",
    "internal_ip_disclosure",
    "stack-trace",
    "stack_trace",
    "email-harvesting",
    "email_harvesting",
    "captcha-bypass",
    "captcha_bypass",
})

# Well-known exclusion patterns mapped to detector sink IDs
_EXCLUSION_TO_SINK: dict[str, str] = {
    "self_xss": "xss_reflected",
    "rate_limiting": "rate_limit",
    "missing_csp_headers": "cors_misconfig",
    "click_jacking": "cors_misconfig",
    "csrf_logout": "cors_misconfig",
    "open_redirect_without_chain": "open_redirect",
    "version_disclosure": "debug_endpoints",
    "server_side_information_disclosure": "path_discovery",
    "debug_endpoint": "debug_endpoints",
    "username_enumeration": "path_discovery",
    "cache_poisoning_without_chain": "host_header_injection",
    "null_origin_cors": "cors_misconfig",
    "subdomain_takeover_without_service": "host_header_injection",
    "directory_listing": "path_discovery",
    "dangling_dns_record": "host_header_injection",
    "next_data_leak": "path_discovery",
    "firebase_api_key_leak": "path_discovery",
    "datadog_rum_token": "path_discovery",
    "host_header_injection_without_chain": "host_header_injection",
    "cors_misconfig_without_xss": "cors_misconfig",
    "stack_trace": "debug_endpoints",
    "internal_ip_disclosure": "debug_endpoints",
    "denial_of_service": "rate_limit",
    "account_lockout": "rate_limit",
    "captcha_bypass": "rate_limit",
}


def exclusion_to_sink(name: str) -> str:
    """Map exclusion name to its corresponding sink ID (with normalisation)."""
    normalized = name.lower().replace("-", "_").strip()
    return _EXCLUSION_TO_SINK.get(normalized, normalized)


# ── Seeded policies ─────────────────────────────────────────────────────

# Known public program policies (sampled). These represent common exclusion patterns.
_SEEDED_POLICIES = [
    ProgramPolicy(
        name="security",
        platform="hackerone",
        url="https://hackerone.com/security",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
        ],
        score_range="$500-$5000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="twitter",
        platform="hackerone",
        url="https://hackerone.com/twitter",
        exclusions=[
            "self-xss", "rate-limiting", "missing-security-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration", "password-policy",
            "content-spoofing", "open-redirect-without-chain",
        ],
        score_range="$560-$1120",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="paypal",
        platform="hackerone",
        url="https://hackerone.com/paypal",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain", "null-origin-cors",
            "cache-poisoning-without-chain",
        ],
        score_range="$50-$10000",
        requires_poc=True,
        requires_browser_poc=True,
    ),
    ProgramPolicy(
        name="shopify",
        platform="hackerone",
        url="https://hackerone.com/shopify",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain", "subdomain-takeover-without-service",
        ],
        score_range="$500-$10000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="cloudflare",
        platform="hackerone",
        url="https://hackerone.com/cloudflare",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain", "dangling-dns-record",
        ],
        score_range="$200-$3000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="discord",
        platform="hackerone",
        url="https://hackerone.com/discord",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain",
        ],
        score_range="$500-$5000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="gitlab",
        platform="hackerone",
        url="https://hackerone.com/gitlab",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain", "host-header-injection-without-chain",
        ],
        score_range="$500-$10000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="slack",
        platform="hackerone",
        url="https://hackerone.com/slack",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain",
        ],
        score_range="$500-$5000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="uber",
        platform="hackerone",
        url="https://hackerone.com/uber",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain",
        ],
        score_range="$500-$5000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="facebook",
        platform="bugcrowd",
        url="https://bugcrowd.com/facebook",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain",
            "account-lockout", "denial-of-service",
        ],
        score_range="$500-$40000",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="bugcrowd",
        platform="bugcrowd",
        url="https://bugcrowd.com/bugcrowd",
        exclusions=[
            "self-xss", "rate-limiting", "missing-security-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain",
        ],
        score_range="$250-$2500",
        requires_poc=True,
    ),
    ProgramPolicy(
        name="general-hackerone",
        platform="hackerone",
        url="https://hackerone.com/",
        exclusions=[
            "self-xss", "rate-limiting", "missing-csp-headers",
            "csrf-logout", "clickjacking", "version-disclosure",
            "debug-endpoint", "username-enumeration",
            "open-redirect-without-chain",
        ],
        score_range="Varies",
        requires_poc=True,
    ),
]


# ── Policy Store ─────────────────────────────────────────────────────────


class PolicyStore:
    """SQLite-backed store for program policies.

    Seeded with common program policies. Extendable via add() / parse_policy_text().
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS program_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        platform TEXT NOT NULL DEFAULT 'hackerone',
        url TEXT DEFAULT '',
        exclusions TEXT DEFAULT '',
        score_range TEXT DEFAULT '',
        requires_poc INTEGER DEFAULT 1,
        requires_browser_poc INTEGER DEFAULT 0,
        out_of_scope TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created_at TEXT DEFAULT '',
        updated_at TEXT DEFAULT ''
    );
    CREATE INDEX IF NOT EXISTS idx_policy_name ON program_policies(name);
    CREATE INDEX IF NOT EXISTS idx_policy_platform ON program_policies(platform);
    """

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "vectors.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        # In-memory lookup: name.lower() -> ProgramPolicy
        self._by_name: dict[str, ProgramPolicy] = {}
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
        for p in _SEEDED_POLICIES:
            self._upsert(p)
        # Load persisted non-seed entries from DB
        self._load_persisted()

    def _load_persisted(self):
        """Load non-seed policies from SQLite into _by_name."""
        seed_names = {p.name.lower() for p in _SEEDED_POLICIES}
        rows = self.conn.execute("SELECT * FROM program_policies").fetchall()
        for row in rows:
            if row["name"].lower() not in seed_names:
                p = ProgramPolicy.from_row(row)
                self._by_name[p.name.lower()] = p

    def _upsert(self, policy: ProgramPolicy):
        self._by_name[policy.name.lower()] = policy
        try:
            row = policy.to_row()
            self.conn.execute(
                """INSERT OR REPLACE INTO program_policies
                (name, platform, url, exclusions, score_range,
                 requires_poc, requires_browser_poc, out_of_scope,
                 notes, created_at, updated_at)
                VALUES (:name, :platform, :url, :exclusions, :score_range,
                        :requires_poc, :requires_browser_poc, :out_of_scope,
                        :notes, :created_at, :updated_at)""",
                row,
            )
            self.conn.commit()
        except Exception as e:
            logger.debug(f"PolicyStore upsert failed: {e}")

    # ── Public API ───────────────────────────────────────────────────

    def lookup(self, name: str) -> Optional[ProgramPolicy]:
        """Look up a program by name (case-insensitive, partial match)."""
        key = name.lower().strip()
        if key in self._by_name:
            return self._by_name[key]
        for stored_name, policy in self._by_name.items():
            if key in stored_name or stored_name in key:
                return policy
        return None

    def lookup_by_sink(self, sink_id: str) -> list[tuple[str, list[str]]]:
        """Find programs that exclude a given sink.

        Returns list of (program_name, [exclusion_reasons]).
        """
        results = []
        sink_norm = sink_id.lower()
        for name, policy in self._by_name.items():
            matching = []
            for exc in policy.exclusions:
                exc_sink = exclusion_to_sink(exc)
                if exc_sink == sink_norm or exc_sink.replace("-", "_") == sink_norm:
                    matching.append(exc)
            if matching:
                results.append((policy.name, matching))
        return results

    def add(self, policy: ProgramPolicy) -> bool:
        """Add or update a policy. Returns True if new."""
        existing = self._by_name.get(policy.name.lower())
        is_new = existing is None
        if not is_new:
            policy.created_at = existing.created_at
        policy.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self._upsert(policy)
        return is_new

    def remove(self, name: str) -> bool:
        """Remove a policy by name."""
        key = name.lower().strip()
        if key in self._by_name:
            del self._by_name[key]
            self.conn.execute("DELETE FROM program_policies WHERE name = ?", (name,))
            self.conn.commit()
            return True
        return False

    def all_policies(self) -> list[ProgramPolicy]:
        """Return all indexed policies."""
        rows = self.conn.execute("SELECT * FROM program_policies").fetchall()
        return [ProgramPolicy.from_row(r) for r in rows]

    def count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) as c FROM program_policies").fetchone()
        return row["c"] if row else 0

    def stats(self) -> dict:
        rows = self.conn.execute(
            "SELECT platform, COUNT(*) as cnt FROM program_policies GROUP BY platform"
        ).fetchall()
        return {
            "total": self.count(),
            "by_platform": {r["platform"]: r["cnt"] for r in rows},
        }

    # ── Policy text parser ───────────────────────────────────────────

    def parse_policy_text(self, text: str, name: str = "", url: str = "",
                          platform: str = "hackerone") -> Optional[ProgramPolicy]:
        """Parse a program policy page text into structured rules.

        Uses regex patterns to extract common policy elements.
        Returns None if parsing fails to find meaningful structure.
        """
        if not text.strip():
            return None

        exclusions = []
        out_of_scope = []
        score_range = ""
        notes = []

        # Extract bounty range
        score_match = re.search(
            r'(?:\$|USD)\s*(\d[\d,]*)\s*(?:-|–|to)\s*(?:\$|USD)?\s*(\d[\d,]*)',
            text, re.IGNORECASE
        )
        if score_match:
            low, high = score_match.group(1), score_match.group(2)
            score_range = f"${low}-${high}"

        # Detect exclusion categories mentioned in the text
        text_lower = text.lower()
        for category in _EXCLUSION_CATEGORIES:
            normalized = category.replace("_", "-").replace("-", " ")
            if normalized in text_lower or category.replace("_", " ") in text_lower:
                exclusions.append(category)
            # Also match the underscore/hyphen variant
            alt = category.replace("-", "_")
            if alt != category and (category.replace("_", "-") in text_lower):
                if alt not in exclusions:
                    exclusions.append(alt)

        # Detect OOS patterns
        oos_patterns = re.finditer(
            r'(?:out.?of.?scope|not.?eligible|excluded|will.?not.?accept)[^.]*\.',
            text, re.IGNORECASE
        )
        for m in oos_patterns:
            sentence = m.group(0).strip()
            if sentence and sentence not in out_of_scope:
                out_of_scope.append(sentence)

        # Determine PoC requirements
        requires_browser = bool(re.search(
            r'browser.?based|browser.?poc|fetch\(\)|curl.?is.?not.?sufficient',
            text_lower
        ))

        name = name or "unknown"
        return ProgramPolicy(
            name=name,
            platform=platform,
            url=url,
            exclusions=exclusions,
            score_range=score_range,
            requires_poc=True,
            requires_browser_poc=requires_browser,
            out_of_scope=out_of_scope,
            notes="; ".join(notes) if notes else "",
        )
