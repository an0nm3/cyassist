---
source: rss/sensepost
title: Intercepting HTTPS Communication in Flutter: Going Full Hardcore Mode with Frida
url: https://sensepost.com/blog/2025/intercepting-https-communication-in-flutter-going-full-hardcore-mode-with-frida/
date: 2025-04-16
item_id: https://sensepost.com/blog/2025/intercepting-https-communication-in-flutter-going-full-hardcore-mode-with-frida/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/intercepting-https-communication-in-flutter-going-full-hardcore-mode-with-frida/

tl;dr  In this blog post, I will share insights I learned while researching the Flutter framework and the  reFlutter  tool. It will dive deep into Flutter&#8217;s architecture, some of its inner workings and dependencies, and finally, drill down into the SSL verification logic. The post will end by exploring what the reFlutter tool actually does and my attempts at replicating the same behaviour with Frida. 
  Note: If you are in a pinch on a mobile assessment where the application uses Flutter, the reFlutter tool is a great option. This blog post does not advocate that you need to use Frida logic. It is simply an exercise in seeing whether a Frida equivalent may exist.
