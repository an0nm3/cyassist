---
source: rss/sensepost
title: The hunt for Chromium issue 1072171
url: https://sensepost.com/blog/2020/the-hunt-for-chromium-issue-1072171/
date: 2020-05-29
item_id: https://sensepost.com/blog/2020/the-hunt-for-chromium-issue-1072171/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/the-hunt-for-chromium-issue-1072171/

Intro 
 The last few months I&#8217;ve been  studying   Chrome&#8217;s v8 internals   and exploits  with the focus of finding a type confusion bug. The good news is that I found one, so the fuzzing and analysis efforts didn&#8217;t go to waste. The bad news is that I can reliably trigger the vulnerability but I haven&#8217;t found a way to weaponise it yet. 
 If you don&#8217;t have prior knowledge of v8, I encourage you to take some time and  read through the previous post I wrote . It covers all of the basics regarding the v8 compiler and tools that helped me throughout my research. More importantly, it will help newcomers understand all of the research described within this post.
