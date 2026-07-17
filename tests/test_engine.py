"""Tests for cyassist/engine/ — vector_schema, curl_parser, tech_detector, report_parser."""

import tempfile

from engine.vector_schema import FeatureVector, VectorStore, payload_hash
from engine.curl_parser import extract_curl_commands, parse_curl_command, extract_urls_fallback
from engine.tech_detector import detect_all, detect_from_headers, detect_from_error
from engine.report_parser import parse_report, extract_sections, extract_cwe


# ── Vector Schema Tests ──────────────────────────────────────────────


def test_feature_vector_defaults():
    v = FeatureVector(
        source_url="https://h1.com/reports/1",
        source_platform="h1",
        cwe="89", sink="sql_query", payload="1=1",
    )
    assert v.source_platform == "h1"
    assert v.normalized_payload_hash != ""


def test_payload_hash():
    h1 = payload_hash("' OR 1=1--")
    h2 = payload_hash("' OR 1=1--")
    h3 = payload_hash("different")
    assert h1 == h2
    assert h1 != h3


def test_vector_store_insert_query():
    db = tempfile.mktemp(suffix=".db")
    store = VectorStore(db_path=db)
    v = FeatureVector(
        source_url="https://h1.com/reports/1",
        source_platform="h1",
        cwe="89", tech=["python"], sink="sql_query",
        payload="1=1", payload_class="boolean_blind",
    )
    store.insert(v)
    assert store.count() == 1
    r = store.query(cwe="89")
    assert len(r) == 1
    assert r[0].cwe == "89"
    store.close()


def test_vector_store_query_empty():
    db = tempfile.mktemp(suffix=".db")
    store = VectorStore(db_path=db)
    r = store.query(cwe="99")
    assert len(r) == 0
    store.close()


def test_vector_store_insert_many():
    db = tempfile.mktemp(suffix=".db")
    store = VectorStore(db_path=db)
    vs = [
        FeatureVector(source_url="a", source_platform="h1", cwe="89", sink="sql", payload="a"),
        FeatureVector(source_url="b", source_platform="h1", cwe="79", sink="xss", payload="b"),
    ]
    assert store.insert_many(vs) == 2
    assert store.count() == 2
    assert len(store.query(cwe="89")) == 1
    assert len(store.query(cwe="79")) == 1
    store.close()


# ── Curl Parser Tests ────────────────────────────────────────────────


def test_parse_get():
    cmd = parse_curl_command('curl "https://example.com/api"')
    assert cmd is not None
    assert cmd.url == "https://example.com/api"
    assert cmd.method == "GET"
    assert cmd.body == ""


def test_parse_post_json():
    cmd = parse_curl_command(
        """curl -X POST https://example.com/api \\
  -H "Content-Type: application/json" \\
  -d '{"key":"value"}'"""
    )
    assert cmd is not None
    assert cmd.method == "POST"
    assert "application/json" in cmd.headers.get("Content-Type", "")
    assert '"key":"value"' in cmd.body


def test_parse_xss_url():
    cmd = parse_curl_command(
        'curl "https://target.com/search?q=<script>alert(1)</script>"'
    )
    assert cmd is not None
    assert "<script>" in cmd.url
    assert "</script>" in cmd.url


def test_parse_multi_line():
    text = """curl \\
  -X PUT \\
  -H 'Authorization: Bearer xyz' \\
  -d 'updated' \\
  https://example.com/resource/42"""
    cmd = parse_curl_command(text)
    assert cmd is not None
    assert cmd.method == "PUT"
    assert "Authorization" in cmd.headers


def test_parse_with_auth():
    cmd = parse_curl_command(
        'curl --user "admin:secret" https://example.com/admin'
    )
    assert cmd is not None
    assert "Authorization" in cmd.headers


def test_extract_curl_commands():
    text = """
### Summary
Test.

### Steps
First request:
curl http://example.com/first

Second:
curl -X POST http://example.com/second -d 'data'
"""
    cmds = extract_curl_commands(text)
    assert len(cmds) == 2


def test_extract_no_curl():
    assert extract_curl_commands("No curl commands here") == []


def test_extract_urls_fallback():
    # Use a domain NOT in the exclusion list
    urls = extract_urls_fallback("Visit https://target.com/page")
    assert len(urls) >= 1
    assert "target.com" in urls[0]


# ── Tech Detector Tests ──────────────────────────────────────────────


def test_detect_from_headers():
    headers = {
        "Server": "nginx/1.18.0",
        "X-Powered-By": "PHP/7.4",
    }
    techs = detect_from_headers(headers)
    assert "nginx" in techs
    assert "php" in techs


def test_detect_from_error_traceback():
    techs = detect_from_error(
        "Traceback (most recent call last):\n  File \"/app/main.py\""
    )
    assert "python" in techs


def test_detect_from_error_nginx():
    techs = detect_from_error("nginx/1.18.0 error log")
    assert "nginx" in techs


def test_detect_all():
    techs = detect_all(
        text="the application uses flask framework",
        url="https://example.com/wp-admin/login.php",
        headers={"Server": "nginx/1.18.0"},
    )
    assert "flask" in techs or "php" in techs or "wordpress" in techs


# ── Report Parser Tests ──────────────────────────────────────────────


def test_extract_sections():
    sections = extract_sections("")
    assert sections.summary == ""


def test_extract_sections_with_headers():
    text = """
### Summary
SQL Injection in search.

### Steps to Reproduce
curl http://target.com/test

### Impact
Full access.
"""
    sections = extract_sections(text, title="Report")
    assert "SQL Injection" in sections.summary
    assert "curl" in sections.steps
    assert "Full access" in sections.impact


def test_extract_cwe():
    assert extract_cwe("CWE-89: SQL Injection", "Title") == "89"
    assert extract_cwe("CWE 79 XSS") == "79"
    assert extract_cwe("No CWE") == ""


def test_parse_report_injection():
    report = """
### Summary
SQL Injection. CWE-89

### Steps to Reproduce
curl -X GET "http://target.com/api?q=test' OR SLEEP(5)--"
"""
    vecs = parse_report(report, source_url="https://h1.com/reports/1")
    assert len(vecs) >= 1
    assert vecs[0].cwe == "89"


def test_parse_report_xss():
    report = """
### Summary
Reflected XSS in search. CWE-79

### Steps to Reproduce
curl "http://target.com/search?q=<script>alert(1)</script>"
"""
    vecs = parse_report(report, source_url="https://h1.com/reports/2", title="XSS")
    assert len(vecs) >= 1
    assert vecs[0].cwe == "79"
    assert "<script>" in vecs[0].payload


def test_parse_report_no_cwe():
    assert len(parse_report("No vulnerability.", source_url="x", title="Test")) == 0


def test_parse_report_ssrf():
    report = """
### Summary
SSRF in upload. CWE-918
curl -X POST http://target.com/upload -d 'url=http://169.254.169.254/'
"""
    vecs = parse_report(report, source_url="https://h1.com/reports/3")
    assert len(vecs) >= 1
    assert vecs[0].cwe == "918"
