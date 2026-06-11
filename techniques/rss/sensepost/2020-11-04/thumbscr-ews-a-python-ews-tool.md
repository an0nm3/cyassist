---
source: rss/sensepost
title: thumbscr-ews – a python EWS tool
url: https://sensepost.com/blog/2020/thumbscr-ews-a-python-ews-tool/
date: 2020-11-04
item_id: https://sensepost.com/blog/2020/thumbscr-ews-a-python-ews-tool/
category: techniques
tags: [Bypass]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/thumbscr-ews-a-python-ews-tool/

Something I have found myself doing more and more often is using Exchange Web Services (EWS) to bypass 2FA. I do this so that I could look through mail for accounts I have compromised. The 2FA bypass is due to a common misconfiguration which can leave EWS unprotected, and has been known about for ages, mostly from the  Black Hills  post in 2016. However, most of the tooling appears to be written in PowerShell, and being the lazy person I am I prefer not to start up a Windows VM when I want to see if I can access a persons email. Hence I started just using a small script around the amazing  exchangelib  where I would just retrieve the top 10 emails using the example provided in the help documentation. I was doing this often enough that I decided to make a more useful tool.
