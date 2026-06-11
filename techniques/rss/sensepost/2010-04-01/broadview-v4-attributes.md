---
source: rss/sensepost
title: BroadView V4 Attributes
url: https://sensepost.com/blog/2010/broadview-v4-attributes/
date: 2010-04-01
item_id: https://sensepost.com/blog/2010/broadview-v4-attributes/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2010/broadview-v4-attributes/

Following on from  Evert&#8217;s posting  about the new BroadView v4, I&#8217;d like to showcase a specific aspect of BV that we&#8217;ve found useful, namely Attributes. These are small pieces of data collected and maintained for each host scanned by BV including somewhat mundane bits of info like IP address and OS but, they also include some really tasty morsels about remote hosts that are scanned. Attributes are collected on a per-scan-per-host basis, and are populated by each test that runs during the scan. Since attribute population is dependent on the selected tests, the set of Attributes available to you would vary according to you configuration.
