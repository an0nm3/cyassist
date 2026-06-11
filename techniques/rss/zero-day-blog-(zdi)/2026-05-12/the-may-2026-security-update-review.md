---
source: rss/zero-day-blog-(zdi)
title: The May 2026 Security Update Review
url: https://www.thezdi.com/blog/2026/5/12/the-may-2026-security-update-review
date: 2026-05-12
item_id: https://www.thezdi.com/blog/2026/5/12/the-may-2026-security-update-review
category: techniques
tags: [Bypass, CVE, Injection, Rce, Xss]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/5/12/the-may-2026-security-update-review

I’m currently in Berlin helping set up for Pwn2Own Berlin, but that doesn’t stop Patch Tuesday from coming, and it’s another big one. At least nothing is listed as being in the wild – for now. Take a break from your regularly scheduled activities and let’s take a look at the latest security patches from Adobe and Microsoft. Due to technical difficulties, there will not be a video companion for this month.   Adobe Patches for May 2026   For May, Adobe released 10 bulletins addressing 52 unique CVEs in Adobe Commerce, After Effects, Adobe Connect, Illustrator, Media Encoder, Premiere Pro, Substance 3D Painter, Substance 3D Sampler, Content Authenticity SDK, and the Adobe Substance 3D Designer. Here’s this month’s overview table: 





















  
  




  
    


 
 
   
   
   
   
   
   
   
 
 
   
     Bulletin ID 
     Product 
     CVE Count 
     Highest Severity 
     Highest CVSS 
     Exploited 
     Deployment Priority 
   
 
 
   
      APSB26-49  
     Adobe Commerce 
     15 
     Critical 
     8.7 
     No 
     2 
   
   
      APSB26-48  
     Adobe After Effects 
     4 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-50  
     Adobe Connect 
     2 
     Critical 
     9.6 
     No 
     3 
   
   
      APSB26-51  
     Adobe Illustrator 
     4 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-47  
     Adobe Media Encoder 
     2 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-46  
     Adobe Premiere Pro 
     3 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-55  
     Adobe Substance 3D Painter 
     2 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-54  
     Adobe Substance 3D Sampler 
     1 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-53  
     Content Authenticity SDK 
     14 
     Critical 
     7.5 
     No 
     3 
   
   
      APSB26-52  
     Adobe Substance 3D Designer 
     5 
     Important 
     6.3 
     No 
     3 
   
 
 
   
     TOTAL 
     10 bulletins 
     52 
      
      
      
      
   
 
 



  




   The obvious priority this month is the patch for Commerce, with its 15 bugs and deployment priority of 2. The Connect fix should also rank up there since both of its CVEs are CVSS 9s. Beyond those, it’s a pretty typical month for Adobe, with most of the bugs either being cross-site scripting (XSS) or open-and-own code executions.   Microsoft Patches for May 2026   This month, Microsoft released a whopping 138 new CVEs in Windows and Windows components, Office and Office Components, Microsoft Edge (Chromium-based), Azure, .NET and Visual Studio, Copilot Chat, Github Copilot, M365 Copilot, SQL Server, TCP/IP, and the Telnet Client – yes, the Telnet client. Two of these bugs were reported through the TrendAI ZDI program. 30 of these bugs are rated Critical, three are rated as Moderate, one is rated Low, and the rest are rated Important in severity.  This large volume of fixes follows the largest monthly release in Microsoft’s history and reflects the trend across the industry of a high number of submissions. While not all of these bugs were found by AI, it’s likely they had an AI-related component – even if it was just AI writing the submission. I should also point out the Pwn2Own Berlin occurs in just a few days, and it’s typical for vendors to patch as much as they can before the event.  None of the bugs patched by Microsoft this month are listed as publicly known or under active attack at the time of release, so we’ve got that going for us. Let’s take a closer look at some of the more interesting updates for this month, starting with a nasty-looking bug in DNS:  -&nbsp;&nbsp;&nbsp;   CVE-2026-41096    - Windows DNS Client Remote Code Execution Vulnerability  This patch fixes a heap-based buffer overflow in the DNS Client triggered by a malicious DNS response. No authentication or user interaction needed, and since the DNS Client runs on virtually every Windows machine, the attack surface is enormous. An attacker with a position to influence DNS responses (MitM, rogue server) could achieve unauthenticated RCE across your enterprise.  -&nbsp;&nbsp;&nbsp;   CVE-2026-41089    - Windows Netlogon Remote Code Execution Vulnerability  This update covers another CVSS 9.8 bug, which is a stack-based buffer overflow that lets an unauthenticated remote attacker execute code on a domain controller by sending a specially crafted network request — no credentials, no user interaction required. Yup – that makes it wormable. This is the highest-impact bug that requires immediate patching: a compromised domain controller is a compromised domain.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-42898    - Microsoft Dynamics 365 On-Premises Remote Code Execution Vulnerability  This bug rates a CVSS 9.9(!) and represents a code injection in Dynamics 365. It allows any authenticated user to execute code with a scope change, meaning exploitation can break out and affect resources beyond the vulnerable component itself. Scope changes are pretty rare, so if you’re running Dynamics 365 On-Prem, definitely test and deploy this patch quickly.  -&nbsp;&nbsp;&nbsp;   CVE-2026-40415    - Windows TCP/IP Remote Code Execution Vulnerability  This bug in the TCP/IP stack results from a use-after-free (UAF) and could allow a remote, unauthenticated threat actor to execute code without user interaction. That makes this another wormable bug. However, this one is much less likely to be exploited. The target needs to be under sustained low-memory (memory pressure) conditions, which is pretty rare. Still, no need to tempt fate here. Test and deploy this one quickly.  Here’s the full list of CVEs released by Microsoft for May 2026: 





















  
  




  
    



















 
  
  
  
  
   CVE 
   Title 
   Severity 
   CVSS 
   Public 
   Exploited 
   Type 
  
  
     CVE-2026-35435   
   Azure AI Foundry
  Elevation of Privilege Vulnerability 
   Critical 
   8.6 
   No 
   No 
   EoP 
  
  
     CVE-2026-35428   
   Azure Cloud Shell
  Spoofing Vulnerability 
   Critical 
   9.6 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-42826   
   Azure DevOps
  Information Disclosure Vulnerability 
   Critical 
   10 
   No 
   No 
   Info 
  
  
     CVE-2026-32207   
   Azure Machine Learning
  Notebook Spoofing Vulnerability 
   Critical 
   8.8 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-33109   
   Azure Managed Instance
  for Apache Cassandra Remote Code Execution Vulnerability 
   Critical 
   9.9 
   No 
   No 
   RCE 
  
  
     CVE-2026-33844   
   Azure Managed Instance
  for Apache Cassandra Remote Code Execution Vulnerability 
   Critical 
   9 
   No 
   No 
   RCE 
  
  
     CVE-2026-41105   
   Azure Monitor Action
  Group Notification System Elevation of Privilege Vulnerability 
   Critical 
   8.1 
   No 
   No 
   EoP 
  
  
     CVE-2026-33111   
   Copilot Chat
  (Microsoft Edge) Information Disclosure Vulnerability 
   Critical 
   7.5 
   No 
   No 
   Info 
  
  
     CVE-2026-26129   
   M365 Copilot
  Information Disclosure Vulnerability 
   Critical 
   7.5 
   No 
   No 
   Info 
  
  
     CVE-2026-26164   
   M365 Copilot
  Information Disclosure Vulnerability 
   Critical 
   7.5 
   No 
   No 
   Info 
  
  
     CVE-2026-33821   
   Microsoft Dynamics 365
  Customer Insights Elevation of Privilege Vulnerability 
   Critical 
   7.7 
   No 
   No 
   EoP 
  
  
     CVE-2026-42898   
   Microsoft Dynamics 365
  On-Premises Remote Code Execution Vulnerability 
   Critical 
   9.9 
   No 
   No 
   RCE 
  
  
     CVE-2026-40379   
   Microsoft Enterprise
  Security Token Service (ESTS) Spoofing Vulnerability 
   Critical 
   9.3 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-40363   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
  
  
     CVE-2026-40358   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
  
  
     CVE-2026-34327   
   Microsoft Partner
  Center Spoofing Vulnerability 
   Critical 
   8.2 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-40365   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-41103   
   Microsoft SSO Plugin
  for Jira &amp; Confluence Elevation of Privilege Vulnerability 
   Critical 
   9.1 
   No 
   No 
   EoP 
  
  
     CVE-2026-33823   
   Microsoft Team Events
  Portal Information Disclosure Vulnerability 
   Critical 
   9.6 
   No 
   No 
   Info 
  
  
     CVE-2026-40364   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
  
  
     CVE-2026-40366   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
  
  
     CVE-2026-40361   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
  
  
     CVE-2026-40367   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
  
  
     CVE-2026-42831   
   Office for Android
  Remote Code Execution Vulnerability 
   Critical 
   7.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-41096   
   Windows DNS Client
  Remote Code Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-35421   
   Windows GDI Remote
  Code Execution Vulnerability 
   Critical 
   7.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40403   
   Windows Graphics
  Component Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40402   
   Windows Hyper-V
  Elevation of Privilege Vulnerability 
   Critical 
   9.3 
   No 
   No 
   EoP 
  
  
     CVE-2026-32161   
   Windows Native WiFi
  Miniport Driver Remote Code Execution Vulnerability 
   Critical 
   7.5 
   No 
   No 
   RCE 
  
  
     CVE-2026-41089   
   Windows Netlogon
  Remote Code Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-32175   
   .NET Core Tampering
  Vulnerability 
   Important 
   4.3 
   No 
   No 
   Tampering 
  
  
     CVE-2026-32177   
   .NET Elevation of
  Privilege Vulnerability 
   Important 
   7.3 
   No 
   No 
   EoP 
  
  
     CVE-2026-35433   
   .NET Elevation of
  Privilege Vulnerability 
   Important 
   7.3 
   No 
   No 
   EoP 
  
  
     CVE-2025-54518 *   
   AMD: CVE-2025-54518
  CPU OP Cache Corruption 
   Important 
    
   No 
   No 
   RCE 
  
  
     CVE-2026-42899   
   ASP.NET Core Denial of
  Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
  
  
     CVE-2026-40381   
   Azure Connected
  Machine Agent Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-42823 †   
   Azure Logic Apps
  Elevation of Privilege Vulnerability 
   Important 
   9.9 
   No 
   No 
   EoP 
  
  
     CVE-2026-33833   
   Azure Machine Learning
  Notebook Spoofing Vulnerability 
   Important 
   8.2 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-32204   
   Azure Monitor Agent
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-42830   
   Azure Monitor Agent
  Metrics Extension Elevation of Privilege Vulnerability 
   Important 
   6.5 
   No 
   No 
   EoP 
  
  
     CVE-2026-33117   
   Azure SDK for Java
  Security Feature Bypass Vulnerability 
   Important 
   9.1 
   No 
   No 
   SFB 
  
  
     CVE-2026-41109   
   GitHub Copilot and
  Visual Studio Code Security Feature Bypass Vulnerability 
   Important 
   8.8 
   No 
   No 
   SFB 
  
  
     CVE-2026-35424   
   Internet Key Exchange
  (IKE) Protocol Denial of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
  
  
     CVE-2026-41614   
   M365 Copilot for
  Desktop Spoofing Vulnerability 
   Important 
   6.2 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-41100   
   Microsoft 365 Copilot
  for Android Spoofing Vulnerability 
   Important 
   4.4 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-40377   
   Microsoft
  Cryptographic Services Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-41094   
   Microsoft Data
  Formulator Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40417   
   Microsoft Dynamics 365
  Business Central Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-42833   
   Microsoft Dynamics 365
  On-Premises Remote Code Execution Vulnerability 
   Important 
   9.1 
   No 
   No 
   RCE 
  
  
     CVE-2026-42838   
   Microsoft Edge
  (Chromium-based) Elevation of Privilege Vulnerability 
   Important 
   5.4 
   No 
   No 
   EoP 
  
  
     CVE-2026-40360   
   Microsoft Excel
  Information Disclosure Vulnerability 
   Important 
   7.8 
   No 
   No 
   Info 
  
  
     CVE-2026-40359   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40362   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-42832   
   Microsoft Excel
  Spoofing Vulnerability 
   Important 
   7.7 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-34329   
   Microsoft Message
  Queuing (MSMQ) Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40419   
   Microsoft Office
  Click-To-Run Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40418   
   Microsoft Office
  Click-To-Run Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-35436   
   Microsoft Office
  Click-To-Run Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40420   
   Microsoft Office
  Click-To-Run Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-42893   
   Microsoft Outlook for
  iOS Tampering Vulnerability 
   Important 
   7.4 
   No 
   No 
   Tampering 
  
  
     CVE-2026-40374   
   Microsoft Power
  Automate Desktop Information Disclosure Vulnerability 
   Important 
   6.5 
   No 
   No 
   Info 
  
  
     CVE-2026-41102   
   Microsoft PowerPoint
  for Android Spoofing Vulnerability 
   Important 
   7.1 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-35439   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40368   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Important 
   8 
   No 
   No 
   RCE 
  
  
     CVE-2026-33110   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-33112   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-40357   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-32185   
   Microsoft Teams
  Spoofing Vulnerability 
   Important 
   5.5 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-41101   
   Microsoft Word for
  Android Spoofing Vulnerability 
   Important 
   7.1 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-35440   
   Microsoft Word
  Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
  
  
     CVE-2026-40421   
   Microsoft Word
  Information Disclosure Vulnerability 
   Important 
   4.3 
   No 
   No 
   Info 
  
  
     CVE-2026-41097   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   6.7 
   No 
   No 
   SFB 
  
  
     CVE-2026-40370 †   
   SQL Server Remote Code
  Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-41613   
   Visual Studio Code
  Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-41612   
   Visual Studio Code
  Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
  
  
     CVE-2026-41611   
   Visual Studio Code
  Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
  
  
     CVE-2026-41610   
   Visual Studio Code
  Security Feature Bypass Vulnerability 
   Important 
   6.3 
   No 
   No 
   SFB 
  
  
     CVE-2026-33839   
   Win32k Elevation of
  Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-33840   
   Win32k Elevation of
  Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34330   
   Win32k Elevation of
  Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34331   
   Win32k Elevation of
  Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-35423   
   Windows 11 Telnet
  Client Information Disclosure Vulnerability 
   Important 
   5.4 
   No 
   No 
   Info 
  
  
     CVE-2026-35438   
   Windows Admin Center
  Elevation of Privilege Vulnerability 
   Important 
   8.3 
   No 
   No 
   EoP 
  
  
     CVE-2026-41086   
   Windows Admin Center
  in Azure Portal Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34344   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34345   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-35416   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-41088   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34343   
   Windows Application
  Identity (AppID) Subsystem Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-35418   
   Windows Cloud Files
  Mini Filter Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-33835   
   Windows Cloud Files
  Mini Filter Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34337   
   Windows Cloud Files
  Mini Filter Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40407   
   Windows Common Log
  File System Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40397   
   Windows Common Log
  File System Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-42896   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-35419   
   Windows DWM Core
  Library Information Disclosure  
   Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
  
  
     CVE-2026-34336   
   Windows DWM Core
  Library Information Disclosure  
   Vulnerability 
   Important 
   7.8 
   No 
   No 
   Info 
  
  
     CVE-2026-33834   
   Windows Event Logging
  Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-32209   
   Windows Filtering
  Platform (WFP) Security Feature Bypass Vulnerability 
   Important 
   4.4 
   No 
   No 
   SFB 
  
  
     CVE-2026-33841   
   Windows Kernel
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-35420   
   Windows Kernel
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40369   
   Windows Kernel
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34332   
   Windows Kernel-Mode
  Driver Remote Code Execution Vulnerability 
   Important 
   8 
   No 
   No 
   RCE 
  
  
     CVE-2026-34339   
   Windows Lightweight
  Directory Access Protocol (LDAP) Denial of Service Vulnerability 
   Important 
   5.5 
   No 
   No 
   DoS 
  
  
     CVE-2026-34341   
   Windows Link-Layer
  Discovery Protocol (LLDP) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-33838   
   Windows Message
  Queuing (MSMQ) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34342   
   Windows Print Spooler
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-41095   
   Windows Projected File
  System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34340   
   Windows Projected File
  System Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-40398   
   Windows Remote Desktop
  Services Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-21530   
   Windows Rich Text Edit
  Elevation of Privilege Vulnerability 
   Important 
   6.7 
   No 
   No 
   EoP 
  
  
     CVE-2026-32170   
   Windows Rich Text Edit
  Elevation of Privilege Vulnerability 
   Important 
   6.7 
   No 
   No 
   EoP 
  
  
     CVE-2026-40410   
   Windows SMB Client
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-35415   
   Windows Storage Spaces
  Controller Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34350   
   Windows Storport
  Miniport Driver Denial of Service Vulnerability 
   Important 
   6.5 
   No 
   No 
   DoS 
  
  
     CVE-2026-40405   
   Windows TCP/IP Denial
  of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
  
  
     CVE-2026-40414   
   Windows TCP/IP Denial
  of Service Vulnerability 
   Important 
   7.4 
   No 
   No 
   DoS 
  
  
     CVE-2026-40401   
   Windows TCP/IP Denial
  of Service Vulnerability 
   Important 
   6.2 
   No 
   No 
   DoS 
  
  
     CVE-2026-40413   
   Windows TCP/IP Denial
  of Service Vulnerability 
   Important 
   7.4 
   No 
   No 
   DoS 
  
  
     CVE-2026-35422   
   Windows TCP/IP Driver
  Security Feature Bypass Vulnerability 
   Important 
   6.5 
   No 
   No 
   SFB 
  
  
     CVE-2026-34351   
   Windows TCP/IP
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40399   
   Windows TCP/IP
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34334   
   Windows TCP/IP
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40406   
   Windows TCP/IP
  Information Disclosure Vulnerability 
   Important 
   7.5 
   No 
   No 
   Info 
  
  
     CVE-2026-33837   
   Windows TCP/IP Local
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40415   
   Windows TCP/IP Remote
  Code Execution Vulnerability 
   Important 
   8.1 
   No 
   No 
   RCE 
  
  
     CVE-2026-42825   
   Windows Telephony
  Service Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-34338   
   Windows Telephony
  Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40382   
   Windows Telephony
  Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-40380   
   Windows Volume Manager
  Extension Driver Remote Code Execution Vulnerability 
   Important 
   6.2 
   No 
   No 
   RCE 
  
  
     CVE-2026-40408   
   Windows WAN ARP Driver
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34333   
   Windows Win32k
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-34347   
   Windows Win32k
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
  
  
     CVE-2026-35417   
   Windows Win32k
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
  
  
     CVE-2026-42891   
   Microsoft Edge
  (Chromium-based) for Android Spoofing Vulnerability 
   Moderate 
   6.5 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-35429   
   Microsoft Edge
  (Chromium-based) for Android Spoofing Vulnerability 
   Moderate 
   4.3 
   No 
   No 
   Spoofing 
  
  
     CVE-2026-41107   
   Microsoft Edge
  (Chromium-based) Information Disclosure Vulnerability 
   Moderate 
   7.4 
   No 
   No 
   Info 
  
  
     CVE-2026-40416   
   Microsoft
  Edge (Chromium-based) for Android Spoofing Vulnerability 
   Low 
   4.3 
   No 
   No 
   Spoofing 
  
 
  
    
    
    
    
    
    
    
  
 
 











  




    * Indicates this CVE had been released by a third party and is now being included in Microsoft releases .   † Indicates further administrative actions are required to fully address the vulnerability.    &nbsp;   Looking at the other Critical-rated bugs in this month’s release, there are quite a few scary-looking bugs (including a CVSS 10!), but there’s no action for the end user as Microsoft has already mitigated these bugs and is just now documenting them. There’s also this month’s crop of Office bugs where the Preview Pane is an attack vector. However, the bug in Office for Android does not have the Preview Pane vector; it’s simple open and own. The bug in the WiFi driver needs a network adjacent attacker. The SharePoint bug requires authentication, but anyone with site privileges has the authentication needed. The bug in SSO Plugin for Jira &amp; Confluence should really be called an authentication bypass, since it allows an unauthenticated attacker to gain access to a system.  Looking at the other code execution bugs, most are of the open and own variety as expected. The bug in Dynamic 365 (On Prem) requires high privileges. The Message Queueing bug requires an adjacent attacker. The bug in SQL Server requires authentication, but as usual, patching won’t be straightforward. Finally, there’s a bug in the kernel that leads to code execution. Most kernel bugs are privilege escalations, but this one could allow code execution if an attacker sends specially crafted NVMe over Fabrics (NVMe‑oF) response messages during the connection handshake process that contains an invalid header length value. Neat.  As usual, the vast majority of the Microsoft release fixes Elevation of Privilege (EoP) bugs. Also as usual, most simply lead to local attackers executing their code at SYSTEM-level privileges or administrative privileges, so there’s not much to add without further technical details about the bugs themselves. There are also a few bugs that just state the attacker could “gain ELEVATED privileges.” How obtuse. The bugs in Azure allow an attacker to access data otherwise hidden from them. The Edge bug allows threat actors to elevate to the privileges of the running application. The bug in Visual Studio allows attackers to get permissions associated with the MCP Server’s managed identity. Finally, there are a couple of sandbox escapes, too, which are always useful.  This month's update includes six Security Feature Bypass vulnerabilities. The most severe is in the Azure SDK for Java (CVSS 9.1). An attacker over the network can bypass the integrity protection provided by authentication tags on encrypted data, effectively manipulating encrypted input in a way that slips past integrity checks during decryption.  Close behind is the bypass affecting the GitHub Copilot integration in Visual Studio Code (CWE-74). This one requires a user interaction, but it allows an attacker to circumvent the path validation safeguards that normally control which files Copilot is permitted to modify. The other Visual Studio Code bypass involves cross-site scripting, improper link resolution, and information exposure triggered when a user opens or views a maliciously crafted notebook.  On the Windows networking side there are two bypasses. The first hits the Windows TCP/IP driver via an authentication bypass using an alternate channel. The other impacts the Windows Filtering Platform through improper access control, allowing a local, low-privileged attacker to bypass FQDN-based network security rules. Finally, there’s a Secure Boot bypass that, you guessed it, bypasses secure boot features.  Moving on to the Information Disclosure bugs fixed this month, we have 15 different CVEs. As usual, the majority of these simply result in info leaks consisting of unspecified memory contents or memory addresses. The bug in Power Automate could expose data marked “Sensitive” within Power Automate Desktop flows. One of the Word bugs could disclose NLTM hashes. The bug in Edge could disclose your cookies, which seems rude. The bug in Visual Studio could expose file path information. Finally, there’s a bug in Telnet for Windows 11 that leaks information being used by Telnet at the time. I didn’t even realize Windows 11 still had a telnet client.  The May release contains 10 spoofing bugs (plus the ones already addressed by Microsoft). The bug in Azure Machine Learning Notebooks vulnerability requires user interaction, but it could expose info through the Azure ML web interface to the attacker. There’s a cluster of fixes for Microsoft's mobile Office suite on Android. Excel, Word, and PowerPoint for Android all carry spoofing flaws rooted in improper access control. Two Copilot products are also affected by spoofing vulns. The M365 Copilot for Desktop has no details provided. The M365 Copilot for Android variant requires low privileges and producing only limited impact on confidentiality and integrity. Microsoft Teams for Android rounds out the mobile app spoofing bugs. Three Edge bugs close things out, all involving misrepresentation of information in the browser UI.   There are two Tampering bugs in this month’s release. The one in .NET Core allows threat actors to write files to an affected system. The other is in Outlook for iOS and manifests as a command injection bug.  There are eight DoS bugs in the May release, but as always, Microsoft provides little to no actionable information about the vulnerabilities. The most interesting from a practical standpoint are two TCP/IP bugs that allow a low-privilege Hyper-V guest to crash the host. Both are triggered from the adjacent network. On the broader network-exposure side, the ASP.NET Core bug is a straightforward infinite loop condition — an unauthenticated attacker sends a crafted request over the network and the server stops responding.  No new advisories are being released this month.   Looking Ahead   Assuming I survive Pwn2Own Berlin (which is looking iffy at the moment), I’ll return on June 9th on what will hopefully be a smaller release than this one. Until then, stay safe, happy patching, and may all your reboots be smooth and clean!
