---
source: telegram/CVEreports
title: GHSA-2VG6-77G8-24MPGHSA-2vg6-77g8-24mp: Insufficient Session Expiration via Incomplete Cleanup in Better Auth EcosystemA critical session persistence vulnerability exists within the Better Auth framew
url: https://t.me/cvereports/1778
date: 2026-07-09
item_id: 1778
category: news---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1778

GHSA-2VG6-77G8-24MPGHSA-2vg6-77g8-24mp: Insufficient Session Expiration via Incomplete Cleanup in Better Auth EcosystemA critical session persistence vulnerability exists within the Better Auth framework when configured to use external secondary storage (such as Redis or Cloudflare KV) with default database options. Due to four incomplete user-deletion code paths, active user sessions are not evicted from secondary storage caches during deletion events. As a result, deleted users retain full system access via their pre-existing session cookies until the Session Time-To-Live (TTL) expires.

**URLs:**
- https://cvereports.com/reports/GHSA-2VG6-77G8-24MP
