---
source: rss/sensepost
title: Being Stubborn Pays Off pt. 2 – Tale of two 0days on PRTG Network Monitor
url: https://sensepost.com/blog/2020/being-stubborn-pays-off-pt.-2-tale-of-two-0days-on-prtg-network-monitor/
date: 2020-05-22
item_id: https://sensepost.com/blog/2020/being-stubborn-pays-off-pt.-2-tale-of-two-0days-on-prtg-network-monitor/
category: techniques
tags: [CVE]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/being-stubborn-pays-off-pt.-2-tale-of-two-0days-on-prtg-network-monitor/

Intro 
 Last year I wrote  how to weaponize CVE-2018-19204 . This blog post will continue and elaborate on the finding and analysis of two additional vulnerabilities that were discovered during the process; one leading to an arbitrary write as system where the contents can&#8217;t be fully controlled and the other leading to Remote Code Execution as SYSTEM. Both vulnerabilities require you to have the administrator password for PRTG Network Monitor. Often you just get lucky, as the software defaults to  prtgadmin:prtgadmin  for the username and password respectively.
