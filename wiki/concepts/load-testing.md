---
title: Load Testing
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [performance-testing, scalability, reliability, devops, api-testing, sre]
---

# Load Testing

## Overview

Load testing is a type of performance testing that evaluates how a system behaves under expected production-like conditions — specifically, the volume and concurrency of user requests, transactions, or operations that the system is anticipated to handle. The goal is to identify performance bottlenecks, validate that the system meets its Service Level Objectives (SLOs), and ensure that the architecture scales gracefully before deploying to production.

Unlike [[unit-testing]] which validates individual components in isolation, or [[integration-testing]] which validates interactions between components, load testing validates the entire integrated system under stress. It reveals emergent behaviors that only appear under load — database connection pool exhaustion, thread pool saturation, lock contention, memory leaks that manifest only under sustained traffic, and cascading failures that begin when one component slows down under pressure.

Load testing is a critical practice in [[site-reliability-engineering]] and [[devops]] pipelines. It transforms assumptions about system capacity into empirical evidence and provides the data needed to make informed capacity planning decisions. Organizations that skip load testing often discover scaling problems only after they cause production incidents — an expensive and embarrassing way to learn.

## Key Concepts

### Simulated Load Patterns

Load tests simulate different usage patterns, each revealing different aspects of system behavior:

**Constant Load**: A steady number of concurrent users or requests per second maintained over a duration. This tests system stability over time and can reveal memory leaks, connection leaks, or gradual performance degradation that constant load would surface.

**Ramp-Up Load**: Users or requests gradually increase over time, starting from zero and building to a peak. This simulates a traffic surge (viral content, marketing campaign, flash sale) and tests the system's ability to handle rapid scaling, including auto-scaling decisions and the behavior of systems with no auto-scaling.

**Spike Load**: An abrupt, dramatic increase in load followed by a return to normal levels. This tests the system's elasticity and how it behaves when pushed well beyond its designed capacity. Spike tests often reveal queuing behavior, timeout configurations, and graceful degradation mechanisms.

**Soak (Endurance) Testing**: Sustained load at or near production capacity over an extended period (hours to days). This reveals long-running issues that shorter tests cannot — gradual heap growth, log file accumulation, disk space consumption, database table bloat, and slow leaks that only manifest over time.

**Variance Testing**: Load with variable request rates and mixes, simulating the irregular traffic patterns of real production systems. This tests how systems adapt to changing conditions and whether performance is consistent across different traffic profiles.

### Key Metrics

Load tests measure several critical metrics:

- **Throughput**: Requests or transactions processed per second (RPS, TPS)
- **Latency**: Time to process a request, typically measured as percentiles (p50, p95, p99, p999)
- **Error Rate**: Percentage of requests that fail (5xx errors, timeouts, exceptions)
- **CPU and Memory Utilization**: Resource consumption of application and database servers
- **Database Metrics**: Query latency, connection pool utilization, lock wait times
- **Network Metrics**: Bandwidth consumption, packet loss, retransmission rates

The relationship between these metrics under increasing load is what reveals bottlenecks. A well-performing system shows throughput increasing linearly with load until it saturates some resource, after which throughput plateaus or drops while latency increases. A poorly performing system may show throughput declining while error rates spike.

### Service Level Objectives (SLOs) and Error Budgets

Load testing validates that the system meets its defined SLOs under expected (and sometimes unexpected) load. Common SLO targets include:

- p99 latency < 500ms for API requests
- Error rate < 0.1% for all requests
- Throughput > 10,000 RPS sustained

An **error budget** is the acceptable amount of unreliability — if your SLO is 99.9% uptime, your error budget is 0.1%. Load testing that consumes a significant portion of the error budget under normal load suggests the system has no headroom for handling traffic spikes or degradation.

### Baselines and Regression Detection

Regular load testing establishes performance baselines. When the baseline changes — same load produces higher latency or lower throughput — it signals a regression. Performance regressions can result from code changes (a new algorithm, an unoptimized query), infrastructure changes (slower storage, fewer compute resources), or configuration changes. CI/CD pipelines increasingly incorporate load testing as a quality gate precisely to catch performance regressions before deployment.

## How It Works

A load testing workflow typically follows these steps:

**1. Define Test Scenarios**: Identify what to test (API endpoints, user flows, background jobs), the expected mix of operations, and the target load profile (concurrent users, requests per second, duration).

**2. Script and Configure**: Write test scripts (often in YAML or code) that define the request sequences, payload sizes, think times between requests, and authentication. Tools like JMeter, k6, Gatling, or Locust provide scripting frameworks for this.

**3. Set Up Monitoring**: Instrument the system under test and the test tool itself with metrics collection. Distributed tracing (like [[opentelemetry]] or Jaeger) is particularly valuable for understanding where latency is introduced in complex microservice architectures.

**4. Execute Tests**: Run the tests, starting with lower load and gradually increasing. Always include a warm-up period where the system initializes caches, JIT compiles code, and establishes database connection pools before measurement begins.

**5. Analyze Results**: Compare measured metrics against SLOs and baselines. Identify the saturation point (when adding more load stops improving throughput). Identify the component that bottlenecked first (often visible in resource utilization metrics reaching 100%).

**6. Optimize and Re-test**: Address identified bottlenecks (scale horizontally, optimize queries, add caching) and re-test to validate improvements.

## Practical Applications

### API and Microservice Testing

Modern architectures with many microservices require load testing at the API gateway level to understand end-to-end behavior. k6 is particularly popular for API load testing due to its scripting simplicity and excellent integration with observability platforms.

```javascript
// k6 load test example
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const latencyTrend = new Trend('latency');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 for 5 minutes
    { duration: '2m', target: 200 },   // Ramp to 200 users
    { duration: '5m', target: 200 },   // Stay at 200
    { duration: '5m', target: 0 },     // Ramp down
  ],
  thresholds: {
    'latency': ['p(95)<500'],           // p95 latency must be < 500ms
    'errors': ['rate<0.01'],            // Error rate < 1%
    'http_req_duration': ['p(99)<1000'], // p99 < 1 second
  },
};

export default function () {
  const res = http.get('https://api.example.com/users/' + Math.random().int(1, 10000));
  
  latencyTrend.add(res.timings.duration);
  errorRate.add(res.status >= 500);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has body': (r) => r.body.length > 0,
  });
  
  sleep(Math.random() * 3 + 1);  // Random think time 1-4 seconds
}
```

### Database Performance Testing

Databases require specialized load testing to reveal query performance issues, index effectiveness, connection pool sizing, and replication lag under write load. Tools like pgbench (PostgreSQL), mysqlslap, or SQL Query Generator can simulate concurrent transactions and measure query latency distribution.

### Chaos Engineering Integration

Load testing and [[chaos-engineering]] are complementary. Load testing reveals how the system behaves at the edges of its capacity; chaos testing reveals how it behaves when components fail. Combining both practices gives a comprehensive picture of resilience. Running load tests during chaos experiments (injecting latency, killing nodes, saturating resources) reveals whether the system's graceful degradation mechanisms work under realistic traffic conditions.

## Examples

A realistic end-to-end e-commerce load test might include:

- Browse product catalog: 70% of simulated users
- Add item to cart: 15% of users
- Checkout: 10% of users
- Search: 5% of users

Each scenario has different resource implications. Search might stress the database's full-text search capabilities; checkout involves payment processing (an external service with its own latency and rate limits). The test reveals not just total capacity but which specific operations become bottlenecks.

Real-world load tests often reveal surprising results. A payment service might fail not because of its own capacity but because a downstream fraud detection service adds 200ms of latency per transaction, causing connection pool exhaustion in the payment service under load. This cascading effect is invisible without full system load testing.

## Related Concepts

- [[performance-testing]] — Broader category including load, stress, spike, and soak testing
- [[site-reliability-engineering]] — Domain where load testing is essential
- [[scalability]] — What load testing validates
- [[chaos-engineering]] — Complementary practice for resilience testing
- [[integration-testing]] — Testing component interactions
- [[opentelemetry]] — Observability instrumentation for load test analysis
- [[api-testing]] — API-level load testing
- [[devops]] — DevOps pipeline integration for load testing

## Further Reading

- "Performance Testing" by Kevin Failor — Practical guide to load testing methodology
- k6 Documentation — Modern, developer-friendly load testing tool
- "Site Reliability Engineering" (Google) — Load testing in the SRE context
- Apache JMeter Documentation — Enterprise-grade load testing tool
- "The Art of Capacity Planning" — Translating load test results into capacity decisions

## Personal Notes

The most valuable load tests I've run were not the ones that confirmed the system could handle expected load — they were the ones that revealed unexpected behavior at the edges. Discovering that your database connection pool size is too small only when you hit 80% of expected peak load is much better than discovering it causes an outage at peak. I always recommend starting load tests earlier than you think necessary in the development cycle — performance problems are exponentially harder to fix as you approach production deployment. Also, don't just test at expected peak load: test at 1.5x and 2x to understand your system's graceful degradation behavior. The goal is not just to confirm everything works at normal load, but to understand how the system fails when pushed beyond its limits.
