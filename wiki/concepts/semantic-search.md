---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 search (extracted)
  - 🔗 vector-db (extracted)
  - 🔗 embedding (extracted)
  - 🔗 rag (inferred)
last_updated: 2026-04-11
tags:
  - search
  - semantic
  - AI
  - retrieval
---

# Semantic Search

> Search that understands meaning, not just keywords.

## Overview

Semantic search understands the **meaning** behind queries and documents, not just keyword matching. It uses embeddings to represent query and documents in vector space, then finds the most similar results.

```
Keyword search: "cat food" → documents containing "cat food"

Semantic search: "cat food" → documents about:
- Pet nutrition
- Cat feeding
- Cat dietary needs
- Feline food brands
```

## How Semantic Search Works

### 1. Encode Query and Documents
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

query = "What do cats like to eat?"
query_embedding = model.encode([query])

documents = [
    "Cats prefer wet food to dry food.",
    "Dogs love playing fetch.",
    "Cats need protein in their diet."
]
doc_embeddings = model.encode(documents)
```

### 2. Find Similar Documents
```python
from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity([query_embedding], doc_embeddings)[0]

# Output: [0.92, 0.15, 0.88]
# Document 1 (0.92) and 3 (0.88) are most relevant
```

## Semantic vs Keyword Search

| Aspect | Keyword | Semantic |
|--------|---------|----------|
| **Matching** | Exact words | Meaning |
| **Query** | "weather today" | "should I bring an umbrella" |
| ** synonyms** | No | Yes |
| **Typos** | Exact only | Handles well |
| **Context** | None | Understands context |

## Implementation

### Simple Vector Search
```python
import numpy as np

def semantic_search(query, documents, top_k=5):
    # Encode
    query_vec = model.encode([query])
    doc_vecs = model.encode(documents)
    
    # Compute similarities
    scores = cosine_similarity(query_vec, doc_vecs)[0]
    
    # Get top-k
    top_idx = np.argsort(scores)[-top_k:][::-1]
    
    return [(documents[i], scores[i]) for i in top_idx]
```

### With Chroma DB
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("documents")

# Add documents
collection.add(
    ids=["1", "2", "3"],
    embeddings=doc_embeddings.tolist(),
    documents=documents
)

# Search
results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3
)
```

### With Pinecone
```python
import pinecone

pinecone.init(api_key="...", environment="...")
index = pinecone.Index("semantic-search")

# Upsert documents
index.upsert([
    (f"doc_{i}", vec.tolist(), {"text": doc})
    for i, (vec, doc) in enumerate(zip(doc_embeddings, documents))
])

# Query
results = index.query(
    vector=query_embedding.tolist(),
    top_k=5,
    include_metadata=True
)
```

## HyDE: Hypothetical Document Embeddings

Generate a hypothetical answer, use it for retrieval:

```python
def hyde_search(query, top_k=5):
    # Generate hypothetical answer
    hypothetical = llm.predict(
        f"If relevant, what would an ideal answer to '{query}' say?"
    )
    
    # Embed both query and hypothetical
    query_emb = model.encode([query])
    hypo_emb = model.encode([hypothetical])
    
    # Retrieve using hypothetical embedding
    results = vectorstore.similarity_search_by_vector(hypo_emb[0], k=top_k)
    
    return results
```

## Reranking

After initial retrieval, rerank for better results:

```python
from sentence_transformers import CrossEncoder

# Initial retrieval (top 20)
candidates = vectorstore.similarity_search(query, k=20)

# Rerank with cross-encoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = reranker.predict([[query, doc] for doc in candidates])

# Reorder
reranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
```

## Hybrid Search

Combine keyword + semantic:
```python
def hybrid_search(query, alpha=0.5):
    # Keyword (BM25)
    bm25_scores = bm25.get_scores(tokenize(query))
    
    # Semantic
    semantic_scores = cosine_similarity(
        model.encode([query]), doc_embeddings
    )[0]
    
    # Combine
    combined = alpha * normalize(bm25_scores) + (1-alpha) * semantic_scores
    
    return np.argsort(combined)[-10:][::-1]
```

## Evaluation

### Metrics
| Metric | What It Measures |
|--------|----------------|
| **Hit@K** | Relevant doc in top K |
| **MRR** | Rank of first relevant |
| **NDCG** | Graded relevance |
| **Recall@K** | % of relevant docs found |

### Benchmark Datasets
- **BEIR**: 17 datasets, diverse retrieval tasks
- **MS MARCO**: 9M queries, passage ranking

## Related Concepts

- [[search]] — Search algorithms (BM25, TF-IDF)
- [[vector-db]] — Vector storage for embeddings
- [[embedding]] — How to create embeddings
- [[rag]] — RAG uses semantic search for retrieval

## External Resources

- [BEIR Benchmark](https://github.com/UKPLab/beir)
- [Sentence Transformers](https://www.sbert.net/)
- [MTEB Benchmark](https://huggingface.co/blog/mteb)