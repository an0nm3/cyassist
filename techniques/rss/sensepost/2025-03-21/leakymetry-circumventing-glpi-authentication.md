---
source: rss/sensepost
title: Leakymetry: Circumventing GLPI Authentication
url: https://sensepost.com/blog/2025/leakymetry-circumventing-glpi-authentication/
date: 2025-03-21
item_id: https://sensepost.com/blog/2025/leakymetry-circumventing-glpi-authentication/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/leakymetry-circumventing-glpi-authentication/

Intro 
 GLPI (Gestionnaire libre de parc informatique) is a popular open-source software in France and Brazil. It is used to create a mapping of a network through an inventory plugin, but also to gather users&#8217; issues through a ticket system. 
 Starting research 
 As I was wondering how the update mechanism worked in GLPI, I saw something really interesting in this file. 
 It is important to note that most of the GLPI files are not accessible without authentication. Because of this, the attack surface on this software is reduced. However, the update.php script is accessible by an unauthenticated user. And this file contains juicy information. I started looking at it, and I immediately saw that this script under certain parameters, disclosed telemetry information.
