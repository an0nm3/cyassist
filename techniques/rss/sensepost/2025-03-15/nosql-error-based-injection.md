---
source: rss/sensepost
title: NoSQL error-based injection
url: https://sensepost.com/blog/2025/nosql-error-based-injection/
date: 2025-03-15
item_id: https://sensepost.com/blog/2025/nosql-error-based-injection/
category: techniques
tags: [Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/nosql-error-based-injection/

TL;DR How to do NoSQL error-based injection   
 In this second blog post (read  the first one here ), on NoSQL injection, I discuss how to do error-based injection. I think this might be a novel approach – at least my Google search-fu isn&#8217;t finding anything. 
 When trying to extract information via NoSQL injection, you typically make use of Boolean conditions to figure out a character. Portswigger has a couple of examples  here . 
 In one of Portswigger&#8217;s examples, they consider the case where you can look up another user&#8217;s profile via a website that’s vulnerable to NoSQL $where injection. To get the first char of the admin user&#8217;s password, we then use the payload    admin' &amp;&amp; this.password[0] == 'a' || 'a'=='b
