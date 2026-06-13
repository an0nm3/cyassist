---
source: rss/project-zero
title: A Deep Dive into the GetProcessHandleFromHwnd API
url: https://projectzero.google/2026/02/gphfh-deep-dive.html
date: 2026-02-26
item_id: https://projectzero.google/2026/02/gphfh-deep-dive.html
category: news
tags: [Bypass]
---

**Source:** Project Zero
**Link:** https://projectzero.google/2026/02/gphfh-deep-dive.html

In my previous blog post I mentioned the GetProcessHandleFromHwnd API. This was an API I didn’t know existed until I found a publicly disclosed UAC bypass using the Quick Assist UI Access application. This API looked interesting so I thought I should take a closer look. I typically start by reading the documentation for an API I don’t know about, assuming it’s documented at all. It can give you an idea of how long the API has existed as well as its security properties. The documentation’s remarks contain the following three statements that I thought were interesting: If the caller has UIAccess, however, they can use a windows hook to inject code into the target process, and from within the target process, send a handle back to the caller. GetProcessHandleFromHwnd is a convenience function that uses this technique to obtain the handle of the process that owns the specified HWND. Note that it only succeeds in cases where the caller and target process are running as the same user.
