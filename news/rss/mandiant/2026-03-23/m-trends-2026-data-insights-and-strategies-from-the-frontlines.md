---
source: rss/mandiant
title: M-Trends 2026: Data, Insights, and Strategies From the Frontlines
url: https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026/
date: 2026-03-23
item_id: https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026/
category: news
tags: [Bypass, Exploit, Injection]
---

**Source:** Mandiant
**Link:** https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026/

Every year, the cyber threat landscape forces defenders to adapt to evolving adversary tactics, techniques, and procedures (TTPs). In 2025, Mandiant observed a clear divergence in adversary pacing that closely aligns with the trends we have been    documenting for defenders    over the past year. On one end of the spectrum, cyber criminal groups optimized for immediate impact and deliberate recovery denial. On the other end, sophisticated cyber espionage groups and insider threats optimized for extreme persistence, utilizing unmonitored edge devices and native network functionalities to evade detection.  
  Today, we release M-Trends 2026. Grounded in over 500,000 hours of frontline incident investigations conducted by Mandiant globally in 2025, this report provides a definitive look at the TTPs actively being used in breaches today.   
  
     aside_block 
     &lt;ListValue: [StructValue([(&#x27;title&#x27;, &#x27;M-Trends 2026 is available!&#x27;), (&#x27;body&#x27;, &lt;wagtail.rich_text.RichText object at 0x7fa60f696130&gt;), (&#x27;btn_text&#x27;, &#x27;Download now&#x27;), (&#x27;href&#x27;, &#x27;https://cloud.google.com/security/resources/m-trends?utm_source=cgc-blog&amp;utm_medium=blog&amp;utm_campaign=FY26-Q1-GLOBAL-STO89-website-dl-dgcsm-mtrends26-162712&amp;utm_content=-&amp;utm_term=-&#x27;), (&#x27;image&#x27;, &lt;GAEImage: m-trends blog callout&gt;)])]&gt; 
  
   By the Numbers: M-Trends 2026  
  The metrics in this year's report highlight how adversaries are shifting their approaches to bypass modern security controls:  
 
 
  Global Median Dwell Time:   Global median dwell time rose to 14 days from 11 days. This shift likely reflects growing sophistication, particularly in evading defenses. When looking specifically at the high quantity of cyber espionage and North Korean IT worker incidents, the median dwell time for both categories was 122 days.  
 
 
  Initial Infection Vectors:   Exploits remained the most common initial infection vector for the sixth consecutive year, accounting for 32% of intrusions. However, highly interactive voice phishing saw a significant surge to 11%, becoming the second-most commonly observed vector.  
 
 
  Detection by Source:   Organizations are improving their internal visibility. Across all 2025 investigations, 52% of the time organizations first detected evidence of malicious activity internally, an increase from 43% in 2024.  
 
 
  Targeted Industries:   The   full scope of incidents affected more than 16 industry verticals, with   the high tech sector (17%) outpacing the financial sector (14.6%) as the most frequently targeted industry, shifting the financial sector out of the top spot it held in 2024 and 2023.  
 
 
  The Collapse of the "Hand-Off" Window  
  One of the most notable trends we observed in 2025 is the increased specialization and collaboration within the cyber crime ecosystem. Initial access partners are using low-impact techniques, such as malicious advertisements or the ClickFix social engineering technique, to gain a foothold. They then hand off this access to secondary groups who execute high-impact operations like ransomware.  
  In 2022, the median time between an initial access event and the hand-off to a secondary threat group was more than 8 hours. In 2025, that window collapsed to just 22 seconds. Initial access partners are increasingly pre-staging the secondary group's preferred malware or tunnels during the initial infection, meaning secondary actors are fully equipped to launch operations the moment they first interact with the network.  
  This pattern is reflected in how attackers are breaching organizations. We found that prior compromise ranked as the third-most common initial infection vector (10%) for intrusions globally, and the top initial infection vector in ransomware operations (30%), doubling what it was in 2024 (15%).  
  Voice Phishing and the SaaS Identity Crisis  
  Historically, email phishing has been an adversary staple. But as automated technical controls have improved, email phishing dropped to just 6% of intrusions in 2025. In its place, adversaries have pivoted to highly interactive, voice-based social engineering.  
  We have extensively documented this progression in blog posts and reports, notably tracking how groups like UNC3944 target IT help desks to bypass multifactor authentication (MFA) and gain initial access to software-as-a-service (SaaS) environments (see:    Vishing for Access: Tracking the Expansion of ShinyHunters-Branded SaaS Data Theft   ).  
  M-Trends 2026 reveals the cascading impact of these techniques. Threat actors are bypassing standard defenses by harvesting long-lived OAuth tokens and session cookies. By compromising third-party SaaS vendors, attackers steal hard-coded keys and personal access tokens, using those secrets to seamlessly pivot into downstream customer environments to execute large-scale data theft.  
  Ransomware Evolves into Recovery Denial  
  Ransomware groups are no longer just encrypting data; they are actively destroying the ability to recover. In 2025, we observed a    systemic shift where ransomware operators   , including prolific groups using REDBIKE (Akira) and AGENDA (Qilin), actively targeted backup infrastructure, identity services, and virtualization management planes.  
  Attackers are exploiting misconfigured Active Directory Certificate Services templates to create admin accounts that bypass password rotation and are actively deleting backup objects from cloud storage. Furthermore, attackers are exploiting the "Tier-0" nature of hypervisors to bypass guest-level defenses. By targeting the virtualization storage layer directly or encrypting hypervisor datastores, they can render all associated virtual machines inoperable simultaneously.  
  This directly aligns with the complex intrusions we outlined in our guide,    From Help Desk to Hypervisor: Defending Your VMware vSphere Estate from UNC3944   . Modern ransomware is now a fundamental resilience problem, forcing organizations into a choice: pay or rebuild.  
  Edge Devices, Zero-Days, and Extreme Persistence  
  While cyber criminals optimize for speed, espionage groups are optimizing for extreme persistence. Threat clusters like UNC6201 and UNC5807 deliberately target edge and core network devices, such as virtual private networks (VPNs) and routers, that typically lack standard endpoint detection and response (EDR) telemetry. M-Trends 2026 reveals that the mean time to exploit vulnerabilities dropped to an estimated -7 days, meaning exploitation is routinely occurring before a patch is even released. This acceleration underscores the severity of the trends and campaigns we have recently documented, from increasing zero-day usage over 2024 (as reported on in    Look at What You Made Us Patch: 2025 Zero-Days in Review2025 Zero-Days in Review   ) to our analysis of    UNC6201 Exploiting a Dell RecoverPoint for Virtual Machines Zero-Day   . By leveraging native packet-capturing functionality on these devices, adversaries can directly intercept sensitive data and plaintext credentials as they transit the network, allowing them to gather intelligence without ever needing to move deeper into traditional sources like workstations or servers.  
  Attackers are deploying custom, in-memory malware like the    BRICKSTORM    backdoor directly onto these network appliances to establish deep persistence that routinely survives standard remediation efforts and system reboots. Because these devices are designed with minimal onboard storage and cannot support traditional security tooling, conducting file system or memory forensics presents a significant challenge, often leaving security teams with limited artifacts to confirm an attacker's presence or properly scope the remediation. Furthermore, this extreme persistence creates a critical visibility gap. With threats like BRICKSTORM achieving dwell times of nearly 400 days, standard 90-day log retention policies leave organizations completely blind to the initial access vector and the full scope of the intrusion.  
  AI Threat Landscape  
  A comprehensive overview of the 2025 threat landscape requires addressing adversary use of artificial intelligence (AI). Ongoing Google Threat Intelligence Group research reveals that adversaries are    integrating AI to accelerate the attack lifecycle   . We have seen malware families like PROMPTFLUX and PROMPTSTEAL actively query large language models (LLMs) mid-execution to evade detection, while "distillation attacks" threaten intellectual property by extracting the proprietary logic and specialized training data of high-value machine learning models. M-Trends 2026 confirms attackers are abusing AI within compromised environments. For example, the QUIETVAULT credential stealer was observed checking targeted machines for local AI command-line tools, executing predefined prompts to search for configuration files.   
  Despite these rapid technological advancements, we do not consider 2025 to be the year where breaches were the direct result of AI. From our view on the frontlines, the vast majority of successful intrusions still stem from fundamental human and systemic failures. However, to ensure organizations are prepared as AI-powered capabilities evolve, Mandiant red teams are actively incorporating AI-driven techniques into engagements—such as prompt injection—to rigorously test defenses against emerging threats. By highlighting the unique risks surrounding AI implementations, such as the abuse of developer toolchains, we help organizations establish behavioral baselines and adopt principles from the    Google Secure AI Framework (SAIF)   . Beyond securing the AI models themselves, we also help organizations leverage AI-powered defense as a force multiplier for security operations. For a deeper dive into AI and security, read our recently published paper,    AI risk and resilience: A Mandiant special report   .  
  Recommendations for Defenders  
  To build true operational resilience and outmaneuver modern adversaries, organizations must move at the speed of the attacker. M-Trends 2026 provides extensive, actionable guidance, including:  
 
 
  Treat Low-Impact Alerts as Critical Indicators:   With hand-off times shrinking to seconds, security teams must restructure response playbooks. Treat routine malware alerts as high-priority indicators of an impending secondary intrusion, and remediate before interactive hands-on-keyboard operations begin.  
 
 
  Isolate Critical Control Planes:   Virtualization and management platforms must be treated as Tier-0 assets with the strictest access constraints. To counter the destruction of recovery capabilities, backup environments should be decoupled from the corporate Active Directory domain and utilize immutable storage (to defend against these attacks, review our guide,    Proactive Preparation and Hardening Against Destructive Attacks: 2026 Edition   ).  
 
 
  Shift to Continuous Identity Verification:   Because interactive social engineering frequently bypasses traditional MFA, organizations must enforce strict least privilege, regularly audit SaaS integrations, and route all SaaS applications through a central identity provider (IdP).  
 
 
  Transition from Static IOCs to Behavioral Anomaly Detection:   With attackers rapidly changing infrastructure and deploying custom, in-memory malware, relying solely on static indicators of compromise (IOCs) is no longer sufficient. Defenders must implement behavior-based detection models that flag anomalous activity and deviations from established baselines, specifically concerning unauthorized access to edge devices, anomalous bulk API operations, or the suspicious use of SaaS integration tokens.  
 
 
  Expand Visibility and Extend Log Retention:   Deploy advanced threat detection across the entire ecosystem. To close the visibility gap associated with multi-year intrusions, organizations must extend log retention policies well beyond standard 90-day windows. Forward critical network device logs—especially application and administrative logs—and hypervisor-level telemetry to centralized, long-term storage to eliminate the blind spots sophisticated actors rely upon.  
 
 
  Be Ready to Respond  
  The Mandiant mission is to help keep every organization secure from cyber threats and confident in their readiness. For 17 years, our annual M-Trends report has been a core component of advancing that mission, sharing frontline knowledge to help defenders close critical visibility gaps.  
  To learn about the cyber threat landscape, and how we recommend organizations adapt to its ongoing changes, explore our M-Trends 2026 resources:  
 
 
   Download the M-Trends 2026 report    for a comprehensive dive into our frontline data.  
 
 
  Read the    M-Trends 2026 Executive Edition    for a high-level look at the data and trends, along with key recommendations.  
 
 
  Register for our upcoming    M-Trends 2026 webinar   —the first in a planned series—for an in-depth look at the data, topics, and recommendations discussed in the report.  
 
 
  Listen to a special episode of the    Google Cloud Security Podcast featuring M-Trends 2026    to learn more about what the findings mean and how the report is created.
