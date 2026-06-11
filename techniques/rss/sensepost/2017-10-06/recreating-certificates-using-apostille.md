---
source: rss/sensepost
title: Recreating certificates using Apostille
url: https://sensepost.com/blog/2017/recreating-certificates-using-apostille/
date: 2017-10-06
item_id: https://sensepost.com/blog/2017/recreating-certificates-using-apostille/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/recreating-certificates-using-apostille/

Sometimes on an engagement, you&#8217;d like to construct a believable certificate chain, that you have the matching private keys for. An example might be that a mobile app is doing cert pinning, based on attributes of the signing certificate, such as the Canonical Name (CN), serial number, or Issuer, or that you are intercepting an embedded app that only supports a particular algorithm. Whatever the reason, it&#8217;s a fairly complicated process if you are not familiar with X509 certificates. And trying to kludge it together with OpenSSL and some shell scripts under time constraints will only make you tear your hair out! While Metasploit can do some of this, it only  clones a single certificate and self-signs it , rather than cloning the entire chain. If you need more than that, keep reading!
