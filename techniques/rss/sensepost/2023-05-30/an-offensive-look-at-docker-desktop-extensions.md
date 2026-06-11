---
source: rss/sensepost
title: an offensive look at docker desktop extensions
url: https://sensepost.com/blog/2023/an-offensive-look-at-docker-desktop-extensions/
date: 2023-05-30
item_id: https://sensepost.com/blog/2023/an-offensive-look-at-docker-desktop-extensions/
category: techniques
tags: [Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/an-offensive-look-at-docker-desktop-extensions/

For our annual internal hacker conference dubbed SenseCon in 2023, I decided to take a quick look at  Docker Desktop Extensions . Almost exactly a year after being  announced , I wondered what the risks of a malicious docker extension could be. This is a writeup of what I learned, a few tricks I used to get some answers and how I found a &#8220;non-issue&#8221; command injection in the extensions SDK. Everything in this post was tested on macOS and Docker Desktop 4.19.0 (106363).
