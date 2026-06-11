---
source: rss/sensepost
title: Jumping into SOCKS
url: https://sensepost.com/blog/2023/jumping-into-socks/
date: 2023-01-24
item_id: https://sensepost.com/blog/2023/jumping-into-socks/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/jumping-into-socks/

On a recent internal assessment, we ran into a problem. While holding low-privileged access to an internal Windows host, we realised the software on the host was communicating to a remote API endpoint over HTTPS. However, the remote endpoint was enforcing authentication using client SSL certificates. 
 Normally, the above scenario is easily fixed by exporting the local client SSL certificate from the host and importing it into either Burp Suite or Postman. In Burp Suite, when you want to use a client SSL certificate, you must manually load the certificate and private key into it. This implies (on Windows, at least) that you&#8217;ll need to export the client SSL certificate. However, this is only possible if you hold appropriate permissions to the certificate and its private key and it allows exporting.
