"""Phase E1b: GraphQL endpoint discoverer.

Probes common GraphQL endpoint paths and attempts introspection queries.
Pure HTTP-based — no browser required.

Output: list of DiscoveredEndpoint with type="graphql", includes
schema operations if introspection succeeds.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore[assignment]

logger = logging.getLogger("graphql_discoverer")


# ── Common GraphQL endpoint paths ───────────────────────────────────────

_GQL_PATHS = [
    "/graphql",
    "/gql",
    "/query",
    "/api",
    "/api/graphql",
    "/api/v1/graphql",
    "/api/v2/graphql",
    "/v1/graphql",
    "/v2/graphql",
    "/graph",
    "/graphiql",
    "/playground",
    "/api/query",
    "/api/v1/query",
    "/api/gql",
    "/_api/graphql",
    "/_graphql",
    "/admin/graphql",
    "/api/admin/graphql",
    "/graphql/v1",
    "/graphql/v2",
    "/graphql/private",
]

# The standard GraphQL introspection query
_INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      name
      kind
      description
      fields {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
    directives { name description locations }
  }
}
"""

# Shorter probe query (succeeds even when introspection is disabled)
_PROBE_QUERY = """
query { __typename }
"""


@dataclass
class GraphQLEndpoint:
    """A discovered GraphQL endpoint with its schema details."""

    url: str
    introspection_available: bool = False
    query_type: str = ""
    mutation_type: str = ""
    subscription_type: str = ""
    operation_count: int = 0
    type_count: int = 0
    directive_count: int = 0
    response_time_ms: float = 0.0

    def to_endpoint(self) -> "DiscoveredEndpoint":
        from engine.discovery.js_analyzer import DiscoveredEndpoint
        return DiscoveredEndpoint(
            type="graphql",
            url=self.url,
            confidence=0.9 if self.introspection_available else 0.7,
            context=(
                f"GQL: query={self.query_type or '?'} "
                f"mutation={self.mutation_type or '?'} "
                f"types={self.type_count} ops={self.operation_count}"
            ),
            source="graphql_introspection",
            method="POST",
        )


class GraphQLDiscoverer:
    """Discover GraphQL endpoints by probing common paths.

    Uses httpx for HTTP calls. Falls back gracefully if httpx is unavailable.
    """

    def __init__(self, base_url: str, timeout: float = 10.0,
                 extra_paths: Optional[list[str]] = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.paths = _GQL_PATHS + (extra_paths or [])

    def discover(self) -> list["DiscoveredEndpoint"]:
        """Probe all paths for GraphQL endpoints.

        Returns deduplicated list of DiscoveredEndpoint from js_analyzer.
        """
        from engine.discovery.js_analyzer import DiscoveredEndpoint

        if httpx is None:
            logger.warning("httpx not available — skipping GraphQL discovery")
            return []

        results: list[DiscoveredEndpoint] = []
        seen_urls: set[str] = set()

        for path in self.paths:
            url = urljoin(self.base_url, path)
            if url in seen_urls:
                continue
            seen_urls.add(url)

            ep = self._probe(url)
            if ep:
                results.append(ep.to_endpoint())

        return self._dedup_urls(results)

    def _probe(self, url: str) -> Optional[GraphQLEndpoint]:
        """Try introspection query on a single URL."""
        try:
            with httpx.Client(timeout=self.timeout, verify=False) as client:
                start = __import__("time").time()

                # Step 1: probe with __typename
                resp = client.post(url, json={"query": _PROBE_QUERY},
                                   headers={"Content-Type": "application/json"})
                rt = (__import__("time").time() - start) * 1000

                if resp.status_code != 200:
                    return None

                body = resp.json()
                if body.get("data", {}).get("__typename") is None:
                    return None

                ep = GraphQLEndpoint(url=url, response_time_ms=rt)

                # Step 2: try full introspection
                intro_resp = client.post(
                    url, json={"query": _INTROSPECTION_QUERY},
                    headers={"Content-Type": "application/json"},
                    timeout=self.timeout,
                )

                if intro_resp.status_code == 200:
                    try:
                        schema = intro_resp.json().get("data", {}).get("__schema", {})
                        if schema:
                            ep.introspection_available = True
                            ep.query_type = (schema.get("queryType") or {}).get("name", "")
                            ep.mutation_type = (schema.get("mutationType") or {}).get("name", "")
                            ep.subscription_type = (schema.get("subscriptionType") or {}).get("name", "")
                            ep.type_count = len(schema.get("types", []))
                            ep.operation_count = sum(
                                len(t.get("fields", []))
                                for t in schema.get("types", [])
                                if t.get("fields")
                            )
                            ep.directive_count = len(schema.get("directives", []))
                    except (json.JSONDecodeError, KeyError, TypeError):
                        pass

                return ep

        except Exception as e:
            logger.debug(f"GraphQL probe failed for {url}: {e}")
            return None

    @staticmethod
    def _dedup_urls(items: list["DiscoveredEndpoint"]) -> list["DiscoveredEndpoint"]:
        seen = set()
        result = []
        for item in items:
            if item.url in seen:
                continue
            seen.add(item.url)
            result.append(item)
        return result
