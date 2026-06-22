#!/usr/bin/env python3
"""Cyassist web dashboard — Flask UI for briefs, CVEs, targets, nuclei findings.

Usage:
  python3 dashboard/app.py [--port 8080]
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    from flask import Flask, render_template_string, jsonify
except ImportError:
    print("Flask required: pip install flask")
    sys.exit(1)

HERE = Path(__file__).resolve().parent.parent
BRIEFS_DIR = HERE / "briefs"
EXPLOITS_DIR = HERE / "exploits"
KEV_DIR = HERE / "kev"
SCORE_DIR = HERE / "cve_scores"
NUCLEI_DIR = HERE / "nuclei_results"
TARGETS_FILE = HERE / "targets.yaml"

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html data-theme="dark">
<head>
  <title>Cyassist Dashboard</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
  <style>
    :root { --border-radius: 6px; }
    .critical { color: #e74c3c; font-weight: bold; }
    .high { color: #e67e22; font-weight: bold; }
    .medium { color: #f1c40f; }
    .low { color: #7f8c8d; }
    .stat-card { text-align: center; padding: 1em; }
    .stat-card h2 { margin: 0; font-size: 2.5em; }
    .stat-card p { margin: 0; color: var(--muted-color); }
    pre { overflow-x: auto; font-size: 0.8em; }
    .nav-link { display: inline-block; margin-right: 1em; }
    .badge { display: inline-block; padding: 0.15em 0.5em; border-radius: 4px; font-size: 0.75em; font-weight: bold; }
    .badge-kev { background: #e74c3c; color: #fff; }
    .badge-poc { background: #3498db; color: #fff; }
    .badge-critical { background: #c0392b; color: #fff; }
    .badge-high { background: #d35400; color: #fff; }
  </style>
</head>
<body>
  <nav class="container-fluid">
    <ul><li><strong>Cyassist Hunter</strong></li></ul>
    <ul>
      <li><a href="/">Overview</a></li>
      <li><a href="/briefs">Briefs</a></li>
      <li><a href="/cves">CVEs</a></li>
      <li><a href="/targets">Targets</a></li>
      <li><a href="/nuclei">Nuclei</a></li>
    </ul>
  </nav>

  <main class="container">
    {% block content %}{% endblock %}
  </main>
</body>
</html>"""


def _load_scores() -> dict:
    f = SCORE_DIR / "enriched.json"
    if f.exists():
        try:
            return json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _load_briefs() -> list:
    briefs = []
    if BRIEFS_DIR.exists():
        for fp in sorted(BRIEFS_DIR.rglob("*.md"), reverse=True)[:50]:
            text = fp.read_text(errors="replace")
            title_m = re.search(r"^# (.+)", text)
            briefs.append({"file": fp.name, "title": title_m.group(1) if title_m else fp.stem,
                           "date": fp.stat().st_mtime, "path": str(fp.relative_to(HERE))})
    return briefs


def _load_targets() -> dict:
    if TARGETS_FILE.exists():
        try:
            import yaml
            with open(TARGETS_FILE) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            try:
                return json.loads(TARGETS_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                pass
    return {}


def _count_exploits() -> int:
    return sum(1 for _ in EXPLOITS_DIR.rglob("*.md")) if EXPLOITS_DIR.exists() else 0


def _count_kev() -> int:
    return sum(1 for _ in KEV_DIR.rglob("*.md")) if KEV_DIR.exists() else 0


def _count_nuclei() -> int:
    return sum(1 for _ in NUCLEI_DIR.rglob("*.json")) if NUCLEI_DIR.exists() else 0


@app.route("/")
def overview():
    scores = _load_scores()
    targets = _load_targets()
    critical = sum(1 for i in scores.values() if i.get("priority_label") == "CRITICAL")
    high = sum(1 for i in scores.values() if i.get("priority_label") == "HIGH")
    stats = {
        "enriched_cves": len(scores),
        "critical": critical,
        "high": high,
        "exploits": _count_exploits(),
        "kev": _count_kev(),
        "nuclei_scans": _count_nuclei(),
        "targets": len(targets),
        "briefs": len(_load_briefs()),
    }
    top_cves = sorted(scores.items(), key=lambda x: x[1].get("priority_score", 0), reverse=True)[:20]
    return render_template_string(HTML + """
    {% block content %}
    <div class="grid">
      {% for label, val in [('CVEs Enriched', stats.enriched_cves), ('Critical', stats.critical),
                            ('High', stats.high), ('Exploits', stats.exploits),
                            ('CISA KEV', stats.kev), ('Nuclei Scans', stats.nuclei_scans),
                            ('Targets', stats.targets), ('Briefs', stats.briefs)] %}
      <article class="stat-card">
        <h2>{{ val }}</h2>
        <p>{{ label }}</p>
      </article>
      {% endfor %}
    </div>

    <h3>Top Priority CVEs</h3>
    <table>
      <thead><tr><th>CVE</th><th>Priority</th><th>CVSS</th><th>EPSS</th><th>KEV</th><th>PoC</th><th>Description</th></tr></thead>
      <tbody>
      {% for cve, info in top_cves %}
      <tr>
        <td><strong>{{ cve }}</strong></td>
        <td><span class="{{ info.priority_label|lower }}">{{ info.priority_label }}</span></td>
        <td>{{ info.cvss or 'N/A' }}</td>
        <td>{{ '%.4f'|format(info.epss|float) }}</td>
        <td>{{ '✓' if info.in_kev else '' }}</td>
        <td>{{ '✓' if info.has_poc else '' }}</td>
        <td><small>{{ info.description[:100] if info.description else '' }}</small></td>
      </tr>
      {% endfor %}
      </tbody>
    </table>
    {% endblock %}
    """, stats=stats, top_cves=top_cves)


@app.route("/briefs")
def briefs():
    briefs = _load_briefs()
    return render_template_string(HTML + """
    {% block content %}
    <h2>Hunting Briefs</h2>
    <table>
      <thead><tr><th>Date</th><th>Title</th><th>File</th></tr></thead>
      <tbody>
      {% for b in briefs %}
      <tr>
        <td>{{ b.date|int|datetime }}</td>
        <td>{{ b.title }}</td>
        <td><a href="/raw/{{ b.path }}">{{ b.file }}</a></td>
      </tr>
      {% endfor %}
      </tbody>
    </table>
    {% endblock %}
    """, briefs=briefs)


@app.route("/cves")
def cves():
    scores = _load_scores()
    sorted_cves = sorted(scores.items(), key=lambda x: x[1].get("priority_score", 0), reverse=True)
    return render_template_string(HTML + """
    {% block content %}
    <h2>All Enriched CVEs</h2>
    <table>
      <thead><tr><th>CVE</th><th>Priority</th><th>CVSS</th><th>EPSS</th><th>KEV</th><th>PoC</th><th>CWEs</th><th>Description</th></tr></thead>
      <tbody>
      {% for cve, info in cves %}
      <tr>
        <td><strong>{{ cve }}</strong></td>
        <td><span class="{{ info.priority_label|lower }}">{{ info.priority_label }} ({{ info.priority_score }})</span></td>
        <td>{{ info.cvss or 'N/A' }}</td>
        <td>{{ '%.4f'|format(info.epss|float) }}</td>
        <td>{{ '✓' if info.in_kev else '' }}</td>
        <td>{{ '✓' if info.has_poc else '' }}</td>
        <td><small>{{ ', '.join(info.cwes[:3]) if info.cwes else '' }}</small></td>
        <td><small>{{ info.description[:150] if info.description else '' }}</small></td>
      </tr>
      {% endfor %}
      </tbody>
    </table>
    {% endblock %}
    """, cves=sorted_cves)


@app.route("/targets")
def targets():
    t = _load_targets()
    return render_template_string(HTML + """
    {% block content %}
    <h2>Registered Targets</h2>
    <div class="grid">
    {% for name, info in targets.items() %}
      <article>
        <h3>{{ name }}</h3>
        {% if info.url %}<p><small>URL:</small> {{ info.url }}</p>{% endif %}
        <p><small>Techs:</small><br>{% for t in info.techs %}<span class="badge">{{ t }}</span> {% endfor %}</p>
        <p><small>Keywords:</small><br>{% for k in info.keywords %}<span class="badge">{{ k }}</span> {% endfor %}</p>
      </article>
    {% endfor %}
    </div>
    {% endblock %}
    """, targets=t)


@app.route("/nuclei")
def nuclei():
    findings = []
    if NUCLEI_DIR.exists():
        for fp in sorted(NUCLEI_DIR.rglob("*.json"), reverse=True)[:10]:
            for line in fp.read_text().strip().split("\n"):
                if line.strip():
                    try:
                        findings.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return render_template_string(HTML + """
    {% block content %}
    <h2>Nuclei Scan Results</h2>
    <table>
      <thead><tr><th>Template</th><th>Severity</th><th>Matched At</th><th>Target</th><th>Name</th></tr></thead>
      <tbody>
      {% for f in findings %}
      <tr>
        <td><code>{{ f.get('template-id', '?') }}</code></td>
        <td>{{ f.get('info', {}).get('severity', '?') }}</td>
        <td><small>{{ f.get('matched-at', '')[:80] }}</small></td>
        <td><small>{{ f.get('host', '') }}</small></td>
        <td>{{ f.get('info', {}).get('name', '')[:60] }}</td>
      </tr>
      {% endfor %}
      </tbody>
    </table>
    {% endblock %}
    """, findings=findings[:200])


@app.route("/raw/<path:path>")
def raw_file(path):
    from flask import send_from_directory
    return send_from_directory(str(HERE), path)


@app.template_filter("datetime")
def _datetime_filter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Cyassist web dashboard")
    p.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")
    p.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    args = p.parse_args()
    print(f"  Dashboard: http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)
