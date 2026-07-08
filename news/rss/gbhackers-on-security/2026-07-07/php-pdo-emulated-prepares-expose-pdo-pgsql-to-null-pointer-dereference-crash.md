---
source: rss/gbhackers-on-security
title: PHP PDO Emulated Prepares Expose pdo_pgsql to NULL Pointer Dereference Crash
url: https://gbhackers.com/php-pdo-ecosystem/
date: 2026-07-07
item_id: https://gbhackers.com/php-pdo-ecosystem/
category: news
tags: [CVE]
---

**Source:** GBHackers on Security
**Link:** https://gbhackers.com/php-pdo-ecosystem/

A recent security audit of PHP’s PDO ecosystem uncovered a denial-of-service vector in the pdo_pgsql driver that can crash PHP processes when emulated prepared statements are enabled. PDO’s parser assumes a valid zend_string and dereferences it, triggering a NULL pointer dereference (SIGSEGV). The issue is tracked as CVE-2025-14180 and rated Moderate (6.3/10). PDO implements two [&#8230;] 
 The post  PHP PDO Emulated Prepares Expose pdo_pgsql to NULL Pointer Dereference Crash  appeared first on  GBHackers Security | #1 Globally Trusted Cyber Security News Platform .
