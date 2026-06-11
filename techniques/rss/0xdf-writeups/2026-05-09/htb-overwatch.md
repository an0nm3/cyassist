---
source: rss/0xdf-writeups
title: HTB: Overwatch
url: https://0xdf.gitlab.io/2026/05/09/htb-overwatch.html
date: 2026-05-09
item_id: https://0xdf.gitlab.io/2026/05/09/htb-overwatch.html
category: techniques
tags: [Exploit, Injection]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/05/09/htb-overwatch.html

Overwatch starts with anonymous SMB access to a software share that hosts a custom .NET monitoring binary. I’ll reverse engineer it to recover SQL Server credentials and identify a WCF service with a PowerShell command injection sink. With the SQL creds, I’ll find a linked server pointing to a non-resolving host and abuse CREATE_CHILD on the AD-integrated DNS zone to add a record pointing the hostname at my host, capturing cleartext SQL authentication with Responder when the linked server connects out. Those credentials provide WinRM as a user in Remote Management Users. From there, I’ll exploit the WCF KillProcess command injection on a localhost SOAP endpoint to get code execution as SYSTEM, demonstrating four different ways to interact with the WCF service. In Beyond Root, I’ll look at a log that captured the Windows Administrator password from an HTB pre-release cleanup script.
