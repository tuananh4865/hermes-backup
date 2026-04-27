---
title: "REST API"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [rest, api, http, web]
---

## Overview

REST (Representational State Transfer) is an architectural style for designing networked applications, particularly web services. First described by Roy Fielding in his 2000 doctoral dissertation, REST provides a standardized approach to communication between client and server systems over HTTP. REST APIs (Application Programming Interfaces) expose resources identified by URLs and allow clients to interact with those resources using standard HTTP methods. The architectural style has become the dominant paradigm for web services due to its simplicity, scalability, and alignment with existing web infrastructure.

## Constraints

REST is defined by six architectural constraints that together promote loose coupling, scalability, and performance.

**Client-Server Architecture** separates the concerns of the user interface from data storage. Clients are responsible for the presentation layer and user experience, while servers manage data persistence and business logic. This separation allows clients and servers to evolve independently and enables horizontal scaling of server infrastructure.

**Statelessness** requires that each request from a client to the server must contain all information necessary to understand and process that request. The server does not store any client context between requests. This constraint simplifies server implementation, improves visibility (monitoring tools can see all necessary information in a single request), and enhances reliability since failures do not depend on stored state.

**Cacheability** allows responses to be marked as cacheable or non-cacheable. When properly implemented, caching can eliminate some client-server interactions entirely, reducing latency and improving efficiency. Web browsers and proxy servers commonly cache HTTP responses, making this constraint fundamental to web performance.

**Uniform Interface** standardizes how clients and servers communicate through resource identifiers (URLs), representation formats (JSON, XML), and standard HTTP methods. This uniformity is what makes REST widely accessible and relatively easy to implement.

**Layered System** allows the architecture to be composed of hierarchical layers, where each layer cannot see beyond the immediate layer it is interacting with. This enables load balancers, caches, and security layers to be inserted without affecting clients or servers.

**Code on Demand** (optional) permits servers to extend client functionality by transferring executable code, such as JavaScript. This constraint is rarely used but provides flexibility for future extensions.

## Methods

REST APIs use standard HTTP methods to perform operations on resources. GET retrieves a resource representation without side effects. POST creates a new resource on the server. PUT replaces an existing resource entirely with the provided representation. PATCH partially updates an existing resource. DELETE removes a resource from the server. These methods map directly to CRUD (Create, Read, Update, Delete) operations, making REST APIs intuitive and predictable.

## Best Practices

Effective REST API design follows consistent naming conventions using nouns rather than verbs in endpoint paths (e.g., /users instead of /getUsers). APIs should use proper HTTP status codes to indicate success, client errors, and server errors. Versioning helps manage API evolution without breaking existing clients. Pagination assists with handling large datasets. Authentication and authorization should use standard mechanisms like OAuth 2.0. Comprehensive documentation and clear error messages benefit both developers and consumers of the API.

## Related

- [[HTTP]] - The underlying protocol that REST APIs operate over
- [[API Design]] - Principles and patterns for creating effective APIs
- [[SOAP]] - A alternative XML-based web services protocol
- [[GraphQL]] - A query language for APIs that addresses some REST limitations
- [[JSON]] - The most common data format for REST API payloads
- [[Web Services]] - Broader category of services accessible over networks
