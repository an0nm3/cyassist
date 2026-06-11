---
source: rss/sensepost
title: Privilege Escalation in SQL Server (Depending on some dodgy requirements)
url: https://sensepost.com/blog/2012/privilege-escalation-in-sql-server-depending-on-some-dodgy-requirements/
date: 2012-08-08
item_id: https://sensepost.com/blog/2012/privilege-escalation-in-sql-server-depending-on-some-dodgy-requirements/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2012/privilege-escalation-in-sql-server-depending-on-some-dodgy-requirements/

I was playing with a few SQL server idiosyncrasies more than a year ago before becoming so completely distracted with the whole SAP protocol-decoding business.  Having some time on my hands for once, I thought I would blog it. 
 Early last year, I found it possible to create jobs owned by other users on MS SQL Server (2000, 2005 and 2008) by an unprivileged user &#8211; providing the user had the capability of creating or altering stored procedures in the [master].[dbo] schema.  The reason for this, comes as a result of cross-database permissions being chained, by default, across the system databases [master], [msdb] and [tempdb].  According to Microsoft, this is by design.
