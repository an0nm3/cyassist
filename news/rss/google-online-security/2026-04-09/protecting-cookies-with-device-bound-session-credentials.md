---
source: rss/google-online-security
title: Protecting Cookies with Device Bound Session Credentials
url: http://security.googleblog.com/2026/04/protecting-cookies-with-device-bound.html
date: 2026-04-09
item_id: http://security.googleblog.com/2026/04/protecting-cookies-with-device-bound.html
category: news---

**Source:** Google Online Security
**Link:** http://security.googleblog.com/2026/04/protecting-cookies-with-device-bound.html

Posted by Ben Ackerman, Chrome team,  Daniel Rubery, Chrome team and Guillaume Ehinger, Google Account Security team 

 
Following our April 2024  announcement , Device Bound Session Credentials (DBSC) is now entering public availability for Windows users on Chrome 146, and expanding to macOS in an upcoming Chrome release. This project represents a significant step forward in our ongoing efforts to combat session theft, which remains a prevalent threat in the modern security landscape.
 
 
Session theft typically occurs when a user inadvertently downloads malware onto their device. Once active, the malware can silently extract existing session cookies from the browser or wait for the user to log in to new accounts, before exfiltrating these tokens to an attacker-controlled server. Infostealer malware families, such as LummaC2, have become increasingly sophisticated at harvesting these credentials. Because cookies often have extended lifetimes, attackers can use them to gain unauthorized access to a user’s accounts without ever needing their passwords; this access is then often bundled, traded, or sold among threat actors.
 
 
Crucially, once sophisticated malware has gained access to a machine, it can read the local files and memory where browsers store authentication cookies. As a result, there is no reliable way to prevent cookie exfiltration using software alone on any operating system. Historically, mitigating session theft relied on detecting the stolen credentials after the fact using a complex set of abuse heuristics – a reactive approach that persistent attackers could often circumvent. DBSC fundamentally changes the web's capability to defend against this threat by shifting the paradigm from reactive detection to proactive prevention, ensuring that successfully exfiltrated cookies cannot be used to access users’ accounts.
 
 How DBSC Works 


 
DBSC protects against session theft by cryptographically binding authentication sessions to a specific device. It does this using hardware-backed security modules, such as the Trusted Platform Module (TPM) on Windows and the Secure Enclave on macOS, to generate a unique public/private key pair that cannot be exported from the machine. The issuance of new short-lived session cookies is contingent upon Chrome proving possession of the corresponding private key to the server. Because attackers cannot steal this key, any exfiltrated cookies quickly expire and become useless to those attackers. This design allows large and small websites to upgrade to secure, hardware-bound sessions by adding dedicated registration and refresh endpoints to their backends, while maintaining complete compatibility with their existing front-end. The browser handles the complex cryptography and cookie rotation in the background, allowing the web app to continue using standard cookies for access just as it always has. 
 
 
Google rolled out an early version of this protocol over the last year. For sessions protected by DBSC, we have observed a significant reduction in session theft since its launch.
 
     
 
 An overview of the DBSC protocol showing the interaction between the browser and server. 
 
 Private by design 


 
A core tenet of the DBSC architecture is the preservation of user privacy. Each session is backed by a distinct key, preventing websites from using these credentials to correlate a user's activity across different sessions or sites on the same device. Furthermore, the protocol is designed to be lean: it does not leak device identifiers or attestation data to the server beyond the per-session public key required to certify proof of possession. This minimal information exchange ensures DBSC helps secure sessions without enabling cross-site tracking or acting as a device fingerprinting mechanism.
 
 Engagement with the ecosystem 


 
DBSC was designed from the beginning to be an open web standard through the W3C process and adoption by the Web Application Security Working Group. Through this process we partnered with Microsoft to design the standard to ensure it works for the web and got input from many in the industry that are responsible for web security.
 
 
Additionally, over the past year, we have also conducted two Origin Trials to ensure DBSC effectively serves the requirements of the broader web community. Many web platforms, including Okta, actively participated in these trials and their own testing and provided essential feedback to ensure the protocol effectively addresses their diverse needs.
 
 
If you are a web developer and are looking for a way to secure your users against session theft, refer to our  developer guide  for implementation details. Additionally, all the details about DBSC can be found on the  spec  and the corresponding  github . Feel free to use the  issues  page to report bugs or provide feature requests.
 
 Future improvements 


 
As we continue to evolve the DBSC standard, future iterations will focus on increasing support across diverse ecosystems and introducing advanced capabilities tailored for complex enterprise environments. Key areas of ongoing development include:
 
 

  Securing Federated Identity:  In modern enterprise environments, Single Sign-On (SSO) is ubiquitous. We are expanding the DBSC protocol to support cross-origin bindings, ensuring that a relying party (RP) session remains continuously bound to the same original device key used by the Identity Provider (IdP). This guarantees that the high-assurance security of the initial device binding is maintained throughout the entire federated login process, creating an unbroken chain of trust. 

  Advanced Registration Capabilities:  While DBSC provides robust protection for established cookies, some environments require an even stronger foundation when the session is first created. We are developing mechanisms to bind DBSC sessions to pre-existing, trusted key material rather than generating a new key at sign-in. This advanced capability enables websites to integrate complementary technologies, such as mTLS certificates or hardware security keys, creating a highly secure registration environment. 

  Broader Device Support:  We are also actively exploring the potential addition of software-based keys to extend protections to devices without dedicated secure hardware.
