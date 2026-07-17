"""Phase A4: Tech Stack Classifier — HTTP-level fingerprinting.

Takes raw response data (headers, body, status, URL) and produces
a ranked tech stack with per-tech confidence scores.

Designed for:
- Rudra probe response analysis (what tech is this target running?)
- Cyassist Pattern Query context enrichment
- Live fingerprinting, not report text mining

Multi-signal agreement:
- ≥2 signals → HIGH confidence
- 1 strong signal (header) → MEDIUM
- 1 weak signal (URL, body) → LOW

Usage:
    classifier = TechClassifier()
    result = classifier.classify(
        headers={"Server": "nginx/1.18", "X-Powered-By": "PHP/7.4"},
        url="https://example.com/wp-admin/login.php",
        body='<link rel="stylesheet" href="/wp-content/themes/..." />',
    )
    # result.techs = {"nginx": 0.9, "php": 0.85, "wordpress": 0.75}
"""

import re
from dataclasses import dataclass, field
from typing import Optional


# ── Signal Weights ───────────────────────────────────────────────────

# Each signal type has a base weight. Agreement = sum of weights for
# a given tech across all signals, capped at 1.0.

_WEIGHT_HEADER = 0.6
_WEIGHT_URL = 0.35
_WEIGHT_BODY = 0.4
_WEIGHT_ERROR = 0.45
_WEIGHT_COOKIE = 0.5

_CONFIDENCE_HIGH = 0.85
_CONFIDENCE_MEDIUM = 0.55
_CONFIDENCE_LOW = 0.25


# ── Patterns ─────────────────────────────────────────────────────────

@dataclass
class TechSignal:
    tech: str
    pattern: str
    signal_type: str  # "header", "url", "body", "error", "cookie"
    header_name: str = ""  # for header signals
    label: str = ""        # human-readable variant


class TechClassifier:
    """Classifies tech stack from HTTP response signals."""

    def __init__(self):
        self.signals = self._build_signals()

    # ── Public API ──────────────────────────────────────────────────

    def classify(
        self,
        headers: Optional[dict[str, str]] = None,
        url: str = "",
        body: str = "",
        status_code: int = 0,
    ) -> dict[str, float]:
        """Classify tech stack. Returns {tech: confidence} dict.

        Confidence is based on multi-signal agreement:
        - 2+ signals → HIGH (~0.85)
        - 1 strong (header/cookie/error) → MEDIUM (~0.55)
        - 1 weak (URL/body) → LOW (~0.25)
        """
        scores: dict[str, float] = {}

        # Collect all signals
        for signal in self.signals:
            if self._match_signal(signal, headers, url, body):
                weight = self._signal_weight(signal.signal_type)
                if signal.tech not in scores:
                    scores[signal.tech] = 0.0
                scores[signal.tech] += weight

        # Cap at 1.0 and adjust per-tech confidence tiers
        result = {}
        for tech, total_weight in scores.items():
            capped = min(total_weight, 1.0)
            if capped >= 0.8:
                # 2+ strong signals
                result[tech] = _CONFIDENCE_HIGH
            elif capped >= 0.4:
                # 1 strong or 2 weak
                result[tech] = _CONFIDENCE_MEDIUM
            else:
                result[tech] = _CONFIDENCE_LOW

        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def top_tech(self, **kwargs) -> str:
        """Return the single highest-confidence tech."""
        result = self.classify(**kwargs)
        return next(iter(result.keys()), "")

    # ── Signal Matching ─────────────────────────────────────────────

    def _match_signal(
        self,
        signal: TechSignal,
        headers: Optional[dict],
        url: str,
        body: str,
    ) -> bool:
        if signal.signal_type == "header":
            if not headers:
                return False
            headers_lower = {k.lower(): v for k, v in headers.items()}
            val = headers_lower.get(signal.header_name.lower(), "")
            if re.search(signal.pattern, str(val), re.IGNORECASE):
                return True
            # Also check if header name matches the pattern
            if signal.header_name and re.search(signal.pattern, signal.header_name, re.IGNORECASE):
                return bool(headers_lower.get(signal.header_name.lower()) is not None)
            return False

        elif signal.signal_type == "url":
            return bool(re.search(signal.pattern, url, re.IGNORECASE))

        elif signal.signal_type == "body":
            return bool(re.search(signal.pattern, body, re.IGNORECASE))

        elif signal.signal_type == "error":
            return bool(re.search(signal.pattern, body, re.IGNORECASE))

        elif signal.signal_type == "cookie":
            if not headers:
                return False
            headers_lower = {k.lower(): v for k, v in headers.items()}
            set_cookie = headers_lower.get("set-cookie", "")
            return bool(re.search(signal.pattern, str(set_cookie), re.IGNORECASE))

        return False

    @staticmethod
    def _signal_weight(signal_type: str) -> float:
        mapping = {
            "header": _WEIGHT_HEADER,
            "url": _WEIGHT_URL,
            "body": _WEIGHT_BODY,
            "error": _WEIGHT_ERROR,
            "cookie": _WEIGHT_COOKIE,
        }
        return mapping.get(signal_type, 0.3)

    # ── Signal Definitions ──────────────────────────────────────────

    def _build_signals(self) -> list[TechSignal]:
        return [
            # ── Web Servers ───────────────────────────────────────
            TechSignal("nginx", r"nginx", "header", header_name="server"),
            TechSignal("apache", r"apache", "header", header_name="server"),
            TechSignal("iis", r"iis", "header", header_name="server"),
            TechSignal("caddy", r"caddy", "header", header_name="server"),
            TechSignal("gunicorn", r"gunicorn", "header", header_name="server"),
            TechSignal("tomcat", r"tomcat", "header", header_name="server"),
            TechSignal("tomcat", r"apache-coyote", "header", header_name="server"),

            # ── CDN / Proxy ───────────────────────────────────────
            TechSignal("cloudflare", r"cloudflare", "header", header_name="server"),
            TechSignal("cloudflare", r"__cfduid", "cookie"),
            TechSignal("cloudflare", r"cf-ray", "header", header_name="cf-ray"),
            TechSignal("akamai", r"akamai", "header", header_name="server"),
            TechSignal("akamai", r"x-akamai", "header", header_name="x-akamai-request-id"),

            # ── Scripting Languages ───────────────────────────────
            TechSignal("php", r"php", "header", header_name="x-powered-by"),
            TechSignal("php", r"\.php(?:[?]|$)", "url"),
            TechSignal("php", r"wp-content", "url"),
            TechSignal("python", r"python", "header", header_name="x-powered-by"),
            TechSignal("python", r"session", "cookie"),
            TechSignal("flask", r"flask", "header", header_name="x-powered-by"),
            TechSignal("flask", r"flask", "body"),
            TechSignal("django", r"django", "header", header_name="x-powered-by"),
            TechSignal("django", r"csrftoken", "cookie"),
            TechSignal("django", r"django", "cookie"),
            TechSignal("fastapi", r"fastapi", "header", header_name="x-powered-by"),
            TechSignal("fastapi", r"uvicorn", "header", header_name="server"),
            TechSignal("ruby", r"ruby", "header", header_name="x-powered-by"),
            TechSignal("ruby", r"rails", "header", header_name="x-powered-by"),
            TechSignal("ruby", r"_rails", "cookie"),
            TechSignal("ruby", r"rack", "header", header_name="x-powered-by"),
            TechSignal("java", r"java", "header", header_name="x-powered-by"),
            TechSignal("java", r"jsessionid", "cookie"),
            TechSignal("java", r"\.jsp(?:[?]|$)", "url"),
            TechSignal("java", r"\.do(?:[?]|$)", "url"),
            TechSignal("java", r"servlet", "header", header_name="x-powered-by"),
            TechSignal("aspnet", r"asp\.net", "header", header_name="x-powered-by"),
            TechSignal("aspnet", r"\.aspx?(?:[?]|$)", "url"),
            TechSignal("aspnet", r"aspnet", "header", header_name="x-powered-by"),
            TechSignal("aspnet", r"__requestverificationtoken", "body"),
            TechSignal("aspnet", r"viewstate", "body"),

            # ── JS Frameworks ─────────────────────────────────────
            TechSignal("express", r"express", "header", header_name="x-powered-by"),
            TechSignal("express", r"connect\.sid", "cookie"),
            TechSignal("nextjs", r"_next/data", "url"),
            TechSignal("nextjs", r"__NEXT_DATA__", "body"),
            TechSignal("nextjs", r"__next", "body"),
            TechSignal("react", r"_reactroot", "body"),
            TechSignal("react", r"react\.", "body"),
            TechSignal("vue", r"vue\.", "body"),
            TechSignal("vue", r"__vue__", "body"),
            TechSignal("angular", r"angular\.", "body"),
            TechSignal("angular", r"ng-app", "body"),
            TechSignal("angular", r"ng-version", "body"),

            # ── CMS ───────────────────────────────────────────────
            TechSignal("wordpress", r"wp-content", "url"),
            TechSignal("wordpress", r"wp-admin", "url"),
            TechSignal("wordpress", r"wp-json", "url"),
            TechSignal("wordpress", r"/wp-", "body"),
            TechSignal("wordpress", r"wordpress", "header", header_name="x-powered-by"),
            TechSignal("laravel", r"laravel", "header", header_name="x-powered-by"),
            TechSignal("laravel", r"laravel_session", "cookie"),
            TechSignal("drupal", r"drupal", "header", header_name="x-powered-by"),
            TechSignal("drupal", r"sites/default", "url"),
            TechSignal("joomla", r"joomla", "header", header_name="x-powered-by"),
            TechSignal("joomla", r"/components/", "url"),
            TechSignal("joomla", r"/modules/", "url"),

            # ── Databases (from errors/bodies) ────────────────────
            TechSignal("mysql", r"mysql", "error"),
            TechSignal("mysql", r"you have an error in your sql", "error"),
            TechSignal("postgresql", r"postgresql", "error"),
            TechSignal("postgresql", r"pg_query", "error"),
            TechSignal("postgresql", r"psql:", "error"),
            TechSignal("mssql", r"sqlstate\[", "error"),
            TechSignal("mssql", r"driver\{sql server\}", "error"),
            TechSignal("oracle", r"ora-\d{5}", "error"),
            TechSignal("sqlite", r"sqlite", "error"),
            TechSignal("mongodb", r"mongodb", "error"),

            # ── APIs ──────────────────────────────────────────────
            TechSignal("graphql", r"/graphql", "url"),
            TechSignal("graphql", r"graphql", "body"),
            TechSignal("rest", r"/api/v\d+/", "url"),
            TechSignal("rest", r"/swagger", "url"),
            TechSignal("rest", r"/openapi", "url"),
            TechSignal("rest", r"swagger", "body"),

            # ── Cloud / Infra ─────────────────────────────────────
            TechSignal("aws", r"x-amz-", "header", header_name="x-amz-request-id"),
            TechSignal("aws", r"x-amz-", "header", header_name="x-amz-id-2"),
            TechSignal("aws", r"amazonaws", "url"),
            TechSignal("gcp", r"x-cloud-trace-context", "header", header_name="x-cloud-trace-context"),
            TechSignal("gcp", r"google", "header", header_name="server"),
            TechSignal("azure", r"x-ms-", "header", header_name="x-ms-request-id"),

            # ── Security Headers (informational) ──────────────────
            TechSignal("has_xfo", r".", "header", header_name="x-frame-options"),
            TechSignal("hsts", r".", "header", header_name="strict-transport-security"),
            TechSignal("has_csp", r".", "header", header_name="content-security-policy"),
        ]


# ── Convenience ──────────────────────────────────────────────────────


def quick_classify(
    headers: Optional[dict] = None,
    url: str = "",
    body: str = "",
) -> dict[str, float]:
    """One-shot classification."""
    return TechClassifier().classify(headers=headers, url=url, body=body)


def classify_target(headers: dict, url: str = "", body: str = "") -> list[str]:
    """Return sorted list of detected techs (confidence >= LOW)."""
    result = quick_classify(headers=headers, url=url, body=body)
    return sorted([t for t, c in result.items() if c >= 0.25])
