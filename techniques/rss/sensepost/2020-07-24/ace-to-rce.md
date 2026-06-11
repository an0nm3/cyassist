---
source: rss/sensepost
title: ACE to RCE
url: https://sensepost.com/blog/2020/ace-to-rce/
date: 2020-07-24
item_id: https://sensepost.com/blog/2020/ace-to-rce/
category: techniques
tags: [Rce]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/ace-to-rce/

tl;dr: In this writeup I am going to describe how to abuse a GenericWrite ACE misconfiguration in Active Directory to run arbitrary executables. 
 During a recent assessment I found a new way to abuse Access Control Entries in a misconfigured Active Directory instance. Before jumping into the juicy bits, I&#8217;d first like to explain what these misconfigurations are, how we find them and finally how to abuse them. If you have preexisting knowledge on this topic you can jump to the section titled  &#8216; A new way of abusing GenericWrite &#8216;.
