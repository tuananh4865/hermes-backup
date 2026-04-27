---
title: "Tun Https Github - 2026-04-13"
created: 2026-04-13
type: concept
tags: [git, github, source-code]
---

# Tun Https Github - 2026-04-13

This guide outlines the architecture and operational workflow of Tun Https Github, a system designed for managing knowledge across multiple layers.

## Summary
Tun Https Github is an AI-assisted wiki system that distinguishes between human knowledge and machine-generated documentation. It prioritizes a persistent database over the AI agent's immediate memory to ensure long-term consistency and accuracy.

## Key Insights
*   The system maintains a strict separation between immutable raw sources (like `raw/transcripts`) and the dynamic wiki pages (`index.md`, `_meta/start-here.md`).
*   Project scanning is mandatory at the start of every session to ensure resource allocation efficiency.
*   AI agents are designed as assistants for users, utilizing semantic retrieval to understand context across documents.

## Analysis
1. The core philosophy of this wiki system is "trust in the wiki over memory," acknowledging that human knowledge is transient while machine-generated content can be replicated and stored permanently. This architectural choice suits systems requiring high volume of documentation compared to text-based knowledge base tools.

2. The separation of concerns is critical; raw files like `transcripts` are protected from modification, ensuring that the historical context of a session remains stable while new content is generated fresh. This prevents drift in knowledge management and ensures the "last 20" entries in `log.md` remain accurate to recent events.

3. The workflow emphasizes automation and organization, utilizing scripts like `wiki_self_heal.py` to maintain quality without manual intervention. By defining a clear hierarchy (Schema, Index, Log) and strict procedural rules (such as the Request-to-SDD workflow), the system ensures that new contributions adhere to consistent standards and are easily searchable over time.