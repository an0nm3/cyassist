---
source: rss/projectdiscovery-blog
title: How We Cut LLM Costs by 59% With Prompt Caching
url: https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching
date: 2026-04-10
item_id: https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching
category: techniques---

**Source:** ProjectDiscovery Blog
**Link:** https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching

At ProjectDiscovery, we've been building Neo, an autonomous security testing platform that runs multi-agent, multi-step workflows, routinely executing 20-40+ LLM steps per task. Vulnerability assessments, code reviews, and security audits at scale, enabling continuous testing across the entire development lifecycle.

When we launched, our LLM costs were staggering. A single complex task with Opus 4.5 could consume 60 million tokens. Then we implemented prompt caching. Here's what changed:
