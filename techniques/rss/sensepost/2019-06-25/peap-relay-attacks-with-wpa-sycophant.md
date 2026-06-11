---
source: rss/sensepost
title: PEAP Relay Attacks with wpa_sycophant
url: https://sensepost.com/blog/2019/peap-relay-attacks-with-wpa_sycophant/
date: 2019-06-25
item_id: https://sensepost.com/blog/2019/peap-relay-attacks-with-wpa_sycophant/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2019/peap-relay-attacks-with-wpa_sycophant/

Back in 2018, I was interested that MSCHAPv2 and NTLMv1 hashes crack using the same algorithms, and wanting to get onto the WiFi of one of our clients, I naively thought &#8220;Surely if you can relay NTLMv1 and it uses the same crypto as MSCHAPv2, you should be able to relay MSCHAPv2!&#8221;. The resulted in the creation of  wpa_sycophant  (and its helper  berate_ap ) to perform PEAP relay attacks. It was presented in  our Defcon talk last year from about 17m in .
