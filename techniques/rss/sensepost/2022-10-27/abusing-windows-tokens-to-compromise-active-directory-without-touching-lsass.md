---
source: rss/sensepost
title: Abusing Windows’ tokens to compromise Active Directory without touching LSASS
url: https://sensepost.com/blog/2022/abusing-windows-tokens-to-compromise-active-directory-without-touching-lsass/
date: 2022-10-27
item_id: https://sensepost.com/blog/2022/abusing-windows-tokens-to-compromise-active-directory-without-touching-lsass/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/abusing-windows-tokens-to-compromise-active-directory-without-touching-lsass/

During an internal assessment, I performed an NTLM relay and ended up owning the NT AUTHORITY\SYSTEM account of the Windows server. Looking at the users connected on the same server, I knew that a domain administrator account was connected. All I had to do to compromise the domain, was compromise the account. This could be achieved by dumping the memory of the LSASS process and collecting their credentials or Kerberos TGT&#8217;s. Seemed easy until I realised an EDR was installed on the system. Long story short, I ended up compromising the domain admin account without touching the LSASS process. To do so, I relied on an internal Windows mechanism called token manipulation.
