---
source: rss/sensepost
title: OpenSSL, Certpinning and  Memory patching. Sounds fun right?
url: https://sensepost.com/blog/2026/openssl-certpinning-and-memory-patching.-sounds-fun-right/
date: 2026-04-01
item_id: https://sensepost.com/blog/2026/openssl-certpinning-and-memory-patching.-sounds-fun-right/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2026/openssl-certpinning-and-memory-patching.-sounds-fun-right/

This blogpost will cover the research I presented at  BSides JoBurg . You can  watch the talk on YouTube , and code can be found on  our GitHub page .  
 This journey started after having looked at some certificate-pinned apps. 
 The majority of apps that appear to implement cert pinning, don&#8217;t actually have cert pinning but rather just use a custom trust manager or are not proxy aware (this also applies to things like Flutter). Thus the first step is to ensure application traffic is forced through our proxy. I utilised an OpenVPN server when working with a physical device and the Android emulator proxy settings when working with a virtual device.
