---
source: rss/cisco-security-advisories
title: Cisco Catalyst SD-WAN Controller, Catalyst SD-WAN Manager, and Catalyst SD-WAN Validator Authenticated Privilege Escalation Vulnerability
url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Catalyst%20SD-WAN%20Controller,%20Catalyst%20SD-WAN%20Manager,%20and%20Catalyst%20SD-WAN%20Validator%20Authenticated%20Privilege%20Escalation%20Vulnerability%26vs_k=1
date: 2026-06-12
item_id: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Catalyst%20SD-WAN%20Controller,%20Catalyst%20SD-WAN%20Manager,%20and%20Catalyst%20SD-WAN%20Validator%20Authenticated%20Privilege%20Escalation%20Vulnerability%26vs_k=1
category: news
tags: [CVE, Exploit, Injection]
---

**Source:** Cisco Security Advisories
**Link:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Catalyst%20SD-WAN%20Controller,%20Catalyst%20SD-WAN%20Manager,%20and%20Catalyst%20SD-WAN%20Validator%20Authenticated%20Privilege%20Escalation%20Vulnerability%26vs_k=1

A vulnerability in the CLI of Cisco Catalyst SD-WAN Controller, formerly SD-WAN vSmart, Cisco Catalyst SD-WAN Manager, formerly SD-WAN vManage, and  Cisco Catalyst SD-WAN Validator , formerly  SD-WAN vBond,  could allow an authenticated, local attacker to execute arbitrary commands as  root  by supplying a crafted file to the affected system. 
 This vulnerability is due to insufficient validation of user-supplied input. An attacker could exploit this vulnerability by uploading a crafted file to the affected system. A successful exploit could allow the attacker to perform command injection attacks on an affected system and elevate their privileges as the  root  user.&nbsp; 
 To exploit this vulnerability, the attacker must have  netadmin  privileges on the affected system. This would require valid credentials or exploitation of  CVE-2026-20182  or  CVE-2026-20127 . Cisco is not aware of successful exploitation by other methods. Cisco has observed limited cases where the exploitation of this bug resulted in a configuration change pushed to edge devices. 
 Cisco recommends that customers upgrade to the fixed software that is documented in the  Catalyst SD-WAN Security Advisory  that was published on May 14, 2026, and verify the configuration of the edge devices. 

 Cisco has released software updates that address this vulnerability. 
 There are no workarounds that address this vulnerability. 
  Important:  To preserve possible indicators of compromise,  customers should issue the   request admin-tech   command from each of the control components in the SD-WAN deployment before upgrading. After the  admin-tech  file has been collected,  software should be upgraded at the earliest opportunity. 
 Before upgrading an SD-WAN deployment to a fixed release, retain relevant logs. After upgrading, verify that the system has not been compromised by checking the logs for the indicators of compromise as documented in this advisory. If the logs show indicators of compromise and the system is confirmed to be compromised, applying the software update alone will not resolve the vulnerability. In such cases, follow the specific remediation steps that will be provided by the Cisco Technical Assistance Center (TAC) to help secure the system. 
 This advisory is available at the following link:  https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx  
			      
		           &lt;br/&gt;Security Impact Rating:  High
		    
		    
		        &lt;br/&gt;CVE: CVE-2026-20245
