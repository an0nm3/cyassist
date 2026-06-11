---
source: rss/sensepost
title: using a cloud mac with a local ios device
url: https://sensepost.com/blog/2022/using-a-cloud-mac-with-a-local-ios-device/
date: 2022-05-28
item_id: https://sensepost.com/blog/2022/using-a-cloud-mac-with-a-local-ios-device/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/using-a-cloud-mac-with-a-local-ios-device/

Doing iOS mobile assessments without macOS around is not exactly fun. This can be for many reasons that include code signing and app deployment to name a few. Alternatives exist for some of these tasks (like the amazing  libimobiledevice  project or more recently an attempt to get  code signing to work without macOS ), but nothing beats using a real macOS device for most of those tasks. Be it to patch mobile apps with a Frida gadget, or to deploy an application from Xcode, whatever your reason for needing this, in this short post I&#8217;ll show you how to use  @CorelliumHQ &#8216;s  usbfluxd  project or a simple SSH tunnel to make a locally connected iOS device (eg. your Linux laptop) available to a remote macOS device such that you could expose it to Xcode, in the cloud.
