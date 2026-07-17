"""Phase A3: API schema — request/response validation for Pattern Query API."""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


# ── Request ──────────────────────────────────────────────────────────


@dataclass
class QueryRequest:
    """Incoming query from Rudra.

    All fields are optional — server returns best guesses based on
    whatever context is available.
    """
    cwe: str = ""
    tech: list[str] = field(default_factory=list)
    sink: str = ""
    param_type: str = ""
    payload_class: str = ""  # e.g., "time_based", "error_based"
    min_confidence: float = 0.0
    limit: int = 5

    @classmethod
    def from_dict(cls, d: dict) -> "QueryRequest":
        return cls(
            cwe=str(d.get("cwe", "")),
            tech=list(d.get("tech", [])),
            sink=str(d.get("sink", "")),
            param_type=str(d.get("param_type", "")),
            payload_class=str(d.get("payload_class", "")),
            min_confidence=float(d.get("min_confidence", 0.0)),
            limit=int(d.get("limit", 5)),
        )

    @classmethod
    def from_json(cls, text: str) -> Optional["QueryRequest"]:
        try:
            d = json.loads(text)
            return cls.from_dict(d)
        except (json.JSONDecodeError, ValueError, TypeError):
            return None


# ── Response ─────────────────────────────────────────────────────────


@dataclass
class PayloadSuggestion:
    """A single payload recommendation, ranked by relevance."""
    payload_class: str
    payload: str
    response_shape: str
    confidence: float
    evidence_count: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class QueryResponse:
    """Response from Pattern Query API to Rudra."""
    suggestions: list[PayloadSuggestion] = field(default_factory=list)
    total_vectors: int = 0
    query_time_ms: float = 0.0
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "suggestions": [s.to_dict() for s in self.suggestions],
            "total_vectors": self.total_vectors,
            "query_time_ms": self.query_time_ms,
            "error": self.error,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def error_response(cls, msg: str) -> "QueryResponse":
        return cls(error=msg)
