---
source: telegram/CVEreports
title: GHSA-CGFV-JRFP-2R7VGHSA-cgfv-jrfp-2r7v: Authenticated SQL Injection in OpenRemote Datapoint Crosstab ExportAn authenticated SQL injection vulnerability exists in the datapoint crosstab export function
url: https://t.me/cvereports/1766
date: 2026-07-08
item_id: 1766
category: news
tags: [Injection]
---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1766

GHSA-CGFV-JRFP-2R7VGHSA-cgfv-jrfp-2r7v: Authenticated SQL Injection in OpenRemote Datapoint Crosstab ExportAn authenticated SQL injection vulnerability exists in the datapoint crosstab export functionality of OpenRemote. The vulnerability is caused by insecure manual SQL string construction that concatenates user-controlled display data, specifically asset display names and attribute names, directly into raw SQL statements. These statements are processed by the PostgreSQL database engine using the crosstab function to structure dynamic CSV outputs.

**URLs:**
- https://cvereports.com/reports/GHSA-CGFV-JRFP-2R7V
