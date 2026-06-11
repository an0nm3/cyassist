---
source: rss/0xdf-writeups
title: HTB: DarkZero
url: https://0xdf.gitlab.io/2026/04/04/htb-darkzero.html
date: 2026-04-04
item_id: https://0xdf.gitlab.io/2026/04/04/htb-darkzero.html
category: techniques
tags: [CVE]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/04/04/htb-darkzero.html

DarkZero is an assume breach Windows box with two forests connected by a bidirectional cross-forest trust. Starting with given credentials, I’ll enumerate MSSQL on DC01 and find a linked server to DC02 in the other forest where the mapped account is sysadmin. I’ll enable xp_cmdshell on DC02 to get a shell as the SQL service account. To escalate to SYSTEM on DC02, I’ll show four paths: recovering SeImpersonatePrivilege from the original logon token via named pipe impersonation, using ADCS certificate enrollment to get an NT hash and change the password for a service logon with RunAsCS, NTLM authentication reflection using the CMTI DNS record trick to relay the machine account back to its own LDAPS, and CVE-2024-30088. As SYSTEM on DC02, I’ll abuse the cross-forest TGT delegation to capture DC01’s machine account TGT and use it to dump all domain hashes from DC01.
