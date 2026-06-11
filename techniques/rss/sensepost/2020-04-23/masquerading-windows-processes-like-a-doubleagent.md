---
source: rss/sensepost
title: Masquerading Windows processes like a DoubleAgent.
url: https://sensepost.com/blog/2020/masquerading-windows-processes-like-a-doubleagent./
date: 2020-04-23
item_id: https://sensepost.com/blog/2020/masquerading-windows-processes-like-a-doubleagent./
category: techniques
tags: [Bypass, Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/masquerading-windows-processes-like-a-doubleagent./

I&#8217;ve been spending some time building new content for our  Introduction to Red Teaming course , which has been great for diving into AV/EDR bypass techniques again. In this blog post, I will demonstrate how to re-weaponise the old &#8220;DoubleAgent&#8221; technique, making endpoint security products do the hacking work for us. 
 One known vector to shimmy past AV solutions is to use process injections. At BlackHat 2019, a number of process injection techniques were  presented  by Itzik Kotler. A typical code injection implementation using known WINAPI functions, such as the combination of  VirtualAlloc ,  WriteProcessMemory  and  CreateRemoteThread  are well known by endpoint security solutions and will often raise alerts. Whether static or dynamic analysis kicks in, the chances of remaining undetected when using these functions are close to  NULL . Alas, the cat and mouse game keeps going endlessly.
