---
source: rss/sensepost
title: Re: Jeremiah Grossmans “How to find your websites”
url: https://sensepost.com/blog/2007/re-jeremiah-grossmans-how-to-find-your-websites/
date: 2007-06-05
item_id: https://sensepost.com/blog/2007/re-jeremiah-grossmans-how-to-find-your-websites/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2007/re-jeremiah-grossmans-how-to-find-your-websites/

Jeremiah from WhiteHatSec has just written  a quick piece  on how to find your websites. Now Footprinting is obviously dear to our hearts, with 3 Blackhat talks on it (or applications of it) (&#8220;    Automation &#8211; Deus ex Machina or Rube Goldberg Machine? &#8220;, &#8220; Putting The Tea Back Into CyberTerrorism &#8220;, &#8220; The Role of Non Obvious Relationships in the Foot Printing Process &#8220;), a  commercial tool  almost dedicated to it, and a full blown chapter on it in  Open Source Penetration Testing  by charl and gareth. Footprinting is a genuinely important part of a companies security assessment, cause it doesn&#8217;t matter if they have multi-layer firewalls and WAF&#8217;s protecting the web app on their www.company.com, and an old barely used sql-injectable form on their community.company.com site that lets you grab SA on their SQL server anyway.. 
(Now that the shameless self promotion is over..) i wanted to touch on an interesting aspect of webserver discovery that is often skipped, and thats the issue of multiple websites running as name based virtual hosts on the same web-server. There was a time (not so long ago) when all of the popular scanning tools, failed to take into account that scanning 209.61.188.39 was not the same as scanning www.sensepost.com (or hackrack.sensepost.com which happens to be on the same ip address).
