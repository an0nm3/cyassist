---
source: rss/zero-day-blog-(zdi)
title: The February 2026 Security Update Review
url: https://www.thezdi.com/blog/2026/2/10/the-february-2026-security-update-review
date: 2026-02-10
item_id: https://www.thezdi.com/blog/2026/2/10/the-february-2026-security-update-review
category: techniques
tags: [Bypass, CVE, Exploit, Injection, Race condition, Rce, Xss]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/2/10/the-february-2026-security-update-review

I have survived the biggest Pwn2Own ever, but I’m back in Tokyo for the second Patch Tuesday of 2026. My location never stops Patch Tuesday from coming, so let’s take a look at the latest security patches from Adobe and Microsoft.  If you’d rather watch the full video recap covering the entire release, you can check it out here: 





















  
  

















  
    
      
    
    
      
        
      
    
    
  




    Adobe Patches for February 2026   For February, Adobe released nine bulletins addressing 44 unique CVEs in Adobe Audition, After Effects, InDesign, Substance 3D Designer, Substance 3D Stager, Adobe Bridge, Substance 3D Modeler, Lightroom Classic, and the Adobe DNG Software Development Kit (SDK). The largest update here is for  After Effects , which fixes 13 Critical and two Important rated bugs. The patch for  Substance 3D Designer  is on the larger side with seven fixes, but only two of those are Critical. On the other hand, the fix for  Substance 3D Stager  corrects five Critical-rated bugs that could lead to code execution. The  Audition  patch fixes six bugs, but only one is Critical.  The other patches are smaller in size. The fix for the  Adobe DNG Software Development Kit (SDK)  corrects two Critical and two Important-rated bugs. The  InDesign  patch fixes three bugs, but only one is Critical. The update for  Adobe Bridge  fixes two Critical bug that could lead to code execution. The patch for  Lightroom Classic  addresses a single Critical bug, and the release is wrapped up with a patch for  Substance 3D Modeler  that fixes a single, Important-rated memory link.  None of the bugs fixed by Adobe this month are listed as publicly known or under active attack at the time of release, and all of the updates released by Adobe this month are listed as deployment priority 3.   Microsoft Patches for February 2026   This month, Microsoft drops 58 new CVEs in Windows and Windows components, Office and Office Components, Azure, Microsoft Edge (Chromium-based), .NET and Visual Studio, GitHub Copilot, Mailslot FS, Exchange Server, Internet Explorer (!), Power BI, Hyper-V Server, and the Windows Subsystem for Linux. Counting the third-party and Chromium updates listed in the release, it brings the total number of CVEs to 62. One of the bugs in the Windows Graphics component was submitted through the ZDI program. Five of these bugs are rated Critical, two are rated Moderate, and the rest are rated Important in severity.  It’s typical to see this number of CVEs released in February, but the number of bugs under active attack is extraordinarily high. Microsoft lists six bugs being exploited at the time of release, with three of these listed as publicly known. Last month only had a single bug being exploited, although there were twice as many CVEs patched. We’ll see if we’re on our way to another “hot exploit summer” as we saw a few years ago or if this is just an aberration.   Let’s take a closer look at some of the more interesting updates for this month, starting with the bugs under active attack:   -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-21510    - Windows Shell Security Feature Bypass Vulnerability  This bug is listed as a security feature bypass, but it could also be classified as code execution. An attacker can bypass Windows SmartScreen and Windows Shell security prompts to execute code on a target system. This bug is also listed as publicly known, but Microsoft doesn’t say where. There is user interaction here, as the client needs to click a link or a shortcut file. Still, a one-click bug to gain code execution is a rarity. Definitely test and deploy this fix quickly.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-21514    - Microsoft Word Security Feature Bypass Vulnerability  This bug also requires user interaction in the form of opening a Word document, but that’s all that’s required to bypass protections to dangerous COM/OLE controls. Thankfully, the Preview Pane is  not  an attack vector here. However, users are well known to open lots of documents they receive in e-mail. This bypass could also result in code execution if the right COM/OLE control is hit. This is also listed as publicly known, so add this to the list to test and deploy quickly.  -&nbsp;&nbsp;&nbsp;   CVE-2026-21519    - Desktop Window Manager Elevation of Privilege Vulnerability  This is the second month in a row that a DWM was listed as being exploited in the wild. That leads me to believe the first patch didn’t completely resolve the vulnerability. Same as last month, this bug allows attackers to run code with SYSTEM privileges. Bugs of this type are typically paired with a code execution bug to take over a system. As always, Microsoft offers no indication of how widespread these exploits may be.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-21533    - Windows Remote Desktop Services Elevation of Privilege Vulnerability  Don’t let the word “Remote” in the title fool you – this is a local bug that allows attackers to run code with SYSTEM privileges. It’s interesting that Microsoft lists “Improper privilege management” as the root cause for this issue. If the system is running Remote Desktop Services, it’s probably a juicy target for attackers to move laterally after an initial breach. Add this one to the list of patches to test and deploy immediately.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-21513    - Internet Explorer Security Feature Bypass Vulnerability  Although long gone by many measurements, IE does still exist on Windows systems, and calling it always results in a vulnerability somehow. This bug manifests similarly to the Shell bug above, as it requires user interaction but could result in code execution. The bypass here is simply the ability to reach IE, which shouldn’t be possible. Again, test and deploy this fix quickly.  -&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-21525    - Windows Remote Access Connection Manager Denial of Service Vulnerability  It’s unusual to see DoS bugs being used in active attacks, but that’s what we have here. A null pointer deref in the Windows Remote Access Connection Manager allows an unauthorized attacker to deny service locally. Most null pointer derefs cause the application or service to crash, but it’s not clear if it will automatically restart. I would exercise caution and patch quickly either way.  Here’s the full list of CVEs released by Microsoft for February 2026: 





















  
  




  
    



















 
  
  
  
  
  
      CVE    
      Title    
      Severity    
      CVSS    
      Public 
      Exploited    
      TYPE    
  
  
        CVE-2026-21514      
      Microsoft Word Security Feature Bypass
  Vulnerability    
      Important    
   7.8 
      Yes    
      Yes    
   SFB 
  
  
        CVE-2026-21510      
      Windows Shell Security Feature Bypass
  Vulnerability    
      Important    
   8.8 
      Yes    
      Yes    
   SFB 
  
  
        CVE-2026-21513      
      Internet Explorer Security Feature Bypass
  Vulnerability    
      Important    
   8.8 
      Yes    
      Yes    
   SFB 
  
  
        CVE-2026-21519      
      Desktop Window Manager Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      Yes    
   EoP 
  
  
        CVE-2026-21533      
      Windows Remote Desktop Services Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      Yes    
   EoP 
  
  
        CVE-2026-21525      
      Windows Remote Access Connection Manager
  Denial of Service Vulnerability    
      Moderate    
   6.2 
      No    
      Yes    
   DoS 
  
  
        CVE-2026-21511      
      Microsoft Outlook Spoofing
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2023-2804 *   
      Red Hat, Inc. CVE-2023-2804: Heap Based
  Overflow libjpeg-turbo    
      Important    
   6.5 
      Yes    
      No    
   RCE 
  
  
        CVE-2026-24302      
      Azure Arc Elevation of Privilege
  Vulnerability    
      Critical    
   8.6 
      No    
      No    
   EoP 
  
  
        CVE-2026-24300      
      Azure Front Door Elevation of Privilege
  Vulnerability    
      Critical    
   9.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21532      
      Azure Function Information Disclosure
  Vulnerability    
      Critical    
   8.2 
      No    
      No    
   Info 
  
  
        CVE-2026-21522      
      Microsoft ACI Confidential Containers
  Elevation of Privilege Vulnerability    
      Critical    
   6.7 
      No    
      No    
   EoP 
  
  
        CVE-2026-23655      
      Microsoft ACI Confidential Containers
  Information Disclosure Vulnerability    
      Critical    
   6.5 
      No    
      No    
   Info 
  
  
        CVE-2026-21218      
      .NET and Visual Studio Spoofing
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-21512      
      Azure DevOps Server Cross-Site Scripting
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   XSS 
  
  
        CVE-2026-21529 †   
      Azure HDInsight Spoofing Vulnerability    
      Important    
   5.7 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-21528      
      Azure IoT Explorer Information Disclosure
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   Info 
  
  
        CVE-2026-21228      
      Azure Local Remote Code Execution
  Vulnerability    
      Important    
   8.1 
      No    
      No    
   RCE 
  
  
        CVE-2026-21531      
      Azure SDK for Python Remote Code Execution
  Vulnerability    
      Important    
   9.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21251      
      Cluster Client Failover (CCF) Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-20846      
      GDI+ Denial of Service Vulnerability    
      Important    
   7.5 
      No    
      No    
   DoS 
  
  
        CVE-2026-21523      
      GitHub Copilot and Visual Studio Code Remote
  Code Execution Vulnerability    
      Important    
   8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21518      
      GitHub Copilot and Visual Studio Code
  Security Feature Bypass Vulnerability    
      Important    
   6.5 
      No    
      No    
   SFB 
  
  
        CVE-2026-21257      
      GitHub Copilot and Visual Studio Elevation
  of Privilege Vulnerability    
      Important    
   8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21256      
      GitHub Copilot and Visual Studio Remote Code
  Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21516      
      GitHub Copilot for Jetbrains Remote Code
  Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21253      
      Mailslot File System Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21537 †   
      Microsoft Defender for Endpoint Linux
  Extension Remote Code Execution Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21259      
      Microsoft Excel Elevation of Privilege
  Vulnerability    
      Important    
   7.3 
      No    
      No    
   EoP 
  
  
        CVE-2026-21258      
      Microsoft Excel Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-21261      
      Microsoft Excel Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-21527      
      Microsoft Exchange Server Spoofing
  Vulnerability    
      Important    
   6.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-21260      
      Microsoft Outlook Spoofing
  Vulnerability    
      Important    
   7.5 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-21229      
      Power BI Remote Code Execution
  Vulnerability    
      Important    
   8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21236      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21238      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21241      
      Windows Ancillary Function Driver for
  WinSock Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21517      
      Windows App for Mac Installer Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21234      
      Windows Connected Devices Platform Service
  Elevation of Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21235      
      Windows Graphics Component Elevation of
  Privilege Vulnerability    
      Important    
   7.3 
      No    
      No    
   EoP 
  
  
        CVE-2026-21246      
      Windows Graphics Component Elevation of
  Privilege Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21232      
      Windows HTTP.sys Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21240      
      Windows HTTP.sys Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21250      
      Windows HTTP.sys Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21244      
      Windows Hyper-V Remote Code Execution
  Vulnerability    
      Important    
   7.3 
      No    
      No    
   RCE 
  
  
        CVE-2026-21247      
      Windows Hyper-V Remote Code Execution
  Vulnerability    
      Important    
   7.3 
      No    
      No    
   RCE 
  
  
        CVE-2026-21248      
      Windows Hyper-V Remote Code Execution
  Vulnerability    
      Important    
   7.3 
      No    
      No    
   RCE 
  
  
        CVE-2026-21255      
      Windows Hyper-V Security Feature Bypass
  Vulnerability    
      Important    
   8.8 
      No    
      No    
   SFB 
  
  
        CVE-2026-21231      
      Windows Kernel Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21239      
      Windows Kernel Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21245      
      Windows Kernel Elevation of Privilege
  Vulnerability    
      Important    
   7.8 
      No    
      No    
   EoP 
  
  
        CVE-2026-21222      
      Windows Kernel Information Disclosure
  Vulnerability    
      Important    
   5.5 
      No    
      No    
   Info 
  
  
        CVE-2026-21243      
      Windows Lightweight Directory Access
  Protocol (LDAP) Denial of Service Vulnerability    
      Important    
   7.5 
      No    
      No    
   DoS 
  
  
        CVE-2026-20841      
      Windows Notepad App Remote Code Execution
  Vulnerability    
      Important    
   8.8 
      No    
      No    
   RCE 
  
  
        CVE-2026-21249      
      Windows NTLM Spoofing Vulnerability    
      Important    
   3.3 
      No    
      No    
   Spoofing 
  
  
        CVE-2026-21508      
      Windows Storage Elevation of Privilege
  Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21237      
      Windows Subsystem for Linux Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-21242      
      Windows Subsystem for Linux Elevation of
  Privilege Vulnerability    
      Important    
   7 
      No    
      No    
   EoP 
  
  
        CVE-2026-1861 *   
      Chromium: CVE-2026-1861 Heap buffer overflow
  in libvpx    
      High 
   N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-1862 *   
      Chromium: CVE-2026-1862 Type Confusion in
  V8    
      High 
   N/A 
      No    
      No    
   RCE 
  
  
        CVE-2026-0391      
      Microsoft Edge (Chromium-based) for Android
  Spoofing Vulnerability    
      Moderate    
   6.5 
      No    
      No    
   Spoofing 
  
 
  
    
    
    
    
    
    
    
  
 
 











  




    * Indicates this CVE had been released by a third party and is now being included in Microsoft releases .   † Indicates further administrative actions are required to fully address the vulnerability.    &nbsp;   Moving on to the Critical-rated bugs, the patch for Azure Front Door sounds frightening, but Microsoft has already fixed the bug and is just now documenting it. That’s also true for the bugs in Azure Arc and Azure Function. There are two Critical-rated bugs in the ACI Confidential Containers. The first allows a container escape while the second discloses secret tokens and keys. Either way, you’ll want to handle those quickly.  Taking a look at the other code execution vulnerabilities in this month’s release, we start with a frightening looking bug in Azure SDK for Python that has the highest CVSS this month of 9.8. A remote, unauthenticated attacker code gain code execution on an affected system via a maliciously crafted continuation token. It’s not clear why this isn’t rated Critical, but I would treat it as such. The three bugs in Hyper-V are actually local open-and-own bugs that require a user to open a malicious file on an affected system. That’s also true for the bug in Notepad. The bug in Power BI is confusing, because Microsoft says it requires authentication and could lead to an attacker running code as an authenticated user. There’s the poorly named “Azure Local Remote Code Execution Vulnerability”, but it requires a machine-in-the-middle (MitM) to exploit. The bug in Defender for Endpoint Linux is restricted to local subnets, but you’ll need to enable auto provisioning to get the patch. The final code execution bugs addressed this month are in GitHub Copilot. Two are command injections and the other is a Time-of-check time-of-use (toctou) race condition, but both could end up in code execution on affected systems.  Patches for Elevation of Privilege (EoP) bugs make up nearly 50% of this release, but most simply lead to local attackers executing their code at SYSTEM-level privileges or administrative privileges. There are only two of note. The first is a command injection bug in GitHub Copilot that leads to executing code at the level of the targeted application. The second is a bug in a kernel that leads to SYSTEM but could also be used for a sandbox escape.  There’s a unusually high number of spoofing bugs in this month’s release, and the ones for Outlook are the most troubling. First, the Preview Pane is an attack vector. Secondly, the bugs could be used to relay NTLM credentials via just an email, which could result in credential disclosure. And you’ll need multiple patches to fully address these bugs. At least they can be applied in any order. &nbsp;There’s a UI misrepresentation bug in Exchange Server that could allow an attacker to either view some sensitive information or “make changes to disclosed information”. At what point does data become disclosed? That odd phrasing makes me think they are using AI to right some of their descriptions. The phrasing also appears in the patch for NTLM. That bug is triggered by opening a specially crafted Office doc, and while they explicitly say it could be used to relay NTLM creds, it sure seems that way. The patch for .NET and Visual Studio fixes a bug that allows attackers to bypass header validation, resulting in the service accepting a message it should reject. Finally, the bug in Azure HDInsight is really just a cross-site scripting (XSS) bug. The caveat here is that you need to restart Ambari server in both of the head nodes to have this fix updated. There is also an XSS in Azure Devops Server, but at least it is labelled as such.  There are a couple of additional security feature bypass bugs to discuss. The first is in Hyper-V and bypasses the Virtualization-based Security feature. The other is in GitHub Copilot and Visual Studio Code. It’s another command injection, but this one can be used to bypass authentication. Neat.  Looking at the remaining info disclosure bugs getting patched this month, most simply result in info leaks consisting of unspecified memory contents or memory addresses. The exception is the bug in Azure IoT Explorer. This bug could be used to view the contents of the target user’s local file system.  We end this month’s release with two DoS bugs: one in LDAP and one in GDI+. Neither descriptions from Microsoft provide any usable information.  No new advisories are being released this month.   Looking Ahead   I plan on being back home for the March release but wherever I’m at, you can rest assured that March 10, I’ll be here to provide my assessment of the release. Until then, stay safe, happy patching, and may all your reboots be smooth and clean!
