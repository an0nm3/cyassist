---
source: rss/google-online-security
title: HTTPS certificate industry phasing out less secure domain validation methods
url: http://security.googleblog.com/2025/12/https-certificate-industry-phasing-out.html
date: 2025-12-10
item_id: http://security.googleblog.com/2025/12/https-certificate-industry-phasing-out.html
category: news---

**Source:** Google Online Security
**Link:** http://security.googleblog.com/2025/12/https-certificate-industry-phasing-out.html

Posted by Chrome Root Program Team  

 
Secure connections are the backbone of the modern web, but a certificate is only as trustworthy as the validation process and issuance practices behind it. Recently, the  Chrome Root Program  and the  CA/Browser Forum  have taken decisive steps toward a more secure internet by adopting new security requirements for HTTPS certificate issuers.
 
 
These initiatives, driven by Ballots  SC-080 ,  SC-090 , and  SC-091 , will sunset 11 legacy methods for Domain Control Validation. By retiring these outdated practices, which rely on weaker verification signals like physical mail, phone calls, or emails, we are closing potential loopholes for attackers and pushing the ecosystem toward automated, cryptographically verifiable security.
 
 
To allow affected website operators to transition smoothly, the deprecation will be phased in, with its full security value realized by March 2028.
 
 
This effort is a key part of our public roadmap, “ Moving Forward, Together, ” launched in 2022. Our vision is to improve security by modernizing infrastructure and promoting agility through automation. While "Moving Forward, Together" sets the aspirational direction, the recent updates to the  TLS Baseline Requirements  turn that vision into policy. This builds on our momentum from earlier this year, including the successful  advocacy for the adoption of other security enhancing initiatives  as industry-wide standards.
 
 
 What’s Domain Control Validation? 
 
 
Domain Control Validation is a security-critical process designed to ensure certificates are only issued to the legitimate domain operator. This prevents unauthorized entities from obtaining a certificate for a domain they do not control. Without this check, an attacker could obtain a valid certificate for a legitimate website and use it to impersonate that site or intercept web traffic.
 
 
Before issuing a certificate, a Certification Authority (CA) must verify that the requestor legitimately controls the domain. Most modern validation relies on “challenge-response” mechanisms, for example, a CA might provide a random value for the requestor to place in a specific location, like a DNS TXT record, which the CA then verifies. 
 
 
Historically, other methods validated control through indirect means, such as looking up contact information in WHOIS records or sending an email to a domain contact. These methods have been proven vulnerable ( example ) and the recent efforts retire these weaker checks in favor of robust, automated alternatives. 
 
 
 Raising the floor of security 
 
 
The recently passed CA/Browser Forum Server Certificate Working Group Ballots introduce a phased sunset of the following Domain Control Validation methods. Alternative existing methods offer stronger security assurances against attackers trying to obtain fraudulent certificates – and the alternative methods are getting  stronger  over time, too.
 
 
Sunsetted methods relying on email:
 
 

  Email, Fax, SMS, or Postal Mail to Domain Contact  

  Email, Fax, SMS, or Postal Mail to IP Address Contact  

  Constructed Email to Domain Contact  

  Email to DNS CAA Contact  

  Email to DNS TXT Contact  
 
 
Sunsetted methods relying on phone: 
 
 

  Phone Contact with Domain Contact  

  Phone Contact with DNS TXT Record Phone Contact  

  Phone Contact with DNS CAA Phone Contact  

  Phone Contact with IP Address Contact  
 
 
Sunsetted method relying on a reverse lookup:
 
 

  IP Address  

  Reverse Address Lookup  
 
 
For everyday users, these changes are invisible - and that’s the point. But, behind the scenes, they make it harder for attackers to trick a CA into issuing a certificate for a domain they don’t control. This reduces the risk that stale or indirect signals, (like outdated WHOIS data, complex phone and email ecosystems, or inherited infrastructure) can be abused. These changes push the ecosystem toward standardized (e.g.,  ACME ), modern, and auditable Domain Control Validation methods. They increase agility and resilience by encouraging site owners to transition to modern Domain Control Validation methods, creating opportunities for faster and more efficient certificate lifecycle management through  automation .
 
 
These initiatives remove weak links in how trust is established on the internet. That leads to a safer browsing experience  for everyone , not just users of a single browser, platform, or website.
