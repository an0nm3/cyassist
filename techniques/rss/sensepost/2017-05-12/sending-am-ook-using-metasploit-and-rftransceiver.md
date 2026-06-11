---
source: rss/sensepost
title: Sending AM-OOK using Metasploit and rftransceiver
url: https://sensepost.com/blog/2017/sending-am-ook-using-metasploit-and-rftransceiver/
date: 2017-05-12
item_id: https://sensepost.com/blog/2017/sending-am-ook-using-metasploit-and-rftransceiver/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/sending-am-ook-using-metasploit-and-rftransceiver/

Introduction 
 Towards the end of last year, I found myself  playing around  with some basic amplitude modulation (AM)/On-off keying (OOK) software defined radio. That resulted in  ooktools  being built to help with making some of that work easier and to help me learn. A little while ago, the Metasploit project announced new  ‘rftransceiver’ capabilities  that were added to the framework with a similar goal of making this research easier. 
     
 How things fit together 
 First things first. I had to try and understand how this new functionality actually works. From the Metasploit blog post, it was possible to see that the additions allowed you to communicate with a RFCat capable device from Metasploit and run modules over a session. A session is started by connecting to a small JSON API (with a python helper) that bridges HTTP requests to  rflib  methods.
