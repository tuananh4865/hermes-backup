---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 knowledge-base (extracted)
  - 🔗 vector-db (extracted)
  - 🔗 embedding (extracted)
  - 🔗 llm (extracted)
  - 🔗 agentic-rag (extracted)
last_updated: 2026-04-11
tags:
  - AI
  - RAG
  - retrieval
  - knowledge-base
---

# RAG (Retrieval-Augmented Generation)

> RAG combines a language model with external knowledge retrieval to produce more accurate, grounded responses.

## Overview

RAG (Retrieval-Augmented Generation) is a technique that enhances LLM responses by:
1. **Retrieving** relevant documents from a knowledge base
2. **Augmenting** the prompt with retrieved context
3. **Generating** a response grounded in that context

This addresses LLM limitations like hallucination and outdated knowledge by grounding responses in verified data.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Query     │────►│   Retrieve   │────►│   Retrieve  │
│             │     │   (Vector    │     │   Top-K     │
│ "What is   │     │    DB)       │     │   Docs      │
│  RAG?"     │     └──────────────┘     └──────┬──────┘
└─────────────┘                                  │
                                                   ▼
                    ┌──────────────┐     ┌─────────────┐
                    │     LLM      │◄────│   Prompt    │
                    │   Generate  │     │  (Query +   │
                    │              │     │   Context)  │
                    └──────────────┘     └─────────────┘
```

## Implementation

### 1. Document Ingestion

```python
from langchain.document_loaders import PDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Load documents
loader = PDFLoader("document.pdf")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# Create embeddings and store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
```

### 2. Retrieval

```python
# Query the vector store
query = "What are the key benefits of RAG?"
results = vectorstore.similarity_search(query, k=5)

# Get the retrieved context
context = "\n\n".join([doc.page_content for doc in results])
```

### 3. Generation with Context

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4")

prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""

response = llm.predict(prompt)
```

## Vector Databases

| Database | Best For | Notes |
|----------|----------|-------|
| **Pinecone** | Production scale | Managed, cloud |
| **Chroma** | Prototyping | Local, simple |
| **Weaviate** | Hybrid search | Graph + vector |
| **Qdrant** | High performance | Rust-based |
| **FAISS** | Local, fast | Facebook's library |

## Chunking Strategies

### Fixed-Size Chunks
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

### Semantic Chunking
Split by natural boundaries:
- Paragraphs
- Sentences
- Code blocks

### Hierarchical Chunking
```
Document
├── Chapter
│   ├── Section
│   │   └── Paragraph
│   └── Section
└── Chapter
```

## Embedding Models

| Model | Dimensions | Best For |
|-------|------------|----------|
| **text-embedding-ada-002** | 1536 | General |
| **text-embedding-3-small** | 1536/512 | Speed |
| **text-embedding-3-large** | 3072 | Quality |
| **BGE** | 1024 | Open source |

## RAG vs Fine-Tuning

| Factor | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Data freshness** | Can update knowledge base | Needs retraining |
| **Hallucination** | Lower (grounded in context) | May still hallucinate |
| **Cost** | Embedding + retrieval | Training compute |
| **Latency** | Retrieval + generation | Generation only |
| **Maintenance** | Update documents | Retrain model |
| **Use case** | Dynamic knowledge | Specific style/format |

**Rule of thumb:** Use RAG when knowledge changes frequently. Use fine-tuning when you need consistent behavior/style.

## Advanced RAG Patterns

### 1. Query Expansion
```python
# Generate multiple queries for better retrieval
queries = [
    query,
    f"What is {entity}?",
    f"How does {entity} work?"
]
```

### 2. HyDE (Hypothetical Document Embeddings)
```python
# Generate hypothetical answer, use it for retrieval
hypothetical = llm.predict(f"Answer: {query}")
# Retrieve docs similar to hypothetical answer
```

### 3. Reranking
```python
from sentence_transformers import CrossEncoder

# Retrieve top 20
candidates = vectorstore.similarity_search(query, k=20)

# Rerank with cross-encoder
reranker = CrossEncoder('cross-encoder/ms-marco')
reranked = reranker.rank(query, [doc.text for doc in candidates])
```

### 4. Hybrid Search
```python
# Combine dense (vector) and sparse (BM25) retrieval
results = 0.7 * vector_search(query) + 0.3 * keyword_search(query)
```

## Production Considerations

### Latency Optimization
- Async retrieval
- Caching (frequently asked questions)
- Smaller embedding models for speed

### Accuracy Optimization
- Query expansion
- Reranking
- Hybrid search
- Human feedback loop

### Cost Management
- Choose smaller embedding models
- Limit context window usage
- Cache retrieval results

## Evaluation Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Hit Rate** | % queries with relevant doc in top-k |
| **MRR** | Mean Reciprocal Rank of first relevant doc |
| **NDCG** | Normalized Discounted Cumulative Gain |
| **Faithfulness** | Does answer match retrieved context? |

## RAG for Agents

RAG is foundational for knowledge-intensive agents:

```python
# Agentic RAG loop
while not task_complete:
    context = retrieve(task)
    action = llm.decide(context + task)
    result = execute(action)
    task = update(task, result)
```

See [[agentic-rag]] for detailed patterns.

## Related Concepts

- [[knowledge-base]] — Building effective knowledge bases
- [[vector-db]] — Vector database deep dive
- [[embedding]] — How embeddings work
- [[llm]] — Large language models
- [[agentic-rag]] — RAG with agentic capabilities

## External Resources

- [RAG Survey](https://arxiv.org/abs/2312.10997)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)
- [RAG vs Fine-tuning](https://arxiv.org/abs/2401.04088)
