---
title: Execution Plan
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, query-optimization, performance, sql, internals]
---

## Overview

An execution plan (also called a query plan or explain plan) is the roadmap a database management system generates for executing a SQL query. When you submit a query, the database's query optimizer does not simply run it step-by-step as written. Instead, it analyzes the query, inspects available [[indexes]], gathers statistics about table sizes and data distribution, and produces a plan that specifies the order and method of each operation — table scans, index lookups, joins, sorts, and aggregations. Understanding execution plans is essential for diagnosing slow queries, optimizing database performance, and understanding why seemingly equivalent queries can have dramatically different performance characteristics.

Execution plans are read from the bottom up: the innermost operations execute first, and their results flow upward. Each operation in the plan shows estimated or actual costs, row counts, and the specific technique used (e.g., nested loop join, hash join, merge join).

## Key Concepts

**Sequential Scan** reads every row in a table from start to finish. It is the default when no useful index exists or when the query selects a large percentage of the table. Sequential scans are not inherently bad — for small tables or bulk operations, they can be faster than index lookups because they avoid random I/O overhead.

**Index Scan** uses an [[database-indexing|index]] to locate rows matching a condition. The database traverses the B-tree index to find relevant entries, then fetches the actual row data (in a heap fetch). Index scans are efficient when the query selects a small fraction of rows. A covering index scan avoids heap fetches entirely if all needed columns are in the index.

**Nested Loop Join** iterates over the outer table and performs an index lookup (or scan) for each row against the inner table. It is efficient when the inner table has a unique index on the join key and the outer table is small. For large tables without good indexes, nested loops become very expensive.

**Hash Join** builds a hash table from the smaller table (the build side) and probes it with rows from the larger table (the probe side). Hash joins are efficient for large table joins without index support and are the default for equi-joins in PostgreSQL when tables are large.

**Merge Join** sorts both inputs on the join key and then merges them like a zipper. It requires sorted inputs but is highly efficient for pre-sorted data (e.g., data stored in index order). Merge joins are common when joining on a range condition.

**Cost Estimation** is the optimizer's internal calculation of how expensive each operation will be, expressed in arbitrary units. PostgreSQL shows `cost=0.00..100.50` format (startup cost..total cost). Lower cost does not always mean faster real-world execution — statistics may be stale, or the optimizer may lack information about caching effects.

## How It Works

The query optimizer generates an execution plan using a cost-based approach. It evaluates multiple candidate plans and picks the one with the lowest estimated cost. The optimizer relies on table statistics (row count, column cardinality, null fraction) collected by the database's ANALYZE command. If statistics are stale or missing, the optimizer makes poor decisions — this is why running `ANALYZE` regularly is critical for performance.

```sql
-- PostgreSQL: view an execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 20;

-- Sample output (truncated):
-- Sort  (cost=1023.45..1025.12 rows=668 width=48)
--   Sort Key: (count(o.id)) DESC
--   -> HashAggregate  (cost=900.00..920.00 rows=668 width=48)
--         Batches: 2  Memory Usage: 512kB  Disk Usage: 1024kB
--         -> Hash Join  (cost=50.00..750.00 rows=10000 width=32)
--               Hash Cond: (o.user_id = u.id)
--               -> Seq Scan on orders  (cost=0.00..400.00 rows=10000)
--               -> Hash  (cost=30.00..30.00 rows=1000 width=16)
--                     -> Index Scan using users_pkey on users
--                           Index Cond: (id = o.user_id)
```

The `ANALYZE` option executes the query (with some safeguards) and shows actual row counts and timing, not just estimates. The `BUFFERS` option shows cache hit rates, revealing whether the query is reading from shared memory or hitting disk.

## Practical Applications

Execution plan analysis is the primary tool for SQL performance tuning. When a query runs slowly, `EXPLAIN` reveals whether the database is doing a sequential scan on a 10-million-row table when an index should be used, or whether a nested loop join is causing an N+1 problem. Identifying and adding a missing [[indexes|index]] can reduce query time from seconds to milliseconds.

Database administrators use execution plans to validate the impact of schema changes. Adding a column, changing an index, or partitioning a table can dramatically alter the optimizer's choices. [[Query-optimization]] is iterative: run the query, read the plan, identify the bottleneck, apply an optimization, and repeat.

## Examples

A common problem is a query that performs well with small data but degrades as data grows — the "hidden full table scan" pattern. Consider a query joining three tables where the optimizer chooses a nested loop with the wrong table as the outer relation, causing millions of unnecessary index lookups. Rewriting the query with a hint (or restructured joins) changes the plan to a hash join that processes the data in a more efficient order.

## Related Concepts

- [[query-optimization]] — The broader discipline of improving database query performance
- [[database-indexing]] — Index structures that enable efficient data access
- [[b-tree]] — The most common index data structure underlying database indexes
- [[sql]] — The query language whose execution is planned by the optimizer
- [[big-o-notation]] — Useful mental framework for understanding algorithmic complexity of plan operations

## Further Reading

- PostgreSQL `EXPLAIN` documentation
- "Use The Index, Luke" — SQL indexing and query optimization tutorial
- "SQL Performance Explained" by Winand
- Oracle, MySQL, and SQL Server execution plan documentation

## Personal Notes

I spent years avoiding `EXPLAIN ANALYZE` output because it looked intimidating. Once I learned to read plans from the bottom up and focus on the most expensive (highest cost) operations, it became the most powerful debugging tool in my kit. The single most common cause of slow queries I've encountered is a sequential scan on a large table that an index would eliminate — almost always visible immediately in the plan.
