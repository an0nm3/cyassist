---
source: rss/sensepost
title: Decrypting iPhone Apps
url: https://sensepost.com/blog/2011/decrypting-iphone-apps/
date: 2011-10-24
item_id: https://sensepost.com/blog/2011/decrypting-iphone-apps/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2011/decrypting-iphone-apps/

This blog post steps through how to convert encrypted iPhone application bundles into plaintext application bundles that are easier to analyse. 
 Requirements: 
1)	Jailbroken iPhone with OpenSSH, gdb plus other utilities (com.ericasadun.utilities etc. etc.) 
2)	An iPhone app 
3)	On your machine: 
 
 otool (comes with iPhone SDK) 
 Hex editor (0xED, HexWorkshop etc.) 
 Ida &#8211; Version 5.2 through 5.6 supports remote debugging of iPhone applications (iphone_server). 
 
 For this article, I will use the app name as “blah”.
