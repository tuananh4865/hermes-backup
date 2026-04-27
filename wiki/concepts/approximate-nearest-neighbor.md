---
title: Approximate Nearest Neighbor
description: Algorithms for fast similarity search in high-dimensional vector spaces
tags: [ai, embeddings, vector-search, algorithms]
---

# Approximate Nearest Neighbor (ANN)

ANN algorithms enable fast similarity search in high-dimensional vector spaces, trading exact accuracy for speed and scalability.

## Overview

Exact nearest neighbor search becomes computationally expensive at scale. ANN algorithms like HNSW, IVF, and FAISS provide sub-linear search times with tunable accuracy tradeoffs.

## Common Algorithms

- **HNSW**: Hierarchical Navigable Small World — graph-based, excellent for in-memory indices
- **IVF**: Inverted File Index — clusters vectors, searches within relevant clusters
- **PQ**: Product Quantization — compresses vectors for memory-efficient storage
- **LSH**: Locality-Sensitive Hashing — hash-based probabilistic search

## Use Cases

- RAG system retrieval at scale
- Similarity search in embedding spaces
- Recommendation systems
- Duplicate detection

## Related

- [[vector-database]]
- [[embeddings]]
- [[rag-systems]]
