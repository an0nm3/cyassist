<pre style="background:#0d1117;color:#e6edf3;font-family:monospace;padding:16px;border-radius:8px;line-height:1.4;font-weight:bold">
  <span style="color:#33cc33">▄▀▀▀  █   █ ▄▀▀▀▄ ▄▀▀▀▀ ▄▀▀▀▀  ▀  ▄▀▀▀▀ ▀▀█▀▀</span>
  <span style="color:#33cc33">█     ▀▄ ▄▀ █▀▀▀█  ▀▀▀▄  ▀▀▀▄  █   ▀▀▀▄   █</span>
  <span style="color:#33cc33"> ▀▀▀    █   ▀   ▀ ▀▀▀▀  ▀▀▀▀   ▀  ▀▀▀▀    ▀</span>
  <span style="color:#33cc33">       ▄▀</span>
  <span style="color:#33cc33">+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+</span>
  <span style="color:#33cc33">|C|Y|B|E|R| |G|L|O|B|A|L| |N|E|W|S|</span>
  <span style="color:#33cc33">+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+</span>
</pre>

<pre style="background:#0d1117;color:#e6edf3;font-family:monospace;padding:16px;border-radius:8px;line-height:1.4;font-weight:bold">
  <span style="color:#FF9933">▄▀▀▀  █   █ ▄▀▀▀▄ ▄▀▀▀▀ ▄▀▀▀▀  ▀  ▄▀▀▀▀ ▀▀█▀▀</span>
  <span style="color:#FF9933">█     ▀▄ ▄▀ █▀▀▀█  ▀▀▀▄  ▀▀▀▄  █   ▀▀▀▄   █</span>
  <span style="color:#FF9933"> ▀▀▀    █   ▀   ▀ ▀▀▀▀  ▀▀▀▀   ▀  ▀▀▀▀    ▀</span>
  <span style="color:#FF9933">       ▄▀</span>
  <span style="color:#FF9933">+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+-+-+</span>
  <span style="color:#e6edf3">|I|N|D|I|A|N| |C|Y|B|E|R| |N|E|W|S|</span>
  <span style="color:#138808">+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+-+-+</span>
</pre>

# Cyassist 🇮🇳 — Indian Cyber News

Daily cybersecurity news feed archive — auto-collected from 35+ RSS and Telegram sources. Built for the Indian bug bounty and security community.

Made with ❤️ by [**4n0n0n3**](https://github.com/4n0n0n3) (Pinaki Ranjan Patra) — [LinkedIn](https://www.linkedin.com/in/pinakirpatra/)

## Features

- **Live archive** — news fetched every 15 min via automated collector
- **Global edition** 🌐 — full cybersecurity news from 35+ sources
- **Indian edition** 🇮🇳 — filter by `-i` for India-relevant cybersecurity news
- **Searchable** — full-text grep across all articles
- **Public reader** — `reader.py` gives you terminal-based browsing

## Quick Start

```bash
git clone https://github.com/4n0n0n3/cyassist.git
cd cyassist

# Interactive reader
python3 reader.py

# India-specific news
python3 reader.py -i

# Headlines for last N days
python3 reader.py -H -d 3

# Search by keyword
python3 reader.py -s "ransomware"
```

<pre style="background:#0d1117;color:#e6edf3;font-family:monospace;padding:16px;border-radius:8px;line-height:1.4">
$ python3 reader.py
  <span style="color:#33cc33;font-weight:bold">▄▀▀▀  █   █ ▄▀▀▀▄ ▄▀▀▀▀ ▄▀▀▀▀  ▀  ▄▀▀▀▀ ▀▀█▀▀</span>
  <span style="color:#33cc33;font-weight:bold">█     ▀▄ ▄▀ █▀▀▀█  ▀▀▀▄  ▀▀▀▄  █   ▀▀▀▄   █</span>
  <span style="color:#33cc33;font-weight:bold"> ▀▀▀    █   ▀   ▀ ▀▀▀▀  ▀▀▀▀   ▀  ▀▀▀▀    ▀</span>
  <span style="color:#33cc33;font-weight:bold">       ▄▀</span>
  <span style="color:#33cc33;font-weight:bold">+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+</span>
  <span style="color:#33cc33;font-weight:bold">|C|Y|B|E|R| |G|L|O|B|A|L| |N|E|W|S|</span>
  <span style="color:#33cc33;font-weight:bold">+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+</span>
  <span style="color:#8b949e">────────────────────────────────────────────────────────────</span>
  Made by 🇮🇳 <span style="font-weight:bold">4n0n0n3</span>
  <span style="color:#8b949e">────────────────────────────────────────────────────────────</span>
</pre>

<pre style="background:#0d1117;color:#e6edf3;font-family:monospace;padding:16px;border-radius:8px;line-height:1.4">
$ python3 reader.py -i
  <span style="color:#FF9933;font-weight:bold">▄▀▀▀  █   █ ▄▀▀▀▄ ▄▀▀▀▀ ▄▀▀▀▀  ▀  ▄▀▀▀▀ ▀▀█▀▀</span>
  <span style="color:#FF9933;font-weight:bold">█     ▀▄ ▄▀ █▀▀▀█  ▀▀▀▄  ▀▀▀▄  █   ▀▀▀▄   █</span>
  <span style="color:#FF9933;font-weight:bold"> ▀▀▀    █   ▀   ▀ ▀▀▀▀  ▀▀▀▀   ▀  ▀▀▀▀    ▀</span>
  <span style="color:#FF9933;font-weight:bold">       ▄▀</span>
  <span style="color:#FF9933;font-weight:bold">+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+-+-+</span>
  <span style="color:#e6edf3">|I|N|D|I|A|N| |C|Y|B|E|R| |N|E|W|S|</span>
  <span style="color:#138808;font-weight:bold">+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+-+-+</span>
  <span style="color:#8b949e">────────────────────────────────────────────────────────────</span>
  Made by 🇮🇳 <span style="font-weight:bold">4n0n0n3</span>
  <span style="color:#8b949e">────────────────────────────────────────────────────────────</span>
</pre>

## Sources

```
news/
├── rss/            # Security news, breaches, CVEs from 35+ sources
└── ... (organized by source → date)
```

## Article Format

```yaml
---
title: "Critical RCE in popular VPN appliance"
source: "rss/the-register"
date: "2026-06-11"
category: "news"
tags: [CVE, RCE, VPN, critical]
url: "https://theregister.com/..."
---
```

## Automation

News is auto-collected via a systemd service running the [intel-collector](https://github.com/4n0n0n3/intel-collector) pipeline. New articles arrive every 15-30 minutes.
