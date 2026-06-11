---
source: rss/sensepost
title: [Another] Intercepting Proxy
url: https://sensepost.com/blog/2015/another-intercepting-proxy/
date: 2015-09-03
item_id: https://sensepost.com/blog/2015/another-intercepting-proxy/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2015/another-intercepting-proxy/

But, Websockets! 
 The last week I was stuck on a web-app assessment where everything was new-age HTML5, with AngularJS and websockets. Apart from the login sequence, all communication happened through websockets. Now intercepting websockets can be done in Burp and you can modify the requests/responses as you wish. There were however multiple issues with this. 
 
 Polling &#8211; the webapp did a &#8216;ping&#8217; request and if this was held up (intercept in burp) the app would timeout and I had to start from scratch. This timeout period was relatively aggressive, so by the time I finished modifying a request, the app had timed out and my changes meant squat. 
 Intercept/Replace rules- ping messages were irritating and Burp had no way to not intercept these.  It also wasn&#8217;t possible to configure out replace rules. And according to this, it isn&#8217;t coming to Burp anytime soon&#8230;  https://support.portswigger.net/customer/portal/questions/11577304-replace-text-in-websocket-operations  
 Replay/Intruder &#8211; there is no way to replay a websocket request in Burp. This also means no Intruder :( 
 
 At this junction, three options were available to me. Use ZAP (which does have intercept rules but not replay/replace/intruder). Use Internet Explorer and force the app into non-websocket mode or write a custom proxy. So the choice was obvious, write a custom proxy.
