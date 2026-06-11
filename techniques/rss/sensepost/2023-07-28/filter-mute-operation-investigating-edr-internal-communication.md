---
source: rss/sensepost
title: Filter-Mute Operation: Investigating EDR Internal Communication
url: https://sensepost.com/blog/2023/filter-mute-operation-investigating-edr-internal-communication/
date: 2023-07-28
item_id: https://sensepost.com/blog/2023/filter-mute-operation-investigating-edr-internal-communication/
category: techniques
tags: [Exploit]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/filter-mute-operation-investigating-edr-internal-communication/

For our annual internal hacker conference dubbed SenseCon in 2023, I decided to take a look at communication between a Windows driver and its user-mode process. Here are some details about that journey. 
 TL;DR 
 Attackers could use Windows kernel R/W exploit primitive to avoid communication between EDR_Driver.sys and its EDR_process.exe. As a result some EDR detection mechanisms will be disabled and make it (partially) blind to malicious payloads. This blogpost describes an alternative approach which doesn&#8217;t remove kernel callbacks and gives some recommendations for protecting against this &#8220;filter-mute&#8221; attack.
