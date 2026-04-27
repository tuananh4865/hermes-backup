---
title: "Similarity Search"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [similarity-search, vector-databases, embeddings, nearest-neighbor, machine-learning]
---

## Overview

Similarity search is the problem of finding items in a dataset that are most similar to a given query item. In the context of machine learning, items are typically represented as vectors in a high-dimensional embedding space, and similarity is measured by distance metrics. This technique is foundational to recommendation systems, image retrieval, semantic search, and the retrieval component of RAG systems.

The core challenge is that naive similarity search—computing distance to every item—is computationally infeasible for large datasets with millions or billions of vectors. Efficient similarity search requires approximate nearest neighbor (ANN) algorithms that sacrifice some accuracy for dramatically better performance, making it possible to query massive vector databases in milliseconds.

## Key Concepts

**Embedding Space** is a vector space where semantically similar items are positioned near each other. Text, images, audio, and code can all be converted to dense vectors using neural networks. The geometry of this space captures semantic relationships—a query vector for "cat" will be closer to "dog" than to "automobile" because cats and dogs share semantic features.

**Distance Metrics** quantify similarity between vectors. Common options include:
- **Cosine Similarity**: Measures the angle between vectors, focusing on direction rather than magnitude. Range: -1 to 1.
- **Euclidean Distance**: Straight-line distance in vector space. Affected by vector magnitude.
- **Dot Product**: Projects one vector onto another. For normalized vectors, relates to cosine similarity.
- **Manhattan Distance**: Sum of absolute component differences. More robust to outliers.

**Approximate Nearest Neighbor (ANN)** algorithms trade exactness for speed. Unlike exact nearest neighbor search that guarantees finding the true k nearest items, ANN returns items that are very close most of the time. Popular ANN algorithms include HNSW (Hierarchical Navigable Small World), IVF (Inverted File Index), and LSH (Locality-Sensitive Hashing).

**Embedding Models** create the vector representations. For text, models like OpenAI's text-embedding-ada-002, sentence-transformers, or open-source options like BGE generate high-quality text embeddings. Image models like CLIP produce embeddings that align images and text in the same vector space.

## How It Works

Vector databases index embeddings to enable fast retrieval. The HNSW algorithm, used by many vector databases, builds a multi-layer graph structure:

```python
# Example: Basic similarity search with FAISS (Facebook AI Similarity Search)
import faiss
import numpy as np

# Create 10,000 random 128-dimensional vectors (simulating embeddings)
dimension = 128
num_vectors = 10_000
embeddings = np.random.rand(num_vectors, dimension).astype('float32')

# Normalize for cosine similarity
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized_embeddings = embeddings / norms

# Build HNSW index
index = faiss.IndexHNSWFlat(dimension, 32)  # 32 = number of connections per node
index.add(normalized_embeddings)

# Search for 5 nearest neighbors to a query vector
query = np.random.rand(1, dimension).astype('float32')
query = query / np.linalg.norm(query, axis=1, keepdims=True)

distances, indices = index.search(query, k=5)

print(f"Indices of nearest neighbors: {indices}")
print(f"Distances: {distances}")
```

More advanced implementations use hybrid search combining dense vectors with sparse BM25 scores:

```python
# Hybrid search combining dense and sparse retrieval
from rank import reciprocal_rank_fusion

def hybrid_search(query, dense_index, sparse_index, k=10):
    # Dense retrieval using vector similarity
    dense_results = dense_index.search(query, k=k*2)

    # Sparse retrieval using BM25 keyword matching
    sparse_results = sparse_index.search(query, k=k*2)

    # Reciprocal Rank Fusion combines rankings
    fused_scores = reciprocal_rank_fusion(
        [dense_results, sparse_results],
        weights=[0.7, 0.3]  # Weight dense higher for semantic queries
    )

    return sorted(fused_scores, key=lambda x: x['score'], reverse=True)[:k]
```

## Practical Applications

Similarity search powers modern AI applications. **Semantic search engines** use embeddings to retrieve documents based on meaning rather than keywords. **Recommendation systems** find items similar to user preferences. **Image search** retrieves visually similar images. **RAG systems** use similarity search to find relevant context passages.

In fraud detection, transactions are embedded and compared to known fraud patterns—similar transactions flagged for review. In drug discovery, molecular structures are embedded to find similar compounds with known properties.

## Examples

Building a semantic document search system:

```python
from sentence_transformers import SentenceTransformer
import faiss
import json

class SemanticSearchEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def index_documents(self, documents):
        """Index a list of documents"""
        self.documents = documents
        embeddings = self.model.encode(documents)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for normalized vectors

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search(self, query, top_k=5):
        """Find most similar documents to query"""
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):  # Valid index
                results.append({
                    'document': self.documents[idx],
                    'score': float(score)
                })

        return results

# Usage
engine = SemanticSearchEngine()
engine.index_documents([
    "Machine learning models require careful tuning of hyperparameters.",
    "Deep learning excels at processing unstructured data like images and text.",
    "Cloud computing provides on-demand access to servers and storage.",
    "Natural language processing enables computers to understand human language.",
    "Database systems organize and store data for efficient retrieval."
])

results = engine.search("What is deep learning good at?")
for r in results:
    print(f"[{r['score']:.4f}] {r['document'][:60]}...")
```

## Related Concepts

- [[embeddings]] - Vector representations enabling similarity computation
- [[vector-databases]] - Storage systems optimized for vector operations
- [[nearest-neighbor-algorithms]] - Exact and approximate NN search techniques
- [[distance-metrics]] - Mathematical measures of vector similarity
- [[rag-implementation]] - Similarity search as a component of RAG

## Further Reading

- "Approximate Nearest Neighbor Search in Vector Spaces" by Kushilevitz et al.
- Facebook AI Similarity Search (FAISS) documentation
- "Vector Databases Compared" - comprehensive comparison of vector DB options
- Ann-Benchmarks.com for algorithm performance comparisons

## Personal Notes

Choosing the right similarity metric matters. For text embeddings from models like OpenAI's, cosine similarity is standard because the models produce normalized vectors. For unnormalized embeddings (like raw neural network outputs), dot product or Euclidean distance may be more appropriate. Always normalize before indexing if you plan to use cosine similarity—floating point errors accumulate and affect results at scale.
