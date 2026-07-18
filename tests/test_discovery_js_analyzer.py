"""Tests for Phase E1a: JS bundle endpoint analyzer."""

from engine.discovery.js_analyzer import JSEndpointAnalyzer, DiscoveredEndpoint


# ── DiscoveredEndpoint Tests ───────────────────────────────────────────


def test_endpoint_defaults():
    ep = DiscoveredEndpoint(type="api", url="/api/v1/users")
    assert ep.confidence == 0.5
    assert ep.source == "js_bundle"
    assert ep.method == ""
    assert ep.context == ""


def test_endpoint_normalize_absolute():
    ep = DiscoveredEndpoint(type="api", url="https://example.com/api/v1/users")
    assert ep.normalize() == "https://example.com/api/v1/users"


def test_endpoint_normalize_relative():
    ep = DiscoveredEndpoint(type="api", url="/api/v1/users")
    assert ep.normalize("https://example.com") == "https://example.com/api/v1/users"


def test_endpoint_normalize_protocol_relative():
    ep = DiscoveredEndpoint(type="api", url="//example.com/api")
    assert ep.normalize() == "https://example.com/api"


def test_endpoint_normalize_no_base():
    ep = DiscoveredEndpoint(type="api", url="/api/v1/users")
    assert ep.normalize() == "/api/v1/users"


def test_endpoint_to_dict():
    ep = DiscoveredEndpoint(type="api", url="/api/data", confidence=0.8)
    d = ep.to_dict()
    assert d["type"] == "api"
    assert d["url"] == "/api/data"
    assert d["confidence"] == 0.8


# ── JSEndpointAnalyzer Tests ───────────────────────────────────────────


def test_analyzer_extract_api_endpoints():
    js = """
        const API = '/api/v1/users';
        fetch('/api/v1/posts/123');
        axios.post('/rest/admin/config', {});
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    urls = [r.url for r in results]
    assert "/api/v1/users" in urls
    assert "/api/v1/posts/123" in urls
    assert "/rest/admin/config" in urls


def test_analyzer_extract_graphql_operations():
    js = """
        const query = `query GetUsers { users { id name } }`;
        const mutation = `mutation CreateUser($input: UserInput!) { createUser(input: $input) { id } }`;
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    ops = [r for r in results if r.type == "graphql"]
    assert len(ops) >= 1
    operation_names = [r.url for r in ops]
    assert any("GetUsers" in name for name in operation_names)


def test_analyzer_extract_fetch_calls():
    js = """
        fetch('/api/data');
        axios.get('/api/config');
        ky.post('/api/upload', {body: formData});
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    urls = [r.url for r in results]
    assert "/api/data" in urls
    assert "/api/config" in urls


def test_analyzer_extract_websockets():
    js = """
        const ws = new WebSocket('wss://api.example.com/ws/live');
        const ws2 = new WebSocket('ws://chat.internal/stream');
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    ws = [r for r in results if r.type == "websocket"]
    assert len(ws) == 2
    assert any("wss://api.example.com/ws/live" in r.url for r in ws)


def test_analyzer_extract_internal_urls():
    js = """
        const db = 'http://localhost:5432/db';
        const internal = 'https://payments.internal/api/v1/charge';
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    internal = [r for r in results if r.type == "internal"]
    assert len(internal) >= 2
    assert any("localhost" in r.url for r in internal)


def test_analyzer_extract_spa_routes():
    js = """
        { path: '/dashboard', component: Dashboard },
        { path: '/users/:id/profile', element: UserProfile },
        { path: '/admin/settings', render: SettingsPage },
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    routes = [r for r in results if r.type == "route"]
    assert len(routes) >= 1
    route_paths = [r.url for r in routes]
    assert any("/dashboard" in p for p in route_paths)


def test_analyzer_extract_secrets():
    js = """
        const key = 'sk_live_abcdef1234567890abcdef';
        const aws = 'AKIA1234567890ABCDEF';
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    secrets = [r for r in results if r.type == "secret"]
    assert len(secrets) >= 1


def test_analyzer_dedup():
    js = """
        const x = '/api/v1/users';
        const y = '/api/v1/users';
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    count = sum(1 for r in results if r.url == "/api/v1/users")
    assert count == 1


def test_analyzer_different_sources():
    js = "fetch('/api/data');"
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js, source_label="custom_bundle")
    for r in results:
        assert r.source == "custom_bundle"


def test_analyzer_empty():
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze("console.log('hello');")
    assert len(results) == 0


def test_analyzer_graphql_endpoint_detection():
    js = """
        const url = '/graphql';
        const gql = '/api/gql';
    """
    analyzer = JSEndpointAnalyzer()
    results = analyzer.analyze(js)

    graphql = [r for r in results if r.type == "graphql"]
    assert len(graphql) >= 2


def test_analyzer_base_url_resolution():
    analyzer = JSEndpointAnalyzer(base_url="https://example.com")
    results = analyzer.analyze("fetch('/api/v1/items');")
    ep = results[0]
    assert ep.normalize("https://example.com") == "https://example.com/api/v1/items"
