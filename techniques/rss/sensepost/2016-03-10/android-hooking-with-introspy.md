---
source: rss/sensepost
title: Android hooking with Introspy
url: https://sensepost.com/blog/2016/android-hooking-with-introspy/
date: 2016-03-10
item_id: https://sensepost.com/blog/2016/android-hooking-with-introspy/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2016/android-hooking-with-introspy/

Here&#8217;s my first blog where I&#8217;ll try to write up how I&#8217;ve managed to set up the  Introspy framework  for the Android emulator. 
 First things first, if you haven&#8217;t downloaded the Android SDK do it now from  here.   
 I am on Ubuntu 14.04 x64 machine but hopefully you will be able to follow this guide as long as you are on a modern linux system. 
   Sidenote  : Since you are gonna run many commands on the emulator I highly recommend that you open a new shell during this proccess ( adb shell ) and run the  logcat  command. That way you can see all the debug messages and if something fails, play around and see how can you solve it.
