# Cyassist v2 — User Manual

> **Intel-Driven Bug Bounty Assistant**  
> SQLite-backed threat intel, Indian cybersecurity news, exploit DNA harvesting, template indexing, and Rudra Framework integration.  
> Storage target: `<100MB` — metadata only, no exploit code cached.  
> Latest: **v2.2.1** — short flags, 3-color Indian logo, white-bg blinking highlights, BB-only news DB, India fallback (7 days), LinkedIn noise removed.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Installation](#3-installation)
4. [Quick Start](#4-quick-start)
5. [Command-Line Flags](#5-command-line-flags)
6. [Sub-Modules](#6-sub-modules)
7. [Intel DB](#7-intel-db)
8. [Indian News Scraping](#8-indian-news-scraping)
9. [Web News Scraping](#9-web-news-scraping)
10. [Exploit DNA Harvesting](#10-exploit-dna-harvesting)
11. [Template Sync](#11-template-sync)
12. [Rudra Bridge](#12-rudra-bridge)
13. [On-Demand Exploit Fetcher](#13-on-demand-exploit-fetcher)
14. [Watch Mode](#14-watch-mode)
15. [Daily Auto-Run](#15-daily-auto-run)
16. [Targets](#16-targets)
17. [Database Schema](#17-database-schema)
18. [False Positive Prevention](#18-false-positive-prevention)

---

## 1. Overview

**Cyassist** is your threat-intel copilot for bug bounty hunting. It scrapes Indian cybersecurity news, harvests exploit metadata from Exploit-DB and GitHub, indexes Nuclei/Metasploit templates, and bridges intel directly into Rudra's probe configuration.

| Attribute | Value |
|-----------|-------|
| Language | Python 3.11+ |
| Storage | SQLite (WAL mode, `<100MB` target) |
| Indian Sources | 8 (CERT-In, ET CISO, Quick Heal, Cyble, Seqrite, Payatu, CloudSEK, RBI) |
| Web Sources | 10+ (THN, BleepingComputer, GBHackers, PacketStorm, Reddit, X/Twitter) |
| Exploit Sources | Exploit-DB RSS + GitHub API |
| Template Sources | Nuclei + Metasploit (local scan) |
| Integrations | Rudra Framework v10+ |


### What Makes Cyassist Different

- **Storage-budget disciplined** — stores only metadata/DNA (CVE ID, technique, sink type, parameter template, URL). No exploit code cached. 100K entries ≈ 1MB.
- **Indian-first** — dedicated scrapers for CERT-In, Indian vendors (Quick Heal, Seqrite, Cyble), and Indian research blogs (Payatu, CloudSEK).
- **Rudra-native bridge** — tech → CVE → sink type → probe config in one call. Feeds directly into Rudra's `pipeline.py`.
- **On-demand fetching** — exploit code fetched read-only at query time, never cached. Zero storage cost.
- **Watch mode** — polls for new CVEs, alerts on high-EPSS/PoC/KEV entries, optionally triggers Rudra auto-scan.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────┐
│  cyassist — Unified CLI (cyassist.py)                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐  ┌────────────┐  ┌─────────────┐         │
│  │ scraper  │  │  harvester │  │ template    │         │
│  │ _india.py│  │  .py       │  │ _sync.py    │         │
│  │          │  │            │  │             │         │
│  │ CERT-In  │  │ Exploit-DB │  │ Nuclei YAML │         │
│  │ ET CISO  │  │ GitHub API │  │ Metasploit  │         │
│  │ Cyble    │  │            │  │             │         │
│  │ Seqrite  │  └─────┬──────┘  └──────┬──────┘         │
│  │ Payatu   │        │               │                  │
│  │ CloudSEK │        ▼               ▼                  │
│  │ RBI      │  ┌──────────────────────────┐             │
│  └────┬─────┘  │       Intel DB           │             │
│       │        │  (intel_db.py — SQLite)  │             │
│  ┌────┴─────┐  │                          │             │
│  │ scraper  │  │  cves  │ exploits │ news │             │
│  │ _web.py  │  │  tech_cve │ templates     │             │
│  │          │  │  targets                    │             │
│  │ THN      │  └──────────┬───────────────┘             │
│  │ BleecComp│             │                              │
│  │ GBHackers│             ▼                              │
│  │ PacketSt┐│  ┌──────────────────────────┐             │
│  │ Reddit  ││  │     Rudra Bridge          │             │
│  │ X/Twitter│  │  (rudra_bridge.py)       │             │
│  └────┬─────┘  │                          │             │
│       │        │  tech→CVE lookup         │             │
│       │        │  CVE→probe config        │             │
│       │        │  finding enrichment      │             │
│       │        │  auto-scan config        │             │
│  ┌────┴─────┐  │  target import           │             │
│  │ on_demand│  └──────────┬───────────────┘             │
│  │ .py      │             │                              │
│  │          │             ▼                              │
│  │ fetch     │  ┌──────────────────────────┐             │
│  │ exploit   │  │      Rudra Pipeline      │             │
│  │ watch mode│  │  (pipeline.py)           │             │
│  │ nuclei    │  │                          │             │
│  └──────────┘  │  17 sink types           │             │
│                │  12 WAF bypass mutators  │             │
│                │  OOB verification        │             │
│                └──────────────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
Scrapers → IntelDB → RudraBridge → Rudra Pipeline → Findings
                ↑                        ↑
         On-Demand Fetch           Watch Mode
         (read-only, no cache)     (poll for new CVEs)
```

---

## 3. Installation

### Prerequisites

- Python 3.11+
- `requests` library (for WAF-bypass HTTP fetching)
- Optional: `nuclei` CLI for template sync and on-demand scanning
- Optional: `git` for Metasploit template scanning

### Setup

```bash
# Cyassist is pre-installed at ~/.local/bin/cyassist
# Test it:
cyassist --help

# Initialise the database:
cyassist --status

# Run the first scrapes:
cyassist --daily
```

### CLI Wrapper

The `cyassist` command is a bash wrapper at `~/.local/bin/cyassist`:

```bash
#!/usr/bin/env bash
exec python3 /home/kali/bugbounty/cyassist/cyassist.py "$@"
```

---

## 4. Quick Start

### Show Indian cyber news (instant) — 3-color flag logo
```bash
cyassist -i
```
Falls back to 7-day window if no India-relevant news found in last 24h.

### Launch news reader (with optional short flags)
```bash
cyassist --reader
cyassist -t              # today's headlines
cyassist -i              # India-filtered
cyassist -i -t           # India today
cyassist -q "SSRF"       # search
cyassist -c techniques    # techniques category
```

### Show database status
```bash
cyassist --status
```

### Scrape Indian news
```bash
cyassist --news-india
```

### Scrape global security news
```bash
cyassist --news-web
```

### Harvest exploit DNA
```bash
cyassist --harvest
```

### Look up CVEs for a technology
```bash
cyassist --tech apache
cyassist --tech nginx
cyassist --tech wordpress
```

### Generate probe config for a CVE
```bash
cyassist --cve CVE-2021-44228
```

### Run daily auto-update (scrape + harvest + sync)
```bash
cyassist --daily
```

### Watch mode (poll every 10 minutes)
```bash
cyassist --watch --watch-interval 600
```

---

## 5. Command-Line Flags

| Flag | Description |
|------|-------------|
| `--status` | Show intel DB stats (size, CVEs, exploits, news, targets) |
| `--size` | Show only the DB size in MB |
| `--news-india` | Scrape Indian news sources (CERT-In, ET CISO, Quick Heal, Cyble, Seqrite, Payatu, CloudSEK, RBI) |
| `--news-web` | Scrape global web news (THN, BleepingComputer, GBHackers, PacketStorm, Reddit, X/Twitter) |
| `--harvest` | Harvest exploit DNA from Exploit-DB RSS |
| `--harvest-cve CVE` | Harvest GitHub PoCs for a specific CVE |
| `--sync-templates` | Index Nuclei + Metasploit templates |
| `--check-templates` | Check if template directories exist |
| `--tech TECH` | Look up CVEs for a technology (e.g. apache, nginx, spring) |
| `--cve CVE-ID` | Generate Rudra probe config for a CVE |
| `--auto-scan URL` | Generate full Rudra scan config for a target URL |
| `--fetch-exploit URL` | Fetch exploit code from URL (read-only, never cached) |
| `--fetch-cve CVE-ID` | Show stored exploit URLs for a CVE |
| `--nuclei URL` | Run nuclei templates against a target |
| `--nuclei-cve CVE-ID` | Filter nuclei templates to a specific CVE |
| `--watch` | Watch mode — poll for new CVEs, alert on changes |
| `--watch-interval N` | Watch polling interval in seconds (default: 300) |
| `--auto-scan-watch` | Auto-trigger Rudra scans on relevant CVEs (watch mode) |
| `--reader` | Launch the news reader (reader.py) |
| `-i`, `--india` | India preset scope — auto-launches reader with 3-color flag logo; falls back to 7 days if no recent India news |
| `-t`, `--today` | Launch reader in today's headlines mode |
| `-T`, `--headlines` | Launch reader in quick headlines mode |
| `-H`, `--summary` | Launch reader in summary mode |
| `-c`, `--category` | Filter reader by category (news\|techniques) |
| `-q`, `--query` | Search keyword via reader |
| `-s`, `--source` | Filter by source name via reader |
| `-n`, `--count` | Count-only mode via reader |
| `--hunt` | Run the hunting pipeline (hunter.py) |
| `--poc` | Show PoCs from the hunter |
| `--daily` | Full auto-run: scrapers → harvest → template sync → bridge |

---

## 6. Sub-Modules

| Module | File | Purpose |
|--------|------|---------|
| Intel DB | `intel_db.py` | SQLite database wrapper, 8 tables, WAL mode |
| India Scraper | `scraper_india.py` | 8 Indian cybersecurity news sources |
| Web Scraper | `scraper_web.py` | 10+ global news/scocial sources |
| DNA Harvester | `harvester.py` | Exploit-DB + GitHub exploit metadata |
| Template Sync | `template_sync.py` | Nuclei YAML + Metasploit .rb indexing |
| Rudra Bridge | `rudra_bridge.py` | Tech→CVE→Sink→Probe pipeline bridge |
| On-Demand | `on_demand.py` | Exploit code fetch + watch mode |
| CLI | `cyassist.py` | Unified entry point, dispatches all modules |
| Reader | `reader.py` | News reader with Indian keywords |
| Hunter | `hunter.py` | Hunting pipeline (legacy) |

---

## 7. Intel DB

The SQLite database at `~/.local/share/cyassist/intel.db` is the central store.

### Tables

| Table | Records | Content |
|-------|---------|---------|
| `cves` | CVE metadata | CVSS, EPSS, KEV status, techniques, descriptions |
| `exploits` | Exploit DNA | technique, sink_type, parameter_template, payload_template, URL |
| `templates` | Template IDs | nuclei_template_id, metasploit_module, CVE ref |
| `tech_cve` | Tech→CVE map | technology, CVE_ID, version_range, sink_type |
| `news` | News articles | source, URL, title, body_snippet (≤500 chars), tags |
| `news_sources` | Source metadata | name, URL, last_scraped, enabled |
| `seen_ids` | Dedup tracking | hash of seen article/exploit URLs |
| `targets` | Registered targets | name, URL, techs, auth_config (from targets.yaml) |

### Storage Budget

- Empty DB: ~0.08MB
- 100K entries: ~1MB
- Target: `<100MB` for years of operation

---

## 8. Indian News Scraping

8 dedicated Indian cybersecurity sources with dual-write to flat files + SQLite:

| Source | URL | Type |
|--------|-----|------|
| CERT-In | cert-in.org.in | Government advisories |
| ET CISO | ciso.economictimes.indiatimes.com | News |
| Quick Heal | quickheal.com/blog | Vendor blog |
| Cyble Blog | cyble.com/blog | Research |
| Seqrite Blog | seqrite.com/blog | Vendor blog |
| Payatu Blog | payatu.com/blog | Research |
| CloudSEK Blog | cloudsek.com/blog | Research |
| RBI Advisories | rbi.org.in | Regulatory |

Run: `cyassist --news-india`

---

## 9. Web News Scraping

Global security news from 10+ sources, stored directly to SQLite:

| Source | Method |
|--------|--------|
| The Hacker News | RSS |
| BleepingComputer | RSS |
| GBHackers | RSS |
| PacketStorm | RSS |
| Reddit (netsec, hacking, cybersecurity, bugbounty) | RSS |
| X/Twitter (vxunderground, PwnAllTheThings, binitamshah, 0xor0ne) | Nitter RSS |

Run: `cyassist --news-web`

---

## 10. Exploit DNA Harvesting

Harvests exploit metadata (never code) from two sources:

### Exploit-DB RSS
- Fetches latest 50 exploits
- Classifies technique (sqli, xss, rce, path_traversal, etc.)
- Maps to Rudra sink types
- Extracts parameter/payload templates
- Stores: `{cve_id, technique, sink_type, parameter_template, payload_template, url}`
- **No exploit code stored** — DNA only

### GitHub API
- Searches for PoC repos by CVE ID
- Stores repo URL and metadata

Run: `cyassist --harvest`  
Run for specific CVE: `cyassist --harvest-cve CVE-2024-XXXXX`

### Technique Classification

| Pattern | Technique | Sink Type |
|---------|-----------|-----------|
| sql injection, sqli | sqli | sql_injection |
| cross site scripting, xss | xss | xss |
| remote code execution, rce | rce | command_injection |
| path traversal, directory traversal | path_traversal | path_traversal |
| server side request forgery, ssrf | ssrf | ssrf |
| local file inclusion, lfi | lfi | lfi |
| command injection, cmdi | cmdi | command_injection |
| server side template, ssti | ssti | ssti |
| authentication bypass, auth bypass | auth_bypass | auth_bypass |
| idor, insecure direct object | idor | idor |
| cross site request forgery, csrf | csrf | csrf |
| open redirect | open_redirect | open_redirect |
| mass assignment, mass_assignment | mass_assignment | mass_assignment |
| prototype pollution | prototype_pollution | prototype_pollution |

---

## 11. Template Sync

Indexes vulnerability templates without downloading the actual files:

### Nuclei Templates
- Scans local `nuclei-templates/` directory
- Parses YAML for CVE references
- Stores: `{template_id, cve_id, severity, technique}`
- **No YAML stored** — IDs only

### Metasploit Modules
- Scans local Metasploit framework
- Parses .rb files for CVE references
- Stores: `{module_path, cve_id, technique}`

Run: `cyassist --sync-templates`  
Check: `cyassist --check-templates`

> **Note:** Requires `nuclei -ut` or `git clone` of nuclei-templates and Metasploit to function fully.

---

## 12. Rudra Bridge

The bridge between Cyassist intel and Rudra's scanning pipeline.

### Tech → CVE Lookup
```bash
cyassist --tech apache
```
Returns CVEs matching the technology from both the static map and the DB.

### CVE → Probe Config
```bash
cyassist --cve CVE-2021-44228
```
Generates a Rudra-compatible probe configuration with:
- Sink type (e.g. `command_injection`)
- Technique (e.g. `rce`)
- Parameter/payload hints from stored exploit DNA
- Associated Nuclei template IDs
- Exploit URLs for reference

### Auto-Scan Config
```bash
cyassist --auto-scan https://target.com
```
Detects technology stack from URL, generates full scan config:
- Probe count by sink type
- Nuclei template count
- Priority CVEs
- Ready-to-run Rudra command

### Finding Enrichment
```json
{
  "url": "https://target.com/api",
  "sink_type": "command_injection",
  "cve_matches": ["CVE-2021-44228"],
  "enriched_technique": "rce",
  "exploit_urls": ["https://exploit-db.com/..."],
  "nuclei_templates": ["CVE-2021-44228"]
}
```

### Static Tech→CVE Map

Built-in map covers 11 technologies:

| Technology | CVEs | Example |
|------------|------|---------|
| apache | 5 | CVE-2021-41773 (path traversal) |
| nginx | 3 | CVE-2021-23017 (DNS resolver) |
| spring | 2 | CVE-2022-22965 (Spring4Shell) |
| wordpress | 3 | CVE-2024-XXXXX (various) |
| servicenow | 2 | CVE-2024-XXXXX |
| jenkins | 3 | CVE-2024-XXXXX |
| next.js | 2 | CVE-2025-29927 (middleware) |
| cloudflare | 1 | CVE-2024-XXXXX |
| okta | 2 | CVE-2024-XXXXX |
| s3 | 2 | CVE-2024-XXXXX |
| graphql | 3 | introspection, batching |

### Target Import

Import targets from `targets.yaml` into the database:
```bash
cyassist --tech rudra
# Or directly via bridge:
python3 /home/kali/bugbounty/cyassist/rudra_bridge.py --import-targets
```

---

## 13. On-Demand Exploit Fetcher

Fetches exploit code read-only at query time. **No code is ever cached.**

### From Exploit-DB
```bash
cyassist --fetch-exploit https://www.exploit-db.com/exploits/52608
```
Searches GitLab's exploitdb mirror for the raw file by EDB ID. Tries root-level and common platform/type directories.

### From GitHub
```bash
cyassist --fetch-exploit https://github.com/rapid7/metasploit-framework
```
Fetches raw content from `raw.githubusercontent.com`. Tries common PoC filenames (exploit.py, poc.py, etc.) plus README fallback.

### By CVE (show stored URLs)
```bash
cyassist --fetch-cve CVE-2021-44228
```
Lists all stored exploit URLs for a CVE without fetching code.

### Nuclei On-Demand
```bash
cyassist --nuclei https://target.com --nuclei-cve CVE-2024-XXXXX
```
Runs nuclei against the target, optionally filtered to CVE-specific templates.

---

## 14. Watch Mode

Monitors the intel DB for new CVEs in real-time.

```bash
cyassist --watch
cyassist --watch --watch-interval 600  # every 10 minutes
```

### Features
- Polls the DB for CVEs added since last check
- Prints new CVEs with CVSS, EPSS, PoC status, KEV status
- Highlights high-EPSS and KEV entries
- Optional auto-scan: checks if any registered target matches the new CVE's technology

### Auto-Scan Mode
```bash
cyassist --watch --auto-scan-watch
```
When a new CVE matches a registered target's tech stack, prints a scan config without executing it. (Explicit opt-in design — you choose when to scan.)

---

## 15. Daily Auto-Run

Runs the full intel update pipeline:
```
scraper_india.py → scraper_web.py → harvester.py → template_sync.py → rudra_bridge.py --import-targets
```

```bash
cyassist --daily
```

### Cron Setup

Add to crontab:
```
0 6 * * * cd /home/kali/bugbounty/cyassist && python3 cyassist.py --daily >> /tmp/cyassist-daily.log 2>&1
```

Or use systemd timer (see `DAILY_CRON.md`).

---

## 16. Targets

Registered targets from `targets.yaml` are imported into the DB for auto-scan and watch mode.

### Current Targets

| Target | Domain | Techs |
|--------|--------|-------|
| indrive | *.indrive.com | istio, OAuth |
| shopify | *.shopify.com | Okta, Cloudflare |
| spotify | *.spotify.com | OAuth, PKCE |
| whatnot | *.whatnot.com | GraphQL, Cloudflare |
| playtika | *.playtika.com | ServiceNow, Cloudflare |
| epic-games | *.epicgames.com | GraphQL, Okta |
| x-twitter | x.com, twitter.com | Cloudflare, Envoy |

### Add a Target

Edit `targets.yaml`:
```yaml
- name: my-target
  url: https://my-target.com
  techs: [apache, wordpress]
  auth: null
```

Then import:
```bash
python3 /home/kali/bugbounty/cyassist/rudra_bridge.py --import-targets
```

---

## 17. Database Schema

```sql
CREATE TABLE cves (
    id TEXT PRIMARY KEY,
    cvss REAL,
    severity TEXT,
    epss REAL DEFAULT 0,
    in_kev INTEGER DEFAULT 0,
    has_poc INTEGER DEFAULT 0,
    techniques TEXT,
    description TEXT,
    affected_software TEXT,
    updated_at TEXT
);

CREATE TABLE exploits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cve_id TEXT REFERENCES cves(id),
    source TEXT,
    title TEXT,
    url TEXT UNIQUE,
    technique TEXT,
    sink_type TEXT,
    parameter_template TEXT,
    payload_template TEXT,
    target_software TEXT,
    version_range TEXT,
    tags TEXT,
    date TEXT
);

CREATE TABLE templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cve_id TEXT REFERENCES cves(id),
    source TEXT,
    template_id TEXT,
    severity TEXT,
    technique TEXT,
    UNIQUE(cve_id, source, template_id)
);

CREATE TABLE tech_cve (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology TEXT,
    cve_id TEXT REFERENCES cves(id),
    version_range TEXT,
    sink_type TEXT,
    technique TEXT,
    source TEXT,
    UNIQUE(technology, cve_id)
);

CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    url TEXT UNIQUE,
    title TEXT,
    date TEXT,
    tags TEXT,
    cve_refs TEXT,
    body_snippet TEXT
);

CREATE TABLE targets (
    name TEXT PRIMARY KEY,
    url TEXT,
    techs TEXT,
    auth_config TEXT,
    created_at TEXT
);
```

---

## 18. False Positive Prevention

Cyassist is designed to avoid the common bug-bounty pitfalls documented in `AGENTS.md`:

| Pitfall | Cyassist Mitigation |
|---------|---------------------|
| Staging bugs rarely pay | Target metadata in DB tracks prod vs staging |
| Next.js `__NEXT_DATA__` | Not indexed — considered public-by-design |
| CORS without XSS | Rudra bridge requires XSS chain for CORS findings |
| Error messages without PII | Not classified as CVEs — filtered at harvest |
| Rate limiting alone | Marked informational unless chainable |
| Space-separated ACAO | Not flagged — browser-parser bug, not exploitable |
| curl PoC for CORS | On-demand fetch uses browser-like User-Agent for realistic testing |
| Mixing multiple bugs in one report | Each CVE/technique stored independently |
| "Could potentially" arguments | Only CVEs with PoC/KEV flagged as exploitable |

### Never-Report List

The following are automatically filtered from exploit intel:
- Next.js `__NEXT_DATA__` secrets
- Firebase API keys (public-by-design)
- DataDog RUM tokens (public-by-design)
- Sentry DSNs (public-by-design)
- Descriptive error messages without data access
- Missing security headers
- Rate limiting without chain
- CORS wildcard without credentials
- Open redirect without chain
- Version disclosure

---

## Appendix A: File Reference

| File | Lines | Purpose |
|------|-------|---------|
| `cyassist.py` | 225 | Unified CLI entry point |
| `intel_db.py` | 360 | SQLite database wrapper |
| `scraper_india.py` | 353 | Indian news scrapers |
| `scraper_web.py` | 334 | Global web news scrapers |
| `harvester.py` | 312 | Exploit DNA harvester |
| `template_sync.py` | 150+ | Template indexer |
| `rudra_bridge.py` | 475 | Rudra integration bridge |
| `on_demand.py` | 290 | On-demand fetcher + watch |
| `reader.py` | 700+ | News reader (existing) |
| `hunter.py` | 300+ | Hunting pipeline (existing) |

## Appendix B: Storage Budget Tracking

| Category | Current | Projected (1 year) |
|----------|---------|-------------------|
| CVEs | 0 (DB empty) | ~10,000 (2MB) |
| Exploits | 50 | ~5,000 (1MB) |
| Templates | 0 | ~50,000 (5MB) |
| Tech→CVE | 0 (static only) | ~5,000 (0.5MB) |
| News | 117 | ~30,000 (3MB) |
| Targets | 0 | ~50 (0.01MB) |
| **Total** | **0.13MB** | **~12MB** |

Target: `<100MB`. Even at 10× growth, Cyassist stays well under budget.
