---
source: rss/sensepost
title: Applescript for HTTP BruteForcing..
url: https://sensepost.com/blog/2008/applescript-for-http-bruteforcing../
date: 2008-01-01
item_id: https://sensepost.com/blog/2008/applescript-for-http-bruteforcing../
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/applescript-for-http-bruteforcing../

A long time ago i blogged on the joys of using VBS to automate bruteforcing [ 1 | 2 ]when one didnt want to mess about duplicating an applications functionality at the protocol level.. Yesterday i had need to brute-force a web application which tried hard to be difficult and annoying.. 
 Normally i would have used  crowbar ,  Suru  or a ugly mangled Python script, but the application was strangely difficult.. 
 i.e. the login process is multi staged, with new cookies being handed out at various stages. 302 redirects are used heavily and then to top it off a healthy dose of JavaScript is sent back in replies that also affect your navigation.. Now all of this can be scripted (obviously) but i figured i would try automating Safari with  applescript  to get the same effect..
