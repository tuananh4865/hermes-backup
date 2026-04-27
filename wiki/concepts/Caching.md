---
title: Caching
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [caching, performance, architecture]
---

# Caching

## Overview

Caching is a performance optimization technique that stores copies of frequently accessed data in a temporary storage layer for faster retrieval on subsequent requests. The fundamental principle behind caching is the exploitation of locality of reference: programs tend to access the same data or instructions repeatedly, and by keeping these items close to where they are needed, systems can dramatically reduce access latency and computational overhead.

In modern software architecture, caching appears at nearly every layer of the technology stack. From CPU registers and memory buffers in hardware, to content delivery networks distributing media globally, to in-memory data stores accelerating database queries, caching is an essential mechanism for building responsive and scalable systems. The technique trades off a modest amount of storage space for significant improvements in read performance, reduced database load, and better overall system throughput.

Effective caching requires careful consideration of data freshness, storage capacity, eviction policies, and cache invalidation strategies. When implemented well, caches can improve response times by orders of magnitude. When implemented poorly, they can introduce stale data problems, consistency issues, and unexpected behavior that is difficult to debug.

## Strategies

Cache systems employ various strategies to manage what data is stored and when it should be removed or refreshed. The choice of strategy depends on the access patterns of the application, the volatility of the data, and the tolerance for staleness.

**Least Recently Used (LRU)** is one of the most common cache eviction policies. LRU discards the least recently accessed items first when the cache reaches its capacity limit. This strategy assumes that items accessed recently are more likely to be accessed again in the near future, which holds true for many real-world workloads such as browsing history, social media feeds, and shopping carts. LRU is simple to implement and performs well in practice, though more sophisticated variants like LRU-K or Two Queues can offer better behavior for certain access patterns.

**Time-To-Live (TTL)** defines an explicit expiration time for each cached item. TTL-based expiration is straightforward to implement and provides strong guarantees about maximum data staleness. It is particularly useful for data that naturally changes over time, such as user session tokens, API responses from third-party services, weather forecasts, or stock prices. TTL requires minimal bookkeeping—just a timestamp check on retrieval—making it both simple and efficient. Many caching systems allow different TTL values for different types of data, enabling fine-grained control over freshness versus performance.

Other notable strategies include **Least Frequently Used (LFU)**, which evicts items accessed the least often over the lifetime of the cache, and **First In First Out (FIFO)**, which follows a simple queue order. Advanced implementations may combine multiple factors or use adaptive algorithms that adjust based on observed access patterns.

## Use Cases

Caching is applied across virtually every domain of computing, from mobile applications to global internet infrastructure.

**Content Delivery Networks (CDN)** use caching to store static assets like images, videos, stylesheets, and JavaScript files at edge locations geographically distributed around the world. By serving content from a location physically close to the end user, CDNs dramatically reduce network latency and bandwidth costs. When a user in Berlin requests an image that was cached from an origin server in California, the CDN delivers it from a nearby point of presence rather than traversing the entire internet. Major CDN providers like Cloudflare, Akamai, and Fastly operate thousands of edge nodes to optimize content delivery at scale. For more on this pattern, see [[CDN]].

**Database caching** reduces the load on primary databases by storing query results or frequently accessed rows in a fast in-memory store like [[Redis]] or [[Memcached]]. Applications that perform repetitive read queries—dashboards, reporting systems, product catalogs—benefit significantly from database caching. Rather than executing a complex JOIN operation against a disk-backed database on every request, the system can return a pre-computed result from memory in milliseconds. Cache-aside and read-through are common patterns where the application first checks the cache and falls back to the database when needed.

**API caching** applies similar principles to external service calls. When an application depends on third-party APIs—whether for payment processing, mapping services, or machine learning inference—the cost and latency of each network request can become a bottleneck. Caching API responses allows the system to serve repeated requests from local storage, reducing costs, improving reliability, and enabling offline operation for certain use cases. HTTP caching headers like Cache-Control and ETag provide standardized mechanisms for controlling how responses are cached by clients and intermediate proxies.

Session storage is another prominent use case, where [[Redis]] or similar in-memory stores hold user session data to enable stateless application servers that can scale horizontally without sharing local memory. For more on the architectural patterns involved, see [[API-Gateway]].

## Related

- [[CDN]] - Content Delivery Networks and edge caching
- [[Redis]] - In-memory data store commonly used for caching
- [[Memcached]] - Distributed memory caching system
- [[API-Gateway]] - Entry point that often incorporates caching logic
- [[Database]] - Where cached data often originates
- [[Load Balancing]] - Works alongside caching to distribute traffic efficiently
- [[Rate Limiting]] - Often combined with caching to manage API usage
- [[KV-Cache]] - Specific caching technique used in LLM inference
