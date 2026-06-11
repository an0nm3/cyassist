---
source: rss/sensepost
title: dwn – a docker pwn tool manager experiment
url: https://sensepost.com/blog/2021/dwn-a-docker-pwn-tool-manager-experiment/
date: 2021-02-08
item_id: https://sensepost.com/blog/2021/dwn-a-docker-pwn-tool-manager-experiment/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2021/dwn-a-docker-pwn-tool-manager-experiment/

Years ago I learnt docker basics because I just couldn&#8217;t get that $ruby_tool to install. The bits of progress I&#8217;d make usually left my host&#8217;s ruby install in shambles. With docker though, I had quick reproducible build &amp; run environments I could clean up easily without leaving a mess behind. The more I used docker, the more I&#8217;ve come to love it, and today it&#8217;s become a natural part of my daily workflow. It&#8217;s not without its flaws though, so in this post I want to show you an experiment of mine where I tried to write a docker pwn tool manager. A &#8220;docker-compose for hackers&#8221; if you will, called  dwn  (/don/). You can find it here:  https://github.com/sensepost/dwn .
