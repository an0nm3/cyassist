---
source: rss/sensepost
title: Reading Large Files and Perf
url: https://sensepost.com/blog/2023/reading-large-files-and-perf/
date: 2023-09-19
item_id: https://sensepost.com/blog/2023/reading-large-files-and-perf/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/reading-large-files-and-perf/

One of the things that has often confused me is how little good advice there is for reading large files efficiently when writing code. 
 Typically most people use whatever the canonical file read suggestion for their language is, until they need to read large files and it’s too slow. Then they google “efficiently reading large files in &lt;lang&gt;” and are pointed to a buffered reader of some sort, and that’s that.
