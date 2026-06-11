---
source: rss/sensepost
title: PowerShell, C-Sharp and DDE The Power Within
url: https://sensepost.com/blog/2016/powershell-c-sharp-and-dde-the-power-within/
date: 2016-05-20
item_id: https://sensepost.com/blog/2016/powershell-c-sharp-and-dde-the-power-within/
category: techniques
tags: [Exploit, Race condition]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2016/powershell-c-sharp-and-dde-the-power-within/

aka Exploiting MS16-032 via Excel DDE without macros. The modified exploit script and video are at the end. 
 A while ago this cool  PowerShell exploit for MS16-032  was released by FuzzySecurity. The vulnerability exploited was in the secondary login function, which had a race condition for a leaked elevated thread handle, we wont go into much details about the vulnerability here though. It is a really awesome vulnerability if you want to read more details about it, I suggest you read  James Forshaw&#8217;s blog post at Project Zero .
