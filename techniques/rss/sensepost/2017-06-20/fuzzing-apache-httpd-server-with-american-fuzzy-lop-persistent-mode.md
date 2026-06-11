---
source: rss/sensepost
title: Fuzzing Apache httpd server with American Fuzzy Lop + persistent mode
url: https://sensepost.com/blog/2017/fuzzing-apache-httpd-server-with-american-fuzzy-lop--persistent-mode/
date: 2017-06-20
item_id: https://sensepost.com/blog/2017/fuzzing-apache-httpd-server-with-american-fuzzy-lop--persistent-mode/
category: techniques
tags: [CVE]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/fuzzing-apache-httpd-server-with-american-fuzzy-lop--persistent-mode/

Intro 
 Recently, I reported  CVE-2017-7668 (Apache Server buffer-over-read) . This is a cross-post from my  personal blog  where I explain how to fuzz network programs with AFL by porting techniques learned in  honggfuzz  into AFL. After a small chat with Dominic he asked me to re-post it here which, for me it&#8217;s an honour to do so! 
 The reported CVE was obtained with code analysis and instrumentation of the right parts of the code (mainly  core  and  parsing ) &#8211; First, with honggfuzz I got the initial dirty test cases and then, through  radamsa  generated a few thousands mutations and finally AFL with the technique described here.
