"""Phase A3: Pattern Query API server.

Dual transport:
1. HTTP (default: localhost:9876) — for full system integration
2. JSON over stdin/stdout — for one-shot CLI from Rudra

Endpoints:
  POST /query  — pattern query
  GET  /health — health check
  GET  /stats  — store statistics
"""

import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
from urllib.parse import urlparse

from engine.vector_schema import VectorStore, FeatureVector
from api.schema import QueryRequest, QueryResponse
from api.query_engine import PatternQueryEngine


def _get_store() -> VectorStore:
    db_path = os.environ.get("CYASSIST_DB", "")
    return VectorStore(db_path=db_path)


# ── HTTP Handler ─────────────────────────────────────────────────────


class QueryHandler(BaseHTTPRequestHandler):
    """HTTP handler for Pattern Query API."""

    store: Optional[VectorStore] = None
    engine: Optional[PatternQueryEngine] = None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json_response({"status": "ok", "timestamp": time.time()})
        elif parsed.path == "/stats":
            self._handle_stats()
        else:
            self._json_response({"error": "not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/query":
            self._handle_query()
        elif parsed.path == "/feedback":
            self._handle_feedback()
        else:
            self._json_response({"error": "not found"}, status=404)

    # ── Handlers ───────────────────────────────────────────────────

    def _handle_stats(self):
        store = self._get_store()
        try:
            top_cwes = store.top_cwes(5)
            self._json_response({
                "total_vectors": store.count(),
                "db_size_bytes": store.size_bytes(),
                "top_cwes": [{"cwe": c, "count": n} for c, n in top_cwes],
            })
        except Exception as e:
            self._json_response({"error": str(e)}, status=500)

    def _handle_query(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            self._json_response({"error": "empty body"}, status=400)
            return
        body = self.rfile.read(length).decode()
        req = QueryRequest.from_json(body)
        if req is None:
            self._json_response({"error": "invalid JSON"}, status=400)
            return
        try:
            resp = self._get_engine().query(req)
            self._json_response(resp.to_dict())
        except Exception as e:
            self._json_response({"error": str(e)}, status=500)

    def _handle_feedback(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            self._json_response({"error": "empty body"}, status=400)
            return
        body = self.rfile.read(length).decode()
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response({"error": "invalid JSON"}, status=400)
            return

        session_id = data.get("rudra_session_id", "")
        vector = FeatureVector(
            source_url=data.get("source_url", ""),
            source_platform="rudra_feedback",
            cwe=data.get("cwe", ""),
            tech=data.get("tech", []),
            sink=data.get("sink", ""),
            payload_class=data.get("payload_class", ""),
            payload=data.get("payload", ""),
            confidence=float(data.get("confidence", 0.5)),
            accepted=bool(data.get("accepted", False)),
            dup_of=data.get("dup_of", ""),
            informative=bool(data.get("informative", False)),
            reward=data.get("reward", ""),
            notes=data.get("notes", ""),
        )
        store = self._get_store()
        result = store.insert_pending(vector, session_id=session_id)
        if result == "accepted":
            self._json_response({"status": "accepted"})
        elif result == "duplicate":
            self._json_response({"status": "duplicate", "message": "already exists"})
        else:
            self._json_response({"error": "storage error"}, status=500)

    # ── Helpers ────────────────────────────────────────────────────

    def _get_store(self) -> VectorStore:
        if QueryHandler.store is None:
            QueryHandler.store = _get_store()
        return QueryHandler.store

    def _get_engine(self) -> PatternQueryEngine:
        if QueryHandler.engine is None:
            QueryHandler.engine = PatternQueryEngine(self._get_store())
        return QueryHandler.engine

    def _json_response(self, data: dict, status: int = 200):
        msg = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)

    def log_message(self, fmt, *args):
        """Suppress default HTTP log to stderr unless VERBOSE is set."""
        if os.environ.get("CYASSIST_VERBOSE"):
            super().log_message(fmt, *args)


# ── CLI / Stdio Transport ────────────────────────────────────────────


def cli_query():
    """Read JSON query from stdin, write JSON response to stdout.

    Usage:
      echo '{"cwe":"89","tech":["python","flask"]}' | python3 -m api.server --stdio
    """
    raw = sys.stdin.read()
    req = QueryRequest.from_json(raw)
    if req is None:
        print(QueryResponse.error_response("invalid JSON input").to_json())
        return 1

    store = _get_store()
    engine = PatternQueryEngine(store)
    resp = engine.query(req)
    print(resp.to_json())
    return 0


# ── Main ──────────────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Cyassist Pattern Query API")
    parser.add_argument("--stdio", action="store_true", help="JSON over stdin/stdout mode")
    parser.add_argument("--port", type=int, default=int(os.environ.get("CYASSIST_PORT", 9876)),
                        help="HTTP server port (env: CYASSIST_PORT)")
    parser.add_argument("--host", type=str, default=os.environ.get("CYASSIST_HOST", "127.0.0.1"),
                        help="HTTP server host (env: CYASSIST_HOST)")
    parser.add_argument("--db", type=str, default=os.environ.get("CYASSIST_DB", ""),
                        help="SQLite database path (env: CYASSIST_DB)")

    args = parser.parse_args()

    if args.db:
        os.environ["CYASSIST_DB"] = args.db

    if args.stdio:
        return cli_query()

    # HTTP mode
    store = _get_store()
    QueryHandler.store = store
    QueryHandler.engine = PatternQueryEngine(store)

    server = HTTPServer((args.host, args.port), QueryHandler)
    print(f"Cyassist Pattern Query API running on http://{args.host}:{args.port}")
    print(f"  Vectors in store: {store.count()}")
    print(f"  Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
