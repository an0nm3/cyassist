---
source: rss/sensepost
title: ASPX and reDuh
url: https://sensepost.com/blog/2009/aspx-and-reduh/
date: 2009-02-09
item_id: https://sensepost.com/blog/2009/aspx-and-reduh/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2009/aspx-and-reduh/

We&#8217;ve received a number of queries regarding folkses unable to get the ASPX version of reDuh to work. 
 In truth, the client had a faulty HTTP implementation meaning that HTTP requests were malformed.  Apache and Tomcat cope admirably with the malformed requests, IIS does not. 
 So, we&#8217;ve built a new client version for reDuh which will play nicely with IIS.  Apart from the bugfix, the new version also supports SSL.  A direct link to the updated client is  here .  More information regarding reDuh is  here .
