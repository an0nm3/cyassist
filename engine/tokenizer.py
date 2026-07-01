"""
CyAssist InMemoryTokenizer — processes raw writeup text in-memory.
Never writes body to disk. Returns structured token sets for DNA extraction.
"""

import re
import hashlib


ENDPOINT_PATTERNS = [
    r"(?:GET|POST|PUT|DELETE|PATCH)\s+(/[a-zA-Z0-9_\-\./{}]+)",
    r"(?:`|')(/[a-zA-Z0-9_\-\./{}]+)(?:`|')",
    r"(?:endpoint|path|route|url)\s*[:=]\s*['\"]([a-zA-Z0-9_\-\./{}]+)['\"]",
    r"(https?://[a-zA-Z0-9\.\-]+(?:\:\d+)?(?:/[a-zA-Z0-9_\-\./{}]+)?)",
]

PARAM_PATTERNS = [
    r"(?:param|parameter|arg|argument)s?\s*[:=]\s*['\"]([a-zA-Z0-9_\-\.\[\]]+)['\"]",
    r"(?:`|')([a-zA-Z0-9_]+_id)(?:`|')",
    r"(?:`|')([a-zA-Z0-9_]+_token)(?:`|')",
    r"(?:`|')(id)(?:`|')",
    r"(\w+\[\])",
]

PAYLOAD_PATTERNS = [
    r"(?:payload|exploit|poc)\s*[:=]\s*['\"]([^'\"]{10,200})['\"]",
    r"(?:```(?:json|bash|curl|http|text)\s*\n)(.*?)(?:```)",
    r"(['\"])(?:%[0-9a-fA-F]{2}|\^|\\x[0-9a-fA-F]{2}|<|>|\"|').{5,100}\1",
]

MUTATION_KEYWORDS = [
    "array_pollution", "prototype_pollution", "mass_assignment",
    "id_enumeration", "parameter_pollution", "race_condition",
    "type_confusion", "null_byte", "unicode_normalization",
    "case_smuggling", "double_encode", "time_manipulation",
]

TECH_KEYWORDS = {
    "graphql": ["graphql", "gql", "graphiql", "apollo", "relay"],
    "rest": ["rest", "restful", "rest api", "json:api"],
    "web3": ["web3", "ethereum", "solidity", "smart contract", "defi"],
    "oauth": ["oauth", "oauth2", "oidc", "openid", "saml"],
    "jwt": ["jwt", "jwk", "json web token"],
    "soap": ["soap", "wsdl", "xml-rpc"],
    "grpc": ["grpc", "protobuf", "protocol buffer"],
    "serverless": ["lambda", "cloud function", "serverless", "faas"],
}

CWE_DETECT = [
    (r"idor|insecure direct|object reference|cwe-639|access control", "CWE-639 (IDOR)"),
    (r"xss|cross.?site script|cwe-79", "CWE-79 (XSS)"),
    (r"sqli|sql injection|cwe-89", "CWE-89 (SQLi)"),
    (r"ssrf|server.?side request forgery|cwe-918", "CWE-918 (SSRF)"),
    (r"rce|remote code exec|cwe-77|cwe-78", "CWE-77/78 (RCE)"),
    (r"auth.?bypass|auth.?bypass|authentication bypass|cwe-287|cwe-288", "CWE-287 (Auth Bypass)"),
    (r"race.?condition|cwe-362", "CWE-362 (Race)"),
    (r"xxe|xml external entity|cwe-611", "CWE-611 (XXE)"),
    (r"csrf|request forgery|cwe-352", "CWE-352 (CSRF)"),
    (r"graphql.*introspection|introspection.*graphql|graphql.*auth", "CWE-200 (GraphQL Introspection)"),
    (r"prototype.?pollution|cwe-1321", "CWE-1321 (Proto Pollution)"),
    (r"path.?traversal|lfi|local file incl|cwe-22", "CWE-22 (Path Traversal)"),
    (r"mass.?assignment|cwe-915", "CWE-915 (Mass Assignment)"),
    (r"deserialization|unserializ|cwe-502", "CWE-502 (Deser)"),
    (r"jwt.*none|alg.*none|jwk.*injection", "CWE-345 (JWT)"),
    (r"open.?redirect|cwe-601", "CWE-601 (Open Redirect)"),
    (r"ssti|template injection|cwe-1336", "CWE-1336 (SSTI)"),
    (r"business.?logic|cwe-840", "CWE-840 (Business Logic)"),
    (r"oauth.*misconfig|redirect_uri|cwe-346", "CWE-346 (OAuth)"),
    (r"replay|timestamp.*bypass|cwe-294", "CWE-294 (Replay)"),
]


class InMemoryTokenizer:
    def __init__(self):
        self._last_result = None

    def tokenize(self, text: str, url: str = "") -> dict:
        text_lower = text.lower()
        result = {
            "body_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            "body_size": len(text),
            "endpoints": self._extract_endpoints(text),
            "parameters": self._extract_parameters(text),
            "payloads": self._extract_payloads(text),
            "cwe_matches": self._detect_cwes(text_lower),
            "mutation_types": self._detect_mutations(text_lower),
            "tech_stack": self._detect_tech(text_lower),
            "urls_referenced": self._extract_urls(text),
            "cve_ids": self._extract_cves(text),
            "severity": self._estimate_severity(text_lower),
        }
        self._last_result = result
        return result

    def _extract_endpoints(self, text: str) -> list[dict]:
        seen = set()
        endpoints = []
        for pat in ENDPOINT_PATTERNS[:3]:
            for m in re.finditer(pat, text, re.IGNORECASE):
                ep = m.group(1).strip()
                if ep not in seen and len(ep) > 2 and " " not in ep:
                    seen.add(ep)
                    endpoints.append({"path": ep, "method": "UNKNOWN"})
        return endpoints[:20]

    def _extract_parameters(self, text: str) -> list[str]:
        seen = set()
        params = []
        for pat in PARAM_PATTERNS:
            for m in re.finditer(pat, text, re.IGNORECASE):
                p = m.group(1).strip()
                if p not in seen and not p.startswith("http") and len(p) < 64:
                    seen.add(p)
                    params.append(p)
        return params[:20]

    def _extract_payloads(self, text: str) -> list[str]:
        payloads = []
        for pat in PAYLOAD_PATTERNS:
            for m in re.finditer(pat, text, re.DOTALL):
                payloads.append(m.group(1).strip()[:300])
        return payloads[:5]

    def _extract_urls(self, text: str) -> list[str]:
        return list(set(re.findall(r"https?://[a-zA-Z0-9\.\-]+(?:\:\d+)?(?:/[a-zA-Z0-9_\-\./~%?&=+#]*)?", text)))[:10]

    def _extract_cves(self, text: str) -> list[str]:
        return list(set(re.findall(r"CVE-\d{4}-\d{4,}", text.upper())))[:10]

    def _detect_cwes(self, text_lower: str) -> list[str]:
        matched = []
        for pat, label in CWE_DETECT:
            if re.search(pat, text_lower):
                if label not in matched:
                    matched.append(label)
        return matched[:5]

    def _detect_mutations(self, text_lower: str) -> list[str]:
        return [kw for kw in MUTATION_KEYWORDS if kw in text_lower]

    def _detect_tech(self, text_lower: str) -> dict[str, list[str]]:
        detected = {}
        for category, keywords in TECH_KEYWORDS.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                detected[category] = found
        return detected

    def _estimate_severity(self, text_lower: str) -> str:
        high = ["critical", "severe", "remote code", "rce", "0-day",
                "zero-day", "unauthenticated", "privilege escalation"]
        medium = ["medium", "sqli", "ssrf", "idor", "xxe", "auth bypass",
                  "authentication bypass", "csrf", "xss"]
        for h in high:
            if h in text_lower:
                return "HIGH"
        for m in medium:
            if m in text_lower:
                return "MEDIUM"
        return "LOW"

    def last_result(self) -> dict:
        return self._last_result
