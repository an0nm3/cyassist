"""Phase E1a: JS bundle endpoint analyzer.

Extracts API endpoints, GraphQL operations, hidden routes, and potential
secrets from JavaScript bundles using regex patterns. Zero external
dependencies beyond stdlib — works on downloaded JS files or strings.

Output: list of DiscoveredEndpoint namedtuples with type, url, confidence.
"""

import json
import logging
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("js_analyzer")


# ── Data Model ──────────────────────────────────────────────────────────


@dataclass
class DiscoveredEndpoint:
    """An endpoint discovered from JS analysis.

    type: one of "api", "graphql", "rest", "websocket", "internal", "route", "secret"
    url: the discovered URL or endpoint path
    confidence: 0.0–1.0
    context: surrounding code snippet (first 120 chars)
    source: where it was found ("js_bundle", "graphql_introspection", "spa_crawl")
    method: HTTP method hint if available ("GET", "POST", etc. or "")
    """

    type: str
    url: str
    confidence: float = 0.5
    context: str = ""
    source: str = "js_bundle"
    method: str = ""

    def normalize(self, base_url: str = "") -> str:
        """Resolve relative URL against a base."""
        if self.url.startswith("http://") or self.url.startswith("https://"):
            return self.url
        if self.url.startswith("//"):
            return "https:" + self.url
        if self.url.startswith("/"):
            if base_url:
                parsed = urllib.parse.urlparse(base_url)
                return f"{parsed.scheme}://{parsed.netloc}{self.url}"
            return self.url
        if base_url:
            return urllib.parse.urljoin(base_url, self.url)
        return self.url

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "url": self.url,
            "confidence": self.confidence,
            "context": self.context[:120],
            "source": self.source,
            "method": self.method,
        }


# ── Pattern Catalogs ────────────────────────────────────────────────────

# API endpoint patterns: /api/v1/..., /rest/..., /graphql, etc.
_API_PATTERN = re.compile(
    r"""['\"`]                         # opening quote
    ((?:/api|/v[12]|/rest|/graphql|/gql|
       /query|/mutate|/webhook|/hook|
       /service|/internal|/private|
       /admin|/manage|/console)
    (?:/[a-zA-Z0-9_\-\.]+)*)           # optional path segments (0+)
    ['\"`]                              # closing quote
    """,
    re.VERBOSE,
)

# GraphQL operation names: query Foo { ... }, mutation Bar { ... }
_GQL_OPERATION = re.compile(
    r"""(?:query|mutation|subscription)\s+
    ([a-zA-Z_]\w*)\s*[\({]            # operation name + opening paren/brace
    """,
    re.VERBOSE,
)

# fetch(url, {method: 'POST'}) or axios.post(url, ...) patterns
_FETCH_CALL = re.compile(
    r"""(?:fetch|axios|ky|got|superagent|request)\s*
    [\(['\"`]                          # opening paren + quote
    ([^'\"`\)]+)                       # URL
    ['\"`]                             # closing quote
    """,
    re.VERBOSE,
)

# WebSocket URLs
_WS_PATTERN = re.compile(
    r"""['\"`](wss?://[a-zA-Z0-9_\-\./?:&=]+)['\"`]""",
    re.VERBOSE,
)

# Internal hostnames / service URLs
_INTERNAL_PATTERN = re.compile(
    r"""['\"`](https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|
    172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|
    192\.168\.\d+\.\d+|
    [a-zA-Z0-9_\-]+\.internal|
    [a-zA-Z0-9_\-]+\.svc\.cluster\.local)
    (?::\d+)?                                # optional port
    (?:/[^\s'\"`]*)?)['\"`]""",
    re.VERBOSE | re.IGNORECASE,
)

# SPA client-side route patterns: { path: '/dashboard', component: ... }
_SPA_ROUTE = re.compile(
    r"""['\"`](/[a-zA-Z0-9_\-\./]+)['\"`]\s*[,:]\s*
    (?:['\"`][a-zA-Z]+['\"`]\s*[,:]?\s*)?
    (?:component|element|render|page)\b""",
    re.VERBOSE | re.IGNORECASE,
)

# Potential secrets (API keys, tokens)
_SECRET_PATTERN = re.compile(
    r"""['\"`]
    ((?:sk|pk|AKIA|eyJ)[a-zA-Z0-9_\-\.=]{10,})  # key-like value
    ['\"`]""",
    re.VERBOSE,
)


# ─── Analyzer ───────────────────────────────────────────────────────────


class JSEndpointAnalyzer:
    """Analyze JavaScript source for endpoints, operations, and secrets."""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url

    def analyze(self, js_source: str, source_label: str = "js_bundle"
                ) -> list[DiscoveredEndpoint]:
        """Run all extractors against JS source text.

        Args:
            js_source: Raw JavaScript source code
            source_label: Label for source tracking (e.g. filename or URL)

        Returns:
            Deduplicated list of DiscoveredEndpoint objects.
        """
        results: list[DiscoveredEndpoint] = []

        results.extend(self._extract_api_endpoints(js_source, source_label))
        results.extend(self._extract_graphql_operations(js_source, source_label))
        results.extend(self._extract_fetch_calls(js_source, source_label))
        results.extend(self._extract_websockets(js_source, source_label))
        results.extend(self._extract_internal_urls(js_source, source_label))
        results.extend(self._extract_spa_routes(js_source, source_label))
        results.extend(self._extract_secrets(js_source, source_label))

        return self._dedup(results)

    def _extract_api_endpoints(self, source: str, label: str
                               ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _API_PATTERN.finditer(source):
            url = m.group(1)
            if url in seen:
                continue
            seen.add(url)
            start = max(0, m.start() - 40)
            ctx = source[start:m.end() + 40].strip()
            confidence = 0.7 if "/api/" in url else 0.5
            ep_type = "graphql" if "graphql" in url or "gql" in url else "api"
            results.append(DiscoveredEndpoint(
                type=ep_type, url=url,
                confidence=confidence, context=ctx,
                source=label,
            ))
        return results

    def _extract_graphql_operations(self, source: str, label: str
                                    ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _GQL_OPERATION.finditer(source):
            op_name = m.group(1)
            if op_name in seen:
                continue
            seen.add(op_name)
            results.append(DiscoveredEndpoint(
                type="graphql",
                url=f"operation:{op_name}",
                confidence=0.8,
                context=f"GraphQL {m.group(0).strip()[:80]}",
                source=label,
                method="POST",
            ))
        return results

    def _extract_fetch_calls(self, source: str, label: str
                             ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _FETCH_CALL.finditer(source):
            url = m.group(1).strip().strip("'\"")
            if url in seen or url.startswith("${"):
                continue
            seen.add(url)
            results.append(DiscoveredEndpoint(
                type="api" if "/api/" in url else "rest",
                url=url,
                confidence=0.6,
                context=source[max(0, m.start() - 20):m.end() + 40].strip(),
                source=label,
            ))
        return results

    def _extract_websockets(self, source: str, label: str
                            ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _WS_PATTERN.finditer(source):
            url = m.group(1)
            if url in seen:
                continue
            seen.add(url)
            results.append(DiscoveredEndpoint(
                type="websocket", url=url,
                confidence=0.9, context=source[m.start():m.end()].strip(),
                source=label,
            ))
        return results

    def _extract_internal_urls(self, source: str, label: str
                               ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _INTERNAL_PATTERN.finditer(source):
            url = m.group(1)
            if url in seen:
                continue
            seen.add(url)
            results.append(DiscoveredEndpoint(
                type="internal", url=url,
                confidence=0.9,
                context=source[max(0, m.start() - 20):m.end() + 20].strip(),
                source=label,
            ))
        return results

    def _extract_spa_routes(self, source: str, label: str
                            ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _SPA_ROUTE.finditer(source):
            route = m.group(1)
            if route in seen:
                continue
            seen.add(route)
            results.append(DiscoveredEndpoint(
                type="route", url=route,
                confidence=0.6,
                context=source[max(0, m.start() - 20):m.end() + 20].strip(),
                source=label,
            ))
        return results

    def _extract_secrets(self, source: str, label: str
                         ) -> list[DiscoveredEndpoint]:
        seen = set()
        results = []
        for m in _SECRET_PATTERN.finditer(source):
            val = m.group(1)
            if val in seen:
                continue
            seen.add(val)
            # Filter out common false positives
            if any(fp in val for fp in ("undefined", "null", "false", "true")):
                continue
            results.append(DiscoveredEndpoint(
                type="secret", url=f"key:{val[:20]}...",
                confidence=0.3,
                context=source[max(0, m.start() - 20):m.end() + 20].strip(),
                source=label,
            ))
        return results

    @staticmethod
    def _dedup(items: list[DiscoveredEndpoint]) -> list[DiscoveredEndpoint]:
        seen: set[str] = set()
        result = []
        for item in items:
            key = f"{item.type}:{item.url}"
            if key in seen:
                continue
            seen.add(key)
            result.append(item)
        return result
