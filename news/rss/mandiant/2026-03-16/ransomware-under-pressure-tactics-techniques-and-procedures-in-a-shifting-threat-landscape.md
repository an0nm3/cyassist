---
source: rss/mandiant
title: Ransomware Under Pressure: Tactics, Techniques, and Procedures in a Shifting Threat Landscape
url: https://cloud.google.com/blog/topics/threat-intelligence/ransomware-ttps-shifting-threat-landscape/
date: 2026-03-16
item_id: https://cloud.google.com/blog/topics/threat-intelligence/ransomware-ttps-shifting-threat-landscape/
category: news
tags: [Bypass, CVE, Exploit]
---

**Source:** Mandiant
**Link:** https://cloud.google.com/blog/topics/threat-intelligence/ransomware-ttps-shifting-threat-landscape/

Written by: Bavi Sadayappan, Zach Riddle, Ioana Teaca, Kimberly Goody, Genevieve Stark 
  
   Introduction     
  Since 2018, when many financially motivated threat actors began shifting their monetization strategy to post-compromise ransomware deployments, ransomware has become one of the most pervasive threats to organizations across almost every industry vertical and region. In recent years ransomware operations have evolved, creating a robust ecosystem that has lowered the barrier to entry via the commoditization and specialization of the supporting underground communities, which is exemplified by the proliferation of the ransomware-as-a-service (RaaS) business model. While ransomware remains a dominant threat due to the volume of activity and the potential for serious operational disruptions, we have observed multiple indicators that suggest the overall profitability of ransomware operations is in decline. This trend is likely the result of multiple factors, including improved cybersecurity practices, increased ability of organizations to recover, and declining ransom payment amounts and rates. Further, numerous disruptions have impacted the ransomware ecosystem in recent years, from external forces like law enforcement operations to internal conflict between actors; both have led to the disappearance or significant debilitation of previously prolific RaaS groups like LockBit, ALPHV, Basta, and RansomHub. However, despite these shakeups, the well-established Qilin and Akira RaaS brands rose up to fill the vacuum, leading to a record high number of victims posted to data leak sites (DLS) in 2025 (Figure 1).  
  This report provides an overview of the ransomware landscape and common tactics, techniques, and procedures (TTPs) directly observed in the 2025 ransomware incidents that Mandiant Consulting responded to. In this analysis, we excluded activity focused only on data theft extortion. Key insights include:   
 
 
  In a third of incidents, the initial access vector was confirmed or suspected exploitation of vulnerabilities, most often in common VPNs and firewalls.   
 
 
  77 percent of analyzed ransomware intrusions included suspected data theft, a notable uptick from 57 percent of incidents in 2024.  
 
 
  In approximately 43% of ransomware intrusions we responded to in 2025, the threat actors were observed targeting virtualization infrastructure, an increase from 29% in 2024.  
 
 
  REDBIKE was the most frequently deployed ransomware family, accounting for 30 percent of analyzed ransomware incidents.  
 
 
  Several trends from prior years remained consistent, including a decreased use of certain intrusion tools like BEACON and MIMIKATZ and a plateau in the reliance of remote management tools.  
 
 
  Google Threat Intelligence Group (GTIG) analysis of TTPs relies primarily on data from Mandiant engagements and therefore represents only a sample of global ransomware intrusion activity. These incidents involved the post-compromise deployment of ransomware following network intrusion activity, with the majority of incidents also involving data theft extortion. The impacted organizations were based across the Asia Pacific region, Europe, North America, and South America and within nearly every industry sector.   
  While we anticipate ransomware will remain one of the most impactful cyber threats in 2026, the reduction in profits may cause some threat actors to leverage other monetization methods and tactics, such as continuing targeting shifts, further increasing data theft extortion operations, the use of more aggressive extortion tactics, or opportunistically using access to victim environments for secondary monetization mechanisms.   
  Recommendations to assist in addressing the threat posed by ransomware are captured in our white paper,    Ransomware Protection and Containment Strategies: Practical Guidance for Endpoint Protection, Hardening, and Containment  .  
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 1: Top 10 DLS in 2025 and associated ransomware families  
      
     

  
       
     
  




 
   2025 Ransomware Landscape   
  In 2025, the ransomware landscape became increasingly crowded, with a record high number of unique DLS with at least one post. The growing pool of ransomware actors engaging in extortion operations combined with persistent targeted efforts by law enforcement and enhanced organizational security has likely shrunk profit margins for ransomware operators in recent years. In response, threat actors appear to be adopting new strategies from who they target to the technologies they use. This evolution has included an apparent increase in targeting smaller organizations, and a possible focus on data theft extortion without ransomware deployment. Furthermore, threat actors are incorporating artificial intelligence (AI) into aspects of their operations (e.g., negotiations) and leveraging Web3 technologies to bolster the resilience of their infrastructure. While we see expansions in these aspects, internal and external disruptions seen in recent years have prompted some threat actors to become more cautious resulting in more rigorous vetting of potential partners. We expect ransomware actors to continue to adjust and evolve their tactics in an attempt to maintain some level of success or regain the levels of profitability they reached historically.  
  2025 marked a record year for the number of posts on DLS, with the total number of posts surpassing that of 2024 by almost 50%. Despite these record setting numbers, we caution against relying solely on DLS data to ascertain the overall volume of ransomware activity. Threat actors typically only create DLS posts for victims that have refused to initiate or complete extortion negotiations. Public reporting    indicates    that ransom payment rates have been declining, which could, at least partially, fuel the steady increase of posts on shaming sites. It can also be difficult to differentiate between DLS posts associated with data theft-only operations and those that also include ransomware deployment. For example, threat actors associated with the CL0P DLS continue to occasionally deploy ransomware but have shifted primarily to data-theft-extortion-only operations. So while CL0P was the third most prolific DLS in 2025, the vast majority of incidents associated with these posts did not involve ransomware. We have also observed numerous instances of threat actors, such as those associated with BABUK 2.0, fabricating and exaggerating claims as well as reposting claims that would at least slightly inflate victim counts. Finally, not all claims are of equal significance. For example, between December 2024 and January 2025, FUNKSEC was the highest volume DLS; however, many of the associated incidents appeared to be lower impact events involving compromising websites for data theft extortion.   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 2: Volume of posts and unique data leak sites from 2020 through 2025  
      
     

  
       
     
  




 
   Although ransomware has historically been highly lucrative, recent disruptions and enhanced organizational security may be impacting these profits. Public reporting indicates that both ransom payment rates and average ransom demands are decreasing. In February 2026, Coveware    reported    that ransom payment rates have generally decreased over the past few years, reaching a historic low in Q4 2025. Similarly, in June 2025, Sophos    reported    that the average ransom demand has dropped by one-third during the last year, to $1.34 million in 2025 from $2 million in 2024. Public reporting further suggests that organizations that have been impacted by ransomware are able to recover more easily, which also likely contributes to reduced ransom payments. For example, in February 2025, Unit 42    reported    that companies have improved their ability to recover from ransomware incidents; nearly half of ransomware victims were able to restore from backup in 2024 compared to around 28% in 2023 and only 11% in 2022.  
  Improvements in organizational security and the growing ability of victims to recover from ransomware attacks may be leading some adversaries to view data theft as a more reliable method for securing payments. In intrusions investigated by Mandiant, we observed a decline in traditional ransomware deployment coinciding with a rise in data theft extortion. Further, some RaaS programs are providing data-theft-extortion-only options in addition to ransomware, which may reflect demand from their customer base. It is also plausible that more robust security posture, particularly at larger organizations, is forcing threat actors to adjust their targeting to focus on a higher volume of attacks targeting smaller organizations with less mature security programs. Analysis of organization size (based on estimated number of employees, when available) of victims posted on DLS indicates threat actors have shifted away from larger organizations and toward smaller organizations (Figure 3). Threat actors have directly commented on this trend. For example, in leaked April and May 2024 chats, a Basta actor theorized that targeting smaller company networks would be more effective compared to "normal networks."   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 3: Percentage of DLS posts for victims with an estimated company size of less than 200 employees  
      
     

  
       
     
  




 
   During 2025, numerous disruptive events impacted the ransomware ecosystem, including both a range of law enforcement and government actions as well as threat actor-related data leaks and disputes, at least some of which appear to be the result of turmoil amongst threat actors (Figure 4). Not only did many of these events result in direct disruption such as arrests, seizures, and sanctions, but some also forced threat actors to shift TTPs and provided valuable insights to security researchers on the inner workings and individuals behind some ransomware operations. Yet the dominance of long-standing Qilin and Akira brands in 2025 demonstrate the resilience of ransomware actors and their ability to fill voids following takedowns and exit scams of competing RaaS operators. There are some indications that the overall instability in the ransomware threat landscape, coupled with pressure from law enforcement, have caused ransomware teams to increase their operational security, which has translated into more rigorous vetting of potential affiliates. We've also seen some private or semi-private offerings gain prominence. For example, 2025 marked the first time in four years that one of the top two most prolific RaaS operations was not public; while Akira appears to have affiliates, they do not have a public advertisement for their operations.   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 4: Key disruptive events impacting the ransomware landscape  
      
     

  
       
     
  




 
   In 2025, ransomware actors continued to evolve their operations by adopting emerging or established technologies to increase the efficiency and efficacy of their operations. Some threat actors are integrating Web3 technologies into their operations, likely as a way to make their infrastructure more resilient to takedown and detection efforts. The Cry0 RaaS claims to leverage Internet Computer Protocol (ICP) blockchain to host negotiation sites via decentralized canister smart contracts, enabling clearnet access without requiring TOR while DEADLOCK ransomware has leveraged Polygon smart contracts in order to store and rotate C2 infrastructure. We have also seen threat actors incorporating AI-features into their RaaS offerings: the GLOBAL RaaS reportedly has an AI-assisted chat that provides victim analysis and assists with communications, CHAOS purportedly includes a "built-in AI chatbot," although its specific use is unclear, while BERT allegedly uses AI-based data analysis to identify victim pressure points. Finally, we have observed twice the number of ransomware families that were capable of running on both Windows and Linux systems compared to 2024. This could suggest that threat actors are shifting toward cross-platform ransomware rather than creating multiple, separate variants to support their operations.  
  Commonly Observed Tactics, Techniques, and Procedures  
  The following sections discuss trends in the TTPs observed in post-compromise ransomware deployment incidents, organized into the corresponding stages of GTIG's attack lifecycle model (Figure 5). The TTPs outlined in this section were observed at Mandiant-led ransomware investigations during 2025.   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 5: Attack lifecycle associated with 2025 ransomware incidents  
      
     

  
       
     
  




 
   Initial Access  
  During 2025, the most commonly identified initial access vector in ransomware incidents was the exploitation or suspected exploitation of vulnerabilities, accounting for a third of incidents, followed by web compromise, stolen credentials, and bruteforce attacks (Figure 6). Notably, while voice phishing was a commonly leveraged tactic in several high profile data theft extortion campaigns, it was not observed in ransomware incidents. This year we included suspected initial access vectors in our analysis to provide a more holistic view, given that some vectors can be more difficult to verify. For example, it can be difficult to confirm the use of stolen credentials, given that the credentials may have been harvested in a separate incident that occurred weeks prior or even on a personal device. Conversely, bruteforce attacks tend to generate many log entries that can be used to confirm the vector.  
 
 
  Throughout 2025 we observed ransomware operators leveraging a wide range of exploits for initial access (Table 1). While the majority of observed or suspected exploitation activity involved vulnerabilities disclosed prior to 2025, we observed multiple indicators that at least some ransomware actors were leveraging    zero-day exploits    in their operations.  
 
 
 
  In the majority of instances where exploits were used or suspected, the threat actors targeted vulnerabilities in common VPNs and firewalls such as Fortinet (CVE-2024-55591, CVE-2024-21762, and CVE-2019-6693), SonicWall (CVE-2024-40766), Palo Alto (CVE-2024-3400), and Citrix (CVE-2023-4966).  
 
 
  We also observed malicious actors successfully exploit a variety of other exposed services, including Veritas Backup Exec, Zoho ManageEngine, Microsoft Sharepoint, and SAP Netweaver.  
 
 
  We observed evidence that multiple ransomware and/or data theft extortion operations leveraged zero-day vulnerabilities for initial access throughout the year.  
 
 
 
  During mid-July 2025, an UNC6357 actor attempted to exploit Microsoft Sharepoint vulnerabilities CVE-2025-53770 and CVE-2025-53771 to gain access to the victim's environment and ultimately deploy LOCKBIT.WARLOCK. While this was observed after disclosure of the vulnerability, we observed evidence—including log data and public    reporting   —suggesting the same actor attempted to exploit the same vulnerability as a zero-day.  
 
 
  In August 2025, GTIG assessed with high confidence that UNC2165 leveraged a zero-day exploit for CVE-2025-8088 to deploy MYTHICAGENT.  
 
 
  While the observed incidents did not involve ransomware deployment, threat actors associated with the CL0P DLS may have    exploited    CVE-2025-61882 as a zero-day against Oracle EBS environments. The CL0P DLS has been associated with multifaceted extortion operations involving CLOP ransomware; however, it is primarily associated with data theft extortion operations rather than ransomware deployment.  
 
 
 
 
  We observed multiple threat clusters leverage malvertising and/or search engine optimization (SEO) tactics to distribute malware payloads for initial access, including both ransomware operators themselves and initial access partners that ultimately led to follow-on ransomware intrusions.   
 
 
 
  We observed multiple UNC6016 malware distribution operations leverage malvertising to distribute malware payloads masquerading as legitimate software tools such as PuTTY to gain initial access. At least a portion of observed UNC6016 access operations ultimately lead to NITROGEN or RHYSIDA ransomware deployments.  
 
 
  UNC2465 routinely leveraged malvertising and/or SEO techniques to distribute SMOKEDHAM payloads masquerading as RVTOOLs installers.  
 
 
 
  While less frequent this year, many threat actors continued to rely on stolen credentials for initial access. In 21% of intrusions where the initial access vector was identified, the threat actor leveraged compromised legitimate credentials to access the victim environment, typically involving authentication to a victim's VPN or a Remote Desktop Protocol (RDP) login. While the source of stolen credentials cannot always be determined, actors can obtain them via numerous techniques including purchasing credentials from underground forums or using credentials exposed in infostealer logs.  
 
 
  We continued to see a subset of actors leveraging bruteforce attacks against victims' VPNs. In one incident involving ransomware that identified itself as Daixin, the threat actor conducted periodic bruteforce attacks against various VPN user accounts over the course of nearly a year before successfully gaining initial access.  
 
 
  We observed multiple intrusions where the ransomware operator gained access to the victim through an intermediary network.   
 
 
 
  We observed multiple disparate ransomware operations that leveraged network access to subsidiaries of victims to subsequently access the victim's network. In one instance the threat actor leveraged access to the subsidiary to bruteforce access to the victim's VPN.  
 
 
  In a separate incident, the threat actor leveraged a VPN connection owned by a third-party vendor to access an operational technology (OT) system within the victim's environment.  
 
 
 
  During one intrusion leading to CLOP ransomware deployment, UNC5833 gained access from an initial access partner who impersonated a helpdesk user to social engineer an employee via a Microsoft Teams chat session to install Quick Assist. While we observed limited use of social engineering by ransomware operators during 2025 in incidents we observed, it remained a popular technique among financially motivated intrusion actors more broadly.  
 
  
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 6: Initial intrusion vectors  
      
     

  
       
     
  




 
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
       
 
 
 
   Vendor   
 
 
   Product   
 
 
   CVE   
 
 
 
 
  Fortinet  
 
 
  FortiOS / FortiProxy  
 
 
  CVE-2024-21762  
 
 
 
 
  Veritas  
 
 
  Backup Exec  
 
 
  CVE-2021-27877  
 
 
 
 
  Veritas  
 
 
  Backup Exec  
 
 
  CVE-2021-27878  
 
 
 
 
  Zoho  
 
 
  ManageEngine ADSelfService Plus  
 
 
  CVE-2021-40539  
 
 
 
 
  Fortinet  
 
 
  FortiOS / FortiProxy  
 
 
  CVE-2024-55591  
 
 
 
 
  Fortinet  
 
 
  FortiOS  
 
 
  CVE-2019-6693  
 
 
 
 
  SonicWall  
 
 
  SonicOS  
 
 
  CVE-2024-40766  
 
 
 
 
  Citrix  
 
 
  NetScaler  
 
 
  CVE-2023-4966  
 
 
 
 
  Microsoft  
 
 
  SharePoint  
 
 
  CVE-2025-53771  
 
 
 
 
  Microsoft  
 
 
  SharePoint  
 
 
  CVE-2025-53770  
 
 
 
 
  SAP  
 
 
  Netweaver  
 
 
  CVE-2025-31324  
 
 
 
 
  Palo Alto  
 
 
  PAN-OS GlobalProtect  
 
 
  CVE-2024-3400  
 
 
 
 
  CrushFTP  
 
 
  CrushFTP  
 
 
  CVE-2025-31161  
 
 
 
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Table 1:  Vulnerabilities likely leveraged for initial access in 2025 ransomware incidents    
   Establish Foothold and Maintain Presence  
  Once inside victim environments, threat actors engaged in many different techniques to establish a foothold and maintain presence, including leveraging valid credentials, tunnelers, backdoors, or legitimate remote access tools. Threat actors continued to use remote management tools to support both these phases of the attack lifecycle, albeit at slightly lower rates than 2024.  
 
 
  Ransomware actors consistently relied on compromised credentials to establish a foothold in victim environments.   
 
 
 
  Once authenticated to network services, they also often used these credentials to provision or modify highly privileged accounts to maintain access. For example, in a RIFTTEAR incident, the threat actor authenticated via Kerberos to a privileged system, provisioned an AD domain user, and added the account to a high-privileged group. We also saw multiple threat actors change passwords to root accounts on ESXi hosts.  
 
 
 
  In 2025, an increased number of threat actors adopted tunnelers to support these phases compared to 2024 observations. Observed tunnelers included publicly available offerings such as PYSOXY, CHISEL, CLOUDFLARED, RPIVOT, and REVSOCKS.CLIENT alongside seemingly private tunnelers like LIONSHARE, VIPERTUNNEL, and BLUNDERBLIGHT.  
 
 
 
  In a LOCKBIT.WARLOCK incident, the exploitation of a Microsoft SharePoint vulnerability enabled remote code execution, granting the access required to install CLOUDFLARED from Github via the Windows msiexec command-line utility, establishing an outbound-only C2 channel.  
 
 
 
  A subset of threat actors deployed backdoors—including CORNFLAKE.V3.JAVASCRIPT, SQUIDGATE, FIREHAWK, HAVOCDEMON, and SMOKEDHAM—to establish a foothold.  
 
 
 
  UNC6021, a suspected FIN6 threat cluster, used SQUIDGATE's built-in functionality to deploy FIREHAWK, a toehold backdoor written in C. Consistent with FIN6 infections, a social engineering engagement on LinkedIn prompted a user to access a malicious website hosting a ZIP archive containing the BULLZLINK downloader. Once executed, it retrieved a dropper variant of SQUIDSLEEP with an embedded SQUIDGATE payload.  
 
 
 
  In 2025, multiple ransomware actors relied on remote monitoring and management tools (RMMs) for multiple phases of the attack lifecycle. We observed a variety of these legitimate tools abused in incidents, including ANYDESK, SCREENCONNECT, and SPLASHTOP (Table 2).   
 
 
 
  In an UNC2465 incident, several weeks after the initial intrusion, the threat actors installed the TERAMIND RMM alongside Time Doctor. Time Doctor is an employee monitoring tool, which is capable of taking screenshots and screen recordings of the system as well as track website and application usage.  
 
 
 
  Threat actors continued to reduce their reliance on BEACON in ransomware operations; we observed BEACON in around 2% of intrusions, a decrease from an already diminished 11% in 2024. However, multiple threat clusters used other post-exploitation frameworks like AdaptixC2 (ADAPTAGENT), Exploration C2 (EXPLORATIONC2), or MYTHIC.  
 
 
 
  In an UNC2165 RANSOMHUB incident, the threat actors used COM hijacking as a persistence mechanism for MYTHIC. UNC2165 created MYTHIC in the "Temp" folder, renamed it to "msedge.dll," and modified the registry key for InprocServer32 to point to the MYTHIC payload.  
 
 
 
  Threat actors often used native Windows features to create services and register scheduled tasks to programmatically and recurrently execute malware, such as backdoors or tunnelers. For example, in a RHYSIDA incident, threat actors registered a scheduled task to run the LIONSHARE tunneler every 12 hours (Figure 7).  
 
 
  In a TridentLocker-branded incident, the threat actors uploaded WAVECALL, a downloader implemented as a .NET assembly, to a victim server running CrushFTP. They modified the command-line instruction used for processing file previews, replacing the configured executable paths for ImageMagick and ExifTool utilities with the WAVECALL assembly, thereby executing it whenever a file preview operation was initiated. The actors later reverted this configuration and updated the command-line instruction to execute a Base64-encoded PowerShell script to deploy a follow-on payload.  
 
  
   /Create /SC MINUTE /MO 720 /TN Reg /TR "C:\Windows\System32\rundll32.exe C:\windows\system32\config\red.dll Test" /ru system  
  Figure 7: Scheduled task for LIONSHARE   
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
       
 
 
 
  ANYDESK  
 
 
  ATERA  
 
 
  CHROMEREMOTEDESKTOP  
 
 
 
 
  DAMEWARE  
 
 
  DWAGENT  
 
 
  MESHAGENT  
 
 
 
 
  RUSTDESK  
 
 
  SCREENCONNECT  
 
 
  SPLASHTOP  
 
 
 
 
  TERAMIND  
 
   
   
 
 
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Table 2: Legitimate remote access tools used to establish a foothold and maintain a presence   
   Escalate Privileges  
  Gaining access to highly privileged accounts is a critical step for ransomware actors as it enables further stages of the attack, such as disabling AV software, deleting backups, and deploying ransomware across the network. Threat actors continue to rely on a variety of privilege escalation tools and techniques, including leveraging MIMIKATZ, dumping credentials stored by the Windows operating system, and abusing Active Directory (AD).  
 
 
  We observed threat actors leverage MIMIKATZ in approximately 18% of ransomware intrusions in 2025, demonstrating a slight, but continued decline in its overall use in recent years dropping from use in 20% of all ransomware intrusions in 2024. Notably, we observed a decline in other publicly available privilege escalation and credential stealing tools as well; for example, we did not observe LAZAGNE in any ransomware intrusions in 2025, a reduction from 2% of intrusions in 2024, 4% in 2023, and 6% in 2022.  
 
 
  Consistent with recent years, throughout 2025 threat actors used a myriad of techniques to target Windows authentication systems to gain access to privileged accounts.  
 
 
 
  We observed threat actors frequently attempting to obtain credentials stored by Windows systems by dumping the Local Security Authority Subsystem Service (LSASS) process memory, copying the Active Directory domain database (NTDS.dit) file, and exporting the Security Account Manager (SAM), SYSTEM, and SECURITY registry hives.  
 
 
  Other observed methods include Kerberoasting, modifying the registry to enable WDigest credentials caching, and the recovery of credentials via the Windows Data Protection API (DPAPI).  
 
 
  Threat actors routinely elevated privileges of compromised and actor-provisioned accounts by adding them to local and domain administrator groups and/or granting the accounts additional privileges such as SeRemoteInteractiveLogonRight, SeDebugPrivilege, SeLoadDriverPrivilege, and SeBackupPrivilege.  
 
 
  In some intrusions, threat actors abused AD roles to obtain elevated privileges through a variety of means, including DCSync replication and the misuse of AD Certificate Services (AD CS). In a MEDUSALOCKER.V2 incident, the threat actors executed the "Move-ADDirectoryServerOperationMasterRole" cmdlet to transfer Flexible Single Master Operation (FSMO) roles from the victim's AD domain controller to a suspected rogue domain controller.  
 
 
 
  We observed multiple threat actors attempt to harvest credentials from various internal sources, including backup tools, browsers, password managers, and credentials stored in cleartext.  
 
 
 
  In approximately 10% of intrusions we observed threat actors targeting Veeam Backup &amp; Replication for credential harvesting, which is consistent with activity observed in 2024. Multiple threat actors used the publicly available Veeam-Get-Creds.ps1 script or custom PowerShell scripts to obtain credentials stored in the Veeam configuration database.  
 
 
  In a handful of incidents, threat actors targeted Chromium-based browsers to obtain stored credentials. For example, in an UNC2165 RANSOMHUB incident, the threat actors executed inline PowerShell to retrieve and decrypt DPAPI-protected master encryption key from the Local State files of Google Chrome and Microsoft Edge allowing access to stored credentials within the browsers.  
 
 
  Threat actors accessed or attempted to access common password management tools, including KeePass, Bitwarden, and the Windows Credential Manager. During one UNC2465 intrusion involving AGENDA ransomware, the threat actor accessed a self-hosted Bitwarden server and exported and exfiltrated the contents of the vault database.  
 
 
  During a REDBIKE ransomware incident, the threat actor likely harvested a cleartext password from a SonicWall appliance, which was also shared with an admin account, granting the actor domain administrator privileges.  
 
 
 
  During one ransomware incident targeting a victim's virtualized environment, the threat actor exploited CVE-2024-37085 to gain administrator access to an ESXi hypervisor.  
 
 
  Internal Reconnaissance  
  In 2025, the tactics leveraged for internal reconnaissance remained fairly consistent with recent years; threat actors continued to rely on native system utilities, PowerShell commands, and publicly available software.  
 
 
  Threat actors consistently used PowerShell to query Active Directory (AD) objects for running processes, network shares, and user group memberships. This activity ranged from using native cmdlets like Get-ADComputer and Get-ADUser to using script blocks to query other system data.  
 
 
 
  In several cases, threat actors used Get-ADComputer and Get-ADUser to export lists of AD objects to a separate file. For example, in an incident involving MEDUSALOCKER.V2, the threat actors queried specific user object properties, exported account identity, contact information, and organizational metadata (Figure 8). At the same incident, the threat actors executed a different command to query domain-joined computers, capturing properties such as the operating system (OS), IPv4 address, and last logon date (Figure 9).  
 
 
  In some instances, threat actors executed PowerShell script blocks that ran a multitude of commands at once. For example, in an INTERLOCK incident, the threat actors ran a condensed one-line script that performed user profiling—including identifying the current user's username, Security Identifier (SID), and group memberships—checked for a domain connection, and enumerated the Domain Admins group. Notably, the script included a jitter, or time delay, to create random pauses between command execution, likely in an attempt to evade detection against rapid-fire command execution.  
 
 
 
  Threat actors continued to rely heavily on internal Windows utilities in this phase of the attack lifecycle, including ipconfig, netstat, ping, and nltest, among others.  
 
 
  Publicly available reconnaissance utilities were used in numerous intrusions. These publicly available tools ranged from those specialized in probing networks, such as Advanced IP Scanner, Softperfect Network Scanner (NETSCAN), and Angry IP Scanner, to red-teaming tools like PowerSploit and IMPACKET. Notably, network reconnaissance utilities like Advanced IP Scanner, NETSCAN, and Angry IP Scanner were used in approximately 50% of intrusions, similar to their observed usage in 2023 and 2024.  
 
 
  We often saw threat actors accessing files and folders related to potentially sensitive information. In some cases, they appeared to search for backup scripts and password managers, while in other cases they were likely attempting to find sensitive files to exfiltrate in order to increase the pressure applied by data theft extortion.  
 
 
 
  In a REDBIKE intrusion, the threat actors searched for keywords like "passport," "i9," and "cyber insurance." In addition to searching for personally identifiable information (PII) like passports and employment eligibility forms, it is plausible that the threat actors were also seeking to obtain the victim's cyber insurance policies to help them determine a negotiation strategy or maximum ransom amount to demand.  
 
 
 
  Several threat actors performed targeted internal reconnaissance for information about virtualized infrastructure within the victim environment, likely to facilitate ransomware deployment on these systems. In a REDBIKE incident, threat actors enumerated hypervisors by running the Get-VM cmdlet and accessed the internal VMware vSphere web portal.  
 
  
   powershell Import-Module ActiveDirectory; Get-ADUser -filter * -properties Enabled,DisplayName,Mail,SAMAccountName,homephone,ipphone,TelephoneNumber,comment,description,title | select Enabled,DisplayName,Mail,SAMAccountName,homephone,ipphone,TelephoneNumber,comment,description,title | export-csv C:\Users\Public\Music\users.csv   
  Figure 8: Get-ADUser HostCmd   
   powershell Import-Module ActiveDirectory; Get-ADComputer -Filter {enabled -eq $true} -properties *|select comment, description, Name, DNSHostName, OperatingSystem, LastLogonDate, ipv4address | Export-CSV C:\users\public\music\AllWindows.csv -NoTypeInformation -Encoding UTF8  
  Figure 9: Get-ADComputer HostCmd   
   Lateral Movement  
  Throughout 2025, actors extensively used common built-in protocols, including RDP, Server Message Block (SMB), and Secure Shell (SSH), combined with compromised credentials or attacker-created accounts for lateral movement. We also observed actors leveraging a variety of tools and utilities to tunnel and proxy traffic within victim environments.  
 
 
  In approximately 85% of intrusions, threat actors leveraged RDP with either compromised or attacker-created accounts for lateral movement.  
 
 
  Across a range of incidents we observed threat actors leveraging SMB for lateral movement to access network shares, stage payloads, and execute remote commands.  
 
 
 
  During one SAFEPAY ransomware incident, the threat actor leveraged SMB to access various network shares and used this access to stage a copy of NETSCAN on multiple hosts.  
 
 
  We also observed multiple actors leverage IMPACKET.SMBEXEC to execute remote commands. For example, in one intrusion leading to MEDUSALOCKER.V2 ransomware, the threat actor leveraged IMPACKET.SMBEXEC to run commands to create a new local administrator account on a remote host.  
 
 
 
  Across numerous incidents we observed various threat actors leverage common public utilities like PuTTY and KiTTY to establish SSH connections to hosts, particularly when moving laterally to ESXi systems.  
 
 
  We continued to observe frequent use of common Windows utilities like PsExec, Windows Remote Management (WinRM), and to a lesser extent Windows Management Instrumentation Command-line (WMIC), for remote execution and lateral movement.  
 
 
 
  In a handful of intrusions, threat actors used PowerShell to establish interactive remote sessions via WinRM using the "Enter-PSSession" cmdlet.  
 
 
  In an UNC5774 INTERLOCK ransomware incident, the threat actors used WinRM to establish a connection to a domain controller and execute remote commands, including using net.exe to reset the password of a user account.  
 
 
  During an UNC2465 incident, the threat actor moved laterally by using WMIC to execute a SMOKEDHAM payload on a remote host.  
 
 
 
  In numerous incidents, threat actors manipulated firewall rules in order to enable different types of traffic, such as RDP or SMB, to be allowed within the victim environment.  
 
 
 
  In one incident, UNC6021, a suspected FIN6 threat cluster, created a scheduled task that ran a netsh command to modify firewall rules to enable remote desktop access (Figure 10).  
 
 
  During one UNC6276 intrusion, the threat actor disabled the firewall on an ESXi host before deploying SYSTEMBC.LINUX on the host.  
 
 
  In one incident the threat actor installed OpenSSH on a host and ran a PowerShell command to configure a new firewall rule to allow inbound traffic on port 22 (Figure 11).  
 
 
  In an intrusion leading to the deployment of INC ransomware, the threat actor leveraged an attacker-created account to create new firewall policies that granted access to multiple additional subnets within the network.  
 
 
 
  Threat actors leveraged a variety of malicious and legitimate utilities to tunnel and proxy traffic within victim networks, including SYSTEMBC, VIPERTUNEL, PYSOXY, CLOUDFLARED, and OpenSSH. During one LOCKBIT.WARLOCK intrusions the threat actor leveraged CLOUDFLARED to tunnel an RDP connection between two hosts.  
 
 
  In a minimal number of incidents, threat actors leveraged publicly available post-exploitation tools including METASPLOIT and AMNESIAC.  
 
 
  Threat actors often abused access to various management consoles for virtual systems to move laterally to virtual hosts.   
 
 
 
  In multiple instances, the threat actors appeared to leverage this access to enable SSH on ESXi hosts prior to establishing SSH connections for lateral movement. For example, in a FOULFOG.LINUX incident, threat actors leveraged access from the victim's VMware vSphere centralized management portal to enable SSH on a vm-host, created user root1, SSHed using the newly created user, and disabled firewall.  
 
 
  During one incident the threat actor leveraged access to the victim's Nutanix Prism Central management tool along with a compromised account to move laterally to multiple additional systems. In the same incident, the threat actor also used the VMware web user interface to access numerous ESXi hosts.  
 
 
 
  In a subset of intrusions we observed evidence of threat actors conducting bruteforce attacks to gain access to accounts on additional systems.  
 
  
   cmd.exe /C netsh advfirewall firewall set rule group="remote desktop" new enable=No  
  Figure 10: netsh command to modify firewall rules to enable remote access   
   powershell.exe -Command New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22  
  Figure 11: PowerShell command to allow inbound SSH traffic   
   Complete Mission  
  The following sections highlight observations from the complete mission phase of the attack lifecycle, covering ransomware deployment, data exfiltration, and anti-analysis and recovery techniques. Threat actors conducting ransomware attacks routinely conduct multifaceted extortion operations involving data theft as it provides additional leverage during negotiations. Threat actors also consistently engage in a diverse range of tactics to ensure the success of their operations and reduce the ability for victims to recover, including tampering with security software, deleting backups, and clearing logs. Notable trends in 2025 include the prevalence of REDBIKE ransomware, an increase in the percentage of incidents involving data theft extortion, and indications that the techniques used to target virtual systems may be maturing.  
  Ransomware Families  
  REDBIKE was the most prominent ransomware observed in 2025 Mandiant incident response investigations, followed by AGENDA and then INC ransomware (Figure 12). In 2024, REDBIKE was tied for the number one spot with LOCKBIT.BLACK and RANSOMHUB; however, in 2024 LOCKBIT experienced significant disruptive actions stemming from law enforcement actions and in 2025 RansomHub abruptly ceased operations. Throughout 2025 we also observed a handful of incidents involving newly identified ransomware, such as NINTHBEE and SILVERPINE, demonstrating that at least a subset of threat actors are developing and maintaining new ransomware families.  
 
 
  REDBIKE was seen in almost 30% of 2025 ransomware incidents, surpassing previous highs for single ransomware families, including LOCKBIT and ALPHV reaching 17% each in 2023.  
 
 
  We continue to observe threat actors reusing existing ransomware families in seemingly unrelated operations conducted under different extortion brands.  
 
 
 
  While we have seen a significant decrease in LOCKBIT ransomware incidents since the legal actions taken against the RaaS in 2024, in 2025 we did observe a handful of LOCKBIT.WARLOCK incidents. The WarLock DLS emerged in July 2025 and has listed over 75 victims since. LOCKBIT.WARLOCK largely leverages the original LOCKBIT codebase; however, it uses different encryption algorithms, and refactors previously inlined operations into dedicated functions.  
 
 
  In 2025, we observed a handful of intrusions involving CONTI ransomware, though the CONTI RaaS was shut down in May 2022 following the leak of associated chat logs and the CONTI source code. For example, we observed CONTI deployed in a 2025 incident associated with the Gunra ransomware group; analysis of the ransomware payload identified it was heavily based on CONTI's source code, with slight variations in obfuscation.  
 
 
 
  We observed three different extortion brands leveraging INC ransomware in their operations: INC Ransom, Sinobi, and Lynx. The INC ransomware source code was advertised in an underground forum in May 2024 but the Lynx and INC Ransom DLS domains were acquired by a common threat actor.  
 
 
  GTIG observed ODDSIDE ransomware in an incident in 2025; ODDSIDE is PowerShell-based ransomware that refers to itself as DARKMATTER. While not completely unheard of, PowerShell-based ransomware is fairly rare.  
 
 
  Notably, in one incident we observed threat actors deploy CLOP ransomware. This is the first time we’ve responded to a CLOP ransomware incident since 2020, though we have occasionally identified CLOP ransomware samples uploaded to malware repositories. In recent years, threat actors associated with the CL0P data leak site have primarily conducted data-theft-extortion-only operations rather than performing encryption.  
 
 
  In a subset of incidents, we were unable to obtain the ransomware payloads. For example, we observed a handful of TridentLocker-branded ransomware incidents in which there is evidence to suggest that the ransomware payload was executed in memory. It's plausible the threat actors used in-memory execution to deploy ransomware to try and bypass security detections and potentially make analysis and recovery efforts more difficult.  
 
 
  Threat actors occasionally abuse legitimate encryption tools in their extortion operations. In 2025, we observed an incident in which threat actors used BitLocker to encrypt over 200 remote hosts.  
 
  
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 12: Distribution of ransomware families observed in 2025 investigations  
      
     

  
       
     
  




 
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
       
 
 
 
   Ransomware Families Observed in 2025 Mandiant Investigations   
 
 
 
 
  AGENDA  
  AGENDA.ESXI  
  AGENDA.RUST  
 
 
  BABUK  
  BABUK.MARIO  
 
 
  CLOP  
 
 
 
 
  CONTI  
 
 
  CRYTOX  
 
 
  DOLLARLOCKER  
 
 
 
 
  FOULFOG.LINUX  
 
 
  INC  
  INC.LINUX  
 
 
  INTERLOCK  
 
 
 
 
  LOCKBIT.UNIX  
  LOCKBIT.WARLOCK  
 
 
  MEDUSALOCKER.V2  
 
 
  NINTHBEE  
 
 
 
 
  NITROGEN  
 
 
  ODDSIDE  
 
 
  PLAYCRYPT  
 
 
 
 
  RANSOMHUB  
 
 
  REDBIKE  
 
 
  RHYSIDA  
 
 
 
 
  RIFTTEAR  
 
 
  SAFEPAY  
 
 
  SILVERPINE  
 
 
 
 
  WHITERABBIT  
 
   
   
 
 
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Table 3: Ransomware families observed in Mandiant's 2025 incident response investigations   
   Data Exfiltration  
  In 2025, we observed confirmed or suspected data theft in approximately 77% of ransomware intrusions, a notable increase from approximately 57% in 2024. In these incidents, the most frequently observed strategies for identifying, staging, and exfiltrating data included the use of legitimate data synchronization tools such as Rclone and MEGASync, file compression using built-in tools or portable versions of WinRar or 7Zip, and FTP clients such as Filezilla or Winscp.  
 
 
  During intrusions where data was stolen, we routinely observed threat actors targeting a variety of sensitive data types, including legal, human resources, accounting, and business development data.  
 
 
 
  We observed evidence of threat actors conducting manual reconnaissance of systems likely to gather sensitive data for exfiltration such as accessing emails and attempting to access SharePoint and other Microsoft 365 environments via the browser.  
 
 
 
  In 2025, threat actors continued to rely on publicly available tools and utilities—including Rclone, MEGASync, Megatools, restic, and possibly Cyberduck—to exfiltrate data.  
 
 
 
  We observed Rclone in approximately 28% of intrusions where data theft was confirmed or suspected to exfiltrate data to attacker-controlled infrastructure.  
 
 
  In one INC ransomware incident, the threat actor used the wget and curl commands to download Rclone and an INC.LINUX ransomware payload respectively to a network-attached storage (NAS) server. The threat actor subsequently ran Rclone to exfiltrate data from the server prior to manually executing the INC.LINUX payload.  
 
 
  Threat actors installed and/or leveraged legitimate FTP/SFTP clients in 26% of intrusions where data theft was observed or suspected. Commonly observed software included FileZilla, WinSCP, and PuTTY Secure Copy.  
 
 
  While not confirmed to be used for data exfiltration, we observed threat actors installing and/or executing various utilities that could be used to aid in the reconnaissance, staging, and export of stolen data such as Total Commander, Xcopy, and Gpg4win.  
 
 
 
  Threat actors leveraged a myriad of legitimate cloud services and infrastructure to exfiltrate stolen data, including Azure, AWS, Backblaze, Cloudzy, Filemail, Google Drive, and MEGA, and OneDrive.  
 
 
 
  In one UNC5471 intrusion leading to AGENDA ransomware, the threat actor leveraged batch scripts alongside WinRAR to automate the archiving of files in directories. The actor then used Megatools and SLEETSEND to exfiltrate the data to the MEGA and Cloudzy cloud storage services.  
 
 
  We observed multiple threat actors transferring stolen data to attacker-controlled OneDrive accounts. During one UNC5496 intrusion, the threat actor ran commands to have Rclone transfer all files that matched a list of common file extension types to a threat actor-controlled OneDrive account.  
 
 
  In multiple incidents, we observed threat actors leveraging AzCopy to transfer stolen files to attacker-controlled Azure storage.  
 
 
 
  During one UNC6098 intrusion, the threat actor leveraged the SQL Server Import and Export Wizard to export a SQL database.  
 
 
  Ransomware Deployment  
  We observed a diverse set of ransomware deployment techniques leveraged in intrusions throughout 2025. Threat actors employed both manual and automated deployment techniques, including the use of batch scripts, scheduled tasks, Group Policy Objects (GPOs), registry keys, and PowerShell scripts. Notably, in almost 20% of incidents, threat actors targeted virtualization infrastructure, and we observed multiple incidents where operators automated portions of their ransomware deployment against ESXi hosts, suggesting techniques used to target virtual systems may be maturing.  
 
 
  Threat actors often relied on automated mechanisms to deploy ransomware. In many cases, they relied on native Windows mechanisms to facilitate ransomware execution.  
 
 
 
  Multiple threat clusters leveraged batch scripts to facilitate ransomware payload execution in victim environments. In one LOCKBIT.WARLOCK intrusion, the threat actor staged NetExec on a domain controller along with files to run the ransomware payload. The threat actor then used NetExec to copy a batch file to numerous hosts via SMB and run it to execute the ransomware payload.  
 
 
  In a separate LOCKBIT.WARLOCK intrusion, the threat actor staged ransomware payloads on multiple hosts via SMB before executing them via scheduled tasks.  
 
 
  During a NINTHBEE ransomware incident, the threat actor modified a GPO to include a malicious scheduled task that disabled Windows Defender and subsequently executed the ransomware payload. In the same intrusion, the threat actor also attempted to execute the NINTHBEE payload on multiple remote hosts via PsExec.  
 
 
  In an incident likely involving DOLLARLOCKER, a threat actor created a Windows service to run a command to execute the ransomware payload.  
 
 
  Multiple threat clusters leveraged the Windows Registry to complete their ransomware deployment objectives. During an UNC5471 intrusion, the threat actor created registry Run keys to execute AGENDA ransomware on multiple servers persistently. In one INTERLOCK ransomware intrusion, following encryption, the threat actor modified the LegalNoticeCaption and LegalNoticeText registry values to display a banner indicating the system was ransomed on start up.  
 
 
 
  In addition to using SMB to stage ransomware payloads, we also observed threat actors leverage SMB to facilitate more expansive ransomware deployment across victim networks. In one incident, actors identified network shares via the "Invoke-ShareFinder" PowerShell cmdlet and likely supplied this list to REDBIKE as a list of targets. Ultimately, encryption was attempted on more than 500 endpoints via SMB.  
 
 
  In a small subset of observed intrusions, threat actors leverage PowerShell to automate the deployment of BitLocker encryption across victims' environments. During one intrusion, the threat actor used a PowerShell script to install, configure, and assign passwords for BitLocker on multiple hosts. The threat actor then enabled encryption on multiple drives on these hosts and scheduled a system restart to force the hosts into a locked state. The actor also modified the registry to display a ransom note on the BitLocker preboot recovery screen.  
 
 
  In approximately 43% of ransomware intrusions we responded to in 2025, the threat actors were observed targeting virtualization infrastructure, an increase from 29% in 2024. While ransomware deployment to virtual systems is often done manually, in 2025 we observed at least some incidents where threat actors attempted to automate portions of the ransomware deployment stage.  
 
 
 
  During an UNC5495 intrusion, the threat actor automated the deployment of BABUK.MARIO by leveraging a batch script that accepted credentials for ESXi hosts. The batch script used a staged copy of KiTTY to copy the ransomware payload to the host and then connect via SSH and run a command to execute the payload on each host. In a separate intrusion, a threat actor leveraged a PowerShell script to authenticate to the victim's vCenter server, set new root passwords, and enable SSH on ESXi hosts. The same script was used to subsequently copy a RIFTEAR ransomware payload to the hosts, delete backups, shutdown virtual machines (VMs), and disable security policies prior to executing the ransomware payload.  
 
 
 
  Prior to ransomware deployment on ESXi hosts, threat actors commonly disabled the ExecInstalledOnly setting on hosts to allow for the execution of custom binaries (Figure 13). During one intrusion, the threat actor also accessed a vCenter server and modified the Lockdown Mode Exception Users settings, which controls users that are allowed to maintain privileges when the host is in lockdown mode.  
 
 
  Across multiple intrusions, threat actors took steps to stop virtual machines and unlock files prior to decryption, almost certainly to maximize the impact of their ransomware payloads.  
 
 
 
  In multiple instances threat actors used or attempted to use IOBIT, a legitimate uninstaller utility, to unlock files in use by other programs prior to executing ransomware payloads.  
 
 
  We also observed multiple actors shutting down virtual machines and deleting backups and snapshots prior to encryption. In at least one intrusion, an actor leveraged a PowerShell script to automate the process of powering off virtual machines.  
 
 
  During one intrusion, the threat actor accessed the victim's Commvault server and deleted vCenter backup volumes prior to encryption to hinder recovery.  
 
 
 
  During a TridentLocker-branded ransomware incident, we assess with moderate confidence that the threat actor leveraged the same CrushFTP preview hijacking technique used for WAVECALL persistence to download and execute a ransomware payload from the WAVECALL C2 server.  
 
  
   esxcli system settings advanced set -o /User/execInstalledOnly -i 0  
  Figure 13: Command to disable ExecInstalledOnly setting on ESXi hosts   
   Anti-Detection, Analysis, and Recovery Tactics  
  Ransomware actors consistently engage in anti-detection, anti-analysis, and anti-recovery tactics in their operations in an effort to not only prevent detection during the intrusion, but increase the difficulty for victims to recover post-encryption. While these tactics are often manually performed by threat actors, numerous ransomware families feature built-in capabilities to hinder analysis and delete backups prior to encryption.  
 
 
  Threat actors consistently disabled and tampered with security controls during ransomware intrusions to avoid detection and/or block of execution of malicious payloads. Most commonly, we observed threat actors disabling Windows Defender, often by modifying the Windows registry. In some other cases, the threat actors modified Defender configurations via the Set-MpPreference PowerShell cmdlet to add exclusions for their malware and ransomware payloads. Threat actors also were observed leveraging GPOs, scheduled tasks, and PowerShell scripts in order to tamper with a variety of security controls.  
 
 
 
  In a REDBIKE incident, threat actors used PowerShell to disable a multitude of Windows Defender features by running commands to modify a variety of values associated with Windows Defender registry keys, including DisableRealtimeMonitoring, DisableScanOnRealtimeEnable, and DisableOnAccessProtection (Figure 14).  
 
 
  In an intrusion involving WHITERABBIT, threat actors executed a Base64-encoded PowerShell command that used the "Add-MpPreference" cmdlet to modify the Defender Exclusion list to include the ransomware binary; a variety of file extensions, such as ".cmd," ".bat," and ".exe"; as well as User Data folders.  
 
 
  In an incident involving NINTHBEE, threat actors registered a scheduled task to execute daily a command that disables Microsoft Defender's real-time scanning for downloaded files and email attachments.  
 
 
 
  Ransomware actors often deleted artifacts and cleared event logs to remove evidence of their activity. These records included information about command execution, firewall traffic, and stolen credentials. The wevtutil utility was used to facilitate log deletion in multiple instances.  
 
 
 
  In a FOULFOG.LINUX incident, the threat actors renamed the ransomware binary to a less suspicious name, "filerw"; deleted the command history for the system; and created an empty file to replace the deleted file.  
 
 
 
  In some cases, threat actors used benign names in their operations in an attempt to masquerade as legitimate software or system resources. For example, in a RIFTTEAR incident, threat actors registered a scheduled task named "\Microsoft\Update" to execute a malicious command likely intended to kill endpoint detection and response (EDR) processes. In a separate case involving CONTI, the ransomware binary had its filename renamed from "enc_lin" to "rsync" in an attempt to appear as the native synchronization command-line utility.  
 
 
  Ransomware actors often disabled or deleted backups to inhibit and/or limit recovery options. In some cases, threat actors stopped backup servers and/or deleted Volume Shadow Copies (VSS) via PowerShell scripts.  
 
 
 
  Notably, in a RANSOMHUB incident, the threat actors used the access to Cisco Integrated Management Controller (CIMC) to map a Debian Linux ISO image via Virtual Media across a nine-node Cohesity cluster. By modifying the boot priority and hardware power-cycling, the nodes booted into the external Linux environment, overwriting the Cohesity operating system (OS) and rendering the backup data inaccessible.  
 
 
 
  In a handful of intrusions, the threat actors used tooling to terminate processes and services associated with security software solutions, specifically those abusing signed kernel mode drivers. Examples include the open-source TERMINATOR and WATCHDOGKILLER, as well as non-publicly available tools such as WARCLAW, a utility that decodes and installs a vulnerable kernel mode driver.  
 
  
   cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d "1" /f 

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d "1" /f 

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d "1" /f 

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableIOAVProtection" /t REG_DWORD /d "1" /f 

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Reporting" /v "DisableEnhancedNotifications" /t REG_DWORD /d "1" /f 

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SpyNet" /v "DisableBlockAtFirstSeen" /t REG_DWORD /d "1" /f 

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SpyNet" /v "SubmitSamplesConsent" /t REG_DWORD /d "0" /f

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\MpEngine" /v "MpEnablePus" /t REG_DWORD /d "0" /f

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d "1"

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender" /v "DisableAntiVirus" /t REG_DWORD /d "1" /f

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SpyNet" /v "SpynetReporting" /t REG_DWORD /d "0" /f

cmd.exe /c reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d "1" /f  
  Figure 14: Windows Defender registry key modification   
   Tool Prevalence  
  Throughout 2025, we continued to see ransomware actors rely heavily on publicly available tools and legitimate software across various stages of ransomware intrusions. While legitimate software remains popular, we observed a slight decrease in the use of RMM tools and post-exploitation C2 frameworks. Notably, both WinRAR and Rclone were observed in almost one-fourth of incidents, likely corresponding with the increase in incidents involving data theft, given that these tools are regularly used to stage and exfiltrate data respectively.  
 
 
  Threat actors used post-exploitation C2 frameworks in about 15% of 2025 ransomware incidents, a decrease from almost 20% in 2024. The decline in the use of post-exploitation frameworks is largely due to the continued reduction in use of Cobalt Strike BEACON.  
 
 
 
  Cobalt Strike BEACON was deployed in only 2% of 2025 ransomware incidents, continuing a multi-year downward trend; in 2021 roughly 60% of ransomware incidents involved BEACON, dropping to around 38% in 2022, 20% in 2023, and 11% in 2024. This decrease could in part be attributed to some subset of actors exploring new frameworks, like AdaptixC2.  
 
 
  We observed approximately 8% of intrusions involving the AdaptixC2 (ADAPTAGENT) post-exploitation framework.    AdaptixC2    is an open-source post-exploitation framework developed for penetration testers; however, similar to the use of CobaltStrike for many years, threat actors often abuse these types of pentesting tools to facilitate their operations.  
 
 
  Less frequently, we observed the penetration frameworks associated with MYTHICAGENT, METASPLOIT, HAVOC, and EXPLORATIONC2.  
 
 
 
  Extending a trend identified last year, threat actors appear slightly less reliant on remote management tools. Around 24% of 2025 incidents involved at least one RMM, compared to 28% in 2024, and 40% in 2023.  
 
 
 
  We observed 10 unique remote management tools in ransomware incidents in 2025 comparable to nine in 2024, but an overall decrease from 13 in 2023.  
 
 
  We also saw a decrease in instances of threat actors leveraging multiple different RMMs within the same intrusion. In 2025, multiple RMMs were only observed in ~5% of incidents, compared to 8% in 2024, and 16% in 2023.  
 
 
  Consistent with recent years, AnyDesk remained the most commonly deployed RMM in ransomware incidents in 2025; however, overall use decreased from roughly 31% in 2023 and 16% in 2024 to 10% in 2025.  
 
 
 
  Threat actors' use of tunnelers remained fairly consistent as compared to 2024; however, there were small shifts in the use of specific tunnelers. For example, CLOUDFLARED was observed in 8% of incidents in 2025 compared to around 4% in 2024.  
 
 
 
  We've observed a negligible decline in the use of SYSTEMBC, with around 14% of incidents involving the tunneler in 2023, a little over 7% in 2024, and down to a little over 6% in 2025. Notably, Operation Endgame    disrupted    SYSTEMBC infrastructure in May 2024; while the malware is still being sold on forums, it's plausible that the law enforcement disruption dissuaded some threat actors from continuing to use the malware in their operations.  
 
 
 
  Throughout 2025, threat actors continued to leverage common publicly available network scanning tools such as Advanced IP Scanner and SoftPerfect Network Scanner in around 50% of intrusions, consistent with the 2024 rate.  
 
 
  In 2025, we observed an increase in the use of public tools like WinRAR and Rclone that are often used by threat actors to facilitate data theft, which aligns with our overall increase in incidents involving suspected or confirmed data theft from 2024 to 2025. Both WinRAR and Rclone were observed in approximately 23% of incidents; in 2024, we observed around 16% of intrusions involving Rclone and only around 8% involving WinRAR.  
 
 
  Remediation and Hardening  
  Recommendations to assist in addressing the threat posed by ransomware are captured in our white paper,    Ransomware Protection and Containment Strategies: Practical Guidance for Endpoint Protection, Hardening, and Containment   .   
  Outlook and Implications  
  Despite ongoing turmoil caused by actor conflicts and disruption, ransomware actors remain highly motivated and the extortion ecosystem demonstrates continued resilience. Several indicators suggest the overall profitability of these operations is, however, declining, and at least some threat actors are shifting their targeting calculus away from large companies to instead focus on higher volume attacks against smaller organizations. This is likely due to increased difficulty in successful deployments due to victims' improved security postures, a greater refusal to pay ransom demands, and enhanced recovery capabilities. In the coming years, evolving regulations, including reporting requirements and payment bans, may further dissuade some companies from making ransom payments. While we anticipate ransomware to remain one of the most dominant threats globally, the reduction in profits may cause some threat actors to seek other monetization methods. This could manifest as increased data theft extortion operations, the use of more aggressive extortion tactics, or opportunistically using access to victim environments for secondary monetization mechanisms such as using compromised infrastructure to send phishing messages.  
  Detections  
  YARA Rules  
   AGENDA    
   rule M_APTFIN_Ransom_AGENDA_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"

	strings:
		$conf1 = "public_rsa_pem" fullword
		$conf2 = "private_rsa_pem" fullword
		$conf3 = "directory_black_list" fullword
		$conf4 = "file_black_list" fullword
		$conf5 = "file_pattern_black_list" fullword
		$conf6 = "process_black_list" fullword
		$conf7 = "win_services_black_list" fullword
		$conf8 = "company_id" fullword
		$conf9 = "note" fullword
		$load_const1 = { 21 B7 F6 F7 }
		$load_const2 = { F6 36 A4 69 }
		$load_s1 = "run_portable_executable" fullword
		$load_s2 = "MemoryLoadLibrary" fullword
		$load_s3 = "_ZN9morph_poc4main"
		$note1 = "Extension: "
		$note2 = "Domain: "
		$note3 = "login: "
		$note4 = "password: "
		$note5 = "Enter credentials-- Credentials"
		$note6 = "-- Qilin"
		$note7 = "-- Recovery"
		$note8 = "www.torproject.org"
		$note9 = ".onion"
		$note10 = "Employees personal data, CVs, DL , SSN."
		$note11 = "%s/%s_RECOVER.txt"
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and (7 of ($conf*) or 7 of ($note*) or all of ($load*))
}   
   AGENDA.RUST   
   rule M_Hunting_Win_Ransomware_AGENDA_RUST_2_MBeta {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"

	strings:
		$rust = "/rust/"
		$conf1 = "\"public_rsa_pem\":"
		$conf2 = "\"private_rsa_pem\":"
		$conf3 = "\"directory_black_list\":"
		$conf4 = "\"file_black_list\":"
		$conf5 = "\"file_pattern_black_list\":"
		$conf6 = "\"process_black_list\":"
		$conf7 = "\"win_services_black_list\":"
		$conf8 = "\"company_id\":"
		$conf9 = "\"n\":"
		$conf10 = "\"p\":"
		$conf11 = "\"fast\":"
		$conf12 = "\"skip\":"
		$conf13 = "\"step\":"
		$conf14 = "\"accounts\":"
		$conf15 = "\"note\":"
	condition:
		uint16(0) == 0x5a4d and uint32(uint32(0x3C)) == 0x00004550 and filesize &lt; 5MB and (($rust and 8 of ($conf*)) or (13 of ($conf*)))
}   
  REDBIKE  
   rule M_Ransom_REDBIKE_2 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"

	strings:
		$a1 = ".akira"
		$a2 = "akira_readme.txt"
		$a3 = "akiralkzxzq2dsrzsrvbr2xgbbu2wgsmxryd4csgfameg52n7efvr2id"
		$s1 = "--encryption_percent" ascii wide nocase
		$s2 = "--encryption_path" ascii wide nocase
		$s3 = "--share_file" ascii wide nocase
	condition:
		((all of ($s*)) and (any of ($a*))) and (uint16(0) == 0x5A4D) and filesize &gt; 500KB and filesize &lt; 2MB
}   
   REDBIKE.LINUX   
   rule M_APTFIN_Ransom_REDBIKE_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"

	strings:
		$a = "akira_readme.txt"
		$b = "save your TIME, MONEY, EFFORTS"
		$c = "akiral2iz6a7qgd3ayp3l6yub7xx2uep76idk3u2kollpj5z3z636bad.onion"
		$d = "--encryption_percent"
		$e = "--encryption_path"
		$f = "--share_file"
	condition:
		all of them and (uint32be(0) == 0x7F454C46)
}   
   CLOP   
   rule M_Hunting_CLOP_rol7XorHash32_ConfigHashes_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"

	strings:
		$hex_asm_literal_a = { 92 F7 53 7A }
		$hex_asm_literal_b = { 43 29 79 71 }
		$hex_asm_literal_c = { 2A 81 C4 E2 }
		$hex_asm_literal_d = { 2E F4 FA 7E }
		$hex_asm_literal_e = { 31 E5 7F 91 }
		$hex_asm_literal_f = { 16 24 45 D6 }
		$hex_asm_literal_g = { 56 22 93 EA }
	condition:
		all of them
}   
   CLOP.LINUX   
   rule M_Ransom_CLOP_3 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$str_jobmessage_a = "Successfully started daemon-name"
		$str_jobmessage_b = "Could not change working directory to /"
		$str_jobmessage_c = "Could not generate session ID for child process"
		$asm_code_fileordirectory = { 25 00 F0 00 00 3D 00 40 00 00 75 }
		$asm_functioncall_open64_readfile = { 80 01 00 00 C7 44 ( 2? | 6? | A? | E? ) ?? 02 00 00 00 }
		$asm_functioncall_open64_writebytes = { B4 01 00 00 C7 44 ( 2? | 6? | A? | E? ) ?? 42 00 00 00 }
		$asm_encryption_filebuffersize = { 00 E1 F5 05 76 ?? C7 45 ?? 00 E1 F5 05 }
		$asm_encryption_generatekey = { 1F 89 ( C? | D? | E? | F? ) C1 ( C? | D? | E? | F? ) 18 8D ( 0? | 1? ) ( 0? | 1? ) 25 FF 00 [0-2] 29 ( C? | D? | E? | F? ) 83 ( C? | D? | E? | F? ) 01 C9 }
	condition:
		uint32(0) == 0x464C457F and all of ($str_*) or (#asm_code_fileordirectory == 2 and #asm_functioncall_open64_writebytes == 2 and ($asm_encryption_generatekey and $asm_functioncall_open64_readfile and $asm_encryption_filebuffersize))
}   
  PLAYCRYPT  
   rule M_Ransomware_PLAYCRYPT_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
		date_created = "2022-12-21"
		date_modified = "2022-12-21"
		rev = "1"
	strings:
		$c1 = { 8A CB 0F B6 D0 8B F2 8B FA D3 EE 8D 4B 01 D3 EF 83 E6 01 83 E7 01 }
		$c2 = { 8D 45 F0 C7 85 D0 FD FF FF 00 00 00 00 50 83 EC 08 }
		$c3 = { 8B 14 0A 8B 4C 32 20 03 D6 89 55 E0 03 CE }
		$c4 = { 8D 8D 80 ?? FF FF E8 C8 ?? FF FF 85 C0 75 61 83 BD [2] FF FF 05 76 58 }
		$c5 = { FF 76 ?? C6 45 EE 00 E8 [2] 00 00 8B F0 8B CF 33 C0 85 F6 0F 48 F0 E8 }
		$c6 = { FF D0 8B F8 83 FF 05 0F [2] 01 00 00 83 FF 06 0F [2] 01 00 00 8B 0E 3B 4E 04 0F [2] 01 00 00 83 FF 04 74 6D 83 FF 01 }
		$s1 = "OpaqueKeyBlob" wide
		$s2 = "AppPolicyGetProcessTerminationMethod"
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and filesize &gt; 100KB and filesize &lt; 200KB and ((2 of ($c*) and all of ($s*)) or (4 of ($c*)))
}   
   PLAYCRYPT.LINUX   
   rule G_Ransom_PLAYCRYPT_LINUX_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "First step is done."
		$s2 = "/dev/urandom"
		$s3 = "esxcli storage filesystem list &gt; storage"
		$s4 = "hosts in exclusion:"
		$s5 = "encrypt: "
		$s6 = ".PLAY" fullword
	condition:
		uint32(0) == 0x464C457F and all of them
}   
  SAFEPAY  
   import "pe"

rule G_Ransom_SAFEPAY_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$hex_asm_snippet = { 10 27 00 00 [0-4] 10 27 00 00 }
	condition:
		pe.imphash() == "ff67c703589f775db9aed5a03e4489b0" and ($hex_asm_snippet)
}   
   rule G_Ransom_SAFEPAY_2 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$code_string_decode = { 8A C2 32 C1 32 44 0D ?? 34 ?? 88 44 0D ?? 41 83 F9 04 [4-64] B? 4D 5A 00 00 }
		$code_hardware_aes_check = { 0F A2 8B F3 5B 89 07 89 77 ?? 89 4F ?? 89 57 [0-12] ( 00 00 00 02 | C1 ?? 19 ) }
		$code_encrypt_file = { 14 00 10 00 [2-24] 14 00 10 00 [2-32] 00 10 00 5? [0-8] FF ( 15 | D? ) }
		$enc_str1 = { C7 45 ?? 67 4B 3D 49 C7 45 ?? 2F 4F 2F 4D }
		$enc_str2 = { C7 45 ?? 10 3C 51 3E C7 45 ?? 5C 38 4F 3A C7 45 ?? 42 34 58 36 C7 45 ?? 43 30 58 32 66 C7 45 ?? 2D 2C }
		$enc_str3 = { C7 45 ?? A3 8F FF 8D C7 45 ?? EF 8B E4 89 C7 45 ?? E0 87 E0 85 C7 45 ?? E7 83 EC 81 C7 45 ?? FB 9F E8 9D C7 45 ?? FF 9B 98 99 }
		$enc_str4 = { C7 45 ?? 44 40 51 47 C7 45 ?? 51 49 10 10 C7 45 ?? 03 48 43 42 C6 45 ?? 29 }
		$enc_str5 = { C7 45 ?? 77 77 73 74 C7 45 ?? 75 6D 64 70 C7 45 ?? 23 68 63 62 C6 45 ?? 09 }
	condition:
		uint16(0) == 0x5a4d and (all of ($code*) or (any of ($code*) and any of ($enc*)) or (2 of ($enc*)))
}   
  INC  
   rule M_Ransom_INC_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "[*] Count of arguments: %d" wide
		$s2 = "[-] Failed" wide
		$s3 = "[+] Start" wide
		$s4 = "INC-README" wide
		$s5 = "--debug" wide
		$s6 = "RECYCLE" wide
	condition:
		all of them and (uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550)
}   
   INC (Lynx Branded)   
   rule M_Ransom_INC_2 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "[+] Proccess %s with PID: %d was killed succesffully" wide
		$s2 = "[*] Sending note to printer:" wide
		$s3 = "[+] Recycling bin..." wide
		$s4 = "[*] Starting full encryption in 5s" wide
		$s5 = "[+] Successfully decoded readme!" wide
		$s6 = "[-] Failed" wide
		$lynx = "lynx" ascii wide nocase
	condition:
		$lynx and 4 of ($s*) and (uint16(0) == 0x5A4D) and filesize &lt; 300KB and filesize &gt; 50KB
}   
   INC (Sinobi Branded)   
   rule G_Ransom_INC_3 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "[+] Proccess %s with PID: %d was killed succesffully" wide
		$s2 = "[*] Sending note to printer:" wide
		$s3 = "[+] Recycling bin..." wide
		$s4 = "[*] Starting full encryption in 5s" wide
		$s5 = "[+] Successfully decoded readme!" wide
		$s6 = "[-] Failed" wide
		$sin = "sinobi" ascii wide nocase
	condition:
		$sin and 4 of ($s*) and (uint16(0) == 0x5A4D) and filesize &lt; 400KB and filesize &gt; 50KB
}   
  INC.LINUX  
   rule M_Ransom_INC_2 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "[*] Count of arguments: %d"
		$s2 = "[-] Failed"
		$s3 = "[+] Start"
		$s4 = "INC-README"
		$s5 = "--debug"
		$s6 = "vmsvc"
	condition:
		all of them and uint32(0) == 0x464c457f
}   
  RANSOMHUB  
   rule M_Ransom_RANSOMHUB_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$str1 = "json:\"settings\""
		$str2 = "json:\"extension\""
		$str3 = "json:\"net_spread\""
		$str4 = "json:\"local_disks\""
		$str5 = "json:\"running_one\""
		$str6 = "json:\"self_delete\""
		$str7 = "json:\"white_files\""
		$str8 = "json:\"white_hosts\""
		$str9 = "json:\"credentials\""
		$str10 = "json:\"kill_services\""
		$str11 = "json:\"set_wallpaper\""
		$str12 = "json:\"white_folders\""
		$str13 = "json:\"note_file_name\""
		$str14 = "json:\"note_full_text\""
		$str15 = "json:\"kill_processes\""
		$str16 = "json:\"network_shares\""
		$str17 = "json:\"note_short_text\""
		$str18 = "json:\"master_public_key\""
	condition:
		14 of them
}   
  FURYSTORM  
   rule G_Ransom_FURYSTORM_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "Whitelist VM id"
		$s2 = "gwfn6l3bk45o2zecvi7xtyqrpsudmahj"
		$s3 = "Dry-run"
		$s4 = "-paths"
		$s5 = "-vmsvc"
		$s6 = "Note: motd=%d login=%d clean=%d"
		$s7 = "Cryptor args"
		$s8 = "VMX found"
		$s9 = "Keys: %016l"
		$s10 = "vim-cmd"
		$s11 = "Dropping readme"
		$s12 = "Encryption params"
	condition:
		uint32(0) == 0x464c457f and filesize &gt; 50KB and filesize &lt; 700KB and 6 of them
}   
   rule G_Ransom_FURYSTORM_2 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$s1 = "Failed decrypt file:"
		$s2 = "Decryptor args:"
		$s3 = "Private key loaded"
		$s4 = "Keys: %016l"
		$s5 = "Dry-run"
		$s6 = "Encryption params"
		$s7 = "Whitelist paths"
		$s8 = "Note: motd=%d"
	condition:
		uint32(0) == 0x464c457f and filesize &gt; 50KB and filesize &lt; 300KB and 6 of them
}   
  FIREFLAME  
   rule M_Autopatt_Ransom_FIREFLAME_1 {
	meta:
		author = "Google Threat Intelligence Group (GTIG)"
	strings:
		$p00_0 = { 8B CE 8D 5F ?? 8A 01 8D 49 ?? 0F B6 C0 83 E8 ?? 8D 04 40 C1 E0 ?? 99 }
		$p00_1 = { 55 8B EC FF 75 ?? E8 [4] 59 8B 4D ?? 89 01 F7 D8 1B C0 }
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and (($p00_0 in (0 .. 380000) and $p00_1 in (260000 .. 280000)))
}   
   Acknowledgements  
  This analysis would not have been possible without the assistance of Dima Lenz, Chastine Altares, Ana Foreman, and the Advanced Practices, Mandiant Consulting, and FLARE teams.
