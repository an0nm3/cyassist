---
source: rss/sensepost
title: Google Docs XSS – no bounty today
url: https://sensepost.com/blog/2013/google-docs-xss-no-bounty-today/
date: 2013-03-04
item_id: https://sensepost.com/blog/2013/google-docs-xss-no-bounty-today/
category: techniques
tags: [Xss]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2013/google-docs-xss-no-bounty-today/

A few days ago, during one of those nights with the baby crying at 2:00 am and the only thing you can do is to read emails, I realised that Gmail shows the content of compressed files when reading them in Google Docs. As often is the case at SensePost, the &#8220;think evil &#8482;&#8221; came to me and I started to ponder the possibilities of injecting HTML inside the file listing.  The idea is actually rather simple. Looking at the file format of a .zip file we see the following:
