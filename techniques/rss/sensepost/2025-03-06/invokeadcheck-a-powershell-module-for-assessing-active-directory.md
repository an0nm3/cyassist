---
source: rss/sensepost
title: InvokeADCheck – A PowerShell Module for Assessing Active Directory
url: https://sensepost.com/blog/2025/invokeadcheck-a-powershell-module-for-assessing-active-directory/
date: 2025-03-06
item_id: https://sensepost.com/blog/2025/invokeadcheck-a-powershell-module-for-assessing-active-directory/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/invokeadcheck-a-powershell-module-for-assessing-active-directory/

Introduction 
 During an Active Directory (AD) assessment, I found myself struggling with a collection of individual PowerShell scripts and their formatting—or rather, the lack thereof. The various PowerShell scripts included public, as well as proprietary, scripts that were used for retrieving Active Directory objects and their attributes. Faced with resource and time constraints within the team, I proposed to try to come up with a better, more efficient way to conduct some of the checks that we do during an AD assessment. Inspired in part by the excellent work of Sean Metcalf, the author of  Invoke-TrimarcADChecks , my colleague Justin ( Justin  &#8211;  P ) and I ( N1ck3nd ) set out to develop what would ultimately become the  InvokeADCheck PowerShell module .
