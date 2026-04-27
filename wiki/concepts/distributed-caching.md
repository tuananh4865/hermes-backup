---
title: Distributed Caching
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, caching, scalability, performance, redis, memcached]
---

# Distributed Caching

## Overview

Distributed caching is a technique for storing frequently accessed data across multiple servers to provide fast, low-latency access to cached information while maintaining high availability and fault tolerance. Unlike a single-node in-memory cache, a distributed cache spans multiple machines, allowing the cache to scale horizontally, handle larger datasets than any single machine's memory would permit, and survive failures of individual nodes without losing the entire cache.

In modern web architectures, distributed caches sit between application servers and databases (or upstream services), dramatically reducing latency for read-heavy workloads and reducing load on origin systems. When a user requests data that is already cached, the response can be returned in microseconds from memory rather than milliseconds from a database. This performance improvement is often the difference between a snappy, responsive application and one that feels sluggish under load.

Distributed caches are a critical component of [[scalability]] architecture. As traffic grows, adding cache nodes is often more cost-effective than scaling database infrastructure. They also provide a layer of insulation against [[distributed-systems]] failures — if a database becomes temporarily unavailable, cached data can often serve read traffic until the database recovers.

## Key Concepts

### Cache Topologies

Distributed caches can be organized in several topologies, each with different tradeoffs:

** replicated cache**: Each node holds a full copy of the cached data. This provides the highest read performance (any node can serve any request) but has the highest memory cost and write complexity (updates must be propagated to all replicas). Memcached's default deployment model is effectively a replicated cache.

**Partitioned (Sharded) Cache**: Each node holds a distinct portion of the cached data, determined by a partitioning strategy. A client determines which node holds a given key by applying a [[consistent-hashing]] or similar algorithm. This model scales linearly with the number of nodes but introduces complexity for operations that span multiple keys.

**Read-Through / Write-Through**: In this pattern, the cache sits transparently between the application and the origin database. On a cache miss, the cache fetches from the origin and populates itself before returning. On writes, updates go to both the cache and the origin, ensuring consistency. This allows existing applications to add caching without changing application logic.

**Write-Behind (Write-Back)**: Updates are written to the cache immediately and asynchronously flushed to the origin. This provides the best write performance but risks data loss if the cache node fails before the write reaches the origin. It is used in scenarios where occasional data loss is acceptable (like analytics event tracking).

### Cache Invalidation Strategies

The biggest challenge in distributed caching is keeping the cache consistent with the source of truth. Stale data can lead to incorrect business decisions, security vulnerabilities, or regulatory violations. Several invalidation strategies exist:

**LRU (Least Recently Used)**: When the cache is full, evict the least recently accessed entry. Simple and effective for general workloads, but can be expensive to maintain exactly in a distributed setting.

**TTL (Time-To-Live)**: Each cache entry has an expiration time. After TTL expires, the entry is considered stale and must be refreshed from the origin on next access. TTL is simple to implement but introduces a trade-off: short TTLs mean fresher data but more origin load; long TTLs mean better cache hit rates but potentially stale data.

**Explicit Invalidation**: When the underlying data changes (e.g., a user updates their profile), the application explicitly deletes or updates the corresponding cache entries. This requires application-level awareness of cache keys and is more complex but provides the strongest consistency guarantees.

**Event-Driven Invalidation**: A more sophisticated approach where the cache subscribes to events from the origin system (e.g., database change data capture events, message queue notifications). When relevant events occur, the cache automatically invalidates affected entries. This is used in sophisticated architectures like those built around [[event-driven-architecture]].

### Consistency and Partition Tolerance

Distributed caches, like all distributed systems, must navigate the [[cap-theorem]]. A distributed cache can be consistent (all nodes see the same data at the same time), available (every request gets a response), and partition tolerant (continues operating despite network partitions between nodes) — but not all three simultaneously.

Most distributed caches prioritize availability and partition tolerance, sacrificing strong consistency. They implement **eventual consistency** — updates propagate asynchronously, and given enough time without further updates, all replicas will converge to the same value. For many applications, eventual consistency is acceptable. For others (financial balances, inventory counts), stronger guarantees may be required, potentially requiring distributed locking or consensus protocols.

## How It Works

A typical distributed cache deployment involves multiple cache nodes arranged in a cluster, a client library that knows how to route requests to the correct node, and coordination infrastructure for cluster management:

**Consistent Hashing**: When a client needs to store or retrieve a key, it computes which node owns that key using a hash ring. Each node is assigned a position on the ring (using the hash of its identifier), and each key is assigned to the first node encountered clockwise from the key's hash position. When nodes are added or removed, only a fraction of keys remap, minimizing disruption.

**Cluster Membership**: Nodes must know about each other to route requests and replicate data. Gossip protocols (used by Cassandra and Consul) allow nodes to discover and track the membership of the cluster without a central coordinator. Other systems use a dedicated coordinator process (like ZooKeeper) for cluster state management.

**Data Replication**: For fault tolerance, cached data is typically replicated to multiple nodes. Synchronous replication ensures strong consistency but adds latency. Asynchronous replication provides lower latency but risks losing the most recent updates if a node fails before replication completes.

**Connection Pooling**: Clients maintain pools of connections to cache nodes, reusing connections across requests to avoid the overhead of establishing new connections for each operation. Connection pools also limit concurrent connections to prevent node overload.

## Practical Applications

### Web Application Caching

The most common use case: caching rendered HTML fragments, API responses, database query results, and session data. A typical stack might have [[redis]] or [[memcached]] caching database query results, [[cdn]] caching static assets at the edge, and application-level in-memory caches (like Python's functools.lru_cache) for hot in-process data.

### API Rate Limiting

Distributed caches store rate limiting counters and sliding window data across multiple application servers. Each incoming request increments a counter in the distributed cache, and servers check the counter before processing requests. Without a distributed cache, rate limiting would be trivially bypassed by hitting different servers.

### Session Storage

Web applications store user sessions (login state, shopping cart contents, preferences) in a distributed cache rather than in the application server's local memory. This enables stateless application servers (easy horizontal scaling) while maintaining session continuity when users are routed to different servers by the [[load-balancer]].

### ML Inference Caching

Machine learning models that perform the same inference repeatedly (e.g., recommendation models for the same user, NLP features for the same document) cache inference results. An LLM caching layer likeGGUF or a vector cache stores computed embeddings or inference outputs, reducing GPU compute costs and latency dramatically.

## Examples

Using Redis as a distributed cache with a read-through pattern:

```python
import redis
import json
import hashlib

redis_client = redis.Redis(host='redis-cluster', port=6379, decode_responses=True)

def get_user_profile(user_id):
    cache_key = f"user:profile:{user_id}"
    
    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss — fetch from database
    profile = db.fetch_user(user_id)
    
    # Store in cache with 5-minute TTL
    redis_client.setex(
        cache_key,
        ttl=300,  # 5 minutes
        value=json.dumps(profile)
    )
    return profile

def update_user_profile(user_id, updates):
    # Write to database
    db.update_user(user_id, updates)
    
    # Explicitly invalidate cache to prevent stale reads
    cache_key = f"user:profile:{user_id}"
    redis_client.delete(cache_key)
```

Using consistent hashing for cache sharding:

```python
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes, virtual_nodes=100):
        self.ring = {}
        self.sorted_keys = []
        self.virtual_nodes = virtual_nodes
        
        for node in nodes:
            self.add_node(node)
    
    def add_node(self, node):
        for i in range(self.virtual_nodes):
            key = hashlib.md5(f"{node}:{i}".encode()).hexdigest()
            self.ring[key] = node
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key):
        hash_key = hashlib.md5(key.encode()).hexdigest()
        for sorted_key in self.sorted_keys:
            if hash_key <= sorted_key:
                return self.ring[sorted_key]
        return self.ring[self.sorted_keys[0]]  # Wrap around

ring = ConsistentHashRing(['cache-1', 'cache-2', 'cache-3'])
node = ring.get_node("user:123")  # Always routes to same node for same key
```

## Related Concepts

- [[caching]] — The general principle of storing data for faster future access
- [[redis]] — Popular in-memory distributed cache
- [[memcached]] — High-performance distributed memory caching system
- [[consistent-hashing]] — Partitioning strategy that minimizes reshuffling on node changes
- [[cap-theorem]] — Tradeoff constraints facing all distributed systems
- [[distributed-systems]] — The architectural foundation for distributed caches
- [[scalability]] — The problem distributed caches help solve
- [[cdn]] — Edge caching for static and dynamic content
- [[load-balancer]] — Routes traffic; often used alongside distributed caches

## Further Reading

- "Caching: Architecture and Patterns" — Overview of caching strategies
- Redis Documentation — Deep dive into Redis data structures and clustering
- "Consistent Hashing and Random Trees" — Original consistent hashing paper
- "Memcached Internals" — Understanding the memory model and protocol

## Personal Notes

The most common distributed caching mistake I've seen is treating the cache as always consistent with the database. Cache invalidation is genuinely hard — when you update a record in the database, finding every cached version of that record across a distributed cache cluster is non-trivial. I've found that the most robust approach is optimistic: assume the cache will eventually be invalidated, use short TTLs as a safety net, and treat cache hits as hints rather than gospel. For truly critical data (financial balances, inventory), I prefer write-through with explicit invalidation and accept the latency cost. Also, watch your cache hit rate carefully — a cache with a 10% hit rate might be costing more in infrastructure than it saves in database load.
