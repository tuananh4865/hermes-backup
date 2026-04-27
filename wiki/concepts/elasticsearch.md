---
title: "Elasticsearch"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [elasticsearch, search-engine, distributed-system, elastic-stack, lucene, nosql, logging, observability]
---

# Elasticsearch

## Overview

Elasticsearch is a distributed, RESTful search and analytics engine built on [[Apache Lucene]]. It excels at full-text search, structured search, and analytical queries across massive datasets. As the heart of the Elastic Stack (ELK Stack), Elasticsearch provides the search and analytics capabilities that power use cases ranging from website search bars to security information and event management (SIEM) systems.

What sets Elasticsearch apart is its ability to scale horizontally—adding more nodes to a cluster increases both storage capacity and query throughput. It achieves this by distributing data across multiple shards (primary and replica) that can reside on different nodes. A cluster with three data nodes can store terabytes of data while serving thousands of queries per second with sub-second latency.

Elasticsearch stores data as JSON documents and exposes a comprehensive REST API for indexing, searching, and managing data. Unlike traditional relational databases that organize data into tables with fixed schemas, Elasticsearch is schema-less in the sense that documents can have different fields. However, mappings define the fields and their data types to optimize storage and query performance.

The project began as a standalone product in 2010 and has since evolved into a comprehensive observability and security platform. Organizations use it for application performance monitoring, log analysis, security analytics, and business intelligence. Companies like Uber, eBay, and Netflix rely on Elasticsearch for critical infrastructure powering their search and analytics needs.

## Key Concepts

**Indices and Documents**: The fundamental unit of data in Elasticsearch is a document—JSON object with typed fields. Documents are stored in indices, which are logical namespaces equivalent to databases in relational terminology:

```json
// Document example - a blog post
{
  "title": "Getting Started with Elasticsearch",
  "author": "Jane Developer",
  "published_at": "2026-04-13T08:00:00Z",
  "content": "Elasticsearch is a powerful search engine...",
  "tags": ["search", "elasticsearch", "backend"],
  "view_count": 1523,
  "comments": [
    { "user": "bob", "text": "Great introduction!" }
  ]
}
```

**Inverted Index**: At its core, Elasticsearch uses Lucene's inverted index data structure. Rather than mapping documents to words (as a book index maps pages to terms), an inverted index maps terms to the documents containing them. This enables extremely fast full-text searches across millions of documents.

**Shards and Replicas**: Indices are divided into shards for horizontal scaling. Each shard is a self-contained Lucene index. Replica shards provide redundancy and improve read throughput:

```
# Index with 3 primary shards and 1 replica
PUT /my_index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  }
}
```

**Mappings**: While Elasticsearch can auto-detect field types, explicit mappings ensure optimal performance and correct handling:

```json
PUT /products/_mapping
{
  "properties": {
    "name": { "type": "text", "analyzer": "english" },
    "price": { "type": "float" },
    "in_stock": { "type": "boolean" },
    "created_at": { "type": "date" },
    "tags": { "type": "keyword" }
  }
}
```

## How It Works

Elasticsearch's distributed architecture enables horizontal scalability while maintaining search consistency:

1. **Cluster Formation**: Nodes discover each other using seed hosts or multicast, forming a cluster. One node acts as the master, managing cluster-level operations like creating/deleting indices and tracking shard allocation.

2. **Document Indexing**: When you index a document, Elasticsearch hashes the document ID to determine which primary shard should store it. The document is written to the primary shard, then replicated to replicas in parallel.

3. **Document Retrieval**: Read requests can be served by the primary shard or any replica. The coordinating node (the one receiving the request) broadcasts to relevant shards, merges results, and returns to the client.

4. **Search Execution**: Search requests go through multiple phases:
   - **Query Phase**: The coordinating node sends the query to all relevant shards, each Lucene segment executes the query locally and returns matching document IDs with scores
   - **Fetch Phase**: The coordinating node retrieves the full documents for the top results from the appropriate shards

```bash
# Cluster health check
GET _cluster/health

# Index a document
POST /blog/_doc
{
  "title": "My First Post",
  "content": "Hello Elasticsearch!"
}

# Search with query
GET /blog/_search
{
  "query": {
    "multi_match": {
      "query": "elasticsearch getting started",
      "fields": ["title^2", "content"]
    }
  },
  "highlight": {
    "fields": {
      "content": {}
    }
  },
  "aggs": {
    "popular_tags": {
      "terms": { "field": "tags.keyword" }
    }
  }
}
```

## Practical Applications

**Full-Text Search**: Elasticsearch powers search features on websites, e-commerce platforms, and documentation portals. It handles relevance ranking, fuzzy matching, phrase queries, and natural language processing features like stemming and synonyms.

**Log Analysis and Observability**: The ELK Stack (Elasticsearch, [[Logstash]], Kibana) is a standard for centralized logging. Logs are collected, parsed, and indexed in Elasticsearch; Kibana provides visualization. This is commonly combined with Beats for data shipping.

**Security Analytics**: Elasticsearch stores security events from multiple sources, enabling threat detection, anomaly detection, and incident investigation. The Elastic Security app provides SIEM capabilities on top.

**Application Performance Monitoring**: [[APM]] (Application Performance Monitoring) tools built on Elasticsearch track request traces, performance metrics, and errors across distributed applications.

**Business Analytics**: The aggregation framework enables real-time analytics on large datasets—calculating averages, percentiles, cardinality, and time-series trends without pre-computation.

## Examples

**Basic CRUD Operations**:

```bash
# Create index with settings
PUT /products
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "product_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "porter_stem"]
        }
      }
    }
  }
}

# Bulk index documents
POST /products/_bulk
{"index":{"_id":"1"}}
{"name":"Laptop","price":999.99,"brand":"TechCorp","in_stock":true}
{"index":{"_id":"2"}}
{"name":"Mouse","price":29.99,"brand":"TechCorp","in_stock":true}
{"index":{"_id":"3"}}
{"name":"Keyboard","price":79.99,"brand":"TypeMaster","in_stock":false}

# Search with filters and aggregations
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "laptop" } }
      ],
      "filter": [
        { "range": { "price": { "gte": 500 } } },
        { "term": { "in_stock": true } }
      ]
    }
  },
  "sort": [{ "price": "asc" }],
  "aggs": {
    "brands": {
      "terms": { "field": "brand.keyword" },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } }
      }
    }
  }
}
```

**Python Client Usage**:

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

# Index a document
doc = {
    "title": "Python Elasticsearch Tutorial",
    "author": "Dev Coder",
    "content": "Learn how to index and search documents...",
    "published_at": "2026-04-13"
}
result = es.index(index="blog", id="python_tutorial", document=doc)

# Search with highlighting
response = es.search(
    index="blog",
    body={
        "query": {"match": {"content": "elasticsearch python"}},
        "highlight": {"fields": {"content": {}}}
    }
)

for hit in response["hits"]["hits"]:
    print(f"Score: {hit['_score']}")
    print(f"Title: {hit['_source']['title']}")
    if "highlight" in hit:
        print(f"Match: {hit['highlight']['content']}")
```

## Related Concepts

- [[Apache Lucene]] - The search library Elasticsearch is built on
- [[Search Engine]] - General search technology concepts
- [[Distributed Systems]] - How Elasticsearch achieves scalability
- [[Logstash]] - Data processing pipeline in the Elastic Stack
- [[Kibana]] - Visualization frontend for Elasticsearch
- [[Beats]] - Lightweight data shippers for the Elastic Stack
- [[APM]] - Application Performance Monitoring with Elastic
- [[NoSQL]] - Elasticsearch as a document-oriented database
- [[REST API]] - How clients interact with Elasticsearch

## Further Reading

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch: The Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html)
- [Lucene Documentation](https://lucene.apache.org/core/)
- [Elastic Blog](https://www.elastic.co/blog)

## Personal Notes

Elasticsearch has become indispensable for any project requiring search at scale. The aggregation framework alone justifies its use over simple LIKE queries in [[SQL]]—being able to calculate percentiles, cardinality, and time-series breakdowns on billions of documents in real-time is powerful. That said, I've learned to be careful with the number of shards upfront; while you can add replica shards dynamically, changing the number of primary shards requires reindexing. Using index templates and rollover policies helps manage indices lifecycle in production environments.
