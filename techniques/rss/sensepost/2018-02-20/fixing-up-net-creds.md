---
source: rss/sensepost
title: Fixing up Net-Creds
url: https://sensepost.com/blog/2018/fixing-up-net-creds/
date: 2018-02-20
item_id: https://sensepost.com/blog/2018/fixing-up-net-creds/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2018/fixing-up-net-creds/

TL; DR: I fixed-up net-creds and MITMf to solve the CHALLENGE NOT FOUND bug. 
 A while back on an internal assessment, I was having a hard time getting a high-privileged user account. 
 This was the third assessment SensePost has done for the client, and they have implemented several of our recommendations. In particular, Responder wasn’t providing me with any hashes even though I was connected to the same network segment as several users, including some administrators. The client has a strict policy of only using the latest operating systems, i.e. Windows 10, and had disabled NBNS and LLMNR.
