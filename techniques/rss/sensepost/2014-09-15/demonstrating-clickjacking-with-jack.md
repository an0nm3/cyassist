---
source: rss/sensepost
title: Demonstrating ClickJacking with Jack
url: https://sensepost.com/blog/2014/demonstrating-clickjacking-with-jack/
date: 2014-09-15
item_id: https://sensepost.com/blog/2014/demonstrating-clickjacking-with-jack/
category: techniques
tags: [Poc]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2014/demonstrating-clickjacking-with-jack/

Jack is a tool I created to help build Clickjacking PoC&#8217;s. It uses basic HTML and Javascript and can be found on github,  https://github.com/sensepost/Jack  
 To use Jack, load Jack&#8217;s HTML,CSS and JS files using the method of your choice and navigate to Jack&#8217;s index.html. 
     
 Jack comes with three additional pages; sandbox.html, targetLogin.html and targetRead.html. targetRead.html can be used to demonstrate Clickjacking that reads values from a page and sandbox.html is used to display the Clickjacking demonstration. Jack by default loads the &#8220;Read&#8221; html page with default CSS and Styles.
