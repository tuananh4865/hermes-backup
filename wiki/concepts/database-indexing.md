---
title: Database Indexing
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [database-indexing, database, performance, b-tree]
---

## Overview

Database indexing is a data structure technique used to accelerate data retrieval operations on a database table. An index works similarly to a book index: instead of scanning every page to find a specific topic, you consult the index at the back to locate page numbers where that topic appears. In database terms, an index stores sorted column values along with pointers to the corresponding rows in the table, enabling the database engine to locate data with minimal I/O operations.

Without an index, a query that filters on a specific column must perform a full table scan, examining every single row to determine whether it matches the query conditions. This becomes prohibitively expensive as table sizes grow into millions or billions of rows. By maintaining an index structure, the database can use efficient lookup algorithms to navigate directly to relevant rows, often reducing query time from linear scanning to logarithmic complexity.

Indexes are created on one or more columns of a table, and each index is automatically maintained by the database engine whenever underlying data is inserted, updated, or deleted. This maintenance overhead means indexes trade write performance for read performance. A well-designed indexing strategy considers the types of queries an application runs, the columns frequently used in WHERE clauses, JOIN conditions, and ORDER BY clauses, and the balance between query speed and write throughput.

## Types

Different index types offer distinct performance characteristics suited to various query patterns and data distributions.

**B-tree indexes** (Balanced Tree) are the most common index type in relational databases. They maintain data in a sorted tree structure where every leaf node is at the same depth, ensuring consistent lookup times regardless of where the target data resides. B-tree indexes excel at range queries, equality searches, and prefix matching operations. They handle inserted data gracefully through automatic balancing and work well with comparative operators such as less than, greater than, and between. Most databases create B-tree indexes by default when you issue a CREATE INDEX statement without specifying an index type.

**Hash indexes** use a hash function to compute a bucket address from indexed values. They provide constant-time O(1) lookup performance for equality comparisons, making them extremely fast for exact match queries. However, hash indexes cannot support range queries, prefix matching, or sorting operations because the hash function destroys the natural ordering of data. They are best suited for in-memory databases or caching layers where primary-key lookups and join operations dominate the workload.

Beyond these fundamental types, databases support additional index varieties including [[bitmap indexes]] which compress data efficiently for low-cardinality columns in analytical workloads, [[GiST indexes]] (Generalized Search Tree) used for geometric and full-text search operations, and [[partial indexes]] that index only a subset of rows matching a condition to reduce storage and maintenance overhead.

## Trade-offs

Indexing involves meaningful trade-offs that every database administrator and application developer must carefully consider.

**Write performance degradation** occurs because every INSERT, UPDATE, or DELETE operation must update not only the table data but also all indexes defined on that table. For tables with many indexes, write-heavy workloads can suffer significant performance penalties as the database must maintain multiple sorted structures simultaneously. The cost compounds when indexes are created on frequently updated columns.

**Storage overhead** is another critical consideration. Indexes consume disk space, sometimes substantially more than the raw table data itself. A table with five or six indexes on large text columns can easily double or triple its storage requirements. This overhead affects backup times, replication latency, and storage costs in cloud environments.

**Maintenance operations** such as table reorganization, vacuum, and index rebuilding may be required to reclaim space and maintain optimal performance as indexes fragment over time. Fragmentation occurs when page splits during inserts cause physical storage order to diverge from logical index order, leading to additional I/O during index traversals.

Choosing which columns to index requires understanding query patterns and balancing competing needs. Over-indexing creates excessive write overhead and consumes resources, while under-indexing leaves queries performing expensive full table scans. [[Query optimization]] tools and [[execution plan]] analysis help identify missing indexes and unused indexes that could be dropped to streamline the schema.

## Related

- [[B-tree]] - The balanced tree data structure underlying most database indexes
- [[Query Optimization]] - The process of selecting the most efficient execution plan for a query
- [[Database Normalization]] - Schema design principles that can reduce the need for indexes
- [[Full-text Search]] - Indexing techniques for text content and document retrieval
- [[Indexing Strategies]] - Approaches to selecting and maintaining appropriate indexes for workload patterns
- [[Execution Plan]] - How the database engine decides to use available indexes when executing queries
