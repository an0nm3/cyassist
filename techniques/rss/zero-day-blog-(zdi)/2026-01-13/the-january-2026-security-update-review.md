---
source: rss/zero-day-blog-(zdi)
title: The January 2026 Security Update Review
url: https://www.thezdi.com/blog/2026/1/13/the-january-2026-security-update-review
date: 2026-01-13
item_id: https://www.thezdi.com/blog/2026/1/13/the-january-2026-security-update-review
category: techniques
tags: [Bypass, CVE, Exploit, Rce, Xss]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/1/13/the-january-2026-security-update-review

I may be in Tokyo preparing for Pwn2Own Automotive, but that doesn’t stop patch Tuesday from coming. Put aside your broken New Year’s resolutions for just a moment as we review the latest security patches from Adobe and Microsoft. If you’d rather watch the full video recap covering the entire release, you can check it out here: 





















  
  

















  
    
      
    
    
      
        
      
    
    
  




    Adobe Patches for January 2026   For January, Adobe released 11 bulletins addressing 25 unique CVEs in Adobe Dreamweaver, InDesign, Illustrator, InCopy, Bridge, Substance 3D Modeler, Substance 3D Stager, Substance 3D Painter, Substance 3D Sampler, Substance 3D Designer, and ColdFusion. The patch for  ColdFusion  fixes a single code execution bug, but the update is listed as Priority 1. It isn’t publicly known or under active attack, though. The fix for  Dreamweaver  corrects five Critical-rated code execution bugs. The update for  InDesign  also has five CVEs, but only four are rated Critical. The  Substance 3D Modeler  patch contains six fixes total, but only two are for arbitrary code execution.  The patch for  Substance 3D Stager  fixes a single, Critical-rated code execution bug. That’s the same story for  Substance 3D Painter ,  Adobe Bridge , and  InCopy . The patch for  Substance 3D Sampler  is a bit odd. It states that it was released in August but updated today. The CVE is from 2026, so this may just be a clerical error. The patch for  Substance 3D Designer  fixes a single Important-severity memory leak. Finally, the fix for  Illustrator  includes one Critical-rated and one Important-severity bug.  None of the bugs fixed by Adobe this month are listed as publicly known or under active attack at the time of release. Besides the fix for ColdFusion, all of the updates released by Adobe this month are listed as deployment priority 3.   Microsoft Patches for January 2026   Microsoft kicks off the new year with a bang, dropping 112 new CVEs in Windows and Windows components, Office and Office Components, Azure, Microsoft Edge (Chromium-based), SharePoint Server, SQL Server, SMB Server, and Windows Management Services.   One of these bugs came through the ZDI program. Of the patches released today, eight are rated Critical while the rest are rated Important in severity. Counting the third-party Chromium updates listed in the release, it brings to total number of CVEs to 114.  It’s not uncommon to see a large release in January. I suspect vendors hold off on certain updates through the holiday season to prevent disruptions should patches fail or cause application compatibility issues. This results in a large January release. Last year was Microsoft’s second busiest in terms of CVEs released. We’ll see if they top that in 2026.  Microsoft lists one bug under active attack, but two others as publicly known at the time of the release (although I think that number should be three). Let’s take a closer look at some of the more interesting updates for this month, starting with the bug under active attack:   -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-20805    - Desktop Window Manager Information Disclosure Vulnerability  It’s a bit unusual to see an information disclosure bug exploited in the wild, but that’s what we have here. This bug allows an attacker to leak a section address from a remote ALPC port. Presumably, threat actors would then use the address in the next stage of their exploit chain – probably gaining arbitrary code execution. This shows how memory leaks can be as important as code execution bugs since they make the RCEs reliable. As always, Microsoft offers no indication of how widespread these exploits may be, but considering the source, they are likely limited.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-21265    - Secure Boot Certificate Expiration Security Feature Bypass Vulnerability  While unlikely to be exploited, this bug could cause quite a bit of headaches for administrators. You will need to update the expiring certificates to continue receiving security updates or trusting new boot loaders. Again, the chances this CVE gets exploited are low. However, the chance this CVE gets ignored and devices using Secure Boot don’t receive patches is quite high. Also, this is listed as publicly known, but that just means Microsoft published information about this months ago.  -&nbsp;&nbsp;&nbsp;   CVE-2026-20952   /   202953    - Microsoft Office Remote Code Execution Vulnerability  Another month with Preview Pane exploit vectors in an Office bug. While we are still unaware of any exploitation of these bugs, they keep adding up. It’s only a matter of time until threat actors find a way to use these types of bugs in their exploits. If you are concerned about these, you can take the extra precaution of disabling the Preview Pane, which at least prevents exploitation without user interaction.  -&nbsp;&nbsp;&nbsp;   CVE-2026-20876    – Windows Virtualization-Based Security (VBS) Enclave Elevation of Privilege Vulnerability  VBS is a newer security feature in Windows, and Virtual Trust Levels (VTL) serve as different privilege levels. VTL2 is currently the highest privileged level, and this bug allows attackers to escalate to VTL2. Microsoft doesn’t say if you need to be at VTL0 or VTL1 to exploit this bug. As far as I can recall, this is the first VTL escalation bug patched within VBS. Microsoft lists this as CVSS 6.7, but I believe this is a scope change since you’re traversing VTL levels. Taking that into consideration makes the&nbsp; CVSS score 8.2 (High).  Here’s the full list of CVEs released by Microsoft for January 2026: 





















  
  




  
    



















 
  
  
  
  
  
  
      CVE    
      Title    
      Severity    
      CVSS    
      Public 
      Exploited    
      Type    
  
  
        CVE-2026-20805      
      Desktop Window Manager Information
  Disclosure Vulnerability    
      Important    
   5.5 
      No    
      Yes    
   Info 
  
  
        CVE-2023-31096 *   
      MITRE: CVE-2023-31096 Windows Agere Soft
  Modem Driver Elevation of Privilege Vulnerability    
      Important    
   7.8 
      Yes    
      No    
   EoP 
  
  
        CVE-2026-21265 †   
      Secure Boot Certificate Expiration Security
  Feature Bypass Vulnerability    
      Important    
   6.4 
      Yes    
      No    
   SFB 
  
  
        CVE-2024-55414 *   
      Windows Motorola Soft Modem Driver Elevation
  of Privilege Vulnerability    
      Important    
   7.8 
      Yes* 
      No    
   EoP 
  
  
        CVE-2026-20955      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Critical    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20957      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Critical    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20952      
      Microsoft Office Remote Code Execution
  Vulnerability    
      Critical    
   8.4 
      No    
      No    
   RCE 
  
  
        CVE-2026-20953      
      Microsoft Office Remote Code Execution
  Vulnerability    
      Critical    
   8.4 
      No    
      No    
   RCE 
  
  
        CVE-2026-20944      
      Microsoft Word Remote Code Execution
  Vulnerability    
      Critical    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20822      
      Windows Graphics Component Elevation of
  Privilege Vulnerability    
      Critical    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20854      
      Windows Local Security Authority Subsystem
  Service (LSASS) Remote Code Execution Vulnerability    
      Critical    
   7.5 
      No    
      No    
   RCE 
  
  
        CVE-2026-20876      
      Windows Virtualization-Based Security (VBS)
  Enclave Elevation of Privilege Vulnerability    
      Critical    
   6.7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21224      
      Azure Connected Machine Agent Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21226      
      Azure Core shared client library for Python
  Remote Code Execution Vulnerability    
      Important    
   7.5 
      No    
      No    
   RCE 
  
  
        CVE-2026-20815      
      Capability Access Management Service
  (camsvc) Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20830      
      Capability Access Management Service
  (camsvc) Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21221      
      Capability Access Management Service
  (camsvc) Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20835      
      Capability Access Management Service
  (camsvc) Information Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20851      
      Capability Access Management Service
  (camsvc) Information Disclosure Vulnerability    
      Important    
   6.2 
      No    
      No    
   Info 
  
  
        CVE-2026-20871      
      Desktop Windows Manager Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20814      
      DirectX Graphics Kernel Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20836      
      DirectX Graphics Kernel Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20962      
      Dynamic Root of Trust for Measurement (DRTM)
  Information Disclosure Vulnerability    
      Important    
   4.4 
      No    
      No    
   Info 
  
  
        CVE-2026-20941      
      Host Process for Windows Tasks Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21219      
      Inbox COM Objects (Global Memory) Remote
  Code Execution Vulnerability    
      Important    
   7 
      No    
      No    
   RCE 
  
  
        CVE-2026-20812      
      LDAP Tampering Vulnerability    
      Important    
   6.5 
      No    
      No    
   Tampering 
  
  
        CVE-2026-20842      
      Microsoft DWM Core Library Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20946      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20950      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20956      
      Microsoft Excel Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20949      
      Microsoft Excel Security Feature Bypass
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   SFB 
  
  
        CVE-2026-20943      
      Microsoft Office Click-To-Run Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20958      
      Microsoft SharePoint Information Disclosure
  Vulnerability    
      Important    
   5.4 
      No    
      No    
   Info 
  
  
        CVE-2026-20963      
      Microsoft SharePoint Remote Code Execution
  Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20947      
      Microsoft SharePoint Server Remote Code
  Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20951      
      Microsoft SharePoint Server Remote Code
  Execution Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20959      
      Microsoft SharePoint Server Spoofing
  Vulnerability    
      Important    
   4.6 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-20803 †   
      Microsoft SQL Server Elevation of Privilege
  Vulnerability    
      Important    
   7.2 
      No    
      No    
   EoP 
  
  
        CVE-2026-20847      
      Microsoft Windows File Explorer Spoofing
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-20948      
      Microsoft Word Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20872      
      NTLM Hash Disclosure Spoofing
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-20925      
      NTLM Hash Disclosure Spoofing
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-20821      
      Remote Procedure Call Information Disclosure
  Vulnerability    
      Important    
   6.2 
      No    
      No    
   Info 
  
  
        CVE-2026-20826      
      Tablet Windows User Interface (TWINUI)
  Subsystem Information Disclosure Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20827      
      Tablet Windows User Interface (TWINUI)
  Subsystem Information Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20829      
      TPM Trustlet Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20811      
      Win32k Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20863      
      Win32k Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20920      
      Win32k Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20965      
      Windows Admin Center Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20810      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20831      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20860      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20839      
      Windows Client-Side Caching (CSC) Service
  Information Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20844      
      Windows Clipboard Server Elevation of
  Privilege Vulnerability    
      Important    
   7.4 
      No    
      No    
   EoP 
  
  
        CVE-2026-20857      
      Windows Cloud Files Mini Filter Driver
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20940      
      Windows Cloud Files Mini Filter Driver
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20820      
      Windows Common Log File System Driver
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20864      
      Windows Connected Devices Platform Service
  Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-0386 †   
      Windows Deployment Services Remote Code
  Execution Vulnerability    
      Important    
   7.5 
      No    
      No    
   RCE 
  
  
        CVE-2026-20817      
      Windows Error Reporting Service Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20808      
      Windows File Explorer Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20823      
      Windows File Explorer Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20932      
      Windows File Explorer Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20937      
      Windows File Explorer Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20939      
      Windows File Explorer Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20804      
      Windows Hello Tampering Vulnerability    
      Important    
   7.7 
      No    
      No    
   Tampering 
  
  
        CVE-2026-20852      
      Windows Hello Tampering Vulnerability    
      Important    
   7.7 
      No    
      No    
   Tampering 
  
  
        CVE-2026-20929      
      Windows HTTP.sys Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20825      
      Windows Hyper-V Information Disclosure
  Vulnerability    
      Important    
   4.4 
      No    
      No    
   Info 
  
  
        CVE-2026-20816      
      Windows Installer Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20849      
      Windows Kerberos Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20833 †   
      Windows Kerberos Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20818      
      Windows Kernel Information Disclosure
  Vulnerability    
      Important    
   6.2 
      No    
      No    
   Info 
  
  
        CVE-2026-20838      
      Windows Kernel Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20809      
      Windows Kernel Memory Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20859      
      Windows Kernel-Mode Driver Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20875      
      Windows Local Security Authority Subsystem
  Service (LSASS) Denial of Service Vulnerability    
      Important    
   7.5 
      No    
      No    
   DoS 
  
  
        CVE-2026-20869      
      Windows Local Session Manager (LSM)
  Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-20858      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20861      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20865      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20866      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20867      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20873      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20874      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20877      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20918      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20923      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20924      
      Windows Management Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20862      
      Windows Management Services Information
  Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20837      
      Windows Media Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20936      
      Windows NDIS Information Disclosure
  Vulnerability    
      Important    
   4.3 
      No    
      No    
   Info 
  
  
        CVE-2026-20840      
      Windows NTFS Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20922      
      Windows NTFS Remote Code Execution
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20824      
      Windows Remote Assistance Security Feature
  Bypass Vulnerability    
      Important    
   5.5 
      No    
      No    
   SFB 
  
  
        CVE-2026-20832      
      Windows Remote Procedure Call Interface
  Definition Language (IDL) Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20828      
      Windows rndismp6.sys Information Disclosure
  Vulnerability    
      Important    
   4.6 
      No    
      No    
   Info 
  
  
        CVE-2026-20843      
      Windows Routing and Remote Access Service
  (RRAS) Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20868      
      Windows Routing and Remote Access Service
  (RRAS) Remote Code Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-20856      
      Windows Server Update Service (WSUS) Remote
  Code Execution Vulnerability    
      Important    
   8.1 
      No    
      No    
   RCE 
  
  
        CVE-2026-20927      
      Windows SMB Server Denial of Service
  Vulnerability    
      Important    
   5.3 
      No    
      No    
   DoS 
  
  
        CVE-2026-20848      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20919      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20921      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20926      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20934      
      Windows SMB Server Elevation of Privilege
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   EoP 
  
  
        CVE-2026-20834      
      Windows Spoofing Vulnerability    
      Important    
   4.6 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-20931      
      Windows Telephony Service Elevation of
  Privilege Vulnerability    
      Important    
   8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20938      
      Windows Virtualization-Based Security (VBS)
  Enclave Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20819      
      Windows Virtualization-Based Security (VBS)
  Information Disclosure Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-20935      
      Windows Virtualization-Based Security (VBS)
  Information Disclosure Vulnerability    
      Important    
   6.2 
      No    
      No    
   Info 
  
  
        CVE-2026-20853      
      Windows WalletService Elevation of Privilege
  Vulnerability    
      Important    
   7.4 
      No    
      No    
   EoP 
  
  
        CVE-2026-20870      
      Windows Win32 Kernel Subsystem Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-0628 *   
      Chromium: CVE-2026-0628 Insufficient policy
  enforcement in WebView tag    
      High 
   N/A 
      No    
      No    
   SFB 
  
 
  
    
    
    
    
    
    
    
  
 
 











  




    * Indicates this CVE had been released by a third party and is now being included in Microsoft releases .   † Indicates further administrative actions are required to fully address the vulnerability.    &nbsp;   Moving on to the other Critical-rated bugs in this month’s release, there are a couple of odd Excel vulns receiving patches. Initially, I though the Preview Pane would be involved, but it isn’t. In fact, it’s not clear what makes these Critical at all. That’s not true for the Word bug, where the Preview Pane  is  an attack vector. The bug in LSASS allows for code execution over a network, but you need to be authenticated. The final Critical bug is a privilege escalation involving GPU paravirtualization and could lead to local users executing code as SYSTEM. For some reason, I feel like we have just scratched the surface with GPU-related bugs.  Taking a look at the other code execution vulnerabilities in this month’s release, there’s the standard open-and-own bugs in Word and Excel. The SharePoint bugs require authentication, but almost every authenticated user will have the needed permissions. There is an interesting SharePoint bug reported by former ZDI analyst Piotr Bazydło. This one doesn’t require authentication but does require user interaction such as importing a malicious WSDL or opening a file. The bug in WSUS looks frightening, but it requires a machine-in-the-middle (MiTM) to exploit the issue. The two bugs in NTFS require authentication. The vuln in Azure Core requires an attacker to change a valid token to be malicious, which requires “developer-type authentication” – whatever that means.  The final code execution bug for January requires extra steps for remediation. Microsoft is removing the hands-free deployment feature of Windows Deployment Services. This means you will need to audit your enterprise to find systems configured with hands-free deployments. From there, you’ll need to opt if for protection in the immediate future. You’ll also need to have a plan to migrate these systems to something other than hands free prior to Microsoft removing the feature in mid-2026.  Elevation of Privilege (EoP) bugs make up the vast majority of this release, but most simply lead to local attackers executing their code at SYSTEM-level privileges or administrative privileges. There are also quite a few bugs that allow attackers to move from Low to Medium integrity to escape AppContainer isolation. These bugs are mostly in the Windows Management Services. There is one bug that leads to “Kernel Memory Access” – whatever that means. There’s another bug that leads to change VTL levels, but this one only gets you VTL1 access. The bug in the Windows Admin Center (WAC) is interesting as it could allow attackers to gain local admin privileges on targeted WAC-managed machines within a tenant. This gives the attacker the ability to interact with other tenant’s applications and content. The bug in WalletService only leads to the privileges of the compromised user. That’s the same for the File Explorer bug. The bug in SQL Server allows an attacker to gain debugging privileges, including the ability to dump memory. As always, SQL admins will need to take extra steps for full remediation of this issue. The final EoP is actually from 2024. Microsoft doesn’t list this as public, but I do. There have already been press articles describing this vulnerability. The bug is in the Motorola Soft Modem drivers, which ship be default on supported Windows OS systems. It’s a deprecated piece of gear, so rather than fix the driver, Microsoft is simply removing the driver completely.   There are a couple of additional security feature bypass bugs to discuss. The first is in Excel, and it could allow attackers to bypass macro protections. It also requires some user interaction, so it’s not just an open-and-own bug. The bug in Remote Assistance allows attacker to evade Mark of the Web (MotW) protections.  There are quite a few information disclosure bug receiving fixes this month. Many only result in info leaks consisting of unspecified memory contents or memory addresses, but there are multiple exceptions. The bug in CamSvc discloses the ever popular “sensitive information”. Another CamSvc bug discloses the memory of the Capability Access Manager service. There are a couple of bugs that allow someone in VTL0 to view VTL1 data – again, a first as far as I know. Windows File Explorer has a few bugs that could disclose an address outside of a sandbox. That would certainly be useful for sandbox escapes. The bug in Kerberos doesn’t sound all that exciting, but it requires additional steps after installing the patch. The bug in TPM allows attacker to disclose “secrets or privileged information belonging to the user of the affected application.” The vulnerability in the Dynamic Root of Trust for Measurement (DRTM) component discloses cryptographic secrets. The Hyper-V bug is fascinating as it allows attackers to disclose data from a Guest VM to Hyper-V host server, bypassing the virtualization security boundary. Finally, the SharePoint info disclosure is interesting as it allows the exposure of data returned from outbound requests SharePoint makes on the attacker’s behalf. It’s like the attacker can use an affected system to perform reconnaissance on their behalf.  The January release contains five fixes for spoofing bugs, although some of the descriptions about the bugs themselves are quite obtuse. We can say the bug in SharePoint is a cross-site scripting (XSS) bug. Two of the bugs simply state that they allow spoofing over a network. The bugs in NTLM Hash Disclosure are least list the fact that user interaction is required.   Speaking of unclear descriptions, there are three bugs with the ever-ineffable Tampering impact. Two are in Windows Hello and allow “an unauthorized attacker to perform tampering locally.” That likely means they can abuse the Hello component to bypass it, but that’s not clearly stated. Similarly, the LDAP bug just states it could allow tampering over a network.   Finally, there are two denial-of-service bugs in SMB and LSASS. However, Microsoft provides no real information about these bugs, just that an attacker could use them to deny service over a network. At least they note the SMB bug requires authentication.  No new advisories are being released this month.   Looking Ahead   Assuming I survive Pwn2Own automotive and haven’t transformed into a giant piece of sushi, I’ll be back for the February release on the 10th. Until then, stay safe, happy patching, and may all your reboots be smooth and clean!
