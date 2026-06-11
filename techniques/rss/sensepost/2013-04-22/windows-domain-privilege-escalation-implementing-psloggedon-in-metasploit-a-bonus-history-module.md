---
source: rss/sensepost
title: Windows Domain Privilege Escalation : Implementing PSLoggedOn in Metasploit (+ a bonus history module)
url: https://sensepost.com/blog/2013/windows-domain-privilege-escalation-implementing-psloggedon-in-metasploit--a-bonus-history-module/
date: 2013-04-22
item_id: https://sensepost.com/blog/2013/windows-domain-privilege-escalation-implementing-psloggedon-in-metasploit--a-bonus-history-module/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2013/windows-domain-privilege-escalation-implementing-psloggedon-in-metasploit--a-bonus-history-module/

There are multiple paths one could take to getting Domain Admin on a Microsoft Windows Active Directory Domain. One common method for achieving this is to start by finding a system where a privileged domain account, such as a domain admin, is logged into or has recently been logged into. Once access to this system has been gained, either stealing their security tokens (ala Incognito or pass-the-hash attacks) or  querying Digest Authentication (with Mimikatz/WCE) to get their clear-text password. The problem is finding out where these user&#8217;s are logged in.
