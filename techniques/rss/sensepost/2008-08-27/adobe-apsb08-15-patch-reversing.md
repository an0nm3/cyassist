---
source: rss/sensepost
title: Adobe APSB08-15 Patch Reversing
url: https://sensepost.com/blog/2008/adobe-apsb08-15-patch-reversing/
date: 2008-08-27
item_id: https://sensepost.com/blog/2008/adobe-apsb08-15-patch-reversing/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/adobe-apsb08-15-patch-reversing/

APSB08-15  is the latest adobe security advisory regarding a memory corruption vulnerabilty in Acrobat Reader versions &lt;8.1.2 
 As expected, the advisory does not include technical details about the attack vector, So let&#8217;s try to reverse the related Adobe patch to find more about this vulnerability. I&#8217;m going to use IDA 5.2 with patchdiff2 plugin (thanks to kris hint on this plug-in). 
 The patch is released as a MSI file. I used Greg Duncan&#8217;s   Less MSIèrables   tool to examine the content of this patch:
