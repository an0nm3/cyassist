---
source: rss/google-online-security
title: Advancing Protection in Chrome on Android
url: http://security.googleblog.com/2025/07/advancing-protection-in-chrome-on.html
date: 2025-07-08
item_id: http://security.googleblog.com/2025/07/advancing-protection-in-chrome-on.html
category: news
tags: [Exploit]
---

**Source:** Google Online Security
**Link:** http://security.googleblog.com/2025/07/advancing-protection-in-chrome-on.html

Posted by David Adrian, Javier Castro &amp; Peter Kotwicz, Chrome Security Team 

 
Android recently announced  Advanced Protection , which extends Google’s  Advanced Protection Program  to a device-level security setting for Android users that need heightened security—such as journalists, elected officials, and public figures. Advanced Protection gives you the ability to activate Google’s strongest security for mobile devices, providing greater peace of mind that you’re better protected against the most sophisticated threats.
 
 
Advanced Protection acts as a single control point for at-risk users on Android that enables important security settings across applications, including many of your favorite Google apps, including Chrome. In this post, we’d like to do a deep dive into the Chrome features that are integrated with Advanced Protection, and how enterprises and users outside of Advanced Protection can leverage them.
 
 
Android Advanced Protection integrates with Chrome on Android in three main ways:
 
 

  Enables the “Always Use Secure Connections”  setting for both public and private sites, so that users are protected from attackers reading confidential data or injecting malicious content into insecure plaintext HTTP connections. Insecure HTTP represents less than 1% of page loads for Chrome on Android.  

  Enables full Site Isolation  on mobile devices   with 4GB+ RAM, so that potentially malicious sites are never loaded in the same process as legitimate websites. Desktop Chrome clients already have full Site Isolation. 

  Reduces attack surface  by disabling Javascript optimizations, so that Chrome has a smaller attack surface and is harder to exploit. 
 
 
Let’s take a look at all three, learn what they do, and how they can be controlled outside of Advanced Protection.
 
 Always Use Secure Connections 


 
“Always Use Secure Connections” (also known as HTTPS-First Mode in blog posts and HTTPS-Only Mode in the enterprise policy) is a Chrome setting that forces HTTPS wherever possible, and asks for explicit permission from you before connecting to a site insecurely. There may be attackers attempting to interpose on connections on any network, whether that network is a coffee shop, airport, or an Internet backbone. This setting protects users from these attackers reading confidential data and injecting malicious content into otherwise innocuous webpages. This is particularly useful for Advanced Protection users, since in 2023, plaintext HTTP was  used as an exploitation vector during the Egyptian election .
 
 
Beyond Advanced Protection, we  previously posted  about how our goal is to eventually enable “Always Use Secure Connections” by default for all Chrome users. As we work towards this goal, in the last two years we have quietly been enabling it in more places beyond Advanced Protection, to help protect more users in risky situations, while limiting the number of warnings users might click through:
 
 

 We added a new variant of the setting that only warns on public sites, and doesn’t warn on local networks or single-label hostnames (e.g.  192.168.0.1 ,  shortlink/ ,  10.0.0.1 ). These names often cannot be issued a publicly-trusted HTTPS certificate. This variant protects against most threats—accessing a public website insecurely—but still allows for users to access local sites, which may be on a more trusted network, without seeing a warning.  

 We’ve automatically enabled “Always Use Secure Connections” for public sites in Incognito Mode for the last year, since Chrome 127 in June 2024. 

 We automatically prevent downgrades from HTTPS to plaintext HTTP on sites that Chrome knows you typically access over HTTPS (a heuristic version of the  HSTS header ), since Chrome 133 in January 2025.         Always Use Secure Connections has two modes—warn on insecure public sites, and warn on any insecure site. 
 
Any user can enable “Always Use Secure Connections” in the Chrome Privacy and Security settings, regardless of if they’re using Advanced Protection. Users can choose if they would like to warn on  any  insecure site, or only insecure public sites. Enterprises can opt their fleet into either mode, and set exceptions using the   HTTPSOnlyMode   and   HTTPAllowlist   policies, respectively. Website operators should protect their users' confidentiality, ensure their content is delivered exactly as they intended, and avoid warnings, by deploying HTTPS.   Full Site Isolation   Site Isolation  is a security feature in Chrome that isolates each website into its own rendering OS process. This means that different websites, even if loaded in a single tab of the same browser window, are kept completely separate from each other in memory. This isolation prevents a malicious website from accessing data or code from another website, even if that malicious website manages to exploit a vulnerability in Chrome’s renderer—a second bug to escape the renderer sandbox is required to access other sites. Site isolation improves security, but requires extra memory to have one process per site. Chrome Desktop isolates all sites by default. However, Android is particularly sensitive to memory usage, so for mobile Android form factors, when Advanced Protection is off, Chrome will only isolate a site if a user logs into that site, or if the user submits a form on that site. On Android devices with 4GB+ RAM in Advanced Protection (and on all desktop clients), Chrome will isolate  all  sites. Full Site Isolation significantly reduces the risk of cross-site data leakage for Advanced Protection users.
  JavaScript Optimizations and Security  
Advanced Protection reduces the attack surface of Chrome by disabling the higher-level optimizing Javascript compilers inside V8. V8 is Chrome’s high-performance Javascript and  WebAssembly  engine. The optimizing compilers in V8 make certain websites run faster, however they historically also have been a source of known exploitation of Chrome. Of all the patched security bugs in V8 with known exploitation, disabling the optimizers would have mitigated ~50%. However, the optimizers are why Chrome scores the highest on industry-wide benchmarks such as  Speedometer . Disabling the optimizers blocks a large class of exploits, at the cost of causing performance issues for some websites.
  
Javascript optimizers can be disabled outside of Advanced Protection Mode via the “Javascript optimization &amp; security” Site Setting. The Site Setting also enables users to disable/enable Javascript optimizers on a per-site basis. Disabling these optimizing compilers is not limited to Advanced Protection. Since Chrome 133, we’ve exposed this as a Site Setting that allows users to enable or disable the higher-level optimizing compilers on a per-site basis, as well as change the default.
        Settings -&gt; Privacy and Security -&gt; Javascript optimization and security 
  
This setting can be controlled by the   DefaultJavaScriptOptimizerSetting    enterprise policy, alongside   JavaScriptOptimizerAllowedForSites   and   JavaScriptOptimizerBlockedForSites   for managing the allowlist and denylist. Enterprises can use this policy to block access to the optimizer, while still allowlisting  1   the SaaS vendors their employees use on a daily basis. It’s available on Android and desktop platforms

  
Chrome aims for the default configuration to be secure for all its users, and we’re continuing to raise the bar for V8 security in the default configuration by  rolling out the V8 sandbox . 
  Protecting All Users  
Billions of people use Chrome and Android, and not all of them have the same risk profile. Less sophisticated attacks by commodity malware can be very lucrative for attackers when done at scale, but so can sophisticated attacks on targeted users. This means that we cannot expect the security tradeoffs we make for the default configuration of Chrome to be suitable for everyone. 
  
Advanced Protection, and the security settings associated with it, are a way for users with varying risk profiles to tailor Chrome to their security needs, either as an individual at-risk user. Enterprises with a fleet of managed Chrome installations can also enable the underlying settings now. Advanced Protection is available on Android 16 in Chrome 137+. 
  
We additionally recommend at-risk users join the  Advanced Protection Program with their Google accounts , which will require the account to use phishing-resistant multi-factor authentication methods and enable Advanced Protection on any of the user’s Android devices. We also recommend users enable automatic updates and always keep their Android phones and web browsers up to date.
  

 Notes     
     Allowlisting only works on platforms capable of full site isolation—any desktop platform and Android devices with 2GB+ RAM. This is because internally allowlisting is dependent on  origin isolation .&nbsp; ↩
