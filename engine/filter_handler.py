"""
CyAssist FilterHandler — filter findings by category (Web2 API, GraphQL, Web3, etc).
"""

import re


CATEGORY_RULES = {
    "web2_api": {
        "cwe_patterns": [
            "cwe-639", "cwe-79", "cwe-89", "cwe-918", "cwe-287",
            "cwe-352", "cwe-611", "cwe-22", "cwe-915", "cwe-601",
        ],
        "tech_tags": ["rest", "oauth", "jwt", "soap"],
        "keywords": [
            "api", "rest", "json", "http", "endpoint", "authentication",
            "authorization", "access token", "bearer",
        ],
    },
    "graphql": {
        "cwe_patterns": ["cwe-200", "cwe-284"],
        "tech_tags": ["graphql"],
        "keywords": [
            "graphql", "gql", "graphiql", "introspection", "query",
            "mutation", "schema", "resolver", "apollo",
        ],
    },
    "web3_defi": {
        "cwe_patterns": ["cwe-754", "cwe-682", "cwe-327"],
        "tech_tags": ["web3"],
        "keywords": [
            "smart contract", "solidity", "ethereum", "defi", "web3",
            "reentrancy", "flash loan", "oracle", "liquidity",
            "token", "approve", "transferfrom", "uniswap",
        ],
    },
    "mobile": {
        "cwe_patterns": [],
        "tech_tags": [],
        "keywords": [
            "android", "ios", "mobile", "apk", "ipa", "deeplink",
            "webview", "jailbreak", "root detection",
        ],
    },
    "cloud_infra": {
        "cwe_patterns": ["cwe-200", "cwe-284"],
        "tech_tags": ["serverless"],
        "keywords": [
            "s3", "bucket", "aws", "azure", "gcp", "cloud",
            "iam", "lambda", "cloudfront", "k8s", "kubernetes",
        ],
    },
    "oauth_sso": {
        "cwe_patterns": ["cwe-346"],
        "tech_tags": ["oauth"],
        "keywords": [
            "oauth", "oidc", "saml", "sso", "redirect_uri",
            "authorization code", "implicit flow", "pkce",
            "openid", "identity provider",
        ],
    },
}


class FilterHandler:
    def __init__(self):
        self.categories = set(CATEGORY_RULES.keys())

    def classify(self, tokenized: dict, metadata: dict = None) -> list[str]:
        matched = []
        cwes = [c.lower() for c in tokenized.get("cwe_matches", [])]
        techs = tokenized.get("tech_stack", {})
        text_for_kw = " ".join([
            *(tokenized.get("endpoints", [])),
            *(tokenized.get("parameters", [])),
            *(tokenized.get("cwe_matches", [])),
            *(tokenized.get("payloads", [])),
        ]).lower()

        if metadata:
            text_for_kw += " " + json_to_text(metadata).lower()

        for cat_name, rules in CATEGORY_RULES.items():
            score = 0

            for cwe_label in cwes:
                for pat in rules["cwe_patterns"]:
                    if pat in cwe_label:
                        score += 3

            for tag, found_kws in techs.items():
                if tag in rules["tech_tags"]:
                    score += 2

            for kw in rules["keywords"]:
                if kw in text_for_kw:
                    score += 1

            if score >= 2:
                matched.append(cat_name)

        return matched

    def filter(self, entries: list[dict], category: str) -> list[dict]:
        if category == "all":
            return entries
        return [e for e in entries if category in e.get("categories", [])]

    def list_categories(self) -> list[str]:
        return sorted(self.categories)


def json_to_text(data: dict) -> str:
    parts = []
    for v in data.values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)
