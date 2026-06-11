---
source: rss/sensepost
title: objection – mobile runtime exploration
url: https://sensepost.com/blog/2017/objection-mobile-runtime-exploration/
date: 2017-07-11
item_id: https://sensepost.com/blog/2017/objection-mobile-runtime-exploration/
category: techniques
tags: [Injection]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/objection-mobile-runtime-exploration/

introduction 
 In this post, I want to introduce you to a toolkit that I have been working on, called objection. The name being a play on the words &#8220;object&#8221; and &#8220;injection&#8221;. objection is a runtime exploration toolkit powered by Frida, aimed at mobile platforms. iOS only for now, objection aims to allow you to perform various security related tasks on unencrypted iOS applications, at runtime, on non-jailbroken iOS devices. Features include inspecting the application specific keychain, as well as inspecting various artifacts left on disk during (or after) execution.
