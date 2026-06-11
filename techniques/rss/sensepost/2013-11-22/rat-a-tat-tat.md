---
source: rss/sensepost
title: RAT-a-tat-tat
url: https://sensepost.com/blog/2013/rat-a-tat-tat/
date: 2013-11-22
item_id: https://sensepost.com/blog/2013/rat-a-tat-tat/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2013/rat-a-tat-tat/

Hey all, 
 So following on from my talk ( slides ,  video ) I am releasing the NMAP service probes and the Poison Ivy NSE script as well as the DarkComet config extractor. 
 
    Rat a-tat-tat    from   SensePost   
 
  nmap-service-probes.pi  
  poison-ivy.nse  
  extract-DCconfig-from-binary.py  
 
 An example of finding and extracting Camellia key from live Poison Ivy C2&#8217;s: 
 nmap -sV -Pn --versiondb=nmap-service-probes.pi --script=poison-ivy.nse &lt;ip_address/range)  
Finding Poison Ivy, DarkComet and/or Xtreme RAT C2&#8217;s: 
 nmap -sV -Pn --versiondb=nmap-service-probes.pi &lt;ip_range&gt;
