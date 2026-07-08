---
source: rss/the-hacker-news
title: 16-Year-Old Linux KVM Flaw Lets Guest VMs Escape to Host on Intel and AMD x86 Systems
url: https://thehackernews.com/2026/07/16-year-old-linux-kvm-flaw-lets-guest.html
date: 2026-07-06
item_id: https://thehackernews.com/2026/07/16-year-old-linux-kvm-flaw-lets-guest.html
category: news
tags: [CVE, Exploit]
---

**Source:** The Hacker News
**Link:** https://thehackernews.com/2026/07/16-year-old-linux-kvm-flaw-lets-guest.html

A use-after-free bug in Linux's KVM hypervisor can be triggered from a guest virtual machine to corrupt the shadow-page state of the host kernel that runs it.

Dubbed 'Januscape' and tracked as&nbsp;CVE-2026-53359, the flaw sits in the shadow MMU code that KVM shares across both Intel and AMD. The public proof-of-concept panics the host; the researcher claims that a separate, unreleased exploit
