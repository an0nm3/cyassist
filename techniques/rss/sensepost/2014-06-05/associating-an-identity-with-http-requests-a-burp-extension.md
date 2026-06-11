---
source: rss/sensepost
title: Associating an identity with HTTP requests – a Burp extension
url: https://sensepost.com/blog/2014/associating-an-identity-with-http-requests-a-burp-extension/
date: 2014-06-05
item_id: https://sensepost.com/blog/2014/associating-an-identity-with-http-requests-a-burp-extension/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2014/associating-an-identity-with-http-requests-a-burp-extension/

This is a tool that I have wanted to build for at least 5 years. Checking my archives, the earliest reference I can find is almost exactly 5 years ago, and I&#8217;ve been thinking about it for longer, I&#8217;m sure. 
 Finally it has made it out of my head, and into the real world! 
  Be free! Be free!  
  So, what does it do, and how does it do it?  
 The core idea for this tool comes from the realisation that, when reviewing how web applications work, it would help immensely to be able to know which  user  was actually making specific requests, rather than trying to just keep track of that information in your head (or not at all). Once you have an identity associated with a request, that enables more powerful analysis of the requests which have been made.
