---
source: rss/sensepost
title: Snoopy with Mana
url: https://sensepost.com/blog/2016/snoopy-with-mana/
date: 2016-09-14
item_id: https://sensepost.com/blog/2016/snoopy-with-mana/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2016/snoopy-with-mana/

In 2011 Glenn and Daniel released Snoopy, a set of tools for tracking and visualising wireless client activity. However, the Snoopy project is no longer maintained. This blog entry is about how I got Snoopy-like functionality built into Mana. 
 Snoopy&#8217;s core functionality was to observe probe requests for remembered networks from wireless clients, although it ended up doing much more. 
 The problem tools like Snoopy face, is that they can&#8217;t monitor the whole 2.4Ghz wireless spectrum for probe requests, without the use of multiple wireless cards. So they channel hop to make sure they see probes on multiple channels. In the 2.4Ghz range this wasn&#8217;t terrible, because the channels overlap, which means you didn&#8217;t have to tune in to all 11 or 14 (depending on location) channels individually to see probes across the spectrum. So while you may have missed a few probe requests, you didn&#8217; t miss many.
