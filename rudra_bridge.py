#!/usr/bin/env python3
"""Cyassist → Rudra Bridge — feeds structured intel into Rudra's pipeline.
Maps: technology→CVE→exploit technique→Rudra sink type→Rudra probes.
No exploit code stored — Rudra handles exploitation via its probes + mutations."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent
RUDRA_DIR = Path.home() / "bugbounty" / ".claude" / "skills" / "rudra"
RUDRA_PIPELINE = RUDRA_DIR / "pipeline.py"
RUDRA_PROBES = RUDRA_DIR / "web-scanner" / "probes.yaml"

try:
    from intel_db import IntelDB
except ImportError:
    IntelDB = None


class Fmt:
    _no_color = not sys.stdout.isatty()
    @classmethod
    def _w(cls, c, s, r="0"):
        if cls._no_color or not s: return s
        return f"\033[{c}m{s}\033[{r}m"
    @classmethod
    def green(cls, s): return cls._w("32", s)
    @classmethod
    def red(cls, s): return cls._w("31", s)
    @classmethod
    def yellow(cls, s): return cls._w("33", s)
    @classmethod
    def bold(cls, s): return cls._w("1", s)
    @classmethod
    def dim(cls, s): return cls._w("2", s)
    @classmethod
    def cyan(cls, s): return cls._w("36", s)


# ── Technology→CVE Knowledge Base ──────────────────────────────────────────
# Technology→possible CVEs mapping for quick lookup.
# cyassist DB stores the canonical list; this is the bootstrap/default set.
TECH_CVE_MAP = {
    "apache": {
        "2.4.49": [("CVE-2021-41773", "path_traversal", "Path Traversal")],
        "2.4.50": [("CVE-2021-42013", "path_traversal", "Path Traversal")],
        "log4j": [("CVE-2021-44228", "rce", "Log4Shell RCE")],
        "struts": [("CVE-2017-5638", "rce", "Struts2 RCE")],
        "shiro": [("CVE-2016-4437", "rce", "Shiro RCE")],
    },
    "nginx": {
        "1.20.0": [],
    },
    "spring": {
        "framework": [("CVE-2022-22965", "rce", "Spring4Shell RCE")],
        "cloud": [("CVE-2022-22963", "rce", "Spring Cloud RCE")],
        "boot": [("CVE-2022-22965", "rce", "Spring4Shell RCE")],
    },
    "wordpress": {
        "any": [
            ("CVE-2025-29927", "rce", "WP RCE"),
            ("CVE-2024-44000", "lfi", "LFI"),
        ],
    },
    "servicenow": {
        "any": [("CVE-2025-29927", "rce", "ServiceNow RCE")],
    },
    "jenkins": {
        "2.541.1": [],
        "any": [
            ("CVE-2024-23897", "lfi", "Jenkins CLI LFI"),
        ],
    },
    "next.js": {
        "any": [("CVE-2025-29927", "rce", "Next.js Middleware Bypass")],
    },
    "cloudflare": {
        "any": [],
    },
    "okta": {
        "any": [],
    },
    "s3": {
        "any": [],
    },
    "graphql": {
        "any": [],
    },
}

# CVE technique → Rudra probe sink type
CVE_TO_SINK = {
    "sqli": "sql_injection",
    "xss": "reflected_xss",
    "ssrf": "ssrf",
    "rce": "command_injection",
    "lfi": "lfi",
    "path_traversal": "path_traversal",
    "ssti": "ssti",
    "xxe": "xxe",
    "idor": "idor",
    "open_redirect": "open_redirect",
    "file_upload": "file_upload",
    "prototype_pollution": "prototype_pollution",
    "race_condition": "race_condition",
    "auth_bypass": "auth_bypass",
    "oauth_misconfig": "oauth_misconfig",
    "jwt_attack": "jwt_attack",
    "nosqli": "nosqli",
    "generic": "generic",
}


def _load_probes() -> dict:
    """Load Rudra's probes.yaml to understand available sink probes."""
    if not RUDRA_PROBES.exists():
        return {}
    try:
        import yaml
        with open(RUDRA_PROBES) as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass
    try:
        return json.loads(RUDRA_PROBES.read_text()) if RUDRA_PROBES.read_text().strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


class RudraBridge:
    def __init__(self, db: IntelDB = None):
        self.db = db or IntelDB()
        self._probes = _load_probes()

    # ── Tech→CVE Lookup ──
    def get_cves_for_tech(self, technology: str, version: str = "") -> list[dict]:
        """Query cyassist DB + static map for CVEs matching a technology."""
        results = []
        tech_lower = technology.lower().strip()

        # 1. Check DB (has enriched CVE data)
        db_cves = self.db.get_cves_by_tech(tech_lower)
        for c in db_cves:
            results.append({
                "cve_id": c["id"],
                "cvss": c.get("cvss"),
                "severity": c.get("severity"),
                "epss": c.get("epss", 0),
                "in_kev": c.get("in_kev", 0),
                "has_poc": c.get("has_poc", 0),
                "techniques": c.get("techniques", []),
                "source": "cyassist-db",
            })

        # 2. Check static map for the tech
        for static_tech, versions in TECH_CVE_MAP.items():
            if static_tech in tech_lower or tech_lower in static_tech:
                ver_data = versions.get("any", [])
                if version and version in versions:
                    ver_data += versions[version]
                else:
                    for ver_key, ver_cves in versions.items():
                        if ver_key != "any":
                            ver_data += ver_cves
                for cve_id, technique, desc in ver_data:
                    if not any(r["cve_id"] == cve_id for r in results):
                        sink_type = CVE_TO_SINK.get(technique, "generic")
                        results.append({
                            "cve_id": cve_id,
                            "technique": technique,
                            "sink_type": sink_type,
                            "description": desc,
                            "source": "static-map",
                        })

        # 3. Check DB for exploits matching this tech
        exploits = self.db.db.execute(
            "SELECT DISTINCT cve_id, technique, sink_type FROM exploits WHERE target_software LIKE ?"
            " LIMIT 20", (f"%{tech_lower}%",)
        ).fetchall()
        for row in exploits:
            if not any(r["cve_id"] == row[0] for r in results):
                results.append({
                    "cve_id": row[0],
                    "technique": row[1] or "generic",
                    "sink_type": row[2] or CVE_TO_SINK.get(row[1], "generic"),
                    "source": "exploit-dna",
                })

        return results

    # ── CVE→Nuclei Template IDs ──
    def get_nuclei_templates(self, cve_id: str) -> list[dict]:
        """Get nuclei template IDs for a CVE from cyassist DB."""
        return self.db.get_templates_for_cve(cve_id)

    # ── CVE→Rudra Probe Config ──
    def cve_to_probe_config(self, cve_id: str) -> Optional[dict]:
        """Generate a Rudra-compatible probe config from CVE data."""
        cve = self.db.get_cve(cve_id)
        if not cve:
            return None

        techniques = cve.get("techniques", [])
        technique = techniques[0] if techniques else "generic"
        sink_type = CVE_TO_SINK.get(technique, "generic")

        exploits = self.db.get_exploits_for_cve(cve_id)
        payload_template = ""
        param_template = ""
        for ex in exploits:
            pt = ex.get("payload_template", "")
            if pt:
                payload_template = pt
            pt2 = ex.get("parameter_template", "")
            if pt2:
                param_template = pt2
            if payload_template and param_template:
                break

        config = {
            "cve_id": cve_id,
            "sink_type": sink_type,
            "technique": technique,
            "cvss": cve.get("cvss"),
            "epss": cve.get("epss", 0),
            "in_kev": bool(cve.get("in_kev")),
            "payload_hint": payload_template[:200],
            "param_hint": param_template[:200],
            "nuclei_templates": [t["template_id"] for t in self.get_nuclei_templates(cve_id)],
            "exploit_urls": [ex["url"] for ex in exploits if ex.get("url")][:5],
        }
        return config

    # ── Enrich Rudra Finding ──
    def enrich_finding(self, finding: dict) -> dict:
        """Enrich a Rudra scanner finding with CVE intel from cyassist."""
        enriched = dict(finding)
        sink_type = finding.get("sink_type", "") or finding.get("category", "")
        target_url = finding.get("url", "") or finding.get("target", "")

        # 1. Try to match technology from URL
        techs = self.detect_tech_from_url(target_url)
        cve_matches = []
        for tech in techs:
            cve_matches.extend(self.get_cves_for_tech(tech))

        # 2. Try to match CVEs by sink type
        if not cve_matches and sink_type:
            sink_exploits = self.db.get_exploits_by_technique(sink_type.replace("_", " "))
            for ex in sink_exploits[:3]:
                cve_matches.append({
                    "cve_id": ex["cve_id"],
                    "technique": ex.get("technique", ""),
                    "source": "sink-match",
                })

        # 3. Add matching nuclei templates
        nuclei_ids = set()
        for match in cve_matches:
            templates = self.get_nuclei_templates(match["cve_id"])
            for t in templates:
                nuclei_ids.add(t["template_id"])

        enriched["cyassist"] = {
            "matched_cves": cve_matches[:5],
            "nuclei_template_ids": list(nuclei_ids)[:10],
            "total_cve_matches": len(cve_matches),
        }

        return enriched

    # ── Tech Detection from URL ──
    def detect_tech_from_url(self, url: str) -> list[str]:
        """Detect likely technologies from URL patterns."""
        techs = []
        if not url:
            return techs
        url_lower = url.lower()
        patterns = {
            "wordpress": ["wp-content", "wp-admin", "wp-json", "/wp/"],
            "next.js": ["_next/", "__next"],
            "graphql": ["/graphql", "/gql"],
            "jenkins": ["/jenkins", "jenkins."],
            "servicenow": ["service-now", "servicenow", "/now/"],
            "s3": [".s3.", "s3.amazonaws"],
            "cloudfront": [".cloudfront.net"],
            "cloudflare": ["cloudflare"],
            "okta": [".okta.", "okta.com"],
            "apache": ["/cgi-bin/", "/server-status"],
            "nginx": ["nginx"],
            "spring": ["/actuator", "/swagger"],
            "rails": ["/rails/", "rails."],
            "laravel": ["laravel"],
            "django": ["django", "csrftoken"],
            "asp.net": [".aspx", ".ashx", ".asmx"],
        }
        for tech, keywords in patterns.items():
            for kw in keywords:
                if kw in url_lower:
                    techs.append(tech)
                    break
        return techs

    # ── Generate Rudra Pipeline Config from CVE Intel ──
    def generate_scan_config(self, target_url: str, techs: list[str] = None) -> dict:
        """Generate a focused Rudra scan configuration based on CVE intel for a target."""
        if not techs:
            techs = self.detect_tech_from_url(target_url)

        config = {
            "target": target_url,
            "probes": [],
            "nuclei_ids": [],
            "priority_cves": [],
        }

        seen_sinks = set()
        for tech in techs:
            cves = self.get_cves_for_tech(tech)
            for match in cves:
                cve_id = match.get("cve_id", "")
                if cve_id:
                    config["priority_cves"].append(cve_id)
                sink_type = match.get("sink_type", "") or CVE_TO_SINK.get(match.get("technique", ""), "")
                if sink_type and sink_type not in seen_sinks:
                    seen_sinks.add(sink_type)
                    config["probes"].append({
                        "sink_type": sink_type,
                        "cve": cve_id,
                        "technique": match.get("technique", ""),
                    })
                templates = self.get_nuclei_templates(cve_id)
                for t in templates:
                    if t["template_id"] not in config["nuclei_ids"]:
                        config["nuclei_ids"].append(t["template_id"])

        config["probe_count"] = len(config["probes"])
        config["nuclei_count"] = len(config["nuclei_ids"])
        return config

    # ── Trigger Rudra Pipeline ──
    def trigger_rudra_scan(self, target_url: str, techs: list[str] = None,
                           extra_args: list[str] = None) -> Optional[dict]:
        """Trigger Rudra pipeline with cyassist intel."""
        if not RUDRA_PIPELINE.exists():
            return {"error": f"Rudra pipeline not found at {RUDRA_PIPELINE}"}

        scan_config = self.generate_scan_config(target_url, techs)

        cmd = ["python3", str(RUDRA_PIPELINE), "--target", target_url]
        for probe in scan_config.get("probes", [])[:5]:
            sink = probe.get("sink_type", "")
            if sink:
                cmd += ["--sink", sink]
        if extra_args:
            cmd.extend(extra_args)

        return {
            "scan_config": scan_config,
            "command": " ".join(cmd),
            "message": f"Configured {scan_config['probe_count']} probes + {scan_config['nuclei_count']} nuclei templates for {target_url}",
        }

    def import_targets_from_rudra(self) -> int:
        """Import registered targets from cyassist's targets.yaml into intel DB."""
        targets_file = HERE / "targets.yaml"
        if not targets_file.exists():
            return 0
        try:
            import yaml
            with open(targets_file) as f:
                targets = yaml.safe_load(f) or {}
        except ImportError:
            try:
                targets = json.loads(targets_file.read_text()) if targets_file.read_text().strip() else {}
            except (json.JSONDecodeError, OSError):
                return 0
        count = 0
        for name, info in targets.items():
            self.db.upsert_target(
                name=name,
                url=info.get("url", ""),
                techs=info.get("techs", []),
                keywords=info.get("keywords", []),
            )
            count += 1
        return count


def main():
    import argparse
    p = argparse.ArgumentParser(description="Cyassist Rudra bridge")
    p.add_argument("--tech", metavar="TECH", help="Look up CVEs for a technology")
    p.add_argument("--cve", metavar="CVE-ID", help="Generate probe config for a CVE")
    p.add_argument("--target", metavar="URL", help="Generate scan config for target URL")
    p.add_argument("--enrich", metavar="FINDING_JSON", help="Enrich a Rudra finding (JSON string)")
    p.add_argument("--auto-scan", metavar="URL", help="Generate auto-scan config for target")
    p.add_argument("--import-targets", action="store_true", help="Import targets from targets.yaml")
    p.add_argument("--status", action="store_true", help="Show DB stats")
    args = p.parse_args()

    if not IntelDB:
        print("Error: intel_db.py required")
        sys.exit(1)

    db = IntelDB()
    bridge = RudraBridge(db)

    if args.tech:
        cves = bridge.get_cves_for_tech(args.tech)
        if cves:
            print(f"  {Fmt.bold(f'{len(cves)} CVEs for {args.tech}')}")
            for c in cves[:20]:
                sev = c.get("severity", c.get("cvss", ""))
                print(f"    {Fmt.cyan(c.get('cve_id', c.get('cve', '')))}  "
                      f"{Fmt.dim(f'CVSS:{sev}')}  "
                      f"{Fmt.green(c.get('technique', ''))}  "
                      f"{Fmt.dim(c.get('source', ''))}")
        else:
            print(f"  {Fmt.yellow(f'No CVEs found for {args.tech}')}")

    elif args.cve:
        config = bridge.cve_to_probe_config(args.cve)
        if config:
            print(json.dumps(config, indent=2))
        else:
            print(f"  {Fmt.yellow(f'No intel found for {args.cve}')}")

    elif args.target or args.auto_scan:
        url = args.target or args.auto_scan
        techs = bridge.detect_tech_from_url(url)
        result = bridge.trigger_rudra_scan(url, techs)
        print(f"  {Fmt.bold('Scan Configuration')}")
        print(f"  Target: {Fmt.cyan(url)}")
        print(f"  Detected techs: {Fmt.green(', '.join(techs) if techs else 'none')}")
        print(f"  Probes: {Fmt.bold(str(result['scan_config']['probe_count']))}")
        print(f"  Nuclei templates: {Fmt.bold(str(result['scan_config']['nuclei_count']))}")
        print(f"  Priority CVEs: {Fmt.bold(str(len(result['scan_config']['priority_cves'])))}")
        print(f"  Command: {Fmt.dim(result['command'])}")
        if result['scan_config']['priority_cves']:
            print(f"  CVEs: {', '.join(result['scan_config']['priority_cves'][:5])}")

    elif args.enrich:
        try:
            finding = json.loads(args.enrich)
            enriched = bridge.enrich_finding(finding)
            print(json.dumps(enriched, indent=2))
        except json.JSONDecodeError:
            print(f"  {Fmt.red('Invalid JSON')}")

    elif args.import_targets:
        count = bridge.import_targets_from_rudra()
        print(f"  {Fmt.green(f'Imported {count} targets into intel DB')}")

    elif args.status:
        stats = db.stats()
        sz = stats["size_mb"]
        print(f"  DB size: {Fmt.bold(f'{sz:.2f}MB')}")
        print(f"  CVEs: {stats['cves']}")
        print(f"  Exploits (DNA): {stats['exploits']}")
        print(f"  Templates indexed: {stats['templates']}")
        print(f"  Tech→CVE mappings: {stats['tech_cve']}")
        print(f"  News articles: {stats['news']}")
        print(f"  Targets: {stats['targets']}")

    db.close()


if __name__ == "__main__":
    main()
