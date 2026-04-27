---
title: Retry Pattern
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [retry-pattern, reliability, fault-tolerance, resilience, microservices]
---

# Retry Pattern

## Overview

The Retry Pattern is a resilience strategy in which a failed operation is automatically re-attempted based on a defined policy. Rather than immediately propagating an error to the caller after a single failure, the retry mechanism attempts the operation multiple times, typically with increasing delays between attempts. This approach is fundamental to building robust distributed systems where transient failures—such as network timeouts, temporary service unavailability, or resource contention—are common and often resolve themselves within seconds.

In cloud-native and microservices environments, virtually every operation that involves network communication or external service calls can fail intermittently. Network packets get lost, services restart, and load balancers may temporarily route requests to an unhealthy instance. The Retry Pattern addresses these transient failures by giving the system a chance to self-heal without human intervention. When combined with other patterns like Circuit Breaker and Timeout, retry logic forms a critical layer of defense against the inherent unreliability of distributed computing.

## Key Concepts

**Transient Failures**: The Retry Pattern is most effective against failures that are temporary or short-lived. These include network latency spikes that cause timeouts, temporary service restarts, brief database connection pool exhaustion, and lock contention scenarios. Retrying against persistent failures (such as authentication errors, invalid input, or permanent service shutdown) wastes resources and can amplify load on already-struggling systems.

**Retry Policies**: A retry policy defines how retries should be conducted. Key parameters include:
- **Max Retries**: The maximum number of retry attempts before giving up
- **Backoff Strategy**: The delay between retry attempts (fixed, linear, exponential)
- **Jitter**: Randomization added to backoff to prevent thundering herd problems
- **Retryable Errors**: Which error types or status codes should trigger retries

**Idempotency**: Safe retry operations require that the operation be idempotent—calling it multiple times produces the same result as calling it once. This is critical for operations that modify state, such as payment processing or database writes. Implementing idempotency keys allows safe retries without duplicate side effects.

## How It Works

When an operation fails, the retry logic evaluates whether the failure is retryable and whether the maximum retry count has been exceeded. If both conditions are favorable, the retry policy calculates the delay before the next attempt and schedules the retry. Popular backoff strategies include:

```python
import random
import time

def exponential_backoff(attempt, base_delay=1, max_delay=60, jitter=True):
    """Calculate delay using exponential backoff with optional jitter."""
    delay = min(base_delay * (2 ** attempt), max_delay)
    if jitter:
        delay = delay * (0.5 + random.random() * 0.5)
    return delay

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry a function with exponential backoff."""
    for attempt in range(max_retries + 1):
        try:
            return func()
        except RetryableError as e:
            if attempt == max_retries:
                raise
            delay = exponential_backoff(attempt, base_delay)
            time.sleep(delay)
```

The jitter component is crucial in production systems because without it, large numbers of clients retry simultaneously (the thundering herd problem), which can overwhelm a recovering service.

## Practical Applications

**Database Operations**: Database connections can momentarily fail due to temporary lock contention or brief overload. Retry logic with short delays allows transactions to complete once the database recovers.

**API Calls**: External APIs may return 503 Service Unavailable or 429 Rate Limited responses that resolve within seconds. Smart retry clients check for specific status codes and respect Retry-After headers.

**Message Queue Publishing**: When publishing messages to a queue fails, retries ensure delivery without losing the message. Combined with publisher confirms, this provides at-least-once delivery guarantees.

**File Operations**: Cloud storage services may occasionally return throttling errors. Retries with exponential backoff allow operations to complete when the service recovers.

## Examples

A typical HTTP client with retry logic:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

response = session.get("https://api.example.com/data")
```

This configuration retries 3 times on server error status codes, with delays of 1, 2, and 4 seconds between attempts.

## Related Concepts

- [[Circuit Breaker]] - Prevents retry storms by failing fast when a service is down
- [[Timeouts]] - Prevents indefinite waiting; combines with retries for better UX
- [[Bulkhead Pattern]] - Isolates failures; retries work best when failures are isolated
- [[Graceful Degradation]] - Provides fallback responses when retries exhaust
- [[Rate Limiting]] - Retry policies should respect rate limits and back off
- [[Backpressure]] - Signals when retry rates should be reduced

## Further Reading

- Microsoft Azure Architecture Center - Retry Pattern
- "Building Microservices" by Sam Newman - chapter on resilience
- Polly library for .NET - comprehensive retry and fault handling policies
- Resilience4j - Java library with rich retry and circuit breaker implementations

## Personal Notes

When implementing retries, always ensure the underlying operation is idempotent or implement idempotency keys. Be careful with retry storms during major outages—they can amplify load on recovering services. Consider retry budgets (limiting total retries across a time window) to prevent unbounded retry accumulation. Monitoring retry rates is essential; high retry rates often indicate deeper issues that need investigation.
