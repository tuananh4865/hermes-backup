---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 wiki (extracted)
  - 🔗 user-profile (extracted)
  - 🔗 karpathy-llm-knowledge-base (extracted)
  - 🔗 karpathy-llm-knowledge-base (extracted)
  - 🔗 wikilinks (extracted)
  - 🔗 self-healing-wiki (extracted)
  - 🔗 automation (extracted)
  - 🔗 wiki (extracted)
  - 🔗 karpathy-llm-knowledge-base (extracted)
relationship_count: 9
---

# Knowledge Base

## Overview

Knowledge base systems cho phép AI truy cập và sử dụng thông tin. [[wiki]] của [[user-profile]] sử dụng Markdown wiki-based approach.

## Related
- [[topic-workflow]]

## Approaches Compared

### 1. Wiki-Based (Current)
```markdown
- Pros: Human-readable, AI-native, no embedding needed
- Cons: No semantic search
- Best for: Structured knowledge, concepts, procedures
- Example: [[karpathy-llm-knowledge-base]]
```

### 2. RAG (Retrieval-Augmented Generation)
```markdown
- Pros: Semantic search, handles unstructured text
- Cons: Embedding overhead, retrieval quality issues
- Best for: Large document collections
- Example: pinecone, weaviate
```

### 3. Vector Database
```markdown
- Pros: Fast similarity search, scales well
- Cons: Infrastructure overhead, needs embeddings
- Best for: High-volume semantic search
```

## Why Wiki Over RAG?

[[karpathy-llm-knowledge-base]]: LLMs are already good at extracting information from well-structured text. A simple wiki with good links and structure often beats complex RAG pipelines.

Key insight:
> "LLMs can read markdown. If your knowledge base is a well-structured wiki, you don't need embeddings."

## Wiki Knowledge Base Features

- [[wikilinks]] — Cross-references between concepts
- [[self-healing-wiki]] — Auto-maintains link integrity
- [[automation]] — Auto-fills gaps in knowledge
-  — Passive knowledge capture

## Related

- [[wiki]] — The wiki implementation
-  — RAG as alternative/complement
- [[karpathy-llm-knowledge-base]] — Source of inspiration
