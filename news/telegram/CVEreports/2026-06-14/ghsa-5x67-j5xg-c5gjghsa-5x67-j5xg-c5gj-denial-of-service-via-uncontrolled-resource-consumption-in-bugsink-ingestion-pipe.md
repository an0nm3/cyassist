---
source: telegram/CVEreports
title: GHSA-5X67-J5XG-C5GJGHSA-5X67-J5XG-C5GJ: Denial of Service via Uncontrolled Resource Consumption in Bugsink Ingestion PipelineBugsink, a Sentry-compatible self-hosted error tracker written in Python an
url: https://t.me/cvereports/1532
date: 2026-06-14
item_id: 1532
category: news---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1532

GHSA-5X67-J5XG-C5GJGHSA-5X67-J5XG-C5GJ: Denial of Service via Uncontrolled Resource Consumption in Bugsink Ingestion PipelineBugsink, a Sentry-compatible self-hosted error tracker written in Python and Django, is vulnerable to a denial of service (DoS) in versions up to and including 2.2.1. The system's ingestion pipeline historically processed every metadata tag supplied with an incoming error event without bounding the maximum number of tags. Because database writes are serialized in Bugsink's typical single-writer architecture, a single event payload carrying an excessive number of tags can monopolize the database write lock, halting event processing for all other users.

**URLs:**
- https://cvereports.com/reports/GHSA-5X67-J5XG-C5GJ
