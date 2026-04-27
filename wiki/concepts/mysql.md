---
title: MySQL
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [mysql, database, sql, rdbms, open-source, backend]
---

# MySQL

## Overview

MySQL is an open-source relational database management system (RDBMS) first released in 1995 by MySQL AB, a Swedish company founded by Michael Widenius (Monty) and David Axmark. It is one of the oldest and most widely deployed database systems in the world, underpinning countless web applications, content management systems, and enterprise software stacks. MySQL uses SQL (Structured Query Language) as its interface for defining, querying, and manipulating data, and stores data in row-based tables with严格定义的 schemas.

MySQL's original creators named it after co-founder Michael Widenius's daughter, My — a naming convention also used by Wikimedia's MariaDB fork (named after his other daughter). Sun Microsystems acquired MySQL AB in 2008 for approximately $1 billion, and Oracle Corporation acquired Sun Microsystems in 2010, inheriting MySQL. This acquisition sparked significant community concern about Oracle's stewardship, leading directly to the creation of MariaDB as a community-driven fork.

Despite these concerns, MySQL has continued to thrive under Oracle's ownership, with regular releases, improved performance, and broad ecosystem support. It is available in multiple editions: the open-source MySQL Community Server, the commercial MySQL Enterprise Edition, and the MySQL Cluster (now MySQL Operator) for distributed deployments. MySQL 8.0, released in 2018, introduced significant improvements including window functions, CTEs (Common Table Expressions), a JSON data type with native functions, and the MySQL Document Store for hybrid SQL/NoSQL workloads.

## Key Concepts

**InnoDB** is MySQL's default storage engine as of MySQL 5.5+ and the most widely used. InnoDB is ACID-compliant (Atomicity, Consistency, Isolation, Durability), supports foreign key constraints, row-level locking for concurrent writes, and crash recovery via its redo log mechanism. Before InnoDB became the default, MyISAM was the default engine — it offered full-text search and count(*) optimization but lacked transactions and foreign key support, making it unsuitable for data-critical applications.

**Replication** is MySQL's built-in mechanism for copying data from a primary (master) database to one or more replica (slave) databases. Replication is asynchronous by default, meaning replicas may lag slightly behind the primary. MySQL supports several replication modes: statement-based replication (replicating SQL statements), row-based replication (replicating actual row changes), and mixed mode. Replication is used for read scaling, geographic distribution, and HA (high availability) failover.

**Partitioning** allows large tables to be split into smaller, more manageable pieces called partitions, based on a partitioning key (range, list, hash, or key-based). Queries that filter on the partition key can dramatically reduce the data scanned, improving query performance. MySQL also supports subpartitioning (partitioning within partitions).

**Stored Procedures and Functions** let developers write executable logic that runs directly inside the database server, reducing round-trips between the application and database. MySQL's stored procedure language is based on SQL/PSM (Persistent Stored Module). Triggers are associated with INSERT, UPDATE, or DELETE events on a specific table to automatically execute defined logic.

**The MySQL Optimizer** analyzes incoming queries and determines the most efficient execution plan, choosing from available indexes, join algorithms (nested loop, hash join, sort-merge), and access methods. Understanding `EXPLAIN` output is a critical skill for diagnosing slow queries. MySQL 8.0 introduced `EXPLAIN ANALYZE`, which actually executes the query and reports real vs. estimated row counts.

## How It Works

MySQL's architecture follows a layered design:

1. **Connection layer**: Handles client connections, authentication, thread pooling, and connection management. MySQL uses thread-per-connection by default (though connection pooling can be implemented at the application level or via proxies like ProxySQL).
2. **SQL layer**: Parses SQL queries into a parse tree, runs the query optimizer to produce an execution plan, and executes the plan by calling the appropriate storage engine APIs.
3. **Storage engine layer**: InnoDB, MyISAM, Memory, and others implement the actual reading and writing of data and index structures. The storage engine layer exposes a unified API (the "handler" interface) so the SQL layer is largely engine-agnostic.

Data in InnoDB is organized into pages (16KB default), which are organized into B+ tree indexes. Primary key access is the fastest because it directly navigates the clustered index. Secondary indexes store primary key values rather than row pointers, so a secondary index lookup requires traversing the secondary index B+ tree, then the primary key index B+ tree.

## Practical Applications

- **Web applications**: MySQL is the "M" in the classic LAMP stack (Linux, Apache, MySQL, PHP/Python/Perl). WordPress, Drupal, and Joomla all use MySQL as their default database.
- **E-commerce**: Magento, WooCommerce, and many Shopify backends use MySQL.
- **Data warehousing**: While not specialized for analytics like ClickHouse or Redshift, MySQL handles OLTP workloads efficiently and integrates with BI tools via connectors.
- **SaaS platforms**: Many multi-tenant SaaS applications use MySQL with schema-per-tenant or database-per-tenant isolation patterns.

## Examples

Creating a table with InnoDB, adding an index, and writing a query:

```sql
CREATE TABLE orders (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  status ENUM('pending', 'shipped', 'delivered', 'cancelled') NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Query using the composite index
SELECT id, total, status, created_at
FROM orders
WHERE user_id = 42 AND status IN ('pending', 'shipped')
ORDER BY created_at DESC
LIMIT 10;
```

## Related Concepts

- [[SQL]] — The structured query language used to interact with MySQL
- [[Database]] — The broader concept of organized data storage and retrieval
- [[Relational Database]] — The type of database MySQL implements
- [[InnoDB]] — MySQL's default and most important storage engine
- [[Replication]] — MySQL's mechanism for distributing data across multiple servers

## Further Reading

- "High Performance MySQL" by Baron Schwartz et al. — The definitive book on MySQL optimization
- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [Use The Index, Luke](https://use-the-index-luke.com/) — Excellent guide to SQL indexing (works for all RDBMS)

## Personal Notes

MySQL's simplicity is both its strength and its limitation. You can get a production-grade database up in minutes, but at scale you need to understand InnoDB internals — buffer pool sizing, redo log configuration, lock monitoring — to avoid performance cliffs. I've found that most MySQL performance problems boil down to missing indexes or poorly written queries that generate full table scans. `EXPLAIN ANALYZE` has become my first tool of choice when debugging slow queries.
