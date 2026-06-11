---
source: rss/sensepost
title: Is URL / Variable Name the new Port Number ??
url: https://sensepost.com/blog/2008/is-url-/-variable-name-the-new-port-number/
date: 2008-01-10
item_id: https://sensepost.com/blog/2008/is-url-/-variable-name-the-new-port-number/
category: techniques
tags: [Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/is-url-/-variable-name-the-new-port-number/

There has been a fair bit of blog buzz about the new SQL Injection worm that ran around infecting sites. I have not looked too deeply into it, but have not yet seen accounts of how the targeting was done. Since the sites do not appear to have been running a common framework i would guess that it was search-engine generated targets based on resource name (like inurl: search.asp).. 
 For ages we have been telling people that if they had to have a /admin/admin.asp on their internet facing web-app that they would at least help minimize their exposure a little by naming it /admin_[bet_u_dont_find_this]/admin_[another_variable].asp
