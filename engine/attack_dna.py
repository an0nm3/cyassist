"""
CyAssist AttackDNAExporter — converts tokenized writeup into compact
attack DNA vectors for fuzzing/reproducibility.
~1KB per vector, no body text stored.
"""

import json
import hashlib
import time
from pathlib import Path


class AttackDNAExporter:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "dna"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_vector(self, metadata: dict, tokenized: dict, categories: list[str]) -> dict:
        eps = tokenized.get("endpoints", [])
        params = tokenized.get("parameters", [])
        payloads = tokenized.get("payloads", [])
        cwes = tokenized.get("cwe_matches", [])
        mutations = tokenized.get("mutation_types", [])

        vector = {
            "report_id": metadata.get("report_id", "unknown"),
            "cwe": "; ".join(cwes) if cwes else "UNKNOWN",
            "severity": tokenized.get("severity", metadata.get("severity", "INFO")),
            "target_context": {
                "discovered_paths": sorted(set(
                    e["path"] for e in eps if e["path"].startswith("/")
                ))[:10],
                "vulnerable_parameters": sorted(set(params))[:10],
            },
            "fuzz_strategy": self._build_fuzz_strategy(cwes, mutations, params, payloads),
            "tech_classification": tokenized.get("tech_stack", {}),
            "categories": categories,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "body_ref": tokenized.get("body_hash", ""),
        }
        vector["_size_bytes"] = len(json.dumps(vector))
        return vector

    def _build_fuzz_strategy(self, cwes: list[str], mutations: list[str],
                              params: list[str], payloads: list[str]) -> dict:
        strategy = {
            "mutation_types": mutations or ["param_fuzzing"],
            "primary_vector": "UNKNOWN",
        }

        for cwe in cwes:
            cwe_lower = cwe.lower()
            if "idor" in cwe_lower:
                strategy["primary_vector"] = "id_enumeration"
                strategy["payload_example"] = params[:3] if params else ["id=N"]
            elif "xss" in cwe_lower:
                strategy["primary_vector"] = "reflected_input"
                strategy["payload_example"] = ["<script>alert(1)</script>"]
            elif "sqli" in cwe_lower:
                strategy["primary_vector"] = "sql_injection"
                strategy["payload_example"] = ["' OR 1=1 --"]
            elif "ssrf" in cwe_lower:
                strategy["primary_vector"] = "oob_interaction"
                strategy["payload_example"] = ["http://attacker.oob/"]
            elif "rce" in cwe_lower:
                strategy["primary_vector"] = "command_injection"
                strategy["payload_example"] = ["; whoami", "| id"]
            elif "graphql" in cwe_lower:
                strategy["primary_vector"] = "introspection_abuse"
                strategy["payload_example"] = ["{__schema{types{name}}}"]
            elif "prototype" in cwe_lower:
                strategy["primary_vector"] = "prototype_pollution"
                strategy["payload_example"] = ['{"__proto__":{"isAdmin":true}}']
            elif "race" in cwe_lower:
                strategy["primary_vector"] = "race_condition"
                strategy["payload_example"] = ["parallel N requests"]
            elif "oauth" in cwe_lower:
                strategy["primary_vector"] = "redirect_uri_tampering"
                strategy["payload_example"] = ["https://attacker.com/callback"]
            elif "replay" in cwe_lower:
                strategy["primary_vector"] = "request_replay"
                strategy["payload_example"] = ["capture-and-resend"]

        if payloads:
            strategy["payload_example"] = payloads[:2]

        return strategy

    def save_vector(self, vector: dict) -> str:
        rid = vector.get("report_id", "unknown").replace("/", "_")
        out_path = self.output_dir / f"dna_{rid}.json"
        out_path.write_text(json.dumps(vector, indent=2))
        return str(out_path)

    def export_one(self, metadata: dict, tokenized: dict, categories: list[str]) -> dict:
        vector = self.build_vector(metadata, tokenized, categories)
        self.save_vector(vector)
        return vector

    def export_catalog(self, vectors: list[dict]) -> str:
        out_path = self.output_dir / "dna_catalog.json"
        catalog = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "count": len(vectors),
            "vectors": vectors,
        }
        out_path.write_text(json.dumps(catalog, indent=2))
        return str(out_path)

    def collect_all(self) -> list[dict]:
        vectors = []
        for fp in sorted(self.output_dir.glob("dna_*.json")):
            if fp.name == "dna_catalog.json":
                continue
            try:
                vectors.append(json.loads(fp.read_text()))
            except (json.JSONDecodeError, OSError):
                continue
        return vectors
