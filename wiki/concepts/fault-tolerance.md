---
title: Fault Tolerance
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [fault-tolerance, reliability, distributed-systems, resilience, availability]
---

# Fault Tolerance

## Overview

Fault tolerance is the ability of a system to continue operating correctly even when one or more of its components fail. Unlike fault avoidance (building components that fail rarely), fault tolerance embraces the reality that failures are inevitable in complex systems and designs for graceful degradation rather than total collapse. A fault-tolerant system doesn't pretend failures won't happen — it detects failures, isolates them, and continues providing service at a reduced capacity or quality rather than experiencing complete outages.

Fault tolerance is a cornerstone of [[reliability engineering]] and is particularly critical in distributed systems, where failures of network links, individual nodes, or services are expected rather than exceptional. The concept is formalized through the CAP theorem — in the presence of network partitions, a system must choose between consistency and availability. Most fault-tolerant designs choose availability with eventual consistency, accepting that reads may be slightly stale during partition events.

## Key Concepts

**Redundancy:** The primary technique for fault tolerance. Adding backup components (active or passive) so that if one fails, others take over. Types include:
- **Active redundancy:** All components process requests simultaneously; on failure, others already have state
- **Passive redundancy:** Standby components remain idle until needed; faster failover but may require state synchronization
- **Hot standby:** Near-instant failover with synchronized state
- **Warm standby:** Partial state sync; some recovery time needed
- **Cold standby:** Offline; longest recovery time but cheapest

**Failure Detection:** Systems must detect failures quickly and accurately. This includes health check endpoints, heartbeat protocols, and distributed consensus mechanisms. The challenge is distinguishing between a slow component and a failed one — timeouts must be carefully tuned.

**Graceful Degradation:** When full capacity can't be maintained, the system degrades purposefully. A video streaming service might reduce quality; an e-commerce site might disable recommendations but maintain checkout. The key is that core functionality remains intact.

**Failover:** Automatically redirecting traffic or requests from a failed component to a healthy one. Requires careful handling of session state — many failover systems require external session stores (Redis, database) to maintain session continuity across nodes.

**Bulkheads:** Named after watertight compartments in ship hulls, bulkheads isolate failures so that one failing component doesn't cascade and bring down the entire system. In practice, this means separate thread pools, connection pools, or service instances for different concerns.

## How It Works

Fault tolerance is implemented through patterns at every layer of the stack:

1. **Hardware level:** RAID drives, dual power supplies, ECC memory, clustered servers
2. **Application level:** The [[Circuit Breaker]] pattern prevents cascading failures by failing fast when a downstream service is unhealthy
3. **Network level:** Multiple network paths, anycast DNS, BGP failover
4. **Data level:** Database replication (synchronous and asynchronous), multi-region deployment

A well-known fault tolerance design pattern is the "two hardware server" approach where one active server handles all traffic and a second identical server mirrors state. On active server failure, the standby takes over within seconds — used by banks and trading systems where even seconds of downtime are costly.

```python
# Simple circuit breaker concept in Python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None

    def call(self, func):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenException("Circuit is OPEN")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
```

## Practical Applications

- **Financial trading systems:** Sub-second failover is required; hot standby clusters with synchronized state
- **Telecom switching systems:** Designed to tolerate component failures without call drops; N+1 redundancy throughout
- **Cloud provider regions:** Multi-region deployments allow traffic to shift away from a failing region
- **Air traffic control systems:** Extreme fault tolerance requirements; triple modular redundancy where three independent systems vote on outputs
- **Content delivery networks:** [[CDN]]s route around failed origin servers by serving cached content

## Examples

- **Netflix's Chaos Monkey:** Intentionally kills servers in production to verify fault tolerance mechanisms work
- **Amazon DynamoDB:** Multi-AZ replication with eventual consistency; remains available during AZ failures
- **Kubernetes:** Has built-in replica sets, health checks, and automated restart of failed pods
- **Erlang/OTP:** Language designed with built-in fault tolerance constructs — processes are isolated and can be restarted independently

## Related Concepts

- [[Circuit Breaker]] — Pattern that prevents cascading failures
- [[Redundancy]] — Duplicating components for fault tolerance
- [[Microservices]] — Architecture that requires explicit fault tolerance design
- [[Service Level Agreement]] (SLA) — Availability guarantees that drive fault tolerance investment
- [[Reliability Engineering]] — The discipline of building reliable systems
- [[Self-Healing Systems]] — Automated recovery from failures
- [[Resilience Patterns]] — Collection of patterns including retry, timeout, bulkhead, and circuit breaker

## Further Reading

- "Designing Data-Intensive Applications" by Martin Kleppmann — covers fault tolerance and distributed systems concepts in depth
- AWS Well-Architected Framework — Reliability Pillar: https://aws.amazon.com/architecture/well-architected/
- "Release It!" by Michael Nygard — practical guide to building resilient systems

## Personal Notes

Fault tolerance is often misunderstood as "making everything redundant." The real skill is deciding what to make fault-tolerant (based on cost, probability of failure, and impact) and designing the right degradation strategy for when things do fail. I've seen teams over-invest in redundant infrastructure for low-impact systems while neglecting core services. Start with failure mode analysis — what actually breaks and what's the business impact — before designing the tolerance mechanisms.
