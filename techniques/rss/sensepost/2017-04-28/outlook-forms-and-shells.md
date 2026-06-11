---
source: rss/sensepost
title: Outlook Forms and Shells
url: https://sensepost.com/blog/2017/outlook-forms-and-shells/
date: 2017-04-28
item_id: https://sensepost.com/blog/2017/outlook-forms-and-shells/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/outlook-forms-and-shells/

Using MS Exchange and Outlook to get a foothold in an organisation, or to maintain persistence, has been a go to attack method for RedTeams lately. This attack has typically relied on using Outlook Rules to trigger the shell execution. Although  Ruler  makes accomplishing this really easy, it has, up until now, required a WebDAV server to host our shell/application. In most cases this is not an issue, but once in a while you run into a restrictive network that does not allow the initial WebDAV connection to be established. In such instances, the attack sadly fails. Another downside to Outlook rules is that we are limited to only providing an application path, and no command-line arguments, meaning none of our fancy Powershell one-liners can be used.
