---
source: rss/cloudflare-blog
title: Our billing pipeline was suddenly slow. The culprit was a hidden bottleneck in ClickHouse
url: https://blog.cloudflare.com/clickhouse-query-plan-contention/
date: 2026-05-14
item_id: https://blog.cloudflare.com/clickhouse-query-plan-contention/
category: news---

**Source:** Cloudflare Blog
**Link:** https://blog.cloudflare.com/clickhouse-query-plan-contention/

When a partitioning change to our petabyte-scale ClickHouse cluster caused critical billing jobs to stall, standard metrics showed no obvious errors. This post explores how we identified severe lock contention in ClickHouse's query planner and built upstream patches to fix it.
