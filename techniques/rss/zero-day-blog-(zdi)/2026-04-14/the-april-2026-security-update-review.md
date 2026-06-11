---
source: rss/zero-day-blog-(zdi)
title: The April 2026 Security Update Review
url: https://www.thezdi.com/blog/2026/4/14/the-april-2026-security-update-review
date: 2026-04-14
item_id: https://www.thezdi.com/blog/2026/4/14/the-april-2026-security-update-review
category: techniques
tags: [Bypass, CVE, Exploit, Race condition, Rce, Xss]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/4/14/the-april-2026-security-update-review

It’s time once again for Patch Tuesday, and this one is huge. We’ve also got multiple exploits in the wild, which adds another layer of urgency to this month’s release. Take a break from your regularly scheduled activities, and let’s take a look at the latest security patches from Adobe and Microsoft. If you’d rather watch the full video recap covering the entire release, you can check it out here: 





















  
  

















  
    
      
    
    
      
        
      
    
    
  




    Adobe Patches for April 2026   For April, Adobe released 12 bulletins addressing 61 unique CVEs in Adobe Acrobat Reader, InDesign, InCopy, FrameMaker, Connect, ColdFusion, Bridge, Photoshop, Illustrator, Experience Manager Screens, and the Adobe DNG SDK. Three of the Cold Fusion bugs came through the TrendAI ZDI program. For this month, I’m introducing an Adobe table as well. I’d love to get your feedback on whether this is helpful. 





















  
  




  
    


 
 
   
   
   
   
   
   
   
 
 
   
     Bulletin ID 
     Product 
     CVE Count 
     Highest Severity 
     Highest CVSS 
     Exploited 
     Deployment Priority 
   
 
 
   
      APSB26-43  
     Adobe Acrobat Reader 
     1 
     Critical 
     8.6 
     Yes 
     1 
   
   
      APSB26-44  
     Adobe Acrobat Reader 
     2 
     Critical 
     8.6 
     No 
     2 
   
   
      APSB26-32  
     Adobe InDesign 
     9 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-33  
     Adobe InCopy 
     2 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-36  
     Adobe FrameMaker 
     11 
     Critical 
     8.6 
     No 
     3 
   
   
      APSB26-37  
     Adobe Connect 
     9 
     Critical 
     9.6 
     No 
     3 
   
   
      APSB26-38  
     Adobe ColdFusion 
     7 
     Critical 
     9.3 
     No 
     1 
   
   
      APSB26-39  
     Adobe Bridge 
     6 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-40  
     Adobe Photoshop 
     1 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-42  
     Adobe Illustrator 
     1 
     Critical 
     7.8 
     No 
     3 
   
   
      APSB26-34  
     Adobe Experience Manager Screens 
     9 
     Important 
     5.4 
     No 
     3 
   
   
      APSB26-41  
     Adobe DNG SDK 
     3 
     Important 
     5.5 
     No 
     3 
   
 
 



  




   Obviously, the active attack in Reader is the highest priority for this month, but don’t ignore the second bunch of Reader patches. Cold Fusion also gets a deployment priority of 1, so if you’re still running that platform, make sure you get the update. Otherwise, the FrameMaker and Connect patches fix 11 and nine bugs, respectively. InDesign and Experience Manager Screens also have nine CVEs addressed.   Outside of the Reader bug, none of the other bugs fixed by Adobe this month are listed as publicly known or under active attack at the time of release. One of the Reader bugs and Cold Fusion have a deployment priority of one, the other Reader bug has a priority of two, while all of the other updates released by Adobe this month are listed as deployment priority 3.   Microsoft Patches for April 2026   This month, Microsoft released a monstrous 163 new CVEs in Windows and Windows components, Office and Office Components, Microsoft Edge (Chromium-based), Azure, .NET and Visual Studio, SQL Server, Hyper-V Server, BitLocker, and the Windows Wallet Service. Counting the third-party and a huge Chromium release, it brings the total number of CVEs to a staggering 247 updates. Six of these bugs were reported through the TrendAI ZDI program. Eight of these bugs are rated Critical, two are rated as Moderate, and the rest are rated Important in severity.  By my count, this is the second-largest monthly release in Microsoft’s history. There are many things we could speculate on to justify the size, but if Microsoft is like the other programs out there (including ours), they are likely seeing a rise in submissions found by AI tools. For us, our incoming rate has essentially tripled, making triage a challenge, to say the least. Whatever the reason, we have a lot of bugs to deal with this month. I should also point out that the Pwn2Own Berlin occurs next month, and it’s typical for vendors to patch as much as they can before the event.  There is one Microsoft bug listed as under active attack at the time of release, and one other that’s publicly known. Let’s take a closer look at some of the more interesting updates for this month, starting with the vulnerability being exploited in the wild:  -&nbsp;&nbsp;&nbsp;   CVE-2026-32201    - Microsoft SharePoint Server Spoofing Vulnerability  Microsoft doesn’t provide a lot of information about this bug, but Spoofing bugs in SharePoint often manifest as cross-site scripting (XSS) bugs. They do note that attackers could view information or make changes to disclosed information. As always, they don’t provide any information on how widespread these attacks are, but I wouldn’t wait to test and deploy this fix – especially if you have internet-connected SharePoint servers.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-33825    - Microsoft Defender Elevation of Privilege Vulnerability  This bug is listed as publicly known, and this time, we know exactly  where  it was disclosed. There have been some questions about how exploitable this bug may be, but it does look like it’s a real problem – just with some reliability issues in its current state. I won’t add on to the commentary from the researcher about working with Microsoft. I’m just glad they are offering a fix for the vulnerability. If you rely on Defender, test and deploy this one quickly.  -&nbsp;&nbsp;   CVE-2026-33827    - Windows TCP/IP Remote Code Execution Vulnerability  This vulnerability allows remote, unauthenticated attackers to exploit code on affected systems without user interaction. That adds up to a wormable bug – at least on systems with IPv6 and IPSec enabled. It is a race condition, which sets exploitability to High on the CVSS scale, but we see race conditions exploited at Pwn2Own all the time, so don’t rely on that obstacle. If you’re running IPv6, I would test and deploy this fix quickly before public exploits become available.  -&nbsp;&nbsp;&nbsp;   CVE-2026-33824    - Windows Internet Key Exchange (IKE) Service Extensions Remote Code Execution Vulnerability  Speaking of wormable bugs, here’s our second one this month. By the title, we can tell that systems with IKE enabled are affected, but that leaves plenty of targets for attackers. Microsoft also notes a significant mitigation for this bug. Blocking UDP ports 500 and 4500 at the perimeter prevents external attackers from reaching the affected service. However, insiders could still target this for lateral movement within an enterprise. For enterprises using IKE, get this fix tested and deployed with haste.  Here’s the full list of CVEs released by Microsoft for April 2026: 





















  
  




  
    




April 2026 Patch Tuesday



 
  
   CVE 
   Title 
   Severity 
   CVSS 
   Public 
   Exploited 
   Type 
  
 
 
    CVE-2026-32201  
   Microsoft SharePoint Server Spoofing Vulnerability 
   Important 
   6.5 
   No 
   Yes 
   Spoofing 
 
 
    CVE-2026-5281 *  
   Chromium: CVE-2026-5281 Use after free in Dawn 
   High 
   N/A 
   No 
   Yes 
   RCE 
 
 
    CVE-2026-33825  
   Microsoft Defender Elevation of Privilege Vulnerability 
   Important 
   7.8 
   Yes 
   No 
   EoP 
 
 
    CVE-2026-23666  
   .NET Framework Denial of Service Vulnerability 
   Critical 
   7.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-32190  
   Microsoft Office Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
 
 
    CVE-2026-33114  
   Microsoft Word Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
 
 
    CVE-2026-33115  
   Microsoft Word Remote Code Execution Vulnerability 
   Critical 
   8.4 
   No 
   No 
   RCE 
 
 
    CVE-2026-32157  
   Remote Desktop Client Remote Code Execution Vulnerability 
   Critical 
   8.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-33826  
   Windows Active Directory Remote Code Execution Vulnerability 
   Critical 
   8 
   No 
   No 
   RCE 
 
 
    CVE-2026-33824  
   Windows Internet Key Exchange (IKE) Service Extensions Remote Code Execution Vulnerability 
   Critical 
   9.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-33827  
   Windows TCP/IP Remote Code Execution Vulnerability 
   Critical 
   8.1 
   No 
   No 
   RCE 
 
 
    CVE-2026-26171  
   .NET Denial of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-32226  
   .NET Framework Denial of Service Vulnerability 
   Important 
   5.9 
   No 
   No 
   DoS 
 
 
    CVE-2026-32178  
   .NET Spoofing Vulnerability 
   Important 
   7.5 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-32203  
   .NET and Visual Studio Denial of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-33116  
   .NET, .NET Framework, and Visual Studio Denial of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
 
 
    CVE-2023-20585 *  
   AMD: CVE-2023-20585 IOMMU Write Buffer Vulnerability 
   Important 
   5.3 
   No 
   No 
   RCE 
 
 
    CVE-2026-32072  
   Active Directory Spoofing Vulnerability 
   Important 
   6.2 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-25184  
   Applocker Filter Driver (applockerfltr.sys) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32171  
   Azure Logic Apps Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32168  
   Azure Monitor Agent Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32192  
   Azure Monitor Agent Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32181  
   Connected User Experiences and Telemetry Service Denial of Service Vulnerability 
   Important 
   5.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-27924  
   Desktop Window Manager Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32152  
   Desktop Window Manager Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32154  
   Desktop Window Manager Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27923  
   Desktop Window Manager Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32155  
   Desktop Window Manager Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-23653  
   GitHub Copilot and Visual Studio Code Information Disclosure Vulnerability 
   Important 
   5.7 
   No 
   No 
   Info 
 
 
    CVE-2026-23653 *  
    GitHub: CVE-2026-32631 &#x27;git clone&#x27; from manipulated repositories can leak NTLM hashes  
   Important 
   7.4 
   No 
   No 
   Info 
 
 
    CVE-2026-33096  
   HTTP.sys Denial of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-25250 *  
   MITRE: CVE-2026-25250 Secure Boot disable Eazy Fix 
   Important 
   6 
   No 
   No 
   SFB 
 
 
    CVE-2026-26181  
   Microsoft Brokering File System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32219  
   Microsoft Brokering File System Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32091  
   Microsoft Brokering File System Elevation of Privilege Vulnerability 
   Important 
   8.4 
   No 
   No 
   EoP 
 
 
    CVE-2026-26152  
   Microsoft Cryptographic Services Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-33103  
   Microsoft Dynamics 365 (On-Premises) Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32188  
   Microsoft Excel Information Disclosure Vulnerability 
   Important 
   7.1 
   No 
   No 
   Info 
 
 
    CVE-2026-32189  
   Microsoft Excel Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32197  
   Microsoft Excel Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32198  
   Microsoft Excel Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32199  
   Microsoft Excel Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32184  
   Microsoft High Performance Compute (HPC) Pack Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26155  
   Microsoft Local Security Authority Subsystem Service Information Disclosure Vulnerability 
   Important 
   6.5 
   No 
   No 
   Info 
 
 
    CVE-2026-27914  
   Microsoft Management Console Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26149  
   Microsoft Power Apps Security Feature Bypass 
   Important 
   9 
   No 
   No 
   SFB 
 
 
    CVE-2026-32200  
   Microsoft PowerPoint Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-26143  
   Microsoft PowerShell Security Feature Bypass Vulnerability 
   Important 
   7.8 
   No 
   No 
   SFB 
 
 
    CVE-2026-33120 †  
   Microsoft SQL Server Remote Code Execution Vulnerability 
   Important 
   8.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-20945  
   Microsoft SharePoint Server Spoofing Vulnerability 
   Important 
   4.6 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-33822  
   Microsoft Word Information Disclosure Vulnerability 
   Important 
   6.1 
   No 
   No 
   Info 
 
 
    CVE-2026-33095  
   Microsoft Word Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-23657  
   Microsoft Word Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32081  
   Package Catalog Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-26170  
   PowerShell Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26183  
   Remote Access Management service/API (RPC server) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26160  
   Remote Desktop Licensing Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26159  
   Remote Desktop Licensing Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26151  
   Remote Desktop Spoofing Vulnerability 
   Important 
   7.1 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-32085  
   Remote Procedure Call Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32167  
   SQL Server Elevation of Privilege Vulnerability 
   Important 
   6.7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32176  
   SQL Server Elevation of Privilege Vulnerability 
   Important 
   6.7 
   No 
   No 
   EoP 
 
 
    CVE-2026-0390  
   UEFI Secure Boot Security Feature Bypass Vulnerability 
   Important 
   6.7 
   No 
   No 
   SFB 
 
 
    CVE-2026-32220  
   UEFI Secure Boot Security Feature Bypass Vulnerability 
   Important 
   4.4 
   No 
   No 
   SFB 
 
 
    CVE-2026-32212  
   Universal Plug and Play (upnp.dll) Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32214  
   Universal Plug and Play (upnp.dll) Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32079  
   Web Account Manager Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-33104  
   Win32k Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32196  
   Windows Admin Center Spoofing Vulnerability 
   Important 
   6.1 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-26178  
   Windows Advanced Rasterization Platform Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32073  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-26168  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26173  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-26177  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-26182  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-27922  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-33099  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-33100  
   Windows Ancillary Function Driver for WinSock Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32088  
   Windows Biometric Service Security Feature Bypass Vulnerability 
   Important 
   6.1 
   No 
   No 
   SFB 
 
 
    CVE-2026-27913  
   Windows BitLocker Security Feature Bypass Vulnerability 
   Important 
   7.7 
   No 
   No 
   SFB 
 
 
    CVE-2026-26175  
   Windows Boot Manager Security Feature Bypass Vulnerability 
   Important 
   4.6 
   No 
   No 
   SFB 
 
 
    CVE-2026-32162  
   Windows COM Elevation of Privilege Vulnerability 
   Important 
   8.4 
   No 
   No 
   EoP 
 
 
    CVE-2026-20806  
   Windows COM Server Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-26176  
   Windows Client Side Caching driver (csc.sys) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27926  
   Windows Cloud Files Mini Filter Driver Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32070  
   Windows Common Log File System Driver Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-33098  
   Windows Container Isolation FS Filter Driver Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26153  
   Windows Encrypted File System (EFS) Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32087  
   Windows Function Discovery Service (fdwsd.dll) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32093  
   Windows Function Discovery Service (fdwsd.dll) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32086  
   Windows Function Discovery Service (fdwsd.dll) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32150  
   Windows Function Discovery Service (fdwsd.dll) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-27931  
   Windows GDI Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-27930  
   Windows GDI Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32221  
   Windows Graphics Component Remote Code Execution Vulnerability 
   Important 
   8.4 
   No 
   No 
   RCE 
 
 
    CVE-2026-27906  
   Windows Hello Security Feature Bypass Vulnerability 
   Important 
   4.4 
   No 
   No 
   SFB 
 
 
    CVE-2026-27928  
   Windows Hello Security Feature Bypass Vulnerability 
   Important 
   8.7 
   No 
   No 
   SFB 
 
 
    CVE-2026-26156  
   Windows Hyper-V Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32149  
   Windows Hyper-V Remote Code Execution Vulnerability 
   Important 
   7.3 
   No 
   No 
   RCE 
 
 
    CVE-2026-27910  
   Windows Installer Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27912  
   Windows Kerberos Elevation of Privilege Vulnerability 
   Important 
   8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26179  
   Windows Kernel Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26180  
   Windows Kernel Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32195  
   Windows Kernel Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-26163  
   Windows Kernel Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32215  
   Windows Kernel Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32217  
   Windows Kernel Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32218  
   Windows Kernel Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-26169  
   Windows Kernel Memory Information Disclosure Vulnerability 
   Important 
   6.1 
   No 
   No 
   Info 
 
 
    CVE-2026-27929  
   Windows LUA File Virtualization Filter Driver Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32071  
   Windows Local Security Authority Subsystem Service (LSASS) Denial of Service Vulnerability 
   Important 
   7.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-20930  
   Windows Management Services Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26162  
   Windows OLE Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-33101  
   Windows Print Spooler Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32084  
   Windows Print Spooler Information Disclosure Vulnerability 
   Important 
   5.5 
   No 
   No 
   Info 
 
 
    CVE-2026-27927  
   Windows Projected File System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26184  
   Windows Projected File System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32069  
   Windows Projected File System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32074  
   Windows Projected File System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32078  
   Windows Projected File System Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26167  
   Windows Push Notifications Elevation of Privilege Vulnerability 
   Important 
   8.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32158  
   Windows Push Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32159  
   Windows Push Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32160  
   Windows Push Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26172  
   Windows Push Notifications Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-20928  
   Windows Recovery Environment Security Feature Bypass Vulnerability 
   Important 
   4.6 
   No 
   No 
   SFB 
 
 
    CVE-2026-32216  
   Windows Redirected Drive Buffering System Denial of Service Vulnerability 
   Important 
   5.5 
   No 
   No 
   DoS 
 
 
    CVE-2026-27909  
   Windows Search Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26161  
   Windows Sensor Data Service Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-26174  
   Windows Server Update Service (WSUS) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32224  
   Windows Server Update Service (WSUS) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-26154  
   Windows Server Update Service (WSUS) Tampering Vulnerability 
   Important 
   7.5 
   No 
   No 
   Tampering 
 
 
    CVE-2026-26165  
   Windows Shell Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-26166  
   Windows Shell Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-27918  
   Windows Shell Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32151  
   Windows Shell Information Disclosure Vulnerability 
   Important 
   6.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32225  
   Windows Shell Security Feature Bypass Vulnerability 
   Important 
   8.8 
   No 
   No 
   SFB 
 
 
    CVE-2026-32202  
   Windows Shell Spoofing Vulnerability 
   Important 
   4.3 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-32082  
   Windows Simple Search and Discovery Protocol (SSDP) Service Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32083  
   Windows Simple Search and Discovery Protocol (SSDP) Service Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32068  
   Windows Simple Search and Discovery Protocol (SSDP) Service Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32183  
   Windows Snipping Tool Remote Code Execution Vulnerability 
   Important 
   7.8 
   No 
   No 
   RCE 
 
 
    CVE-2026-32089  
   Windows Speech Brokered Api Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32090  
   Windows Speech Brokered Api Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32153  
   Windows Speech Runtime Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27907  
   Windows Storage Spaces Controller Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32076  
   Windows Storage Spaces Controller Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27908  
   Windows TDI Translation Driver (tdx.sys) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-27921  
   Windows TDI Translation Driver (tdx.sys) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-27915  
   Windows UPnP Device Host Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27919  
   Windows UPnP Device Host Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32075  
   Windows UPnP Device Host Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-27916  
   Windows UPnP Device Host Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27920  
   Windows UPnP Device Host Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32077  
   Windows UPnP Device Host Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27925  
   Windows UPnP Device Host Information Disclosure Vulnerability 
   Important 
   6.5 
   No 
   No 
   Info 
 
 
    CVE-2026-32156  
   Windows UPnP Device Host Remote Code Execution Vulnerability 
   Important 
   7.4 
   No 
   No 
   RCE 
 
 
    CVE-2026-32223  
   Windows USB Printing Stack (usbprint.sys) Elevation of Privilege Vulnerability 
   Important 
   6.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32165  
   Windows User Interface Core Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-27911  
   Windows User Interface Core Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32163  
   Windows User Interface Core Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-32164  
   Windows User Interface Core Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-23670  
   Windows Virtualization-Based Security (VBS) Security Feature Bypass Vulnerability 
   Important 
   5.7 
   No 
   No 
   SFB 
 
 
    CVE-2026-27917  
   Windows WFP NDIS Lightweight Filter Driver (wfplwfs.sys) Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32080  
   Windows WalletService Elevation of Privilege Vulnerability 
   Important 
   7 
   No 
   No 
   EoP 
 
 
    CVE-2026-32222  
   Windows Win32k Elevation of Privilege Vulnerability 
   Important 
   7.8 
   No 
   No 
   EoP 
 
 
    CVE-2026-21637 *  
    HackerOne: CVE-2026-21637 TLS PSK/ALPN Callback Exceptions Bypass Error Handlers 
    Moderate 
   7.5 
   No 
   No 
   SFB 
 
 
    CVE-2026-33119  
   Microsoft Edge (Chromium-based) for Android Spoofing Vulnerability 
   Moderate 
   5.4 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-33829  
   Windows Snipping Tool Spoofing Vulnerability 
   Moderate 
   4.3 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5858 *  
   Chromium: CVE-2026-5858 Heap buffer overflow in WebML 
   Critical 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5859 *  
   Chromium: CVE-2026-5859 Integer overflow in WebML 
   Critical 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5272 *  
   Chromium: CVE-2026-5272 Heap buffer overflow in GPU 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5273 *  
   Chromium: CVE-2026-5273 Use after free in CSS 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5274 *  
   Chromium: CVE-2026-5274 Integer overflow in Codecs 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5275 *  
   Chromium: CVE-2026-5275 Heap buffer overflow in ANGLE 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5276 *  
   Chromium: CVE-2026-5276 Insufficient policy enforcement in WebUSB 
   High 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5277 *  
   Chromium: CVE-2026-5277 Integer overflow in ANGLE 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5279 *  
   Chromium: CVE-2026-5279 Object corruption in V8 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5280 *  
   Chromium: CVE-2026-5280 Use after free in WebCodecs 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5283 *  
   Chromium: CVE-2026-5283 Inappropriate implementation in ANGLE 
   High 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5284 *  
   Chromium: CVE-2026-5284 Use after free in Dawn 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5285 *  
   Chromium: CVE-2026-5285 Use after free in WebGL 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5286 *  
   Chromium: CVE-2026-5286 Use after free in Dawn 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5287 *  
   Chromium: CVE-2026-5287 Use after free in PDF 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5289 *  
   Chromium: CVE-2026-5289 Use after free in Navigation 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5290 *  
   Chromium: CVE-2026-5290 Use after free in Compositing 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5860 *  
   Chromium: CVE-2026-5860 Use after free in WebRTC 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5861 *  
   Chromium: CVE-2026-5861 Use after free in V8 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5862 *  
   Chromium: CVE-2026-5862 Inappropriate implementation in V8 
   High 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5863 *  
   Chromium: CVE-2026-5863 Inappropriate implementation in V8 
   High 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5864 *  
   Chromium: CVE-2026-5864 Heap buffer overflow in WebAudio 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5865 *  
   Chromium: CVE-2026-5865 Type Confusion in V8 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5866 *  
   Chromium: CVE-2026-5866 Use after free in Media 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5867 *  
   Chromium: CVE-2026-5867 Heap buffer overflow in WebML 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5868 *  
   Chromium: CVE-2026-5868 Heap buffer overflow in ANGLE 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5869 *  
   Chromium: CVE-2026-5869 Heap buffer overflow in WebML 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5870 *  
   Chromium: CVE-2026-5870 Integer overflow in Skia 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5871 *  
   Chromium: CVE-2026-5871 Type Confusion in V8 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5872 *  
   Chromium: CVE-2026-5872 Use after free in Blink 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5873 *  
   Chromium: CVE-2026-5873 Out of bounds read and write in V8 
   High 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5291 *  
   Chromium: CVE-2026-5291 Inappropriate implementation in WebGL 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5292 *  
   Chromium: CVE-2026-5292 Out of bounds read in WebCodecs 
   Medium 
   N/A 
   No 
   No 
   Info 
 
 
    CVE-2026-5874 *  
   Chromium: CVE-2026-5874 Use after free in PrivateAI 
   Medium 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5875 *  
   Chromium: CVE-2026-5875 Policy bypass in Blink 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5876 *  
   Chromium: CVE-2026-5876 Side-channel information leakage in Navigation 
   Medium 
   N/A 
   No 
   No 
   Info 
 
 
    CVE-2026-5877 *  
   Chromium: CVE-2026-5877 Use after free in Navigation 
   Medium 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5878 *  
   Chromium: CVE-2026-5878 Incorrect security UI in Blink 
   Medium 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5879 *  
   Chromium: CVE-2026-5879 Insufficient validation of untrusted input in ANGLE 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5880 *  
   Chromium: CVE-2026-5880 Incorrect security UI in browser UI 
   Medium 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5881 *  
   Chromium: CVE-2026-5881 Policy bypass in LocalNetworkAccess 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5882 *  
   Chromium: CVE-2026-5882 Incorrect security UI in Fullscreen 
   Medium 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5883 *  
   Chromium: CVE-2026-5883 Use after free in Media 
   Medium 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5884 *  
   Chromium: CVE-2026-5884 Insufficient validation of untrusted input in Media 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5885 *  
   Chromium: CVE-2026-5885 Insufficient validation of untrusted input in WebML 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5886 *  
   Chromium: CVE-2026-5886 Out of bounds read in WebAudio 
   Medium 
   N/A 
   No 
   No 
   Info 
 
 
    CVE-2026-5887 *  
   Chromium: CVE-2026-5887 Insufficient validation of untrusted input in Downloads 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5888 *  
   Chromium: CVE-2026-5888 Uninitialized Use in WebCodecs 
   Medium 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5889 *  
   Chromium: CVE-2026-5889 Cryptographic Flaw in PDFium 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5890 *  
   Chromium: CVE-2026-5890 Race in WebCodecs 
   Medium 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5891 *  
   Chromium: CVE-2026-5891 Insufficient policy enforcement in browser UI 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5892 *  
   Chromium: CVE-2026-5892 Insufficient policy enforcement in PWAs 
   Medium 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5893 *  
   Chromium: CVE-2026-5893 Race in V8 
   Medium 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5894 *  
   Chromium: CVE-2026-5894 Inappropriate implementation in PDF 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5895 *  
   Chromium: CVE-2026-5895 Incorrect security UI in Omnibox 
   Low 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5896 *  
   Chromium: CVE-2026-5896 Policy bypass in Audio 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5897 *  
   Chromium: CVE-2026-5897 Incorrect security UI in Downloads 
   Low 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5898 *  
   Chromium: CVE-2026-5898 Incorrect security UI in Omnibox 
   Low 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5899 *  
   Chromium: CVE-2026-5899 Incorrect security UI in History Navigation 
   Low 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5900 *  
   Chromium: CVE-2026-5900 Policy bypass in Downloads 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5901 *  
   Chromium: CVE-2026-5901 Policy bypass in DevTools 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5902 *  
   Chromium: CVE-2026-5902 Race in Media 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5903 *  
   Chromium: CVE-2026-5903 Policy bypass in IFrameSandbox 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5904 *  
   Chromium: CVE-2026-5904 Use after free in V8 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5905 *  
   Chromium: CVE-2026-5905 Incorrect security UI in Permissions 
   Low 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5906 *  
   Chromium: CVE-2026-5906 Incorrect security UI in Omnibox 
   Low 
   N/A 
   No 
   No 
   Spoofing 
 
 
    CVE-2026-5907 *  
   Chromium: CVE-2026-5907 Insufficient data validation in Media 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5908 *  
   Chromium: CVE-2026-5908 Integer overflow in Media 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5909 *  
   Chromium: CVE-2026-5909 Integer overflow in Media 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5910 *  
   Chromium: CVE-2026-5910 Integer overflow in Media 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5911 *  
   Chromium: CVE-2026-5911 Policy bypass in ServiceWorkers 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5912 *  
   Chromium: CVE-2026-5912 Integer overflow in WebRTC 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5913 *  
   Chromium: CVE-2026-5913 Out of bounds read in Blink 
   Low 
   N/A 
   No 
   No 
   Info 
 
 
    CVE-2026-5914 *  
   Chromium: CVE-2026-5914 Type Confusion in CSS 
   Low 
   N/A 
   No 
   No 
   RCE 
 
 
    CVE-2026-5915 *  
   Chromium: CVE-2026-5915 Insufficient validation of untrusted input in WebML 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5918 *  
   Chromium: CVE-2026-5918 Inappropriate implementation in Navigation 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-5919 *  
   Chromium: CVE-2026-5919 Insufficient validation of untrusted input in WebSockets 
   Low 
   N/A 
   No 
   No 
   SFB 
 
 
    CVE-2026-33118  
   Microsoft Edge (Chromium-based) Spoofing Vulnerability 
   Low 
   4.3 
   No 
   No 
   Spoofing 
 
  
  




    * Indicates this CVE had been released by a third party and is now being included in Microsoft releases .   † Indicates further administrative actions are required to fully address the vulnerability.    &nbsp;   Looking at the other Critical-rated bugs in this month’s release, there are three Office-related bugs where the Preview Pane is once again listed as an exploit vector. I would still like to have a full-proof way of disabling the Preview Pane, but I don’t see that as an option. There’s a bug in the RDP client, but that involves connecting to a malicious RDP server. The bug in Active Directory requires authentication and a network adjacent attacker. The final Critical-rated bug is an interesting DoS in .NET Framework. An unauthenticated attacker could deny service over a network – presumably crippling any affected app made in .NET. You rarely see Critical-rated DoS bugs, but this one deserves the moniker.  Moving on to the other code execution bugs, you have quite a few open-and-own bugs in Office components, most notably Excel, where the Preview Pane is not an attack vector. The bug in SQL Server requires authentication, and as usual, additional steps are needed to ensure you have the correct update to remediate this vulnerability. The two bugs in Hyper-V almost reads like a privilege escalation since it allows unauthorized attackers to execute code locally. That’s the same for the bugs in the Windows Snipping Tool and the UPnP Device host.   More than half of this release addresses Elevation of Privilege (EoP) bugs. However, most simply lead to local attackers executing their code at SYSTEM-level privileges or administrative privileges, so there’s not much to add without further technical details about the bugs themselves. The bugs in SQL Server could allow an attacker to gain SQL sysadmin privileges. One of the kernel bugs simply states an attacker could “elevate privileges locally”. How obtuse. That’s similar for the bug in afd.sys and Desktop Windows Manager, but Microsoft also states that these bugs could crash an affected system. There are several bugs that result in a sandbox escape, including Windows Push Notifications, AFD for Winsock, Management Services, and User Interface Core. Of these, CVE-2026-26167 (Push Notifications) is the most notable — it's the only one with low attack complexity, meaning no race condition needed. The rest all require winning a race condition (AC:H). The bugs in UPnP are interesting as they allow attackers to gain access to a limited set of administrator-protected objects. Not a full escalation but definitely getting access to resources they shouldn’t. The vulnerability in the Brokering File System allows attackers to gain the level of the logged on user, so don’t do your normal activities as a user with admin privileges. The bug in Azure Monitor Agent leads to root-level access.   There are a dozen different security features bypass bugs in the April release. Some of these are obvious by the title alone. For example, the bugs in Windows Hello bypass safety features within the Hello app itself. The bug in the Biometric Service allows attackers to bypass biometric protections. The vulns in BitLocker and Secure Boot bypass protections in those components. The bug in Power Apps allows attackers to bypass a security warning dialog and trick targets into triggering an external protocol call that performs unintended actions on the user’s device. The bug in Windows Shell allows attackers to bypass Mark of the Web (MotW) protections. The bug in PowerShell could almost be described as a code execution bug as exploiting it bypasses dynamic-expression security checks, which could result in code execution. The vulnerability in the Windows Recovery Environment allows local attackers to bypass BitLocker device encryption. Finally, the bug in Virtualization‑Based Security (VBS) is the most interesting of the bunch – and not just because VBS is a (relatively) new feature. The problem allows attackers to manipulate allow a compromised Windows kernel to modify memory belonging to the secure kernel, breaking the intended isolation guarantees provided by VBS. Somewhat of a sandbox escape, but this time, you’re escaping from Virtual Trust Level 0 (VTL0) to Virtual Trust Level 1 (VTL1). Neat.  Moving on to the Information Disclosure bugs fixed this month, we have 20 different CVEs. Fortunately, most of these simply result in info leaks consisting of unspecified memory contents or memory addresses. While useful in crafting exploits, they aren’t exactly exciting on their own. There are also several bugs that disclose addresses from an object a contained in a sandboxed execution environment. This includes bugs in the Print Spooler, Package Catalog, and Web Account Manager. The bug in Dynamics 365 discloses the ever ineffable “sensitive information”. There are three different info disclosure bugs in UPnP. Two allow an attacker to read from the file system, while the third discloses anything available to the LOCAL SERVICE account. The final info disclosure bug resides in Copilot and Visual Studio and allows attackers to disclose the contents of the Model Context Protocol (MCP) when using Copilot. There are those who think MCP is dead (thanks to agentic AI agents), but if you’re using a custom MCP, I doubt you would want it leaked.  The April release contains just a handful of Spoofing bugs. Some, like the bugs in .NET, Active Directory, and Windows Shell, just say that they allow spoofing over a network. Others, like the bug in Windows Snipping Tool, say similar but also note that it could be used to relay NTLMv2 hashes. The patch for RDP  notes  that there are new warning dialogs coming this month. The bug in the Windows Admin Center would allow an attacker to interact with other tenant’s applications and content. Finally, the spoofing bug in SharePoint is another XSS issue.  There are eight DoS bugs in the April release, but as always, Microsoft provides no actionable information about the vulnerabilities. Microsoft does offer a mitigation for the http.sys bug that can be applied while you test and deploy the patch, but I would rely on the patch rather than the mitigation. Another exception is the bug for Connected User Experiences and Telemetry Service, which allows attackers to deny service locally rather than over the network.  The final(!) bug in the April release is a Tampering bug in WSUS that reads like a DoS. According to Microsoft, “An attacker can send specially crafted packets which could affect availability of the service and result in Denial of Service (DoS).” But sure – let’s call it Tampering.   No new advisories are being released this month.   Looking Ahead   I will be in Berlin for the next Patch Tuesday, which will be May 12, and I’ll provide my full thoughts then on what will hopefully be a smaller release than this one. Until then, stay safe, happy patching, and may all your reboots be smooth and clean!
