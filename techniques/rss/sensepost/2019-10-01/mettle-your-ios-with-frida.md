---
source: rss/sensepost
title: mettle your ios with frida
url: https://sensepost.com/blog/2019/mettle-your-ios-with-frida/
date: 2019-10-01
item_id: https://sensepost.com/blog/2019/mettle-your-ios-with-frida/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2019/mettle-your-ios-with-frida/

For a long time I have wondered about getting Meterpreter running on an iOS device using Frida. It wasn&#8217;t until I had a Twitter conversation with  @timwr  that I was reminded of  Mettle . It was finally time to give it a try. I built an objection plugin that would load it for you, which you can find  here .  
  My talk at DEF CON 27  mainly covered some ideas on how we could interact with live object instances in interesting ways. However, there were also some examples of how we could use Frida&#8217;s  Module.load()  API to side load existing external tooling that come in the form of shared libraries (either by default or wrapping them ourselves). With Mettle targeting low-resource or embedded devices, its native code approach meant it also supported iOS. So if we could get a compiled Mettle dylib, we could load it with Frida. You don&#8217;t need Frida to load a dylib of course. Using something like  insert_dylib  would work just as well. The nice thing about using something like Frida though is that we have some external control over the loading process and any post processing that we may need.
