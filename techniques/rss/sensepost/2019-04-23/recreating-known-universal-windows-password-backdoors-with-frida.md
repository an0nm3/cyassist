---
source: rss/sensepost
title: recreating known universal windows password backdoors with Frida
url: https://sensepost.com/blog/2019/recreating-known-universal-windows-password-backdoors-with-frida/
date: 2019-04-23
item_id: https://sensepost.com/blog/2019/recreating-known-universal-windows-password-backdoors-with-frida/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2019/recreating-known-universal-windows-password-backdoors-with-frida/

tl;dr 
 I have been actively using  Frida  for little over a year now, but primarily on mobile devices while building the  objection  toolkit. My interest in using it on other platforms has been growing, and I decided to play with it on Windows to get a feel. I needed an objective, and decided to try port a well-known local Windows password backdoor to Frida. This post is mostly about the process of how Frida will let you quickly investigate and prototype using dynamic instrumentation.
