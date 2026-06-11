---
source: rss/sensepost
title: HTTP Methods per Directory
url: https://sensepost.com/blog/2010/http-methods-per-directory/
date: 2010-06-28
item_id: https://sensepost.com/blog/2010/http-methods-per-directory/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2010/http-methods-per-directory/

A very common finding in our day to day vulnerability management endevours is the HTTP Methods Per Directory. 
 In its most basic form, HackRack will determine which HTTP methods are allowed on various web or CGI directories by calling the OPTIONS methods per directory. On its own it is not always significant but as soon as you have directories that allow for PUT or DELETE, and weak directory permissions are in place, the picture can become much more colourful.
