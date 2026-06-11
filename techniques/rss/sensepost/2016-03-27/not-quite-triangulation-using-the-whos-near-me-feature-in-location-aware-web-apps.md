---
source: rss/sensepost
title: Not-quite-triangulation using the who’s near me feature in location-aware web apps
url: https://sensepost.com/blog/2016/not-quite-triangulation-using-the-whos-near-me-feature-in-location-aware-web-apps/
date: 2016-03-27
item_id: https://sensepost.com/blog/2016/not-quite-triangulation-using-the-whos-near-me-feature-in-location-aware-web-apps/
category: techniques
tags: [Sqli, Xss]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2016/not-quite-triangulation-using-the-whos-near-me-feature-in-location-aware-web-apps/

When assessing web applications, we typically look for vulnerabilities such as SQLi and XSS, which are generally a result of poor input validation. However, logical input validation is just as important, and you can get tons of interesting info if it&#8217;s not done properly. 
 Take the plethora of mobile apps that let you find people that are using the same app nearby.  Logical validation on the coordinates you send should check that
