---
source: rss/sensepost
title: Dress Code – The Talk
url: https://sensepost.com/blog/2023/dress-code-the-talk/
date: 2023-08-23
item_id: https://sensepost.com/blog/2023/dress-code-the-talk/
category: techniques
tags: [Bypass, Xss]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/dress-code-the-talk/

TL;DR  
 This post is a summary of the contents of my talk in  Defcon 31 AppSec Village  last August 2023, and part of what I will explain in Canada at the  SecTor  conference on the 24th of October 2023 at 4:00 PM. 
 There are two (big) blocks in this post. Sorry for the length &lt;(_ _)&gt;: 
 
 The  first part  is about the not so well-known CSP bypasses that I found during this research. These can be of use in your next pentest, bug bounty, etc. Have a look at the 8 third-party domains that can be abused to bypass a strict policy to execute that sweet Cross-Site Scripting (XSS) or clickjacking proof of concept that was initially being blocked. 
 The  second part  takes a step back and delves into the process of getting Content-Securiy-Policy (CSP) data from top 1 million sites and the conclusions I draw from it. After reading this part you will get a sense of how widespread and well-implemented CSP is across the Internet. You will also learn the common pitfalls people fall into when implementing the policy. The tool I wrote to scan and collect this information and review the results can be found in  https://github.com/sensepost/dresscode   
 
 Index 
 
  Context  
  Bypasses 
 
  Lab Environment  
  Hotjar  
  Facebook  
  JSDelivr  
  Amazon AWS  
  Cloudfront, Azure, Heroku, Firebase  
 
 
  CSP Health Status 
 
  The Architecture  
  Dashboard &#8211; CSP Health Status  
 
 
  Conclusions  
 
 Context 
 Last year I was working on a web application assessment, one of these assessments that are repeated every year in which the analyst has to face a hardened application. Therefore, every year, the report gets smaller and smaller when we look at the number of vulnerabilities.
