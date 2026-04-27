---
title: LlamaIndex
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [llamaindex, rag, framework, llm, data-indexing]
---

# LlamaIndex

## Overview

LlamaIndex (formerly GPT Index) is a data framework for building applications that connect custom data sources to [[large language model]]s. It provides the infrastructure to ingest, index, and query private or domain-specific data and inject it into an LLM's context for retrieval-augmented generation ([[RAG]]). In essence, LlamaIndex acts as the "memory" layer between your documents and the LLM—transforming unstructured and structured data into optimized queryable indices that the LLM can reference during generation.

The framework was created by Jerry Liu and first released in 2022, gaining rapid adoption as developers realized that LLMs trained on public data alone cannot answer questions about private documents, proprietary codebases, or real-time information. LlamaIndex addresses this by providing a standardized, composable approach to building data pipelines that feed into LLMs. It is one of the two dominant RAG frameworks alongside [[LangChain]].

## Key Concepts

### Data Connectors (Readers)

LlamaIndex's data connectors (called **Readers**) ingest data from virtually any source:
- **Local**: PDF, TXT, Markdown, CSV, JSON, Notion, Obsidian
- **Cloud**: [[Google Drive]], [[Notion]], [[Slack]], [[AWS S3]]
- **Databases**: [[PostgreSQL]], [[MongoDB]], [[SQLite]], [[MySQL]]
- **APIs**: REST APIs, [[GraphQL]], [[Twitter]], [[Wikipedia]]
- **Messaging**: [[Slack]], [[Discord]] messages and threads

Each reader handles the specific parsing logic for its source and outputs a set of `Document` objects.

### Documents and Nodes

The core data unit in LlamaIndex is the **Document**—an object containing text content and associated metadata (source file, page number, author, creation date, custom metadata). Documents are split into **Nodes** (chunks) by a text splitter. Chunking strategy is critical: too large and you lose retrieval precision; too small and you lose context.

LlamaIndex provides multiple node parsers:
- `SentenceSplitter`: Split by sentence boundaries
- `TokenSplitter`: Split by token count (important for LLM context limits)
- `RecursiveCharacterTextSplitter`: Hierarchical splitting by multiple delimiters
- `CodeSplitter`: Language-aware code splitting

### Index Types

LlamaIndex supports multiple index structures, each optimized for different query patterns:

| Index Type | Use Case | Query Approach |
|---|---|---|
| **VectorStoreIndex** | Semantic search | ANN vector similarity |
| **SummaryIndex** | List/aggregation queries | LLM summarization |
| **KeywordTableIndex** | Keyword search | BM25 or simple keyword matching |
| **KnowledgeGraphIndex** | Multi-hop reasoning | Graph traversal |
| **SQLIndex** | Structured data queries | SQL generation |

The most commonly used is **VectorStoreIndex**, which embeds each node and stores vectors in a [[vector database]] like [[Pinecone]], [[Chroma]], [[Weaviate]], or [[Qdrant]].

### Query Engines

Once an index is built, a **Query Engine** handles the retrieval and generation pipeline:
1. **Retrieval**: Given a user query, find the most relevant nodes
2. **Post-processing**: rerank, filter, or transform retrieved nodes
3. **Response Synthesis**: Feed nodes + query to the LLM for generation

Advanced query engine features:
- **Retrievers**: Custom retrieval strategies (hybrid search, multi-vector)
- **Node Postprocessors**: Reranking (e.g., [[Cohere]] Rerank), redundancy filtering
- **Response Synthesizers**: "compact" (pack chunks into LLM context), "refine" (iteratively improve answer), "simple" (single-shot)

### Data Agents

LlamaIndex includes **Data Agents**—LLM-powered agents that can interact with data sources in a read-write manner. Agents can:
- Search Wikipedia for real-time information
- Query SQL databases with natural language
- Retrieve docs from [[Google Drive]]
- Perform web searches and synthesize results

Agents use a ReAct-style (Reason + Act) loop to decide when to query data and when to generate a response.

## How It Works

A typical LlamaIndex RAG pipeline:

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms import OpenAI

# Step 1: Load documents from a directory
documents = SimpleDirectoryReader("./data").load_data()

# Step 2: Build index (embedding + storage)
index = VectorStoreIndex.from_documents(documents)

# Step 3: Create query engine
query_engine = index.as_query_engine(llm=OpenAI(model="gpt-4"))

# Step 4: Query
response = query_engine.query("What were the key findings in Q1?")
print(response)
```

Internally:
1. Documents → Nodes (via text splitter)
2. Nodes → Embeddings (via embedding model, e.g., OpenAI `text-embedding-3-small`)
3. Embeddings → Vector store (Pinecone, Chroma, etc.)
4. Query → Embed query → ANN search → Top-k nodes → LLM synthesis → Response

## Practical Applications

LlamaIndex is used to build a wide range of LLM applications:

- **Private document Q&A**: Ask questions about your company's internal docs
- **Codebase understanding**: Query implementation details across a large codebase
- **Customer support bots**: RAG over knowledge base articles
- **Research assistants**: Synthesize information from papers and web sources
- **Multi-modal RAG**: Combine text, image captions, and structured data
- **Agentic data pipelines**: Agents that retrieve, reason, and write data

## Examples

Building a RAG pipeline with a custom vector store (Pinecone):

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import PineconeVectorStore
from llama_index.storage import StorageContext
import pinecone

# Initialize Pinecone
pinecone.init(api_key="your-api-key", environment="us-west-2")
pinecone.create_index("my-index", dimension=1536, metric="cosine")

# Load documents
documents = SimpleDirectoryReader("./docs").load_data()

# Connect to Pinecone vector store
vector_store = PineconeVectorStore(index_name="my-index")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build index directly into Pinecone
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the quarterly report")
print(response)
```

Using a Data Agent for Wikipedia queries:

```python
from llama_index.agent import ReActAgent
from llama_index.tools import WikipediaToolSpec

wiki = WikipediaToolSpec()
agent = ReActAgent.from_tools(wiki.to_tool_list())

response = agent.chat(
    "Compare the GDP per capita of Germany and Japan in 2024"
)
print(response)
```

## Related Concepts

- [[rag]] — Retrieval-augmented generation, the paradigm LlamaIndex implements
- [[LangChain]] — The other dominant LLM data framework
- [[vector-database]] — Where LlamaIndex stores embeddings
- [[embeddings]] — Vector representations of text used for retrieval
- [[Large Language Model]] — The models LlamaIndex queries
- [[agent-frameworks]] — Broader agent frameworks landscape
- [[knowledge-management]] — Using LlamaIndex for knowledge management
- [[Chroma]] — Open-source vector database often used with LlamaIndex
- [[Pinecone]] — Managed vector database for production RAG

## Further Reading

- [LlamaIndex Official Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub Repository](https://github.com/run-llama/llama_index)
- [Jerry Liu's Introduction to LlamaIndex](https://medium.com/@jerryjliu)
- [RAG cookbook with LlamaIndex](https://github.com/run-llama/llama_index/tree/main/docs/examples)
- [Comparison: LlamaIndex vs LangChain](https://www.pinecone.io/learn/series/langchain/langchain-vs-llamaindex/)

## Personal Notes

My workflow with LlamaIndex: start with `SimpleDirectoryReader` and the default `VectorStoreIndex` for quick prototypes. Once I need to optimize, I swap the vector store (Chroma for local dev, Pinecone for production) and tune the chunk size (I find 512 tokens a good default). The `as_query_engine` with `response_mode="compact"` is almost always better than the default since it packs more context into each LLM call. One gotcha: embedding models matter a lot—OpenAI's `text-embedding-3-small` is fast and good, but for domain-specific vocabulary, fine-tuning an embedding model pays dividends. For agents, the `ReActAgent` with tool specs is powerful but can be slow; `ContextRetriever` augmentation often works well as a faster alternative.
