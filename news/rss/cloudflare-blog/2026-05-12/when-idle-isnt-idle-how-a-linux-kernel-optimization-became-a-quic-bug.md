---
source: rss/cloudflare-blog
title: When "idle" isn't idle: how a Linux kernel optimization became a QUIC bug
url: https://blog.cloudflare.com/quic-death-spiral-fix/
date: 2026-05-12
item_id: https://blog.cloudflare.com/quic-death-spiral-fix/
category: news---

**Source:** Cloudflare Blog
**Link:** https://blog.cloudflare.com/quic-death-spiral-fix/

We investigated a bug where CUBIC's congestion window became pinned at its minimum floor, causing a performance to plummet. The fix involved correctly measuring idle periods to distinguish RTT wait times from actual application idleness.
