---
source: rss/sensepost
title: HTTPS  via WinAPI
url: https://sensepost.com/blog/2012/https-via-winapi/
date: 2012-11-19
item_id: https://sensepost.com/blog/2012/https-via-winapi/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2012/https-via-winapi/

Hijacking SSL sessions initiated by the browser is a trivial task. The challenge comes when trying to intercept SSL traffic in applications such as Dropbox or Easynote. These apps create additional measures to verify certificates and their integrity, hence not very friendly to perform with Burp. 
 One quick solution to the above problem is hiding one level above (or below :) the OSI layer. Live API monitoring // hooking can be used to capture and manipulate  HTTP/S &#8220;traffic&#8221; before it being placed on the wire, more or less the same way are used to doing it in Burp.
