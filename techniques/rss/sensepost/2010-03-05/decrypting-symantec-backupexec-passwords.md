---
source: rss/sensepost
title: Decrypting Symantec BackupExec passwords
url: https://sensepost.com/blog/2010/decrypting-symantec-backupexec-passwords/
date: 2010-03-05
item_id: https://sensepost.com/blog/2010/decrypting-symantec-backupexec-passwords/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2010/decrypting-symantec-backupexec-passwords/

BackupExec agent is often among common services found on the internal pen tests. The agent software stores an encrypted  &#8220;logon account&#8221;  password in its backend MS SQL database (LoginAccounts table). These accounts include the &#8220;system logon account&#8221; which is used to run agent services and an optional number of active directory accounts that are used to access resources over the network. The following scenarios can result in access to encrypted passwords:
