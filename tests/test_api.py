"""Tests for Phase A3 — Pattern Query API (schema + query engine + server)."""

import json, tempfile, time

from engine.vector_schema import VectorStore, FeatureVector
from api.schema import QueryRequest, QueryResponse
from api.query_engine import PatternQueryEngine


def _seeded_store():
    """Create a temp store with sample vectors."""
    db = tempfile.mktemp(suffix=".db")
    store = VectorStore(db_path=db)
    store.insert_many([
        FeatureVector(source_url="h1://1", source_platform="h1", cwe="89",
                      tech=["python", "flask", "mysql"], sink="cursor.execute",
                      payload_class="time_based", payload="1' OR SLEEP(5)--",
                      response_shape="timing_delta", confidence=0.92, evidence_count=34),
        FeatureVector(source_url="h1://2", source_platform="h1", cwe="89",
                      tech=["python", "flask", "mysql"], sink="cursor.execute",
                      payload_class="error_based", payload="1' AND 1=1--",
                      response_shape="error_message", confidence=0.78, evidence_count=18),
        FeatureVector(source_url="h1://3", source_platform="h1", cwe="89",
                      tech=["php", "wordpress", "mysql"], sink="sql_query",
                      payload_class="error_based", payload="1' UNION SELECT 1,2,3--",
                      response_shape="content_change", confidence=0.80, evidence_count=22),
        FeatureVector(source_url="h1://4", source_platform="h1", cwe="79",
                      tech=["python", "flask"], sink="render_template",
                      payload_class="reflected", payload="<script>alert(1)</script>",
                      response_shape="content_reflection", confidence=0.88, evidence_count=45),
        FeatureVector(source_url="h1://5", source_platform="h1", cwe="918",
                      tech=["python", "flask"], sink="http_fetch",
                      payload_class="ssrf_oob", payload="http://169.254.169.254/",
                      response_shape="oob_interaction", confidence=0.75, evidence_count=8),
    ])
    return store


# ── Schema Tests ────────────────────────────────────────────────────


def test_query_request_defaults():
    req = QueryRequest()
    assert req.cwe == ""
    assert req.tech == []
    assert req.limit == 5


def test_query_request_from_dict():
    req = QueryRequest.from_dict({"cwe": "89", "tech": ["python"], "limit": 3})
    assert req.cwe == "89"
    assert req.tech == ["python"]
    assert req.limit == 3


def test_query_request_from_json():
    req = QueryRequest.from_json('{"cwe":"79","tech":["flask"]}')
    assert req.cwe == "79"
    assert req.tech == ["flask"]


def test_query_request_from_json_invalid():
    assert QueryRequest.from_json("not json") is None
    assert QueryRequest.from_json("") is None


def test_payload_suggestion_to_dict():
    from api.schema import PayloadSuggestion
    s = PayloadSuggestion(payload_class="time_based", payload="SLEEP(5)",
                          response_shape="timing_delta", confidence=0.9, evidence_count=10)
    d = s.to_dict()
    assert d["payload_class"] == "time_based"
    assert d["confidence"] == 0.9


def test_query_response_to_dict():
    from api.schema import PayloadSuggestion
    resp = QueryResponse(
        suggestions=[
            PayloadSuggestion("time_based", "SLEEP(5)", "timing_delta", 0.9, 10),
        ],
        total_vectors=10,
        query_time_ms=3.5,
    )
    d = resp.to_dict()
    assert len(d["suggestions"]) == 1
    assert d["total_vectors"] == 10


def test_query_response_error():
    resp = QueryResponse.error_response("something went wrong")
    assert resp.error == "something went wrong"
    assert resp.suggestions == []


def test_query_response_to_json():
    resp = QueryResponse.error_response("fail")
    j = resp.to_json()
    assert "fail" in j
    assert json.loads(j)["error"] == "fail"


# ── Query Engine Tests ──────────────────────────────────────────────


def test_query_by_cwe():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(QueryRequest(cwe="89"))
    assert resp.total_vectors >= 2
    assert len(resp.suggestions) > 0
    assert all(s.payload_class != "" for s in resp.suggestions)
    store.close()


def test_query_returns_time_ms():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(QueryRequest(cwe="89"))
    assert resp.query_time_ms > 0
    store.close()


def test_query_empty_results():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(QueryRequest(cwe="999"))
    assert resp.suggestions == []
    assert resp.total_vectors == 0
    store.close()


def test_query_tech_filter():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    # PHP-specific query should get PHP result first
    resp = engine.query(QueryRequest(cwe="89", tech=["php", "wordpress"]))
    assert resp.total_vectors >= 1
    store.close()


def test_query_sink_filter():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(QueryRequest(cwe="79", sink="render_template"))
    assert len(resp.suggestions) >= 1
    store.close()


def test_query_limit():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(QueryRequest(cwe="89", limit=1))
    assert len(resp.suggestions) == 1
    store.close()


def test_query_dedup_by_payload():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    # Add duplicate payload
    store.insert(FeatureVector(source_url="h1://dup", source_platform="h1", cwe="89",
                               tech=["python"], sink="cursor.execute",
                               payload_class="time_based", payload="1' OR SLEEP(5)--",
                               response_shape="timing_delta", confidence=0.5, evidence_count=1))
    resp = engine.query(QueryRequest(cwe="89", limit=10))
    # Same payload should only appear once
    seen = [s.payload for s in resp.suggestions]
    assert len(seen) == len(set(seen)), f"duplicate payloads: {seen}"
    store.close()


def test_query_payload_class_filter():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(QueryRequest(cwe="89", payload_class="time_based"))
    assert len(resp.suggestions) >= 1
    assert all(s.payload_class == "time_based" for s in resp.suggestions)
    store.close()


def test_query_min_confidence():
    store = _seeded_store()
    engine = PatternQueryEngine(store)
    # High confidence should filter out lower ones
    resp = engine.query(QueryRequest(cwe="89", min_confidence=0.9))
    assert all(s.confidence >= 0.9 for s in resp.suggestions)
    store.close()
