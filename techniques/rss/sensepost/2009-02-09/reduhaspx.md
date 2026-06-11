---
source: rss/sensepost
title: reDuh.ASPX
url: https://sensepost.com/blog/2009/reduh.aspx/
date: 2009-02-09
item_id: https://sensepost.com/blog/2009/reduh.aspx/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2009/reduh.aspx/

An additional issue has been discovered in the ASPX version of reDuh.  Although the script did work as expected, it did not set the ScriptTimeout value.  This resulted in reDuh terminating active connections once the page timeout had expired. 
 This has been fixed in the ASPX version.  A copy can be grabbed from  here .  More information regarding reDuh can be found  here .
