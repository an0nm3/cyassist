---
source: rss/sensepost
title: Using & improving frida-trace
url: https://sensepost.com/blog/2025/using-improving-frida-trace/
date: 2025-03-19
item_id: https://sensepost.com/blog/2025/using-improving-frida-trace/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/using-improving-frida-trace/

TL;DR In this blog I want to show you how useful   frida-trace   can be at hooking thousands of methods at a time. I also wrote some scripts for improving its output a bit. 
 I often find that half of the problem is finding out what you don’t know. Take a mobile application for instance: 
 
 Which class is responsible for the SSL pinning? 
 Which class does the crypto? 
 What method is used to retrieve data from the local storage? 
 
 Once you have enough information, life becomes a lot easier. Unfortunately, finding this information can be difficult – especially when the mobile application you’ve been given is obfuscated beyond recognition, and the client refuses to provide you the original version, or the source code.
