---
source: rss/sensepost
title: A new look at null sessions and user enumeration
url: https://sensepost.com/blog/2018/a-new-look-at-null-sessions-and-user-enumeration/
date: 2018-05-11
item_id: https://sensepost.com/blog/2018/a-new-look-at-null-sessions-and-user-enumeration/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2018/a-new-look-at-null-sessions-and-user-enumeration/

Hello, 
 TLDR; I think I found three new ways to do user enumeration on Windows domain controllers, and I wrote  some scripts  for it. 
 Over the years, I have often used the NULL session vulnerability to enumerate lists of users, groups, shares and other interesting information from remote Windows systems. 
 For the uninitiated, Windows exposes several administrative and hidden shares via SMB by default. 
 Some of these shares allow one to access the complete storage device on remote systems. For example, C$ will allow one to access the C Drive. Another share, Admin$, allows one to access the Windows installation directory. To be able to mount these shares however, one needs to be an administrator on the remote system.
