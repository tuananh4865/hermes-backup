---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 topic-workflow (extracted)
  - 🔗 github-sync-setup (extracted)
  - 🔗 user-profile (extracted)
relationship_count: 3
---

# Karpathy LLM Knowledge Base

## Source
Inspired by Andrej Karpathy's tweet about using Obsidian as a personal wiki for LLMs.

## Core Idea

Karpathy uses a markdown wiki (Obsidian vault) as the "knowledge base" or "brain" for LLMs — replacing traditional RAG.

## Why Wiki Over Vector DB?

### Traditional RAG Problems
- Vector similarity search has limitations
- Embeddings lose nuance
- Hard to maintain complex relationships

### Wiki Approach Benefits
- Human-readable
- Easy to edit and maintain
- Natural organization (folders, links)
- Full context preserved
- No embedding/retrieval complexity

## Karpathy's System Components

1. **Raw content** — Immutable source data
2. **Wiki/Concepts** — Synthesized knowledge
3. **User profile** — Learned preferences and facts
4. **LLM** — Reads wiki as its "memory"

## Related
- [[topic-workflow]] — Implementation of this concept
- [[github-sync-setup]] — Syncing the wiki across devices
- [[user-profile]] — User context that powers the system
