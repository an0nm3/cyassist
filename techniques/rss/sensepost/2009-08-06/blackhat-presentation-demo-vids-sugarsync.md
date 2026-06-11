---
source: rss/sensepost
title: BlackHat presentation demo vids: SugarSync
url: https://sensepost.com/blog/2009/blackhat-presentation-demo-vids-sugarsync/
date: 2009-08-06
item_id: https://sensepost.com/blog/2009/blackhat-presentation-demo-vids-sugarsync/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2009/blackhat-presentation-demo-vids-sugarsync/

[part 1 in a series of 5 video write-ups from our BlackHat 09 talk, summary  here ]  
 Goal 
 We wanted to demonstrate how access to cloud resources can bring certain attack classes within reach of regular users. Instead of focusing on brute-forcing regular user credentials such as usernames and passwords, we decided to look at less noisy options since failed logins would typically be a closely watched metric. 
 To this end, different types of session identifiers were examined. The thinking was that by bruting session IDs instead of credentials the monitoring systems might be less likely to pickup the attack, and the cloud gives the attacker vast amounts of bandwidth and processing power that was not previously available. However even with access to cloud resources, most &#8220;strong&#8221; session IDs would still be large enough to avoid this attack (think 128-bit sessions such as those stored in ASP.NET cookies).
