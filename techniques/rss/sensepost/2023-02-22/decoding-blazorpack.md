---
source: rss/sensepost
title: Decoding BlazorPack
url: https://sensepost.com/blog/2023/decoding-blazorpack/
date: 2023-02-22
item_id: https://sensepost.com/blog/2023/decoding-blazorpack/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/decoding-blazorpack/

TL;DR: I couldn&#8217;t make a custom BlazorPack editor work in Burp, so I used Mallet instead. From an indecipherable binary mess to this, in about  100 lines : 
     Decoded BlazorPack messages  
 For details on how to do this yourself, even for other protocols, read on! 
 On a recent assessment,  Marianka  ran into a website using BlazorPack. As Microsoft describes it: &#8220;Today&#8217;s modern apps are expected to deliver up-to-date information without hitting a refresh button. Add real-time functionality to your dashboards, maps, games and more.&#8221;
