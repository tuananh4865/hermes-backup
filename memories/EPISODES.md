---
title: Session Episodes
created: 2026-05-06
updated: 2026-05-06
type: session-log
tags: [memory, sessions]
confidence: high
---

# Session Episodes Log

> Cross-session memory: each session summary is stored here.
> Format: ## Session YYYY-MM-DD — topic | turns | outcome
> Bounded: last 30 sessions retained

## Session 2026-05-06 — Memory System Upgrade | 15+ turns

### Summary
Researched long-term memory architectures (MemGPT, Letta, Mem0, Graphiti, Anthropic, Microsoft AMV-L). Implemented hybrid retrieval (BM25 + semantic) in WikiMemoryProvider. Retrieval tested working: ByteRover query → exact setup command, gemma-4-e2b query → correct config.

### Key Files
- `~/.hermes/plugins/memory/wiki/__init__.py` — hybrid retrieval added
- `~/.hermes/memories/EPISODES.md` — this file

### Decisions
- Phase 2 (Retrieval) prioritized over Phase 1 (Entity Extraction) because write without retrieval = useless
- Option A (lightweight TF-IDF) chosen over Option B (ChromaDB) — no new dependencies

### Outcome
Agent now has hybrid memory retrieval: BM25 (0.6 weight) + semantic n-gram (0.4 weight) via RRF fusion.
