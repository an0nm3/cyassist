---
source: rss/sensepost
title: Android Application Specific Proxies, Easy Mode
url: https://sensepost.com/blog/2021/android-application-specific-proxies-easy-mode/
date: 2021-01-29
item_id: https://sensepost.com/blog/2021/android-application-specific-proxies-easy-mode/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2021/android-application-specific-proxies-easy-mode/

In this post I want to share two things. First, a quick primer on how you would you go about navigating the source code when contributing to  objection , and secondly an application specific proxy feature I added to it.  
 Introduction 
 While on holiday I wanted to look into a certain mobile application that dealt with medical information. I was mostly interested in the data that was sent and received by the application so this meant proxying the traffic into Burp. I did not have a test device with me, so I had to use my personal device. This being my personal device meant that once I had the proxy set, certain applications would cease to function normally (especially those with SSL pinning) as Burp was in the middle.
