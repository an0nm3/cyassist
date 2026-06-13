---
source: rss/mandiant
title: Look What You Made Us Patch: 2025 Zero-Days in Review
url: https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/
date: 2026-03-05
item_id: https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/
category: news
tags: [Bypass, CVE, Exploit, Injection, Rce]
---

**Source:** Mandiant
**Link:** https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/

Written by: Casey Charrier, James Sadowski, Zander Work, Clement Lecigne, Benoît Sevens, Fred Plan 
  
   Executive Summary  
  Google Threat Intelligence Group (GTIG) tracked 90 zero-day vulnerabilities exploited in-the-wild in 2025. Although that volume of zero-days is lower than the record high observed in 2023 (100), it is higher than 2024’s count (78) and remained within the 60–100 range established over the previous four years, indicating a trend toward stabilization at these levels.  
  In 2025, we continued to observe the structural shift, first identified in 2024, toward increased enterprise exploitation. Both the raw number (43) and proportion (48%) of vulnerabilities impacting enterprise technologies reached all-time highs, accounting for almost 50% of total zero-days exploited in 2025. We observed a sustained decrease in detected browser-based exploitation, which fell to historical lows, while seeing increased abuse of operating system vulnerabilities.  
  State-sponsored espionage groups continue to prioritize edge devices and security appliances as prime entry points into victim networks, with just over half of attributed zero-day exploitation by these groups focused on these technologies. Commercial surveillance vendors (CSVs) maintained an interest in mobile and browser exploitation, adapting and expanding their exploit chains to bypass more recently implemented security boundaries and other mobile security improvements. Multiple intrusions linked to BRICKSTORM malware deployment demonstrated a range of objectives, but the targeting of technology companies demonstrated the potential theft of valuable IP to further the development of zero-day exploits.  
  Key Takeaways  
 
  Complexity drives higher mobile vulnerability counts.  Mobile zero-day discovery counts fluctuated over the last three years, dropping from 17 in 2023 to 9 in 2024, before rebounding to 15 in 2025. As vendor mitigations evolve and increasingly prevent more simplistic exploitation, threat actors have been forced to expand or adjust their techniques. In some cases, attackers have increased the number of chained vulnerabilities to reach desired levels of access within highly protected components. Conversely, threat actors have also managed successful exploitation with fewer or singular bugs by targeting lower levels of access within a single capability, such as an application or service.  
  Enterprise software and edge devices remain prime targets.  Marking a new high, 48% of 2025’s zero-days targeted enterprise-grade technology. Increased exploitation of security and networking devices highlights the critical risk that can be posed by trusted edge infrastructure, while targeting of enterprise software exhibits the value of highly interconnected platforms that provide privileged access across networks and data assets. Networking and security appliances continued to be highly targeted, by a variety of threat actors, to gain initial access.  
  Commercial surveillance vendors (CSVs) further reduce barriers to zero-day access.   For the first time since we began tracking zero-day exploitation, we attributed more zero-days to CSVs than to traditional state-sponsored cyber espionage groups. This illustrates the expansion of access to zero-day exploitation via these vendors to a wider array of customers than ever before.  
  People’s Republic of China (PRC)-nexus cyber espionage groups continue to dominate traditional state-sponsored espionage zero-day exploitation.   Consistent with the trend we have observed for nearly a decade, in comparison to other state sponsors, PRC-nexus groups remained the most prolific users of zero-day vulnerabilities in 2025. These groups, such as UNC5221 and UNC3886, continued to focus heavily on security appliances and edge devices to maintain persistent access to strategic targets.  
  Zero-day exploitation by financially motivated threat groups ties previous high.   In 2025, we attributed the exploitation of 9 zero-days to confirmed or likely financially motivated threat groups. This nearly matches the total volume of 2023 and represents a higher proportion of all attributed vulnerabilities in 2025.   
 
  2026 Zero-Day Forecast  
  Targets and Techniques Continue to Expand  
  As certain vendors continue to drive improvements that have made vulnerability exploitation more difficult, particularly in the browser and mobile space, adversaries will continue to adapt with more expansive techniques and diverse targets. Enterprise exploitation will continue to be further enabled by the breadth of applications used across infrastructure. Increased numbers of software, devices, and applications expand attack surfaces, with successful exploitation requiring only a single point of failure to achieve a breach.  
  AI Changes the Game  
  We anticipate that AI will accelerate the ongoing race between attackers and defenders in 2026 creating a more dynamic threat environment. We expect adversaries will utilize AI to automate and scale attacks by accelerating reconnaissance, vulnerability discovery, and exploit development. Reducing the time required for these phases will place further pressure on defenders to better detect and respond to zero-day exploitation. At the same time, AI will empower defenders to harness tools like agentic solutions to enhance security operations. AI agents can proactively discover and help patch previously unknown security flaws, enabling vendors to neutralize vulnerabilities before exploitation.   
  Using Access for Research  
  A    BRICKSTORM malware campaign in 2025   , attributed to PRC-nexus espionage operators, may indicate a new paradigm for zero-day exploitation where data theft has the potential to enable long-term zero-day development. Instead of just exfiltrating sensitive client data, the threat actors targeted intellectual property from the victim companies, potentially including source code and proprietary development documents. This IP could be used to discover new vulnerabilities in the vendor's software, not only posing a threat to the victims themselves but also to victims’ downstream customers.  
  Scope  
  This report describes what Google Threat Intelligence Group (GTIG) knows about zero-day exploitation in 2025. GTIG defines a zero-day as a vulnerability that was maliciously exploited in the wild before a patch was made publicly available. The following analysis leverages original research conducted by GTIG combined with reliable open-source reporting, though we cannot independently confirm the reports of every source.   
  Research in this space is dynamic and the numbers may adjust due to the ongoing discovery of past incidents. Our analysis represents exploitation tracked by GTIG but may not reflect all zero-day exploitation. The numbers presented here reflect our best understanding of current data, and we note that all zero-days included in our 2025 dataset have patches available. GTIG acknowledges that the trends observed and discussed in this report are based on detected and disclosed zero-days, with a cutoff date of Dec. 31, 2025.   
  A Numerical Analysis   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 1: Zero-days by year  
      
     

  
       
     
  




 
   GTIG tracked 90 vulnerabilities that were disclosed in 2025 and exploited as zero-days. This number is consistent with a consolidating upward trend that we have observed over the last five years; the total annual volume of zero-days has fluctuated within a 60-100 range over this time period, but has remained elevated compared to pre-2021 levels. As certain categories of exploitation shift over time, whether due to vendor mitigations or newer high-value opportunities, total zero-day counts continue to appear within an expected range, rather than seeing drastic overall decreases or increases.  
  Enterprise Exploitation Expands Further in 2025   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 2: 2025 zero-days in end-user vs enterprise products  
      
     

  
       
     
  




 
   Enterprise Technologies  
  We identified 43 (48%) zero-days in enterprise software and appliances in 2025, up from 36 (46%) in 2024. This consistent proportion underscores the shift toward enterprise infrastructure as a structural change in the threat landscape, reflecting the value of tools that enable privilege escalation, high-level access, and broad scale of impact.  
 
  Security &amp; Networking:   These vulnerabilities made up about half (21) of the enterprise-related zero-days in 2025, remaining a prominent target for achieving code execution and unauthorized access via privileged infrastructure components. A lack of input validation and incomplete authorization processes were common flaws within these products, demonstrating how basic systemic failures continue to persist, but are fixable with proper implementation standards and approaches. Edge devices–often including security and networking devices–sit at the perimeter of an organization's infrastructure and remain high value targets  .   The absence of EDR technology on most edge devices, like routers, switches, and security appliances, can create a blind spot for defenders, making it an ideal attack surface. This limitation can hinder the ability to detect anomalies or gather host-based evidence once these devices are compromised. While 14 zero-days in 2025 were identified as affecting edge devices, this figure likely underrepresents the true scale of activity due to inhibited detection capabilities.  
  Enterprise Software:   High-profile exploitation of enterprise tools and virtualization technologies demonstrates that attackers are deeply embedding themselves in critical business infrastructure. Threat actors continue to pursue the most vulnerable and exposed assets to work around mitigations that may exist in specific areas of or products within an infrastructure.  
 
  End User Platforms and Products  
  In 2025, 52% (47) of the tracked zero-days were used to exploit end-user platforms and products.  
 
 
  Operating Systems (OSs):   OSs, including both desktop and mobile, were the most exploited product category in 2025, accounting for 44% (39) of all zero-days. This is a rise from previous years when comparing both raw numbers (31 in 2024, and 33 in 2023) and proportions of total zero-day exploitation (40% in 2024 and 33% in 2023). Desktop OS zero-days have fluctuated between 16 and 23 annually while maintaining a gradual upward trajectory, illustrating the foundational role of these platforms and the massive scale of effect permitted by OS-level exploitation.  
 
 
  Mobile Devices:   Mobile OS exploitation in particular saw a notable increase, with a total of 15 zero-days in 2025 compared to the 9 identified in 2024. Given that we observed 17 mobile-related zero-days in 2023, the following factors likely accounted for this temporary decline and the subsequent resurgence in activity:  
 
 
 
  Multiple exploit chains discovered in 2025 included three or more vulnerabilities, inflating the number of individual vulnerabilities required to achieve a single objective.  
 
 
  Threat researchers discovered more complete exploit chains in 2025 than have been found in the past, when sometimes only partial chains or a single vulnerability was identified and could be accounted for.  
 
 
  Threat actors, and CSVs in particular, have found    novel techniques    to bypass new security boundary implementations.  
 
 
 
  Browsers:   Browsers accounted for less than 10% of 2025 zero-day exploitation, a marked decrease from the browser-heavy years of 2021-2022. This suggests that browser hardening measures are working. However, we also assess that attackers’ operational security has improved and therefore made their actions more difficult to observe and track, potentially reducing the volume of observed exploitation in this space.  
 
 
  Exploitation by Vendor   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 3: 2025 zero-day exploitation by vendor  
      
     

  
       
     
  




 
   2025’s exploited vendors followed the same pattern we observed last year, with big tech experiencing the most zero-day exploitation and security vendors following directly behind. Big tech companies continue to dominate the user base for consumer products, making them prime targets for exploitation, particularly in    desktop OSs   ,    browsers    and    mobile systems   . Cisco and Fortinet remain commonly targeted networking and security vendors, while Ivanti and VMware continue to see exploitation that reflects the high value threat actors place on VPNs and virtualization platforms.  
  We observed 20 vendors who were exploited by just one zero-day each, further demonstrating threat actors’ success in targeting varying vendors and products to find successful footholds in desired targets.  
  Types of Exploited Vulnerabilities  
  As observed in prior years, zero-day exploitation was primarily used to achieve remote code execution, followed by gaining privilege escalation. These were especially common consequences in observed exploitation of big tech and security vendors. Both code execution and unauthorized access were common goals of network and edge infrastructure exploitation, displaying the advantage of exploiting high-privilege assets with widespread reach across systems and networks.  
  2025 saw an array of both structural design flaws and pervasive implementation issues, exemplifying the omnipresence of known, yet prolific, problems.   
 
  Injection &amp; Deserialization:   Command injection and deserialization were critical vectors in the enterprise space. These types of vulnerabilities often allow for reliable remote code execution (RCE) without the complexity of memory corruption exploits. SQL and command injection vulnerabilities were common in web-facing enterprise appliances, providing rudimentary avenues for initial access.  
  Memory Corruption  : Threat actors continued to rely on memory corruption, with memory safety issues (particularly use-after-free [UAF] and out-of-bounds write) accounting for roughly 35% of the vulnerabilities. UAF weaknesses remained a top vector for user-centered products like browsers and OS kernels.  
  Access Control:   The prevalence of authentication and authorization bypass vulnerabilities highlights the difficulty edge devices face in securing both the network perimeter and their own administrative interfaces.  
  Logic and Design Flaws:   Frequently exploited in enterprise appliances, these issues represent fundamental architectural weaknesses where the system’s intended logic or design is inherently insecure. Because the software is behaving as designed, these flaws are harder for vendors to detect.  
 
  Who Is Driving Exploitation   
 






  
     
       
  

     

      
      
        
         
        
         
      
          Figure 4: Attributed 2025 zero-day exploitation  
      
     

  
       
     
  




 
   Commercial Surveillance Vendor Exploitation Grows  
  For the first time since we started tracking zero-day exploitation, we attributed more exploitation to CSVs than to traditional state-sponsored cyber espionage groups. Despite these actors’ increased focus on operational security that likely hinders discovery, this continues to reflect a trend we began to observe over the last several years–a growing proportion of zero-day exploitation is conducted by CSVs and/or their customers, demonstrating a slow but sure movement in the landscape. Historically, traditional state-sponsored cyber espionage groups have been the most prolific attributed users of zero-day vulnerabilities. Over the last few years, the increase of zero-day exploitation attributed to CSVs and their customers has demonstrated the growing ability of these vendors to provide zero-day access to a wider range of threat actors than ever before.   
  GTIG has reported    extensively    on the capabilities CSVs provide their clients as well as how many CSV customers use zero-day exploits in attacks which erode civil liberties and human rights. In late 2025, we    reported    on how Intellexa, a prolific procurer and user of zero-days, adapted its operations and tool suite and continues to deliver extremely capable spyware to high paying customers.   
  People’s Republic of China (PRC)-Nexus Cyber Espionage Groups Still Most Prolific   
  Although the proportion of 2025 zero-day exploitation that we attributed to traditional state-sponsored cyber espionage groups was lower than in previous years, these groups remained significant developers and users of zero-day exploits in 2025. Consistent with the trend we have observed for nearly a decade, PRC-nexus cyber espionage groups remained the most prolific users of zero-days across state actors in 2025. We attributed the use of at least 10 zero-days to assessed PRC-nexus cyber espionage groups. This was double what we attributed to these groups in 2024, but below the 12 zero-days we attributed in 2023. PRC-nexus espionage zero-day exploitation continued to focus on edge and networking devices that are difficult to monitor, allowing them to maintain long-term footholds in strategic networks. Examples of this include the exploitation of    CVE-2025-21590 by UNC3886    and the exploitation of    CVE-2025-0282 by UNC5221   .  
  Observed mass exploitation of vulnerabilities suggests that PRC-nexus espionage operators are increasingly adept at developing, sharing, and distributing exploits among themselves. Historically, zero-day exploits were closely held and leveraged only by the most resourced threat groups. Over time, however, we have observed that an increasing number of activity clusters are exploiting vulnerabilities closer to public disclosure, indicating that PRC-nexus espionage operators have potentially reduced the time to both develop exploits and distribute them among otherwise separate groups. This is reflected not only in the gradual proliferation of exploit code targeting specific vulnerabilities, but also by the shrinking gap between the public disclosure of n-day vulnerabilities and their widespread exploitation by multiple groups.   
  In sharp contrast to 2024, during which we attributed the exploitation of five zero-days to North Korean state-sponsored threat actors, we did not attribute any zero-days to North Korean groups in 2025.  
  Financially Motivated Exploitation Spikes  
  We tracked the exploitation in 2025 of nine zero-days by likely or confirmed financially motivated threat groups, including the reported exploitation of two zero-days in operations that led to ransomware deployment. This almost ties the previous high of 10 zero-days we attributed to financially motivated groups in 2023 and is nearly double the five zero-days we attributed to financially motivated actors in 2024. Although the total volume of zero-day exploitation we have attributed to financially motivated groups has varied year over year, the sustained presence of these threat actors in the zero-day landscape reflects their continued investment in zero-day exploit development and deployment. Financially motivated actors, including ransomware affiliates, were linked to a substantial number of enterprise exploits, reflecting a trend we observed across multiple motivations.  
 
   We observed zero-day exploitation by FIN11 or associated clusters in four of the last five years–2021, 2023, 2024, and 2025. In late September 2025, GTIG began tracking a new, large-scale extortion campaign by a threat actor claiming affiliation with the CL0P extortion brand, which has predominantly been used by FIN11. The actor sent a high volume of emails to executives at numerous organizations, alleging the theft of sensitive data from the victims' Oracle E-Business Suite (EBS) environments.    Our analysis    indicated that the CL0P extortion campaign followed months of intrusion activity targeting EBS customer environments. The threat actor exploited CVE-2025-61882 and/or CVE-2025-61884 as a zero-day against Oracle EBS customers as early as Aug. 9, 2025, weeks before a patch was available, with additional suspicious activity dating back to July 10, 2025.   
    GTIG identified UNC2165, a financially motivated group that overlaps with public reporting on Evil Corp and has prominent members in Russia, leveraging    CVE-2025-8088    to distribute malware in mid-July 2025. This activity marked the first instance where we observed UNC2165 use a zero-day for initial access. Additional evidence from underground activity and VirusTotal RAR archive submissions indicate that CVE-2025-8088 was also exploited during this same period by other actors, including a threat cluster with suspected overlaps with CIGAR/UNC4895 (publicly reported as RomCom). UNC4895 is another Russian threat group that has conducted both financially motivated and espionage operations, including the exploitation of two other zero-days in 2024.    
 
  Spotlights: Notable Threat Actor Activity and Techniques  
  Browser Sandbox Escapes  
  The discovery of various browser sandbox escapes in 2025 provided an opportunity to evaluate current trends and developments in this area. Analysis of those identified this year revealed a significant trend: none were generic to the browser sandbox itself (e.g., CVE-2021-37973,    CVE-2023-6345   , CVE-2023-2136); instead, these sandbox escapes were specifically designed to exploit components of either the underlying operating system or hardware used. This section gives a brief technical overview of these vulnerabilities.  
  Operating System-Based Sandbox Escapes  
   CVE-2025-2783    targeted the Chrome sandbox on Windows. The vulnerability was caused by the improper handling of sentinel OS handles (-2) that weren’t properly validated. By manipulating inter-process communication (IPC) messages via the ipcz framework,    an attacker    could relay these special handles back to a renderer process. The exploit allowed a compromised renderer to gain access to handles, leading to code injection within more privileged processes and ultimately to a sandbox escape.  
  CVE-2025-48543 affected the Android Runtime (ART), the system that translates application bytecode into native machine instructions to improve execution speed and power efficiency. A UAF vulnerability occurred during the deserialization of Java objects, such as abstract classes, that should not be instantiable in the first place. The most notable aspect of the exploit is how the bug can be reached from a compromised Chrome renderer. On recent Android versions, the exploit sent a Binder transaction to deliver a serialized payload embedded into a Notification Parcel object. The subsequent    unparceling    of the malicious object caused a UAF in ART, leading to arbitrary code execution within system_server, a service that operates with system-level privileges. While this specific vulnerability class and attack vector may be new publicly, we have observed    Parcel mismatch    n-day vulnerabilities being exploited to achieve Chrome sandbox escapes using the same attack vector in the past.  
  Device-Specific Sandbox Escapes  
  CVE-2025-27038 is a UAF vulnerability in the Qualcomm Adreno GPU user-land library that can be triggered through a sequence of WebGL commands followed by a specifically crafted glFenceSync call. The vulnerability allows attackers to achieve code execution within the Chrome GPU process on Android devices. We observed in-the-wild exploitation of this vulnerability in a chain with vulnerabilities in the Chrome renderer (CVE-2024-0519) and the KGSL driver (CVE-2023-33106).  
  In a similar instance, CVE-2025-6558 targeted the Mali GPU user-land library. This vulnerability was triggered by a sequence of OpenGLES calls that were not properly validated by the browser. Specifically, an out-of-bounds write was caused within the user-land driver due to the issuance of glBufferData() with the GL_TRANSFORM_FEEDBACK_BUFFER parameter while a previous glBeginTransformFeedback() operation remained active. Google addressed this issue in ANGLE by    implementing    validation to invalidate this specific call sequence. We observed in-the-wild exploitation of this vulnerability in a chain with vulnerabilities in the Chrome renderer (CVE-2025-5419) and in the Linux kernel's posix CPU timers implementation (CVE-2025-38352).  
  Additionally, CVE-2025-14174 is a vulnerability that affected the Metal backend on Apple devices. In that case, ANGLE incorrectly communicated a buffer size during the implementation of texImage2D operation, resulting in an out-of-bounds memory access within the Metal GPU user-mode driver.  
  SonicWall Full-Chain Exploit  
  In late 2025, GTIG collected a multi-stage exploit for SonicWall Secure Mobile Access (SMA) 1000 series appliances. The exploit chain leveraged multiple vulnerabilities to provide either authenticated or unauthenticated remote code execution as   root   on a targeted appliance, including one that was being leveraged as zero-day.  
  Authentication Bypass (n-day)  
  The exploit can be leveraged with or without an authenticated   JSESSIONID   session token. When executed without a token, the exploit attempts to get one for the built-in   admin   user by exploiting a weakness in SSO token generation within the Central Management Server feature in SMA 1000.  
  This vulnerability was    patched    as a part of CVE-2025-23006. It was reported to SonicWall by Microsoft Threat Intelligence Center (MSTIC), and was reportedly exploited in the wild prior to it being patched in January 2025. GTIG is currently unable to assess if prior exploitation of this vulnerability is linked to use of this new exploit chain.  
  Remote Code Execution (n-day)  
  Once the exploit has a valid session cookie for the target, it attempts to attain remote code execution through a deserialization vulnerability, where an object is serialized and encoded with Base64, and then passed between the web application client and the appliance server without any integrity checks. This allows an attacker to forge a malicious Java object and send it to the server, which parses the object and causes arbitrary Java bytecode to be executed. The exploit leverages this primitive to run arbitrary shell commands using a payload generated by    ysoserial   , a common tool used to assist with exploiting Java serialization-related vulnerabilities.  
  This vulnerability was patched by encrypting objects with AES-256-ECB prior to sending them to the client, using an ephemeral key generated randomly at server startup and stored in-memory. Payloads mutated without knowledge of the key won't be successfully parsed, which mitigates the risk of deserializing untrusted objects without another vulnerability leaking the encryption key. The patch was silently released in March 2024 without a CVE.  
  Local Privilege Escalation (0-day)  
  After exploiting the aforementioned deserialization vulnerability, the exploit is able to execute arbitrary shell commands as the   mgmt-server   user, which runs the Java process hosting the management web application. To escalate to root privileges, the exploit used a zero-day in   ctrl-service  , a custom XML-RPC service written in Python and bound to a loopback address on port 8081. This makes it inaccessible directly to a remote attacker, but accessible after already gaining code execution on the device at a lower privilege level. While this vulnerability could be exploited when combined with a newly discovered RCE vulnerability, or with direct console/SSH access to the appliance, we've presently only observed it being chained with the RCE exploit previously discussed.  
  GTIG reported this vulnerability to SonicWall, who published a    patch    for it in December 2025 as CVE-2025-40602. To fix this vulnerability, SonicWall added signature verification to the service to prevent it from executing unsigned files.  
  DNG Vulnerabilities  
  This section specifically examines samples exploiting CVE-2025-21042, a vulnerability for which GTIG has not confirmed zero-day exploitation; however, we include this discussion of the underlying exploitation techniques because zero-days CVE-2025-21043 and CVE-2025-43300 share identical exploitation conditions.  
  Between July 2024 and February 2025, several suspicious image files were uploaded to VirusTotal. Thanks to a lead from Meta, these samples came to the attention of Google Threat Intelligence Group. Upon investigation of these images, we discovered that they were digital negative (DNG) images targeting the Quram library, an image parsing library specific to Samsung devices.    
  The VirusTotal submission filenames of several of these exploits indicated that these images were received over WhatsApp. The final payload, however, indicated that the exploit expects to run within the   com.samsung.ipservice   process. This is a Samsung-specific system service responsible for providing “intelligent” or AI-powered features to other Samsung applications, and will periodically scan and parse images and videos in Android’s MediaStore.  
  When WhatsApp receives and downloads an image, it will insert the image in MediaStore. This permits downloaded WhatsApp images (and videos) to hit the image parsing attack surface within the   com.samsung.ipservice   application. However, WhatsApp does not intend to automatically download images from untrusted contacts. Without additional bypasses, and assuming the image is sent by an untrusted contact, a target would have to click the image to trigger the download and have it added to the MediaStore. This classifies as a “1-click” exploit. GTIG does not have any knowledge or evidence of the attacker using such a bypass to achieve 0-click exploitation.  
  com.samsung.ipservice   comes with a proprietary image parsing library named “Quram,” which is written in C++. The image parsing is done in-process, unsandboxed with respect to the service’s privilege. This breaks the    Rule Of 2    and means a single memory corruption vulnerability can grant attackers access to everything to which   com.samsung.ipservice   has access, i.e. a phone’s entire MediaStore.  
  This is exactly what the attackers did when they discovered a powerful memory corruption vulnerability (CVE-2025-21042), which allows controlled out-of-bounds write at controlled offsets from a heap buffer. With this single vulnerability, they were able to obtain code execution within the   com.samsung.ipservice   process and execute a payload with that process’ privileges.  
  There were no significant hurdles for the attackers aside from some ASLR bypassing tricks. No control flow integrity mitigations, like pointer authentication code (PAC) or branch target identification (BTI), are compiled into the Quram library. This allowed the attackers to use arbitrary addresses as jump-oriented programming (JOP) gadgets and construct a bogus vtable. The scudo allocator also failed to engage proper hardening techniques. The heap spraying primitives - more or less inherent to the DNG format - are powerful and allow for a predictable heap layout, even with scudo’s randomization strategy. The absence of scudo’s “quarantine” feature on Android is also convenient for deterministically reclaiming a free’d allocation.  
  This case illustrates how certain image formats can provide strong primitives out of the box for turning a single memory corruption bug into 0-click ASLR bypasses and resulting remote code execution. By corrupting the bounds of the pixel buffer using CVE-2025-21042, subsequent exploitation can occur by taking advantage of the DNG specification and its implementation.  
  The bug exploited in this case is both powerful and quite shallow. As    Project Zero’s Reporting Transparency    illustrates, several other vulnerabilities in the same component have been discovered over the recent months.  
  These types of exploits do not need to be part of long and complex exploit chains to achieve something useful for attackers. By finding ways to reach the right attack surface with a single relevant vulnerability, attackers are able to access all the images and videos of an Android’s MediaStore, posing a powerful capability for surveillance vendors.  
     A more detailed technical analysis of the exploit can be found on    Project Zero’s blog   .      
   Prioritizing Defenses and Mitigating Zero-Day Threats  
  Defenders should prepare for   when, not if,   a compromise happens.    GTIG continues to observe vulnerability exploitation as the number one initial access vector in Mandiant incident response investigations   , outnumbering other vectors like stolen credentials and phishing. System architectures should be designed and built with ingrained security awareness, enabling inherent segmentation and least privilege access. Comprehensive defensive measures as well as response efforts require a real-time inventory of all assets to be audited and maintained. While not preventative, continuous monitoring and anomaly detection, within both systems and networks, paired with refined and actionable alerting capabilities is a real-time way to detect and act against threats as they occur.   
  The following is a non-comprehensive set of approaches and guidelines for defending against zero-day exploitation on both personal devices and within organizational infrastructure:  
  1. Architectural Hardening &amp; Surface Reduction  
 
 
 
 
  Infrastructure:  
 
 
  Ensure your DMZ, firewalls, and VPNs are properly segmented from critical assets, including the core network and domain controllers, in order to prevent lateral movement from compromised external components.  
 
 
  Monitor execution flow within applications in order to block unauthorized database queries and shell commands  
 
 
  Do not expose network ports of devices to the internet when not strictly required  
 
 
 
 
  Personal devices:  
 
 
  Turn off the device and/or leave the device at home when under increased risk of exploitation.  
 
 
  Put the device in before first unlock (BFU) mode and USB restricted mode when under increased risk of physical attacks.  
 
 
  Turn off cellular, WiFi and bluetooth when under increased risk of close proximity attacks.  
 
 
  Apply patches as soon as they become available.  
 
 
  Use ad blockers, configure Apple ad privacy settings, and enable the Android privacy sandbox options when possible.  
 
 
  Enable Android Advanced Protection Mode and iOS Lockdown Mode.  
 
 
  Remove applications, and disable services and features- including ones enabled by default- when not used.  
 
 
 
 
 
 
  2. Advanced Detection &amp; Behavioral Monitoring  
 
 
 
 
  Infrastructure:  
 
 
  Enforce strict driver blocklists and flag anomalous kernel-level behavior that traditional EDR might overlook.  
 
 
  Establish a baseline for system processes in order to be able to flag "Living off the Land" (LotL) activity and other persistence mechanisms.  
 
 
  Deploy canary tokens and files to collect high-fidelity alerts of lateral movement.  
 
 
 
 
  Personal devices:  
 
 
  Seek expert advice (e.g., Amnesty, CitizenLab, and Access Now) when receiving suspicious links or attachments, as well as when observing suspicious application and or operating system crashes.  
 
 
  Enroll in    Google’s Advanced Protection Program   .  
 
 
  Enable    Android Advanced Protection Mode   .  
 
 
  Enable    Enhanced Safe Browsing in Chrome   .  
 
 
  Enable    Safari fraudulent website warning   .  
 
 
  Enable    Edge enhanced security protections   .  
 
 
 
 
 
 
  3. Operational Response  
 
 
 
 
  Infrastructure:  
 
 
  Maintain a Software Bill of Materials (SBoM) to reference and locate affected libraries of disclosed zero-days (e.g., Log4j) across the environment.  
 
 
  Establish a process for bypassing standard change management when vulnerabilities require immediate attention.  
 
 
  If a patch is unavailable, isolate systems and components with stop-gap measures such as disabling specific services or blocking specific ports at the perimeter.  
 
 
 
 
  Personal devices:  
 
 
  Reboot phone regularly.  
 
 
  Do not click on links or download attachments from unknown contacts.  
 
 
 
 
 
 
  Prioritization is a consistent struggle for most organizations due to limited resources requiring deciding what solutions are implemented–and for every choice of where to put resources, a different security need is neglected. Know your threats and your attack surface in order to prioritize decisions for best defending your systems and infrastructure.
