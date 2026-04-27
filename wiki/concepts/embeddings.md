---
title: Embeddings
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [embeddings, vector, nlp, machine-learning, retrieval, rag]
---

# Embeddings

## Overview

Embeddings are numerical vector representations of text, images, or other data types that capture semantic meaning in a continuous high-dimensional space. Where traditional text representation might use simple bag-of-words or one-hot encoding (sparse, high-dimensional, lacking semantic relationships), embeddings map entities into dense vectors where similar concepts cluster near each other. This mathematical structure enables computers to perform semantic operations—finding related concepts, measuring similarity, and reasoning about relationships—using straightforward vector mathematics like cosine similarity or Euclidean distance.

The advent of modern transformer-based language models (BERT, GPT, sentence transformers) made embedding generation significantly more powerful. These models learn contextual representations that capture nuanced meaning, polysemy, and semantic relationships from massive text corpora. The result is embeddings that understand that "bank" in "river bank" differs semantically from "bank" in "investment bank"—context that simpler models miss.

Embeddings form the foundation of retrieval-augmented generation (RAG) systems, semantic search engines, recommendation systems, and numerous other applications where understanding meaning matters more than exact keyword matching.

## Key Concepts

### Vector Representation

An embedding converts input content into a vector—typically 768 to 1536 dimensions for modern sentence embeddings. Each dimension captures some aspect of meaning or usage. The magic is that these dimensions emerge during training rather than being manually specified.

```python
# Conceptual example using sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
sentences = ["machine learning optimizes models from data",
             "deep learning uses neural networks",
             "cooking involves preparing food with heat"]

embeddings = model.encode(sentences)
# embeddings[0] is now a 384-dimensional vector
```

### Similarity Metrics

With embeddings in vector space, we measure similarity:

- **Cosine Similarity**: Measures angle between vectors (0 to 1, where 1 is identical)
- **Dot Product**: Raw similarity score, affected by vector magnitude
- **Euclidean Distance**: Straight-line distance between points

### Embedding Models

Different models serve different purposes:

| Model | Dimensions | Use Case |
|-------|------------|----------|
| OpenAI text-embedding-ada-002 | 1536 | General purpose, production |
| Cohere embed-english-v3 | 1024 | Multilingual support |
| sentence-transformers/all-MiniLM-L6-v2 | 384 | Fast, local inference |
| BGE-large-zh | 1024 | Chinese language |

## How It Works

Embeddings are generated through neural networks trained on large corpora with objectives that encourage semantically similar items to have similar vectors:

1. **Contextual Learning**: Models like BERT learn by predicting words in context
2. **Contrastive Learning**: Modern models like SBERT use pairs of sentences to learn similarity
3. **Fine-tuning**: Domain-specific fine-tuning adapts general embeddings to specialized vocabularies

The resulting dense vectors capture semantic relationships such that analogies like "king - man + woman ≈ queen" become arithmetic operations on vectors.

## Practical Applications

Embeddings power modern AI systems:

- **RAG (Retrieval-Augmented Generation)**: Fetch relevant context from documents to augment LLM responses
- **Semantic Search**: Find results based on meaning, not exact keywords
- **Duplicate Detection**: Identify near-duplicate content across large datasets
- **Recommendation Systems**: Suggest similar items based on embedding proximity
- **Clustering**: Group related content without predefined categories

### Code Example: Simple RAG Retrieval

```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Knowledge base
documents = [
    "Python list comprehensions provide concise syntax for creating lists",
    "Context managers ensure proper resource cleanup using __enter__ and __exit__",
    "Decorators modify function behavior without changing their code",
    "Generators yield values lazily, improving memory efficiency"
]

# Index documents
doc_embeddings = model.encode(documents)

def retrieve(query, top_k=2):
    query_embedding = model.encode([query])
    similarities = np.dot(doc_embeddings, query_embedding.T).flatten()
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [documents[i] for i in top_indices]

# Usage
results = retrieve("how to manage resources in Python")
print(results)
```

## Related Concepts

- [[vector-database]] — Storing and querying embedding vectors efficiently
- [[retrieval]] — Retrieval-augmented generation context
- [[large-language-models]] — Models that use embeddings
- [[semantic-search]] — Search based on meaning rather than keywords
- [[rag-systems]] — Combining retrieval with generation

## Further Reading

- [Sentence-BERT Paper](https://arxiv.org/abs/1908.10084)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Embedding Model Comparison](https://txt.cohere.com/sentence-embeddings/)

## Personal Notes

When implementing embeddings, model choice matters significantly. Smaller models like MiniLM work well for experimentation but may miss nuanced relationships that larger models capture. Also consider embedding dimensions for storage planning—1M documents × 1536 dimensions × 4 bytes = ~6GB for vectors alone.
