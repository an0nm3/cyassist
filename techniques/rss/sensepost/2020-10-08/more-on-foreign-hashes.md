---
source: rss/sensepost
title: More On Foreign Hashes
url: https://sensepost.com/blog/2020/more-on-foreign-hashes/
date: 2020-10-08
item_id: https://sensepost.com/blog/2020/more-on-foreign-hashes/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/more-on-foreign-hashes/

This is an update on  this previous post  on foreign NT hashes where I got things a little wrong by believing the source encoding matters for an NT hash. It doesn&#8217;t really, let me show you why. 
 I spent a bit of time exploring further, in particular, I took it down to a test case. Jameel gave me his name as a password in Arabic: 
   Included as a picture because WordPress is messing with my UTF8. &#8220;echo d8acd985d98ad9842031|xxd -ps -r&#8221; can give it to you straight  
 That&#8217;s  Jameel1  in Arabic. It&#8217;s encoded in UTF8 in most places, whose bytes are:
