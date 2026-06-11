---
source: rss/sensepost
title: Understanding PEAP In-Depth
url: https://sensepost.com/blog/2019/understanding-peap-in-depth/
date: 2019-04-18
item_id: https://sensepost.com/blog/2019/understanding-peap-in-depth/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2019/understanding-peap-in-depth/

tl;dr  We reported a long standing PEAP bug in all Apple devices that would allow an attacker to force any Apple device (iOS, macOS or tvOS) to associate with a malicious access point, even if the authentication server (RADIUS) couldn&#8217;t prove knowledge of the password. To understand it fully, we go on a deep dive into EAP and MSCHAPv2.  
 Table of Contents 
   PEAP at a High Level    MSCHAPv2    Decrypting the Inner Tunnel    The Inner MSCHAPv2 Exchange    Byte-Level Description of the MSCHAPv2 Exchange    MSCHAPv2 Calculations    MSCHAPv2 Failure Behaviour      The Apple Vulnerability    Apple&#8217;s Fix    Disclosure Timeline &amp; Details      Original Vulnerability Report   
 While prepping for our Defcon talk last year,  Michael  kept pushing me to implement  hostapd-wpe &#8216;s EAP success attack. In this attack, the authentication server will accept any username, then skip the step where it proves knowledge of the password back to the station (because it doesn&#8217;t know the password), and instead sends an EAP-success message back to the station. I refused for a long time, because I thought it was a dumb attack that would never work. This is because in MSCHAPv2 the authentication server also proves knowledge of the password back to the station, and if it couldn&#8217;t, I assumed the station would just refuse to continue, after all, that&#8217;s the whole point.
