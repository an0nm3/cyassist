"""Phase A3: Query engine — ranks payload suggestions from VectorStore."""

import time
from typing import Optional

from engine.vector_schema import VectorStore
from api.schema import QueryRequest, QueryResponse, PayloadSuggestion


class PatternQueryEngine:
    """Ranks and returns payload suggestions matching a query.

    Ranking factors:
    1. Exact tech match > partial tech match > no tech match
    2. Higher confidence first
    3. Higher evidence_count first
    4. Sink match as tiebreaker
    """

    def __init__(self, store: VectorStore):
        self.store = store

    def query(self, req: QueryRequest) -> QueryResponse:
        t0 = time.time()

        # Step 1: query by CWE alone (broadest net)
        raw = self.store.query(
            cwe=req.cwe,
            min_confidence=req.min_confidence,
            limit=req.limit * 5,  # fetch extra for ranking
        )

        total_raw = len(raw)

        # Step 2: apply tech filter
        tech_filtered = self._apply_tech_filter(raw, req.tech)

        # Step 3: apply param_type filter
        if req.param_type:
            tech_filtered = [
                v for v in tech_filtered
                if v.param_type == req.param_type
            ]

        # Step 4: apply payload_class filter
        if req.payload_class:
            tech_filtered = [
                v for v in tech_filtered
                if v.payload_class == req.payload_class
            ]

        # Step 5: rank and dedup by payload
        ranked = self._rank(tech_filtered, req)
        suggestions = []
        seen_payloads = set()
        for v in ranked:
            if v.payload not in seen_payloads:
                seen_payloads.add(v.payload)
                suggestions.append(PayloadSuggestion(
                    payload_class=v.payload_class,
                    payload=v.payload,
                    response_shape=v.response_shape,
                    confidence=v.confidence,
                    evidence_count=v.evidence_count,
                ))
            if len(suggestions) >= req.limit:
                break

        elapsed = (time.time() - t0) * 1000

        return QueryResponse(
            suggestions=suggestions,
            total_vectors=total_raw,
            query_time_ms=round(elapsed, 2),
        )

    # ── Ranking Logic ──────────────────────────────────────────────

    def _apply_tech_filter(
        self,
        vectors: list,
        query_tech: list[str],
    ) -> list:
        """Filter vectors by tech stack match.

        Priority: exact tech list match > subset match > any overlap > no match.
        """
        if not query_tech:
            return vectors

        query_tech_set = set(t.lower() for t in query_tech)

        exact = []
        subset = []
        overlap = []
        no_match = []

        for v in vectors:
            v_tech_set = set(t.lower() for t in v.tech)
            if v_tech_set == query_tech_set:
                exact.append(v)
            elif v_tech_set and v_tech_set.issubset(query_tech_set):
                subset.append(v)
            elif v_tech_set & query_tech_set:
                overlap.append(v)
            else:
                no_match.append(v)

        return exact + subset + overlap + no_match

    def _rank(self, vectors: list, req: QueryRequest) -> list:
        """Rank vectors by confidence, evidence_count, sink match."""
        def score(v):
            s = v.confidence * 100
            s += min(v.evidence_count, 50) * 0.5
            if req.sink and v.sink == req.sink:
                s += 10
            if req.param_type and v.param_type == req.param_type:
                s += 5
            return s

        return sorted(vectors, key=score, reverse=True)
