---
source: rss/cisco-security-advisories
title: Cisco Identity Services Engine Remote Code Execution Vulnerabilities
url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-rce-4fverepv?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Identity%20Services%20Engine%20Remote%20Code%20Execution%20Vulnerabilities%26vs_k=1
date: 2026-04-15
item_id: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-rce-4fverepv?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Identity%20Services%20Engine%20Remote%20Code%20Execution%20Vulnerabilities%26vs_k=1
category: news
tags: [CVE, Exploit, Rce]
---

**Source:** Cisco Security Advisories
**Link:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-rce-4fverepv?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Identity%20Services%20Engine%20Remote%20Code%20Execution%20Vulnerabilities%26vs_k=1

Multiple vulnerabilities in Cisco Identity Services Engine (ISE) could allow an authenticated, remote attacker to execute arbitrary commands on the underlying operating system of an affected device. To exploit these vulnerabilities, the attacker must have at least Read Only Admin credentials. 
 These vulnerabilities are due to insufficient validation of user-supplied input. An attacker could exploit these vulnerabilities by sending a crafted HTTP request to an affected device. A successful exploit could allow the attacker to obtain user-level access to the underlying operating system and then elevate privileges to&nbsp; root . In single-node Cisco ISE deployments, successful exploitation of these vulnerabilities could cause the affected ISE node to become unavailable, resulting in a denial of service (DoS) condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored. 
 Cisco has released software updates that address these vulnerabilities. There are no workarounds that address these vulnerabilities. 
 This advisory is available at the following link:  https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-rce-4fverepv  
			      
		           &lt;br/&gt;Security Impact Rating:  Critical
		    
		    
		        &lt;br/&gt;CVE: CVE-2026-20180,CVE-2026-20186
