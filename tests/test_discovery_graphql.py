"""Tests for Phase E1b: GraphQL endpoint discovery."""

from unittest.mock import patch, MagicMock
import json

from engine.discovery.graphql_discoverer import GraphQLDiscoverer


def _mock_response(status=200, json_data=None):
    """Create a mock httpx response."""
    mock = MagicMock()
    mock.status_code = status
    mock.json.return_value = json_data or {}
    return mock


def test_discoverer_probe_success():
    """Single endpoint responds to __typename probe."""
    discoverer = GraphQLDiscoverer("https://example.com")

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value
        # __typename probe succeeds
        instance.post.side_effect = [
            _mock_response(200, {"data": {"__typename": "Query"}}),
            # introspection fails
            _mock_response(403, {"error": "Introspection disabled"}),
        ]

        results = discoverer.discover()
        assert len(results) >= 1


def test_discoverer_probe_fails():
    """Endpoint does not respond to __typename probe."""
    discoverer = GraphQLDiscoverer("https://example.com")

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value
        instance.post.return_value = _mock_response(404, {})

        results = discoverer.discover()
        # All paths fail — no results
        assert len(results) == 0


def test_discoverer_introspection_success():
    """Full introspection succeeds on a GraphQL endpoint."""
    schema = {
        "data": {
            "__schema": {
                "queryType": {"name": "Query"},
                "mutationType": {"name": "Mutation"},
                "subscriptionType": None,
                "types": [
                    {"name": "Query", "kind": "OBJECT",
                     "fields": [{"name": "users", "type": {"name": "User", "kind": "OBJECT", "ofType": None}}]},
                    {"name": "User", "kind": "OBJECT",
                     "fields": [{"name": "id", "type": {"name": "ID", "kind": "SCALAR", "ofType": None}}]},
                ],
                "directives": [],
            }
        }
    }

    discoverer = GraphQLDiscoverer("https://example.com")

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value
        instance.post.side_effect = [
            _mock_response(200, {"data": {"__typename": "Query"}}),
            _mock_response(200, schema),
        ]

        results = discoverer.discover()
        assert len(results) >= 1
        ep = results[0]
        assert ep.confidence >= 0.8


def test_discoverer_multiple_paths():
    """Multiple paths are probed; only active one returns result."""
    discoverer = GraphQLDiscoverer("https://example.com")

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value
        # First path fails, second succeeds
        call_count = 0

        def side_effect(url, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return _mock_response(404, {})
            return _mock_response(200, {"data": {"__typename": "Query"}})

        instance.post.side_effect = side_effect

        results = discoverer.discover()
        assert len(results) >= 1


def test_discoverer_extra_paths():
    """Custom paths are probed in addition to defaults."""
    discoverer = GraphQLDiscoverer("https://example.com",
                                    extra_paths=["/custom/graphql"])

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value
        instance.post.return_value = _mock_response(200, {"data": {"__typename": "Query"}})

        results = discoverer.discover()
        assert len(results) >= 1


def test_discoverer_dedup():
    """Identical URLs are not duplicated."""
    discoverer = GraphQLDiscoverer("https://example.com",
                                    extra_paths=["/graphql"])

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value

        def side_effect(url, **kwargs):
            from unittest.mock import MagicMock
            resp = MagicMock()
            # Only succeed for exact /graphql path (once), to test dedup
            if url.rstrip("/") == "https://example.com/graphql":
                resp.status_code = 200
                resp.json.return_value = {"data": {"__typename": "Query"}}
            else:
                resp.status_code = 404
                resp.json.return_value = {}
            return resp

        instance.post.side_effect = side_effect

        results = discoverer.discover()
        graphql_results = [r for r in results if "/graphql" in r.url]
        assert len(graphql_results) == 1


def test_discoverer_timeout():
    """Timeout on probe does not crash."""
    discoverer = GraphQLDiscoverer("https://example.com", timeout=0.001)

    with patch("httpx.Client") as MockClient:
        instance = MockClient.return_value.__enter__.return_value
        instance.post.side_effect = Exception("timeout")

        results = discoverer.discover()
        assert len(results) == 0


def test_discoverer_no_httpx():
    """Graceful fallback when httpx is unavailable."""
    import engine.discovery.graphql_discoverer as gd
    original = gd.httpx
    gd.httpx = None

    try:
        discoverer = GraphQLDiscoverer("https://example.com")
        results = discoverer.discover()
        assert len(results) == 0
    finally:
        gd.httpx = original
