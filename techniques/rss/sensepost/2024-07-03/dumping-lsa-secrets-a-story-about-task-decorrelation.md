---
source: rss/sensepost
title: Dumping LSA secrets: a story about task decorrelation
url: https://sensepost.com/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/
date: 2024-07-03
item_id: https://sensepost.com/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/

While doing an internal assessment, I was able to compromise multiple computers and servers but wasn&#8217;t able to dump the LSA secrets because of a particular EDR being installed and pretty aggressive against me. 
 In this blog post we&#8217;ll see how this EDR was blocking me and why it is still possible to dump these secrets exploiting decorrelation attacks! As a bonus, I&#8217;ll show you a fancy way of retrieving the Windows boot key without having to dump the SYSTEM hive.
