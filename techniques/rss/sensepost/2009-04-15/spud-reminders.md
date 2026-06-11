---
source: rss/sensepost
title: SPUD reminder(s)
url: https://sensepost.com/blog/2009/spud-reminders/
date: 2009-04-15
item_id: https://sensepost.com/blog/2009/spud-reminders/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2009/spud-reminders/

After some queries regarding  SPUD , I thought it would be a good idea to blog this reminder: 
 * Spud can only be run as an administrative user. 
* Spud cannot be run by directly accessing the .exe.  You should run SPUD from the shortcut provided.  The reason being: SPUD cannot start from the \bin directory, but only from the \bin parent directory. (default: Program Files\SensePost SPUD). I.e, run &#8220;bin\SPUD.exe&#8221; from the installation directory as below:
