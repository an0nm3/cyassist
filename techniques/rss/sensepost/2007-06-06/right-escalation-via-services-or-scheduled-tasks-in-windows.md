---
source: rss/sensepost
title: Right escalation via services or scheduled tasks in Windows
url: https://sensepost.com/blog/2007/right-escalation-via-services-or-scheduled-tasks-in-windows/
date: 2007-06-06
item_id: https://sensepost.com/blog/2007/right-escalation-via-services-or-scheduled-tasks-in-windows/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2007/right-escalation-via-services-or-scheduled-tasks-in-windows/

Scheduled tasks and services are often run as accounts with excessive privileges (HP Insight, backups etc) instead of limited service accounts. By exploring the tasks under c:\windows\tasks or the services by managing the computer, you can quickly see possible options to escalate your rights. By replacing at the actual exe that the service or task runs with a exe of your own, you can spawn a netcat shell. I use a batch file to exe converter and use the batchfile to call nc.exe with the correct parameters. *You can not alter the service or task itself in anyway else you loose the stored credentials.  Attached are some screenshots that should illustrate this.
