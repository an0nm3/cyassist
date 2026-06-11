---
source: rss/sensepost
title: From a GLPI patch bypass to RCE
url: https://sensepost.com/blog/2024/from-a-glpi-patch-bypass-to-rce/
date: 2024-06-20
item_id: https://sensepost.com/blog/2024/from-a-glpi-patch-bypass-to-rce/
category: techniques
tags: [Bypass, Rce]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2024/from-a-glpi-patch-bypass-to-rce/

Introduction 
 GLPI is a popular software used by companies, mainly in France. GLPI is usually used for two main purposes. Firstly it allows companies to see the  inventory  of their different equipment (such as: computers, software, printers, etc…). Secondly it is used for its ticketing system, allowing users to create  tickets  about their issues. It also has different roles for each user, those who can only create tickets (low privileges user), and those who get central access (again there are different roles here). During an internal penetration test, chances are that if you got an account, you will be a low privilege user, known as  Self-Service .
