---
source: rss/sensepost
title: tip toeing past android 7’s network security configuration
url: https://sensepost.com/blog/2018/tip-toeing-past-android-7s-network-security-configuration/
date: 2018-03-12
item_id: https://sensepost.com/blog/2018/tip-toeing-past-android-7s-network-security-configuration/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2018/tip-toeing-past-android-7s-network-security-configuration/

In late Jan, someone opened an Github  issue  in the objection repository about Android 7&#8217;s  Network Security Configuration . The issue author included a  blogpost  from the NCC group about this very topic which included some very helpful bits of information (which you should totally read). 
 Naturally, I wanted to enhance objection to be able to get past this new security feature, so the testing began. I installed a Burp CA as one would normally do for assessments as well as a small test application with certificate pinning disabled and quickly realised that literally no network traffic was passing through. Inspecting the output of  adb logat , one would see messages such as the following for our failed requests:
