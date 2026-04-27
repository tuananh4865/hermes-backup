---
title: RPC (Remote Procedure Call)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rpc, distributed-systems, api, protocol-buffers, grpc, thrift]
---

# RPC (Remote Procedure Call)

## Overview

Remote Procedure Call (RPC) is a foundational distributed systems paradigm that enables a program to execute code on a remote system as if it were a local function call. RPC abstracts the complexities of network communication—including serialization, deserialization, connection management, and error handling—presenting developers with a familiar programming model where remote operations appear as ordinary function invocations.

The concept dates to the early days of distributed computing, with early implementations like Sun RPC (NFS relies on this) in the 1980s. The appeal is straightforward: developers can build distributed systems using the same patterns they use for local computation, without needing to become experts in network programming. This productivity benefit made RPC the dominant paradigm for service-to-service communication in both enterprise systems and modern microservices architectures.

However, RPC's transparency comes with trade-offs. The illusion that remote calls behave like local calls can be dangerously misleading—network calls are orders of magnitude slower, can fail due to network problems that don't exist in local computation, and exhibit different failure modes (partial failures, timeouts, retry storms). Experienced distributed systems engineers learn to respect these differences.

## Key Concepts

**Stubs** are client-side proxies that expose the same interface as the remote service. When a client calls a stub method, the stub handles serialization of arguments, transmits the request to the server, waits for the response, and returns the deserialized result to the caller. Modern RPC frameworks generate stubs automatically from interface definitions.

**IDL (Interface Definition Language)** provides a way to formally define the interfaces between client and server, independent of any programming language. Protocol Buffers, Thrift, and gRPC use IDLs to generate type-safe stubs in multiple languages from a single interface definition.

**Serialization** transforms structured data (objects, structs, arguments) into a byte stream suitable for network transmission. Different RPC frameworks use different serialization formats: gRPC uses Protocol Buffers (binary, efficient), JSON-RPC uses JSON (human-readable, verbose), and Apache Thrift uses its own binary format.

**Transport Protocols** handle the actual network communication. Common options include HTTP/1.1, HTTP/2 (used by gRPC), and raw TCP. The transport choice affects connection reuse, multiplexing, and streaming capabilities.

**Error Handling Models** differ significantly between RPC frameworks. Some propagate exceptions across the network (like gRPC's status codes), while others use dedicated result types that must be explicitly checked. Understanding the failure modes—timeouts, connection errors, server-side exceptions—is critical for building robust distributed systems.

## How It Works

An RPC call follows a well-defined lifecycle:

1. **Client Call**: The client invokes a stub method with arguments
2. **Marshalling**: The stub serializes the arguments into a wire format
3. **Transport**: The serialized request is transmitted to the server
4. **Dispatch**: The server receives the request and dispatches it to the appropriate handler
5. **Execution**: The server executes the actual business logic
6. **Response**: Results are serialized and sent back to the client
7. **Unmarshalling**: The client deserializes the response
8. **Return**: Control returns to the caller with the result or error

```protobuf
// Protocol Buffers IDL example (bookstore.proto)
syntax = "proto3";

package bookstore;

service BookService {
  rpc GetBook(GetBookRequest) returns (Book);
  rpc ListBooks(ListBooksRequest) returns (stream Book);
  rpc CreateBook(CreateBookRequest) returns (Book);
}

message GetBookRequest {
  string isbn = 1;
}

message Book {
  string isbn = 1;
  string title = 2;
  string author = 3;
  float price = 4;
}
```

## Practical Applications

**Microservices Communication** is the most common modern use case for RPC. Services in a microservices architecture use RPC to communicate with each other, often with gRPC for internal communication (efficient binary format, streaming support) and REST/JSON APIs at the boundaries (easier debugging, broader tooling support).

**Database Client Libraries** often use RPC-style communication internally—the Postgres wire protocol, MySQL protocol, and Redis RESP are all forms of RPC where clients execute remote commands and receive responses.

**Cross-Language Integration** benefits from RPC's language-agnostic interface definitions. A Python microservice can call a Rust microservice seamlessly if both are generated from the same IDL definition, eliminating the need for custom integration code.

**Edge Computing** uses RPC to coordinate between central cloud infrastructure and edge nodes, enabling distributed computation without complex manual data transfer.

## Examples

**gRPC** (Google RPC) is the dominant modern RPC framework, built on HTTP/2 and Protocol Buffers. It supports streaming (client, server, and bidirectional), automatic client/server code generation in 10+ languages, and interop testing with major languages.

**Apache Thrift** (originally from Facebook) provides multi-language RPC with code generation for many languages, supporting both blocking and non-blocking clients.

**JSON-RPC** is a lightweight RPC protocol over JSON. It has no code generation and is often implemented manually, making it popular for simpler integrations and where HTTP/JSON compatibility is required.

```python
# Python gRPC client example
import grpc
from generated import bookstore_pb2_grpc, bookstore_pb2

channel = grpc.insecure_channel('localhost:50051')
stub = bookstore_pb2_grpc.BookServiceStub(channel)

# Simple RPC call
response = stub.GetBook(bookstore_pb2.GetBookRequest(isbn="978-0134685991"))
print(f"Found: {response.title} by {response.author}")

# Server streaming RPC
for book in stub.ListBooks(bookstore_pb2.ListBooksRequest()):
    print(f"{book.isbn}: {book.title}")
```

## Related Concepts

- [[api]] — API design principles and REST vs RPC trade-offs
- [[protocol-buffers]] — Protocol Buffers serialization format
- [[distributed-systems]] — Distributed systems patterns and challenges
- [[denial-of-service]] — RPC can be vectors for DoS attacks without proper protection
- [[rate-limiting]] — Essential for protecting RPC services from abuse

## Further Reading

- "Distributed Systems" by Maarten van Steen and Andrew Tanenbaum
- gRPC Documentation: https://grpc.io/docs/
- "Building Microservices" by Sam Newman
- Apache Thrift Documentation

## Personal Notes

RPC is one of those technologies where the documentation is deceptively simple but production use reveals deep complexity. Start with the happy path, but spend serious time understanding failure modes—timeouts, retries with idempotency, circuit breakers, and deadline propagation. A distributed system built on RPC without proper failure handling will fail spectacularly in production. Also, use Protocol Buffers or Thrift over JSON-RPC for any performance-sensitive path—the efficiency gains are substantial and the schema evolution capabilities are worth the upfront IDL investment.
