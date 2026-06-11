---
source: rss/sensepost
title: NTHashes and Encodings
url: https://sensepost.com/blog/2020/nthashes-and-encodings/
date: 2020-08-19
item_id: https://sensepost.com/blog/2020/nthashes-and-encodings/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/nthashes-and-encodings/

If you&#8217;ve ever cracked a hash with hashcat, you&#8217;ll know that sometimes it will give you a  $HEX[0011223344]  style clear. This is done to preserve the raw byte value of the clear when the encoding isn&#8217;t known (or there&#8217;s a colon &#8220;:&#8221; character). 
 Investigation 
 Driven by an inability to crack the majority of a certain set of hashes I suspected were in a foreign charset, I decided to have a closer look at what was going on. Let&#8217;s take a look at the following examples:
