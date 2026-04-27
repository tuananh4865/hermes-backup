---
title: "pgvector — PostgreSQL Vector Database"
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [vector-db, postgresql, pgvector, rag, local-llm, embedding]
confidence: high
sources:
  - Tiger Data — Pgvector vs Pinecone (2024-06)
  - Zilliz — FAISS vs pgvector (2024)
  - Encore.dev — pgvector Guide (2025)
related:
  - [[vector-db]]
  - [[rag]]
  - [[agent-memory]]
  - [[ollama]]
  - [[local-llm-agents]]
---

# pgvector — PostgreSQL Vector Database

## Overview

pgvector is a PostgreSQL extension that adds vector similarity search capabilities — enabling semantic search and RAG (Retrieval-Augmented Generation) without a separate database. It's the lowest-cost path to production-grade vector search for most AI agent use cases.

## Why pgvector for AI Agents?

**Zero infrastructure overhead:**
- Runs in existing PostgreSQL instance
- No separate vector database to maintain
- Same backup, replication, and security as your main database

**Cost comparison:**
| Database | Monthly Cost | Notes |
|----------|-------------|-------|
| pgvector | ~$0 (PostgreSQL already running) | Best value |
| Pinecone | $70-500+/mo | Managed, scalable |
| Weaviate | $50-200+/mo | Self-hosted option |
| Qdrant | Free (self-hosted) | Best performance |

**Agent memory use case:**
pgvector excels at storing conversation history, fact embeddings, and retrieval contexts — the core components of agent memory systems.

## Installation

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),  -- OpenAI ada-002 = 1536 dims
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create HNSW index for fast approximate nearest neighbor
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

## RAG Pipeline with pgvector

```python
import psycopg2
from openai import OpenAI

conn = psycopg2.connect(os.environ["DATABASE_URL"])
client = OpenAI()

def rag_retrieve(query: str, top_k: int = 5):
    # 1. Embed query
    query_embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query
    ).data[0].embedding

    # 2. Search pgvector
    cur = conn.cursor()
    cur.execute("""
        SELECT content, 1 - (embedding <=> %s) AS similarity
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT %s
    """, (query_embedding, query_embedding, top_k))

    return cur.fetchall()
```

## Performance Characteristics

**Throughput:**
- pgvector handles ~1,000 queries/second on standard PostgreSQL
- HNSW indexes: sub-10ms query latency for 1M vectors
- ivfflat indexes: good for lower dimensions (<768)

**Scalability:**
- Good up to ~1M vectors per table
- Beyond that: consider Pinecone or Weaviate
- Sharding possible but adds complexity

**Index types:**
| Index | Build Time | Query Speed | Memory |
|-------|-----------|-------------|--------|
| ivfflat | Fast | Medium | Low |
| hnsw | Slow | Fastest | Higher |

## pgvector vs Alternatives

| Feature | pgvector | Pinecone | FAISS | Qdrant |
|---------|----------|----------|-------|--------|
| Infrastructure | Existing PG | Separate | In-process | Separate |
| Cost | Free | $70+/mo | Free | Free |
| Managed option | ✅ RDS | ✅ Native | ❌ | ✅ |
| Filtering | ✅ SQL | Limited | ❌ | ✅ |
| Updates | ✅ Yes | Eventually | ❌ | ✅ |

**pgvector wins on:** cost, simplicity, SQL joins, existing infra
**Pinecone wins on:** managed scale, global replication, zero ops
**Qdrant wins on:** performance, filtering, open source

## For Local AI Agents

For personal AI agents running on MacBook:

```bash
# Docker setup (simplest)
docker run -d \\
  --name pgvector \\
  -e POSTGRES_PASSWORD=secret \\
  -p 5432:5432 \\
  -v pgdata:/var/lib/postgresql/data \\
  ankane/pgvector

# Or via Homebrew
brew install postgresql@16
CREATE EXTENSION vector;
```

Combined with [[ollama]] and [[local-llm-agents]], pgvector creates a fully local RAG stack:
1. [[ollama]] — LLM inference
2. pgvector — vector storage + retrieval
3. Custom agent — orchestration

## Related Concepts

- [[vector-db]] — Vector database landscape comparison
- [[rag]] — Retrieval-Augmented Generation patterns
- [[agent-memory]] — Agent memory architectures using vector storage
- [[ollama]] — Local LLM runtime
- [[local-llm-agents]] — AI agents on local models
