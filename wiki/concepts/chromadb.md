---
title: "ChromaDB"
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [vector-database, rag, embeddings, python, local-ai]
related:
  - [[rag-retrieval-augmented-generation]]
  - [[local-llm]]
  - [[ollama]]
  - [[qdrant]]
  - [[pinecone]]
  - [[agent-memory]]
sources:
  - https://docs.trychroma.com/
---

# ChromaDB

ChromaDB is an open-source **vector database** designed for AI applications — particularly [[rag-retrieval-augmented-generation]] and embedding-based search. It stores embeddings (vector representations of text, images, or any data) and enables fast similarity search.

## Why ChromaDB?

**For local AI stacks**, ChromaDB is the go-to vector DB because:

- **Simple API** — Python-first, easy to get started in minutes
- **Local-first** — Runs entirely in-process, no server needed
- **Free & open source** — MIT license, no API costs
- **LLM-compatible** — Works with LangChain, LlamaIndex, and raw embeddings

## Installation

```bash
pip install chromadb chromadb[duckdb]

# Optional: for faster embedding queries
pip install chromadb[hnswlib]
```

## Basic Usage

### Create a Collection and Add Data

```python
import chromadb

# Persistent client (saves to disk)
client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection
collection = client.create_collection(
    name="my_docs",
    metadata={"description": "My document embeddings"}
)

# Add documents with metadata
collection.add(
    documents=[
        "ChromaDB is a vector database for AI.",
        "RAG combines retrieval and generation.",
        "Embeddings convert text to vectors.",
    ],
    metadatas=[
        {"source": "chroma-docs", "category": "overview"},
        {"source": "rag-guide", "category": "technique"},
        {"source": "embeddings-guide", "category": "technique"},
    ],
    ids=["doc1", "doc2", "doc3"]
)
```

### Query for Similar Documents

```python
# Query by text (auto-embeds the query)
results = collection.query(
    query_texts=["What is ChromaDB?"],
    n_results=2
)

# Results
print(results)
# {'ids': [['doc1', 'doc2']], 'documents': [...], 'metadatas': [...], 'distances': [...]}
```

### Query by Embeddings

```python
# Query with pre-computed embeddings
collection.query(
    query_embeddings=[[0.1, 0.2, ...]],
    n_results=2
)
```

## ChromaDB with LangChain

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Use Ollama for embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create vector store
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Add documents
vectorstore.add_documents(texts=[...], ids=[...])

# Similarity search
results = vectorstore.similarity_search("your query", k=3)
```

## ChromaDB with LlamaIndex

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# Load from Chroma
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=[vector_store])

# Create index
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Your question")
```

## Deployment Options

### Local (Development)

```python
# In-process, no server
client = chromadb.Client()
```

### Persistent (Production on a Single Machine)

```python
# Persists to disk
client = chromadb.PersistentClient(path="/data/chroma_db")
```

### Client-Server Mode

```python
# Server (run in background)
# pip install chromadb[server]
# chromadb --host 0.0.0.0 --port 8000

# Client
import chromadb
client = chromadb.HttpClient(host="localhost", port=8000)
```

### Docker

```bash
docker run -p 8000:8000 chromadb/chroma
```

## Embedding Models

ChromaDB works with any embedding model:

| Model | Use Case | Setup |
|-------|----------|-------|
| **nomic-embed-text** | General purpose, high quality | `ollama pull nomic-embed-text` |
| **all-MiniLM-L6-v2** | Fast, lightweight | `sentence-transformers` |
| **text-embedding-3-small** | OpenAI API | `openai` Python package |
| **embeddings-api** | Custom/managed | Any API |

```python
# With Ollama embeddings
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
```

## RAG Pipeline with ChromaDB

Full [[rag-retrieval-augmented-generation]] example:

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# 1. Load and chunk documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 2. Create vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 3. Create retriever + QA chain
llm = Ollama(model="qwen2.5:14b")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 4. Ask questions
answer = qa_chain.run("What is ChromaDB used for?")
```

## Limitations

- **Single-machine only** — No native distributed mode (use Qdrant or Pinecone for scale)
- **No built-in authentication** — Add nginx/Cloudflare for API security
- **Query performance** — Slower than dedicated vector DBs on large datasets (1M+ vectors)
- **Metadata filtering** — Limited compared to Pinecone or Weaviate

## ChromaDB vs Alternatives

| Feature | ChromaDB | Qdrant | Pinecone |
|---------|----------|--------|----------|
| **Deployment** | Local/Docker | Self-hosted/Cloud | Cloud only |
| **Pricing** | Free | $25/mo+ | $70/mo+ |
| **Scale** | <1M vectors | 10M+ vectors | Unlimited |
| **Performance** | Good | Excellent | Excellent |
| **Filtering** | Basic | Advanced | Advanced |
| **Cloud-native** | ❌ | ✅ | ✅ |

**When to use ChromaDB:** Local dev, small-scale RAG (<100K docs), prototyping, solo developers.
**When to use Qdrant:** Self-hosted production, need filtering, larger scale.
**When to use Pinecone:** Fully-managed, no ops team, production at scale.

## Related Concepts

- [[rag-retrieval-augmented-generation]] — The technique ChromaDB enables
- [[local-llm]] — Combining with local LLM inference
- [[ollama]] — Local LLM runtime
- [[agent-memory]] — Using vector DBs as agent memory
- [[qdrant]] — Alternative vector database
- [[pinecone]] — Managed vector database

## Further Reading

- [ChromaDB Documentation](https://docs.trychroma.com/) — Official docs
- [ChromaDB GitHub](https://github.com/chroma-core/chroma) — Open source repo
