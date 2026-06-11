---
source: rss/sensepost
title: Is TLS more secure? The WinRMS case.
url: https://sensepost.com/blog/2025/is-tls-more-secure-the-winrms-case./
date: 2025-04-14
item_id: https://sensepost.com/blog/2025/is-tls-more-secure-the-winrms-case./
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/is-tls-more-secure-the-winrms-case./

0/ TL;DR 
  WinRM is protected against NTLMRelay as communications are encrypted. However WinRMS (the one communicating over HTTPS) is not entirely. That said, WinRMS is not configured on a default server installation (while WinRM is). So, if someone tried to harden their servers&#8217; configurations (by removing the HTTP endpoint), they would open a new possible target that can be used to relay HTTP/SMB and LDAP NTLMv1 only authentications to WinRMS and thus gain remote code execution.
