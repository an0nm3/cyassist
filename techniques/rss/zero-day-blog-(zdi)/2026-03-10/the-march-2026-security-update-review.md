---
source: rss/zero-day-blog-(zdi)
title: The March 2026 Security Update Review
url: https://www.thezdi.com/blog/2026/3/10/the-march-2026-security-update-review
date: 2026-03-10
item_id: https://www.thezdi.com/blog/2026/3/10/the-march-2026-security-update-review
category: techniques
tags: [Bypass, CVE, Exploit, Race condition, Rce, Ssrf, Xss]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/3/10/the-march-2026-security-update-review

I am back in the friendly confines of the Mid-South headquarters of TrendAI ZDI (a.k.a. my home office), and am all set for the third patch Tuesday of 2026. Take a break from your regularly scheduled activities and let’s take a look at the latest security patches from Adobe and Microsoft.If you’d rather watch the full video recap covering the entire release, you can check it out here: 





















  
  

















  
    
      
    
    
      
        
      
    
    
  




    Adobe Patches for March 2026   For March, Adobe released eight bulletins addressing 80 unique CVEs in Adobe Acrobat Reader, Commerce, Illustrator, Substance 3D Painter, Premier Pro, Experience Manager, Substance 3D Stager, and the Adobe DNG Software Development Kit (SDK). Two of these bugs were submitted through the TrendAI ZDI program. If you need to prioritize, the update for  Acrobat  likely has the most impact, with the patch fixing two Critical-rated and one Important bugs. The fix for  Experience Manager  is the largest this month with 33 CVEs addressed. However, these are simple cross-site scripting (XSS) bugs, so it’s not too exciting. The fix for  Commerce  is also quite large with 19 CVEs. Most of these are also XSS bugs, but there’s a few security feature bypass bugs in there, too. Adobe actually gives this patch a deployment priority of 2, but it’s not under active attack at the time of release.   The fix for  Illustrator  corrects seven bugs, including a few Critical-rated ones. The patch for  Substance 3D Painter  fixes nine different CVEs, all rated Important. That’s not the case for  Substance 3D Stager , which fixes six different Critical bugs that could lead to arbitrary code execution. The patch for the  Adobe DNG Software Development Kit  (SDK) addresses one Critical and one Important bug. Finally, the update for Premiere Pro correct a single, Critical-rated bug that could lead to arbitrary code execution.   None of the bugs fixed by Adobe this month are listed as publicly known or under active attack at the time of release, and beyond the update for Commerce, all of the other updates released by Adobe this month are listed as deployment priority 3.   Microsoft Patches for March 2026   This month, Microsoft released 84 new CVEs in Windows and Windows components, Office and Office Components, Microsoft Edge (Chromium-based), Azure, SQL Server, Hyper-V Server, and the Windows Resilient File System (ReFS). Counting the third-party and Chromium updates listed in the release, it brings to total number of CVEs to 94. Five of these bugs were reported through the TrendAI ZDI program. Eight of these bugs are rated Critical, and the rest are rated Important in severity.  This volume is relatively typical for a March release, and the lack of bugs under active attack is a nice change from last month. There are two vulnerabilities listed as publicly known at the time of release, but none listed as actively exploited.  Let’s take a closer look at some of the more interesting updates for this month, starting with a bug with an AI slant:  -&nbsp;&nbsp;&nbsp;   CVE-2026-26144    - Microsoft Excel Information Disclosure Vulnerability  This is a fascinating bug and an attack scenario we’re likely to see more often. The vulnerability is a simple cross-site scripting (XSS) bug in Excel, but an attacker could use it to cause the Copilot Agent to exfiltrate data off the target. This essentially makes it a zero-click information disclosure. Although not stated, the disclosure is likely at the level of the logged-on user, so there isn’t a privilege escalation component. Info disclosures rarely get rated Critical, but it makes sense here.  -&nbsp;&nbsp;&nbsp;   CVE-2026-26110   /   CVE-2026-26113    - Microsoft Office Remote Code Execution Vulnerability   Another month and another pair of Office bugs where the Preview Pane is an exploit vector. I’ve lost count of how many of these bugs have been patched over the last year, but it’s just a matter of time until they start appearing in active exploits. The latest versions of Outlook allow you to hide the Preview Pane, but it isn’t clear if this would mitigate these attacks. The best option is still to test and deploy the update, but considering how many of these patches exist, it’s likely further updates will be needed to fully address these issues.  -&nbsp;&nbsp;&nbsp;   CVE-2026-23669    - Windows Print Spooler Remote Code Execution Vulnerability  Just reading the title makes me twitch with remembrances of  Print Nightmare  from a few years ago. This bug works in the same manner as those exploits. An authenticated attacker sends specially crafted messages to an affected system to gain arbitrary code execution. No user interaction is required. Let’s hope we don’t end up in a new nightmare of spooler exploits. Test and deploy this one quickly.  -&nbsp;&nbsp;&nbsp;   CVE-2026-23668    - Windows Graphics Component Elevation of Privilege Vulnerability  This vulnerability was submitted to the ZDI program by Marcin Wiązowski as two separate bugs, and it demonstrates the need for variant investigations when creating security patches. Both cases are caused by the lack of proper locking when performing operations on an object. However, in one case, it’s in the cdd.dll driver while the other is in the win32kfull driver. Either way, an attacker could use these to elevate privileges to SYSTEM and execute arbitrary code. Since the fix for both is to add object locking to the GDI object, the cases are combined into a single CVE. That’s not a problem, but it does show how variants can occur, and fixes should be as broad as possible.  Here’s the full list of CVEs released by Microsoft for March 2026: 





















  
  




  
    



















 
  
  
  
  
  
  
      CVE    
      Title    
      Severity    
      CVSS    
      Public 
      Exploited    
      Type    
  
  
        CVE-2026-26127      
      .NET Denial of Service Vulnerability    
      Important    
   7.5 
      Yes    
      No    
   DoS 
  
  
        CVE-2026-21262      
      SQL Server Elevation of Privilege
  Vulnerability    
      Important    
   8.8 
      Yes    
      No    
   EoP 
  
  
        CVE-2026-23651      
      Microsoft ACI Confidential Containers
  Elevation of Privilege Vulnerability    
      Critical    
   6.7 
      No    
      No    
   EoP 
  
  
        CVE-2026-26124      
      Microsoft ACI Confidential Containers
  Elevation of Privilege Vulnerability    
      Critical    
   6.7 
      No    
      No    
   EoP 
  
  
        CVE-2026-26122      
      Microsoft ACI Confidential Containers
  Information Disclosure Vulnerability    
      Critical    
   6.5 
      No    
      No    
   Info 
  
  
        CVE-2026-21536      
      Microsoft Devices Pricing Program Remote
  Code Execution Vulnerability    
      Critical    
   9.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26144      
      Microsoft Excel Information Disclosure
  Vulnerability    
      Critical    
   7.5 
      No    
      No    
   Info 
  
  
        CVE-2026-26110      
      Microsoft Office Remote Code Execution
  Vulnerability    
      Critical    
   8.4 
      No    
      No    
   RCE 
  
  
        CVE-2026-26113      
      Microsoft Office Remote Code Execution
  Vulnerability    
      Critical    
   8.4 
      No    
      No    
   RCE 
  
  
        CVE-2026-26125      
      Payment Orchestrator Service Elevation of
  Privilege Vulnerability    
      Critical    
   8.6 
      No    
      No    
   EoP 
  
  
        CVE-2026-26131      
      .NET Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25177      
      Active Directory Domain Services Elevation
  of Privilege Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-26117      
      Arc Enabled Servers - Azure Connected
  Machine Agent Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-26130      
      ASP.NET Core Denial of Service
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   DoS 
  
  
        CVE-2026-23661      
      Azure IoT Explorer Information Disclosure
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Info 
  
  
        CVE-2026-23662      
      Azure IoT Explorer Information Disclosure
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Info 
  
  
        CVE-2026-23664      
      Azure IoT Explorer Information Disclosure
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Info 
  
  
        CVE-2026-26121      
      Azure IOT Explorer Spoofing
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-26118      
      Azure MCP Server Tools Elevation of
  Privilege Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-23667      
      Broadcast DVR Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-25190      
      GDI Remote Code Execution Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-25181      
      GDI+ Information Disclosure
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Info 
  
  
        CVE-2026-26030 *   
      GitHub: CVE-2026-26030 Microsoft Semantic
  Kernel InMemoryVectorStore filter functionality vulnerable    
      Important    
   9.9 
      No    
      No    
   RCE 
  
  
        CVE-2026-23654 *   
      GitHub: Zero Shot SCFoundation Remote Code
  Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26141      
      Hybrid Worker Extension (Arc-enabled Windows
  VMs) Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-23665 †   
      Linux Azure Diagnostic extension (LAD)
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-23674      
      MapUrlToZone Security Feature Bypass
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   SFB 
  
  
        CVE-2026-26123      
      Microsoft Authenticator Information
  Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-26148 †   
      Microsoft Azure AD SSH Login extension for
  Linux Elevation of Privilege Vulnerability    
      Important    
   8.1 
      No    
      No    
   EoP 
  
  
        CVE-2026-25167      
      Microsoft Brokering File System Elevation of
  Privilege Vulnerability    
      Important    
   7.4 
      No    
      No    
   EoP 
  
  
        CVE-2026-26107      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26108      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26109      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   8.4 
      No    
      No    
   RCE 
  
  
        CVE-2026-26112      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26134      
      Microsoft Office Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-26106      
      Microsoft SharePoint Server Remote Code
  Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26114      
      Microsoft SharePoint Server Remote Code
  Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26105      
      Microsoft SharePoint Server Spoofing
  Vulnerability    
      Important    
   8.1 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-24283      
      Multiple UNC Provider Kernel Driver
  Elevation of Privilege Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25165      
      Performance Counters for Windows Elevation
  of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-24282      
      Push message Routing Service Elevation of
  Privilege Vulnerability 
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-26115      
      SQL Server Elevation of Privilege
  Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-26116      
      SQL Server Elevation of Privilege
  Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20967      
      System Center Operations Manager (SCOM)
  Elevation of Privilege Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-24285      
      Win32k Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-24291      
      Windows Accessibility Infrastructure
  (ATBroker.exe) Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25186      
      Windows Accessibility Infrastructure
  (ATBroker.exe) Information Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-23660 †   
      Windows Admin Center in Azure Portal
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-24293      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25176      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25178      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-25179      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-23656      
      Windows App Installer Spoofing
  Vulnerability    
      Important    
   5.9 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-25171      
      Windows Authentication Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-23671      
      Windows Bluetooth RFCOM Protocol Driver
  Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-24292      
      Windows Connected Devices Platform Service
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-24295      
      Windows Device Association Service Elevation
  of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-24296      
      Windows Device Association Service Elevation
  of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-25189      
      Windows DWM Core Library Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25174      
      Windows Extensible File Allocation Table
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25168      
      Windows Graphics Component Denial of Service
  Vulnerability    
      Important    
   6.2 
      No    
      No    
   DoS 
  
  
        CVE-2026-25169      
      Windows Graphics Component Denial of Service
  Vulnerability    
      Important    
   6.2 
      No    
      No    
   DoS 
  
  
        CVE-2026-23668      
      Windows Graphics Component Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-25180      
      Windows Graphics Component Information
  Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-25170      
      Windows Hyper-V Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-24297      
      Windows Kerberos Security Feature Bypass
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   SFB 
  
  
        CVE-2026-24287      
      Windows Kernel Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-24289      
      Windows Kernel Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-26132      
      Windows Kernel Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-24288      
      Windows Mobile Broadband Driver Remote Code
  Execution Vulnerability    
      Important    
   6.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-25175      
      Windows NTFS Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-23669      
      Windows Print Spooler Remote Code Execution
  Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-24290      
      Windows Projected File System Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-23673      
      Windows Resilient File System (ReFS)
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25172      
      Windows Routing and Remote Access Service
  (RRAS) Remote Code Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-25173      
      Windows Routing and Remote Access Service
  (RRAS) Remote Code Execution Vulnerability    
      Important    
   8 
      No    
      No    
   RCE 
  
  
        CVE-2026-26111      
      Windows Routing and Remote Access Service
  (RRAS) Remote Code Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-25185      
      Windows Shell Link Processing Spoofing
  Vulnerability    
      Important    
   5.3 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-24294      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-26128      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25166      
      Windows System Image Manager Assessment and
  Deployment Kit (ADK) Remote Code Execution Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-25188      
      Windows Telephony Service Elevation of
  Privilege Vulnerability    
      Important    
   8.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-23672      
      Windows Universal Disk Format File System
  Driver (UDFS) Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-25187      
      Winlogon Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-3536 *   
      Chromium: CVE-2026-3536 Integer overflow in
  ANGLE    
      Critical    
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3538 *   
      Chromium: CVE-2026-3538 Integer overflow in
  Skia    
      Critical    
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3539 *   
      Chromium: CVE-2026-3539 Object lifecycle
  issue in DevTools    
      High 
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3540 *   
      Chromium: CVE-2026-3540 Inappropriate
  implementation in WebAudio    
      High 
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3541 *   
      Chromium: CVE-2026-3541 Inappropriate
  implementation in CSS    
      High 
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3542 *   
      Chromium: CVE-2026-3542 Inappropriate
  implementation in WebAssembly    
      High 
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3543 *   
      Chromium: CVE-2026-3543 Inappropriate
  implementation in V8    
      High 
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3544 *   
      Chromium: CVE-2026-3544 Heap buffer overflow
  in WebCodecs    
      High 
      N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-3545 *   
      Chromium: CVE-2026-3545 Insufficient data
  validation in Navigation    
      High 
      N/A 
      No    
      No    
   RCE 
  
 
  
    
    
    
    
    
    
    
  
 
 











  




    * Indicates this CVE had been released by a third party and is now being included in Microsoft releases .   † Indicates further administrative actions are required to fully address the vulnerability.    &nbsp;   Looking at the other Critical-rated bugs in this month’s release, they are all cloud-native and require no user action. Microsoft has already remediated the vulnerabilities.  Moving on to the other code execution bugs, the vulnerabilities in SharePoint Server pop out first. Both require authentication, but it’s essentially the lowest level of authentication, so these would be ideal cases for lateral movement within an enterprise. There are the standard open-and-own cases within Office components. There an interesting sounding bug in the Windows Mobile Broadband Driver that requires physical access, but Microsoft doesn’t elaborate on the attack scenario beyond that fact. The bug in the System Image Manager Assessment and Deployment Kit (ADK) requires authentication. The bug in GDI requires user interaction. The remaining code execution bugs are in the RRAS protocol. We’ve seen bugs in this component in the past, but never in the wild. I wouldn’t ignore these, but I wouldn’t rush them out either.  Similar to last month, updates for Elevation of Privilege (EoP) bugs make up nearly half of this month’s release. And as we saw last month, but most simply lead to local attackers executing their code at SYSTEM-level privileges or administrative privileges. The bugs in SQL Server allow attackers to elevate to SQL sysadmin privileges. The bug in the Azure MCP Server is more complex. It allows attackers to obtain the permissions associated with the MCP Server’s managed identity, which lets them perform actions that the managed identity is able to reach. The bug in the Azure AD SSH Login extension for Linux leads to root access, and it won’t be easy to patch. You’ll need to run the update instructions from the command line on each affected system. That’s the same case for the bug in the Linux Azure Diagnostic extension (LAD). There’s an odd bug in the Hybrid Worker Extension (Arc‑enabled Windows VMs) that leads to “ELEVATED” privileges, which is something I’ve never seen before. The bug in the Broadcast DVR component allows an attacker to go from low integrity level up to medium. There’s a bug listed as an EoP in the Push message Routing Service, but reading the description, Microsoft notes it could lead to an information disclosure. It’s likely this is an error and should be an Information Disclosure bug. The final EoP is in the Azure Portal Windows Admin Center and leads to SYSTEM. However, there’s no patch to remediate this bug. Instead, you need to install the latest version of the Windows Admin Center extension through the Azure Portal by hand.   There are two security feature bypass patches in the March release. The first is a bypass of the MapURLToZone method, which (as expected) allows attackers to bypass MapURLToZone protections. The third bypass is in Kerberos and could allow an attacker to either view some sensitive information or make changes to “disclosed” information. This is a race condition that occurs while the group policy is being reapplied, so the window to exploit this would be extremely small.  Looking at the remaining info disclosure bugs getting patched this month, only two result in info leaks consisting of unspecified memory contents or memory addresses. Ther others provide more interesting results. There are three bugs in the Azure IoT Explorer have some wide-ranging implications. According to Microsoft, exploitation could result in, “device connection information, authentication tokens, request data, file paths, and other information transmitted between the application and the IoT Hub.” The bug in Authenticator almost reads like a security feature bypass, as exploit results in the disclosure of a one‑time sign‑in code or authentication deep link. The attacker would receive the sign‑in information and could potentially use it to authenticate as the user, allowing access to information or services available to that account. The last info disclosure bug is in the Accessibility Infrastructure and allows an attacker to gain secrets or privileged information belonging to the user of the affected application.  There are only four spoofing bugs in the March release. The first is in SharePoint server and manifests as an XSS. The second bug is a Server-Side Request Forgery (SSRF) in the Azure IoT Explorer. The remaining two are a bit more cryptic. The bug in Windows Shell Link Processing results from the “exposure of sensitive information to an unauthorized actor,” and could lead to spoofing. That sounds like credential exposure, but it’s not explicitly called out. The final spoofing bug results from the insufficient verification of data authenticity in Windows App Installer. Again, this sounds vaguely like credential reflection, but without further information, we can only speculate.   Finally, there are four denial-of-service (DoS) bugs in the release, including one that’s listed as publicly known in the .NET Framework. As usual, Microsoft provides no actionable information about these bugs.  No new advisories are being released this month.   Looking Ahead   I plan on being at RSA for the first time in my career, so if you’re around, please stop by and say hello. I like it when people say hello. Otherwise, I’ll be back on April 14 with my assessment of that patch Tuesday release. Until then, stay safe, happy patching, and may all your reboots be smooth and clean!
