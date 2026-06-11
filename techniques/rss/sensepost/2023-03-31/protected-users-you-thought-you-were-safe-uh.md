---
source: rss/sensepost
title: Protected Users: you thought you were safe uh?
url: https://sensepost.com/blog/2023/protected-users-you-thought-you-were-safe-uh/
date: 2023-03-31
item_id: https://sensepost.com/blog/2023/protected-users-you-thought-you-were-safe-uh/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2023/protected-users-you-thought-you-were-safe-uh/

On the 31st of October 2022, a PR on  CrackMapExec from Thomas Seigneuret (@Zblurx)  was merged. This PR fixed Kerberos authentication in the CrackMapExec framework. Seeing that, I instantly wanted to try it out and play a bit with it. While doing so I discovered a weird behaviour with the Protected Users group. In this blogpost I&#8217;ll explain what the Protected Users group is, why it is a nice security feature and yet why it is incomplete for the Administrator (RID500) user.
