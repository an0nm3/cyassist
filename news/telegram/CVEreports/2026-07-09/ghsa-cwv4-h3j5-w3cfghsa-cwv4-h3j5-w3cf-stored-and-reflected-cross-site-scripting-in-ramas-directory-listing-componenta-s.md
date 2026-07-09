---
source: telegram/CVEreports
title: GHSA-CWV4-H3J5-W3CFGHSA-CWV4-H3J5-W3CF: Stored and Reflected Cross-Site Scripting in rama's Directory Listing ComponentA Stored and Reflected Cross-Site Scripting (XSS) vulnerability was identified in
url: https://t.me/cvereports/1785
date: 2026-07-09
item_id: 1785
category: news
tags: [Xss]
---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1785

GHSA-CWV4-H3J5-W3CFGHSA-CWV4-H3J5-W3CF: Stored and Reflected Cross-Site Scripting in rama's Directory Listing ComponentA Stored and Reflected Cross-Site Scripting (XSS) vulnerability was identified in the Rust web service library 'rama' prior to version 0.3.0-rc.1. When serving directories using DirectoryServeMode::HtmlFileList, the library improperly escapes directory names, filenames, and request path components before injecting them into dynamically generated HTML files. This allows attackers to execute malicious scripts inside user browser sessions.

**URLs:**
- https://cvereports.com/reports/GHSA-CWV4-H3J5-W3CF
