---
source: rss/sensepost
title: A journey implementing Channel Binding on MSSQLClient.py
url: https://sensepost.com/blog/2025/a-journey-implementing-channel-binding-on-mssqlclient.py/
date: 2025-07-25
item_id: https://sensepost.com/blog/2025/a-journey-implementing-channel-binding-on-mssqlclient.py/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/a-journey-implementing-channel-binding-on-mssqlclient.py/

A few weeks ago my friend  Zblurx  pushed a PR to Impacket in which he implemented the Channel Binding Token computation based on code that was developed by  @lowercase_drm  for the  ldap3 library . This PR allowed any tool relying on the ldap3 library to be able to connect to LDAP servers even if LDAP signing and LDAPS channel binding are enabled. Looking at the code I thought it would be easy to implement the same mechanism on other protocols such as MSSQL which I was already working on pushing as  PRs on NetExec .
