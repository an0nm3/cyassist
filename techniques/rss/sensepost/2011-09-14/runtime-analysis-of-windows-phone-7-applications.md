---
source: rss/sensepost
title: Runtime analysis of Windows Phone 7 Applications
url: https://sensepost.com/blog/2011/runtime-analysis-of-windows-phone-7-applications/
date: 2011-09-14
item_id: https://sensepost.com/blog/2011/runtime-analysis-of-windows-phone-7-applications/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2011/runtime-analysis-of-windows-phone-7-applications/

Runtime analysis is an integral part of most application security assessment processes. Many powerful tools have been developed to perform execution/data flow analysis and code debugging for desktop and server operating systems. Although a few dynamic analysis tools such as DroidBox are available for Android, I currently know of no similar public tools for the Windows Phone 7 platform. The main challenge for Windows Phone 7 is the lack of a programable debugging interface in both the Emulator and phone devices. The Visual Studio 2010 debugger for Phone applications does not have an &#8220;Attach to process&#8221; feature and can only be used to debug applications for which the source code is available.  Although the Kernel Independent Transport Layer (KITL) can be enabled on some Windows Phone devices at boot time which could be very useful for Kernel and unmanged code debugging, it can&#8217;t be used directly for code tracing of phone applications which are executed by the .NET  compact framework.
