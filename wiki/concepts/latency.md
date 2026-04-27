---
title: "Latency"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [performance, networking, systems, latency]
---

# Latency

## Overview

Latency is the time delay between a cause and its effect in a computing system. In networking contexts, it measures the time data takes to travel from source to destination. In system performance, it measures the time between requesting an operation and receiving its result. Latency is a critical metric in distributed systems, web applications, gaming, financial trading, and any system where timely response matters.

Low latency is often described as "latency matters" or "latency is the new currency" in modern computing, where microseconds can translate to millions in revenue for high-frequency trading systems or user satisfaction metrics for consumer applications.

## Key Concepts

**Latency vs Throughput**: While latency measures the time for a single operation, throughput measures how many operations can be completed per unit time. High throughput doesn't guarantee low latency—a system can process many requests slowly.

**End-to-End Latency**: The total latency from the original requester to the final responder and back. This accumulates delays from network hops, processing time, queuing, and transmission.

**Latency Percentiles**: Because latency distributions are often skewed, looking at averages alone is misleading. Common percentiles include p50 (median), p95, p99, and p999. A service might have 10ms average latency but 500ms p99 latency due to occasional slowdowns.

**Propagation Delay**: The time it takes for a signal to travel through the physical medium. Cabled fiber travels at roughly 200,000 km/s, setting physical limits on how fast data can move across distances.

**Transmission Delay**: The time required to push all packets onto the link, determined by packet size divided by bandwidth.

**Processing Delay**: Time spent in routers and switches examining headers, performing lookups, and making forwarding decisions.

## How It Works

Latency accumulates through several components in a typical request path:

1. **DNS Resolution**: Converting a hostname to an IP address typically adds 5-100ms
2. **TCP Connection Setup**: A new TCP connection requires a 3-way handshake (SYN, SYN-ACK, ACK), adding 1-100ms depending on distance
3. **TLS Handshake**: Secure connections add another 1-2 round trips for cryptographic key exchange
4. **Request Transmission**: Time to send the request data onto the network
5. **Server Processing**: Time for the server to receive, parse, process, and generate a response
6. **Response Transmission**: Time for the response to travel back to the client
7. **Client Processing**: Time for the client to receive and render the response

Each hop through network equipment adds small processing delays, and queuing at congested links can introduce variable delays.

## Practical Applications

**Content Delivery Networks (CDNs)**: By caching content at edge locations geographically close to users, CDNs dramatically reduce latency for static assets.

**Database Optimization**: Techniques like read replicas, connection pooling, and query optimization reduce database-related latency.

**Async Processing**: Moving slow operations to background workers prevents blocking and improves apparent responsiveness.

**Connection Keep-Alive**: Reusing TCP connections avoids repeated handshake overhead.

**Precomputing and Caching**: Computing results in advance and storing them for quick retrieval eliminates latency for repeated requests.

## Examples

```bash
# Measure network latency with ping
ping -c 5 google.com

# Output:
# PING google.com (142.250.80.46): 56 data bytes
# 64 bytes from 142.250.80.46: icmp_seq=0 ttl=117 time=14.2 ms
# 64 bytes from 142.250.80.46: icmp_seq=1 ttl=117 time=14.1 ms
# round-trip min/avg/max = 14.1/14.2/14.4 ms
```

```python
# Python example: measuring latency with time.perf_counter()
import time

start = time.perf_counter()
result = some_expensive_operation()
end = time.perf_counter()

latency_ms = (end - start) * 1000
print(f"Operation took {latency_ms:.2f}ms")
```

## Related Concepts

- [[Throughput]] - Operations per unit time, related to capacity
- [[Bandwidth]] - The data transfer capacity of a network connection
- [[Jitter]] - Variation in latency over time
- [[Distributed Systems]] - Systems where latency between nodes is a key design factor
- [[Caching]] - A strategy to reduce latency by storing computed results
- [[Load Balancing]] - Distributing requests to manage latency across servers

## Further Reading

- "Systems Performance: Enterprise and the Cloud" by Brendan Gregg
- "Designing Data-Intensive Applications" by Martin Kleppmann
- Google's "SRE Chapter on Latency"

## Personal Notes

Latency is one of the most user-visible performance characteristics. When building systems, I always measure p99 and p999 latency, not just averages. The "tail latency" problem—what happens at high percentiles—often determines whether your SLA is achievable in production.
