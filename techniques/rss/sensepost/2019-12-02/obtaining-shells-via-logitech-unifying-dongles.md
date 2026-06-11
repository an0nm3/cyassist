---
source: rss/sensepost
title: Obtaining shells via Logitech Unifying Dongles
url: https://sensepost.com/blog/2019/obtaining-shells-via-logitech-unifying-dongles/
date: 2019-12-02
item_id: https://sensepost.com/blog/2019/obtaining-shells-via-logitech-unifying-dongles/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2019/obtaining-shells-via-logitech-unifying-dongles/

In this post, I will recap some of the security research conducted on wireless keyboards and mice, and eventually show how current wireless keyboards and mice can be used to obtain a covert shell on a target computer. 
 Around 2009, Max Moser  realised  that most wireless keyboards were simply transmitting the keystrokes in clear text. His initial research targeted systems using 27MHz radios. In 2010, he presented  followup research  targeting systems using 2.4GHz radios, which suffered from similar vulnerabilities. Manufacturers responded ( eventually !) by encrypting the keystrokes, but most elected not to encrypt the mouse movements,  because that would introduce latency and increase power consumption for no real benefit.
