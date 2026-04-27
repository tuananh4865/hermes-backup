---
title: "Queueing Theory"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [queueing-theory, operations-research, performance-engineering, probability, computer-science]
---

# Queueing Theory

## Overview

Queueing theory is the mathematical study of waiting lines or queues, analyzing the behavior of systems where entities (customers, tasks, data packets) arrive at a service facility, wait for service, and then leave after being served. Originally developed by Agner Krarup Erlang in the early 1900s to model telephone call centers for the Copenhagen Telephone Company, queueing theory has since become a foundational discipline in operations research, computer science, telecommunications, traffic engineering, and any field where resource allocation under demand uncertainty is a concern.

The power of queueing theory lies in its ability to predict system performance metrics — average wait time, probability of waiting, server utilization, expected queue length — using mathematical models that require only a few parameters about arrival patterns and service times. These predictions enable engineers to design systems with appropriate capacity, set service level agreements (SLAs), and make informed trade-offs between cost (more servers) and customer satisfaction (shorter waits).

At its core, queueing theory formalizes an intuition everyone has: if arrivals are fast and service is slow, queues grow. But the quantitative relationships between arrival rates, service rates, number of servers, and queue disciplines reveal surprising results, such as the fact that a system with 90% utilization will have dramatically longer waits than one with 80% utilization — and the relationship is nonlinear.

## Key Concepts

**Arrival process** describes how entities join the queue. The most common model is a Poisson process, where arrivals occur randomly at a constant average rate λ (lambda). This memoryless property means the time since the last arrival tells you nothing about when the next arrival will occur.

**Service process** describes how entities are served. The service time distribution is often exponential, though other distributions (deterministic, normal, heavy-tailed) may be appropriate depending on the context.

**Queueing discipline** (or service discipline) determines the order in which entities are served. Common disciplines include:
- **FIFO (First-In-First-Out)**: Standard queue, first arrival served first
- **LIFO (Last-In-First-Out)**: Stack behavior, last arrival served first (useful in some computing contexts)
- **Priority queues**: Entities with higher priority are served before lower priority
- **Processor Sharing**: All entities receive equal service share (modeling time-sharing computers)

**Number of servers** (c) determines how many entities can be served simultaneously. Single-server queues (c=1) are the simplest; multi-server queues (c≥2) appear in banks, call centers, and web server pools.

**System capacity** (K) and **population size** (N) are bounds on the system. A finite-queue system may reject arrivals when the queue is full; an infinite-queue system never rejects arrivals but queues may grow without bound.

**Kendall's notation** standardizes queueing model descriptions: A/B/c/K/N/D where A is arrival distribution, B is service distribution, c is servers, K is system capacity, N is population, D is discipline. Shorthand omits trailing elements when they are infinite/default.

## How It Works

The most important formula in queueing theory is **Little's Law**, which relates average number of entities in the system (L), average arrival rate (λ), and average time in the system (W):

```
L = λ × W
```

This deceptively simple relationship holds regardless of the arrival or service distributions, as long as the system is stable (arrival rate < service capacity).

The **M/M/1 queue** (Poisson arrivals, exponential service, single server) is the canonical queueing model. Key results include:

```python
import math

def mm1_queue_metrics(arrival_rate, service_rate):
    """
    Calculate performance metrics for M/M/1 queue.
    
    Parameters:
    - arrival_rate (λ): Average arrivals per time unit
    - service_rate (μ): Average services per time unit
    
    Returns dictionary of performance metrics.
    """
    rho = arrival_rate / service_rate  # Utilization (must be < 1 for stability)
    
    if rho >= 1:
        return {"error": "System is unstable - utilization >= 1"}
    
    # Average number in system (including one being served)
    L = rho / (1 - rho)
    
    # Average time in system (including service)
    W = 1 / (service_rate - arrival_rate)
    
    # Average number waiting (not being served)
    Lq = rho ** 2 / (1 - rho)
    
    # Average waiting time (excluding service)
    Wq = rho / (service_rate - arrival_rate)
    
    # Probability queue is empty (no waiting)
    P0 = 1 - rho
    
    # Probability of waiting (finding system busy)
    Pw = rho
    
    return {
        "utilization": rho,
        "avg_in_system": L,
        "avg_time_in_system": W,
        "avg_in_queue": Lq,
        "avg_waiting_time": Wq,
        "prob_empty": P0,
        "prob_waiting": Pw
    }

# Example: web server handling requests
# Arrivals: 90 requests/second, Service: 100 requests/second
metrics = mm1_queue_metrics(arrival_rate=90, service_rate=100)
print(f"Utilization: {metrics['utilization']:.2%}")
print(f"Avg wait time: {metrics['avg_waiting_time']*1000:.2f} ms")
print(f"Avg time in system: {metrics['avg_time_in_system']*1000:.2f} ms")
```

**Utilization and delay relationship** is exponential. Going from 80% to 90% utilization roughly doubles the average wait time. Going from 90% to 95% roughly doubles it again. This nonlinearity means systems operated near 100% utilization are catastrophically sensitive to arrival spikes.

## Practical Applications

Queueing theory informs design and operation in numerous domains:

- **Call centers**: Sizing agent pools to meet service level targets (e.g., "80% of calls answered in 20 seconds")
- **Web infrastructure**: Configuring thread pools, connection pools, and auto-scaling triggers
- **Manufacturing**: Production line design, inventory management
- **Transportation**: Traffic signal timing, airport security lane staffing
- **Healthcare**: ER staffing models, operating room scheduling

## Examples

Consider a web API with the following characteristics:
- Average request rate: 500 requests/second
- Average service time per request: 2ms (service rate = 500 requests/second per worker)
- Need to decide: how many workers (servers)?

At 1 worker: utilization = 500/500 = 100% — unstable, infinite queue growth
At 2 workers: utilization = 500/1000 = 50% — comfortable, low latency
At 3 workers: utilization = 500/1500 = 33% — over-provisioned, unnecessary cost

Queueing models predict the latency at each configuration, allowing informed capacity decisions.

## Related Concepts

- [[Little's Law]] — Fundamental relationship L = λW in queueing systems
- [[Poisson Process]] — Common model for random arrivals
- [[ Markov Chains]] — Foundation for analyzing queueing behavior
- [[Performance Engineering]] — Applying queueing theory to computer systems
- [[Load Balancing]] — Distributing arrivals across multiple servers
- [[Capacity Planning]] — Using queueing models to provision resources

## Further Reading

- "Introduction to Operations Research" by Hillier and Lieberman — Comprehensive queueing theory coverage
- "Probability and Computing" — Randomized algorithms and probability relevant to queueing
- "The Uniformly Most Powerful Test" and related statistical works on queueing inference

## Personal Notes

Queueing theory is one of those areas where the math can get intimidating, but the key insights are accessible. The exponential relationship between utilization and wait time is the most important thing to internalize: running a system at high utilization saves resources but creates brittleness. A 95% utilized system will have dramatically worse tail latency than an 85% utilized one, and production incidents often trace back to this exact trade-off being miscalculated. The other key insight is Little's Law: you can always trade between time, throughput, and work-in-progress inventory.
