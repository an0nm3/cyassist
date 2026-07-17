"""Tests for Phase A4 — Tech Stack Classifier."""

from engine.tech_classifier import TechClassifier, quick_classify, classify_target


def _c():
    return TechClassifier()


# ── Web Servers ─────────────────────────────────────────────────────


def test_nginx():
    r = _c().classify(headers={"Server": "nginx/1.18.0"})
    assert r.get("nginx", 0) >= 0.5, f"nginx not detected: {r}"


def test_apache():
    r = _c().classify(headers={"Server": "Apache/2.4.41"})
    assert r.get("apache", 0) >= 0.5


def test_iis():
    r = _c().classify(headers={"Server": "Microsoft-IIS/10.0"})
    assert r.get("iis", 0) >= 0.5


def test_caddy():
    r = _c().classify(headers={"Server": "Caddy"})
    assert r.get("caddy", 0) >= 0.5


def test_tomcat():
    r = _c().classify(headers={"Server": "Apache-Coyote/1.1"})
    assert r.get("tomcat", 0) >= 0.5


# ── Backend Languages ────────────────────────────────────────────────


def test_php():
    r = _c().classify(headers={"X-Powered-By": "PHP/7.4"})
    assert r.get("php", 0) >= 0.5


def test_php_from_url():
    r = _c().classify(url="https://example.com/index.php?id=1")
    assert r.get("php", 0) >= 0.25


def test_python_flask():
    r = _c().classify(headers={"X-Powered-By": "flask"})
    assert r.get("flask", 0) >= 0.5


def test_django():
    r = _c().classify(headers={"X-Powered-By": "django"})
    assert r.get("django", 0) >= 0.5


def test_express():
    r = _c().classify(headers={"X-Powered-By": "Express"})
    assert r.get("express", 0) >= 0.5


def test_java():
    r = _c().classify(headers={"Set-Cookie": "JSESSIONID=abc123"})
    assert r.get("java", 0) >= 0.25


def test_aspnet():
    r = _c().classify(url="https://example.com/login.aspx")
    assert r.get("aspnet", 0) >= 0.25


def test_ruby_rails():
    r = _c().classify(headers={"X-Powered-By": "rails"})
    assert r.get("ruby", 0) >= 0.5


# ── CMS ──────────────────────────────────────────────────────────────


def test_wordpress():
    r = _c().classify(url="https://example.com/wp-admin/login.php")
    assert r.get("wordpress", 0) >= 0.25
    assert r.get("php", 0) >= 0.25


def test_wordpress_multi_signal():
    r = _c().classify(
        headers={"X-Powered-By": "PHP/7.4"},
        url="https://example.com/wp-content/themes/x/style.css",
        body='<link rel="stylesheet" href="/wp-content/themes/x/style.css" />',
    )
    assert r.get("wordpress", 0) >= 0.5
    assert r.get("php", 0) >= 0.5


def test_laravel():
    r = _c().classify(headers={"Set-Cookie": "laravel_session=abc"})
    assert r.get("laravel", 0) >= 0.25


# ── JS Frameworks ───────────────────────────────────────────────────


def test_nextjs():
    r = _c().classify(url="https://example.com/_next/data/build-id/page.json")
    assert r.get("nextjs", 0) >= 0.25


def test_react():
    r = _c().classify(body='<div id="root"></div><script>React.</script>')
    assert r.get("react", 0) >= 0.25


def test_vue():
    r = _c().classify(body="Vue.component('my-comp', { template: '...' })")
    assert r.get("vue", 0) >= 0.25


def test_angular():
    r = _c().classify(body='<app-root ng-version="17.0.0"></app-root>')
    assert r.get("angular", 0) >= 0.25


# ── Cloud / CDN ─────────────────────────────────────────────────────


def test_cloudflare():
    r = _c().classify(headers={"Server": "cloudflare"})
    assert r.get("cloudflare", 0) >= 0.5


def test_aws():
    r = _c().classify(headers={"x-amz-request-id": "abc123"})
    assert r.get("aws", 0) >= 0.25


# ── APIs ─────────────────────────────────────────────────────────────


def test_graphql():
    r = _c().classify(url="https://api.example.com/graphql")
    assert r.get("graphql", 0) >= 0.25


def test_rest_api():
    r = _c().classify(url="https://api.example.com/api/v3/users")
    assert r.get("rest", 0) >= 0.25


# ── Multi-signal Agreement ──────────────────────────────────────────


def test_php_wordpress_nginx():
    """Triple signal: server header + x-powered-by + URL."""
    r = _c().classify(
        headers={"Server": "nginx/1.18", "X-Powered-By": "PHP/7.4"},
        url="https://example.com/wp-admin/login.php",
    )
    for tech in ("nginx", "php", "wordpress"):
        assert tech in r, f"{tech} not in {r}"
    assert r.get("nginx", 0) >= 0.55
    assert r.get("php", 0) >= 0.55


def test_python_flask_postgres():
    """Triple signal: cookie + powered-by + error."""
    r = _c().classify(
        headers={
            "X-Powered-By": "flask",
            "Set-Cookie": "session=abc123",
        },
        body='<html>Error: psql: FATAL</html>',
    )
    assert r.get("flask", 0) >= 0.5
    assert r.get("postgresql", 0) >= 0.25


# ── Top Tech ─────────────────────────────────────────────────────────


def test_top_tech():
    c = TechClassifier()
    top = c.top_tech(headers={"Server": "nginx/1.18"})
    assert top == "nginx"


def test_top_tech_empty():
    c = TechClassifier()
    top = c.top_tech(headers={}, url="", body="")
    assert top == ""


# ── Convenience ─────────────────────────────────────────────────────


def test_quick_classify():
    r = quick_classify(headers={"Server": "nginx/1.18"})
    assert "nginx" in r


def test_classify_target():
    techs = classify_target(
        headers={"Server": "nginx/1.18", "X-Powered-By": "PHP/7.4"},
        url="https://example.com/wp-admin/login.php",
    )
    for t in ("nginx", "php", "wordpress"):
        assert t in techs, f"{t} missing"


def test_classify_target_no_match():
    assert classify_target(headers={}, url="", body="") == []
