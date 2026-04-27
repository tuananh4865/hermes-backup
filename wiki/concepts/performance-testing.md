---
title: Performance Testing
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [performance, testing, quality-assurance, observability, reliability]
---

## Overview

Performance testing is a category of software testing that evaluates how a system behaves under expected and stress conditions. Unlike functional testing, which verifies that software produces correct outputs, performance testing measures characteristics like response time, throughput, resource consumption, and stability over time. The goal is to identify bottlenecks, validate service level objectives (SLOs), and ensure the system can handle its intended production load before it ships.

Performance testing is not a single activity but a family of distinct test types, each answering different questions. Running a "performance test" without specifying which type is like saying a car is being "driven" — it could mean highway cruising, a race track, or a crash test. The right test type depends on what you want to learn about the system's behavior.

## Key Concepts

**Load Testing** evaluates system behavior under anticipated normal load. The goal is to verify that response times, error rates, and resource utilization stay within acceptable bounds when the system processes the expected volume of concurrent users or transactions. Load tests are typically modeled after production traffic patterns using historical data or synthetic profiles. A load test might simulate 500 concurrent users making requests to an API and verify that the 95th-percentile latency stays under 200ms.

**Stress Testing** pushes the system beyond its normal operating capacity to identify its breaking point. How does the system behave at 2x or 10x the expected load? Does it fail gracefully, or does it cascade into a catastrophic outage? Stress tests reveal whether the system degrades predictably (returning errors under load) or unpredictably (deadlocks, memory exhaustion, full crashes).

**Spike Testing** tests the system's reaction to sudden, dramatic increases in load — like what happens when a flash sale starts or a viral post drives sudden traffic. The system may handle steady-state load well but fail when load jumps unexpectedly. Spike tests help validate auto-scaling configurations and queue handling.

**Soak Testing** (endurance testing) runs the system at a moderate load for an extended period — hours or even days. The goal is to uncover memory leaks, log rotation failures, database connection pool exhaustion, and other degradation that only manifests over time. A soak test might run for 24 hours and track whether response times drift upward as memory slowly accumulates garbage.

**Key Performance Indicators (KPIs)** include latency (response time), throughput (requests per second or transactions per second), error rate (percentage of requests that fail), CPU utilization, memory usage, disk I/O, and network bandwidth. [[Service level objectives]] (SLOs) define the targets for these KPIs; performance tests validate whether those targets are met.

## How It Works

Performance tests are typically executed using specialized load generation tools that simulate many concurrent users or clients. Tools like k6, Apache JMeter, Gatling, Locust, and wrk can generate HTTP traffic, maintain sessions, vary request distributions, and report aggregate statistics.

```javascript
// k6 script example — simple load test
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95th percentile under 500ms
    http_req_failed: ['rate<0.01'],    // Error rate under 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

Results are analyzed to identify bottlenecks. If a 95th-percentile latency spikes while CPU is still low, the bottleneck is likely in a dependent service or a thread pool. If CPU maxes out at 60% of expected load, the application code or algorithm may be inefficient. [[Observability]] tooling — distributed tracing, metrics, and log analysis — is critical for correlating load test results with internal system behavior.

## Practical Applications

Performance testing is mandatory before any significant product launch or infrastructure change. A mobile app update that slows the checkout flow by 200ms can measurably impact conversion rates. A database migration that doubles query time under load can degrade an entire API tier. Running performance tests in CI/CD pipelines catches regressions before they reach production.

For [[microservices]]-based systems, performance testing must account for inter-service communication. Load testing a single service in isolation does not reveal bottlenecks in the service mesh, shared database, or message queue. End-to-end performance tests that exercise entire workflows are necessary for validating [[service-level-objectives]] at the system level.

## Examples

A real-world example: a video streaming platform runs a soak test before a major content release. They simulate 50,000 concurrent viewers for 12 hours. Midway through, they notice memory usage climbing steadily — a classic sign of a memory leak in the viewer authentication module. The leak is caught and fixed before the release, preventing a potential outage that would have affected millions of simultaneous viewers during peak viewing.

## Related Concepts

- [[service-level-objectives]] — The targets that performance testing validates
- [[observability]] — Required for interpreting performance test results
- [[load-testing]] — Subtype focused on expected load conditions
- [[stress-testing]] — Subtype focused on extreme conditions
- [[benchmarking]] — Systematic comparison of performance across implementations

## Further Reading

- "Performance Testing Guidance for Web Applications" — Microsoft patterns & practices
- k6 documentation and best practices guides
- Google SRE workbook sections on latency and throughput
- "Thinking, Fast and Slow" — interesting parallel on human performance under load

## Personal Notes

The most valuable performance test is the one that most closely models your actual production traffic. Generic load tests that uniformly hit every endpoint miss the real-world reality of hot paths, cold paths, and skewed access distributions. Investing in realistic traffic simulation pays dividends far beyond the effort of writing the test script. Also: always run performance tests in an environment as close to production as possible — testing on undersized hardware gives misleading results.
