---
source: rss/0xdf-writeups
title: HTB: Eighteen
url: https://0xdf.gitlab.io/2026/04/11/htb-eighteen.html
date: 2026-04-11
item_id: https://0xdf.gitlab.io/2026/04/11/htb-eighteen.html
category: techniques
tags: [Exploit]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/04/11/htb-eighteen.html

Eighteen is a Windows Server 2025 assume-breach box starting with MSSQL credentials. I’ll use MSSQL login impersonation to access the financial planner database and recover a Werkzeug PBKDF2 hash for the web admin. After cracking the hash and spraying the password against domain users, I’ll get a WinRM shell. From there, I’ll identify that the domain is running at the Windows 2025 functional level and exploit Bad Successor, abusing the dMSA migration feature to create a delegated managed service account that inherits the Administrator’s group memberships, giving full domain admin access.
