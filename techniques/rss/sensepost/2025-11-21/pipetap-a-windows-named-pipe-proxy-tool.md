---
source: rss/sensepost
title: pipetap – a windows named pipe proxy tool
url: https://sensepost.com/blog/2025/pipetap-a-windows-named-pipe-proxy-tool/
date: 2025-11-21
item_id: https://sensepost.com/blog/2025/pipetap-a-windows-named-pipe-proxy-tool/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2025/pipetap-a-windows-named-pipe-proxy-tool/

Windows named pipes, being one of many available mechanisms for inter-component / inter-process communications, is interesting from a security perspective. While hunting for vulnerabilities in various bits of software, I often see the pattern of a privileged process that exposes a named pipe such that a client process can interact with it. More often than not, you&#8217;ll eventually be curious enough to want to snoop on the data that is transferred over this named pipe. At this stage you&#8217;ll Google &#8220;Windows Named Pipe Proxy&#8221;, find some results and away you go. My hope is that pipetap is another one of these results you&#8217;ll find that can help with your Windows named pipe reverse engineering journey. You can find it here:  https://github.com/sensepost/pipetap
