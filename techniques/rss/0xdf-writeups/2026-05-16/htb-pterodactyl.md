---
source: rss/0xdf-writeups
title: HTB: Pterodactyl
url: https://0xdf.gitlab.io/2026/05/16/htb-pterodactyl.html
date: 2026-05-16
item_id: https://0xdf.gitlab.io/2026/05/16/htb-pterodactyl.html
category: techniques
tags: [Exploit]
---

**Source:** 0xdf Writeups
**Link:** https://0xdf.gitlab.io/2026/05/16/htb-pterodactyl.html

Pterodactyl hosts a Minecraft community site alongside an instance of the Pterodactyl game-server management panel. I’ll exploit an unauthenticated directory traversal in the panel’s locale endpoint that gets PHP to include arbitrary files on disk, and chain it with the classic PEAR pearcmd technique to write and execute a webshell. From there I’ll read database credentials, crack a bcrypt hash, and pivot to a user who reuses that password. The box runs openSUSE, where I’ll abuse a PAM environment-variable flaw to convince Polkit I’m a local console session, then exploit a libblockdev/udisks vulnerability to mount a crafted XFS image carrying a SetUID-root shell and escalate to root. In Beyond Root, I’ll get CopyFail and DirtyFrag (two recent Linux kernel page-cache privilege-escalation exploits) working on the host.
