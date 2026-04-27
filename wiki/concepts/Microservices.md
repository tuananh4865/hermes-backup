---
title: Microservices
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [microservices, architecture, distributed-systems, cloud-native]
---

# Microservices

## Overview

Microservices is an architectural style that structures an application as a collection of small, autonomous, and independently deployable services. Rather than building a monolithic application where all components are tightly coupled within a single codebase and deployment unit, microservices architecture decomposes functionality into discrete services that communicate via well-defined APIs, typically over HTTP with JSON or through asynchronous messaging systems like [[Kafka]] or [[RabbitMQ]].

Each microservice owns its dedicated data store and encapsulates a specific business capability, allowing teams to develop, test, deploy, and scale services independently. This architectural approach emerged as a response to the limitations of monolithic architectures, particularly in large-scale, fast-paced development environments where teams need the flexibility to iterate quickly without affecting the entire system.

The philosophy behind microservices centers on the concept of modularity at the architecture level. Services can be written in different programming languages, use different database technologies, and be maintained by different teams. The only interface that matters is the contract defined by the API, enabling true technology heterogeneity and organizational autonomy.

## vs Monolith

The traditional monolithic architecture serves as the primary alternative to microservices. In a monolith, all components reside within a single codebase, share the same database, and deploy as one unit. While monoliths offer simplicity in development and deployment, they present significant limitations at scale.

**Coupling** is the fundamental issue. In a monolith, changes to one component often require rebuilding and redeploying the entire application. A bug in the payment processing code could potentially affect the user interface, and a surge in traffic on one feature forces scaling of the entire system. This tight coupling slows down development teams, creates deployment risk, and makes it difficult to adopt new technologies incrementally.

**Deployment risk** increases with monolith size. When everything deploys together, any change carries the risk of breaking the whole system. Teams become cautious about releasing updates, leading to longer release cycles and accumulated technical debt. Microservices mitigate this by limiting the blast radius of any single deployment to only the service being changed.

**Scalability** differs dramatically between the two approaches. A monolith scales by duplicating the entire application, even if only one component is under load. Microservices allow targeted scaling of specific services based on their actual resource needs, improving efficiency and reducing infrastructure costs.

**Team organization** also influences the architectural choice. Microservices align well with Conway's Law, which suggests that system design mirrors organizational communication structures. Small, cross-functional teams can own entire services from conception through production, fostering accountability. Monoliths tend to create siloed teams organized around technical layers rather than business capabilities.

That said, monoliths remain valid for smaller applications, startups moving fast, and teams without the operational maturity to manage distributed systems complexity. The operational overhead of microservices, including service discovery, distributed tracing, and robust CI/CD pipelines, is substantial and not always justified for simpler use cases.

## Patterns

Several established patterns help practitioners implement microservices architecture effectively.

**API Gateway** serves as the single entry point for client requests, handling cross-cutting concerns like authentication, rate limiting, and request routing. The gateway aggregates responses from multiple backend services when needed and shields clients from the complexity of the internal service topology.

**Service Discovery** enables services to locate each other without hardcoded network addresses. Service registries maintain a dynamic catalog of available instances, and clients query this registry to find healthy endpoints. This pattern supports elastic scaling and self-healing infrastructure.

**Circuit Breaker** prevents cascading failures by stopping requests to a failing service. When a service's error rate exceeds a threshold, the circuit breaker "opens" and returns a fallback response or error immediately, giving the failing service time to recover while protecting overall system availability.

**Saga Pattern** manages distributed transactions across multiple services without traditional ACID transactions. Sagas coordinate a series of local transactions, each triggering the next step, with compensating transactions to handle rollbacks when failures occur. This is essential for maintaining data consistency in scenarios where operations span multiple services.

**Event Sourcing** and **CQRS** (Command Query Responsibility Segregation) are complementary patterns that separate read and write operations. Event sourcing stores state changes as a sequence of events, while CQRS splits the data model into separate representations for reading and writing, both particularly valuable in distributed systems where data ownership is fragmented.

## Related

- [[Kubernetes]] - Container orchestration platform commonly used to deploy and manage microservices at scale
- [[Kafka]] - Distributed event streaming platform for asynchronous communication between services
- [[RabbitMQ]] - Message broker implementing various messaging patterns for service communication
- [[Serverless-Functions]] - Related architectural approach where functions serve as independently deployable units
- [[Web API]] - The contract layer through which microservices typically communicate
- [[Authentication]] - Cross-cutting concern often implemented at the API gateway layer in microservices architectures
- [[Distributed Systems]] - The broader field of computer science that microservices architecture belongs to
- [[Multi-Agent Systems]] - Related concept where multiple autonomous entities coordinate to achieve goals
