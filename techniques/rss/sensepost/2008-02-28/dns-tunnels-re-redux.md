---
source: rss/sensepost
title: DNS Tunnels (RE-REDUX)
url: https://sensepost.com/blog/2008/dns-tunnels-re-redux/
date: 2008-02-28
item_id: https://sensepost.com/blog/2008/dns-tunnels-re-redux/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/dns-tunnels-re-redux/

On a recent assessment we came across the following scenario: 
 1) We have command execution through a web command interpreter script (cmd.jsp) on a remote Linux webserver 
2) The box is firewalled only allowing 53 UDP ingress and egress 
 3) The box is sitting on the network perimeter, with one public IP and one internal IP, and not in a DMZ 
So we want to tunnel from the SensePost offices to Target Company&#8217;s internal machines, with this pretty restrictive setup. How did we accomplish this?
