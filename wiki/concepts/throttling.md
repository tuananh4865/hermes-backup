---
title: Throttling
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rate-limiting, performance, api, resource-management, infrastructure]
---

# Throttling

## Overview

Throttling is a technique used to limit the rate at which operations can be performed or resources can be consumed within a system. It serves as a form of flow control that prevents any single client, service, or process from overwhelming shared infrastructure, ensuring fair resource allocation and maintaining system stability under load. Throttling is distinct from queuing (which buffers requests) and blocking (which stops requests entirely)—throttling regulates the pace at which requests are processed, typically by enforcing maximum throughput limits per unit of time.

In modern distributed systems, throttling is a critical mechanism for maintaining quality of service across multiple competing consumers of shared resources. Without throttling, a single misbehaving client could consume all available memory, CPU cycles, network bandwidth, or API quota, causing degradation or failures for all other users. Throttling provides a more graceful degradation path by ensuring that all clients receive at least some level of service.

## Key Concepts

**Rate Limiting** is the most common form of throttling, expressed as a maximum number of operations allowed within a specific time window. For example, an API might permit 100 requests per minute per API key, or a database connection pool might limit concurrent queries to 50. Rate limits are typically implemented using token bucket or sliding window algorithms that track request counts over time and enforce boundaries dynamically.

**Burst Limits** control the maximum rate at which requests can be made in short, intense bursts, separate from sustained rate limits. A system might allow 1000 requests per minute overall but no more than 100 requests in any single second. Burst limits prevent sudden traffic spikes from causing immediate overload while still permitting legitimate bursty traffic patterns.

**Resource Quotas** throttle based on total resource consumption rather than request rates. Cloud platforms commonly enforce quotas on CPU hours, storage bytes, network bandwidth, or API calls per billing period. Quotas differ from rate limits in that they represent cumulative allocations rather than instantaneous limits, often resetting on a daily, weekly, or monthly cycle.

**Priority-based Throttling** assigns different tiers of service quality to different classes of users or requests. Paid customers might receive higher throttling thresholds than free tier users, or critical infrastructure requests might bypass throttling entirely while best-effort requests are heavily constrained. This approach allows systems to maintain fairness while also supporting business models based on tiered service levels.

## How It Works

Throttling implementations typically work by tracking usage counters associated with each client identity (API key, user ID, IP address, etc.) and comparing current usage against configured limits. When a request arrives, the throttling middleware checks whether allowing the request would exceed the limit. If within limits, the request proceeds and the counter increments. If the limit would be exceeded, the request is either rejected immediately with an error response or queued until the limit window resets.

```
Token Bucket Algorithm Example:

bucket_capacity = 100 tokens
refill_rate = 10 tokens per second

request arrives:
  if tokens_available >= 1:
    consume 1 token
    allow request
  else:
    reject request (HTTP 429 Too Many Requests)
```

Different algorithms suit different use cases. Token bucket allows bursty traffic up to a maximum while maintaining long-term average rates. Leaky bucket smooths traffic into a constant outflow rate regardless of input patterns. Sliding window provides more even limit enforcement compared to fixed windows that can allow double the rate at window boundaries.

## Practical Applications

**API Rate Limiting** protects web APIs from abuse and enables fair pricing tiers. When clients exceed their rate limits, APIs typically return HTTP 429 responses with Retry-After headers indicating when they can resume. This client-server negotiation allows graceful degradation rather than hard failures.

**Database Connection Pooling** uses throttling to prevent too many concurrent queries from overwhelming database resources. Applications request connections from a pool, and when all connections are in use, additional requests either wait (if queuing is enabled) or fail immediately with a timeout error.

**Cloud Resource Governance** enforces quotas on infrastructure consumption, preventing runaway processes from accumulating unlimited resources and protecting against billing surprises. Organizations set budgets and limits on compute, storage, and network resources per project or team.

**Network Bandwidth Management** throttles traffic to enforce quality of service guarantees. ISPs may throttle heavy users during peak hours, or enterprises may limit bandwidth for certain applications (like video streaming) to prioritize business-critical traffic.

## Examples

```python
# Simple token bucket rate limiter implementation
import time

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, 
                          self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

# Usage
limiter = TokenBucket(capacity=100, refill_rate=10)  # 100 burst, 10/sec

if limiter.consume():
    process_request()
else:
    return HTTP_429("Rate limit exceeded. Retry after 1 second.")
```

## Related Concepts

- [[rate-limiting]] — Broader patterns for controlling request rates
- [[load-balancing]] — Distributing traffic across multiple resources
- [[backpressure]] — Upstream signals to slow down request flow
- [[circuit-breaker]] — Pattern for failing fast when downstream services are unhealthy
- [[api-gateway]] — Central point for enforcing throttling policies

## Further Reading

- "Rate Limiting: How to Design Stable APIs" | API Design Guide (API Evangelist)
- "Token Bucket Algorithm" | Computer Networks Textbook
- Cloudflare Rate Limiting Documentation

## Personal Notes

Throttling is one of those infrastructure concerns that feels abstract until it bites you. A single client inadvertently launching thousands of requests per second can cascade into outages affecting hundreds of other users. The discipline is in setting appropriate limits—too strict and you frustrate legitimate users; too permissive and you leave systems vulnerable. Effective throttling also requires good observability: you need to know when limits are being hit, which clients are responsible, and whether limits need adjustment as traffic patterns evolve.
