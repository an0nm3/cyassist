---
source: rss/xpn-infosec-blog
title: The SQL Server Crypto Detour
url: https://blog.xpnsec.com/the-sql-server-crypto-detour/
date: 2025-04-16
item_id: https://blog.xpnsec.com/the-sql-server-crypto-detour/
category: techniques---

**Source:** XPN InfoSec Blog
**Link:** https://blog.xpnsec.com/the-sql-server-crypto-detour/

One of the things that I love about my role at SpecterOps is getting to dig into various technologies and seeing the resulting research being used in real-time. This post will explore one such story of how I was able to go from a simple request of recovering credentials from a database backup, to reverse engineering how SQL Server encryption works, finding some new methods of brute-forcing database encryption keys.. and finally identifying a mistake in ManageEngine’s ADSelfService product which allows encrypted database backups to reveal privileged credentials.
