---
source: rss/sensepost
title: Covert Login Alerting
url: https://sensepost.com/blog/2020/covert-login-alerting/
date: 2020-07-13
item_id: https://sensepost.com/blog/2020/covert-login-alerting/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/covert-login-alerting/

Intro 
 For the longest time I had the idea to implement a notification system that would alert me if someone ever logged in (or tried to login) to an SSH server or XSession on a machine I controlled, using known compromised credentials that were obtained via a data breach or a canary password. In this post I am going to show you how I implemented just that using  Canary Tokens .
