---
source: rss/sensepost
title: Playing with Python Pickle #2
url: https://sensepost.com/blog/2010/playing-with-python-pickle-%232/
date: 2010-11-09
item_id: https://sensepost.com/blog/2010/playing-with-python-pickle-%232/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2010/playing-with-python-pickle-%232/

[This is the second in a series of posts on Pickle. Link to part  one .] 
 In the previous post I introduced Python&#8217;s Pickle mechanism for serializing and deserializing data and provided a bit of background regarding where we came across serialized data, how the virtual machine works and noted that Python intentionally does not perform security checks when unpickling. 
 In this post, we&#8217;ll work through a number of examples that depict exactly why unpickling untrusted data is a dangerous operation. Since we&#8217;re going to handcraft Pickle streams, it helps to have an opcode reference handy; here are the opcodes we&#8217;ll use:
