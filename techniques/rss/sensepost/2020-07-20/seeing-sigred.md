---
source: rss/sensepost
title: Seeing (Sig)Red
url: https://sensepost.com/blog/2020/seeing-sigred/
date: 2020-07-20
item_id: https://sensepost.com/blog/2020/seeing-sigred/
category: techniques
tags: [CVE, Poc, Rce]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/seeing-sigred/

After the SigRed (CVE-2020-1350)  write-up was published by Check Point , there was enough detailed information for the smart people, like  Hector  and others of the  Twitterverse  (careful with the  fake PoC !), to swiftly write a proof of concept to crash Windows DNS. CP did not publish enough details about how to convert this into an RCE, so it looks like a PoC to execute code is still going to take some time to surface. In this post I will describe how I created a Suricata rule to detect exploitation attempts of CVE-2020-1350.
