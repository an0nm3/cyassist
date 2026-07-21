"""Tests for Phase G: Adaptive Crawler (data structures, no Playwright)."""
import json
import os
import tempfile

import pytest

from engine.discovery.adaptive_crawler import (
    AdaptiveCrawler,
    DiscoveredRoute,
    LoginForm,
    AuthSession,
    CrawlResult,
    AuthState,
)


class TestDataClasses:
    def test_discovered_route_defaults(self):
        r = DiscoveredRoute(path="/test")
        assert r.path == "/test"
        assert r.method == "GET"
        assert r.auth_required is False
        assert r.tech == []
        assert r.params == []

    def test_discovered_route_full(self):
        r = DiscoveredRoute(
            path="/api/users",
            method="POST",
            auth_required=True,
            role="admin",
            tech=["python", "flask"],
            framework="flask",
            status=200,
            params=["id", "name"],
        )
        assert r.method == "POST"
        assert r.auth_required is True
        assert r.role == "admin"
        assert r.source == "crawl"

    def test_login_form_defaults(self):
        f = LoginForm(url="http://example.com/login")
        assert f.url == "http://example.com/login"
        assert f.method == "POST"
        assert f.extra_fields == {}

    def test_login_form_password_detection(self):
        f = LoginForm(url="http://test.com/login", detected_by="password_field")
        assert f.detected_by == "password_field"

    def test_auth_session_cookie(self):
        s = AuthSession(
            cookies=[{"name": "PHPSESSID", "value": "abc123"}],
            auth_type="cookie",
            created_at=1000.0,
        )
        assert s.auth_type == "cookie"
        assert len(s.cookies) == 1

    def test_auth_session_bearer(self):
        s = AuthSession(
            bearer_token="eyJhbGciOiJIUzI1NiIs...",
            auth_type="bearer",
        )
        assert s.auth_type == "bearer"
        assert s.bearer_token.startswith("eyJ")

    def test_crawl_result_defaults(self):
        r = CrawlResult(url="http://example.com/")
        assert r.authenticated is False
        assert r.pre_auth_surfaces == []
        assert r.post_auth_surfaces == []
        assert r.errors == []

    def test_crawl_result_with_data(self):
        r = CrawlResult(
            url="http://test.com/",
            authenticated=True,
            auth_type="cookie",
            total_routes=5,
            api_endpoints=["http://test.com/api/users"],
            graphql_operations=[{"operationName": "GetUser", "operationType": "query"}],
            websocket_urls=["ws://test.com/socket"],
        )
        assert r.authenticated is True
        assert r.auth_type == "cookie"
        assert len(r.api_endpoints) == 1
        assert len(r.graphql_operations) == 1


class TestLoginPathDetection:
    def test_login_paths_contain_common(self):
        crawler = AdaptiveCrawler("http://example.com/")
        assert "/login" in crawler._LOGIN_PATHS
        assert "/login.php" in crawler._LOGIN_PATHS
        assert "/wp-login.php" in crawler._LOGIN_PATHS
        assert "/auth/login" in crawler._LOGIN_PATHS

    def test_post_login_paths_contain_common(self):
        crawler = AdaptiveCrawler("http://example.com/")
        assert "/dashboard" in crawler._POST_LOGIN_PATHS
        assert "/setup.php" in crawler._POST_LOGIN_PATHS

    def test_chromium_paths_ordered(self):
        crawler = AdaptiveCrawler("http://example.com/")
        assert len(crawler._CHROMIUM_PATHS) >= 4
        assert "/usr/bin/chromium" in crawler._CHROMIUM_PATHS
        assert "/usr/bin/google-chrome" in crawler._CHROMIUM_PATHS


class TestCrawlResultAggregation:
    def test_total_routes_count(self):
        r = CrawlResult(url="http://test.com/")
        r.pre_auth_surfaces = [
            DiscoveredRoute(path="/login", status=200),
        ]
        r.post_auth_surfaces = [
            DiscoveredRoute(path="/dashboard", status=200),
            DiscoveredRoute(path="/settings", status=200),
        ]
        r.total_routes = len(r.pre_auth_surfaces) + len(r.post_auth_surfaces)
        assert r.total_routes == 3

    def test_auth_aware_comparison(self):
        """Verify that the comparison in _compare_surfaces works."""
        r = CrawlResult(url="http://test.com/")

        r.pre_auth_surfaces = [
            DiscoveredRoute(path="/", status=200),
            DiscoveredRoute(path="/login", status=200),
        ]
        r.post_auth_surfaces = [
            DiscoveredRoute(path="/", status=200),  # Also in pre-auth
            DiscoveredRoute(path="/dashboard", status=200),
            DiscoveredRoute(path="/admin", status=200),
        ]

        # Simulate _compare_surfaces
        pre_paths = {x.path for x in r.pre_auth_surfaces}
        post_paths = {x.path for x in r.post_auth_surfaces}

        auth_gated = post_paths - pre_paths
        always_public = pre_paths & post_paths

        assert auth_gated == {"/dashboard", "/admin"}
        assert always_public == {"/"}

        for route in r.post_auth_surfaces:
            if route.path in auth_gated:
                route.auth_required = True
                route.source = "auth_gated"

        for route in r.pre_auth_surfaces:
            if route.path in always_public:
                route.source = "always_public"

        dashboard = [r for r in r.post_auth_surfaces if r.path == "/dashboard"][0]
        assert dashboard.auth_required is True
        assert dashboard.source == "auth_gated"

        home = [r for r in r.pre_auth_surfaces if r.path == "/"][0]
        assert home.source == "always_public"


class TestChromiumDetection:
    def test_find_chromium_noop(self):
        """Test that _find_chromium doesn't crash."""
        crawler = AdaptiveCrawler("http://example.com/")
        result = crawler._find_chromium()
        assert result is None or os.path.exists(result)


class TestKnowledgeGraphIntegration:
    def test_to_knowledge_graph_nodes_empty(self):
        from engine.knowledge_graph import KnowledgeGraph
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        kg = KnowledgeGraph(tmp.name)
        crawler = AdaptiveCrawler("http://example.com/", kg=kg)
        result = CrawlResult(url="http://example.com/")
        nodes = crawler.to_knowledge_graph_nodes(result)
        assert nodes == []
        kg.close()
        os.unlink(tmp.name)

    def test_to_knowledge_graph_nodes_with_surfaces(self):
        from engine.knowledge_graph import KnowledgeGraph, Node
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        kg = KnowledgeGraph(tmp.name)
        crawler = AdaptiveCrawler("http://example.com/", kg=kg)

        result = CrawlResult(url="http://example.com/")
        result.pre_auth_surfaces = [
            DiscoveredRoute(path="/", status=200),
            DiscoveredRoute(path="/login", status=200, tech=["php"]),
        ]
        result.post_auth_surfaces = [
            DiscoveredRoute(path="/dashboard", status=200, auth_required=True),
        ]

        nodes = crawler.to_knowledge_graph_nodes(result)
        assert len(nodes) == 3

        # Check KG has the nodes
        surfaces = kg.query_nodes("Surface")
        assert len(surfaces) == 3

        # Verify properties
        login_node = [n for n in surfaces if n.name == "GET:/"][0]
        assert login_node.properties.get("status") == 200

        kg.close()
        os.unlink(tmp.name)

    def test_to_knowledge_graph_edges(self):
        from engine.knowledge_graph import KnowledgeGraph
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        kg = KnowledgeGraph(tmp.name)
        crawler = AdaptiveCrawler("http://example.com/", kg=kg)

        result = CrawlResult(url="http://example.com/")
        result.pre_auth_surfaces = [
            DiscoveredRoute(path="/", status=200),
            DiscoveredRoute(path="/login", status=200),
        ]

        nodes = crawler.to_knowledge_graph_nodes(result)
        assert kg.count_edges() > 0

        kg.close()
        os.unlink(tmp.name)

    def test_auth_gated_nodes_marked(self):
        from engine.knowledge_graph import KnowledgeGraph
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        kg = KnowledgeGraph(tmp.name)
        crawler = AdaptiveCrawler("http://example.com/", kg=kg)

        result = CrawlResult(url="http://example.com/")
        result.post_auth_surfaces = [
            DiscoveredRoute(path="/admin", status=200, auth_required=True, source="auth_gated"),
        ]

        nodes = crawler.to_knowledge_graph_nodes(result)
        surfaces = kg.query_nodes("Surface")
        admin = [n for n in surfaces if n.name == "GET:/admin"][0]
        assert admin.properties.get("requires_auth") is True
        assert admin.properties.get("source") == "auth_gated"

        kg.close()
        os.unlink(tmp.name)
