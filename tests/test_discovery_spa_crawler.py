"""Tests for Phase E1c: SPA crawler — Playwright-based route discovery."""

from unittest.mock import patch, MagicMock

from engine.discovery.spa_crawler import SPACrawler, SPACrawlResult


def test_crawler_no_playwright():
    """Graceful fallback when Playwright is unavailable."""
    import engine.discovery.spa_crawler as sc
    original = sc.HAS_PLAYWRIGHT
    sc.HAS_PLAYWRIGHT = False

    try:
        crawler = SPACrawler("https://example.com")
        result = crawler.crawl()
        assert isinstance(result, SPACrawlResult)
        assert len(result.errors) == 1
        assert "Playwright not installed" in result.errors[0]
    finally:
        sc.HAS_PLAYWRIGHT = original


def test_crawl_result_defaults():
    result = SPACrawlResult(url="https://example.com")
    assert result.routes_discovered == []
    assert result.api_endpoints == []
    assert result.graphql_operations == []
    assert result.websocket_urls == []
    assert result.duration_ms == 0.0


def test_crawl_result_to_endpoints():
    result = SPACrawlResult(url="https://example.com")
    result.routes_discovered = ["/", "/dashboard", "/users"]
    result.api_endpoints = ["https://api.example.com/api/v1/users"]
    result.graphql_operations = [
        {"url": "https://api.example.com/graphql",
         "operationName": "GetUsers",
         "operationType": "query",
         "method": "POST"}
    ]
    result.websocket_urls = ["wss://api.example.com/ws"]

    endpoints = result.to_endpoints()
    types = [e.type for e in endpoints]
    assert "route" in types
    assert "api" in types  # URL contains "/api/" → "api"
    assert "graphql" in types
    assert "websocket" in types


def test_crawl_result_dedup():
    result = SPACrawlResult(url="https://example.com")
    result.routes_discovered = ["/dashboard", "/dashboard"]
    result.api_endpoints = ["/api/v1/users", "/api/v1/users"]

    endpoints = result.to_endpoints()
    route_count = sum(1 for e in endpoints if e.type == "route")
    api_count = sum(1 for e in endpoints if e.type == "api")
    assert route_count == 1
    assert api_count == 1
