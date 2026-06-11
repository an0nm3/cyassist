---
source: rss/nviso-labs
title: Securing AI systems without overconfidence or fear – Part 2: Attack surfaces and the checkpoint flow
url: https://blog.nviso.eu/2026/05/22/securing-ai-systems-without-overconfidence-or-fear-part-2-attack-surfaces-and-the-checkpoint-flow/
date: 2026-05-22
item_id: https://blog.nviso.eu/2026/05/22/securing-ai-systems-without-overconfidence-or-fear-part-2-attack-surfaces-and-the-checkpoint-flow/
category: techniques---

**Source:** NVISO Labs
**Link:** https://blog.nviso.eu/2026/05/22/securing-ai-systems-without-overconfidence-or-fear-part-2-attack-surfaces-and-the-checkpoint-flow/

Part 1 explained how we have to bound behavior instead of asserting exact outputs. This post maps where to place those boundaries. AI systems expose attack surfaces at three runtime checkpoints (i.e., input, processing and output) and the checks differ by system type (classical ML, LLM-based, or hybrid).
