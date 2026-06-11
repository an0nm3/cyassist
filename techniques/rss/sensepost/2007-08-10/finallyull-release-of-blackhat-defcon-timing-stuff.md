---
source: rss/sensepost
title: F(inally)ull Release of BlackHat-Defcon Timing Stuff..
url: https://sensepost.com/blog/2007/finallyull-release-of-blackhat-defcon-timing-stuff../
date: 2007-08-10
item_id: https://sensepost.com/blog/2007/finallyull-release-of-blackhat-defcon-timing-stuff../
category: techniques
tags: [Exploit, Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2007/finallyull-release-of-blackhat-defcon-timing-stuff../

The  slides  |  tool  |  paper  from BlackHat07/DefCon07 have been posted online for your wget&#8217;ing pleasure. 
 More details on squeeza (the tool) can be found on the  squeeza page , but in a nutshell is a sql injection tool that uses Metasploits concept of splitting exploit/payloads/etc with SQL Injection attacks. Current modules are written for MS-SQL server but include functionality for (user defined sql queries, some db schema enumeration, command execution, file-transfer, db_info) and the information is returned (channel selection) via one of (application error messages, DNS, Timing). The modularity&#8217;ness means that these all mix and match &#8211; I.e. if you write a module to &#8220;extract data from all tables that look like username*&#8221;, the results would be available on any of the available channels.. (Its a pretty neat tool.. and saved our bacon more than once) So check it out, and send feedback to research@sensepost.com
