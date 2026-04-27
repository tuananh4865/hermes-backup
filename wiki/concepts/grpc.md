---
title: "gRPC"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [grpc, rpc, api, google]
---

# gRPC

## Overview

gRPC is an open-source remote procedure call (RPC) framework developed by Google that enables client and server applications to communicate transparently across different environments. Originally developed in 2015 and later donated to the Cloud Native Computing Foundation (CNCF), gRPC has become a foundational technology for building high-performance distributed systems, [[microservices]] architectures, and API-based communication between services.

Unlike traditional REST-based APIs that use JSON or XML as data formats, gRPC uses HTTP/2 as its transport protocol and Protocol Buffers (Protobuf) as its interface definition language and underlying message serialization format. This combination delivers significant performance improvements, with gRPC being capable of handling hundreds of thousands of requests per second on commodity hardware, often outperforming REST by 5 to 10 times in latency and throughput benchmarks.

gRPC follows a contract-first approach where the service interface is defined explicitly in a `.proto` file before any implementation code is written. This design provides strong typing, language agnosticism, and automatic generation of client and server code in any of the 50+ supported programming languages. The framework handles connection management, load balancing, health checking, and authentication automatically, allowing developers to focus on business logic rather than infrastructure concerns.

gRPC supports four communication patterns: unary calls (single request, single response), server-side streaming, client-side streaming, and bidirectional streaming. This flexibility makes it suitable for a wide range of applications from traditional request-response services to real-time data pipelines.

## Protocol Buffers

[[protocol-buffers]] (Protobuf) are Google's language-neutral, platform-neutral mechanism for serializing structured data. Interface definitions are written in `.proto` files using a domain-specific language that defines messages (similar to structs or data classes) and service methods. The Protobuf compiler (`protoc`) then generates strongly-typed code for both the server and client in the target language.

Protobuf messages are binary-encoded, making them significantly smaller and faster to parse than JSON or XML equivalents. A message defined in protobuf might look like this: the developer defines the structure once in a `.proto` file, and then generates native code for their programming language of choice. This eliminates the need for manual serialization logic and ensures both client and server use identical data structures.

The Protocol Buffers schema also serves as documentation and a contract between services. Because the schema is explicit and versioned, incompatible changes can be caught at compile time rather than runtime. Proto3, the latest version of the language, adds support for more languages and simplified syntax while retaining backwards compatibility with proto2.

## vs REST

gRPC and REST represent two different paradigms for building APIs, each with distinct advantages and trade-offs.

**Performance** is where gRPC typically excels. Binary protobuf serialization produces messages that are 3 to 10 times smaller than equivalent JSON payloads, and parsing binary data is significantly faster than parsing JSON strings. Combined with HTTP/2's multiplexing capabilities, gRPC can handle many concurrent requests over a single TCP connection, reducing connection overhead dramatically.

**Type Safety** differs substantially between the two approaches. gRPC uses `.proto` files to define services and messages with explicit types, catching mismatches at compile time across all languages. REST with JSON lacks this enforcement; clients and servers must manually agree on field names and types, often leading to runtime errors when schemas diverge.

**Browser Support** remains a limitation for gRPC. While gRPC-Web provides partial browser support, REST's universal HTTP/1.1 compatibility means any client with an HTTP stack can consume REST APIs without special libraries. This makes REST the standard choice for public-facing APIs.

**Streaming Capabilities** also differ significantly. gRPC natively supports server-side, client-side, and bidirectional streaming as first-class features. REST requires workarounds like Server-Sent Events, WebSockets, or polling mechanisms to achieve similar functionality.

**Human Readability** is an advantage for REST APIs using JSON. During development and debugging, developers can read and modify request payloads directly. gRPC's binary format requires tooling to inspect, which can complicate debugging but also provides a minor security benefit through obscurity.

For internal service-to-service communication in [[microservices]] architectures, gRPC is often the preferred choice due to its performance and type safety. For external-facing APIs consumed by diverse clients, REST remains the dominant convention.

## Related

- [[microservices]] - Architecture pattern where gRPC is commonly used for service communication
- [[api]] - Application programming interfaces; gRPC provides a high-performance alternative to REST APIs
- [[rpc]] - Remote procedure call; gRPC is a modern implementation of the RPC concept
- [[protocol-buffers]] - Google's data serialization format that powers gRPC's performance
- [[http2]] - The transport protocol that enables gRPC's multiplexing and streaming capabilities
- [[service-mesh]] - Infrastructure layer where gRPC is frequently used for inter-service communication
