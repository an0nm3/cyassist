---
source: rss/zero-day-blog-(zdi)
title: The June 2026 Security Update Review
url: https://www.thezdi.com/blog/2026/6/9/the-june-2026-security-update-review
date: 2026-06-09
item_id: https://www.thezdi.com/blog/2026/6/9/the-june-2026-security-update-review
category: techniques
tags: [Bypass, CVE, Exploit, Injection, Rce, Ssrf, Xss]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/6/9/the-june-2026-security-update-review

I’ve made it through Pwn2Own Berlin, had a little vacation, and now I’m back for Patch Tuesday. Microsoft and Adobe didn’t disappoint. In fact, they have heralded my return with the largest Patch Tuesday release ever. Thanks? Take a break from your regularly scheduled activities and let’s take a look at the latest security patches from Adobe and Microsoft. If you’d rather watch the full video recap covering the entire release, you can check it out here: 





















  
  

















  
    
      
    
    
      
        
      
    
    
  




    Adobe Patches for June 2026   For May, June released 11 bulletins addressing 123 unique CVEs in Adobe Acrobat Reader, ColdFusion, Experience Manager, Experience Manager Forms, InDesign, InCopy, Substance 3D Sampler, Content Credentials SDK, Dreamweaver, Format Plugins, and Adobe Campaign Classic. A total of 11 of these CVEs were reported through the ZDI program.  Here’s this month’s overview table: 





















  
  




  
    


 
 
   
   
   
   
   
   
   
 
 
   
     Bulletin ID 
     Product 
     CVE Count 
     Highest Severity 
     Highest CVSS 
     Exploited 
     Deployment Priority 
   
 
 
   
      APSB26-66  
     Adobe Campaign Classic 
     2 
     Critical 
     10.0 
     No 
     1 
   
   
      APSB26-64  
     Adobe ColdFusion 
     7 
     Critical 
     9.6 
     No 
     1 
   
   
      APSB26-63  
     Adobe Acrobat Reader 
     20 
     Critical 
     7.8 
     No 
     2 
   
   
      APSB26-57  
     Adobe Experience Manager Forms 
     3 
     Critical 
     9.3 
     No 
     2 
   
   
      APSB26-62  
     Adobe Dreamweaver 
     5 
     Critical 
     8.6 
     No 
     3 
   
   
      APSB26-65  
     Adobe Format Plugins 
     2 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-59  
     Adobe InCopy 
     3 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-58  
     Adobe InDesign 
     12 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-60  
     Adobe Substance 3D Sampler 
     4 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-61  
     Content Credentials SDK 
     8 
     Critical 
     7.5 
     No 
     3 
   
   
      APSB26-56  
     Adobe Experience Manager 
     57 
     Important 
     5.4 
     No 
     3 
   
 
 
   
     TOTAL 
     11 bulletins 
     123 
      
      
      
      
   
 
 



  




   Obviously, the update for Campaign Classic should be on the top of your deployment list if you’re a user. A CVSS 10 is rare; two in the same bulletin is pretty much a unicorn. Adobe says there are no active attacks, but I would expect heavy research into creating one. The update for Coldfusion is also a Priority 1, but again, no known attacks is the wild. I suspect the Reader patch will also receive a lot of attention as malicious PDFs are common in ransomware attacks. The update for Experience Manager may be large, but it’s mostly just cross-site scripting (XSS) bugs.   Microsoft Patches for June 2026   This month, Microsoft released a new record 208 CVEs Windows and Windows components, Office and Office Components, Microsoft Edge (Chromium-based), Azure, .NET and Visual Studio, Github Copilot, Defender, Exchange Server, Hyper-V, Secure Boot, and BitLocker. At least, that’s my count. Microsoft’s tools seem to be having some issues, as they initially included a CVE from 2020 in this release. Regardless, the count is over 200, and I counted several times.  One of these bugs came through the ZDI program, but bugs submitted during Pwn2Own Berlin remain unpatched. If you include the Chromium and other third-party bugs, the total CVE count for June comes to a staggering 571 CVEs. 38 of these cases are rated Critical while the rest are rated Important in severity.  I’ve been counting CVEs on Patch Tuesday since 2017, and this is by far the largest monthly release in that time. The previous record was 177 set last year. It is extraordinary that Microsoft can produce so many patches in a single month, but it does raise concerns. How many of these cases were found using AI tools? How many patches were generated using AI to assist in coding or testing? What quality issues may exist in these patches? And likely most importantly, is this the new normal? The last two months were also large releases. Should sysadmins adjust their processes for prioritization and patch deployment based on this new volume of updates? Unfortunately, Microsoft is not providing those answers right now. Hopefully that changes in the future. BTW – just a note – the current number of CVEs shipped by Microsoft this year exceeds the total number of CVEs shipped in all of 2018.  One of the bugs patched by Microsoft this month is listed as under active exploitation and three others are listed as publicly known at the time of release. Let’s take a closer look at some of the more interesting updates for this month, starting with the bug being exploited in the wild.  -&nbsp;&nbsp;   CVE-2026-41091    - Microsoft Defender Elevation of Privilege Vulnerability  Since Microsoft doesn’t provide info on how widespread exploitation is, we must read some tea leaves. For this patch, several different people were acknowledged, which indicates multiple parties say this is in the wild, meaning exploitation is likely significant. The good news is that most people won’t need to take action as Defender updates itself. However, if you don’t have this configured or are in an isolated environment, you’ll need to update to the latest version.  -&nbsp;&nbsp;&nbsp;   CVE-2026-45657    - Windows Kernel Remote Code Execution Vulnerability  This CVSS 9.8 bug allows remote, unauthenticated attackers to execute code at SYSTEM level without user interaction. Yup – this is wormable. The problem lies in the way the kernel handles TCP/IP. This was listed as “Exploitation Less Likely” by Microsoft, but rest assured that every researcher and bug shop on the planet is reversing this patch right now trying to create an exploit. Test and deploy this patch quickly.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-47291    - HTTP.sys Remote Code Execution Vulnerability  Our second CVSS 9.8 bug of the month, this also allows remote, unauthenticated attackers to execute code on affected systems without user interaction. However, there is a caveat. Systems using the default MaxRequestBytes registry value used by the Windows HTTP stack are not affected by this bug. You can edit your registry settings if you need protection while you test and deploy the patch. The bulletin includes instructions and even a PowerShell script for doing this action. Microsoft lists this as “Exploitation more likely”, so I would definitely check your registry settings.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-44815    - DHCP Client Service Remote Code Execution Vulnerability  Here’s another CVSS 9.8 that has an odd incongruity. Although the CVSS says no permissions are required for exploitation, the write-up states it must be an “authenticated” user. I would err on the side of caution here and believe the CVSS. If that’s correct, then we have another bug where a remote, unauthenticated attacker could execute code on affected systems without user interaction. And since the DHCP client is on every OS, it’s a juicy target. This is another one to test and deploy with haste.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-45585   /   CVE-2026-50507    - Windows BitLocker Security Feature Bypass Vulnerability  If you’ve followed the ongoing saga of Nightmare Eclipse vs. MSRC, the bugs should look familiar. One is definitely a fix for “YellowKey”, while the other appears to be a fix for “GreenPlasma”. The researcher has promised a “ bone shattering ” drop on June 14, so let’s hope Microsoft is able to reach some understanding with the researcher before more 0-days are released. Also, there is a script provided by Microsoft as a mitigation, but the better strategy is to test and deploy the updates.  &nbsp;Here’s the full list of CVEs released by Microsoft for June 2026: 





















  
  




  
    



















 
  
  
  
  
   CVE 
   Title 
   Severity 
   CVSS 
   Public 
   Exploited 
   XI 
   Type 
  
  
     CVE-2026-41091   
   Microsoft Defender
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   Yes 
   Yes 
   0 
   EoP 
  
  
     CVE-2026-49160   
   HTTP.sys Denial of
  Service Vulnerability 
   Important 
   7.5 
   Yes 
   No 
   1 
   DoS 
  
  
     CVE-2026-50507   
   Windows BitLocker
  Security Feature Bypass Vulnerability 
   Important 
   6.8 
   Yes 
   No 
   1 
   SFB 
  
  
     CVE-2026-45586   
   Windows Collaborative
  Translation Framework (CTFMON) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   Yes 
   No 
   1 
   EoP 
  
  
     CVE-2025-10263 *   
   ARM: CVE-2025-10263
  Completion of affected memory accesses might not be guaranteed by completion
  of a TLBI [kernel] 
   Critical 
   9.3 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-48567   
   Azure HorizonDB    Elevation of Privilege Vulnerability 
   Critical 
   10 
   No 
   No 
   N/A 
   EoP 
  
  
     CVE-2026-32193   
   Azure Kubernetes
  Service (AKS) Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-47644   
   Copilot Chat
  (Microsoft Edge) Information Disclosure Vulnerability 
   Critical 
   6.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-44815   
   DHCP Client Service
  Remote Code Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47291   
   HTTP.sys Remote Code
  Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   1 
   RCE 
  
  
     CVE-2026-42824   
   M365 Copilot
  Information Disclosure Vulnerability 
   Critical 
   6.5 
   No 
   No 
   N/A 
   Info 
  
  
     CVE-2026-45476   
   Microsoft Azure
  Network Adapter Elevation of Privilege Vulnerability 
   Critical 
   8.2 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44810   
   Microsoft
  Cryptographic Services Elevation of Privilege Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-48579   
   Microsoft Exchange
  Online Information Disclosure Vulnerability 
   Critical 
   9.1 
   No 
   No 
   N/A 
   Info 
  
  
     CVE-2026-47655   
   Microsoft Graph
  Information Disclosure Vulnerability 
   Critical 
   6.5 
   No 
   No 
   N/A 
   Info 
  
  
     CVE-2026-45497   
   Microsoft M365 Copilot
  Remote Code Execution Vulnerability 
   Critical 
   7.7 
   No 
   No 
   N/A 
   RCE 
  
  
     CVE-2026-45460   
   Microsoft Office
  Information Disclosure Vulnerability 
   Critical 
   4.7 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-45472   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45474   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45461   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45463   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45456   
   Microsoft Outlook and
  Word Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45458   
   Microsoft Outlook and
  Word Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47635   
   Microsoft Outlook and
  Word Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-26142   
   Nuance PowerScribe
  Remote Code Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47289   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47654   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   7.5 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-48563   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   7.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-42992   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   7.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44799   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   7.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44801   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   7.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-42985   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   1 
   RCE 
  
  
     CVE-2026-45648   
   Windows Active
  Directory Domain Services Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-42987   
   Windows Deployment
  Services (WDS) Remote Code Execution 
   Critical 
   8.1 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-33828   
   Windows Device Health
  Attestation (DHA) Elevation of Privilege Vulnerability 
   Critical 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-44803   
   Windows Graphics
  Component Remote Code Execution Vulnerability 
   Critical 
   7.8 
   No 
   No 
   1 
   RCE 
  
  
     CVE-2026-44812   
   Windows Graphics
  Component Remote Code Execution Vulnerability 
   Critical 
   7.8 
   No 
   No 
   1 
   RCE 
  
  
     CVE-2026-45607   
   Windows Hyper-V Remote
  Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45641   
   Windows Hyper-V Remote
  Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47652   
   Windows Hyper-V Remote
  Code Execution Vulnerability 
   Critical 
   8.2 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47288   
   Windows Kerberos Key
  Distribution Center (KDC) Remote Code Execution 
   Critical 
   7.1 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-45657   
   Windows Kernel Remote
  Code Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-48574   
   Windows Media Remote
  Code Execution Vulnerability 
   Critical 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45490   
   .NET SDK Elevation of
  Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45491   
   .NET Tampering
  Vulnerability 
   Important 
   6.2 
   No 
   No 
   3 
   Tampering 
  
  
     CVE-2026-45591   
   ASP.NET Core Denial of
  Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   2 
   DoS 
  
  
     CVE-2026-47643   
   Azure Stack Edge
  Remote Code Execution Vulnerability 
   Important 
   9.8 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-41098   
   Azure Stack Edge
  Spoofing Vulnerability 
   Important 
   8.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45642   
   Microsoft Azure
  Attestation service and Device Health Attestation Service Spoofing
  Vulnerability 
   Important 
   3.9 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45650   
   Microsoft Bing Search
  Spoofing Vulnerability 
   Important 
   4.3 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45637   
   Microsoft DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45647   
   Microsoft Defender for
  Endpoint for Mac Elevation of Privilege Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-40371   
   Microsoft Dynamics 365
  (on-premises) Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44822   
   Microsoft Excel
  Information Disclosure Vulnerability 
   Important 
   8.2 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-45455   
   Microsoft Excel
  Information Disclosure Vulnerability 
   Important 
   3.3 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45469   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44817   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-44818   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44820   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44823   
   Microsoft Excel Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45459   
   Microsoft Excel
  Security Feature Bypass Vulnerability 
   Important 
   3.3 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-45504   
   Microsoft Exchange
  Server Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45502   
   Microsoft Exchange
  Server Information Disclosure Vulnerability 
   Important 
   5 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-45503   
   Microsoft Exchange
  Server Information Disclosure Vulnerability 
   Important 
   8.1 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-45583   
   Microsoft Exchange
  Server Remote Code Execution Vulnerability 
   Important 
   7.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45500   
   Microsoft Exchange
  Server Spoofing Vulnerability 
   Important 
   6.1 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45501   
   Microsoft Exchange
  Server Spoofing Vulnerability 
   Important 
   6.5 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-47631   
   Microsoft Exchange
  Server Spoofing Vulnerability 
   Important 
   8.1 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-42986   
   Microsoft Graphics
  Component Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   1 
   EoP 
  
  
     CVE-2026-41092   
   Microsoft Kinect
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45644   
   Microsoft Live Share
  Canvas SDK Elevation of Privilege Vulnerability 
   Important 
   8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-47293   
   Microsoft Office
  Click-To-Run Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45485   
   Microsoft Office
  Information Disclosure Vulnerability 
   Important 
   3.3 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-44821   
   Microsoft Office
  Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45483   
   Microsoft Office
  Project Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45475   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44819   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-44824   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45645   
   Microsoft Office
  Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-49161   
   Microsoft PC Manager
  Security Feature Bypass Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   SFB 
  
  
     CVE-2026-42902   
   Microsoft PowerToys
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45484   
   Microsoft SharePoint
  Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45454   
   Microsoft SharePoint
  Remote Code Execution Vulnerability 
   Important 
   6.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-47298   
   Microsoft SharePoint
  Server Remote Code Execution Vulnerability 
   Important 
   8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45467   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45468   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45479   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45453   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-47636   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-47637   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-47638   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-47639   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   3 
   Spoofing 
  
  
     CVE-2026-47641   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-33113   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45462   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45464   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-45465   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-47634   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   7.3 
   No 
   No 
   1 
   Spoofing 
  
  
     CVE-2026-47640   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   3 
   Spoofing 
  
  
     CVE-2026-45481   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   7.3 
   No 
   No 
   1 
   Spoofing 
  
  
     CVE-2026-48560   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-48562   
   Microsoft SharePoint
  Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   2 
   Spoofing 
  
  
     CVE-2026-42835   
   Microsoft Teams for
  Android Information Disclosure Vulnerability 
   Important 
   8.1 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45606   
   Microsoft UxTheme
  Library (uxtheme.dll) Denial of Service Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   DoS 
  
  
     CVE-2026-45482   
   Microsoft Visual
  Studio Code CoPilot Chat Extension Security Feature Bypass Vulnerability 
   Important 
   8.4 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-45466   
   Microsoft Word
  Information Disclosure Vulnerability 
   Important 
   3.3 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-45471   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45486   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45643   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45457   
   Microsoft Word Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-42980   
   NT OS Kernel Elevation
  of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   1 
   EoP 
  
  
     CVE-2026-42916   
   NT OS Kernel Elevation
  of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45649   
   Office for Android
  Spoofing Vulnerability 
   Important 
   7.1 
   No 
   No 
   3 
   Spoofing 
  
  
     CVE-2026-47653   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-42909   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Important 
   7.5 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-42913   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Important 
   7.5 
   No 
   No 
   3 
   RCE 
  
  
     CVE-2026-42993   
   Remote Desktop Client
  Remote Code Execution Vulnerability 
   Important 
   7.5 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45588   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-48568   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-48570   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-48573   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-48575   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-48576   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-48578   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-45654   
   Secure Boot Security
  Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-45656   
   UEFI Secure Boot
  Security Feature Bypass Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-8863   
   UEFI Secure Boot
  Security Feature Bypass Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-40376   
   Visual Studio Code
  Elevation of Privilege Vulnerability 
   Important 
   7.5 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-47281   
   Visual Studio Code
  Elevation of Privilege Vulnerability 
   Important 
   9.6 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-47284   
   Visual Studio Code
  Information Disclosure Vulnerability 
   Important 
   6.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-47292   
   Visual Studio Code
  MSSQL Extension Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-48569   
   Visual Studio Code
  Security Feature Bypass Vulnerability 
   Important 
   7.1 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-47287   
   Visual Studio Code
  Tampering Vulnerability 
   Important 
   6.5 
   No 
   No 
   2 
   Tampering 
  
  
     CVE-2026-42829   
   Windows Administrator
  Protection Secure Feature Bypass Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-34335   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45601   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45598   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45596   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45638   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45603   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42911   
   Windows Ancillary
  Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45594   
   Windows Application
  Identity (AppID) Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45655   
   Windows BitLocker
  Security Feature Bypass Vulnerability 
   Important 
   5.3 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-45658   
   Windows BitLocker
  Security Feature Bypass Vulnerability 
   Important 
   7.8 
   No 
   No 
   1 
   SFB 
  
  
     CVE-2026-45640   
   Windows Bluetooth Port
  Driver Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45605   
   Windows Bluetooth
  Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-47656   
   Windows Boot Manager
  Security Feature Bypass Vulnerability 
   Important 
   7.9 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-44809   
   Windows Common Log
  File System Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45634   
   Windows DHCP Client
  Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-45608   
   Windows DHCP Client
  Information Disclosure Vulnerability 
   Important 
   6.8 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-41108   
   Windows DNS Client
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42905   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   1 
   EoP 
  
  
     CVE-2026-44811   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44808   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44807   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42983   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44802   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44813   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44804   
   Windows DWM Core
  Library Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-48566   
   Windows DWM Core
  Library Information Disclosure  
   Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-44814   
   Windows DWM Core
  Library Information Disclosure  
   Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45602   
   Windows Dynamic Host
  Configuration Protocol (DHCP) Tampering Vulnerability 
   Important 
   9.1 
   No 
   No 
   2 
   Tampering 
  
  
     CVE-2026-42836   
   Windows Function
  Discovery Service (fdwsd.dll) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42910   
   Windows Hotpatch
  Monitoring Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42972   
   Windows Hyper-V
  Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45592   
   Windows Internet
  (wininet.dll) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42903   
   Windows Kerberos
  Denial of Service Vulnerability 
   Important 
   6.5 
   No 
   No 
   3 
   DoS 
  
  
     CVE-2026-42914   
   Windows Kerberos
  Denial of Service Vulnerability 
   Important 
   5.3 
   No 
   No 
   2 
   DoS 
  
  
     CVE-2026-48583   
   Windows Kernel
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45653   
   Windows Kernel
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42984   
   Windows Kernel
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45600   
   Windows Kernel-Mode
  Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45604   
   Windows Managed
  Installer Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45595   
   Windows Mark of the
  Web Security Feature Bypass Vulnerability 
   Important 
   5.4 
   No 
   No 
   2 
   SFB 
  
  
     CVE-2026-45636   
   Windows NTFS Remote
  Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-50508   
   Windows NTLM Spoofing
  Vulnerability 
   Important 
   6.5 
   No 
   No 
   1 
   Spoofing 
  
  
     CVE-2026-48565   
   Windows Narrator
  Braille Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-44805   
   Windows Network
  Controller (NC) Host Agent Denial of Service Vulnerability 
   Important 
   5.5 
   No 
   No 
   3 
   DoS 
  
  
     CVE-2026-42981   
   Windows Performance
  Monitor Remote Code Execution Vulnerability 
   Important 
   8.1 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-42974   
   Windows Performance
  Monitor Remote Code Execution Vulnerability 
   Important 
   8.1 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45487   
   Windows Program
  Compatibility Assistant Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42828   
   Windows Projected File
  System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42837   
   Windows Projected File
  System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42969   
   Windows Push
  Notification Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   3 
   Info 
  
  
     CVE-2026-42971   
   Windows Push
  Notification Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-42970   
   Windows Push
  Notification Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-42973   
   Windows Push
  Notification Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-42978   
   Windows Push
  Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42977   
   Windows Push
  Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42979   
   Windows Push
  Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42991   
   Windows Push
  Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45639   
   Windows Remote Desktop
  Protocol (RDP) Information Disclosure Vulnerability 
   Important 
   7.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-42908   
   Windows Remote Desktop
  Protocol (RDP) Information Disclosure Vulnerability 
   Important 
   7.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-45593   
   Windows SDK Elevation
  of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42906   
   Windows Shell
  Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-42907   
   Windows Shell
  Information Disclosure Vulnerability 
   Important 
   6.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-47648   
   Windows Storage
  Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42915   
   Windows TCP/IP Denial
  of Service Vulnerability 
   Important 
   5.7 
   No 
   No 
   2 
   DoS 
  
  
     CVE-2026-42904   
   Windows TCP/IP
  Elevation of Privilege Vulnerability 
   Important 
   9.6 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-42968   
   Windows Telephony
  Server Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   2 
   Info 
  
  
     CVE-2026-42912   
   Windows Telephony
  Service Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-45597   
   Windows UI Automation
  Manager (uiamanager.dll) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   3 
   EoP 
  
  
     CVE-2026-45599   
   Windows UPnP Device
  Host Remote Code Execution Vulnerability 
   Important 
   8.1 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-45635   
   Windows UPnP Device
  Host Remote Code Execution Vulnerability 
   Important 
   8.1 
   No 
   No 
   2 
   RCE 
  
  
     CVE-2026-40409   
   Windows Universal Disk
  Format File System Driver (UDFS) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-40404   
   Windows Universal Disk
  Format File System Driver (UDFS) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   2 
   EoP 
  
  
     CVE-2026-42989   
   Winlogon
  Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   1 
   EoP 
  
 
  
    
    
    
    
    
    
    
    
  
 
 











  




    * Indicates this CVE had been released by a third party and is now being included in Microsoft releases .   † Indicates further administrative actions are required to fully address the vulnerability.    &nbsp;   Looking at the other Critical-rated bugs in this release, the scariest-looking one is actually nothing to concern yourself with at all. The CVSS 10 bug in Azure HorizonDB has already been addressed by Microsoft and is just being documented now. That’s also the case for five others. Of course, there wouldn’t be a release without Office bugs that have the Preview Pane as an attack vector. There are multiple in June. There’s a handful of bugs in the Remote Desktop Client, but these rely on connecting to a malicious RDP server. There are three patches for Hyper-V that allow for guest-to-host code execution. The bug in Active Directory requires authentication, but any authenticated user can hit it. For the Windows Directory Service vulnerability, it needs to be listening for TFTP. You have blocked that everywhere, right? The bug in Azure Network Adapter is somewhat unique as you need to update your Linux kernel to be protected. The bug in Azure Kubernetes allows an attacker to break out of a container and gain control of the AKS worker node. Finally, the bug in the Kerberos Key Distribution Center (KDC) seems unlikely, but if exploited, it could allow authenticated attackers to get code execution on affected systems.  Moving on to the other code execution bugs, there are the ubiquitous open-an-own bugs in Office components like Excel and Word. The code injection bug in Exchange Server looks troubling, but it requires a machine-in-the-middle (MiTM), so exploitation is unlikely. The bugs in SharePoint require authentication, but you should note that the patch applies to both SharePoint Server 2016 and SharePoint Enterprise Server 2016. The two bugs in UPnP are interesting. Both can lead to code execution by causing an error during the handling of specially crafted data, which could lead to a Use After Free (UAF) bug. The bugs in RDP Client all require connecting to a malicious RDP server, but it’s not clear why some are rated Critical and some are rated Important. The NTFS vulnerability requires a user to mount a virtual hard drive on an affected system. The last RCE bug this month is in Azure Stack Edge and requires the attacker to send a specially crafted file upload request that includes a manipulated file name or path, leading to code execution.  There are more than 60 Elevation of Privilege (EoP) bugs in this month’s release, and as usual, most simply lead to local attackers executing their code at SYSTEM-level privileges or administrative privileges, so there’s not much to add without further technical details about the bugs themselves. A notable exception is in Exchange Server, where a user on Outlook Web Access (OWA) could gain access to other mailboxes. The bug in Visual Studio Code could allow attackers to gain permissions associated with the MCP Server’s managed identity. The bugs in Windows SDK and Windows UI Automation Manager could let attacker go from low integrity up to medium integrity code execution. The bug in Bluetooth just allows “elevated” privileges without really describing what elevated might be.   Moving on to the more than 20 security feature bypass (SFB) bugs in the June release, there are a total of 10 that impact Secure Boot. All carry scope change (S:C) in the CVSS, meaning successful exploitation affects security boundaries beyond the vulnerable component itself — specifically the ability to load untrusted code at boot, bypass Virtual Secure Mode, and undermine boot integrity guarantees. CVE-2026-45654 explicitly calls out VSM exposure. The bulk of these are credited to Alon Leviev (STORM), which is notable given his prior BootKitty/BlackLotus-adjacent research. The bugs in the Windows Boot Manager have a similar impact as the Secure Boot bugs. The UEFI Secure Boot vulnerabilities go a layer deeper. They require either local admin or physical access but could allow for the running of untrusted code even before the OS loads. Rootkits anyone? The four bugs in BitLocker all require physical access but could yield encrypted data if exploited. The bug in Windows Administration Protection allows attackers to bypass the feature that prevents standard-user apps from performing admin-level actions. The bug in Visual Studio Copilot Chat could be the most interesting non-boot bug here as it allows authentication impersonation. Mark of the Web (MotW) and Excel vulns could bypass user warnings. Lastly, the bug in PC Manager bypasses expected user controls.   Turning our attention to the mass of spoofing bugs in the release, we instantly see 18 impacting SharePoint Server. Fortunately, these are simply cross-site scripting (XSS) bugs. It’s the Exchange bugs we should really watch for. One is an XSS that an attacker can exploit by convincing an Exchange administrator to open a malicious link or message, which then runs code in the admin's web session. That's a meaningful privilege escalation path. Another is listed as an SSRF-based attack, but no other details are available. The last is a lower-impact XSS with limited confidentiality/integrity loss. The bug in Bing Search (remember Bing?) is a classic search result spoofing. The bug in Azure Stack Edge is interesting as it could allow access to resources outside the vulnerable component's security boundary. The bug in Office for Android requires user interaction. The Office Project Server bug is an authenticated XSS with low impact. The final spoofing bug is in Azure Attestation but has already been addressed. You should still verify you are protected by following the instructions in the write-up from Microsoft.  There are 30 different information disclosure bugs in this release, and fortunately, the vast majority of these simply result in info leaks consisting of unspecified memory contents or memory addresses. The two bugs in Visual Studio require user interaction and could “disclose information over a network.” How obtuse. The bug in GitHub Copilot and Visual Studio Code could disclose discloses a sign-in access token for a user's work account. That's a meaningful credential exposure, not just random memory. That leaves the two bugs in Exchange Server. One could allow an authenticated user to gain information about which network services that the Exchange server can reach. The other sounds much like the spoofing bug in OWA as it allows attackers to see information in mailboxes they should not have access to.  I’ve never been a fan of the “tampering” category, as it could mean so many different things. For example, the bug in .NET simply says it could allow an unauthorized attacker to perform tampering locally. Similarly, the bug in Visual Studio says the same, expect here the tampering occurs over a network. Microsoft doesn’t even bother with a CWE for the tampering bug in the DHCP Server, so your guess is as good as mine.  There are seven DoS bugs in the June release, and as usual, Microsoft provides little to no actionable information about the vulnerabilities. The most interesting is the bug in HTTP.sys, which is listed as publicly known. This is an uncontrolled resource consumption, rated "Exploitation More Likely," and publicly disclosed. Since, HTTP.sys sits at the core of IIS and Windows web services, a network-accessible DoS here can take down any Windows server running HTTP-based services. Based on the Acknowledgement, it looks like this bug may have been found using AI. There are no real details for the other bugs, but based simply on the impact, I would focus on the Kerberos and TCP/IP bugs if you had to prioritize.  No new advisories are being released this month.   Looking Ahead   The next Patch Tuesday will be on July 14 and will be the last one before Black Hat/DEFCON. It’s usually a big release, so strap in and hang on. I’ll be back then to give you my full thoughts. Until then, stay safe, happy patching, and may all your reboots be smooth and clean!  &nbsp;
