# Security Intel Repository

Automatically collected bug bounty techniques, PoCs, bypasses, and security research.
Sourced from 70+ RSS feeds, Telegram channels, and web scrapers.

## Contents

```
techniques/
├── rss/            # Blog posts, research papers, writeups
│   ├── portswigger-research/
│   ├── projectdiscovery-blog/
│   ├── assetnote-blog/
│   ├── ncc-group-research/
│   └── ... (30+ sources)
├── telegram/       # Telegram channel posts
│   ├── bug_bounty_channel/
│   ├── thebugbountyhunter/
│   ├── github_repos/
│   ├── brutsecurity/
│   └── cybdetective/
└── ... (organized by source → date)
```

## Format

Each file is a markdown document with YAML front-matter:

```yaml
---
title: "SSRF bypass via DNS rebinding"
source: "rss/assetnote-blog"
date: "2026-06-11"
category: "techniques"
tags: [SSRF, bypass, dns]
url: "https://blog.assetnote.io/..."
---
```

## Auto-updated

This repo is updated automatically by [intel-collector](https://github.com/an0nm3/intel-collector).
New techniques are committed and pushed as they're discovered.

## Usage

```bash
git clone https://github.com/an0nm3/intel-repo.git
cd intel-repo

# Search techniques by keyword
grep -r "prototype pollution" techniques/

# Find CVEs
grep -r "CVE-2026-" techniques/

# List all unique sources
find techniques -name "*.md" -exec grep -h "^source:" {} \; | sort -u
```
