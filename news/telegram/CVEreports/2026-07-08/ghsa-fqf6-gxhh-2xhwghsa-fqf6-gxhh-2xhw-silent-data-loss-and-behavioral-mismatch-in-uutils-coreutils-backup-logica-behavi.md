---
source: telegram/CVEreports
title: GHSA-FQF6-GXHH-2XHWGHSA-FQF6-GXHH-2XHW: Silent Data Loss and Behavioral Mismatch in uutils coreutils Backup LogicA behavioral mismatch vulnerability (CWE-701) in the Rust-based uutils coreutils implem
url: https://t.me/cvereports/1776
date: 2026-07-08
item_id: 1776
category: news---

**Channel:** CVEreports
**Link:** https://t.me/cvereports/1776

GHSA-FQF6-GXHH-2XHWGHSA-FQF6-GXHH-2XHW: Silent Data Loss and Behavioral Mismatch in uutils coreutils Backup LogicA behavioral mismatch vulnerability (CWE-701) in the Rust-based uutils coreutils implementation of common command-line utilities allows silent data loss. When the --suffix argument is executed without explicit backup flags, the uucore library fails to enter backup mode, silently overwriting target files instead of creating preserving copies as expected under GNU standards.

**URLs:**
- https://cvereports.com/reports/GHSA-FQF6-GXHH-2XHW
