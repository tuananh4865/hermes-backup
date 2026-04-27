---
title: api-design
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [api-design, rest, web, architecture]
---

# api-design

## Overview

API design is the process of defining the contract, structure, and conventions that allow software applications to communicate with each other. A well-designed API provides a clear, predictable interface that enables developers to build clients and integrations without needing to understand the internal implementation of the server. API design spans decisions about data formats, authentication mechanisms, request and response structures, versioning approaches, and error reporting. It is a foundational concern in distributed systems, microservices architectures, and any context where systems must expose functionality to external consumers or other services.

Good API design prioritizes usability, consistency, and evolvability. Usability means that developers can predict how the API behaves based on documentation and intuition. Consistency ensures that similar operations follow similar patterns across the entire API surface. Evolvability allows the API to grow and change over time without breaking existing clients, which is critical for long-lived systems that must maintain backward compatibility while adding new features.

APIs can be designed around various architectural styles, including REST, GraphQL, gRPC, and WebSocket-based protocols. Each style has distinct trade-offs in terms of flexibility, performance, tooling support, and client complexity. The most prevalent style for web APIs remains REST, which provides a mature, widely understood set of conventions that align well with HTTP semantics.

## REST Principles

Representational State Transfer (REST) is an architectural style that leverages HTTP conventions to build scalable, stateless web services. REST APIs are organized around resources, which are identifiable entities that clients interact with through a uniform interface.

**Resources** are the core building blocks of a REST API. Each resource has a unique identifier, typically expressed as a URL path such as `/users/{id}` or `/orders/{id}`. Resources represent nouns in your domain model, not actions or verbs. This naming convention makes APIs intuitive because they mirror the structure of the data rather than the operations performed on it.

**Verbs** represent the actions to perform on resources. REST relies on standard HTTP methods:

- **GET** retrieves a representation of a resource without side effects. GET requests should be idempotent and safe.
- **POST** creates a new resource. The request body typically includes the data for the resource to create.
- **PUT** replaces an existing resource entirely with the provided representation. It is idempotent but not safe.
- **PATCH** partially updates an existing resource, applying only the fields included in the request body.
- **DELETE** removes a resource, also idempotent but not safe.

Using the correct verb for each operation is essential for predictability. Clients depend on verbs carrying semantic meaning about what will happen and whether they can be retried safely.

**Status codes** communicate the outcome of a request. REST APIs use HTTP status codes to indicate success, client errors, server errors, and redirects:

- **2xx** codes indicate successful operations: 200 OK for general success, 201 Created for resource creation, 204 No Content for successful operations with no response body.
- **4xx** codes indicate client errors: 400 Bad Request for malformed input, 401 Unauthorized for missing authentication, 403 Forbidden for insufficient permissions, 404 Not Found for missing resources, 422 Unprocessable Entity for validation errors.
- **5xx** codes indicate server errors: 500 Internal Server Error for unexpected failures, 503 Service Unavailable for temporary unavailability.

Returning the correct status code allows clients to handle errors programmatically and distinguish between recoverable and fatal conditions.

## Versioning

API versioning enables an API to evolve without breaking existing clients. As requirements change, new fields may be added, resources may be restructured, or behaviors may be modified. Versioning provides a mechanism for managing these changes while maintaining backward compatibility with older client versions.

**URL path versioning** embeds the version in the resource path, such as `/v1/users` or `/v2/orders`. This approach is straightforward and visible, making it easy for developers to understand which version they are using. It also simplifies routing and debugging because the version is explicit in every request.

**Header versioning** uses custom headers like `API-Version: 2024-01-01` or `Accept: application/vnd.example.v2+json`. This keeps URLs clean and resource-focused but requires clients to manage headers for each request, adding complexity.

**Query parameter versioning** appends a version indicator to the URL, such as `/users?version=2`. It offers a middle ground between the visibility of path versioning and the cleanliness of header-based approaches.

Regardless of the chosen strategy, versioning should be accompanied by a deprecation policy that communicates how long older versions will be supported and what migration paths are available. Documentation should clearly describe differences between versions and highlight any breaking changes.

## Best Practices

Consistent naming conventions make APIs self-documenting and easier to work with. Path segments should use lowercase letters and hyphens for multi-word names, such as `/order-items` rather than `/orderItems` or `/order_items`. Plural nouns are conventional for collections, so `/users` rather than `/user`.

Error responses should be consistent and informative. Include an error code or identifier that clients can programmatically inspect, a human-readable message describing the problem, and when appropriate, additional context such as field-level validation errors. A structured error response body might look like `{ "error": "validation_failed", "message": "The request body contains invalid fields.", "details": [{ "field": "email", "issue": "Invalid format" }] }`.

Pagination is necessary for endpoints that return collections, as unbounded result sets can degrade performance and consume excessive bandwidth. Cursor-based pagination is generally more robust than offset-based pagination for large or frequently updated datasets because it remains stable even as new records are inserted.

Authentication and authorization should be handled using standard protocols such as OAuth 2.0 or API keys. Tokens should be transmitted securely, typically via the `Authorization` header, and should have limited lifetimes to reduce the impact of compromised credentials.

Documentation is not optional. Provide clear, up-to-date reference documentation that covers all endpoints, request and response formats, authentication requirements, error codes, and usage examples. Interactive documentation tools such as OpenAPI (formerly Swagger) enable developers to explore and test APIs directly from the documentation page.

## Related

- [[REST Principles]] - Deeper exploration of resource-oriented architecture
- [[HTTP Status Codes]] - Comprehensive reference for HTTP response codes
- [[GraphQL API Design]] - Alternative query-based API approach
- [[Microservices Architecture]] - How APIs underpin service decomposition
- [[API Security]] - Authentication, authorization, and rate limiting
- [[OpenAPI Specification]] - Standard for describing REST APIs
- [[Web Architecture]] - The broader context of web-based system design
