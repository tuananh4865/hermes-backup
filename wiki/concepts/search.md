---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 rag (extracted)
  - 🔗 vector-db (extracted)
  - 🔗 embedding (extracted)
  - 🔗 seo (inferred)
last_updated: 2026-04-11
tags:
  - search
  - information-retrieval
  - algorithms
  - ranking
---

# Search

> Information retrieval systems, algorithms, and implementation.

## Overview

Search is the problem of finding relevant information from a collection. Key types:
- **Full-text search**: Find documents containing query terms
- **Semantic search**: Find documents semantically similar to query
- **Faceted search**: Filter by categories/attributes
- **Vector search**: Similarity in embedding space

## Search Algorithms

### TF-IDF (Term Frequency-Inverse Document Frequency)

Classic IR algorithm:
```python
def tf_idf(term, document, corpus):
    tf = document.count(term) / len(document)
    idf = log(len(corpus) / sum(1 for doc in corpus if term in doc))
    return tf * idf
```

**Scoring:**
- High TF: Term appears frequently in document
- High IDF: Term is rare across corpus

### BM25 (Best Matching 25)

Improved probabilistic model:
```python
from rank_bm25 import BM25Okapi

corpus = ["doc1 text", "doc2 text", "doc3 text"]
tokenized_corpus = [doc.split() for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

scores = bm25.get_scores(query.split())
```

**Advantages over TF-IDF:**
- Sublinear TF scaling (diminishing returns)
- Document length normalization
- Term frequency saturation

### Vector Search

Represent queries and documents as embeddings, find nearest neighbors:

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

docs = ["doc1 content", "doc2 content", "doc3 content"]
query = "search query"

doc_embeddings = model.encode(docs)
query_embedding = model.encode([query])

# Cosine similarity
similarities = np.dot(doc_embeddings, query_embedding) / (
    np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_embedding)
)
```

## Search Systems

### Elasticsearch

Production-grade full-text search:
```bash
# Create index
curl -X PUT "localhost:9200/my-index"

# Index document
curl -X POST "localhost:9200/my-index/_doc/1" \
  -H 'Content-Type: application/json' \
  -d '{"content": "document text"}'

# Search
curl -X GET "localhost:9200/my-index/_search?q=query"
```

### Meilisearch

Lightweight, fast search:
```python
import meilisearch

client = meilisearch.Client('http://localhost:7700')
index = client.index('documents')

# Add documents
index.add_documents([{"id": 1, "content": "..."}])

# Search
results = index.search("query")
```

### Typesense

Designed for instant search:
```python
import typesense

client = typesense.Client({
    'master_node': {'host': 'localhost', 'port': '8107'},
    'nearest_node': {'host': 'localhost', 'port': '8107'}
})
```

## Semantic Search with Vector Databases

### Pinecone
```python
import pinecone

pinecone.init(api_key="...", environment="...")
index = pinecone.Index("my-index")

# Query
results = index.query(
    vector=query_embedding.tolist(),
    top_k=10,
    include_metadata=True
)
```

### Weaviate
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Query
result = client.query.get("Article", ["title", "content"]) \
    .with_near_text({"concepts": ["search query"]}) \
    .do()
```

## Ranking Factors

### Document Ranking
| Factor | Description |
|--------|-------------|
| **Relevance** | How well document matches query |
| **Freshness** | How recent is the document |
| **Authority** | Page rank, domain reputation |
| **Popularity** | Click-through, engagement |
| **Location** | Geographic relevance |

### Web Search Ranking (Google-style)

Major factors:
1. **Content relevance** — keyword matching, semantic similarity
2. **Page quality** — E-E-A-T (Experience, Expertise, Authority, Trust)
3. **User engagement** — CTR, dwell time, bounce rate
4. **Technical SEO** — crawlability, speed, mobile-friendliness
5. **Link signals** — backlinks, anchor text

## Search UX Patterns

### Search Bar
```
┌────────────────────────────────────────┐
│ 🔍 Search...                        │
└────────────────────────────────────────┘
```

### Autocomplete
```javascript
// Show suggestions as user types
input.addEventListener('input', async (e) => {
  const suggestions = await searchAPI.suggest(e.target.value);
  showDropdown(suggestions);
});
```

### Filters/Facets
```
Category: [All ▼]
  □ Electronics (124)
  □ Clothing (89)
  □ Books (56)

Price Range: [────●────]
  $0        $500

In Stock Only: [✓]
```

## Evaluation Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Precision@K** | Relevant in top-K / K | How many top results are relevant |
| **Recall@K** | Relevant in top-K / Total relevant | Did we find all relevant docs |
| **MAP** | Mean Average Precision | Overall ranking quality |
| **NDCG** | Normalized DCG | Graded relevance (not binary) |

## Search for AI

### RAG Search Pipeline
```
Query → Embed → Vector DB → Top-K docs → LLM → Response
```

### Hybrid Search
Combine keyword + vector search:
```python
def hybrid_search(query, alpha=0.5):
    # BM25 score
    bm25_score = bm25.get_scores(query.split())
    
    # Vector score
    vector_score = cosine_similarity(query_embedding, doc_embeddings)
    
    # Combine
    return alpha * normalize(bm25_score) + (1-alpha) * normalize(vector_score)
```

## Related Concepts

- [[rag]] — RAG uses search for retrieval
- [[vector-db]] — Vector databases for semantic search
- [[embedding]] — How text is converted to vectors
- [[seo]] — Search engine optimization

## External Resources

- [Elasticsearch](https://www.elastic.co)
- [Meilisearch](https://www.meilisearch.com)
- [Typesense](https://typesense.org)
- [BM25 Paper](https://dl.acm.org/doi/10.1145/290941.290970)
