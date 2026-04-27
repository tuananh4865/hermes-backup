---
title: "Cassandra"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [database, nosql, distributed-systems, scalable, wide-column-store]
---

# Cassandra

## Overview

Apache Cassandra is an open-source, distributed NoSQL database designed to handle massive amounts of data across multiple commodity servers without a single point of failure. Originally developed at Facebook (released as open-source in 2008) and now maintained by the Apache Software Foundation, Cassandra excels at providing high availability, linear scalability, and tunable consistency—making it the preferred choice for applications requiring uptime guarantees and the ability to write anywhere in the cluster.

Unlike traditional relational databases that run on single servers or rely on primary-replica replication, Cassandra uses a peer-to-peer architecture where every node is equal and can serve any request. Data is distributed across the cluster using consistent hashing, and the gossip protocol enables nodes to discover cluster topology and detect failures. This design means Cassandra has no master node to fail—no downtime for planned maintenance either, as nodes can be upgraded incrementally.

Cassandra's data model is a hybrid between a key-value store and a traditional relational database: it uses wide-column families (similar to Google Bigtable's model) organized into keyspaces, with rows identified by a primary key and columns that can be added dynamically.

## Key Concepts

### Data Model

Cassandra organizes data in a hierarchy: **Keyspace** (database) → **Table** (column family) → **Row** → **Column**. Unlike SQL, tables must be designed with specific query patterns in mind—denormalization is expected and encouraged. This "query-first" design contrasts with relational modeling's "normalize then optimize" approach.

Primary keys consist of a partition key (determining which node stores the data) and optional clustering columns (determining sort order within a partition):

```sql
CREATE KEYSPACE IF NOT EXISTS users WITH REPLICATION = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3
};

CREATE TABLE users_by_email (
  email TEXT PRIMARY KEY,
  user_id UUID,
  name TEXT,
  created_at TIMESTAMP
);

CREATE TABLE user_posts (
  user_id UUID,
  post_id TIMEUUID,
  title TEXT,
  content TEXT,
  PRIMARY KEY (user_id, post_id)
) WITH CLUSTERING ORDER BY (post_id DESC);
```

### Consistency Levels

Cassandra offers tunable consistency—you can choose how many replicas must acknowledge a read or write. Higher consistency means stronger guarantees but slower performance; lower consistency means faster writes but potential staleness:

- **ONE**: Only one replica responds (fastest write, possible stale reads)
- **QUORUM**: Majority of replicas respond (balanced)
- **ALL**: All replicas must respond (strongest consistency, slowest)
- **LOCAL_QUORUM**: Quorum within the local datacenter (for geo-distributed clusters)

```python
# Python driver example with consistency level
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster(['10.0.0.1', '10.0.0.2', '10.0.0.3'])
session = cluster.connect('users')

query = SimpleStatement(
    "INSERT INTO user_posts (user_id, post_id, title, content) VALUES (%s, %s, %s, %s)",
    consistency_level=ConsistencyLevel.QUORUM
)
session.execute(query, (user_id, post_id, title, content))
```

### The CAP Theorem

Cassandra is often described as an AP system (Available and Partition-tolerant) in the CAP theorem, though this is configurable. In practice, Cassandra prioritizes availability during network partitions—writes never fail because any node can accept them—but you can tune toward stronger consistency when needed. For most use cases, QUORUM provides a good balance.

## How It Works

When a write occurs, Cassandra uses a partitioner (typically Murmur3) to compute a token hash from the partition key, determining which node(s) own the data range. The coordinator node (the one receiving the request) routes the write to the appropriate replicas based on the replication strategy defined for the keyspace.

Writes are written to a commit log (for durability) and to an in-memory structure called a memtable. When memtables fill up, they're flushed to disk as SSTables (Sorted String Tables). Over time, SSTables accumulate and Cassandra runs compaction to merge them, reclaiming space and improving read performance.

## Practical Applications

**Time-Series Data**: Cassandra handles high write throughput, making it popular for IoT sensor data, monitoring metrics, and financial tick data. The wide columns naturally model time-series with many data points per timestamp.

**Messaging and Chat**: WhatsApp, Discord, and Netflix Message use Cassandra for storing message history with time-based queries and user-specific partitions.

**Product Catalogs**: E-commerce platforms use Cassandra for product catalogs where read/write ratios vary by product popularity and inventory needs must be real-time.

**Activity Logs and Events**: High-volume event logging from web or mobile applications—Cassandra's linear scaling means capacity grows by adding nodes rather than migrating to larger servers.

## Examples

A practical Python example querying Cassandra with the DataStax driver:

```python
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timedelta

# Connect to Cassandra
cluster = Cluster(['10.0.0.1', '10.0.0.2'], 
                  auth_provider=PlainTextAuthProvider('cassandra', 'password'))
session = cluster.connect('mykeyspace')

# Query user posts from the last week
one_week_ago = datetime.now() - timedelta(days=7)

# Use prepared statements for efficiency
prepared = session.prepare("""
    SELECT post_id, title, content, writetime
    FROM user_posts
    WHERE user_id = ? AND post_id > ?
    ORDER BY post_id DESC
    LIMIT 20
""")

result = session.execute(prepared, [user_id, one_week_ago])
for row in result:
    print(f"{row.title}: {row.content[:50]}...")
```

## Related Concepts

- [[NoSQL]] - Broad category of non-relational databases
- [[Distributed Systems]] - Field of systems like Cassandra that span multiple nodes
- [[Eventual Consistency]] - Consistency model where updates propagate asynchronously
- [[SSTable]] - On-disk format Cassandra uses for storing data
- [[Gossip Protocol]] - Failure detection mechanism in Cassandra clusters
- [[Wide-Column Store]] - NoSQL database model Cassandra implements

## Further Reading

- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
- [DataStax Driver Documentation](https://docs.datastax.com/en/developer/python-driver/latest/) - Popular Python client
- [Cassandra: The Definitive Guide](https://www.datastax.com/resources/whitepaper/cassandra-the-definitive-guide) - Comprehensive book

## Personal Notes

Cassandra's "write-everywhere" philosophy means consistency bugs can be subtle—replicas can diverge during network partitions and won't auto-resolve. Operations teams need robust monitoring and careful capacity planning. Also, the data modeling learning curve is steep if you're coming from relational backgrounds—you genuinely need to design tables around query patterns, not domain entities. Once that clicks, though, the operational simplicity of "add nodes to scale" is genuinely freeing.
