---
title: Web API
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [api, web, rest, graphql, http]
---

# Web API

## Overview

A Web API (Application Programming Interface) is a set of protocols, definitions, and tools that enables different software applications to communicate over the internet. Web APIs abstract the internal workings of a service and expose only the operations and data that external clients need, creating a contract between the service provider and its consumers. By standardizing how systems interact, Web APIs form the backbone of modern distributed computing and microservices architectures.

The ubiquity of Web APIs stems from their ability to enable the modular, interconnected software ecosystem we have today. When you use a mobile app to check the weather, book a ride, or send a message, that app is making requests to one or more Web APIs behind the scenes. The API acts as a clean boundary that hides complexity while enabling rich functionality.

## Key Concepts

**HTTP Methods**: Web APIs use the HTTP protocol's methods to indicate the type of operation being performed. The most common methods are GET (retrieve data), POST (create new resources), PUT/PATCH (update existing resources), and DELETE (remove resources). Each method has specific semantics about what it should do to the resource at the given endpoint.

**Request and Response Format**: Modern Web APIs typically use JSON (JavaScript Object Notation) for structuring data in both requests and responses. JSON's lightweight, human-readable format and native compatibility with JavaScript made it the de facto standard. Some APIs still use XML, particularly in enterprise or legacy systems.

**Authentication and Authorization**: APIs must verify who is making a request (authentication) and what they're allowed to do (authorization). Common approaches include API keys (simple but limited), OAuth 2.0 (industry standard for delegated access), and JWT (JSON Web Tokens) for stateless authentication.

**Status Codes**: HTTP status codes communicate the outcome of a request. 200-level codes indicate success, 400-level codes indicate client errors (bad request, not found), 500-level codes indicate server errors. Understanding status codes is essential for building robust API clients.

**Rate Limiting**: To prevent abuse and ensure fair usage, APIs enforce rate limits that cap how many requests a client can make in a given time period. Rate limits are communicated through headers like `X-RateLimit-Remaining`.

## How It Works

When a client makes a request to a Web API, several things happen in sequence:

1. **DNS Resolution**: The domain name is resolved to an IP address
2. **TCP Connection**: A connection is established to the server (often port 443 for HTTPS)
3. **TLS Handshake**: If using HTTPS, encryption parameters are negotiated
4. **HTTP Request**: The request is sent with method, headers, and optional body
5. **Server Processing**: The server authenticates the request, validates input, and performs the requested operation
6. **Response Generation**: The server prepares the response, including status code and body
7. **Response Transmission**: The response travels back to the client
8. **Connection Handling**: Depending on keep-alive settings, the connection may be reused or closed

```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json
X-RateLimit-Remaining: 499

{
  "id": "123",
  "name": "Jane Developer",
  "email": "jane@example.com",
  "created_at": "2024-03-15T10:30:00Z"
}
```

## Practical Applications

Web APIs power virtually every modern web and mobile application. Social media platforms expose APIs that allow third-party apps to post updates or retrieve user data. Payment gateways like Stripe provide APIs that handle transaction processing without merchants needing to handle sensitive card data. Weather services expose APIs that return forecast data for integration into calendars, travel apps, or smart home systems.

In enterprise contexts, Web APIs enable microservices architectures where large applications are decomposed into smaller, independently deployable services that communicate via well-defined APIs. This approach offers better scalability, fault isolation, and technology diversity than monolithic architectures.

## Examples

**REST API Example**: A task management API might expose endpoints for creating and retrieving tasks:

```javascript
// Create a new task
const response = await fetch('https://api.tasks.example.com/v1/tasks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Review API documentation',
    priority: 'high',
    due_date: '2026-04-20'
  })
});

const task = await response.json();
console.log(`Created task with ID: ${task.id}`);
```

**GraphQL API Example**: Unlike REST's fixed endpoints, GraphQL provides a single endpoint where clients specify exactly what data they need:

```graphql
query {
  user(id: "123") {
    name
    email
    tasks(filter: { status: "pending" }) {
      edges {
        node {
          id
          title
          due_date
        }
      }
    }
  }
}
```

## Related Concepts

- [[rest-api]] — RESTful API design patterns and constraints
- [[api]] — General API concepts and design principles
- [[graphql]] — GraphQL query language for APIs
- [[http]] — The underlying protocol for Web APIs
- [[microservices]] — Architecture pattern that relies heavily on Web APIs

## Further Reading

- "REST API Design Rulebook" by Mark Masse — Guidelines for consistent REST API design
- [Google Cloud API Design Guide](https://cloud.google.com/apis/design) — Best practices for API design
- [RESTful API Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html) — Levels of REST adoption

## Personal Notes

The evolution from SOAP/XML to REST/JSON was a huge usability improvement for web APIs. GraphQL's emergence addresses a real problem with REST—over-fetching or under-fetching data. The industry is still finding the right balance between API flexibility and simplicity.
