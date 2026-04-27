---
title: Contract Testing
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [contract-testing, testing, microservices, api]
---

## Overview

Contract testing is an approach to verifying that the interfaces between services communicate correctly according to a shared agreement. In modern distributed systems, where microservices interact through APIs, ensuring that each service honors its end of the bargain is critical for system reliability. Rather than deploying all services together and testing the entire system end-to-end, contract testing allows teams to validate individual services in isolation by checking that they meet the expectations defined in a contract.

A contract represents the agreement between a consumer service and a provider service. The consumer describes what data it expects from the provider—such as request formats, response structures, status codes, and error handling—while the provider specifies how it will respond under various conditions. Contract tests then verify that both sides adhere to these specifications. This approach catches mismatches early, before services are deployed, and prevents the scenario where a change in one service silently breaks another.

Contract testing becomes especially valuable in teams practicing continuous delivery or operating with independent service ownership. When multiple teams develop services in parallel, integration problems often surface only during expensive end-to-end testing or, worse, in production. Contract testing provides a lightweight mechanism to validate compatibility continuously, reducing integration friction and increasing confidence in deployments.

There are two primary perspectives in contract testing. Consumer-driven contract testing places the responsibility of defining the contract on the consuming service, as that service knows best what it needs from its providers. Provider-driven contract testing has the provider define and publish its interface, with consumers validating against it. Both approaches aim to achieve the same goal—ensuring alignment between services—but differ in who authors and owns the contract specification.

## Pact

[[Pact]] is the most widely adopted framework for consumer-driven contract testing. Originally developed at Real Estate Australia (REA) Group and now part of the Pactflow ecosystem, it provides tooling for writing tests that capture the expectations of a consumer service and verify them against the actual behavior of the provider service.

The Pact workflow begins with the consumer. Developers write a test that defines the expected interactions with a provider—such as a GET request to retrieve user data and the expected response structure. Pact records these expectations as a "contract" file, which is then shared with the provider. The provider runs the contract against its actual implementation to verify it can satisfy the consumer's requirements. If the provider changes its API in a way that breaks the contract, the test fails, alerting the team to a potential breaking change.

Pact supports multiple programming languages including Java, JavaScript, Python, Ruby, .NET, and Go, making it accessible across diverse technology stacks. It also integrates with CI/CD pipelines, enabling automated contract validation on every build. Pact Broker, a companion tool, allows teams to publish and share contracts, track version compatibility, and visualize the relationships between services.

One of Pact's key strengths is its focus on consumer-driven contracts. By putting the consumer in control of defining what it needs, Pact ensures that provider APIs evolve to serve actual consumer requirements rather than speculation. This reduces the risk of over-engineering APIs and aligns development with genuine business needs.

## Related

- [[API Testing]] - Broader discipline of testing application programming interfaces for correctness and reliability
- [[Microservices]] - Architectural style where contract testing plays a critical role in maintaining service independence
- [[Integration Testing]] - Testing that contract testing partially replaces in distributed system contexts
- [[Service Level Agreements]] - Formal agreements related to contract expectations in production environments
- [[End-to-End Testing]] - Comprehensive testing approach that contract testing complements but does not replace
