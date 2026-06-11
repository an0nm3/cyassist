---
source: rss/sensepost
title: A distinguisher for SHA256 using Bitcoin (mining faster along the way)
url: https://sensepost.com/blog/2017/a-distinguisher-for-sha256-using-bitcoin-mining-faster-along-the-way/
date: 2017-10-16
item_id: https://sensepost.com/blog/2017/a-distinguisher-for-sha256-using-bitcoin-mining-faster-along-the-way/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2017/a-distinguisher-for-sha256-using-bitcoin-mining-faster-along-the-way/

This post assumes a passing familiarity with what a  Distinguishing Attack  on a cryptographic hash is, as well as the high level composition of Bitcoin  block headers  and  mining  them. 
  tldr:  
  To distinguish between an ideal random permutation hash and SHA256, hash a large amount (~2^80) of candidate 1024 bit blocks twice, as done in Bitcoin. Ensure that the bits of the candidate blocks are sparsely set (much fewer than the 512 mean expected), according to the Bitcoin protocol, discarding candidate blocks that do not meet the Bitcoin &#8220;difficulty&#8221; standard (where the resultant hashes start with a the large number of 0’s). With the remaining set of valid input candidates (467369 when this analysis was done), observe a particular set of 32 bits in the input block (located where Bitcoin has the nonce, input bits 607-639). Note that the mean number of bits set in the nonce field is skewed to the left, i.e. fewer than the expected value of 16 bits set (estimated mean 15.428).
