#!/usr/bin/env python3
"""Cyassist GPT briefs — LLM-summarized exploitation writeups.

Supports: Anthropic Claude, OpenAI GPT, Google Gemini (via API), Ollama (local)
Falls back to template-based briefs when no LLM is configured.
"""

import datetime
import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent
BRIEFS_DIR = HERE / "briefs"

USER_AGENT = "cyassist-gpt/1.0"


class Fmt:
    @classmethod
    def red(cls, s): return f"\033[31m{s}\033[0m"
    @classmethod
    def green(cls, s): return f"\033[32m{s}\033[0m"
    @classmethod
    def yellow(cls, s): return f"\033[33m{s}\033[0m"
    @classmethod
    def bold(cls, s): return f"\033[1m{s}\033[0m"
    @classmethod
    def dim(cls, s): return f"\033[2m{s}\033[0m"


def _fetch_url(url: str, data: bytes = None, headers: dict = None, timeout: int = 60) -> Optional[bytes]:
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    try:
        req = urllib.request.Request(url, data=data, headers=req_headers)
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read()
    except Exception as e:
        print(f"  {Fmt.red(f'API call failed: {e}')}", file=sys.stderr)
        return None


# ── LLM Backends ─────────────────────────────────────────────────────────

def _call_anthropic(prompt: str, model: str = "claude-sonnet-4-20250514") -> Optional[str]:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    payload = json.dumps({
        "model": model,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    data = _fetch_url("https://api.anthropic.com/v1/messages", data=payload, headers=headers)
    if not data:
        return None
    try:
        body = json.loads(data)
        return body.get("content", [{}])[0].get("text", "")
    except (json.JSONDecodeError, IndexError, KeyError):
        return None


def _call_openai(prompt: str, model: str = "gpt-4o") -> Optional[str]:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return None
    payload = json.dumps({
        "model": model,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    headers = {
        "authorization": f"Bearer {key}",
        "content-type": "application/json",
    }
    data = _fetch_url("https://api.openai.com/v1/chat/completions", data=payload, headers=headers)
    if not data:
        return None
    try:
        body = json.loads(data)
        return body.get("choices", [{}])[0].get("message", {}).get("content", "")
    except (json.JSONDecodeError, IndexError, KeyError):
        return None


def _call_gemini(prompt: str, model: str = "gemini-2.0-flash") -> Optional[str]:
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return None
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 2000},
    }).encode()
    headers = {"content-type": "application/json"}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    data = _fetch_url(url, data=payload, headers=headers)
    if not data:
        return None
    try:
        body = json.loads(data)
        return body.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except (json.JSONDecodeError, IndexError, KeyError):
        return None


def _call_ollama(prompt: str, model: str = "llama3") -> Optional[str]:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
    }).encode()
    data = _fetch_url("http://localhost:11434/api/generate", data=payload)
    if not data:
        return None
    try:
        body = json.loads(data)
        return body.get("response", "")
    except json.JSONDecodeError:
        return None


def llm_generate(prompt: str) -> Optional[str]:
    """Try each LLM backend in order until one works."""
    for name, fn in [("Anthropic", _call_anthropic), ("OpenAI", _call_openai),
                     ("Gemini", _call_gemini), ("Ollama", _call_ollama)]:
        result = fn(prompt)
        if result:
            return result
    return None


# ── Exploit Brief Generation ────────────────────────────────────────────

def _template_brief(cve_id: str, info: dict, poc_repos: list = None,
                    exploit_entries: list = None, nuclei_findings: list = None) -> str:
    """Generate a structured exploit brief without an LLM."""
    cvss = info.get("cvss", "N/A")
    severity = info.get("severity", "N/A")
    epss = info.get("epss", 0)
    epss_pct = info.get("epss_percentile", 0)
    cwes = info.get("cwes", [])
    desc = info.get("description", "")
    in_kev = info.get("in_kev", False)
    has_poc = info.get("has_poc", False)
    vector = info.get("vector", "")

    lines = [f"# {cve_id} — Exploitation Brief", ""]
    lines.append(f"**Severity:** {severity} | **CVSS:** {cvss} | **EPSS:** {epss:.4f} (p{epss_pct:.2f})")
    if in_kev:
        lines.append("**CISA KEV:** ✓ Actively exploited in the wild")
    lines.append("")

    if desc:
        lines.append(f"**Description:** {desc}")
        lines.append("")

    if cwes:
        lines.append(f"**CWEs:** {', '.join(cwes)}")
        lines.append("")

    if vector:
        lines.append(f"**Vector:** `{vector}`")
        lines.append("")

    if poc_repos:
        lines.append("## GitHub PoC Repositories")
        for r in poc_repos[:5]:
            lines.append(f"- [{r.get('name', '?')}]({r.get('url', '')}) - ★{r.get('stars', 0)}")
            if r.get("desc"):
                lines.append(f"  - {r['desc'][:200]}")
        lines.append("")

    if exploit_entries:
        lines.append("## Exploit Database Entries")
        for e in exploit_entries[:5]:
            lines.append(f"- [{e.get('title', '?')}]({e.get('url', '')})")
        lines.append("")

    if nuclei_findings:
        lines.append("## Nuclei Scan Results")
        for f in nuclei_findings[:10]:
            tmpl = f.get("template-id", "?")
            matched = f.get("matched-at", "")
            severity_f = f.get("info", {}).get("severity", "?")
            lines.append(f"- [{severity_f}] {tmpl} @ {matched}")
        lines.append("")

    lines.append("## Hunting Guidance")
    lines.append(f"- Prioritize: this CVE has {'HIGH' if (epss > 0.05 or in_kev) else 'MODERATE'} exploitation likelihood")
    if has_poc:
        lines.append("- Working PoC exists — can be weaponized immediately")
    if cwes:
        cwe_links = [f"https://cwe.mitre.org/data/definitions/{c.split('-')[1]}.html" for c in cwes if c.startswith("CWE-")]
        for link in cwe_links:
            lines.append(f"- CWE reference: {link}")
    lines.append(f"- NVD entry: https://nvd.nist.gov/vuln/detail/{cve_id}")
    lines.append("")

    return "\n".join(lines)


def generate_exploit_brief(cve_id: str, info: dict, poc_repos: list = None,
                           exploit_entries: list = None, nuclei_findings: list = None,
                           use_llm: bool = True) -> str:
    """Generate an exploitation brief. Uses LLM if available, template fallback."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    brief_file = BRIEFS_DIR / f"exploit-{cve_id}-{today}.md"

    if use_llm:
        poc_context = ""
        if poc_repos:
            poc_context += "GitHub PoCs:\n" + "\n".join(
                f"  - {r['name']} ({r['url']}) ★{r['stars']}"
                for r in poc_repos[:5]) + "\n"
        if exploit_entries:
            poc_context += "Exploit-DB entries:\n" + "\n".join(
                f"  - {e['title']}" for e in exploit_entries[:5]) + "\n"

        prompt = f"""You are a security researcher writing an exploit brief for {cve_id}.

CVE Details:
- CVSS: {info.get('cvss', 'N/A')} ({info.get('severity', 'N/A')})
- EPSS: {info.get('epss', 0):.4f} (percentile: {info.get('epss_percentile', 0):.2f})
- CWE: {', '.join(info.get('cwes', []))}
- In CISA KEV: {info.get('in_kev', False)}
- PoC available: {info.get('has_poc', False)}
- Description: {info.get('description', '')[:500]}
{poc_context}
Provide a concise exploitation brief covering:
1. The vulnerability type and root cause
2. Attack vector and prerequisites
3. How to reproduce / exploit (step by step)
4. What to look for when hunting (signatures, patterns)
5. Remediation advice
Keep it actionable for a bug bounty hunter."""
        result = llm_generate(prompt)
        if result:
            brief_file.write_text(result)
            return result

    brief = _template_brief(cve_id, info, poc_repos, exploit_entries, nuclei_findings)
    brief_file.write_text(brief)
    return brief


def generate_all_briefs(enriched: dict, poc_map: dict = None,
                        nuclei_findings: dict = None, target_map: dict = None) -> list[str]:
    """Generate exploit briefs for high-priority CVEs."""
    generated = []
    sorted_cves = sorted(enriched.items(),
                         key=lambda x: x[1].get("priority_score", 0), reverse=True)
    for cve_id, info in sorted_cves:
        pri = info.get("priority_score", 0)
        if pri < 30:
            continue
        poc_repos = (poc_map or {}).get(cve_id, [])
        cve_findings = []
        if nuclei_findings:
            for tf in nuclei_findings.values():
                cve_findings.extend(
                    [f for f in tf if cve_id.lower() in f.get("template-id", "").lower()]
                )
        brief = generate_exploit_brief(cve_id, info, poc_repos=poc_repos if isinstance(poc_repos, list) else None,
                                       exploit_entries=None, nuclei_findings=cve_findings)
        generated.append(cve_id)
        print(f"  {Fmt.green(f'  Brief generated: {cve_id}')}")
    return generated


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Cyassist GPT exploit briefs")
    p.add_argument("--cve", metavar="CVE-ID", help="Generate brief for a specific CVE")
    p.add_argument("--all", action="store_true", help="Generate briefs for all enriched CVEs")
    args = p.parse_args()

    if args.cve:
        brief = generate_exploit_brief(args.cve, {
            "cvss": None, "severity": "UNKNOWN",
            "epss": 0, "cwes": [], "in_kev": False,
            "has_poc": False, "description": "",
        })
        print(brief[:2000])
    else:
        p.print_help()
