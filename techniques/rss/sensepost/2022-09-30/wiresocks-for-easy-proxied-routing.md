---
source: rss/sensepost
title: WireSocks for Easy Proxied Routing
url: https://sensepost.com/blog/2022/wiresocks-for-easy-proxied-routing/
date: 2022-09-30
item_id: https://sensepost.com/blog/2022/wiresocks-for-easy-proxied-routing/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/wiresocks-for-easy-proxied-routing/

I built some infrastructure that you could deploy and use to easily tunnel from arbitrary sources over a proxy such as SOCKS, using anything that can run WireGuard. This is convenient in cases where it would be nicer to have a full network route to a target network (with working DNS) vs just having application specific proxy rules. In this post I&#8217;ll elaborate a bit on that idea. If you are just looking for the code you can find it here:  https://github.com/sensepost/wiresocks .
