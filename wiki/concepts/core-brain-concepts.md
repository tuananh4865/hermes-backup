---
confidence: medium
last_verified: 2026-04-10
relationships:
  - 🔍 karpathy-llm-knowledge-base (inferred)
  - 🔍 local-llm (inferred)
  - 🔍 topic-workflow (inferred)
relationship_count: 3
---

# Core Brain Concepts

## Overview

Core concepts for building a **personal wiki brain** — a knowledge management system that acts like a second brain, storing and connecting information in ways that enable fast retrieval and insight discovery.

## Fundamental Principles

### 1. Progressive Summarization

Capture first, organize later. Notes should be easy to add quickly, then refined over time into denser summaries.

**Layers:**
- Layer 0: Raw capture (highlights, bookmarks, voice memos)
- Layer 1: Bolded key passages
- Layer 2: Highlights + brief notes
- Layer 3: Executive summary
- Layer 4: Personal synthesis

### 2. Evergreen Notes

Notes should be written to evolve — atomic enough to be reusable, linked enough to form a knowledge graph.

**Characteristics:**
- Atomic: One concept per note
- Title as assertion: "X enables Y" not just "X"
- Connected: Links to related concepts
- Updated: Living documents that evolve with understanding

### 3. Knowledge Graph Thinking

Not a hierarchy but a network. Ideas connect across topics, creating unexpected relationships.

```
User's interests → concepts → connections → insights
```

## Wiki Brain Architecture

```
raw/           → processed/     → concepts/
(raw capture)    (cleaned)        (synthesized)
     ↓               ↓                 ↓
  transcripts    organized by       linked by
  bookmarks      topic              wikilinks
  highlights
```

## Key Properties

| Property | Description |
|----------|-------------|
| **Searchability** | Everything findable within seconds |
| **Linkability** | Ideas connect across topics |
| **Reviewability** | Stale content surfaces for update |
| **Autonomy** | System self-maintains with agent assistance |

## For LLMs

When a personal wiki is used to ground LLM responses:

-  — Why Markdown + wikilinks work for LLMs
- [[karpathy-llm-knowledge-base]] — How to structure knowledge for LLMs
-  — Using LLMs as autonomous knowledge managers

## Related

-  — Tool implementation
- [[local-llm]] — Running LLMs locally for privacy
- [[topic-workflow]] — How topics are processed
