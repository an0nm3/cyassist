---
source: rss/sensepost
title: Getting rid of pre- and post-conditions in NoSQL injections
url: https://sensepost.com/blog/2025/getting-rid-of-pre-and-post-conditions-in-nosql-injections/
date: 2025-03-11
item_id: https://sensepost.com/blog/2025/getting-rid-of-pre-and-post-conditions-in-nosql-injections/
category: techniques
tags: [Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/getting-rid-of-pre-and-post-conditions-in-nosql-injections/

TL;DR: I found a cool way to get rid of pre-conditions in NOSQL syntax injection s 
 I have been investigating NoSQL injection for a bit,  trying to make it  better , or at least somewhat equivalent to SQL injection. One of the things that are tricky with NoSQL injection is getting rid of pre- and post-conditions. 
 For this post I&#8217;m focusing on MongoDB, so  
  s/NoSQL injection/Mongo injection/g  
   Background   
 In case you forgot, most MongoDB queries will look something like this in the background:
