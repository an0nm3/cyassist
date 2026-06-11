---
source: rss/0xdf-writeups
title: HTB: MonitorsFour
url: https://0xdf.gitlab.io/2026/05/23/htb-monitorsfour.html
date: 2026-05-23
item_id: https://0xdf.gitlab.io/2026/05/23/htb-monitorsfour.html
category: techniques
tags: [Bypass, CVE, Exploit]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/05/23/htb-monitorsfour.html

MonitorsFour continues the Monitors series, this time on a Windows host. A company website exposes an authenticated API endpoint that returns every employee’s record. I’ll bypass auth with a PHP type juggling flaw to dump a collection of crackable password hashes. Those credentials open a Cacti instance, where I’ll exploit CVE-2025-24367 to inject commands into rrdtool and drop a webshell, landing in a Docker container. Enumeration shows the host is running Docker Desktop on a WSL2 backend, and that the container can reach the Docker Engine API directly (CVE-2025-9074). I’ll create a new container that mounts the Windows host’s drive and read the root flag. In Beyond Root, I’ll turn that filesystem access into a shell on Windows through a scheduled task, and break down the PHP type juggling bug.
