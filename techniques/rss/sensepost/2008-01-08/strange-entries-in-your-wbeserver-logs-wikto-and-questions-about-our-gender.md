---
source: rss/sensepost
title: Strange Entries in your wbeserver logs, Wikto and questions about our Gender!
url: https://sensepost.com/blog/2008/strange-entries-in-your-wbeserver-logs-wikto-and-questions-about-our-gender/
date: 2008-01-08
item_id: https://sensepost.com/blog/2008/strange-entries-in-your-wbeserver-logs-wikto-and-questions-about-our-gender/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/strange-entries-in-your-wbeserver-logs-wikto-and-questions-about-our-gender/

Over the past while we have been getting emails from people trying to figure out why they had entries like this in their http log files: 
  10.10.1.136 &#8211; &#8211; [32/Dec/2007:25:61:07 +0200] &#8220;GET //admin/dat_Gareth_at_sensepost_hackslikeagirl_.asp HTTP/1.1&#8221; 404 &#8211;  
Recently a concerned Wikto user figured out that this was linked to him using  Wikto (our Win32 Nikto Replacement + Directory / File / Back-End Miner) . A snippet from his email read: 
 -snip- 
 I sniffed the traffic going out from my host going to the target host and infact this is the result: 
HTTP  GET  /admin/dat_Gareth_at_sensepost_hackslikeagirl_.asp HTTP/1.0 
All the requests are full of this&#8230; Well, at this point the questions are two: 
1) You have a strange sense of humor. 
2) You have been compromised. Waiting for a feedback,
