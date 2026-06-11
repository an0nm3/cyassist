---
source: rss/sensepost
title: Something about sudo, Kingcope and re-inventing  the wheel
url: https://sensepost.com/blog/2013/something-about-sudo-kingcope-and-re-inventing-the-wheel/
date: 2013-05-27
item_id: https://sensepost.com/blog/2013/something-about-sudo-kingcope-and-re-inventing-the-wheel/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2013/something-about-sudo-kingcope-and-re-inventing-the-wheel/

Willems and I are currently on an internal assessment and have popped a couple hundred (thousand?) RHEL machines, which was trivial since they are all imaged. Anyhoo &#8211; long story short, we have a user which is allowed to make use of sudo for a few commands, such as reboot and service. I immediately thought it would be nice to turn this into a local root somehow. Service seemed promising and I had a looksy how it works. Whilst it does do sanitation of the library path it does not remove LD_PRELOAD. So if we could sneak LD_PRELOAD past sudo then all should be good ?
