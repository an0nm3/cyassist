---
source: rss/sensepost
title: Playing with Python Pickle #1
url: https://sensepost.com/blog/2010/playing-with-python-pickle-%231/
date: 2010-11-09
item_id: https://sensepost.com/blog/2010/playing-with-python-pickle-%231/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2010/playing-with-python-pickle-%231/

In our recent memcached investigations (a blog post is still in the wings) we came across numerous caches storing serialized data. The caches were not homogenous and so the data was quite varied: Java objects, ActiveRecord objects from RoR, JSON, pre-rendered HTML, .Net serialized objects and serialized Python objects. Serialized objects can be useful to an attacker from a number of standpoints: such objects could expose data where naive developers make use of the objects to hold secrets and rely on the user to proxy the objects to various parts of an application. In addition, altering serialized objects could impact on the deserialization process, leading to compromise of the system on which the deserialization takes place.
