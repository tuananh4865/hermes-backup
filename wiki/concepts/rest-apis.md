---
title: "REST APIs"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rest-api, rest, api, web-services, http]
---

# REST APIs

## Overview

REST (Representational State Transfer) is an architectural style for designing networked applications, introduced by Roy Fielding in his 2000 doctoral dissertation. REST APIs (also called RESTful APIs) are web services that adhere to REST constraints and expose resources via HTTP endpoints. Rather than using complex protocols like SOAP or XML-RPC, REST leverages standard HTTP methods—GET, POST, PUT, DELETE, PATCH—to perform operations on resources identified by URLs.

The fundamental idea behind REST is that every piece of information your application manages is a **resource**, accessible through a uniform interface. Clients interact with resources by transferring representations—JSON, XML, or other formats—between themselves and the server. This separation of concerns, stateless communication, and cacheable responses make REST APIs highly scalable and widely supported across languages, platforms, and tools.

REST has become the dominant style for public web APIs because of its simplicity, readability, and alignment with HTTP semantics. Major platforms like GitHub, Twitter, Stripe, and AWS expose their functionality through REST APIs, making it an essential skill for backend developers, frontend engineers, and anyone building software that communicates over a network.

## Core Principles

REST is built on six architectural constraints that distinguish it from other API styles:

**Client-Server Architecture** separates the concerns of data storage (server) from user interface (client). This separation allows clients and servers to evolve independently, scale separately, and be implemented using different technologies. The client need not know anything about how data is stored, and the server need not know anything about the user interface.

**Statelessness** means each request from client to server must contain all information needed to understand and process that request. The server stores no client context between requests. Each request is independent, which simplifies the server logic, improves reliability, and makes caching straightforward—but it also means clients must resend any authentication credentials with every request.

**Cacheability** allows responses to be labeled as cacheable or non-cacheable. When properly implemented, caching can eliminate redundant client-server interactions, reduce latency, and improve overall system efficiency. REST mandates that data implicitly or explicitly labels itself as cacheable or non-cacheable.

**Uniform Interface** enforces a consistent contract between client and server. Resources are identified in requests (via URLs), and the representation of a resource contains enough information to modify or delete it. All interactions follow the same rules and use the same methods, creating a predictable and discoverable API surface.

**Layered System** allows the architecture to be composed of hierarchical layers, where each layer cannot see beyond the immediate layer it interacts with. A client cannot tell whether it is communicating directly with the end server or with an intermediary like a load balancer, proxy, or gateway.

**Code on Demand** (optional) allows servers to extend client functionality by sending executable code. While rarely used in practice, this constraint permits clients to download scripts that enhance their behavior.

## HTTP Methods and CRUD Operations

REST APIs map CRUD (Create, Read, Update, Delete) operations to standard HTTP methods:

| Method | CRUD Operation | Description |
|--------|---------------|-------------|
| GET | Read | Retrieve a resource or collection of resources without side effects |
| POST | Create | Submit a new resource to the server |
| PUT | Update (replace) | Replace an existing resource entirely with the submitted data |
| PATCH | Update (modify) | Partially update an existing resource |
| DELETE | Delete | Remove a resource from the server |

```http
GET /api/users/123 HTTP/1.1
Host: example.com
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}
```

```http
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "name": "Bob Smith",
  "email": "bob@example.com"
}

HTTP/1.1 201 Created
Location: /api/users/124
```

## Response Codes

REST APIs use HTTP status codes to communicate the result of an operation:

- **2xx**: Success codes. `200 OK` (standard success), `201 Created` (resource successfully created), `204 No Content` (success with no body, e.g., DELETE).
- **3xx**: Redirection codes. `301 Moved Permanently`, `304 Not Modified` (for caching).
- **4xx**: Client error codes. `400 Bad Request` (malformed request), `401 Unauthorized` (missing authentication), `403 Forbidden` (authenticated but not permitted), `404 Not Found`, `422 Unprocessable Entity` (validation errors).
- **5xx**: Server error codes. `500 Internal Server Error`, `503 Service Unavailable`.

## Best Practices

Well-designed REST APIs follow conventions that make them intuitive and maintainable:

**Use nouns, not verbs**, in endpoint paths: `/api/users` not `/api/getUsers`. HTTP methods already convey the action.

```http
# Good
GET /api/products/42
DELETE /api/orders/99

# Avoid
GET /api/getProduct?id=42
DELETE /api/deleteOrder?id=99
```

**Version your API** to allow breaking changes without disrupting existing clients: `/api/v1/users`, `/api/v2/users`.

**Use pagination** for large collections: `GET /api/posts?page=2&limit=20`.

**Provide meaningful error responses** with error codes, messages, and sometimes links to documentation:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Email address is invalid",
    "field": "email",
    "docs": "https://api.example.com/errors/VALIDATION_FAILED"
  }
}
```

## Related Concepts

- [[GraphQL]] — An alternative query language and runtime for APIs that solves REST's over-fetching and under-fetching problems
- [[API Design]] — The broader practice of designing application programming interfaces
- [[HTTP]] — The underlying protocol that REST APIs are built upon
- [[Microservices]] — Architectural style where REST APIs commonly facilitate service-to-service communication
- [[JSON]] — The most common data format for REST API request and response bodies

## Further Reading

- [Roy Fielding's REST dissertation](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) — The original specification
- [REST API Tutorial](https://restfulapi.net/) — Comprehensive REST API design guide
- [HTTP Status Codes Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Personal Notes

REST APIs are the backbone of modern web services. The simplicity of mapping HTTP methods to CRUD operations makes them intuitive, but designing truly RESTful APIs requires understanding the deeper constraints Fielding outlined. Versioning strategy and error response design are often overlooked aspects that cause significant pain as APIs evolve.
