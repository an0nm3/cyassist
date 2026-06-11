---
source: rss/sensepost
title: BlackHat Write-up: go-derper and mining memcaches
url: https://sensepost.com/blog/2010/blackhat-write-up-go-derper-and-mining-memcaches/
date: 2010-08-04
item_id: https://sensepost.com/blog/2010/blackhat-write-up-go-derper-and-mining-memcaches/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2010/blackhat-write-up-go-derper-and-mining-memcaches/

[Update: Disclosure and other points discussed in a little more detail  here .] 
 Why memcached? 
 At BlackHat USA last year we spoke about attacking cloud systems, while the thinking was broadly applicable, we focused on specific providers ( overview ). This year, we continued in the same vein except we focused on a particular piece of software used in numerous large-scale application including many cloud services. In the realm of &#8220;software that enables cloud services&#8221;, there appears to be a handful of &#8220;go to&#8221; applications that are consistently re-used, and it&#8217;s curious that a security practitioner&#8217;s perspective has not as yet been applied to them (disclaimer: I&#8217;m not aware of parallel work).
