---
source: rss/sensepost
title: select * from projectdiscovery join steampipe
url: https://sensepost.com/blog/2023/select-from-projectdiscovery-join-steampipe/
date: 2023-07-03
item_id: https://sensepost.com/blog/2023/select-from-projectdiscovery-join-steampipe/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/select-from-projectdiscovery-join-steampipe/

Recently, I decided to take a look at  Steampipe  again. I like SQL and the structure it provides, and after playing around a bit I figured: &#8220;Wouldn&#8217;t it be cool to write a plugin for the immensely popular  projectdiscovery  tools?&#8221;. That is exactly what I did and you can find the source code for it here:  https://github.com/sensepost/steampipe-plugin-projectdiscovery . 
 overview 
 For the purposes of footprinting, everything you can do with steampipe you can do with a bash script. You technically don&#8217;t need SQL. However, with bash you always need to bust out some text wrangling with tools like  sed  and  awk . That in itself isn&#8217;t bad, but the data is inherently unstructured and error-prone as a result. Instead, if we could have our data in a database, we could do arbitrary lookups, join and more!
