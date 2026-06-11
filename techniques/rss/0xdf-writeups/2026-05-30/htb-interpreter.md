---
source: rss/0xdf-writeups
title: HTB: Interpreter
url: https://0xdf.gitlab.io/2026/05/30/htb-interpreter.html
date: 2026-05-30
item_id: https://0xdf.gitlab.io/2026/05/30/htb-interpreter.html
category: techniques
tags: [Exploit]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/05/30/htb-interpreter.html

Interpreter is a Linux box hosting Mirth Connect, a Java-based healthcare integration engine. I’ll exploit an unauthenticated XStream deserialization vulnerability in the Mirth API to get remote code execution and a foothold as the mirth service account. From the Mirth config I’ll grab database credentials, dump a user password hash from MariaDB, and crack it to pivot to the next user. For root, I’ll abuse a localhost Flask notification server that wraps XML-supplied fields in an evaluated f-string, allowing Python code execution as root.
