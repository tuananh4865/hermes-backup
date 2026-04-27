---
title: Agent Memory Architecture
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent-memory, rag, agentic-ai, llm-architecture]
related:
  - [[self-improving-agents]]
  - [[rag]]
  - [[agentic-ai]]
---

# Agent Memory Architecture

Agent memory architecture determines how autonomous AI agents store, retrieve, and leverage information across interactions — the foundation of truly self-improving agents.

## Memory Layers

### 1. Short-Term Memory (STM)

- **Purpose**: Current session context
- **Implementation**: Sliding window attention, system prompt
- **Capacity**: Limited by context window (128K for GPT-4, 32K for Claude 3)
- **Decay**: Cleared between sessions

### 2. Long-Term Memory (LTM)

- **Purpose**: Persistent knowledge across sessions
- **Implementation**: Vector database (Pinecone, Chroma, Qdrant)
- **Retrieval**: Semantic search over embeddings
- **Update**: Periodic summarization and re-indexing

### 3. Episodic Memory

- **Purpose**: Specific experiences with outcomes
- **Storage**: (situation, action, result, lesson) tuples
- **Use**: Informs future decisions in similar contexts
- **Learning**: Patterns extracted from episodes become procedures

### 4. Semantic Memory

- **Purpose**: Generalized knowledge and facts
- **Implementation**: Structured knowledge graphs or vector stores
- **Content**: Extracted entities, relationships, rules
- **Updates**: Incremental learning from episodes

## RAG for Agents

Retrieval-Augmented Generation extends agent memory:

```
Query → Retrieve relevant docs → Augment prompt → Generate response
```

### Agent-Specific RAG Patterns

- **Tool documentation RAG** — Agent retrieves API specs before tool use
- **History RAG** — Retrieve past successes/failures for similar tasks
- **Knowledge base RAG** — Domain-specific knowledge retrieval
- **Memory consolidation** — Periodically distill recent episodes into LTM

## Architecture Comparison

| Architecture | Memory Type | Use Case |
|-------------|-------------|----------|
| ReAct | Minimal STM | Simple single-step tasks |
| Reflexion | STM + episodic | Learning from failures |
| AutoGPT | STM + LTM (RAG) | Complex multi-step projects |
| Voyager | STM + LTM + skills | Minecraft-style open world |

## Key Design Decisions

1. **Retrieval quality vs speed** — Semantic search adds latency
2. **Memory compression** — Summarize old episodes to save space
3. **Forgetting vs remembering** — Not all experiences are worth keeping
4. **Consistency maintenance** — LTM updates shouldn't contradict facts

## Implementation Patterns

```python
# Simplified agent memory loop
class AgentMemory:
    def recall(self, query):
        return vector_store.similarity_search(query, k=5)
    
    def memorize(self, episode):
        embedding = embed(episode)
        vector_store.add(embedding)
        
    def consolidate(self):
        # Periodically summarize old episodes
        old_episodes = vector_store.get_oldest(100)
        summary = llm.summarize(old_episodes)
        vector_store.replace(old_episodes, summary)
```

## Related

- [[self-improving-agents]] — Self-improvement built on memory
- [[rag]] — RAG fundamentals
- [[agentic-ai]] — Agent architectures
