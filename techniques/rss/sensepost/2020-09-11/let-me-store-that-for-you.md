---
source: rss/sensepost
title: Let me store that for you
url: https://sensepost.com/blog/2020/let-me-store-that-for-you/
date: 2020-09-11
item_id: https://sensepost.com/blog/2020/let-me-store-that-for-you/
category: techniques
tags: [CVE]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/let-me-store-that-for-you/

A while ago Jonas Lykkegaard disclosed a zeroday that could be used to create files in the SYSTEM folder. CVE-2020-16885 got assigned for this vulnerability, and was since patched with KB4580346. This vulnerability was very convenient for Dynamic-link library (DLL) side-loading, which I will show in this blog post. Below you can find  his  original Twitter message. 
  
  Unprivileged users are not allowed to create files in system32 folder- on hyper-v hosts they finally realised that unprivileged lives matters too as anyone can now create files there , with creater as owner, just open like this:  pic.twitter.com/Pd6nnqhcKZ
