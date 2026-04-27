---
title: "Cache"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [caching, performance, memory-hierarchy, distributed-systems, web-performance]
---

# Cache

## Overview

Cache is a hardware or software mechanism that stores data in a location designed for faster access than the original source. The fundamental principle behind caching is the observation that programs frequently access the same data multiple times—caching exploits this locality of reference to reduce access latency and improve system performance. Whether it's a CPU cache holding recently accessed memory, a CDN cache storing web content at edge locations, or an application cache holding computed results, the underlying concept remains consistent: store frequently accessed data closer to where it's consumed.

Caches exist at multiple levels of computing systems, forming a memory hierarchy from the fastest, smallest, most expensive storage (closest to the CPU) to slower, larger, cheaper storage (further away). This hierarchy reflects fundamental tradeoffs between speed, capacity, and cost. Registers within the CPU provide the fastest access but hold only tiny amounts of data. L1, L2, and L3 CPU caches store recently used memory contents. Main memory (RAM) provides larger capacity with slower access times. Disk-based storage and network-accessed data provide the largest capacity but the slowest access.

In software systems, caching takes many forms beyond hardware memory hierarchies. Web browsers cache static assets to avoid repeated network requests. Content delivery networks cache copies of media and web content at geographically distributed servers. Database systems cache query results and index pages in memory. Application servers cache computed results, API responses, and session data. Each caching layer reduces latency and load on backend systems, improving both performance and scalability.

Understanding caching principles is essential for building performant systems. Cache hit rates—the percentage of data requests served from cache versus requiring retrieval from the original source—directly impact performance. Cache invalidation strategies determine how cached data is updated when the source data changes. The complexity of keeping caches consistent with source data is a fundamental challenge in distributed systems.

## Key Concepts

**Cache Hit and Cache Miss** are the two fundamental outcomes of a cache lookup. A cache hit occurs when the requested data is found in the cache, enabling fast retrieval. A cache miss occurs when the data is not in the cache, requiring retrieval from the slower underlying storage. Cache performance is typically measured by hit rate (hits divided by total requests) or miss rate (misses divided by total requests). Even a small improvement in hit rate can dramatically improve overall performance, given the large latency difference between cache and backend storage.

**Temporal and Spatial Locality** are the two patterns of data access that caches are designed to exploit. Temporal locality means that recently accessed data is likely to be accessed again soon—caches naturally capture this by keeping recently used items. Spatial locality means that items near recently accessed data are likely to be accessed soon—caches typically store not just the requested data but surrounding data in fixed-size blocks called cache lines or pages, anticipating nearby accesses.

**Cache Eviction Policies** determine which items are removed from the cache when it becomes full and new data needs to be stored. Common policies include Least Recently Used (LRU), which evicts the item accessed longest ago; First In, First Out (FIFO), which evicts the oldest item; Least Frequently Used (LFU), which evicts the item with fewest accesses; and Random, which evicts a random item. LRU is widely used because it approximates optimal replacement for many access patterns, though it requires more metadata overhead than simpler policies.

**Write Policies** determine how updates to cached data are handled. Write-through caching writes data to both cache and backend storage simultaneously, ensuring consistency but offering no write performance benefit. Write-back (or write-behind) caching writes to cache only initially, deferring writes to backend storage until the cached item is evicted. Write-around caching bypasses the cache on writes, writing directly to backend storage and invalidating any cached copy. The choice of write policy involves tradeoffs between consistency, performance, and implementation complexity.

## How It Works

At the hardware level, CPU caches work by monitoring memory accesses and maintaining copies of recently accessed memory locations. When the CPU requests data from memory, the cache hardware checks whether the address is currently stored in the cache (a hit) or needs to be fetched from main memory (a miss). On a miss, the cache fetches a block of memory containing the requested address (exploiting spatial locality) and delivers the requested data to the CPU while simultaneously storing the block in the cache.

Cache mapping determines how memory addresses are assigned to cache locations. Direct-mapped caches assign each memory address to exactly one cache location (simple but potentially causes conflicts). Fully associative caches allow any memory address to be stored in any cache location (maximum flexibility but expensive to implement). Set-associative caches compromise by grouping cache locations into sets, with each memory address mapped to a specific set but able to occupy any location within that set.

Software caching layers implement similar logic but with additional considerations around expiration, consistency, and distributed operation. Application code typically checks the cache first before querying the database or computing a result. On a cache miss, the application fetches the data, stores it in the cache with an appropriate TTL (time to live), and returns it to the caller. Cache-aside patterns require explicit invalidation when source data changes, while read-through patterns handle caching transparently to the calling code.

Distributed caches like Redis or Memcached add network latency to the caching equation but enable sharing cached data across multiple application instances. These systems typically run as separate processes (often on dedicated servers) and communicate via network protocols. Partitioning and replication strategies determine how cached data is distributed across cluster nodes, affecting both performance and availability.

## Practical Applications

Web caching is ubiquitous in modern internet infrastructure. Browser caches store static assets (images, CSS, JavaScript) locally, reducing page load times and server load. Proxy servers cache responses for multiple users, further amplifying the performance benefits. CDNs cache content at edge locations worldwide, bringing cached data physically closer to end users. HTTP caching headers (Cache-Control, ETag, Last-Modified) provide mechanisms for controlling how and when content is cached.

Database caching dramatically improves query performance. Query result caches store the results of expensive queries, avoiding repeated computation. Buffer pools cache database pages in memory, reducing disk I/O. Connection pools cache database connections to avoid the overhead of establishing new connections. These caching layers are often automatically managed by the database engine, though application-level caching of denormalized views or computed aggregates is also common.

API and application-level caching reduces load on backend services. Expensive computations can be cached with appropriate invalidation. External API responses can be cached to reduce rate limiting concerns and improve response times. Session data cached in memory stores enables stateless application architectures. The choice of cache backend (in-process memory, distributed cache, database) depends on factors like data size, consistency requirements, and whether cache needs to be shared across instances.

## Examples

```python
# Example: Simple in-memory cache with TTL in Python
import time
from functools import wraps

def cache_with_ttl(ttl_seconds):
    def decorator(func):
        cache = {}
        def wrapper(*args):
            now = time.time()
            if args in cache:
                value, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return value
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

@cache_with_ttl(ttl_seconds=300)
def expensive_computation(n):
    # Simulate expensive operation
    return sum(i * i for i in range(n))
```

```bash
# Example: Redis cache commands
GET user:1234:profile           # Retrieve cached user profile
SET user:1234:profile '{"name":"Alice","email":"alice@example.com"}' EX 3600
                              # Cache with 1-hour TTL
DEL user:1234:profile           # Explicit cache invalidation
FLUSHDB                        # Clear entire database (use with care!)
```

These examples demonstrate caching at different levels—application code using decorators for function result caching and Redis providing distributed caching with automatic expiration. Both illustrate the core cache patterns: checking for cached data, computing and storing on miss, and invalidating when necessary.

## Related Concepts

- [[Caching]] - The broader discipline of storing data for faster access
- [[Memory Hierarchy]] - The organization of computer memory from fast/small to slow/large
- [[Redis]] - Popular in-memory data store commonly used for caching
- [[CDN]] - Content Delivery Network, distributed caching for web content
- [[Memcached]] - Distributed memory caching system
- [[Cache Invalidation]] - Strategies for keeping caches consistent with source data
- [[Self-Healing Wiki]] - The system that auto-created this page

## Further Reading

- "Computer Systems: A Programmer's Perspective" by Bryant and O'Hallaron - Memory hierarchy and caching in depth
- "Designing Data-Intensive Applications" by Martin Kleppmann - Caching patterns in distributed systems
- RFC 9111 - HTTP Caching specification
- Redis documentation on caching patterns and eviction policies

## Personal Notes

Caching is one of the most impactful optimization techniques available, but it's also easy to get wrong. The hardest part is usually not implementing the cache itself but designing appropriate invalidation strategies. Stale data can cause subtle bugs that are difficult to reproduce and diagnose. My rule of thumb: cache data where the cost of serving stale information is acceptable, and always ensure you have a clear path to invalidation when the underlying data changes.

Another common pitfall is premature optimization—adding caching before understanding actual performance bottlenecks. Caching adds complexity and can introduce failure modes (cache service unavailable). Measure first, identify the actual bottlenecks, and then consider whether caching addresses those bottlenecks cost-effectively.
