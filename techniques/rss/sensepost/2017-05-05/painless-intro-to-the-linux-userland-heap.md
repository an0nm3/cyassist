---
source: rss/sensepost
title: Painless intro to the Linux userland heap
url: https://sensepost.com/blog/2017/painless-intro-to-the-linux-userland-heap/
date: 2017-05-05
item_id: https://sensepost.com/blog/2017/painless-intro-to-the-linux-userland-heap/
category: techniques
tags: [Exploit]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/painless-intro-to-the-linux-userland-heap/

-1 – Pre-Intro 
 When looking at heap exploit tutorials most of the time I found myself lacking knowledge on the actual implementation and, soon, had the urge of knowing how it&#8217;s allocated and freed and why it&#8217;s done that way, memory wise. 
 -0.9 – ptmalloc2 
 The best source of knowledge with regards to the implementation of the heap is itself, the source code. Do not fear it, thankfully it is widely commented!
