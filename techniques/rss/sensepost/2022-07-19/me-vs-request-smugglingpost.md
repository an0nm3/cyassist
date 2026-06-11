---
source: rss/sensepost
title: me vs request smugglingPOST
url: https://sensepost.com/blog/2022/me-vs-request-smugglingpost/
date: 2022-07-19
item_id: https://sensepost.com/blog/2022/me-vs-request-smugglingpost/
category: techniques
tags: [Exploit]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/me-vs-request-smugglingpost/

I&#8217;ve come to realise that I wasn&#8217;t the only one that has never actually exploited an  HTTP Request Smuggling  vulnerability, three years after  James Kettle  reminded the world of it. Like many, I&#8217;ve seen the buzz, read it all, thought I understood it, but honestly, I didn&#8217;t. While the potential impact sounds great from an attacker perspective, I&#8217;ve been mostly confused by a lot of it. That was until the  2022 HackTheBox Business CTF  challenge called PhishTale in the web category came around. Focussing less on the overall solving of the challenge and more on the request smuggling, in this post I&#8217;ll tell you about my journey of how I finally got to exploit an HTTP desync attack (specifically HTTP2 request smuggling).
