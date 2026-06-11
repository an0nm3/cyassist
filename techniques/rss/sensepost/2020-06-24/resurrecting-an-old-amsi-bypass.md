---
source: rss/sensepost
title: Resurrecting an old AMSI Bypass
url: https://sensepost.com/blog/2020/resurrecting-an-old-amsi-bypass/
date: 2020-06-24
item_id: https://sensepost.com/blog/2020/resurrecting-an-old-amsi-bypass/
category: techniques
tags: [Bypass]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/resurrecting-an-old-amsi-bypass/

While working on  DoubleAgent  as part of the  Introduction To Red Teaming  course we&#8217;re developing for  RingZer0 , I had a look at Anti-Malware Scan Interface (AMSI) bypasses. One of the objectives I had was to find a new way to evade AMSI. As with my DoubleAgent work, this did not lead to the identification of a novel finding, but instead revealed that old techniques can be revived with minimal work. This blog post describes how to resurrect the original  DLL hijack  documented by  Cn33liz  by extending it to simply define the typically exported functions found in  amsi.dll  in a fake DLL. This gives a low privileged user an AMSI bypass if they can write to a directory.
