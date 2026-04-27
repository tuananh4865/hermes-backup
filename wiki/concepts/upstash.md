---
title: Upstash
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [upstash, redis, serverless, database]
---

## Overview

Upstash is a serverless data platform that provides [[Redis]] and [[Kafka]] as cloud-native, pay-per-request services. Unlike traditional database hosting, Upstash is designed specifically for serverless and edge computing environments where cold starts, connection limits, and billing based on execution time are common constraints. The platform abstracts away infrastructure management so developers can focus on building applications without worrying about scaling or server maintenance.

Upstash differentiates itself by offering a serverless-first approach with per-request pricing rather than per-hour or per-node billing. This makes it particularly attractive for workloads with variable traffic patterns, such as [[serverless functions]], [[edge computing]] applications, and [[microservices]] architectures. The platform maintains compatibility with standard database protocols, allowing existing Redis and Kafka clients to connect with minimal code changes.

## Products

### Upstash Redis

Upstash Redis is the flagship product, offering a fully managed [[Redis]] database with serverless pricing. It supports both [[REST API]] and the native Redis protocol, enabling use cases ranging from caching and session storage to real-time leaderboards and rate limiting. The service provides multi-region replication, TLS encryption, and built-in durability options. Developers can choose between a Global database for low-latency access worldwide or a Regional database for single-region deployments.

### Upstash Kafka

Upstash Kafka is a serverless Apache Kafka service designed for event streaming and messaging workloads. It eliminates the operational complexity of managing Kafka clusters while maintaining compatibility with the Kafka ecosystem. The service offers automatic scaling, managed schema registry, and pay-per-message pricing. This makes it practical for use cases like building event-driven architectures, processing clickstream data, and implementing reliable message queues.

### QStash

QStash is Upstash's messaging and workflow orchestration product. It provides HTTP-based message delivery with automatic retries, dead-letter queues, and built-in deduplication. QStash integrates seamlessly with serverless platforms like [[Vercel]], [[Cloudflare Workers]], and AWS Lambda. It supports scheduling, fan-out patterns, and pub/sub messaging, making it a lightweight alternative to traditional message brokers for serverless environments.

## Use Cases

Upstash is commonly used for caching in [[serverless functions]] where database connections are short-lived. Session storage, rate limiting, and temporary data persistence are popular patterns with the Redis product. For event-driven systems, Upstash Kafka enables building pipelines that ingest and process streams without managing infrastructure. QStash excels at background job processing and cross-service communication in serverless architectures.

The platform is particularly well-suited for [[AI agent]] workflows where memory stores, task queues, and real-time data caching are needed. Developers building applications on [[edge computing]] platforms benefit from Upstash's global distribution and low-latency access patterns.

## Related

- [[Redis]] - The in-memory data store underlying Upstash Redis
- [[Kafka]] - Event streaming platform for Upstash Kafka
- [[Serverless Functions]] - Compute model optimized for Upstash
- [[Edge Computing]] - Deployment context where Upstash excels
- [[Microservices]] - Architecture pattern using Upstash products
- [[Database]] - General category of data storage solutions
