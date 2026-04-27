---
title: Timeouts
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [timeouts, reliability, fault-tolerance, networking, distributed-systems]
---

# Timeouts

## Overview

Timeouts are predefined time limits that specify how long a system will wait for a response, operation, or condition before terminating the attempt and treating it as a failure. In distributed systems, timeouts are one of the most fundamental and widely applicable reliability patterns, serving as the first line of defense against hanging operations, network partitions, and unresponsive services. Without timeouts, a single slow or failing component could cause threads, connections, and entire processes to wait indefinitely, eventually exhausting system resources.

The concept applies across all layers of the stack: network timeouts at the TCP level, application timeouts for API calls, database query timeouts, and business process timeouts for long-running workflows. Setting appropriate timeouts is both an art and a science—too short and legitimate operations fail prematurely; too long and failures take too long to detect, delaying recovery.

## Key Concepts

**Timeout Types**: Timeouts come in several forms depending on what they're protecting:
- **Connect Timeout**: Maximum time to establish a network connection before giving up
- **Read/Receive Timeout**: Maximum time to wait for data after a connection is established
- **Write/Send Timeout**: Maximum time to wait for a write operation to complete
- **Request Timeout**: End-to-end time limit for a complete request-response cycle
- **Idle Timeout**: Time to wait for activity before closing an idle connection
- **Business Process Timeout**: Time limits on business workflows independent of technical operations

**Timeout Units**: In most systems, timeouts are measured in milliseconds or seconds. HTTP clients commonly default to connect timeouts of a few seconds and read timeouts of 10-30 seconds, but these should be tuned to your specific use case and expected response times.

**Timeout Cascading**: In microservices architectures, timeouts compound. If Service A calls B, which calls C, and each has a 1-second timeout, the end-to-end timeout for A's request to C could be several seconds. Proper timeout configuration requires understanding the full call chain.

## How It Works

Timeout implementation typically involves setting a deadline and checking whether it has passed:

```python
import signal
import functools

class TimeoutError(Exception):
    pass

def timeout(seconds, error_message="Operation timed out"):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError(error_message)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator

@timeout(5)
def fetch_data_from_api():
    # This will TimeoutError if it takes more than 5 seconds
    return api_client.get()
```

In production systems, most HTTP libraries and frameworks handle timeouts internally:

```python
import requests

response = requests.get(
    "https://api.example.com/data",
    timeout=(3.05, 10)  # (connect_timeout, read_timeout)
)
```

## Practical Applications

**API Calls**: External API integrations should always have timeouts. Without them, network issues or provider problems can cause your application to hang indefinitely.

**Database Queries**: Long-running queries can tie up connection pools. Setting query timeouts prevents runaway queries from affecting overall system availability.

**Background Jobs**: Job processing systems should timeout stuck workers to prevent zombie processes and reclaim resources.

**Health Checks**: Timeout too short and healthy services appear unhealthy; too long and unhealthy services delay failure detection.

**User Experience**: Perceived performance depends partly on timeout handling. Showing users immediate feedback (spinner, progress indicator) while operations are in-flight, and clear messages when timeouts occur, is better than unexplained waiting.

## Examples

Configuring timeouts in a Python HTTP client:

```python
import httpx

client = httpx.Client(
    timeout=httpx.Timeout(
        connect=5.0,      # 5 seconds to establish connection
        read=10.0,        # 10 seconds to receive response
        write=5.0,        # 5 seconds to send request
        pool=30.0         # 30 seconds to get connection from pool
    )
)

# Per-request timeout override
response = client.get("https://api.example.com/data", timeout=20.0)
```

Using timeouts with asyncio for concurrent operations:

```python
import asyncio

async def fetch_with_timeout(url, timeout_seconds=5):
    async with asyncio.timeout(timeout_seconds):
        async with httpx.AsyncClient() as client:
            return await client.get(url)
```

## Related Concepts

- [[Circuit Breaker]] - Timeouts often trigger circuit breaker trips
- [[Retry Pattern]] - Retries typically use timeouts to detect failures
- [[Backpressure]] - Timeout-induced failures can signal backpressure upstream
- [[Graceful Degradation]] - Timeout handling often returns degraded responses
- [[Bulkhead Pattern]] - Isolated pools often have their own timeout configurations

## Further Reading

- "Release It!" by Michael Nygard - foundational text on timeout configuration
- HTTPX documentation on timeouts
- "Timeouts and Failure Handling" - Google SRE best practices
- Akka Timeout patterns for actor systems

## Personal Notes

Start with conservative timeouts and adjust based on observed performance. Log timeout occurrences as warnings—they often indicate early signs of system degradation. Consider percentile-based timeout configuration where different percentiles get different timeouts (p50, p95, p99). Circuit breakers should have shorter timeouts than the underlying operation's typical duration.
