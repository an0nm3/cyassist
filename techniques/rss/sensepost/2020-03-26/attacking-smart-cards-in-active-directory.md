---
source: rss/sensepost
title: Attacking smart cards in active directory
url: https://sensepost.com/blog/2020/attacking-smart-cards-in-active-directory/
date: 2020-03-26
item_id: https://sensepost.com/blog/2020/attacking-smart-cards-in-active-directory/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/attacking-smart-cards-in-active-directory/

Introduction 
 Recently, I encountered a fully password-less environment. Every employee in this company had their own smart card that they used to login into their computers, emails, internal applications and more. None of the employees at the company had a password at all &#8211; this sounded really cool. 
 In this post I will detail a technique used to impersonate other users by modifying a User Principal Name (UPN) on an Active Directory domain that only uses smart cards.
