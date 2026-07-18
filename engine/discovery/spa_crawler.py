"""Phase E1c: SPA crawler — Playwright-based route + API endpoint discovery.

Navigates modern SPAs, intercepts XHR/fetch calls, follows client-side
router links, and collects discovered API endpoints, routes, and
GraphQL operations.

Requires Playwright (pip install playwright && playwright install chromium).
Gracefully falls back if Playwright is unavailable.
"""

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse

logger = logging.getLogger("spa_crawler")

try:
    from playwright.sync_api import sync_playwright, Page, Route, Request
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@dataclass
class SPACrawlResult:
    """Results from a single SPA crawl session."""

    url: str
    routes_discovered: list[str] = field(default_factory=list)
    api_endpoints: list[str] = field(default_factory=list)
    graphql_operations: list[dict] = field(default_factory=list)
    websocket_urls: list[str] = field(default_factory=list)
    js_bundles: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    duration_ms: float = 0.0

    def to_endpoints(self) -> list["DiscoveredEndpoint"]:
        """Convert crawl results to DiscoveredEndpoint objects."""
        from engine.discovery.js_analyzer import DiscoveredEndpoint

        results = []
        seen = set()

        for route in self.routes_discovered:
            if route not in seen:
                seen.add(route)
                results.append(DiscoveredEndpoint(
                    type="route", url=route,
                    confidence=0.7, context="SPA crawl route discovery",
                    source="spa_crawl",
                ))

        for ep in self.api_endpoints:
            if ep not in seen:
                seen.add(ep)
                results.append(DiscoveredEndpoint(
                    type="api" if "/api/" in ep else "rest",
                    url=ep,
                    confidence=0.8, context="SPA crawl XHR interception",
                    source="spa_crawl",
                ))

        for op in self.graphql_operations:
            key = f"gql:{op.get('operationName', '')}"
            if key not in seen:
                seen.add(key)
                results.append(DiscoveredEndpoint(
                    type="graphql",
                    url=f"operation:{op.get('operationName', 'unknown')}",
                    confidence=0.8,
                    context=f"GQL {op.get('operationType', 'query')} "
                            f"{op.get('operationName', '')}",
                    source="spa_crawl",
                    method=op.get("method", "POST"),
                ))

        for ws in self.websocket_urls:
            if ws not in seen:
                seen.add(ws)
                results.append(DiscoveredEndpoint(
                    type="websocket", url=ws,
                    confidence=0.9, context="SPA crawl WS discovery",
                    source="spa_crawl",
                ))

        return results


class SPACrawler:
    """Playwright-based SPA crawler for route + API discovery.

    Usage:
        crawler = SPACrawler("https://target.com")
        result = crawler.crawl()
        for ep in result.to_endpoints():
            print(ep.url)
    """

    def __init__(self, target_url: str, max_routes: int = 20,
                 timeout_ms: int = 30000, headless: bool = True,
                 cookies: Optional[list[dict]] = None):
        self.target_url = target_url
        self.max_routes = max_routes
        self.timeout_ms = timeout_ms
        self.headless = headless
        self.cookies = cookies or []

    def crawl(self) -> SPACrawlResult:
        """Execute the SPA crawl. Returns SPACrawlResult.

        If Playwright is unavailable, returns an empty result with
        an error message.
        """
        result = SPACrawlResult(url=self.target_url)
        start = time.time()

        if not HAS_PLAYWRIGHT:
            result.errors.append("Playwright not installed — install with: "
                                  "pip install playwright && playwright install chromium")
            result.duration_ms = (time.time() - start) * 1000
            return result

        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=self.headless)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                )

                if self.cookies:
                    context.add_cookies(self.cookies)

                page = context.new_page()

                # Intercept all network requests
                api_urls: set[str] = set()
                ws_urls: set[str] = set()
                gql_ops: list[dict] = []

                def _on_request(request: Request):
                    url = request.url
                    parsed = urlparse(url)

                    # Skip non-HTTP(S) and same-origin static assets
                    if parsed.scheme not in ("http", "https"):
                        if parsed.scheme in ("ws", "wss"):
                            ws_urls.add(url)
                        return

                    # Skip static assets
                    if any(ext in url for ext in (".js", ".css", ".png", ".jpg",
                                                  ".gif", ".svg", ".ico", ".woff",
                                                  ".woff2", ".ttf", ".eot")):
                        if ".js" in url:
                            result.js_bundles.append(url)
                        return

                    # Check for API calls
                    if "/api/" in url or "/rest/" in url or "/graphql" in url:
                        api_urls.add(url)

                    # Detect GraphQL requests
                    if "graphql" in url.lower() or "gql" in url.lower():
                        try:
                            body = request.post_data or ""
                            if body:
                                payload = json.loads(body)
                                if "query" in payload or "operationName" in payload:
                                    gql_ops.append({
                                        "url": url,
                                        "operationName": payload.get("operationName", ""),
                                        "operationType": (
                                            "mutation" if "mutation" in payload.get("query", "")
                                            else "query"
                                        ),
                                        "method": request.method,
                                    })
                        except (json.JSONDecodeError, ValueError):
                            pass

                page.on("request", _on_request)

                # Navigate to the target
                try:
                    page.goto(self.target_url, wait_until="networkidle",
                              timeout=self.timeout_ms)
                except Exception as e:
                    result.errors.append(f"Navigation failed: {e}")

                # Collect current route
                current_url = page.url
                parsed_current = urlparse(current_url)
                result.routes_discovered.append(parsed_current.path or "/")

                # Discover links on the page
                links = page.eval_on_selector_all(
                    "a[href]",
                    """els => els.map(el => el.getAttribute('href'))
                               .filter(h => h && !h.startsWith('#')
                                       && !h.startsWith('mailto:')
                                       && !h.startsWith('tel:'))"""
                )

                # Follow discoverable routes (up to max_routes limit)
                visited_routes = {parsed_current.path or "/"}
                for link in links:
                    if len(visited_routes) >= self.max_routes:
                        break

                    resolved = urljoin(current_url, link)
                    parsed_link = urlparse(resolved)

                    # Only follow same-origin links
                    if parsed_link.netloc and parsed_link.netloc != parsed_current.netloc:
                        continue

                    path = parsed_link.path or "/"
                    if path in visited_routes:
                        continue
                    visited_routes.add(path)

                    if path not in result.routes_discovered:
                        result.routes_discovered.append(path)

                    # Navigate to the link
                    try:
                        page.goto(resolved, wait_until="networkidle",
                                  timeout=self.timeout_ms)
                    except Exception:
                        continue

                # Close
                context.close()
                browser.close()

                # Populate result
                result.api_endpoints = list(api_urls)
                result.websocket_urls = list(ws_urls)
                result.graphql_operations = gql_ops

        except Exception as e:
            result.errors.append(f"Crawl failed: {e}")

        result.duration_ms = (time.time() - start) * 1000
        return result
