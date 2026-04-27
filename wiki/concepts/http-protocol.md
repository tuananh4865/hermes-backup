---
title: "HTTP Protocol"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [http, web, networking, request, response, rest, api]
---

## Overview

HTTP (HyperText Transfer Protocol) is the foundation of data communication on the World Wide Web. It is an application-layer protocol that defines how clients (typically browsers) request data from servers and how servers respond to those requests. HTTP follows a request-response model where clients initiate communication by sending a request, and servers process it and return a response containing the requested resource or status information.

HTTP is a stateless protocol—each request is independent, with no built-in mechanism for remembering previous requests. This simplicity enabled scalability but required additional mechanisms (cookies, sessions, tokens) for stateful interactions. The protocol has evolved through versions: HTTP/1.0, HTTP/1.1 (the most widely deployed), HTTP/2 (introducing multiplexing and header compression), and HTTP/3 (using QUIC for faster, more reliable connections).

Understanding HTTP is essential for web developers, API designers, and anyone building distributed systems. It governs not just web browsing but also REST API design, microservices communication, and modern single-page applications.

## Key Concepts

**HTTP Methods** (also called verbs) indicate the desired action:

- GET retrieves a resource without side effects
- POST creates a new resource
- PUT replaces an existing resource entirely
- PATCH partially updates a resource
- DELETE removes a resource
- HEAD retrieves headers only (no body)
- OPTIONS checks allowed methods for a resource

**Status Codes** indicate the outcome of a request:

- 1xx: Informational (100 Continue, 101 Switching Protocols)
- 2xx: Success (200 OK, 201 Created, 204 No Content)
- 3xx: Redirection (301 Moved Permanently, 304 Not Modified)
- 4xx: Client Error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
- 5xx: Server Error (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable)

**Headers** provide metadata about requests and responses. Key headers include Content-Type, Content-Length, Authorization, Cache-Control, User-Agent, and Cookie. Custom headers using the X- prefix (now deprecated in favor of standardized headers) enable extension functionality.

## How It Works

An HTTP transaction begins when a client opens a TCP connection to a server (typically port 80 for HTTP, 443 for HTTPS/TLS). The client sends a request line specifying the method, path, and protocol version, followed by headers and optional body content.

```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
User-Agent: MyApp/1.0
```

The server processes the request, performs the indicated action, and returns a response line with status code, headers, and optional body.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600
Date: Mon, 13 Apr 2026 04:58:00 GMT

{"id": 123, "name": "Alice", "email": "alice@example.com"}
```

HTTP/2 introduced multiplexing, allowing multiple requests/responses to share a single connection through interleaved frames. HTTP/3 uses QUIC (built on UDP) to reduce connection establishment time and improve performance on unreliable networks.

## Practical Applications

HTTP powers web browsing, REST API design, and service-oriented architectures. RESTful APIs use HTTP methods semantically: GET for retrieval, POST for creation, PUT/PATCH for updates, DELETE for removal. GraphQL APIs typically use POST for all operations, with the query in the body.

Webhooks use HTTP callbacks to notify systems of events. OAuth 2.0 flows use HTTP redirects and token exchanges for authentication. SPDY and HTTP/2 multiplexing improved page load times significantly by eliminating head-of-line blocking in HTTP/1.1.

## Examples

```bash
# GET request with curl
curl -X GET "https://api.example.com/users/123" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $API_TOKEN"

# POST request to create a resource
curl -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"name": "Bob", "email": "bob@example.com"}'

# Checking available HTTP methods with OPTIONS
curl -X OPTIONS "https://api.example.com/users" -i
```

## Related Concepts

- [[HTTPS]] - Secure HTTP over TLS encryption
- [[REST API]] - Architectural style using HTTP semantics
- [[Network Protocols]] - Lower-layer communication rules
- [[Cookies]] - State management in stateless HTTP
- [[WebSocket]] - Bidirectional persistent connections

## Further Reading

- MDN Web Docs HTTP documentation
- RFC 9110 (HTTP Semantics) and RFC 9111 (HTTP Caching)
- "HTTP/2 in Action" by Barry Pollard

## Personal Notes

When designing APIs, align with HTTP semantics—use the right methods and status codes. This makes your API intuitive and allows clients to rely on standard behavior. Also consider idempotency: GET, PUT, and DELETE should be safe to retry, while POST should not. HTTP caching is powerful but often misunderstood—learn Cache-Control directives thoroughly.
