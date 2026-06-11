---
source: rss/sensepost
title: CertPotato – Using ADCS to privesc from virtual and network service accounts to local system
url: https://sensepost.com/blog/2022/certpotato-using-adcs-to-privesc-from-virtual-and-network-service-accounts-to-local-system/
date: 2022-11-04
item_id: https://sensepost.com/blog/2022/certpotato-using-adcs-to-privesc-from-virtual-and-network-service-accounts-to-local-system/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/certpotato-using-adcs-to-privesc-from-virtual-and-network-service-accounts-to-local-system/

The goal of this blog post is to present a privilege escalation I found while working on ADCS. We will see how it is possible to elevate our privileges to NT AUTHORITY\SYSTEM from virtual and network service accounts of a domain-joined machine (for example from a webshell on a Windows server) using ADCS. I want to call this attack chain &#8220;CertPotato&#8221; as homage to other *Potato tools and as a way to better remember it.
