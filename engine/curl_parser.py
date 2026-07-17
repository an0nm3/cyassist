"""Phase A2: Curl command parser — extract structured HTTP request data.

Given the text of a bug bounty report, finds and parses curl commands.
Handles the wide variance in curl formatting across H1 reports.

Capabilities:
- Extract curl commands via regex from report body text
- Parse URL, HTTP method, headers, request body, cookies
- Handle -X, -d, -H, -b, -v, --data, --header, --cookie flags
- Handle multi-line curl commands (backslash continuation)
- Handle inline single-line curl commands
- Fallback: if no curl, try raw URL extraction
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse, parse_qs


@dataclass
class ParsedRequest:
    """A single HTTP request parsed from a curl command in a report."""
    raw: str  # the original curl command
    url: str = ""
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    body: str = ""
    cookies: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    path: str = ""
    host: str = ""


# Regex patterns for curl extraction
_CURL_RE = re.compile(
    r'(?:^|\n)\s*(?:```)?\s*\$?\s*(curl\b.*?)(?=\n```|\n(?:\w|\s*$)|\Z)',
    re.DOTALL | re.IGNORECASE,
)

_SINGLE_LINE_CURL = re.compile(
    r'\$?\s*(curl\b[^\n]+)',
    re.IGNORECASE,
)

# Flag patterns
_FLAG_X = re.compile(r'-X\s+(\w+)', re.IGNORECASE)
_FLAG_D = re.compile(r'-d\s+(?:"([^"]*)"|\'([^\']*)\'|(\S+))')
_FLAG_DATA = re.compile(r'--data(?:-raw)?(?:=|\s+)(?:"([^"]*)"|\'([^\']*)\'|(\S+))')
_FLAG_H = re.compile(r'-H\s+(?:"([^"]*)"|\'([^\']*)\')')
_FLAG_HEADER = re.compile(r'--header(?:=|\s+)(?:"([^"]*)"|\'([^\']*)\')')
_FLAG_B = re.compile(r'-b\s+(?:"([^"]*)"|\'([^\']*)\'|(\S+))')
_FLAG_COOKIE = re.compile(r'--cookie(?:=|\s+)(?:"([^"]*)"|\'([^\']*)\')')
_FLAG_V = re.compile(r'-[vV]|--verbose')

# Auth pattern
_AUTH_BASIC = re.compile(r'--user\s+(?:"([^"]+)"|\'([^\']+)\')')

# URL extraction — matches the first URL-like token in a curl command
# First tries to match a quoted URL (with angle brackets for payloads like XSS),
# then falls back to unquoted URL matching.
_QUOTED_URL_RE = re.compile(
    r"""(?:https?://[^\s"']+)""",
    re.IGNORECASE,
)

_URL_RE = re.compile(
    r"(?:https?://[^\s'\"<>\]\)]+)",
    re.IGNORECASE,
)


def _normalize_method(m: str) -> str:
    return m.upper().strip() if m else "GET"


def _normalize_url(url_str: str) -> str:
    """Clean URL string (strip trailing punctuation that's not part of URL)."""
    url_str = url_str.strip().rstrip(".,;:!?)'\"")
    # Remove surrounding quotes
    url_str = url_str.strip("'\"")
    return url_str


def _extract_url(text: str) -> Optional[str]:
    """Extract the first URL from text.

    Strategy: try quoted URL first (captures XSS payloads with angle brackets),
    then fall back to the restrictive URL pattern (safe for inline text).
    """
    # Try quoted URL first — look for URL inside quotes (covers XSS payloads)
    quote_m = _QUOTED_URL_RE.search(text)
    if quote_m:
        url = quote_m.group(0)
        # Make sure the URL isn't truncated by an unclosed quote
        if url.count('"') % 2 != 0:
            # Remove trailing quote if unbalanced
            url = url.rstrip('"')
        return _normalize_url(url)
    m = _URL_RE.search(text)
    if m:
        return _normalize_url(m.group(0))
    return None


def _flag_value(match) -> str:
    """Extract value from a regex match that may have multiple capture groups."""
    for g in match.groups():
        if g is not None:
            return g
    return ""


def parse_curl_command(curl_text: str) -> Optional[ParsedRequest]:
    """Parse a single curl command string into a ParsedRequest.

    Handles:
      curl -X POST https://example.com/api/login -d 'user=admin'
      curl https://example.com/api/data -H 'Authorization: Bearer xyz'
      curl \\
        -X PUT \\
        -H 'Content-Type: application/json' \\
        -d '{"key":"value"}' \\
        https://example.com/api/update
    """
    # Normalize line continuations
    text = curl_text.replace("\\\n", " ").replace("\\\r\n", " ").strip()

    # Remove common prefixes
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    text = re.sub(r'^\$\s*', '', text)
    text = text.strip()

    if not text.lower().startswith("curl"):
        return None

    p = ParsedRequest(raw=curl_text.strip())

    # Extract URL
    url = _extract_url(text)
    if not url:
        return None
    p.url = url

    # Parse URL components
    parsed = urlparse(url)
    p.path = parsed.path or "/"
    p.host = parsed.netloc
    p.params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()}

    # Extract method from -X flag
    x_match = _FLAG_X.search(text)
    if x_match:
        p.method = _normalize_method(x_match.group(1))
    # Heuristic: if -d present but no -X, method is POST
    elif _FLAG_D.search(text) or _FLAG_DATA.search(text):
        p.method = "POST"

    # Extract body from -d / --data
    body = ""
    d_match = _FLAG_D.search(text)
    if d_match:
        body = _flag_value(d_match)
    data_match = _FLAG_DATA.search(text)
    if data_match:
        body = _flag_value(data_match)
    if body:
        p.body = body

    # Extract headers from -H / --header
    for h_match in _FLAG_H.finditer(text):
        header_line = _flag_value(h_match)
        if ":" in header_line:
            key, val = header_line.split(":", 1)
            p.headers[key.strip()] = val.strip()

    for h_match in _FLAG_HEADER.finditer(text):
        header_line = _flag_value(h_match)
        if ":" in header_line:
            key, val = header_line.split(":", 1)
            p.headers[key.strip()] = val.strip()

    # Extract cookies from -b / --cookie
    for c_match in _FLAG_B.finditer(text):
        cookie_str = _flag_value(c_match)
        for pair in cookie_str.split(";"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                p.cookies[k.strip()] = v.strip()

    for c_match in _FLAG_COOKIE.finditer(text):
        cookie_str = _flag_value(c_match)
        for pair in cookie_str.split(";"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                p.cookies[k.strip()] = v.strip()

    # Extract auth from --user
    auth_match = _AUTH_BASIC.search(text)
    if auth_match:
        p.headers["Authorization"] = f"Basic {_flag_value(auth_match)}"

    # Detect verbose mode
    if _FLAG_V.search(text):
        p.headers.setdefault("_verbose", "true")

    return p


def extract_curl_commands(text: str) -> list[ParsedRequest]:
    """Extract all curl commands from a block of text (e.g., a report body).

    Tries multi-line first, then falls back to single-line extraction.
    """
    results = []

    # Try multi-line extraction
    for m in _CURL_RE.finditer(text):
        curl_text = m.group(1).strip()
        parsed = parse_curl_command(curl_text)
        if parsed:
            results.append(parsed)

    # Try single-line extraction (catches inline curls in paragraphs)
    if not results:
        for m in _SINGLE_LINE_CURL.finditer(text):
            parsed = parse_curl_command(m.group(1))
            if parsed:
                results.append(parsed)

    return results


def extract_urls_fallback(text: str) -> list[str]:
    """Fallback: if no curl commands found, extract raw URLs from text."""
    urls = []
    for m in _URL_RE.finditer(text):
        url = _normalize_url(m.group(0))
        # Filter out common non-target URLs
        parsed = urlparse(url)
        if parsed.netloc and parsed.netloc not in (
            "example.com", "hackerone.com", "github.com",
            "youtube.com", "twitter.com", "x.com",
        ):
            urls.append(url)
    return list(set(urls))
