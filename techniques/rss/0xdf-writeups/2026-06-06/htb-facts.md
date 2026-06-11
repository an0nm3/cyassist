---
source: rss/0xdf-writeups
title: HTB: Facts
url: https://0xdf.gitlab.io/2026/06/06/htb-facts.html
date: 2026-06-06
item_id: https://0xdf.gitlab.io/2026/06/06/htb-facts.html
category: techniques
tags: [Mass assignment]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/06/06/htb-facts.html

Facts is a Linux box hosting a trivia website built on the Camaleon CMS, a Ruby on Rails application. I’ll abuse a mass assignment vulnerability in Camaleon to promote my account to administrator, then use credentials from the admin panel to authenticate to a local MinIO S3 service. From the bucket I’ll grab an encrypted SSH private key, crack its passphrase with john, and SSH in as the next user. For root, I’ll abuse a sudo rule on facter, Puppet’s system inventory tool, that lets me load arbitrary Ruby code from a custom facts directory and run it as root. In Beyond Root, I’ll show an alternative foothold using a path traversal in Camaleon’s S3 uploader to read arbitrary files, and use the leaked Rails master key to decrypt the application’s encrypted credentials and session cookies.
