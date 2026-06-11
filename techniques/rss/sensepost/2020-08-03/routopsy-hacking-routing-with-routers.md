---
source: rss/sensepost
title: Routopsy – Hacking Routing with Routers
url: https://sensepost.com/blog/2020/routopsy-hacking-routing-with-routers/
date: 2020-08-03
item_id: https://sensepost.com/blog/2020/routopsy-hacking-routing-with-routers/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/routopsy-hacking-routing-with-routers/

This is a summary of our  BlackHat USA 2020  talk.  
  Introduction  
 On some of our engagements,  Szymon  and  I  found ourselves on various networks vulnerable to; insecure, misconfigured, and often overlooked networking protocols. These included dynamic routing protocols (referred to as  DRP &#8216;s) and first hop redundancy protocols (referred to as  FHRP &#8216;s). We decided to focus on these two classes of networking protocols to manipulate traffic flows and identify  non-conventional  ways of performing Person-in-the-Middle (PitM) attacks. This post details the results of that research and the tool we wrote to explore this attack surface. The tool is called Routopsy and is available on  Github .
