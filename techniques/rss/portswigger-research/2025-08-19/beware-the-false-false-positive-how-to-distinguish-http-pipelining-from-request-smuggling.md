---
source: rss/portswigger-research
title: Beware the false false-positive: how to distinguish HTTP pipelining from request smuggling
url: https://portswigger.net/research/how-to-distinguish-http-pipelining-from-request-smuggling
date: 2025-08-19
item_id: https://portswigger.net/research/how-to-distinguish-http-pipelining-from-request-smuggling
category: techniques---

**Source:** PortSwigger Research
**Link:** https://portswigger.net/research/how-to-distinguish-http-pipelining-from-request-smuggling

Sometimes people think they've found HTTP request smuggling, when they're actually just observing HTTP keep-alive or pipelining. This is usually a false positive, but sometimes there's actually a real
