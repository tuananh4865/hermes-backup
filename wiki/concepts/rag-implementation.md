---
title: "RAG Implementation"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rag, llm, retrieval-augmented-generation, vector-databases, machine-learning]
---

## Overview

RAG (Retrieval-Augmented Generation) is an architectural pattern that enhances [[large-language-models|model]] responses by grounding them in external knowledge retrieved at inference time. Rather than relying solely on training data, RAG systems fetch relevant documents or information from a knowledge base and include them in the prompt sent to the LLM. This approach reduces hallucination, enables access to up-to-date information, and allows models to reason about private or domain-specific data they were never trained on.

The RAG architecture was popularized by Meta AI researchers in 2020 with the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." The key insight was that separating knowledge storage from the language model itself provides more flexibility and verifiability than fine-tuning. Organizations can update their knowledge base without retraining expensive models.

## Key Concepts

**Retrieval** is the process of finding relevant documents from a knowledge corpus given a user query. Modern RAG systems typically use dense retrieval with [[embeddings]]—both queries and documents are embedded into vector space, and similarity search finds the nearest documents.

**Chunking** is the practice of splitting large documents into smaller pieces before embedding. Chunk size affects retrieval precision and context completeness. Common strategies include fixed-size chunking (512 tokens), semantic chunking (split by paragraphs or sections), and recursive chunking that respects document structure.

**Vector Databases** store embeddings and enable efficient similarity search. Options include Milvus, Pinecone, Weaviate, Chroma, and Qdrant. Traditional databases like PostgreSQL (with pgvector) also support vector operations.

**Reranking** improves retrieval quality by using a more computationally expensive model to reorder initially retrieved documents. After an initial vector search retrieves candidates, a cross-encoder scores relevance more accurately.

**Hybrid Search** combines keyword-based (BM25) and semantic (vector) retrieval, often with reciprocal rank fusion, to capture both exact term matches and semantic similarity.

## How It Works

A RAG pipeline operates in two phases: indexing (offline) and retrieval (online).

**Indexing Phase:**

```python
# Document indexing pipeline
from langchain.document_loaders import PDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 1. Load documents
loader = PDFLoader('./knowledge-base/*.pdf')
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# 3. Generate embeddings and store in vector database
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory='./vector-store'
)
vectorstore.persist()
```

**Retrieval Phase:**

```python
# Query-time retrieval and generation
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load vector store
vectorstore = Chroma(
    persist_directory='./vector-store',
    embedding_function=OpenAIEmbeddings()
)

# 2. Create retrieval chain
llm = ChatOpenAI(model_name='gpt-4')
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',  # Packs retrieved docs into prompt
    retriever=vectorstore.as_retriever(
        search_kwargs={'k': 4}  # Retrieve top 4 chunks
    )
)

# 3. Ask questions
response = qa_chain.run(
    "What are the key requirements for system onboarding?"
)
```

## Practical Applications

RAG powers enterprise AI assistants that need to answer questions about internal policies, codebases, or documentation. Legal firms use RAG to query case law; healthcare organizations build assistants that reference medical literature. Customer service bots retrieve from product knowledge bases to answer product questions accurately.

RAG is essential for domains where accuracy is critical and information changes frequently—news summarization, financial research, and technical support. By grounding responses in retrieved evidence, RAG makes answers verifiable and updatable without model retraining.

## Examples

An advanced RAG implementation with reranking:

```python
# Advanced RAG with reranking using Cohere
from cohere import Client as CohereClient
from rank import Ranker

cohere_client = CohereClient(api_key='your-api-key')

def advanced_rag_query(query, vectorstore, top_k=20, final_k=5):
    # Step 1: Initial dense retrieval
    initial_results = vectorstore.similarity_search(query, k=top_k)

    # Step 2: Rerank with cross-encoder
    reranker = Ranker(model='cross-encoder/ms-marco-MiniLM-L-12-v2')
    reranked = reranker.rank(query, initial_results, top_k=final_k)

    # Step 3: Generate with retrieved context
    context = "\n\n".join([doc.page_content for doc in reranked])

    prompt = f"""Based on the following context, answer the question.
If the context doesn't contain the answer, say so.

Context:
{context}

Question: {query}
Answer:"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response.choices[0].message.content
```

## Related Concepts

- [[large-language-models]] - The generation component of RAG
- [[similarity-search]] - Dense retrieval using vector embeddings
- [[embeddings]] - Vector representations enabling semantic search
- [[vector-databases]] - Storage for embeddings and efficient retrieval
- [[information-retrieval]] - Classical retrieval theory underlying RAG

## Further Reading

- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Meta AI 2020)
- LangChain documentation on RAG implementations
- "Building RAG Systems with Open Source Models" guide
- Pinecone's RAG architecture guide

## Personal Notes

RAG quality depends heavily on chunking strategy and embedding choice. I found thatsemantic chunking with overlap consistently outperforms fixed-size chunking for technical documentation. Also, retrieval quality matters more than generation quality—a poor retrieval cannot be fixed by a better LLM. Always evaluate the retrieval component separately before optimizing the generation side.
