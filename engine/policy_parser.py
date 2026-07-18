"""Phase D1: Program Policy Parser — structured exclusion rules.

Parses HackerOne/Bugcrowd program policy pages into structured rules.
Policies use structured fields (boolean/string scope) instead of plain text.

Schema:
    ProgramPolicy:
        name: str
        platform: str              # "hackerone" | "bugcrowd"
        url: str
        exclusions: list[str]      # Generic exclusion categories
        out_of_scope: list[str]    # OOS text snippets
        score_range: str           # "$500-$5000"
        requires_poc: bool
        requires_browser_poc: bool
        allow_self_xss: bool       # True = self-XSS accepted
        allow_clickjacking: bool   # True = clickjacking accepted
        requires_account: bool     # True = need test account
        minimum_severity: str      # "none", "low", "medium", "high", "critical"
        accepts_duplicates: bool   # True = duplicate reports accepted
        csrf_scope: str            # "any", "authenticated", "out_of_scope"
        oauth_scope: str           # "in_scope", "informative", "out_of_scope"
        api_scope: str             # "in_scope", "restricted", "out_of_scope"
        mobile_scope: str          # "in_scope", "out_of_scope"
        notes: str

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


_VALID_SEVERITIES = frozenset({"none", "low", "medium", "high", "critical"})
_VALID_SCOPES = frozenset({"in_scope", "out_of_scope", "informative", "restricted", "authenticated", "any"})


@dataclass
class ProgramPolicy:
    """Structured program policy / scope rules."""

    name: str
    platform: str = "hackerone"
    url: str = ""
    exclusions: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    score_range: str = ""
    requires_poc: bool = True
    requires_browser_poc: bool = False
    allow_self_xss: bool = False
    allow_clickjacking: bool = False
    requires_account: bool = False
    minimum_severity: str = "none"
    accepts_duplicates: bool = False
    csrf_scope: str = "any"
    oauth_scope: str = "in_scope"
    api_scope: str = "in_scope"
    mobile_scope: str = "out_of_scope"
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
        # Validate enum-like fields
        if self.minimum_severity not in _VALID_SEVERITIES:
            self.minimum_severity = "none"
        for scope_field in ("csrf_scope", "oauth_scope", "api_scope", "mobile_scope"):
            val = getattr(self, scope_field)
            if val not in _VALID_SCOPES:
                object.__setattr__(self, scope_field, "out_of_scope")

    def to_row(self) -> dict:
        return {
            "name": self.name,
            "platform": self.platform,
            "url": self.url,
            "exclusions": _serialize_list(self.exclusions),
            "out_of_scope": _serialize_list(self.out_of_scope),
            "score_range": self.score_range,
            "requires_poc": int(self.requires_poc),
            "requires_browser_poc": int(self.requires_browser_poc),
            "allow_self_xss": int(self.allow_self_xss),
            "allow_clickjacking": int(self.allow_clickjacking),
            "requires_account": int(self.requires_account),
            "minimum_severity": self.minimum_severity,
            "accepts_duplicates": int(self.accepts_duplicates),
            "csrf_scope": self.csrf_scope,
            "oauth_scope": self.oauth_scope,
            "api_scope": self.api_scope,
            "mobile_scope": self.mobile_scope,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_row(cls, row) -> "ProgramPolicy":
        """Create from sqlite3.Row or dict."""
        def _get(key, default=""):
            try:
                return row[key]
            except (KeyError, IndexError, TypeError):
                return default
        return cls(
            name=row["name"],
            platform=_get("platform", "hackerone"),
            url=_get("url", ""),
            exclusions=_deserialize_list(_get("exclusions", "")),
            out_of_scope=_deserialize_list(_get("out_of_scope", "")),
            score_range=_get("score_range", ""),
            requires_poc=bool(_get("requires_poc", 1)),
            requires_browser_poc=bool(_get("requires_browser_poc", 0)),
            allow_self_xss=bool(_get("allow_self_xss", 0)),
            allow_clickjacking=bool(_get("allow_clickjacking", 0)),
            requires_account=bool(_get("requires_account", 0)),
            minimum_severity=_get("minimum_severity", "none"),
            accepts_duplicates=bool(_get("accepts_duplicates", 0)),
            csrf_scope=_get("csrf_scope", "any"),
            oauth_scope=_get("oauth_scope", "in_scope"),
            api_scope=_get("api_scope", "in_scope"),
            mobile_scope=_get("mobile_scope", "out_of_scope"),
            notes=_get("notes", ""),
            created_at=_get("created_at", ""),
            updated_at=_get("updated_at", ""),
        )

    def matches_finding(self, sink_id: str, severity: str = "") -> tuple[bool, str]:
        """Check if a finding should be excluded under this policy.

        Returns (excluded, reason).
        """
        # Severity gate
        if severity and self.minimum_severity != "none":
            sev_order = ["none", "low", "medium", "high", "critical"]
            if sev_order.index(severity) < sev_order.index(self.minimum_severity):
                return True, f"Below minimum severity ({self.minimum_severity})"

        # Check structured allow_* flags
        finding_normalized = sink_id.lower().replace("-", "_")
        if not self.allow_self_xss and "self_xss" in finding_normalized:
            return True, "Self-XSS not accepted"
        if not self.allow_clickjacking and "clickjack" in finding_normalized:
            return True, "Clickjacking not accepted"

        # Scope checks
        if (self.csrf_scope == "out_of_scope"
                and ("csrf" in finding_normalized or "cors" in finding_normalized)):
            return True, "CSRF out of scope per policy"

        # Check exclusion list (generic catch-all)
        for exc in self.exclusions:
            exc_lower = exc.lower().replace("_", "-").replace(" ", "-")
            if exc_lower in finding_normalized.replace("_", "-") or finding_normalized.replace("_", "-") in exc_lower:
                return True, f"Excluded by program policy: '{exc}'"

        # OOS text snippets (word-level matching)
        finding_words = set(finding_normalized.replace("-", " ").replace("_", " ").split())
        for oos in self.out_of_scope:
            oos_words = set(oos.lower().replace("-", " ").replace("_", " ").split())
            if finding_words and len(finding_words & oos_words) >= 2:
                return True, f"Out of scope: '{oos[:80]}'"

        return False, ""

    def to_summary(self) -> str:
        """One-line summary for display."""
        parts = [f"Policy: {self.name} ({self.platform})"]
        if self.exclusions:
            parts.append(f"excludes {len(self.exclusions)} categories")
        if self.minimum_severity != "none":
            parts.append(f"min severity: {self.minimum_severity}")
        scope_flags = []
        if self.allow_self_xss:
            scope_flags.append("self-xss OK")
        if self.allow_clickjacking:
            scope_flags.append("clickjacking OK")
        if self.requires_account:
            scope_flags.append("needs account")
        if scope_flags:
            parts.append(", ".join(scope_flags))
        if self.score_range:
            parts.append(f"bounty: {self.score_range}")
        return " | ".join(parts)


# ── Serialization helpers ───────────────────────────────────────────────


def _serialize_list(items: list[str]) -> str:
    return "\n".join(items) if items else ""


def _deserialize_list(text: str) -> list[str]:
    return [s.strip() for s in text.split("\n") if s.strip()] if text else []


# ── Exclusion categories (common across programs) ───────────────────────

_EXCLUSION_CATEGORIES = frozenset({
    "self-xss", "self_xss",
    "rate-limiting", "rate_limiting",
    "missing-csp-headers", "missing_csp_headers",
    "missing-security-headers", "missing_security_headers",
    "csrf-logout", "csrf_logout",
    "clickjacking", "click_jacking",
    "cors-misconfig-without-xss", "cors_misconfig_without_xss",
    "host-header-injection-without-chain", "host_header_injection_without_chain",
    "open-redirect-without-chain", "open_redirect_without_chain",
    "version-disclosure", "version_disclosure",
    "server-side-information-disclosure", "server_side_information_disclosure",
    "debug-endpoint", "debug_endpoint",
    "username-enumeration", "username_enumeration",
    "password-policy", "password_policy",
    "content-spoofing", "content_spoofing",
    "cache-poisoning-without-chain", "cache_poisoning_without_chain",
    "null-origin-cors", "null_origin_cors",
    "subdomain-takeover-without-service", "subdomain_takeover_without_service",
    "session-timeout", "session_timeout",
    "directory-listing", "directory_listing",
    "dangling-dns-record", "dangling_dns_record",
    "http-verbose", "http_verbose",
    "next-data-leak", "next_data_leak",
    "firebase-api-key-leak", "firebase_api_key_leak",
    "datadog-rum-token", "datadog_rum_token",
    "account-lockout", "account_lockout",
    "denial-of-service", "denial_of_service",
    "two-factor-authentication-bypass-without-demo", "two_factor_authentication_bypass_without_demo",
    "internal-ip-disclosure", "internal_ip_disclosure",
    "stack-trace", "stack_trace",
    "email-harvesting", "email_harvesting",
    "captcha-bypass", "captcha_bypass",
})

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
    normalized = name.lower().replace("-", "_").strip()
    return _EXCLUSION_TO_SINK.get(normalized, normalized)


# ── Seeded policies ─────────────────────────────────────────────────────

_SEEDED_POLICIES = [
    ProgramPolicy(
        name="security", platform="hackerone",
        url="https://hackerone.com/security",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration"],
        score_range="$500-$5000", csrf_scope="authenticated",
    ),
    ProgramPolicy(
        name="twitter", platform="hackerone",
        url="https://hackerone.com/twitter",
        exclusions=["self-xss", "rate-limiting", "missing-security-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration", "password-policy",
                     "content-spoofing", "open-redirect-without-chain"],
        score_range="$560-$1120", minimum_severity="low",
    ),
    ProgramPolicy(
        name="paypal", platform="hackerone",
        url="https://hackerone.com/paypal",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain", "null-origin-cors",
                     "cache-poisoning-without-chain"],
        score_range="$50-$10000", requires_browser_poc=True,
    ),
    ProgramPolicy(
        name="shopify", platform="hackerone",
        url="https://hackerone.com/shopify",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain", "subdomain-takeover-without-service"],
        score_range="$500-$10000", minimum_severity="medium",
    ),
    ProgramPolicy(
        name="cloudflare", platform="hackerone",
        url="https://hackerone.com/cloudflare",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain", "dangling-dns-record"],
        score_range="$200-$3000",
    ),
    ProgramPolicy(
        name="discord", platform="hackerone",
        url="https://hackerone.com/discord",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain"],
        score_range="$500-$5000", requires_account=True,
    ),
    ProgramPolicy(
        name="gitlab", platform="hackerone",
        url="https://hackerone.com/gitlab",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain", "host-header-injection-without-chain"],
        score_range="$500-$10000", csrf_scope="authenticated",
    ),
    ProgramPolicy(
        name="slack", platform="hackerone",
        url="https://hackerone.com/slack",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain"],
        score_range="$500-$5000",
    ),
    ProgramPolicy(
        name="uber", platform="hackerone",
        url="https://hackerone.com/uber",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain"],
        score_range="$500-$5000",
    ),
    ProgramPolicy(
        name="facebook", platform="bugcrowd",
        url="https://bugcrowd.com/facebook",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain",
                     "account-lockout", "denial-of-service"],
        score_range="$500-$40000", accepts_duplicates=False,
        oauth_scope="out_of_scope",
    ),
    ProgramPolicy(
        name="bugcrowd", platform="bugcrowd",
        url="https://bugcrowd.com/bugcrowd",
        exclusions=["self-xss", "rate-limiting", "missing-security-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain"],
        score_range="$250-$2500",
    ),
    ProgramPolicy(
        name="general-hackerone", platform="hackerone",
        url="https://hackerone.com/",
        exclusions=["self-xss", "rate-limiting", "missing-csp-headers",
                     "csrf-logout", "clickjacking", "version-disclosure",
                     "debug-endpoint", "username-enumeration",
                     "open-redirect-without-chain"],
        score_range="Varies",
    ),
]


# ── Policy Store ─────────────────────────────────────────────────────────


class PolicyStore:
    """SQLite-backed store for program policies."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS program_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        platform TEXT NOT NULL DEFAULT 'hackerone',
        url TEXT DEFAULT '',
        exclusions TEXT DEFAULT '',
        out_of_scope TEXT DEFAULT '',
        score_range TEXT DEFAULT '',
        requires_poc INTEGER DEFAULT 1,
        requires_browser_poc INTEGER DEFAULT 0,
        allow_self_xss INTEGER DEFAULT 0,
        allow_clickjacking INTEGER DEFAULT 0,
        requires_account INTEGER DEFAULT 0,
        minimum_severity TEXT DEFAULT 'none',
        accepts_duplicates INTEGER DEFAULT 0,
        csrf_scope TEXT DEFAULT 'any',
        oauth_scope TEXT DEFAULT 'in_scope',
        api_scope TEXT DEFAULT 'in_scope',
        mobile_scope TEXT DEFAULT 'out_of_scope',
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
        self._load_persisted()

    def _load_persisted(self):
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
            cols = ", ".join(row.keys())
            placeholders = ", ".join(f":{k}" for k in row)
            self.conn.execute(
                f"INSERT OR REPLACE INTO program_policies ({cols}) VALUES ({placeholders})",
                row,
            )
            self.conn.commit()
        except Exception as e:
            logger.debug(f"PolicyStore upsert failed: {e}")

    # ── Public API ───────────────────────────────────────────────────

    def lookup(self, name: str) -> Optional[ProgramPolicy]:
        key = name.lower().strip()
        if key in self._by_name:
            return self._by_name[key]
        for stored_name, policy in self._by_name.items():
            if key in stored_name or stored_name in key:
                return policy
        return None

    def lookup_by_sink(self, sink_id: str) -> list[tuple[str, list[str]]]:
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
        existing = self._by_name.get(policy.name.lower())
        is_new = existing is None
        if not is_new:
            policy.created_at = existing.created_at
        policy.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self._upsert(policy)
        return is_new

    def remove(self, name: str) -> bool:
        key = name.lower().strip()
        if key in self._by_name:
            del self._by_name[key]
            self.conn.execute("DELETE FROM program_policies WHERE name = ?", (name,))
            self.conn.commit()
            return True
        return False

    def all_policies(self) -> list[ProgramPolicy]:
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
        if not text.strip():
            return None

        exclusions = []
        out_of_scope = []
        score_range = ""
        text_lower = text.lower()

        score_match = re.search(
            r'(?:\$|USD)\s*(\d[\d,]*)\s*(?:-|–|to)\s*(?:\$|USD)?\s*(\d[\d,]*)',
            text, re.IGNORECASE
        )
        if score_match:
            score_range = f"${score_match.group(1)}-${score_match.group(2)}"

        for category in _EXCLUSION_CATEGORIES:
            normalized = category.replace("_", "-").replace("-", " ")
            if normalized in text_lower or category.replace("_", " ") in text_lower:
                exclusions.append(category)
            elif category.replace("_", "-") in text_lower:
                exclusions.append(category)

        oos_patterns = re.finditer(
            r'(?:out.?of.?scope|not.?eligible|excluded|will.?not.?accept)[^.]*\.',
            text, re.IGNORECASE
        )
        for m in oos_patterns:
            sentence = m.group(0).strip()
            if sentence and sentence not in out_of_scope:
                out_of_scope.append(sentence)

        requires_browser = bool(re.search(
            r'browser.?based|browser.?poc|fetch\(\)|curl.?is.?not.?sufficient',
            text_lower
        ))

        requires_account = bool(re.search(
            r'requires? (a |an )?account|need (a |an )?account|test account|demo account',
            text_lower
        ))

        # Detect minimum severity
        min_sev = "none"
        for sev_text, sev_val in [("critical", "critical"), ("high", "high"),
                                   ("medium", "medium"), ("low", "low")]:
            if re.search(rf"minimum severity[:\s]*{sev_text}", text_lower):
                min_sev = sev_val
                break

        return ProgramPolicy(
            name=name or "unknown",
            platform=platform,
            url=url,
            exclusions=exclusions,
            score_range=score_range,
            requires_poc=True,
            requires_browser_poc=requires_browser,
            requires_account=requires_account,
            minimum_severity=min_sev,
            out_of_scope=out_of_scope,
        )
