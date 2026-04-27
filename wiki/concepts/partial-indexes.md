---
title: "Partial Indexes"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, postgresql, performance, indexing, sql]
---

# Partial Indexes

A partial index is a database index that covers only a subset of rows in a table, defined by a predicate (WHERE clause). By indexing only the rows relevant to a query, partial indexes are smaller, faster to maintain, and consume less storage than full-table indexes.

## Overview

Traditional indexes include every row in the table (or every row in an indexed partition). For large tables where only a fraction of rows are queried frequently, this wastes resources. Partial indexes solve this by indexing only rows that satisfy a condition.

The concept originated with PostgreSQL in the 1990s and has since been adopted by other databases including SQLite, MySQL (via generated columns and filtered indexes), and Oracle. PostgreSQL's implementation remains the most full-featured.

The key insight: if your application consistently queries `WHERE status = 'active'`, an index on `status` that includes only active rows is both smaller and more targeted than a full index.

## How Partial Indexes Work

When you create a partial index with a WHERE clause, the database builds the index structure for only the matching rows at creation time. As rows are inserted, updated, or deleted, the index updates only for affected rows that match the predicate.

Query optimization works the same way as regular indexes: the planner examines the WHERE clause and decides whether the partial index can satisfy the query. For the optimizer, a partial index looks like a regular index on a smaller table.

```sql
-- Full index (all rows)
CREATE INDEX idx_orders_status ON orders(status);

-- Partial index (active orders only)
CREATE INDEX idx_orders_active ON orders(status) WHERE status = 'active';

-- Query using partial index
SELECT * FROM orders WHERE status = 'active' AND customer_id = 123;
-- This can use idx_orders_active
```

## Practical Applications

**Soft-Deleted Records**

Applications often use soft deletes (`deleted_at` timestamp instead of actual deletion). Most queries ignore deleted records.

```sql
-- Index only non-deleted rows
CREATE INDEX idx_articles_published 
ON articles(published_at) 
WHERE deleted_at IS NULL;

-- Queries for active content automatically use this index
SELECT * FROM articles WHERE published_at > '2025-01-01' AND deleted_at IS NULL;
```

**Status-Based Filtering**

E-commerce, task management, and workflow systems often filter by status where one status dominates queries.

```sql
-- In a task system, most queries look for open tasks
CREATE INDEX idx_tasks_open ON tasks(assignee_id, created_at) WHERE status = 'open';

-- Analytics queries on completed tasks
CREATE INDEX idx_tasks_completed ON tasks(completed_at) WHERE status = 'completed';
```

**Tenant Isolation in Multi-Tenant Systems**

In a SaaS application with row-level security, partial indexes enforce isolation efficiently.

```sql
-- Index only rows for current tenant
CREATE INDEX idx_documents_tenant ON documents(folder_id) WHERE tenant_id = current_tenant_id;
```

**Optimizing Extreme Values**

When you frequently query the latest or oldest records:

```sql
-- Index recent high-value orders for reporting
CREATE INDEX idx_orders_recent_highvalue 
ON orders(customer_id, created_at) 
WHERE created_at > '2025-01-01' AND total > 10000;
```

## Storage and Performance Benefits

A partial index on 1% of a million-row table is roughly 100x smaller than a full index. Benefits include:

| Aspect | Full Index | Partial Index |
|--------|------------|---------------|
| Storage | O(n) | O(filtered n) |
| Write overhead | Higher | Lower |
| Index scan speed | Slower (larger) | Faster (smaller) |
| Memory efficiency | Worse | Better (fits in RAM) |

The smaller size means the index fits in RAM more easily, reducing disk I/O. Write operations (INSERT/UPDATE) incur less overhead since fewer index entries change.

## Limitations

**Predicate Matching**: The query's WHERE clause must match the index's predicate exactly (or be implied by it). `WHERE status = 'active' AND type = 'order'` won't use an index defined `WHERE status = 'active'` if the planner decides a seq scan is faster—but it usually will use it.

**Limited Expressiveness**: Partial index predicates cannot include subqueries, functions (except immutables), or reference other tables. Complex filtering logic may not be expressible.

**Maintenance**: As data distribution changes (e.g., more orders become 'completed' than 'active'), the partial index may become less effective. Periodic review of index effectiveness is needed.

## Monitoring and Tuning

PostgreSQL provides tools to analyze index usage:

```sql
-- Check if an index is being used
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE indexrelname = 'idx_orders_active';

-- Find unused indexes
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND NOT indexname LIKE '%_pkey';

-- Check index size
SELECT pg_size_pretty(pg_relation_size('idx_orders_active'));
```

The `pg_stat_user_indexes` view reveals which indexes are scanned and how effective they are. An index with zero scans is a candidate for removal.

## Related Concepts

- [[PostgreSQL Indexes]] - General indexing in PostgreSQL
- [[Database Indexing]] - Broad concept of index structures
- [[Query Optimization]] - How the database chooses indexes
- [[Soft Delete]] - Pattern where partial indexes are commonly used
- [[B-Tree Index]] - Most common index type partial indexes use

## Further Reading

- PostgreSQL Documentation: "Partial Indexes"
- "The Art of PostgreSQL" by Dimitri Fontaine
- "High Performance PostgreSQL" by Sven Wegmann

## Personal Notes

Partial indexes are underused. Many developers facing slow queries reach for full indexes or denormalization without considering that a well-targeted partial index solves the problem with far less overhead. The soft-delete case is particularly valuable—almost every application I've worked with would benefit from partial indexes on active records. The key habit to develop: whenever you write a query with a WHERE clause filtering on a specific value or range, consider whether a partial index matches.
