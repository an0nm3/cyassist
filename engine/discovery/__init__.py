"""Phase E1: Modern target discovery engine.

Sub-modules:
  js_analyzer.JSEndpointAnalyzer    — Extract endpoints/ops/secrets from JS bundles
  graphql_discoverer.GraphQLDiscoverer — Probe GraphQL endpoints + introspection
  spa_crawler.SPACrawler            — Playwright-based SPA route + XHR discovery
"""

from engine.discovery.js_analyzer import JSEndpointAnalyzer, DiscoveredEndpoint
from engine.discovery.graphql_discoverer import GraphQLDiscoverer
from engine.discovery.spa_crawler import SPACrawler, SPACrawlResult

__all__ = [
    "JSEndpointAnalyzer",
    "DiscoveredEndpoint",
    "GraphQLDiscoverer",
    "SPACrawler",
    "SPACrawlResult",
]
