---
source: rss/sensepost
title: Client Side Fingerprinting in Prep for SE
url: https://sensepost.com/blog/2013/client-side-fingerprinting-in-prep-for-se/
date: 2013-01-16
item_id: https://sensepost.com/blog/2013/client-side-fingerprinting-in-prep-for-se/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2013/client-side-fingerprinting-in-prep-for-se/

On a recent engagement, we were tasked with trying to gain access to the network via a phishing attack (specifically phishing only). In preparation for the attack, I wanted to see what software they were running, to see if Vlad and I could target them in a more intelligent fashion. As this technique worked well, I thought this was a neat trick worth sharing. 
 First off the approach was to perform some footprinting to see if I could find their likely Internet breakout. While I found the likely range (it had their mail server in it) I couldn&#8217;t find the exact IP they were being NAT&#8217;ed to. Not wanting to stop there, I tried out  Vlad&#8217;s Skype IP disclosure trick , which worked like a charm. What&#8217;s cool about this approach is that it gives you both the internal and external IP of the user (so you can confirm they are connected to their internal network if you have another internal IP leak). You don&#8217;t even need to be &#8220;friends&#8221;,  you can just search for people who list the company in their details, or do some more advanced OSINT to find Skype IDs of employees.
