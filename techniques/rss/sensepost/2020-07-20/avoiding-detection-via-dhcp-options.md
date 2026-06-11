---
source: rss/sensepost
title: Avoiding detection via DHCP options
url: https://sensepost.com/blog/2020/avoiding-detection-via-dhcp-options/
date: 2020-07-20
item_id: https://sensepost.com/blog/2020/avoiding-detection-via-dhcp-options/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/avoiding-detection-via-dhcp-options/

When conducting a red team exercise, we want to blend in as much as possible with the existing systems on the target network. For most large networks, that means looking like a Windows machine when you request a DHCP address. 
 In a lot of cases, though, the machine that we connect to the target network is not going to be running Windows, but more likely, a variant of Linux. By default, Linux DHCP requests don&#8217;t look the same as Windows DHCP requests. One way of visualising this would be to take packet captures from Wireshark, copying DHCP requests into a text file and comparing them using  Meld .
