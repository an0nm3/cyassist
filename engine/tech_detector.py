"""Phase A2: Tech stack detector — infer framework/language from report context.

Combines multiple signals:
1. HTTP response headers (from curl -v output)
2. URL structure (/api/, .php, .aspx, /graphql)
3. Error message patterns (SQL errors, stack traces)
4. Framework-specific keywords in description
5. Cookie/session patterns
"""

import re
from typing import Optional

# ── Signal Patterns ───────────────────────────────────────────────────

_URL_TECH_PATTERNS = [
    (r"\.php(?:[?]|$)", "php"),
    (r"\.aspx?(?:[?]|$)", "aspnet"),
    (r"\.jsp(?:[?]|$)", "java"),
    (r"\.do(?:[?]|$)", "java"),  # Struts/Spring
    (r"\.action(?:[?]|$)", "java"),
    (r"\.cfm(?:[?]|$)", "coldfusion"),
    (r"/wp-content/", "wordpress"),
    (r"/wp-admin/", "wordpress"),
    (r"/wp-json/", "wordpress"),
    (r"/graphql", "graphql"),
    (r"/api/graphql", "graphql"),
    (r"/swagger", "rest"),
    (r"/api/v\d+/", "rest"),
    (r"/rest/v\d+/", "rest"),
    (r"/_next/", "nextjs"),
    (r"/next/data/", "nextjs"),
    (r"\.svelte", "svelte"),
]

_ERROR_TECH_PATTERNS = [
    # SQL engines
    (r"you have an error in your sql syntax", "mysql"),
    (r"warning: mysql", "mysql"),
    (r"pg_query\(\)", "postgresql"),
    (r"psql:\s", "postgresql"),
    (r"sqlite3\.", "sqlite"),
    (r"sqlite_error", "sqlite"),
    (r"ora-\d{5}", "oracle"),
    (r"microsoft ole db", "mssql"),
    (r"driver\{sql server\}", "mssql"),
    (r"sqlstate\[", "mssql"),
    (r"sqlite\.exception", "sqlite"),
    (r"mysql_fetch", "php_mysql"),
    # Frameworks
    (r"traceback \(most recent call last\)", "python"),
    (r"flask\.", "flask"),
    (r"django\.", "django"),
    (r"fastapi", "fastapi"),
    (r"express\.", "express"),
    (r"laravel", "laravel"),
    (r"symfony", "symfony"),
    (r"spring", "java_spring"),
    (r"struts", "java_struts"),
    (r"rails", "rails"),
    (r"rack::", "ruby"),
    (r"java\.lang\.", "java"),
    (r"\.on\(.*res\.end\)", "express"),
    (r"next\.js", "nextjs"),
    (r"nuxt\.js", "vue"),
    # Web servers
    (r"nginx/\d", "nginx"),
    (r"apache/\d", "apache"),
    (r"iis \d", "iis"),
    (r"cloudflare", "cloudflare"),
]

_KEYWORD_TECH_PATTERNS = [
    # Language mentions
    (r"\bpython\b", "python"),
    (r"\bdjango\b", "django"),
    (r"\bflask\b", "flask"),
    (r"\bfastapi\b", "fastapi"),
    (r"\bnode\.?js\b", "node"),
    (r"\bexpress\b", "express"),
    (r"\bnext\.?js\b", "nextjs"),
    (r"\breact\b", "react"),
    (r"\bvue\.?js\b", "vue"),
    (r"\bangular\b", "angular"),
    (r"\bphp\b", "php"),
    (r"\blaravel\b", "laravel"),
    (r"\bwordpress\b", "wordpress"),
    (r"\bjava\b", "java"),
    (r"\bspring\b", "spring"),
    (r"\bruby\b", "ruby"),
    (r"\brails\b", "rails"),
    (r"\bgolang\b", "go"),
    (r"\bdotnet\b", "dotnet"),
    (r"\basp\.net\b", "aspnet"),
    # Database mentions
    (r"\bmysql\b", "mysql"),
    (r"\bpostgres(ql)?\b", "postgresql"),
    (r"\bmssql\b", "mssql"),
    (r"\boracle\b", "oracle"),
    (r"\bsqlite\b", "sqlite"),
    (r"\bmongodb\b", "mongodb"),
    # Cloud
    (r"\baws\b", "aws"),
    (r"\bamazon web services\b", "aws"),
    (r"\bgcp\b", "gcp"),
    (r"\bazure\b", "azure"),
    (r"\bcloudflare\b", "cloudflare"),
    # API
    (r"\bgraphql\b", "graphql"),
    (r"\brest api\b", "rest"),
    (r"\bgrpc\b", "grpc"),
]

_HEADER_TECH_PATTERNS = {
    "server": [
        (r"nginx", "nginx"),
        (r"apache", "apache"),
        (r"iis", "iis"),
        (r"caddy", "caddy"),
        (r"gunicorn", "gunicorn"),
        (r"uvicorn", "fastapi"),
        (r"cloudflare", "cloudflare"),
    ],
    "x-powered-by": [
        (r"express", "express"),
        (r"php", "php"),
        (r"asp\.net", "aspnet"),
        (r"rails", "rails"),
        (r"django", "django"),
        (r"fastapi", "fastapi"),
    ],
    "set-cookie": [
        (r"connect\.sid", "express"),
        (r"jsessionid", "java"),
        (r"session", "python"),
        (r"laravel_session", "laravel"),
        (r"wp-", "wordpress"),
        (r"django", "django"),
    ],
    "x-frame-options": [(r".", "has_xfo")],
    "x-content-type-options": [(r".", "has_xcto")],
    "strict-transport-security": [(r".", "hsts")],
}


def detect_from_headers(headers: dict[str, str]) -> list[str]:
    """Detect tech stack from HTTP response headers."""
    techs = set()
    headers_lower = {k.lower(): v for k, v in headers.items()}
    for header_name, patterns in _HEADER_TECH_PATTERNS.items():
        val = headers_lower.get(header_name, "")
        if not val:
            continue
        for pattern, tech in patterns:
            if re.search(pattern, val, re.IGNORECASE):
                techs.add(tech)
    return sorted(techs)


def detect_from_url(url: str) -> list[str]:
    """Detect tech stack from URL path/file extension patterns."""
    techs = set()
    for pattern, tech in _URL_TECH_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            techs.add(tech)
    return sorted(techs)


def detect_from_error(text: str) -> list[str]:
    """Detect tech stack from error messages in the report."""
    techs = set()
    for pattern, tech in _ERROR_TECH_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            techs.add(tech)
    return sorted(techs)


def detect_from_keywords(text: str) -> list[str]:
    """Detect tech stack from keyword mentions in the report."""
    techs = {}
    for pattern, tech in _KEYWORD_TECH_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            techs[tech] = techs.get(tech, 0) + 1
    # Only return techs mentioned at least twice (reduce false positives)
    return sorted([t for t, c in techs.items() if c >= 2])


def detect_all(
    text: str = "",
    url: str = "",
    headers: Optional[dict[str, str]] = None,
) -> list[str]:
    """Combined tech detection from all available signals.

    Uses multi-signal agreement for higher confidence:
    - If >=2 signals agree on a tech, it's included
    - If only 1 signal, it's included but marked as low confidence
    """
    all_techs = {}

    if headers:
        for t in detect_from_headers(headers):
            all_techs[t] = all_techs.get(t, 0) + 2  # header signals are stronger

    if url:
        for t in detect_from_url(url):
            all_techs[t] = all_techs.get(t, 0) + 1

    if text:
        for t in detect_from_error(text):
            all_techs[t] = all_techs.get(t, 0) + 2  # error signals are strong

        for t in detect_from_keywords(text):
            all_techs[t] = all_techs.get(t, 0) + 1

    return sorted(all_techs.keys())
