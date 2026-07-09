---
source: telegram/CVEreports
title: GHSA-Q855-8RH5-JFGQGHSA-Q855-8RH5-JFGQ: Missing Authentication and CSRF in ha-mcp bare root settings and policy routesThe ha-mcp add-on for Home Assistant exposes its settings and security policy rout
url: https://t.me/cvereports/1784
date: 2026-07-09
item_id: 1784
category: news
tags: [Bypass]
---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1784

GHSA-Q855-8RH5-JFGQGHSA-Q855-8RH5-JFGQ: Missing Authentication and CSRF in ha-mcp bare root settings and policy routesThe ha-mcp add-on for Home Assistant exposes its settings and security policy routes without authentication at the bare root path of TCP port 9583. This exposure allows unauthorized adjacent network clients to reconfigure tools, alter policies, and bypass human-in-the-loop approval gates. The vulnerability has been addressed in development build 7.6.0.dev393 and subsequent releases by restricting access to root-mounted routes exclusively to the Supervisor Ingress IP.

**URLs:**
- https://cvereports.com/reports/GHSA-Q855-8RH5-JFGQ
