"""Phase A2: H1 report parser — extract structured data from disclosed reports.

Takes a report's text (Summary, Steps to Reproduce, Impact sections)
and extracts: CWE, tech stack, payload, endpoint, HTTP method, parameters,
response shape.

Output is a list of FeatureVector candidates ready for VectorStore insertion.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Optional

from .curl_parser import extract_curl_commands, extract_urls_fallback, parse_curl_command
from .tech_detector import detect_all, detect_from_error, detect_from_url, detect_from_keywords
from .vector_schema import FeatureVector, payload_hash, calculate_confidence


# ── Section extraction ─────────────────────────────────────────────────

_SECTION_RE = re.compile(
    r"#{1,3}\s*(Summary|Impact|Steps?\s*(?:to\s+)?Reproduce|"
    r"Supporting\s*Material|References|Vulnerability\s*Type|"
    r"Description|How\s*to\s*reproduce|PoC|Proof\s*of\s*Concept)",
    re.IGNORECASE,
)

_CWE_TITLE_RE = re.compile(
    r"CWE[-:#;]?\s*(\d{2,4})", re.IGNORECASE,
)

_CWE_TAG_RE = re.compile(
    r"(?:CWE-|cwe[:_])?(\d{2,4})",
)

_PAYLOAD_CLASS_RE = {
    "time_based": re.compile(
        r"\b(SLEEP|WAITFOR|BENCHMARK|pg_sleep|sleep\(|"
        r"time-based|blind\s*time|timing|delay)\b",
        re.IGNORECASE,
    ),
    "error_based": re.compile(
        r"\berror\b.*\b(sql|database|mysql|mssql|oracle|postgres)\b|"
        r"\b(error|sqli|sql error)\b",
        re.IGNORECASE,
    ),
    "union_based": re.compile(
        r"\bUNION\b.*\bSELECT\b", re.IGNORECASE,
    ),
    "boolean_blind": re.compile(
        r"\b(boolean|blind|true|false|content.change|condition)\b",
        re.IGNORECASE,
    ),
    "reflected": re.compile(
        r"\b(reflected|xss|alert|prompt|<script|<img)\b",
        re.IGNORECASE,
    ),
    "stored": re.compile(
        r"\b(stored|persistent|saved)\b.*\b(xss|script)\b|"
        r"\b(xss|script)\b.*\b(stored|persistent|saved)\b",
        re.IGNORECASE,
    ),
    "ssrf_oob": re.compile(
        r"\b(ssrf|server.side.request|oob|out.of.band|"
        r"external.interaction|callback|webhook)\b",
        re.IGNORECASE,
    ),
    "idor": re.compile(
        r"\b(idor|insecure.direct.object|object.reference|"
        r"id.enumeration|access.control)\b",
        re.IGNORECASE,
    ),
    "command_injection": re.compile(
        r"\b(rce|command|code.exec|shell|remote.code|"
        r"cmd.injection|whoami|id\b)",
        re.IGNORECASE,
    ),
    "open_redirect": re.compile(
        r"\b(open.redirect|url.redirect|unvalidated.redirect)\b",
        re.IGNORECASE,
    ),
    "prototype_pollution": re.compile(
        r"\b(prototype.pollution|__proto__|merge.pollute)\b",
        re.IGNORECASE,
    ),
}


# ── Report Sections ────────────────────────────────────────────────────


@dataclass
class ReportSections:
    """Extracted sections from a bug bounty report."""
    title: str = ""
    summary: str = ""
    steps: str = ""
    impact: str = ""
    supporting: str = ""
    raw_text: str = ""


def extract_sections(text: str, title: str = "") -> ReportSections:
    """Split report text into sections by markdown headers."""
    sections = ReportSections(raw_text=text, title=title)
    if not text:
        return sections

    # Find all section headers and their positions
    matches = list(_SECTION_RE.finditer(text))
    if not matches:
        sections.summary = text  # no headers, treat whole text as summary
        return sections

    for i, m in enumerate(matches):
        section_name = m.group(1).lower().strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        if "summary" in section_name or "description" in section_name:
            sections.summary = content
        elif "reproduce" in section_name or "poc" in section_name or "proof" in section_name:
            sections.steps = content
        elif "impact" in section_name:
            sections.impact = content
        elif "material" in section_name or "reference" in section_name:
            sections.supporting = content

    return sections


# ── CWE Extraction ─────────────────────────────────────────────────────


def extract_cwe(text: str, title: str = "") -> str:
    """Extract CWE ID from report text or title.

    Priority:
    1. Explicit "CWE-XX" in tags/metadata
    2. "CWE-XX" in title
    3. "CWE-XX" in body text
    4. Implied from vulnerability type
    """
    # Check title first (most reliable)
    if title:
        m = _CWE_TITLE_RE.search(title)
        if m:
            return m.group(1)

    # Check body for explicit CWE mentions
    m = _CWE_TITLE_RE.search(text)
    if m:
        return m.group(1)

    return ""


# ── Payload Class Classification ───────────────────────────────────────


def classify_payload_class(text: str) -> str:
    """Classify the vulnerability type based on report text.

    Returns: "time_based", "error_based", "union_based", "reflected",
             "ssrf_oob", "idor", "command_injection", etc.
    """
    scores = {}
    for cls_name, pattern in _PAYLOAD_CLASS_RE.items():
        matches = pattern.findall(text)
        if matches:
            scores[cls_name] = len(matches)

    if scores:
        return max(scores, key=scores.get)
    return "unknown"


# ── Response Shape ─────────────────────────────────────────────────────


def classify_response_shape(text: str) -> str:
    """Classify how the vulnerability was confirmed.

    Returns: "timing_delta", "error_message", "content_reflection",
             "content_change", "status_code_change", "oob_interaction"
    """
    text_lower = text.lower()

    if any(w in text_lower for w in ["timing", "delay", "sleep", "slow", "timeout", "latency"]):
        return "timing_delta"
    if any(w in text_lower for w in ["error", "exception", "stack trace", "warning:"]):
        return "error_message"
    if any(w in text_lower for w in ["reflected", "injected", "appeared in", "displayed"]):
        return "content_reflection"
    if any(w in text_lower for w in ["different content", "status code", "200", "403", "500"]):
        return "status_code_change"
    if any(w in text_lower for w in ["callback", "webhook", "oob", "dns", "external"]):
        return "oob_interaction"
    if any(w in text_lower for w in ["unauthorized", "access", "other user"]):
        return "access_change"

    return "content_change"


# ── Full Report Parse ──────────────────────────────────────────────────


def parse_report(
    text: str,
    source_url: str = "",
    source_platform: str = "h1",
    title: str = "",
) -> list[FeatureVector]:
    """Parse a bug bounty report into feature vectors.

    Returns a list of FeatureVector candidates (usually 1-3 per report).

    Processing pipeline:
    1. Extract sections (Summary, Steps, Impact)
    2. Extract curl commands from all sections
    3. Detect tech stack from: headers (in curl -v), URL patterns, error messages, keywords
    4. Extract CWE from title/body
    5. Classify payload and response shape
    6. Build feature vectors
    """
    vectors = []

    # Step 1: Extract sections
    sections = extract_sections(text, title)
    all_text = sections.raw_text

    # Step 2: Extract curl commands
    curl_cmds = extract_curl_commands(all_text)
    urls = extract_urls_fallback(all_text) if not curl_cmds else []

    # Step 3: Extract CWE
    cwe = extract_cwe(all_text, title)
    if not cwe:
        # No CWE found — cannot build useful vector
        return []

    # Step 4: Detect tech stack from all sources
    techs = set()

    # From curl response headers (if curl -v is used)
    for cmd in curl_cmds:
        if cmd.headers:
            from .tech_detector import detect_from_headers
            techs.update(detect_from_headers(cmd.headers))

    # From URLs
    for u in urls:
        techs.update(detect_from_url(u))
    for cmd in curl_cmds:
        techs.update(detect_from_url(cmd.url))

    # From error messages and keywords in text
    techs.update(detect_from_error(all_text))
    techs.update(detect_from_keywords(all_text))

    # Step 5: For each curl command, build a feature vector
    if curl_cmds:
        for cmd in curl_cmds:
            payload_class = classify_payload_class(all_text)
            response_shape = classify_response_shape(all_text)

            # Determine param type from request body or URL params
            param_type = _guess_param_type(cmd.body, cmd.params)

            # Find the payload — it's either in the body, URL, or headers
            payload = cmd.body or next(
                (v for v in cmd.params.values() if len(str(v)) > 3),
                "",
            )

            if payload:
                vec = FeatureVector(
                    source_url=source_url,
                    source_platform=source_platform,
                    report_title=title,
                    cwe=cwe,
                    tech=sorted(techs) if techs else [],
                    sink=_guess_sink(cmd, sections, all_text),
                    param_type=param_type,
                    payload_class=payload_class,
                    payload=payload,
                    response_shape=response_shape,
                    auth_required=_guess_auth(cmd.headers, all_text),
                    confidence=calculate_confidence(
                        evidence_count=1,
                        has_cwe=bool(cwe),
                        has_payload=bool(payload),
                        has_tech=bool(techs),
                        has_sink=True,
                    ),
                )
                vectors.append(vec)

    # Step 6: If no curl commands but URLs exist, build from URL + text features
    if not vectors and urls:
        payload_class = classify_payload_class(all_text)
        response_shape = classify_response_shape(all_text)

        vec = FeatureVector(
            source_url=source_url,
            source_platform=source_platform,
            report_title=title,
            cwe=cwe,
            tech=sorted(techs) if techs else [],
            sink=_guess_sink_from_text(all_text),
            param_type=param_type,
            payload_class=payload_class,
            payload=f"URL: {urls[0]}" if urls else "",
            response_shape=response_shape,
            confidence=calculate_confidence(
                evidence_count=1,
                has_cwe=bool(cwe),
                has_payload=bool(urls),
                has_tech=bool(techs),
                has_sink=True,
            ),
        )
        vectors.append(vec)

    return vectors


# ── Internal Helpers ────────────────────────────────────────────────────


def _guess_param_type(body: str, params: dict) -> str:
    """Guess the parameter type from request body and URL params."""
    if not body and not params:
        return ""

    # Try to parse as JSON
    if body:
        try:
            json.loads(body)
            return "json"
        except (json.JSONDecodeError, ValueError):
            pass

    # Check for URL-encoded form data
    if body and ("=" in body and "&" in body):
        return "form"
    if body and "=" in body:
        return "form_single"

    # URL path params
    if params:
        # Check if numeric
        numeric = sum(1 for v in params.values() if str(v).isdigit())
        if numeric == len(params) and len(params) > 0:
            return "integer"
        return "string"

    if body:
        return "string"

    return ""


def _guess_sink(cmd, sections, all_text: str) -> str:
    """Guess the vulnerable sink/function from context."""
    # Check for SQLi indicators
    text_lower = all_text.lower()
    if "sql" in text_lower or "database" in text_lower or "injection" in text_lower:
        if cmd.method in ("POST", "PUT"):
            return "sql_query_execute"
        return "sql_query"

    if "xss" in text_lower or "cross-site" in text_lower:
        return "render_template"

    if "ssrf" in text_lower or "server-side" in text_lower:
        if cmd.method == "POST":
            return "http_fetch_post"
        return "http_fetch"

    if "idor" in text_lower or "insecure direct" in text_lower:
        return "direct_object_reference"

    if "rce" in text_lower or "command" in text_lower or "exec" in text_lower:
        return "shell_exec"

    if "open redirect" in text_lower or "url redirect" in text_lower:
        return "redirect_handler"

    if "template" in text_lower or "ssti" in text_lower:
        return "template_engine"

    # Fallback: guess from HTTP method
    method_map = {"GET": "api_fetch", "POST": "api_submit", "PUT": "api_update", "DELETE": "api_delete"}
    return method_map.get(cmd.method, "api_fetch")


def _guess_sink_from_text(text: str) -> str:
    """Guess sink from text when no curl command is available."""
    text_lower = text.lower()
    if "sql" in text_lower:
        return "sql_query"
    if "xss" in text_lower:
        return "render_template"
    if "ssrf" in text_lower:
        return "http_fetch"
    if "idor" in text_lower:
        return "direct_object_reference"
    if "rce" in text_lower:
        return "shell_exec"
    return "api_endpoint"


def _guess_auth(headers: dict, text: str) -> bool:
    """Guess if the endpoint requires authentication."""
    # Check for auth headers in curl
    if any("auth" in k.lower() or "token" in k.lower() or "cookie" in k.lower() for k in headers):
        return True

    # Check for auth keywords in text
    text_lower = text.lower()
    if any(w in text_lower for w in [
        "login", "authenticated", "session", "bearer",
        "authorization", "authentication", "logged in",
        "token", "cookie",
    ]):
        return True

    return False
