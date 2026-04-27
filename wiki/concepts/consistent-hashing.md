---
title: "Consistent Hashing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, algorithms, scalability, data-structures]
---

# Consistent Hashing

## Overview

Consistent hashing is a distributed hashing scheme that minimizes key redistribution when nodes are added or removed from a cluster. Traditional hash-based distribution (`hash(key) mod n`) causes O(n) keys to remap when the number of nodes changes, triggering massive data movement and cache invalidation. Consistent hashing, introduced by Karger et al. at MIT in 1997 for use in Akamai's content delivery network, solves this by arranging both keys and nodes on a logical ring (a circular namespace), ensuring only approximately 1/n keys need remapping when nodes are added or removed.

The algorithm is fundamental to distributed systems requiring high availability and scalability—it's used in Amazon DynamoDB, Apache Cassandra, Memcached, Redis Cluster, and many NoSQL databases. Consistent hashing enables horizontal scaling where nodes can be added without disrupting existing data placement, making it essential for systems that must scale dynamically.

## Key Concepts

**Hash Ring**: Consistent hashing maps both keys and nodes to points on a circular hash space, typically using a hash function like MD5 or SHA-1 to distribute values uniformly. Keys are assigned to the first node encountered when traversing the ring clockwise from the key's position.

**Virtual Nodes**: Simple consistent hashing suffers from non-uniform load distribution because nodes map to single points on the ring. Virtual nodes (vnodes) solve this by mapping each physical node to multiple points on the ring, improving load balance. A typical configuration uses 100-200 virtual nodes per physical node.

**Replication**: Consistent hashing naturally supports data replication by assigning each key to the next N nodes clockwise on the ring, providing fault tolerance and geographic distribution.

**Minimum Ring Size**: When using vnodes, the number of virtual nodes determines how finely work can be distributed. Too few vnodes causes uneven distribution; too many increases memory overhead for membership tracking.

## How It Works

The consistent hashing algorithm proceeds as follows:

1. Assign each node a position on the ring by hashing the node identifier (e.g., `hash("node-1")`, `hash("node-2")`)
2. To find which node owns a key, hash the key to a ring position: `hash("user:12345")`
3. Walk clockwise from the key's position to find the first node—this node owns the key
4. For replication, subsequent nodes clockwise become replicas

```python
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        
        for node in nodes or []:
            self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        for i in range(self.replicas):
            key = f"{node}:{i}"
            hash_val = self._hash(key)
            self.ring[hash_val] = node
            self.sorted_keys.append(hash_val)
        self.sorted_keys.sort()
    
    def remove_node(self, node):
        for i in range(self.replicas):
            key = f"{node}:{i}"
            hash_val = self._hash(key)
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)
    
    def get_node(self, key):
        if not self.ring:
            return None
        hash_val = self._hash(key)
        # Binary search for first node >= hash_val
        for node_hash in self.sorted_keys:
            if node_hash >= hash_val:
                return self.ring[node_hash]
        return self.ring[self.sorted_keys[0]]  # Wrap around

# Usage
ring = ConsistentHashRing(nodes=['cache-1', 'cache-2', 'cache-3'])
print(ring.get_node('user:12345'))  # Returns owning node
```

## Practical Applications

Consistent hashing is the backbone of distributed caching systems like Memcached and Redis Cluster, where it determines which cache server stores each key. It enables Amazon DynamoDB and Cassandra to distribute data across clusters while maintaining availability during node failures and additions. Load balancers use consistent hashing to route requests to the same backend server based on session identifiers, maintaining session affinity without centralized state.

The technique is fundamental to [[Distributed Systems]] design, particularly in implementations requiring [[Horizontal Scaling]] and [[High Availability]].

## Examples

A real-world scenario: a content delivery network using consistent hashing to cache user sessions:

```python
# CDN edge cache example
class EdgeCache:
    def __init__(self):
        self.ring = ConsistentHashRing(
            nodes=['edge-us-east', 'edge-us-west', 'edge-eu'],
            replicas=150  # 150 vnodes per edge location
        )
        self.cache = {}  # Simplified local cache
    
    def get(self, user_id, path):
        cache_key = f"{user_id}:{path}"
        edge = self.ring.get_node(cache_key)
        
        # In reality, this would be a network call to the edge
        if edge in self.cache:
            return self.cache[edge].get(cache_key)
        return None
    
    def route_request(self, user_id):
        edge = self.ring.get_node(user_id)
        return f"Routing to {edge} for user {user_id}"

cdn = EdgeCache()
print(cdn.route_request('user-abc-123'))  # Deterministic routing
```

## Related Concepts

- [[Distributed Systems]] - The broader context of multi-node computing
- [[Distributed Caching]] - Using consistent hashing in cache systems
- [[Data Partitioning]] - Strategies for distributing data across nodes
- [[CAP Theorem]] - Tradeoffs in distributed consistency and availability
- [[Amazon DynamoDB]] - Production implementation of consistent hashing
- [[Hash Functions]] - The underlying mechanism for mapping to ring positions

## Further Reading

- Original 1997 paper: "Consistent Hashing and Random Trees" by Karger et al.
- "Cassandra: A Decentralized Structured Storage System" - Practical consistent hashing implementation
- Blog posts by CodeAhoy explaining consistent hashing with visualizations

## Personal Notes

Implementing consistent hashing for the first time, I was surprised how subtle the vnode configuration is in practice. Too few replicas and hot spots develop on specific nodes; too many and the membership gossip protocol carries excessive payload. The ring-based approach also makes it non-trivial to implement features like "move these keys to this node" for planned maintenance. Many production systems add二层 abstractions on top of pure consistent hashing to handle weight configurations and migration quotas. The algorithm is elegant in its simplicity but the operational reality requires careful tooling.
