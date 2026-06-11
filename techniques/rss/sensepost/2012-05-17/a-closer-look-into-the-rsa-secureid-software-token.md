---
source: rss/sensepost
title: A closer look into the RSA SecureID software token
url: https://sensepost.com/blog/2012/a-closer-look-into-the-rsa-secureid-software-token/
date: 2012-05-17
item_id: https://sensepost.com/blog/2012/a-closer-look-into-the-rsa-secureid-software-token/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2012/a-closer-look-into-the-rsa-secureid-software-token/

Widespread use of smart phones by employees to perform work related activities has introduced the idea of using these devices as an authentication token. As an example of such attempts, RSA SecureID software tokens are available for iPhone, Nokia and the Windows platforms. Obviously, mobile phones would not be able to provide the level of tamper-resistance that hardware tokens would, but I was interested to know how easy/hard it could be for a potential attacker to clone RSA SecureID software tokens. I used the Windows version of the RSA SecurID Software Token for Microsoft Windows version 4.10 for my analysis and discovered the following issues:
