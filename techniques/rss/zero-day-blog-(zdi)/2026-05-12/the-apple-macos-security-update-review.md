---
source: rss/zero-day-blog-(zdi)
title: The Apple macOS Security Update Review
url: https://www.thezdi.com/blog/2026/5/12/the-apple-macos-security-update-review
date: 2026-05-12
item_id: https://www.thezdi.com/blog/2026/5/12/the-apple-macos-security-update-review
category: techniques
tags: [Bypass, CVE]
---

**Source:** Zero Day Blog (ZDI)
**Link:** https://www.thezdi.com/blog/2026/5/12/the-apple-macos-security-update-review

We’ve received some feedback from those who read the Patch Blog that they would like something similar for macOS updates. Unfortunately, Apple doesn’t schedule these for a particular day, but we can provide our thoughts and analysis on the days they do release their latest patches.   For May 2026, Apple released 82 unique CVEs across the three macOS versions: 79 for macOS Tahoe 26.5, 45 for macOS Sequoia 15.7.7, and 42 for macOS Sonoma 14.8.7. Since Apple doesn’t provide CVSS scores or other severity information, we’re left to speculate on which of these bugs is the most severe. However, there are a couple that stand out.  -&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-28819 (Wi-Fi)  stands out as the strongest candidate for the most severe as it states, “An app may be able to execute arbitrary code with kernel privileges.” The combination of arbitrary code execution at the kernel level is about as bad as it gets on a severity scale. Plus, it affects all three macOS versions (Tahoe, Sequoia, and Sonoma).  -&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-43668 (mDNSResponder)  also piques my interest since, “A remote attacker may be able to cause unexpected system termination or corrupt kernel memory.” The remote attack vector with kernel memory corruption on all three OS versions makes this a serious one, especially since mDNSResponder is always running.  -&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  CVE-2026-28972 (Kernel)  This one states that “An app may be able to cause unexpected system termination or write kernel memory.” An out-of-bounds write directly into kernel memory on all three OS versions. This one may also have implications in the upcoming Pwn2Own Berlin contest.  Here’s a look at all the bugs released by Apple this month: 





















  
  




  
    


  82Unique CVEs
   79macOS Tahoe 26.5 
   45macOS Sequoia 15.7.7 
   42macOS Sonoma 14.8.7 



 
 
   
   
   
   
   
   
 
 
   
     CVE ID 
     Component 
     Impact 
     macOS Tahoe 26.5 
     macOS Sequoia 15.7.7 
     macOS Sonoma 14.8.7 
   
 
 
   
      CVE-2026-28991  
     Accelerate 
     An app may be able to cause a denial-of-service 
     Yes 
     No 
     No 
   
   
      CVE-2026-28988  
     Accounts 
     An app may be able to bypass certain Privacy preferences 
     Yes 
     No 
     No 
   
   
      CVE-2026-28959  
     APFS 
     An app may be able to cause unexpected system termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28995  
     App Intents 
     A malicious app may be able to break out of its sandbox 
     Yes 
     No 
     No 
   
   
      CVE-2026-1837  
     AppleJPEG 
     Processing a maliciously crafted image may lead to a denial-of-service 
     Yes 
     No 
     No 
   
   
      CVE-2026-28956  
     AppleJPEG 
     Processing a maliciously crafted media file may lead to unexpected app termination or corrupt process memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-39869  
     Audio 
     Processing an audio stream in a maliciously crafted media file may terminate the process 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28922  
     CoreMedia 
     An app may be able to access private information 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28936  
     CoreServices 
     Processing a maliciously crafted file may lead to unexpected app termination 
     Yes 
     No 
     Yes 
   
   
       CVE-2026-28918  
     CoreSymbolication 
     Parsing a maliciously crafted file may lead to an unexpected app termination 
     Yes 
     No 
     No 
   
   
      CVE-2026-28878  
     Crash Reporter 
     An app may be able to enumerate a user's installed apps 
     No 
     Yes 
     No 
   
   
      CVE-2026-28915  
     CUPS 
     An app may be able to gain root privileges 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-43659  
     FileProvider 
     An app may be able to access sensitive user data 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28923  
     GPU Drivers 
     A malicious app may be able to break out of its sandbox 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28925  
     HFS 
     An app may be able to cause unexpected system termination or write kernel memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2025-43524  
     Icons 
     An app may be able to break out of its sandbox 
     No 
     Yes 
     Yes 
   
   
      CVE-2026-43661  
     ImageIO 
     Processing a maliciously crafted image may corrupt process memory 
     Yes 
     No 
     No 
   
   
      CVE-2026-28977  
     ImageIO 
     Processing a maliciously crafted file may lead to unexpected app termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28990  
     ImageIO 
     Processing a maliciously crafted image may corrupt process memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28978  
     Installer 
     A malicious app may be able to break out of its sandbox 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28992  
     IOHIDFamily 
     An attacker may be able to cause unexpected app termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28943  
     IOHIDFamily 
     An app may be able to determine kernel memory layout 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28969  
     IOKit 
     An app may be able to cause unexpected system termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-43655  
     IOSurfaceAccelerator 
     An app may be able to cause unexpected system termination or read kernel memory 
     Yes 
     No 
     No 
   
   
      CVE-2026-43654  
     Kernel 
     An app may be able to disclose kernel memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28908  
     Kernel 
     An app may be able to modify protected parts of the file system 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28954  
     Kernel 
     A maliciously crafted disk image may bypass Gatekeeper checks 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28897  
     Kernel 
     A local user may be able to cause unexpected system termination or read kernel memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28952  
     Kernel 
     An app may be able to cause unexpected system termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28951  
     Kernel 
     An app may be able to gain root privileges 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28972  
     Kernel 
     An app may be able to cause unexpected system termination or write kernel memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28986  
     Kernel 
     An app may be able to cause unexpected system termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28987  
     Kernel 
     An app may be able to leak sensitive kernel state 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28983  
     LaunchServices 
     A remote attacker may be able to cause a denial of service 
     Yes 
     No 
     No 
   
   
      CVE-2026-28929  
     Mail Drafts 
     Replying to an email could display remote images in Mail in Lockdown Mode 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-43653  
     mDNSResponder 
     An attacker on the local network may be able to cause a denial-of-service 
     Yes 
     No 
     Yes 
   
   
      CVE-2026-28985  
     mDNSResponder 
     An attacker on the local network may be able to cause a denial-of-service 
     Yes 
     No 
     No 
   
   
      CVE-2026-43668  
     mDNSResponder 
     A remote attacker may be able to cause unexpected system termination or corrupt kernel memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-43666  
     mDNSResponder 
     An attacker on the local network may be able to cause a denial-of-service 
     Yes 
     Yes 
     Yes 
   
   
       CVE-2026-28941  
     Model I/O 
     Processing a maliciously crafted file may lead to a denial-of-service or potentially disclose memory contents 
     Yes 
     Yes 
     No 
   
   
       CVE-2026-28940  
     Model I/O 
     Processing a maliciously crafted image may corrupt process memory 
     Yes 
     Yes 
     No 
   
   
      CVE-2026-28961  
     Network Extensions 
     An attacker with physical access to a locked device may be able to view sensitive user information 
     Yes 
     No 
     No 
   
   
      CVE-2026-28906  
     Networking 
     An attacker may be able to track users through their IP address 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28840  
     PackageKit 
     An app may be able to gain root privileges 
     No 
     Yes 
     Yes 
   
   
      CVE-2026-43656  
     Quick Look 
     Parsing a maliciously crafted file may lead to an unexpected app termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-43652  
     Sandbox 
     An app may be able to access protected user data 
     Yes 
     No 
     No 
   
   
      CVE-2026-39870  
     SceneKit 
     Processing a maliciously crafted image may corrupt process memory 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28846  
     SceneKit 
     A remote attacker may be able to cause unexpected app termination 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28993  
     Shortcuts 
     An app may be able to access user-sensitive data 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28848  
     SMB 
     A remote attacker may be able to cause unexpected system termination 
     Yes 
     Yes 
     No 
   
   
      CVE-2026-28930  
     Spotlight 
     An app may be able to access protected user data 
     Yes 
     No 
     No 
   
   
      CVE-2026-28974  
     Spotlight 
     An app may be able to cause a denial-of-service 
     Yes 
     Yes 
     No 
   
   
      CVE-2026-28996  
     Storage 
     An app may be able to access sensitive user data 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28919  
     StorageKit 
     An app may be able to gain root privileges 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28924  
     Sync Services 
     An app may be able to access Contacts without user consent 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-39871  
     TV App 
     An app may be able to observe unprotected user data 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28976  
     UserAccountUpdater 
     An app may be able to gain root privileges 
     Yes 
     No 
     No 
   
   
      CVE-2026-43660  
     WebKit 
     Processing maliciously crafted web content may prevent Content Security Policy from being enforced 
     Yes 
     No 
     No 
   
   
      CVE-2026-28907  
     WebKit 
     Processing maliciously crafted web content may prevent Content Security Policy from being enforced 
     Yes 
     No 
     No 
   
   
      CVE-2026-28962  
     WebKit 
     Processing maliciously crafted web content may disclose sensitive user information 
     Yes 
     No 
     No 
   
   
      CVE-2026-43658  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected Safari crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28905  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
       CVE-2026-28847  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28904  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
       CVE-2026-28955  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28903  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28953  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28902  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28901  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28913  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28883  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28958  
     WebKit 
     An app may be able to access sensitive user data 
     Yes 
     No 
     No 
   
   
      CVE-2026-28917  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28947  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected Safari crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28946  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected Safari crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28942  
     WebKit 
     Processing maliciously crafted web content may lead to an unexpected Safari crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28971  
     WebKit 
     A malicious iframe may use another website's download settings 
     Yes 
     No 
     No 
   
   
      CVE-2026-28944  
     WebRTC 
     Processing maliciously crafted web content may lead to an unexpected process crash 
     Yes 
     No 
     No 
   
   
      CVE-2026-28819  
     Wi-Fi 
     An app may be able to execute arbitrary code with kernel privileges 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28994  
     Wi-Fi 
     An attacker in a privileged network position may be able to perform denial-of-service attack using crafted Wi-Fi packets 
     Yes 
     Yes 
     Yes 
   
   
      CVE-2026-28914  
     zip 
     A maliciously crafted ZIP archive may bypass Gatekeeper checks 
     Yes 
     No 
     No 
   
   
      CVE-2026-28920  
     zlib 
     Visiting a maliciously crafted website may leak sensitive data 
     Yes 
     Yes 
     Yes 
   
 
 

  CVEs marked with the scarab logo were reported through the  TrendAI Zero Day Initiative  program. 


  




   We’ll continue these macOS updates if people find them useful. Stay tuned for the regularly schedule Patch Tuesday blog covering Adobe and Microsoft.
