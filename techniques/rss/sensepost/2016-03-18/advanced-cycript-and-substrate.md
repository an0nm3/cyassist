---
source: rss/sensepost
title: Advanced Cycript and Substrate
url: https://sensepost.com/blog/2016/advanced-cycript-and-substrate/
date: 2016-03-18
item_id: https://sensepost.com/blog/2016/advanced-cycript-and-substrate/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2016/advanced-cycript-and-substrate/

Mobile assessments are always fun as the environment is constantly evolving. A recent trend has been the use of custom protocols for communication between the application and server. This holds particularly true for financial institutes who are aiming to protect both the confidentiality and integrity of data. Most of these custom protocols are over TCP, wrap data in custom crypto, which usually includes signing of the payload to prevent tampering. Even when transmitted over HTTPS, we have noticed a trend where data within the HTTP body gets encrypted and signed using some custom crypto. Both of these processes can greatly frustrate testers using standard network intercepting tools.
