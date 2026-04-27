---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 vector-db (extracted)
  - 🔗 transformer (extracted)
  - 🔗 embedding (extracted)
  - 🔗 similarity-search (inferred)
last_updated: 2026-04-11
tags:
  - AI
  - embeddings
  - machine-learning
  - NLP
---

# Embedding

> Vector representations of text, images, or other data that capture semantic meaning.

## Overview

Embeddings convert discrete data (text, images) into dense vectors of numbers that computers can process. The magic is that **similar concepts have similar vectors**.

```
Text → Embedding Model → Vector [0.1, -0.3, 0.5, ...]

"Dog" → [0.2, 0.1, -0.4, ...]
"Cat" → [0.18, 0.12, -0.38, ...]  # Similar!
"Pizza" → [-0.3, 0.8, 0.1, ...]  # Different!
```

## How Embeddings Work

### From Words to Vectors

**Old approach (one-hot):**
```
"dog" = [1, 0, 0, 0, ...]
"cat" = [0, 1, 0, 0, ...]
# Problems: No similarity, huge size
```

**Modern embeddings:**
```
"dog" → [0.2, 0.1, -0.4, 0.7, ...]  # 1536 dimensions typically
"cat" → [0.18, 0.12, -0.38, 0.65, ...]
# Similar vectors = similar meaning!
```

### Embedding Models

| Model | Dimensions | Best For | Provider |
|-------|------------|----------|----------|
| **text-embedding-ada-002** | 1536 | General purpose | OpenAI |
| **text-embedding-3-small** | 1536/512 | Speed | OpenAI |
| **text-embedding-3-large** | 3072 | Quality | OpenAI |
| **BGE-large** | 1024 | Open source | BAAI |
| **e5-mistral** | 1024 | Open source | Microsoft |
| **GTE-large** | 1024 | Open source | Thenlper |

## Creating Embeddings

### OpenAI API
```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="The quick brown fox jumps over the lazy dog"
)

vector = response.data[0].embedding
print(f"Vector size: {len(vector)}")  # 3072
```

### Hugging Face
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = ["Hello world", "Hi there"]
embeddings = model.encode(sentences)

print(embeddings.shape)  # (2, 384)
```

### Local with Ollama
```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "Hello world"
}'
```

## Embedding Applications

### 1. Semantic Search
```python
# Index documents
doc_embeddings = model.encode(documents)

# Search query
query_embedding = model.encode([query])

# Find similar
similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
top_k = sorted(enumerate(similarities), key=lambda x: -x[1])[:5]
```

### 2. RAG (Retrieval-Augmented Generation)
```python
# Store in vector database
vectorstore = Chroma.from_documents(chunks, embeddings)

# Retrieve relevant context
results = vectorstore.similarity_search(query, k=5)
context = "\n\n".join([r.page_content for r in results])
```

### 3. Clustering
```python
from sklearn.cluster import KMeans

embeddings = model.encode(texts)
clusters = KMeans(n_clusters=5).fit_predict(embeddings)
```

### 4. Recommendation
```python
# Find similar items
item_embedding = model.encode([item])
recommendations = find_similar(item_embedding, all_items, k=10)
```

## Embedding Dimensions

| Use Case | Recommended Dimensions | Notes |
|----------|----------------------|-------|
| Semantic search | 768-1536 | Balance speed/quality |
| Memory systems | 384-768 | Faster similarity |
| Embedding only | 256-512 | When not searching |
| High precision | 3072+ | Slower but better |

## Similarity Metrics

### Cosine Similarity (Most Common)
```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity("dog", "cat")  # ~0.85
similarity("dog", "pizza")  # ~0.30
```

### Dot Product
```python
def dot_product(a, b):
    return np.dot(a, b)
# Good for normalized vectors
```

### Euclidean Distance
```python
from scipy.spatial.distance import euclidean

distance = euclidean(vec1, vec2)
# Lower = more similar
```

## Fine-tuning Embeddings

For domain-specific tasks:

```python
from sentence_transformers import SentenceTransformer, InputExample
from sentence_transformers import TripletLoss

# Create training examples
examples = [
    InputExample(texts=["machine learning", "artificial intelligence"]),
    InputExample(texts=["cat", "kitten"]),
]

# Fine-tune
model = SentenceTransformer('all-MiniLM-L6-v2')
model.fit(examples)
```

## Embedding Cache

Reduce API calls by caching:

```python
from functools import lru_cache

@lru_cache(maxsize=10000)
def get_embedding(text):
    return openai.embeddings.create(input=text).data[0].embedding
```

## Related Concepts

- [[vector-db]] — Stores embeddings for search
- [[transformer]] — Architecture behind modern embeddings
- [[rag]] — Embeddings power RAG retrieval
- [[similarity-search]] — Finding similar vectors

## External Resources

- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Hugging Face Sentence Transformers](https://www.sbert.net/)
- [MTEB Benchmark](https://huggingface.co/blog/mteb) — Embedding evaluation