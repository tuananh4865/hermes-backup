---
title: "MariaDB"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [mariadb, database, sql, mysql-fork, open-source, backend]
---

# MariaDB

## Overview

MariaDB is a free, open-source relational database management system (RDBMS) that serves as a community-developed fork of [[MySQL]]. It was created in 2010 after concerns arose about Oracle's acquisition of MySQL and whether the open-source project would continue to be developed freely. MariaDB is named after Michael "Monty" Widenius's youngest daughter, following the naming tradition started with MySQL (named after his other daughter).

MariaDB maintains strong compatibility with MySQL while adding significant new features, performance optimizations, and storage engines not available in the original project. The database is a drop-in replacement for MySQL in most cases, meaning existing MySQL databases and applications can often migrate to MariaDB without code changes. It is the default database in many Linux distributions, including Debian and Red Hat Enterprise Linux, and is used by organizations ranging from Wikipedia and Google to Samsung and booking.com.

As a relational database, MariaDB stores data in tables with rows and columns, uses [[SQL]] for queries, and supports [[ACID]] transactions with [[MVCC]] (Multi-Version Concurrency Control) similar to [[PostgreSQL]]. It runs on Linux, Windows, macOS, and various Unix-like operating systems, making it accessible for virtually any development environment or production deployment.

## Key Concepts

**Storage Engines**: MariaDB's architecture supports multiple storage engines, each optimized for different use cases:

| Engine | Description |
|--------|-------------|
| InnoDB | Default engine; supports transactions, row-level locking, foreign keys |
| MyRocks | Facebook-developed; optimized for write-heavy workloads and compression |
| Aria | Crash-safe alternative to MyISAM; supports full-text indexing |
| Memory | In-memory storage; extremely fast for temporary tables and caches |
| ColumnStore | Column-oriented engine for analytics and big data |
| Spider | Sharding engine for horizontal partitioning across servers |

**Compatibility with MySQL**: MariaDB maintains API and protocol compatibility with MySQL, allowing most MySQL connectors and tools to work without modification. The `mysql` command-line client and most GUI tools like [[phpMyAdmin]] work seamlessly with both databases.

**Thread Pool**: MariaDB includes an improved thread pool implementation that more efficiently handles thousands of connections by reducing overhead from thread creation. This is particularly valuable for web applications with many concurrent but mostly idle connections.

**Virtual Columns**: MariaDB supports computed columns that store pre-calculated values based on other column data, enabling efficient querying without application-level computation:

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    price DECIMAL(10,2),
    quantity INT,
    total DECIMAL(10,2) AS (price * quantity) STORED
);
```

## How It Works

MariaDB follows the traditional client-server architecture:

1. **Client Connection**: Applications connect via the MariaDB client library or connector (available for PHP, Python, Java, Node.js, and other languages) using TCP/IP or Unix sockets.

2. **Connection Handling**: The server spawns a thread for each connection. The thread handles authentication, query parsing, execution, and result delivery.

3. **Query Processing**: When a SQL query arrives, the parser validates syntax, the optimizer creates an execution plan using statistics from storage engines, and the executor runs the plan and returns results.

4. **Storage Engine Layer**: The storage engines handle the actual data storage and retrieval. InnoDB stores data in tablespaces, MyRocks uses RocksDB's log-structured merge trees, and Aria uses its own crash-safe table format.

5. **Replication**: MariaDB supports asynchronous and semi-synchronous replication. Primary server writes to a binary log; replicas connect and apply those changes to their own data:

```bash
# Primary configuration (my.cnf)
[mariadb]
log-bin
server-id=1
binlog_format=ROW

# Replica configuration
[mariadb]
server-id=2
relay-log=relay-bin
read_only=ON
```

## Practical Applications

**Web Applications**: MariaDB powers countless websites and web applications, particularly in the LAMP/LEMP stack (Linux, Apache/Nginx, MariaDB, PHP/Python). Its compatibility with MySQL makes it a natural choice for WordPress, Drupal, and other popular CMS platforms.

**Data Warehousing**: With the ColumnStore engine, MariaDB handles analytical queries on large datasets efficiently. It can replace expensive commercial data warehouses for many business intelligence use cases.

**Financial Systems**: The InnoDB engine's ACID compliance and row-level locking make MariaDB suitable for financial applications requiring transactional integrity, such as accounting software and transaction logging.

**High-Availability Clustering**: MariaDB Galera Cluster provides synchronous multi-master replication, ensuring all nodes have identical data and can handle write traffic with automatic failover:

```bash
# Basic Galera Cluster configuration
[mariadb]
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_address="gcomm://node1,node2,node3"
binlog_format=ROW
default_storage_engine=InnoDB
```

## Examples

**Basic Database Operations**:

```sql
-- Create database and tables
CREATE DATABASE IF NOT EXISTS myapp;
USE myapp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Insert with transactions
START TRANSACTION;
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');
INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com');
COMMIT;

-- Query with joins
SELECT u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING order_count > 5;
```

**User Management and Permissions**:

```sql
-- Create application user with limited privileges
CREATE USER 'myapp'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.* TO 'myapp'@'localhost';

-- Create read-only reporting user
CREATE USER 'reporter'@'%' IDENTIFIED BY 'report_password';
GRANT SELECT ON myapp.* TO 'reporter'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
```

**Backup and Restore**:

```bash
# Full backup using mysqldump
mysqldump -u root -p --all-databases > backup.sql
mysqldump -u root -p myapp > myapp_backup.sql

# Point-in-time recovery using binary logs
mysql -u root -p myapp < myapp_backup.sql
mysqlbinlog --stop-datetime="2026-04-13 10:00:00" /var/log/mariadb/bin-log.000001 | mysql -u root -p

# Physical backup with Mariabackup
mariabackup --backup --target-dir=/backup --user=root --password=secret
mariabackup --prepare --target-dir=/backup
mariabackup --copy-back --target-dir=/backup
```

## Related Concepts

- [[MySQL]] - The original database MariaDB forked from
- [[SQL]] - The query language for relational databases
- [[PostgreSQL]] - Another popular open-source relational database
- [[Database]] - General database concepts and terminology
- [[ACID]] - Transaction properties MariaDB supports
- [[MVCC]] - Concurrency control mechanism in InnoDB
- [[Replication]] - Data copying between MariaDB servers
- [[phpMyAdmin]] - Web interface for MariaDB administration
- [[Galera Cluster]] - Synchronous multi-master clustering for MariaDB

## Further Reading

- [MariaDB Documentation](https://mariadb.com/kb/en/documentation/)
- [MariaDB Knowledge Base](https://mariadb.com/kb/en/knowledge-base/)
- "Understanding MySQL and MariaDB" by Yvo van Doorn
- [MariaDB Foundation](https://mariadb.org/)

## Personal Notes

MariaDB has become my go-to relational database for most projects where PostgreSQL isn't specifically required. The Galera Cluster functionality is particularly impressive for applications requiring high availability without the complexity of managing a full [[PostgreSQL]] replication setup. I've found the MyRocks engine valuable for write-intensive workloads like logging systems where the compression ratio can significantly reduce storage requirements. Migration from MySQL has been painless in every case I've encountered—the drop-in replacement promise generally delivers.
