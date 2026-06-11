---
source: rss/sensepost
title: Efficient HTTP Scripting in the Shell
url: https://sensepost.com/blog/2018/efficient-http-scripting-in-the-shell/
date: 2018-09-05
item_id: https://sensepost.com/blog/2018/efficient-http-scripting-in-the-shell/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2018/efficient-http-scripting-in-the-shell/

Javier had a simple shell script he posted to our internal chat a few days ago. It&#8217;s goal was to pull all the IP ranges for a country in preparation for a footprint from https://ipinfo.io/ (Let&#8217;s use PL as an example). Given this involved pulling multiple webpages, I was interested to know what the most efficient approach to this in the shell would be. Truthfully, the actual problem, pulling data from the site or gathering BGP routes, didn&#8217;t interest me, I wanted to look at how to do mass HTTP enum most efficiently with curl.
