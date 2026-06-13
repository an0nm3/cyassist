---
source: rss/project-zero
title: Bypassing Windows Administrator Protection
url: https://projectzero.google/2026/26/windows-administrator-protection.html
date: 2026-01-26
item_id: https://projectzero.google/2026/26/windows-administrator-protection.html
category: news
tags: [Bypass]
---

**Source:** Project Zero
**Link:** https://projectzero.google/2026/26/windows-administrator-protection.html

A headline feature introduced in the latest release of Windows 11, 25H2 is Administrator Protection. The goal of this feature is to replace User Account Control (UAC) with a more robust and importantly, securable system to allow a local user to access administrator privileges only when necessary. This blog post will give a brief overview of the new feature, how it works and how it’s different from UAC. I’ll then describe some of the security research I undertook while it was in the insider preview builds on Windows 11. Finally I’ll detail one of the nine separate vulnerabilities that I found to bypass the feature to silently gain full administrator privileges. All the issues that I reported to Microsoft have been fixed, either prior to the feature being officially released (in optional update KB5067036) or as subsequent security bulletins. Note: As of 1st December 2025 the Administrator Protection feature has been disabled by Microsoft while an application compatibility issue is dealt with. The issue is unlikely to be related to anything described in this blog post so the analysis doesn’t change.
