---
title: "Database Proxy"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, middleware, proxy, connection-pooling, sharding]
---

# Database Proxy

## Overview

A database proxy is an intermediate layer that sits between application code and a database server. It intercepts queries, can modify or route them, and manages connections on behalf of clients. Database proxies provide functionality like connection pooling, query routing, load balancing,读写分离 (read/write splitting), sharding, and security enforcement without requiring changes to application code.

Proxies are particularly valuable in distributed database architectures where a single logical database spans multiple physical servers, or where you need to offload infrastructure concerns from application logic. They can implement sophisticated routing logic based on query analysis, distribute load across replicas, and provide a unified endpoint for connection management.

## Key Concepts

**Connection Pooling** is the primary function of most database proxies. Creating new database connections is expensive (network round-trip, authentication, TCP handshake). A proxy maintains a pool of pre-established connections and assigns them to clients as needed. This amortizes connection overhead across many requests and prevents applications from exhausting the database's connection limit.

**Read/Write Splitting** routes read queries to replica databases and write queries to the primary. This scales read throughput horizontally by adding read replicas while keeping writes centralized. The proxy must parse queries to determine type (SELECT vs INSERT/UPDATE/DELETE) and route accordingly.

**Query Routing** goes beyond simple read/write splitting. Advanced proxies can:
- Route queries to specific shards based on a routing key (see [[Sharding]])
- Route specific tables or queries to specific database instances
- Aggregate results from multiple shards for queries that span partitions

**Prepared Statement Handling** requires careful proxy implementation. Some proxies must re-prepare statements on each connection since prepared statements are connection-specific, while others cache prepared statements across connections or handle statement state differently per protocol.

## How It Works

A database proxy typically operates in one of two modes:

**Proxy Mode**: The application connects to the proxy instead of the database directly. The proxy maintains its own connection pool to the actual database servers. This is transparent to the application—the proxy appears to be the database.

```bash
# Application connects to proxy
app -> proxy (connection pool) -> primary database
                        \-> read replica 1
                        \-> read replica 2
```

**Sidecar Mode**: The proxy runs alongside each application instance or as a Kubernetes sidecar container. It intercepts local database calls and manages connections through a local daemon, reducing cross-namespace network traffic.

Most production proxies (like [[PgBouncer]], [[ProxySQL]], or [[Vitess]]) operate in proxy mode and support multiple database protocols including [[PostgreSQL]] and [[MySQL]].

## Practical Applications

**Multi-Tenant SaaS**: A proxy can enforce tenant isolation, route each tenant's queries to their dedicated database schema, and prevent cross-tenant data access at the infrastructure level.

**Horizontal Scaling**: Route queries to appropriate shards based on tenant ID, user ID, or geographic region to distribute load across multiple database instances.

**Rolling Deployments**: Proxy allows database upgrades without downtime by gradually shifting traffic from old to new database versions while maintaining connection compatibility.

**Security Enforcement**: Centralize query filtering, prevent dangerous operations (like `DROP TABLE`), enforce prepared statement usage, and add authentication caching.

## Examples

Configuring ProxySQL for read/write splitting in MySQL:

```ini
# proxysql.cnf

# Define the backend databases
mysql_servers:
(
    { address="10.0.0.1", port=3306, hostgroup=0, status="MASTER" },  -- primary
    { address="10.0.0.2", port=3306, hostgroup=1, status="REPLICA" }, -- replica 1
    { address="10.0.0.3", port=3306, hostgroup=1, status="REPLICA" }  -- replica 2
)

# Route writes to hostgroup 0, reads to hostgroup 1
mysql_query_rules:
(
    { rule_id=1, match_pattern="^SELECT.*FOR UPDATE", destination_hostgroup=0, apply=1 },
    { rule_id=2, match_pattern="^SELECT", destination_hostgroup=1, apply=1 },
    { rule_id=3, match_pattern=".", destination_hostgroup=0, apply=1 }  -- everything else to primary
)
```

Connection pooling with PgBouncer:

```ini
; pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

## Related Concepts

- [[Connection Pooling]] - Managing reusable database connections
- [[Sharding]] - Horizontal partitioning of data across databases
- [[read-write-splitting]] - Distributing reads to replicas for scalability
- [[PgBouncer]] - PostgreSQL connection pooler
- [[ProxySQL]] - MySQL proxy with advanced routing
- [[Vitess]] - Database clustering system that includes proxy routing

## Further Reading

- [ProxySQL Documentation](https://proxysql.com/documentation/) - Comprehensive proxy configuration guide
- [PgBouncer Documentation](https://www.pgbouncer.org/) - PostgreSQL connection pooling
- [Vitess Documentation](https://vitess.io/docs/) - Horizontal scaling for MySQL

## Personal Notes

Database proxies are often invisible infrastructure, but they're critical for scaling. When designing multi-tenant systems, I route tenant traffic through a proxy layer—it's much easier to implement tenant-specific routing, rate limiting, and failover at the proxy level than in application code.

The biggest gotcha with proxies is prepared statements. If you're using an ORM that heavily relies on prepared statements, test thoroughly with your proxy configuration. Some proxies handle them poorly or require specific settings to work correctly.

Also watch out for connection pool saturation during traffic spikes. With transaction-mode pooling (releases connection back to pool after each transaction), you need enough pool size to handle concurrent transactions. Monitor `pools` and `clients` metrics in PgBouncer or equivalent.
