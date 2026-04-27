---
title: Database Replication
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, distributed-systems, high-availability, scalability]
---

# Database Replication

## Overview

Database replication is the process of copying and maintaining database objects (tables, entire databases) across multiple database servers. Replication provides redundancy, improves read scalability, and can enhance availability by allowing applications to fail over to replica servers when the primary fails. It is a fundamental technique for building resilient, high-performance database infrastructure.

Replication can be synchronous (wait for confirmation from replicas before committing) or asynchronous (commit to primary and propagate changes later). Each approach has trade-offs: synchronous provides stronger consistency but adds latency, while asynchronous offers better performance at the cost of potential temporary inconsistency.

Modern database systems implement replication through various mechanisms including log shipping, statement-based replication, row-based replication, and virtual synchronous replication. Understanding these mechanisms helps in diagnosing issues, optimizing performance, and designing reliable database architectures.

## Key Concepts

### Primary-Replica Architecture

The most common replication topology:

- **Primary (Master)**: Handles all writes and optionally reads
- **Replica (Slave/Standby)**: Receives changes from primary, serves reads

Write operations propagate from primary to replicas. If the primary fails, a replica can be promoted to take over.

### Synchronous vs Asynchronous Replication

**Synchronous**: Transaction commits only after replicas confirm receipt. Guarantees no data loss but increases latency, especially with distant replicas.

```
BEGIN TRANSACTION
  INSERT INTO orders VALUES (...)
COMMIT
    ↓
Wait for 2 of 3 replicas to acknowledge
    ↓
Transaction confirmed
```

**Asynchronous**: Primary commits locally and propagates changes in background. Lower latency but potential for data loss if primary fails before propagation.

### Replication Modes

- **Statement-based**: Replicas replay SQL statements (e.g., `UPDATE orders SET...`)
- **Row-based**: Replicas replay row changes (before/after images)
- **Mixed**: Database chooses per-statement which method to use

### Failover and Promotion

When a primary fails:

1. Detection: Monitoring system identifies primary is unreachable
2. Promotion: A replica is designated as the new primary
3. Reconfiguration: Applications redirect writes to new primary
4. Recovery: Old primary, if recoverable, becomes a replica

Automatic failover minimizes downtime but requires careful implementation to avoid split-brain scenarios.

## How It Works

### PostgreSQL Streaming Replication

PostgreSQL uses WAL (Write-Ahead Logging) for replication:

```
Primary Server
    ↓
WAL records generated for each write
    ↓
WAL sender process streams to replicas
    ↓
Replica servers
    ↓
WAL receiver → replay to local database
```

The replica applies changes in real-time, maintaining near-current state.

### MySQL Binary Log Replication

MySQL records changes in the binary log:

1. Primary writes to binary log
2. Replica's IO thread copies binary log events to relay log
3. Replica's SQL thread replays relay log

```sql
-- Check replication status on replica
SHOW REPLICA STATUS\G

-- Key columns to monitor:
-- Seconds_Behind_Source: lag in seconds
-- Replica_IO_Running: IO thread status
-- Replica_SQL_Running: SQL thread status
-- Relay_Log_File: current relay log position
```

## Practical Applications

### Read Scaling

Direct read traffic to replicas to scale read throughput:

```python
# Simple load balancing between primary and replicas
import random

class DatabaseRouter:
    def __init__(self, primary, replicas):
        self.primary = primary
        self.replicas = replicas
    
    def get_connection(self, for_write=False):
        if for_write:
            return self.primary
        # Round-robin or random replica selection
        return random.choice([self.primary] + self.replicas)
```

### Geographic Distribution

Place replicas in different data centers for lower latency to global users:

- US West: Primary
- US East: Replica for East Coast users
- EU: Replica for European users

### High Availability

Automatic failover ensures continuous availability:

```yaml
# Patroni configuration example for PostgreSQL HA
scope: postgres-cluster
namespace: /db/
name: node-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: node-1:8008

databases:
  postgres:
    action:
      - checkout_leader: 30
      - promote: request

consul:
  host: 127.0.0.1:8500
  register_service: true
```

### Disaster Recovery

Maintain offsite replicas for protection against site-wide failures:

```
Primary: AWS us-east-1
Replica 1: AWS us-west-2 (cross-region backup)
Replica 2: On-premises datacenter (hybrid cloud backup)
```

## Examples

Monitoring replication lag in PostgreSQL:

```sql
-- Check replication status on primary
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
       (sent_lsn - replay_lsn) AS replication_lag
FROM pg_stat_replication;

-- Monitor replay lag on replica
SELECT now() - pg_last_xact_replay_timestamp() AS replication_delay;

-- Create a replication slot (ensures WAL retention)
SELECT pg_create_physical_replication_slot('standby1_slot');
```

## Related Concepts

- [[Distributed Databases]] - Databases spanning multiple nodes
- [[Consistency Models]] - Understanding ACID and eventual consistency
- [[Failover]] - Automatic switching to backup systems
- [[CAP Theorem]] - Trade-offs in distributed systems
- [[Database Sharding]] - Horizontal partitioning of data

## Further Reading

- "Database Internals" by Alex Petrov
- PostgreSQL Documentation: High Availability
- MySQL Replication Documentation
- "Designing Data-Intensive Applications" by Martin Kleppmann

## Personal Notes

Replication is essential but adds complexity. Monitor replication lag continuously—if your replica is 30 minutes behind, you're not getting the HA benefits you think. For truly critical systems, synchronous replication or Quorum commits provide stronger guarantees. Also, remember that replication protects against hardware failure, not data corruption or software bugs—if bad data gets written to primary, it propagates to replicas. Regular backups remain essential.
