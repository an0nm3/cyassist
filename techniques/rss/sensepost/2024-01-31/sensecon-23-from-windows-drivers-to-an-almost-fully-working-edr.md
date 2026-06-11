---
source: rss/sensepost
title: Sensecon 23: from Windows drivers to an almost fully working EDR
url: https://sensepost.com/blog/2024/sensecon-23-from-windows-drivers-to-an-almost-fully-working-edr/
date: 2024-01-31
item_id: https://sensepost.com/blog/2024/sensecon-23-from-windows-drivers-to-an-almost-fully-working-edr/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2024/sensecon-23-from-windows-drivers-to-an-almost-fully-working-edr/

TL;DR I wanted to better understand EDR&#8217;s so I built a  dummy EDR  and talk about it here.  
 EDR ( E ndpoint  D etection and  R esponse) is a kind of security product that aims to detect abnormal activities being executed on a computer or a server. 
 When looking for resources about how EDR&#8217;s work, I realised that, even if there is a lot of literature available about EDR&#8217;s, there aren&#8217;t many articles explaining how an EDR&#8217;s is architected and how the different components of a EDR are orchestrated. This article aims to demystify how EDR&#8217;s work while building a custom one that will implement a few techniques used by real EDR&#8217;s.
