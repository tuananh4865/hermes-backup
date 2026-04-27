---
title: Rate Limiting
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rate-limiting, api, security, performance, throttling]
---

# Rate Limiting

## Overview

Rate Limiting is a technique used to control the rate of requests that clients can make to a service, API, or system resource. It protects infrastructure from abuse, ensures fair resource allocation among users, and prevents system overload during traffic spikes or malicious attacks such as denial-of-service (DoS). By enforcing quotas on request frequency, organizations can maintain stable performance and availability for legitimate users while mitigating the impact of excessive or malicious traffic.

Rate limiters typically operate at the entry point of a service, evaluating each incoming request against a set of predefined rules. When a client exceeds the allowed request threshold, the server responds with an HTTP 429 (Too Many Requests) status code, often accompanied by headers such as `Retry-After` or `X-RateLimit-Remaining` to inform the client when they can resume sending requests.

## Key Concepts

**Rate Limiting Algorithms**: Several algorithms exist for implementing rate limiting, each with distinct characteristics:

**Token Bucket**: Tokens are added to a bucket at a fixed rate. Each request consumes a token. The bucket has a maximum capacity. If no tokens are available, requests are rejected. This algorithm allows burst traffic up to the bucket capacity while enforcing an average rate over time.

**Sliding Window**: Requests are tracked within a rolling time window. The algorithm counts how many requests have occurred in the current window and rejects requests that exceed the limit. This approach provides smoother rate enforcement compared to fixed windows and reduces sudden spikes at window boundaries.

**Leaky Bucket**: Requests enter a queue (the bucket) and are processed at a constant rate. Excess requests are dropped if the queue is full. This algorithm produces a steady, uniform output rate regardless of input bursts, making it suitable for traffic shaping and smoothing.

**Fixed Window**: Requests are counted in fixed time intervals (e.g., every minute). When a window resets, the counter resets to zero. This is simple to implement but can have boundary issues where double the requests pass through at window edges.

## How It Works

Rate limiting can be implemented at multiple layers of the stack. Application-level rate limiting embeds logic directly within the API code, offering flexibility but higher overhead. Middleware and reverse proxy solutions (such as API gateways) handle rate limiting centrally before requests reach application servers, reducing complexity and enabling consistent policy enforcement across services.

```python
import time
from collections import defaultdict
from threading import Lock

class TokenBucketRateLimiter:
    def __init__(self, rate=10, capacity=10):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = Lock()
    
    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
    
    def retry_after(self):
        with self.lock:
            return max(0, (1 - self.tokens) / self.rate)
```

Distributed rate limiting extends these concepts across multiple server nodes using shared state stores like Redis. This ensures rate limits remain consistent regardless of which server handles a request.

## Practical Applications

**API Protection**: Public and private APIs use rate limiting to prevent abuse, ensure fair usage among clients, and protect backend services from overload. API rate limits are often tiered (different limits for different subscription levels).

**DoS/DDoS Mitigation**: Rate limiting is a front-line defense against denial-of-service attacks. By limiting request rates from individual IPs or accounts, services can survive traffic spikes that would otherwise cause outages.

**Cost Control**: In cloud environments where infrastructure costs scale with usage, rate limiting prevents unexpected cost overruns from runaway clients or accidental infinite loops.

**Regulatory Compliance**: Some regulations require data processing systems to limit request rates to ensure fair access to public services.

## Examples

Configuring rate limiting in a Flask application:

```python
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# Simple in-memory rate limiter
request_counts = defaultdict(list)

def rate_limit(max_requests=100, window_seconds=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            client_ip = request.remote_addr
            
            # Clean old entries and count recent requests
            request_counts[client_ip] = [
                t for t in request_counts[client_ip]
                if now - t < window_seconds
            ]
            
            if len(request_counts[client_ip]) >= max_requests:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": window_seconds
                }), 429
            
            request_counts[client_ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route("/api/data")
@rate_limit(max_requests=100, window_seconds=60)
def get_data():
    return jsonify({"data": "value"})
```

## Related Concepts

- [[Circuit Breaker]] - Prevents cascade failures; often used alongside rate limiting
- [[Backpressure]] - Flow control that signals when clients should slow down
- [[Throttling]] - Related technique for limiting resource usage
- [[Graceful Degradation]] - System can reduce functionality instead of hard limiting
- [[Timeouts]] - Prevents indefinite waiting; complements rate limiting
- [[Load Balancing]] - Distributes load across instances; rate limiters often sit in front

## Further Reading

- IETF RateLimit Header scheme for HTTP APIs
- Cloudflare's rate limiting best practices
- "Rate Limiting" by Martin Fowler
- Stripe's API rate limit design and Retry-After header implementation

## Personal Notes

Rate limiting is most effective when combined with clear client feedback. Always include rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset) so clients can adjust their behavior proactively. Consider implementing progressive rate limiting that starts with warnings before hard limits. For distributed systems, use Redis or similar for centralized rate limit counters to ensure consistency across instances.
