---
title: "REST Principles"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [api-design, web-services, architecture, http]
---

# REST Principles

REST (Representational State Transfer) is an architectural style for designing networked applications, introduced by Roy Fielding in his 2000 doctoral dissertation. REST is not a protocol or standard but a set of constraints that when applied to an API's design, promote scalability, loose coupling, and predictability.

## Overview

RESTful APIs are built on the foundation of HTTP (Hypertext Transfer Protocol), leveraging its methods, status codes, and headers to enable client-server communication. The core idea is that clients interact with servers through a fixed set of operations (HTTP verbs) applied to resources, identified by URLs. Each representation of a resource—JSON, XML, HTML, etc.—contains the information needed for clients to transition the application state.

The architectural style emerged as a simpler alternative to earlier distributed computing approaches like CORBA, DCOM, and SOAP. By constraining the interface to a small, well-understood set of operations, REST enables intermediaries (proxies, caches, gateways) to understand and transform messages without deep knowledge of individual services.

## Key Constraints

REST is defined by six architectural constraints that work together:

**Client-Server Architecture** separates concerns between the user interface (client) and data storage (server). Clients are not concerned with data persistence, which remains encapsulated on the server. This separation allows components to evolve independently and scale horizontally.

**Statelessness** requires that each request from client to server must contain all information needed to understand and process it. The server stores no client context between requests. This improves visibility (monitoring requests is straightforward), scalability (no server-side session affinity), and reliability (failed requests can be safely retried).

**Cacheability** allows responses to be labeled as cacheable or non-cacheable. When properly implemented, caching eliminates some client-server interactions and improves performance and scalability.

**Layered System** allows an architecture to be composed of hierarchical layers, where each layer cannot see beyond the immediate layer it's calling. This promotes modularity and enables load balancers, firewalls, and other intermediaries.

**Code on Demand** (optional) allows servers to temporarily extend client functionality by transferring executable code. JavaScript in browsers is the most common example.

**Uniform Interface** is the distinguishing constraint of REST, requiring four properties: resource identification through URLs; resource manipulation through representations; self-descriptive messages; and hypermedia as the engine of application state (HATEOAS).

## HTTP Methods in REST

The uniform interface relies on a standard mapping of HTTP methods to CRUD operations:

| Method | Semantic | Idempotent | Safe |
|--------|----------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Update resource (partial) | No | No |
| DELETE | Remove resource | Yes | No |

GET retrieves a representation of a resource without side effects. POST submits data to create a new resource or trigger an action. PUT replaces the entire resource at a given URI. PATCH applies partial modifications. DELETE removes the specified resource.

## HATEOAS and Hypermedia

Hypermedia as the Engine of Application State (HATEOAS) is often considered the defining feature of true REST. It means that, beyond providing data, responses include links to related actions. A client discovering an API through these links, rather than through out-of-band knowledge, can interact with the service without prior documentation.

```json
{
  "account": {
    "id": "12345",
    "balance": 1000.00,
    "currency": "USD",
    "links": {
      "deposit": "/accounts/12345/deposit",
      "withdraw": "/accounts/12345/withdraw",
      "transfer": "/accounts/12345/transfer"
    }
  }
}
```

This approach enables loose coupling: clients don't need to hardcode URI structures, and servers can evolve their routing without breaking clients.

## Practical Applications

REST is the dominant style for public web APIs due to its simplicity, scalability, and excellent tooling support. Major platforms—GitHub, Stripe, Twilio—expose RESTful interfaces. Inside organizations, REST is commonly used for microservices communication, mobile backends, and single-page applications connecting to backend services.

Frameworks like Express.js (Node.js), Flask/Django REST Framework (Python), and Spring Boot (Java) provide scaffolding for building REST APIs. API gateways (Kong, AWS API Gateway) handle cross-cutting concerns like authentication, rate limiting, and logging for REST services.

## Richardson Maturity Model

Leonard Richardson proposed a model that breaks down REST compliance into levels:

- **Level 0**: Single URI endpoint, single HTTP method (often XML-RPC or SOAP in disguise)
- **Level 1**: Multiple resources but single HTTP method
- **Level 2**: Proper HTTP verbs and status codes
- **Level 3**: HATEOAS (full REST)

Most "REST APIs" in practice reach Level 2. Achieving Level 3 requires more investment but provides the long-term benefits of truly evolvable APIs.

## Common Mistakes

Many "REST APIs" violate core principles. Using POST for all operations defeats the uniform interface. Returning 200 OK for error cases breaks visibility. Omitting hypermedia links couples clients to implementation details. Understanding the original constraints prevents these anti-patterns.

## Related Concepts

- [[HATEOAS]] - Hypermedia as the engine of application state
- [[HTTP Protocol]] - The protocol REST is built upon
- [[API Gateway]] - Intermediary for REST API management
- [[Microservices]] - Architecture style often paired with REST
- [[GraphQL]] - Alternative API query language

## Further Reading

- Fielding, R. T. (2000). "Architectural Styles and the Design of Network-based Software Architectures"
- Richardson, L., & Ruby, S. (2007). "RESTful Web Services"
- "API Design Patterns" by J.J. Geewax

## Personal Notes

REST's simplicity is both its strength and weakness. The constraints are easy to follow at small scale but become challenging with complex operations. For most web APIs, a well-designed Level 2 REST API hits the sweet spot of usability and evolvability. Don't feel pressured to implement full HATEOAS if your clients can't consume it—but understand what you're trading off.
