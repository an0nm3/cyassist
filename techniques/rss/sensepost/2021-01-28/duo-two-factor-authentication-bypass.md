---
source: rss/sensepost
title: Duo Two-factor Authentication Bypass
url: https://sensepost.com/blog/2021/duo-two-factor-authentication-bypass/
date: 2021-01-28
item_id: https://sensepost.com/blog/2021/duo-two-factor-authentication-bypass/
category: techniques
tags: [Bypass]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2021/duo-two-factor-authentication-bypass/

It&#8217;s too easy when hacking, to assume something is invulnerable and not interrogate it. This was the case for me when it came to Duo&#8217;s two-factor authentication solution. However, we were able to discover two variants of the same 2FA bypass. These rely on redirecting a victim&#8217;s push notifications to an attacker-controlled device, to authorise access to a victim account. Interactions with Duo had this fixed in record time, and were easily some of the best vendor/researcher interactions we&#8217;ve ever had. If you&#8217;re looking for their technical guidance around this, you can find it  here .
