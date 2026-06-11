---
source: rss/sensepost
title: Introduction to WebAssembly
url: https://sensepost.com/blog/2018/introduction-to-webassembly/
date: 2018-11-14
item_id: https://sensepost.com/blog/2018/introduction-to-webassembly/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2018/introduction-to-webassembly/

I&#8217;ve started seeing WebAssemly (WASM) stuff popping up in a few places, most notably  CloudFlare&#8217;s recent anti-container isolated v8 workload stuff  and I wanted to understand it a little better. 
 Essentially, WebAssembly is a way to compile stuff to a browser-native binary format .wasm, which you can then load with JavaScript and interact with. 
 Simplest C 
 Since this is binary, I wanted to start with a C program. Since it&#8217;s C, to avoid includes or C&lt;-&gt;JS string handling, I&#8217;m just going to return 42 like other tutorials start with :)
