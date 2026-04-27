---
title: "Indexing Strategies"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [database-systems, performance-optimization, data-structures, query-optimization]
---

# Indexing Strategies

## Overview

Indexing strategies encompass the techniques and design decisions that determine how databases organize, access, and retrieve data efficiently. An index is a data structure that improves the speed of data retrieval operations at the cost of additional storage space and write overhead. In an increasingly data-driven world, proper indexing is critical for application performance—slow queries frustrate users, increase operational costs, and can determine whether a system scales or collapses under load.

Indexing strategy involves selecting which columns to index, choosing appropriate index types, designing composite indexes to support common query patterns, and managing the tradeoffs between read performance and write overhead. Poor indexing decisions can actually degrade performance, which is why understanding indexing internals matters for developers, DBAs, and architects alike. Different database systems also offer different indexing capabilities—understanding what your specific system provides enables better design decisions.

## Key Concepts

**B-Tree Indexes** are the most common index type in relational databases, including PostgreSQL, MySQL, and Oracle. B-trees maintain sorted data in a balanced tree structure, enabling O(log n) lookup, insertion, and deletion. They handle range queries efficiently (finding all records where date BETWEEN x AND y) and work well with equality conditions. B-tree indexes are optimal for columns with high cardinality (many distinct values) and support both ascending and descending scans.

**Hash Indexes** provide O(1) average-case lookup for equality conditions but cannot handle range queries. They work by computing a hash of the indexed value to locate records. Hash indexes are useful for MEMORY tables and scenarios involving exact-match lookups, but most production databases recommend B-tree indexes even for equality-heavy workloads due to their versatility.

**Composite Indexes** index multiple columns together in a specific order. The column order matters enormously—queries can use the index for filtering on leading columns but typically cannot use it efficiently for filters on trailing columns alone. A composite index on (city, state, zipcode) can efficiently serve queries filtering on city, or city+state, but cannot help queries filtering only on state or zipcode. This is called the "leftmost prefix" rule.

**Partial Indexes** index only a subset of rows based on a WHERE condition. This reduces index size and maintenance overhead while still accelerating the specific queries that matter. A table with a million orders might have a partial index on (customer_id) WHERE status = 'pending' to accelerate processing of outstanding orders without indexing the thousands of completed orders.

## How It Works

When a query planner receives a query, it determines whether any available index can assist. The planner considers statistics about data distribution, the specific conditions in the query, and index structure. For a query like `SELECT * FROM orders WHERE customer_id = 1234 AND status = 'shipped'`, the planner might use a composite index on (customer_id, status) if available, or might choose to scan an index on just customer_id and filter by status, or might decide a full table scan is faster if most orders belong to that customer.

```sql
-- Example: Analyzing index usage with EXPLAIN
EXPLAIN ANALYZE
SELECT o.order_id, o.total, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01'
  AND o.status = 'completed';

-- Sample output showing index usage:
-- Index Scan using idx_orders_created_status on orders  (cost=0.56..8.67 rows=2 width=32)
--   Index Cond: ((created_at >= '2024-01-01') AND ((status)::text = 'completed'))
--   ->  Index Scan using customers_pkey on customers  (cost=0.42..0.44 rows=1 width=24)
--      Index Cond: (id = o.customer_id)

-- Example: Creating strategic indexes
CREATE INDEX idx_orders_customer_status_date 
ON orders(customer_id, status, created_at DESC);

CREATE INDEX idx_products_category_price 
ON products(category_id, price) 
INCLUDE (name, description);  -- PostgreSQL covering index

-- Example: Partial index for common query pattern
CREATE INDEX idx_support_tickets_open 
ON support_tickets(created_at) 
WHERE status IN ('open', 'in_progress');
```

Covering indexes (or indexes with INCLUDE columns) allow an index to fully satisfy a query without accessing the main table—a technique called index-only scans. This dramatically reduces I/O for queries that can be satisfied entirely from the index.

## Practical Applications

Indexing strategies vary by workload type. **OLTP** (Online Transaction Processing) systems prioritize write performance and single-row lookups, requiring indexes that stay compact and support quick point queries. **OLAP** (Online Analytical Processing) systems prioritize complex aggregations and scans, benefiting from columnar storage and indexes optimized for large-range queries. Modern data warehouses often use columnstore indexes that store data column-by-column rather than row-by-row, dramatically accelerating analytical queries.

Read-heavy workloads may benefit from more indexes despite write overhead, while write-heavy workloads require index discipline to prevent accumulation of bloat. The optimal strategy depends on the specific query patterns—before adding indexes, examine actual query patterns using logs or monitoring tools rather than guessing what queries will run.

Database systems also offer specialized indexes for specific use cases: **GIN indexes** for full-text search and JSON data, **GiST indexes** for geometric and geographic data, **bloom filters** for probabilistic existence checks, and **vector indexes** for similarity search in AI applications. PostgreSQL particularly stands out for its rich indexing ecosystem.

## Examples

Consider an e-commerce database with the following query patterns:
```sql
-- Frequent queries:
-- Q1: SELECT * FROM products WHERE category_id = X AND price BETWEEN a AND b
-- Q2: SELECT * FROM products WHERE name ILIKE '%keyword%'
-- Q3: SELECT * FROM products ORDER BY created_at DESC LIMIT 20
-- Q4: SELECT * FROM products WHERE brand_id = X ORDER BY price ASC
```

Strategic indexes might include:
1. Composite index on (category_id, price) for Q1
2. GIN index on name using pg_trgm extension for Q2  
3. Index on (created_at DESC) for Q3
4. Composite index on (brand_id, price) for Q4

Notice that no single index serves all queries—this is why query pattern analysis matters before indexing.

## Related Concepts

- [[Query Optimization]] - Techniques for improving query execution plans
- [[Data Modeling]] - Designing database schemas and relationships
- [[B-Tree Data Structure]] - Underlying mechanism for common database indexes
- [[Full-Text Search]] - Specialized indexing for text content
- [[Columnstore Databases]] - Column-oriented storage for analytical workloads
- [[Database Performance]] - Monitoring and tuning database systems

## Further Reading

- *Use The Index, Luke* by Markus Winand - Comprehensive guide to SQL indexing
- PostgreSQL documentation on index types and usage
- *Designing Data-Intensive Applications* chapter on storage and retrieval
- Database vendor-specific indexing guides (Oracle, MySQL, SQL Server)

## Personal Notes

Indexing is both art and science. The scientific part is understanding how B-trees, composite indexes, and index-only scans work. The art is predicting query patterns, prioritizing conflicting needs, and knowing when denormalization serves better than indexing. I've seen systems brought to their knees by excessive indexing—every index slows writes and consumes memory. Always index with purpose, verify with EXPLAIN ANALYZE, and remember that the best index is the one that actually accelerates your real queries, not theoretical ones.
