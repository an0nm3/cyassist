---
source: rss/sensepost
title: Liniaal – Empire through Exchange
url: https://sensepost.com/blog/2017/liniaal-empire-through-exchange/
date: 2017-03-22
item_id: https://sensepost.com/blog/2017/liniaal-empire-through-exchange/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/liniaal-empire-through-exchange/

Getting access to an internal network is always great, keeping this access can be a whole other challenge. At times we want to fly below the radar and ensure our access doesn&#8217;t get detected or blocked by traditional network based solutions. To this end, communicating directly through an Exchange server can be very beneficial and solve both challenges. 
 Technical details 
  Ruler  provides us with a means of getting a shell on an internal network. This is all done through Exchange and ensures our &#8220;trigger&#8221; for getting a shell back is usually only an email away. To a large degree this gives us the desired persistence we may want, however, we are still dependent on our traditional communication channels, be it DNS, HTTP(s) or TCP. This means our tools can need to traverse the traditional network boundary, aka, the web-gateway. Defenders place all their in-line defences here and should be able to detect and block our traffic. Exchange usually falls outside of this monitoring, as it should only be sending and receiving email. Sure there can be DLP and in-line scanning for malicious mail attachments, but this is usually aimed at the actual email messages. Do you have or have you seen in-line inspection of the Exchange/Outlook transport? Not the IMAP/SMTP traffic, the MAPI/HTTP or the RPC/HTTP channel that external Outlook clients use to communicate with the Exchange server. In my experience, the answer is usually no, there is no inspection of these transports.
