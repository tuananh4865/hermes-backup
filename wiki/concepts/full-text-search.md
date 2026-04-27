---
title: "Full Text Search"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [search, databases, information-retrieval, elasticsearch, solr]
---

# Full Text Search

## Overview

Full text search (FTS) is a technique for searching text content within documents or databases by matching user queries against the meanings and structures of the text, not just exact substring matches. Unlike simple `LIKE '%query%'` SQL searches that scan every record character by character, full text search systems build inverted indexes that map terms to document locations, enabling fast retrieval of relevant results even across millions of documents.

Modern full text search goes beyond simple word matching to support stemming (matching "running" to "run"), synonym expansion (matching "car" to "automobile"), relevance ranking (scoring results by importance), phrase queries, fuzzy matching (typo tolerance), and boolean operators. Engines like Elasticsearch, Apache Solr, and Meilisearch power everything from product catalogs and documentation sites to enterprise knowledge bases and logging systems like the ELK stack. At a smaller scale, SQLite's FTS5 extension and PostgreSQL's `tsvector`/`tsquery` provide embedded full text search without external infrastructure.

## Key Concepts

**Inverted Index** — The fundamental data structure behind full text search. Rather than listing documents and their contents, an inverted index maps each unique term to the list of documents (and positions within those documents) where it appears. This allows instant lookup: to find documents containing "kernel," you directly retrieve the posting list for "kernel" rather than scanning every document.

```
Document 1: "The Linux kernel is Unix-like"
Document 2: "Kernel methods in machine learning"
Document 3: "Understanding kernel density estimation"

Inverted Index:
"kernel"     → [(1, pos 2), (2, pos 0), (3, pos 1)]
"linux"      → [(1, pos 1)]
"unix"       → [(1, pos 3)]
"machine"    → [(2, pos 1)]
```

**Stemming and Lemmatization** — Stemming trims words to their root form using heuristics (e.g., "running," "runner," "ran" → "run"). Lemmatization uses dictionaries and morphological analysis to find the base dictionary form. Both reduce vocabulary size and improve recall by grouping related words.

**Relevance Scoring / TF-IDF** — Term Frequency-Inverse Document Frequency is a classic scoring algorithm: rare terms across the corpus get higher weight, while terms appearing in every document get lower weight. Modern engines use more sophisticated algorithms like BM25 (Elasticsearch's default) which improves on TF-IDF by accounting for document length normalization.

**Stop Words** — Common words like "the," "a," "is" are often excluded from indexes because they appear everywhere and add no discriminative power. However, excluding stop words can break phrase searches like "to be or not to be," which is why sophisticated engines handle them carefully.

**Fuzzy Matching** — Handles typos by allowing edits (insertions, deletions, substitutions, transpositions) up to a configurable distance (the Levenshtein distance). A fuzzy query for "algoritm" will match "algorithm."

**Boosting** — Giving certain fields higher weight in relevance scoring. For example, matching a query against a product's title should rank higher than matching against its long description, so you "boost" the title field.

**Faceted Search** — Aggregating results by categories (brand, price range, rating) to let users filter and drill down interactively. Facets are computed from the result set and returned alongside search results.

## How It Works

A typical FTS indexing and querying workflow with Elasticsearch:

```python
# Indexing documents (conceptual Python pseudocode for Elasticsearch DSL)
from elasticsearch import Elasticsearch

es = Elasticsearch()

# Define mapping with custom analyzers
mapping = {
    "mappings": {
        "properties": {
            "title":   {"type": "text", "analyzer": "english", "boost": 2.0},
            "content": {"type": "text", "analyzer": "english"},
            "tags":    {"type": "keyword"},  # exact match, not analyzed
            "created": {"type": "date"}
        }
    }
}

# Index a document
doc = {
    "title": "Introduction to Neural Networks",
    "content": "Neural networks are computing systems inspired by biological...",
    "tags": ["ml", "deep-learning"],
    "created": "2024-01-15"
}
es.index(index="articles", id=1, document=doc)

# Search with relevance scoring
query = {
    "query": {
        "multi_match": {
            "query": "neural network training",
            "fields": ["title^2", "content"],  # ^2 boosts title
            "type": "best_fields"
        }
    },
    "highlight": {
        "fields": {"content": {"fragment_size": 150}}
    }
}
results = es.search(index="articles", body=query)
```

## Practical Applications

- **Web Search Engines** — Google, Bing, and DuckDuckGo use massively distributed full text search to index billions of web pages.
- **E-commerce Product Search** — Finding products by name, description, brand while handling synonyms, typos, and relevance ranking.
- **Documentation Sites** — Algolia DocSearch, Lunr.js, and Elasticsearch-powered documentation portals make finding technical information fast.
- **Enterprise Search** — Searching across internal wikis, emails, and documents (SharePoint, Confluence).
- **Log Analysis / SIEM** — The ELK stack (Elasticsearch, Logstash, Kibana) ingests and indexes terabytes of logs for real-time search and alerting.
- **Recommendation Systems** — Full text search can power content-based recommendations by finding similar documents.

## Examples

**PostgreSQL Native FTS** — No external engine needed for many use cases:

```sql
-- Add a search vector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Populate it with title and content (english stemming)
UPDATE articles SET search_vector =
    setweight(to_tsvector('english', coalesce(title,'')), 'A') ||
    setweight(to_tsvector('english', coalesce(content,'')), 'B');

-- Create a GIN index for fast searching
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Search with ranking
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'neural & network') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

**Simple Client-Side Search with Lunr.js** — For small datasets, no server needed:

```javascript
import lunr from 'lunr';

const index = lunr(function () {
  this.ref('id');
  this.field('title');
  this.field('content');
  documents.forEach(doc => this.add(doc));
});

const results = index.search('neural network');
// [{ ref: '1', score: 1.234, matchData: {...} }]
```

## Related Concepts

- [[Inverted Index]] — The core data structure enabling fast text retrieval
- [[Elasticsearch]] — The most popular open-source distributed search engine
- [[Information Retrieval]] — The academic field studying search and retrieval
- [[BM25]] — The relevance scoring algorithm used by Elasticsearch
- [[Stemming]] — Word normalization technique used in FTS
- [[TF-IDF]] — Classic term weighting scheme for relevance scoring
- [[Search Engine Optimization]] — Improving text discoverability in web search

## Further Reading

- Manning, C., Raghavan, P., & Schütze, H. "Introduction to Information Retrieval" — The definitive textbook on FTS and IR.
- "Elasticsearch: The Definitive Guide" — Official comprehensive guide to Elasticsearch.
- "PostgreSQL Full Text Search" — Excellent official documentation with practical examples.
- "How Search Engines Work" — Google's visual guide to web crawling and indexing.
- "BM25: The Next Generation of Lucene Relevance" — Technical deep dive into relevance ranking.

## Personal Notes

Full text search is one of those areas where "good enough" is often the enemy of "great." SQLite FTS5 or PostgreSQL `tsvector` will carry you surprisingly far — most applications never need Elasticsearch. I learned this the hard way after deploying a full ELK stack for a small internal tool, only to realize I'd created an operational nightmare for myself. Start simple, scale up when you hit real limits. The key insight that changed how I think about FTS is that it's fundamentally a ranking problem, not just a matching problem: you want the *best* results, not just any results that match.
