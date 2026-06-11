---
source: rss/0xdf-writeups
title: HTB: Sorcery
url: https://0xdf.gitlab.io/2026/04/25/htb-sorcery.html
date: 2026-04-25
item_id: https://0xdf.gitlab.io/2026/04/25/htb-sorcery.html
category: techniques
tags: [Exploit, Injection, Rce, Ssrf, Xss]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/04/25/htb-sorcery.html

Sorcery is a Linux box with a Rust Rocket web app backed by Neo4j, Gitea, and a Kafka message bus. I’ll exploit Cypher injection in a derive-macro-generated query to leak the seller registration key, then use XSS in a product description to register a passkey on the admin account through a headless Chrome bot. I’ll also show a shortcut to change the admin’s password using cypher injection. As admin, a port-debug tool becomes an SSRF I can use to send Kafka wire protocol messages, which I’ll use to get RCE in the DNS container. From there, I’ll recover a CA keypair from FTP, phish the next user with mitmproxy proxying their own Gitea login page, read a password out of an Xvfb framebuffer, and reverse a .NET binary to generate OTPs for Docker Registry auth. Pulling layers out of a pushed image leaks another password, and the final pivots abuse FreeIPA roles to change one user’s password over LDAP and bootstrap sudo rights to root. I’ll show a couple unintended paths using pspy to capture creds as well.
