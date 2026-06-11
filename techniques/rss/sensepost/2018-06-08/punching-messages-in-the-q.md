---
source: rss/sensepost
title: punching messages in the q
url: https://sensepost.com/blog/2018/punching-messages-in-the-q/
date: 2018-06-08
item_id: https://sensepost.com/blog/2018/punching-messages-in-the-q/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2018/punching-messages-in-the-q/

We&#8217;ve done several assessments of late where we needed to (ab)use MQ services. We&#8217;ve detailed our experiences and results below. Built  a tool, punch-q , so you don&#8217;t have to go through the same, and included some info for blue teams, including an  osquery extension . 
 Depending on how old a version you are working with, or which document you read online, you might know IBM&#8217;s Message Queue solution as MQSeries, Webshere MQ or IBM MQ. The latter being the latest name it got around 2014 with the release of version 8. Nonetheless, in the last few months I have come across a number of distinct instances of MQ, each used in their own interesting ways for arbitrary systems integrations. Be it for simple messages being passed around or to facilitate file transfers, MQ played a significant role when it came to the overall business processes these companies had. In order to help me understand the technology better, I discovered some prior research by the folks at MWR, with a very informative talk done at Defcon 15 called  MQ Jumping . A subsequent  white paper  was released and is definitely worth a read.
