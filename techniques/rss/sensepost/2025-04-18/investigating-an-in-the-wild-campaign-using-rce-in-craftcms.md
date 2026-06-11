---
source: rss/sensepost
title: Investigating an in-the-wild campaign using RCE in CraftCMS
url: https://sensepost.com/blog/2025/investigating-an-in-the-wild-campaign-using-rce-in-craftcms/
date: 2025-04-18
item_id: https://sensepost.com/blog/2025/investigating-an-in-the-wild-campaign-using-rce-in-craftcms/
category: techniques
tags: [CVE, Rce]
---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/investigating-an-in-the-wild-campaign-using-rce-in-craftcms/

Introduction  
 In mid-February, Orange Cyberdefense&#8217;s CSIRT was tasked with investigating a server that had been hosting a now-unavailable website. The site had been built using CraftCMS running version 4.12.8. The forensic investigation and post-analysis with the Ethical Hacking team led to the discovery of two CVEs: CVE-2024-58136 and CVE-2025-32432. 
 This blog post aims to present: 
 
 The investigation that led to the finding of those two CVEs, and details of the different IOCs found during the analysis. 
 The technical details of both CVEs, explaining how the Craft CMS was vulnerable through the Yii Framewrork. 
 An assessment of the vulnerable assets online. 
 
  I. Forensic investigation  
  TL;DR  
 
 On the 14th of February, a threat actor compromised a web server using CVE-2025-32432. 
 The threat actor used it to download a file manager written in PHP on the server which was later used to upload other PHP files to the server. 
 
 The rest of this section will cover the following points:
