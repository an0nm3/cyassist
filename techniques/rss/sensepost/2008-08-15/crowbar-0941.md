---
source: rss/sensepost
title: Crowbar 0.941
url: https://sensepost.com/blog/2008/crowbar-0.941/
date: 2008-08-15
item_id: https://sensepost.com/blog/2008/crowbar-0.941/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2008/crowbar-0.941/

Quick update on your favourite brute forcer&#8230; The file input &#8220;MS EOF char&#8221; issue has been resolved, and provision has been made for blank passwords too.  The above mentioned error meant that Crowbar incorrectly used EOF characters on *nix based files. 
 Regarding the blank passwords, simply include the word &#8220;[blank]&#8221; (without the &#8220;&#8221;) in your brute force file and crowbar will test for blank usernames/passwords as well. 
 For those of you that don&#8217;t know, Crowbar is a generic brute force tool used for web applications.  It&#8217;s free, it&#8217;s light-weight, it&#8217;s fast, it&#8217;s kewl :&gt;
