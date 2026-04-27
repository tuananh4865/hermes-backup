---
title: Vector Database
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [vector-database, embeddings, semantic-search, pinecone, chromadb, retrieval]
---

# Vector Database

## Overview

A vector database is a specialized storage system designed to efficiently store, index, and query high-dimensional embedding vectors. Unlike traditional databases that excel at exact-match queries and structured data, vector databases are optimized for similarity search—finding the most similar items to a given query vector. This capability makes them essential infrastructure for AI applications that rely on semantic understanding: retrieval-augmented generation (RAG), semantic search, recommendation systems, and anomaly detection.

The core challenge vector databases solve is that similarity search in high-dimensional space is computationally expensive. A naive approach comparing a query vector against every stored vector scales linearly with the database size, making it impractical for large collections. Vector databases employ sophisticated indexing structures and approximate nearest neighbor (ANN) algorithms to achieve sub-linear search times, often sacrificing a small amount of accuracy for dramatic speed improvements.

## Key Concepts

### Approximate Nearest Neighbor (ANN) Indexing

Vector databases use ANN algorithms rather than exact search because exact matching becomes prohibitively slow above a few thousand vectors:

| Algorithm | Description | Speed/Accuracy Tradeoff |
|-----------|-------------|------------------------|
| HNSW | Hierarchical Navigable Small World—graph-based, excellent accuracy | Fast with high recall |
| IVF | Inverted File Index—partitions space into clusters | Balanced |
| PQ | Product Quantization—compresses vectors for memory efficiency | Memory-optimized |
| LSH | Locality-Sensitive Hashing—hash-based probabilistic search | Fast, lower accuracy |

### Indexing Strategies

Modern vector databases combine multiple techniques:

```python
# Example: Creating an index in ChromaDB
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()

collection = client.create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # Use cosine similarity
)

# Add documents
doc_embeddings = model.encode(["doc1 text", "doc2 text", "doc3 text"])
collection.add(
    embeddings=doc_embeddings.tolist(),
    documents=["doc1 text", "doc2 text", "doc3 text"],
    ids=["1", "2", "3"]
)
```

### Metadata Filtering

Production vector databases support hybrid queries—combining vector similarity with traditional metadata filters. This enables scenarios like "find products similar to this one, but only from category electronics, priced under $100."

## How It Works

Vector databases store embeddings alongside optional metadata:

1. **Ingestion**: Documents are embedded via an external model, producing vectors
2. **Indexing**: Vectors are indexed using ANN algorithms (HNSW being most common)
3. **Querying**: Query embedding is compared against indexed vectors
4. **Filtering**: Optional metadata filters narrow the candidate set
5. **Ranking**: Results ranked by similarity score and returned

### Distance Metrics

Vectors are compared using various distance metrics:

- **Cosine Similarity**: Measures angle between vectors (0° = identical, 90° = orthogonal)
- **Dot Product**: Raw inner product, good for normalized vectors
- **Euclidean Distance**: Straight-line distance, sensitive to magnitude

## Practical Applications

Vector databases are foundational for modern AI applications:

### RAG Systems

```python
# Complete RAG pipeline with vector DB
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.get_collection("knowledge_base")

def rag_query(question, top_k=5):
    # Embed question
    query_embedding = model.encode([question])
    
    # Retrieve similar documents
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )
    
    # Combine context with question for LLM
    context = "\n\n".join(results['documents'][0])
    return f"Context: {context}\n\nQuestion: {question}"
```

### Semantic Search

Replacing keyword-based search with meaning-based retrieval. A query for "financial advisory" returns documents about investment management even if that exact phrase doesn't appear.

### Recommendation Systems

Finding similar items based on embedding proximity—recommended products, content, or connections based on learned representations.

## Popular Vector Databases

| Database | Deployment | Notable Features |
|----------|------------|------------------|
| Pinecone | Cloud-native | Managed service, serverless option |
| Weaviate | Self-hosted or cloud | Hybrid search (vector + keyword) |
| ChromaDB | Local/embedded | Lightweight, great for prototyping |
| pgvector | PostgreSQL extension | Leverage existing Postgres infrastructure |
| Qdrant | Self-hosted or cloud | Rust-based, high performance |
| Milvus | Self-hosted | Cloud-native, very scalable |

## Related Concepts

- [[embeddings]] — Vector representations stored in vector databases
- [[retrieval]] — RAG context and retrieval mechanisms
- [[semantic-search]] — Search powered by vector similarity
- [[rag-systems]] — Combining retrieval with language models
- [[approximate-nearest-neighbor]] — The algorithmic foundation

## Further Reading

- [Pinecone Vector Database Guide](https://www.pinecone.io/learn/vector-database/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [HNSW Algorithm Explained](https://www.pinecone.io/learn/vector-indexes/)
- [Ann-Benchmark Results](https://ann-benchmarks.com/)

## Personal Notes

Vector databases are deceptively simple in concept but operationally complex. A few practical considerations: index construction time can be significant for large datasets (hours for billions of vectors), and the accuracy/speed tradeoff in ANN requires tuning. Also, embedding model choice matters—garbage in, garbage out. Consider using domain-adapted embeddings for specialized applications.
