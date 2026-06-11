---
source: rss/sensepost
title: RSA SecureID software token update
url: https://sensepost.com/blog/2012/rsa-secureid-software-token-update/
date: 2012-05-24
item_id: https://sensepost.com/blog/2012/rsa-secureid-software-token-update/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2012/rsa-secureid-software-token-update/

There has been a healthy reaction to our initial  post  on our research into the RSA SecureID Software Token. A number of readers had questions about certain aspects of the research, and I thought I&#8217;d clear up a number of concerns that people have. 
 The research pointed out two findings; the first of which is in fact a design vulnerability in RSA software&#8217;s &#8220;Token Binding&#8221; mechanism. The second finding is another design issue that affects not only RSA software token but also any other software, which generates pseudo-random numbers from a &#8220;secret seed&#8221; running on traditional computing devices such as laptops, tablets or mobile phones.  The correct way of performing this has been approached with hardware tokens, which are often tamper-resistant.
