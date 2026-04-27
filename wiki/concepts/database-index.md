---
title: Database Index
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [database, index, performance, b-tree, query-optimization]
---

# Database Index

## Overview

A database index is a specialized data structure that dramatically improves the speed of data retrieval operations on a database table. Think of it like the index at the back of a book—it doesn't change the content, but it allows you to find what you're looking for without reading every single page. Similarly, a database index stores sorted values from one or more columns along with pointers to the corresponding rows, enabling the database to locate data using efficient search algorithms rather than scanning every row.

Indexes are one of the most important performance optimization tools in database systems. Without indexes, a query like `SELECT * FROM users WHERE email = 'john@example.com'` would require scanning every row in the users table. With an index on the email column, the database can navigate directly to the matching row in a fraction of the time. However, indexes come with costs: they consume additional storage space, and every INSERT, UPDATE, or DELETE operation must update all affected indexes, adding write overhead. This trade-off between read performance and write performance is central to index design decisions.

Modern database systems support multiple index types optimized for different use cases. B-tree indexes are the most common, ideal for range queries and equality comparisons. Hash indexes excel at single-value lookups. GiST and GIN indexes support complex data types like arrays, JSON, and full-text. Understanding these trade-offs enables developers and DBAs to choose the right index strategy for their workload.

## Key Concepts

### B-Tree Indexes

B-tree (Balanced Tree) indexes are the default index type in most relational databases. They maintain sorted data in a balanced tree structure where every leaf node is at the same depth:

```
        [50, 75]
       /   |   \
   [25]  [50] [75, 90]
   /  \   |    /   \
 10  30  50  60  80  95
```

Key properties:
- **Height-balanced** - All leaf nodes are equidistant from the root, ensuring O(log n) lookups
- **Sorted** - Leaf nodes are linked, enabling efficient range scans
- **Clustered** - Physically orders data on disk to match index order (for clustered indexes)

B-tree indexes excel at:
- Equality comparisons: `WHERE email = 'john@example.com'`
- Range queries: `WHERE age BETWEEN 25 AND 35`
- Prefix matching: `WHERE name LIKE 'Jo%'`
- Sorting: `ORDER BY created_at DESC`

### Index Types

**Single-Column Index** - Index on one column only:
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Composite Index** - Index on multiple columns:
```sql
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```

The order of columns in a composite index matters—the index can only be used for queries that reference the leading column(s).

**Unique Index** - Ensures all values in the index are unique:
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**Partial Index** - Index only rows meeting a condition:
```sql
CREATE INDEX idx_active_users ON users(email) WHERE active = true;
```

**Expression Index** - Index computed values:
```sql
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

### Hash Indexes

Hash indexes use a hash table for O(1) average-case lookups:

```sql
CREATE INDEX idx_session_token ON sessions(token) USING hash;
```

Hash indexes are optimal for equality comparisons but cannot support range queries or sorting. They're useful for fields with high cardinality where B-trees would degenerate into linear scans.

## How It Works

### Index Selection

When a query is executed, the query optimizer determines whether to use an index:

```sql
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
```

```
Index Scan using idx_users_email on users  (cost=0.43..8.45 rows=1 width=104)
  Index Cond: ((email)::text = 'john@example.com'::text)
```

The optimizer considers:
- **Selectivity** - What fraction of rows match? Highly selective indexes are more valuable
- **Statistics** - Database maintains statistics about data distribution
- **Query cost** - Estimated I/O and CPU costs for each plan
- **Index availability** - Whether relevant indexes exist

### Index Maintenance

Indexes are automatically maintained by the database:

```sql
-- Insert: Add new index entries
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
-- Index entries for idx_users_email and any other indexes are updated

-- Update: Remove old entries, add new ones
UPDATE users SET email = 'new@example.com' WHERE id = 1;

-- Delete: Remove index entries
DELETE FROM users WHERE id = 1;
```

### Covering Indexes

A covering index includes all columns needed by a query, allowing the database to satisfy the query entirely from the index without accessing the table:

```sql
-- Without covering index: Index lookup + table access
CREATE INDEX idx_orders_user ON orders(user_id);
-- Query needs: user_id, created_at, total
-- Must access table for created_at and total

-- With covering index: Index lookup only
CREATE INDEX idx_orders_user_cover ON orders(user_id, created_at, total);
-- All needed columns are in the index
```

## Practical Applications

### Identifying Missing Indexes

Query the database's statistics to find missing indexes:

```sql
-- PostgreSQL: Find frequently executed slow queries
SELECT 
    query,
    calls,
    mean_time,
    total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Find tables with high sequential scan rates
SELECT 
    relname,
    seq_scan,
    idx_scan,
    seq_scan / (idx_scan + 1) AS seq_scan_ratio
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan * 10
ORDER BY seq_scan_ratio DESC;
```

### Index Creation Strategy

```python
# Systematic approach to adding indexes

def analyze_queries(queries):
    """Analyze slow queries to identify index candidates"""
    candidates = []
    for query in queries:
        plan = explain(query)
        if plan.uses_seq_scan:
            columns = extract_filter_columns(query)
            candidates.append(columns)
    return prioritize_candidates(candidates)

# Principles:
# 1. Index columns used in WHERE, JOIN ON, ORDER BY
# 2. Consider composite indexes for queries filtering multiple columns
# 3. Remove unused indexes to reduce write overhead
# 4. Monitor index hit ratios and bloat
```

### Index Bloat

Indexes can become bloated over time due to updates and deletions:

```sql
-- PostgreSQL: Check index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- Rebuild bloated indexes
REINDEX INDEX CONCURRENTLY idx_users_email;
```

## Examples

### Creating and Using Indexes

```sql
-- Basic index creation
CREATE INDEX idx_products_category ON products(category_id);

-- Composite index for common query pattern
CREATE INDEX idx_orders_cust_date 
    ON orders(customer_id, order_date DESC)
    WHERE status = 'active';

-- Partial index for partitioned data
CREATE INDEX idx_messages_unread 
    ON messages(user_id, created_at) 
    WHERE read_at IS NULL;

-- JSON index for document queries
CREATE INDEX idx_users_metadata ON users USING gin(metadata);
-- Query: SELECT * FROM users WHERE metadata @> '{"role": "admin"}';
```

### Index-Only Scans

```sql
-- Create covering index
CREATE INDEX idx_orders_cover 
    ON orders(customer_id, order_date) 
    INCLUDE (total, status);

-- This query can be satisfied entirely from the index
SELECT order_date, total 
FROM orders 
WHERE customer_id = 123
ORDER BY order_date DESC
LIMIT 10;
```

## Related Concepts

- [[sql]] — SQL databases and query language
- [[postgresql]] — PostgreSQL's specific indexing features
- [[mysql]] — MySQL indexing
- [[query-optimization]] — Optimizing database queries
- [[b-tree]] — B-tree data structure details
- [[covering-index]] — Indexes that cover query needs
- [[index-bloat]] — Managing index fragmentation

## Further Reading

- [PostgreSQL Index Documentation](https://www.postgresql.org/docs/current/indexes.html)
- [Use The Index, Luke](https://use-the-index-luke.com/) - Comprehensive index guide
- [Database Indexing Strategies](https://www.sqlshack.com/database-indexing-strategies/)

## Personal Notes

I've learned that more indexes isn't always better. Early in my career, I created indexes liberally, but then noticed slow writes and high disk usage. The turning point was learning to analyze actual query patterns using `pg_stat_statements` rather than guessing what queries would be important. Now I follow a simple rule: create an index only when I have evidence (from logs or analysis) that it will help a real query. Also, partial indexes are underused—they can dramatically reduce index size and maintenance overhead for queries that only target a subset of rows.
