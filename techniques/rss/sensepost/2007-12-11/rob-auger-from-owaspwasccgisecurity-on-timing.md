---
source: rss/sensepost
title: Rob Auger from OWASP/WASC/CGiSecurity on Timing..
url: https://sensepost.com/blog/2007/rob-auger-from-owasp/wasc/cgisecurity-on-timing../
date: 2007-12-11
item_id: https://sensepost.com/blog/2007/rob-auger-from-owasp/wasc/cgisecurity-on-timing../
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2007/rob-auger-from-owasp/wasc/cgisecurity-on-timing../

Rob had a  rant on his site  on the timing attack, with a CSRF twist.. We met him after our Vegas talk, but im not really sure how his attack differs from our published one.. 
 my on-list response: 
 -snip-
From: haroon meer 
To: bugtraq@cgisecurity.net
Cc: websecurity@webappsec.org
Subject: Re: [WEB SECURITY] Performing Distributed Brute Forcing of CSRF
vulnerable login pages
 Hi Robert.. 
 Thanks for the kind words on the talk.. If you check out the visio at:
  http://www.sensepost.com/blogstatic/2007/08/dxsrt.png   you will see that
its pretty much the same attack..
In a shameless display of self-pimpage, check out the paper
  http://www.sensepost.com/research/squeeza/dc-15-meer_and_slaviero-WP.pdf   
from page 12.. Figure 23 for example shows the results in a
victim/zombies browser, after he has visited our page.. Effectively he
tries the userlist we send him (in this case on a standard squirrelmail
login page). Once he detects a timing diff (again using a trivial
algorithm to avoid latency disparity) he simply makes another request to
the attacker to report his success..
