---
source: rss/sensepost
title: Revisting XXE and abusing protocols
url: https://sensepost.com/blog/2014/revisting-xxe-and-abusing-protocols/
date: 2014-01-28
item_id: https://sensepost.com/blog/2014/revisting-xxe-and-abusing-protocols/
category: techniques
tags: [Poc, Rce, Xxe]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2014/revisting-xxe-and-abusing-protocols/

Recently a security researcher reported a bug in Facebook that could potentially allow Remote Code Execution (RCE). His writeup of the incident is available  here  if you are interested. The thing that caught my attention about his writeup was not the fact that he had pwned Facebook or earned $33,500 doing it, but the fact that he used OpenID to accomplish this. After having a quick look at the output from the PoC and rereading the vulnerability description I had a pretty good idea of how the vulnerability was triggered and decided to see if any other platforms were vulnerable.
