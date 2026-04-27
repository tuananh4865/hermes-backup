---
title: RAG Systems
description: Retrieval-Augmented Generation systems combining vector search with LLM generation
tags: [ai, llm, rag, retrieval]
---

# RAG Systems

Retrieval-Augmented Generation (RAG) systems combine vector-based retrieval with large language model generation to produce more accurate, grounded outputs.

## Overview

RAG systems retrieve relevant documents from a knowledge base and feed them alongside the user's query to an LLM, enabling responses grounded in specific context rather than model weights alone.

## Key Concepts

- **Vector Embedding**: Text converted to dense numerical vectors representing semantic meaning
- **Retrieval**: Finding most similar documents to a query vector using cosine similarity or other metrics
- **Augmented Generation**: Retrieved context prepended to prompt before LLM generation

## When to Use

- Grounding responses in specific documents or knowledge bases
- Reducing LLM hallucinations by citing retrieved evidence
- Accessing proprietary or frequently-updated information

## Related

- [[embeddings]]
- [[vector-database]]
- [[rag]]
- [[agentic-rag]]
