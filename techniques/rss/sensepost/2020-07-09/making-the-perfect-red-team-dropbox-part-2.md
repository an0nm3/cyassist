---
source: rss/sensepost
title: Making the Perfect Red Team Dropbox (Part 2)
url: https://sensepost.com/blog/2020/making-the-perfect-red-team-dropbox-part-2/
date: 2020-07-09
item_id: https://sensepost.com/blog/2020/making-the-perfect-red-team-dropbox-part-2/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/making-the-perfect-red-team-dropbox-part-2/

In  part 1  of this series, we set up the NanoPi R1S as a USB attack tool, covering OS installation, installation of P4wnP1, and even keylogging a &#8220;passed through&#8221; keyboard. In this part, I am going to focus on operations as an Ethernet attack tool, using two scenarios. Firstly, as a box which can be connected to an unused Ethernet port, and provide remote access to the target&#8217;s network, and secondly, as an Ethernet Person in the Middle (PitM), where it can be placed in between a legitimate device and its upstream switch, and mask its own traffic using the legitimate device&#8217;s IP address and MAC address. In the second scenario, we can also defeat Network Access Control measures, because the legitimate device will handle all of that.
