---
title: "Agent Memory Patterns"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ai-agents, memory, llm, context-management]
---

# Agent Memory Patterns

## Overview

Agent Memory Patterns encompass the architectural techniques AI agents use to retain, recall, and leverage information across interactions. Unlike traditional software where memory is simply read/write state, agent memory must handle the complexity of natural language, the limitations of context windows, and the challenge of determining what information is relevant to future situations. Effective memory management determines whether an agent can maintain coherent long-term relationships, accumulate expertise, and deliver personalized experiences over extended timeframes.

The fundamental tension in agent memory is between comprehensiveness and accessibility. Storing everything is impossible—context windows are finite and retrieval costs grow with data volume. Yet storing too little loses critical context. Agent memory patterns provide structured approaches to navigating this tradeoff, segmenting memory into types optimized for different purposes and implementing retrieval mechanisms that surface relevant information when needed.

## Key Concepts

**Memory Segmentation**: Effective agents separate memory into distinct categories, each with different characteristics. Episodic memory captures specific past experiences—what happened, when, and in what context. Semantic memory stores general knowledge and facts accumulated over time. Working memory provides temporary storage for active reasoning and immediate context. This segmentation mirrors cognitive science research on human memory architecture and enables differentiated management strategies.

**Vector Embeddings and Semantic Search**: Modern agent memory often stores information as vector embeddings—numerical representations that capture semantic meaning. When a new situation arises, the agent can search memory for semantically similar past experiences, even when exact wording differs. This enables flexible, associative recall rather than brittle keyword matching. [[vector-databases]] like Pinecone, Weaviate, or Chroma provide infrastructure for this style of retrieval.

**Memory Consolidation**: Agents employ consolidation processes to transfer information from short-term to long-term memory, compressing experiences into higher-level abstractions. A conversation about user preferences might consolidate into a simple preference profile entry, reducing storage requirements while preserving essential information.

**Context Window Management**: With finite context, agents must actively manage what information occupies the limited available space. Techniques include summarization of older context, strategic placement of important information (often at the start or end of context where models attend more heavily), and explicit management of working memory structures.

**Personalization and User Modeling**: Long-running agents build models of user preferences, communication styles, and needs over time. These models inform responses without requiring explicit re-explanation in each interaction. Privacy considerations arise—users may not realize how much is being remembered and for how long.

## How It Works

A typical memory-enabled agent architecture includes several interacting components:

```
┌─────────────────────────────────────────────────────────────┐
│                      Agent Core                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Perceive  │→ │   Reason   │→ │       Act           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────┐               ┌─────────────────────────┐
│ Working Memory  │               │    Memory Controller    │
│ (Current ctx)   │               └─────────────────────────┘
└─────────────────┘                          │
                                             ▼
                              ┌─────────────────────────┐
                              │    Memory Store         │
                              ├─────────────────────────┤
                              │ • Episodic (vectors)    │
                              │ • Semantic (facts)       │
                              │ • Procedural (skills)    │
                              └─────────────────────────┘
```

The Memory Controller orchestrates reads and writes, deciding when to store information, when to retrieve from long-term memory, and how to integrate retrieved information into current context. It evaluates recency, relevance, frequency, and importance when determining what to surface.

## Practical Applications

**Customer Service Agents**: Retaining context across multiple support interactions enables agents to remember previous issues, recognize returning customers, and build rapport. A customer explaining a problem shouldn't need to re-explain their setup in each message.

**Personal Assistants**: Calendar agents that remember scheduling preferences, meeting patterns, and communication norms provide more natural, less fatiguing interactions. Code assistants that recall a project's architecture, coding conventions, and past decisions are more effective than fresh sessions each time.

**Research Agents**: Agents conducting literature review or extended analysis benefit from memory of earlier findings, avoiding redundant work and building coherent arguments across sessions.

**Game and Simulation Agents**: NPCs and game agents with memory of past player interactions behave more believably, reacting to previous encounters rather than treating each interaction as entirely new.

## Examples

```python
# Simplified memory retrieval pseudocode
class MemoryController:
    def __init__(self, vector_store, semantic_store):
        self.vector_store = vector_store
        self.semantic_store = semantic_store
    
    async def retrieve(self, query, current_context, limit=5):
        # Vector search for similar past experiences
        episodic_matches = await self.vector_store.search(
            query, 
            filter={"relevance_score": {"$gt": 0.7}},
            limit=limit
        )
        
        # Semantic search for relevant facts
        semantic_matches = await self.semantic_store.search(query, limit=3)
        
        # Merge and rank by predicted relevance
        combined = self.merge_and_rank(
            episodic_matches, 
            semantic_matches,
            current_context
        )
        
        # Return top candidates for context integration
        return combined[:limit]
    
    async def store(self, interaction):
        # Generate embeddings for episodic storage
        embedding = await self.embed(interaction.summary)
        await self.vector_store.insert({
            "embedding": embedding,
            "summary": interaction.summary,
            "timestamp": interaction.timestamp,
            "entities": extract_entities(interaction),
            "importance": interaction.estimated_importance
        })
```

## Related Concepts

- [[vector-databases]] - Infrastructure for semantic memory storage and retrieval
- [[context-window-management]] - Techniques for maximizing utility of limited context
- [[ai-agents]] - The broader systems within which memory patterns operate
- [[prompt-engineering]] - How memory integration is communicated to language models

## Further Reading

- [MemGPT Paper](https://arxiv.org/abs/2312.14869) - A system for infinite context in LLM applications
- [LangChain Memory Documentation](https://python.langchain.com/docs/modules/memory/) - Practical implementation patterns
- [Vector Database Comparisons](https://arxiv.org/abs/2303.13553) - Survey of vector storage options

## Personal Notes

Building memory-enabled agents reveals how human memory intuitions fail us. I initially designed an agent that remembered everything, assuming more memory equals better performance. The agent became slower, more expensive, and often more confused—retrieving contradicting past statements or surfacing irrelevant old context. The breakthrough came when I treated memory like a CDN: cache aggressively at multiple tiers, expire content strategically, and only serve what's likely relevant. The resulting agent felt smarter despite remembering far less.
