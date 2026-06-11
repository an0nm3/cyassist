---
source: rss/sensepost
title: From 500 to Account Takeover
url: https://sensepost.com/blog/2021/from-500-to-account-takeover/
date: 2021-03-02
item_id: https://sensepost.com/blog/2021/from-500-to-account-takeover/
category: techniques
tags: [Bypass, Xss]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2021/from-500-to-account-takeover/

Introduction 
 What seemed like a regular Cross-site Scripting (XSS) vulnerability on an HTTP 500 &#8220;Internal Server Error&#8221;-page, I managed to turn into a one-click account takeover on an assessment. In this blog post I want to describe the path I took to achieve this leveraging a known Cloudflare WAF bypass and Google analytics to extract session tokens serving as a CSP bypass. 
 Reconnaissance 
 At the beginning of the assessment, it quickly came to my attention that the web application stored the Session ID as part of some kind of error reporting JavaScript function in a  message  variable. This function would be executed if  window.error  was triggered:
