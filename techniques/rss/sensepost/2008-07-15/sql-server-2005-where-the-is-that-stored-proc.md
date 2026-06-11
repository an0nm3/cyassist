---
source: rss/sensepost
title: SQL Server 2005 – Where the $%#@ is that stored proc ?
url: https://sensepost.com/blog/2008/sql-server-2005-where-the-%23@-is-that-stored-proc/
date: 2008-07-15
item_id: https://sensepost.com/blog/2008/sql-server-2005-where-the-%23@-is-that-stored-proc/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/sql-server-2005-where-the-%23@-is-that-stored-proc/

While doing some prodding on SQL Server, i came across this newness (of course this is probably old hat to many SQL2005 dba&#8217;s) 
 Essentially i was tryign to track down something in sp_addserver. 
 The source of this stored proc [ System Databases\Master\System Stored Procedures\sys.sp_addserver ] showed that another stored proc called:  sys.sp_MSaddserver_internal  was being called. 
 For the life of me though, i could not track down  sys.sp_MSaddserver_internal . 
 Turns out the answer is reasonably well documented [ SQL Books Online ], with 2005 &#8211; MSFT moved stored procs / and friends into a readonly hidden db. This can be made visible by copying the physical .mdf files and attaching them. [ Process reasonably documented on the interwebs if you know what to search for ]
