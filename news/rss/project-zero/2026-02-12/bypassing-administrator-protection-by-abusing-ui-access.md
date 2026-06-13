---
source: rss/project-zero
title: Bypassing Administrator Protection by Abusing UI Access
url: https://projectzero.google/2026/02/windows-administrator-protection.html
date: 2026-02-12
item_id: https://projectzero.google/2026/02/windows-administrator-protection.html
category: news
tags: [Bypass]
---

**Source:** Project Zero
**Link:** https://projectzero.google/2026/02/windows-administrator-protection.html

In my last blog post I introduced the new Windows feature, Administrator Protection and how it aimed to create a secure boundary for UAC where one didn’t exist. I described one of the ways I was able to bypass the feature before it was released. In total I found 9 bypasses during my research that have now all been fixed. In this blog post I wanted to describe the root cause of 5 of those 9 issues, specifically the implementation of UI Access, how this has been a long standing problem with UAC that’s been under-appreciated, and how it’s being fixed now. A Question of Accessibility Prior to Windows Vista any process running on a user’s desktop could control any window created by another, such as by sending window messages. This behavior could be abused if a privileged user, such as SYSTEM, displayed a user interface on the desktop. A limited user could control the UI and potentially elevate privileges. This was referred to as a Shatter Attack, and was usually fixed by removing user interface components from privileged code.
