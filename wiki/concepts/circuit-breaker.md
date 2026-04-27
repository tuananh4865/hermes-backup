---
title: Circuit Breaker
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [circuit-breaker, architecture, reliability, fault-tolerance, microservices]
---

# Circuit Breaker

## Overview

The Circuit Breaker pattern is a fault-tolerance design pattern that prevents cascading failures in distributed systems by detecting failures and encapsulating logic to prevent a failure from constantly recurring during maintenance, temporary external system failure, or unexpected system difficulties. Named after the electrical device that protects circuits from damage caused by overload or short circuits, the software pattern monitors for failures and "trips" to stop further requests from being sent to a failing service, giving that service time to recover.

In modern microservices architectures, where applications depend on multiple remote services, a single failing service can cause resource exhaustion, timeouts, and cascading failures across the entire system. The Circuit Breaker acts as a proxy that monitors for failures and trips when a failure threshold is reached. Once tripped, subsequent calls to the circuit breaker return with an error or cached response without invoking the actual service.

## Key Concepts

The Circuit Breaker pattern operates through three distinct states that govern how it behaves:

**Closed State**: In normal operation, the circuit breaker is closed and all requests pass through to the downstream service. The breaker monitors request outcomes and counts failures. When the number of failures exceeds a predefined threshold within a specified time window, the breaker transitions to the open state.

**Open State**: When the circuit is open, requests are blocked immediately and fail fast without attempting to contact the downstream service. This gives the failing service time to recover. After a configured timeout period elapses, the circuit transitions to a half-open state.

**Half-Open State**: In this transitional state, the circuit allows a limited number of test requests to pass through to the downstream service. If these requests succeed, the circuit transitions back to closed state, indicating recovery. If any request fails, the circuit returns to the open state and the timeout period restarts.

## How It Works

The implementation of a Circuit Breaker involves tracking failures across a sliding time window. When failures exceed a threshold percentage, the breaker trips. Different libraries and frameworks implement variations of this behavior with configurable parameters:

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout_duration=60, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.timeout_duration = timeout_duration
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time >= self.timeout_duration:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenException("Circuit is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
```

The key parameters include `failure_threshold` (number of failures before tripping), `timeout_duration` (how long the circuit stays open before transitioning to half-open), and `success_threshold` (number of successes needed in half-open state to close the circuit).

## Practical Applications

Circuit Breakers are essential in scenarios involving:

**Microservices Communication**: When Service A calls Service B, and Service B becomes unavailable, a Circuit Breaker prevents Service A from waiting for timeouts on every request, freeing up thread pools and preventing resource exhaustion.

**External API Integration**: Third-party APIs may experience downtime or slow responses. Circuit Breakers provide graceful degradation by returning cached data or fallback values when the external service is unavailable.

**Database Connections**: Database overload or connectivity issues can cascade through an application. Circuit Breakers help isolate database failures and prevent application-wide outages.

## Examples

Consider an e-commerce application where the `PaymentService` becomes slow or unavailable:

```python
payment_circuit = CircuitBreaker(
    failure_threshold=3,
    timeout_duration=30
)

def checkout(cart_id, payment_info):
    try:
        return payment_circuit.call(process_payment, cart_id, payment_info)
    except CircuitOpenException:
        return {"status": "pending", "message": "Payment service temporarily unavailable"}
    except PaymentFailedException:
        return {"status": "failed", "message": "Payment declined"}
```

When the payment service fails 3 times, subsequent checkout attempts immediately return a pending status rather than waiting for timeouts, improving user experience while the payment service recovers.

## Related Concepts

- [[Retry Pattern]] - Often used alongside Circuit Breaker to attempt failed requests after recovery
- [[Bulkhead Pattern]] - Isolation pattern that limits the impact of failures to one component
- [[Graceful Degradation]] - Designing systems to maintain partial functionality during failures
- [[Backpressure]] - Flow control mechanism related to handling system overload
- [[Timeouts]] - A simpler form of failure handling that can complement Circuit Breakers
- [[Rate Limiting]] - Prevents overload through request throttling

## Further Reading

- Martin Fowler's "Circuit Breaker" article and patterns of enterprise application architecture
- Microsoft Azure Architecture Center's Cloud Design Patterns - Circuit Breaker pattern
- "Release It!" by Michael Nygard - foundational text on building resilient systems

## Personal Notes

Circuit Breakers are most effective when combined with monitoring and alerting. The transitions between states should be logged and alerts should fire when circuits trip, as this indicates downstream service issues that may require attention. Consider implementing fallback logic that returns cached data or degraded responses when the circuit is open.
