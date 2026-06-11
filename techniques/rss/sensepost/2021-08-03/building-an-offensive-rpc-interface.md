---
source: rss/sensepost
title: Building an offensive RPC interface
url: https://sensepost.com/blog/2021/building-an-offensive-rpc-interface/
date: 2021-08-03
item_id: https://sensepost.com/blog/2021/building-an-offensive-rpc-interface/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2021/building-an-offensive-rpc-interface/

Using the Windows Remote Procedure Call (RPC) interface is an interesting concept when conssidering the fact that it allows you to call functions, over the network in a remote process. I wanted to better understand how RPC worked, and decided to build my own RPC interface to help with that. As a result, I wrote an RPC interface that will spawn a reverse shell given an IP address and a port. In this post I&#8217;ll show you how to do just that and what I learnt in a few sections:
