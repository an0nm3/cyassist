---
source: telegram/CVEreports
title: GHSA-9H47-PQCX-HJR4GHSA-9H47-PQCX-HJR4: Insecure Cryptographic Defaults in Better Auth OIDC ProviderThe Better Auth framework's OIDC provider implementation (oidcProvider) contained insecure cryptogra
url: https://t.me/cvereports/1779
date: 2026-07-09
item_id: 1779
category: news---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1779

GHSA-9H47-PQCX-HJR4GHSA-9H47-PQCX-HJR4: Insecure Cryptographic Defaults in Better Auth OIDC ProviderThe Better Auth framework's OIDC provider implementation (oidcProvider) contained insecure cryptographic defaults before version 1.6.11. It advertised the insecure alg=none signing algorithm and accepted plain PKCE challenges by default, leaving downstream clients vulnerable to token signature bypasses and authorization code interception attacks.

**URLs:**
- https://cvereports.com/reports/GHSA-9H47-PQCX-HJR4
