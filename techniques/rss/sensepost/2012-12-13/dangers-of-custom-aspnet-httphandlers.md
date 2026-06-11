---
source: rss/sensepost
title: Dangers of Custom ASP.NET HttpHandlers
url: https://sensepost.com/blog/2012/dangers-of-custom-asp.net-httphandlers/
date: 2012-12-13
item_id: https://sensepost.com/blog/2012/dangers-of-custom-asp.net-httphandlers/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2012/dangers-of-custom-asp.net-httphandlers/

ASP.NET HttpHandlers  are interesting components of a .NET web application when performing security assessments, mainly due to the fact they are the most exposed part of the application processing client requests in HttpContext level and at the same time, not yet part of the official ASP.NET framework. 
 As a result, data validation vulnerabilities in custom HttpHandlers can be exploited far easier than issues on the inner layer components. However, they are mostly overlooked during the web application tests for two reasons:
