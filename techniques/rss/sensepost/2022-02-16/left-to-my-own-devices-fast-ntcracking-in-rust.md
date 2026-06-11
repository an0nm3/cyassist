---
source: rss/sensepost
title: Left To My Own Devices – Fast NTCracking in Rust
url: https://sensepost.com/blog/2022/left-to-my-own-devices-fast-ntcracking-in-rust/
date: 2022-02-16
item_id: https://sensepost.com/blog/2022/left-to-my-own-devices-fast-ntcracking-in-rust/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/left-to-my-own-devices-fast-ntcracking-in-rust/

When I got a new MacBook with an M1 Pro chip, I was excited to see the performance benefits. The first thing I did was to fire up hashcat which gave an impressive benchmark speed for NT hashes (mode 1000) of around 9 GH/s, a solid doubling of the benchmark speed of my old Intel MacBook Pro. But, when it came to actually cracking things, the speed dropped off considerably. Instead of figuring out why, I decided to try my hand at writing my own NT hash cracker, because I’m kind of addicted to writing single use tooling in rust then taking time to perf optimise it.
