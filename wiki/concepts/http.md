---
title: HTTP
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [http, protocol, web, networking]
---

# HTTP

HTTP (Hypertext Transfer Protocol) is the foundational protocol governing data communication on the World Wide Web. It defines how clients and servers exchange information, enabling the retrieval of web pages, API calls, and multimedia content. HTTP operates as a request-response protocol, where a client—typically a web browser or application—sends a request to a server, which then processes the request and returns a response containing the requested data or status information.

The protocol was originally developed by Tim Berners-Lee in 1991 at CERN, with HTTP/1.0 being the first standardized version. Since then, the protocol has evolved through HTTP/1.1, HTTP/2, and HTTP/3, each iteration bringing improvements in performance, security, and efficiency. HTTP/2 introduced multiplexing and header compression, while HTTP/3 leverages the QUIC transport protocol for even faster, more reliable connections. HTTPS (HTTP Secure) adds TLS encryption to protect data in transit, making secure web communication the default for sensitive applications.

## Overview

HTTP is an application-layer protocol that runs on top of TCP/IP networking protocols. It follows a stateless client-server model, meaning each request from a client to a server is independent and not influenced by previous requests. While this design simplifies server implementation and scalability, it has led to the development of mechanisms like cookies and sessions to maintain state across multiple requests.

The HTTP communication flow begins when a client constructs and sends an HTTP request message to a server. This request specifies the method to be performed, the resource being requested (identified by a URL), and optional headers containing metadata. The server receives the request, processes it, and returns an HTTP response containing a status code, response headers, and optionally a message body with the requested content.

HTTP is a text-based protocol, with messages encoded in ASCII. Each request and response consists of a start line, headers, and an optional body. This human-readable format facilitates debugging and development, though parsing efficiency has driven the binary encoding used in HTTP/2 and HTTP/3.

## Methods

HTTP defines a set of methods (also called verbs) that indicate the desired action to be performed on a resource. Each method has specific semantics, and using them correctly ensures consistent and predictable behavior across web applications.

**GET** requests the retrieval of a resource without modifying it. GET is the most common HTTP method, used for fetching web pages, images, API data, and other content. It should be idempotent, meaning multiple identical requests produce the same result as a single request.

**POST** submits data to the server for processing. It is commonly used for creating new resources, submitting forms, and triggering actions that may modify server state. Unlike GET, POST requests typically include a request body containing the data being submitted.

**PUT** uploads or replaces a resource at a specific URL with the data provided in the request body. If the resource does not exist, PUT may create it. PUT is idempotent, as sending the same request multiple times yields the same result.

**DELETE** removes the specified resource from the server. Like GET, it should be idempotent—deleting a resource that has already been removed should return a success status.

**PATCH** applies partial modifications to a resource, unlike PUT which replaces the entire resource. PATCH is used when only specific fields of a resource need to be updated.

**HEAD** is identical to GET but requests only the headers of the response, without the message body. It is useful for checking metadata, validating resource existence, or determining if a resource has been modified without downloading the entire content.

**OPTIONS** requests information about the communication options available for a target resource or server. It allows clients to discover which HTTP methods and features are supported before making actual requests.

## Status Codes

HTTP status codes are three-digit numbers returned in responses to indicate the outcome of a request. They are grouped into five classes based on the first digit, each conveying a distinct category of response.

**1xx (Informational)** status codes indicate that the request has been received and the server is continuing to process it. Examples include 100 Continue (the client should continue sending the request) and 101 Switching Protocols (the server is switching protocols as requested).

**2xx (Success)** codes confirm that the request was successfully received, understood, and accepted. The most common is 200 OK, indicating a successful GET or POST request. 201 Created reports successful resource creation, while 204 No Content indicates success with no content to return.

**3xx (Redirection)** codes signal that further action is needed to complete the request. 301 Moved Permanently and 302 Found (or 307 Temporary Redirect) redirect clients to different URLs. 304 Not Modified is used for caching, telling the client that the requested resource has not changed since last retrieval.

**4xx (Client Error)** codes indicate problems with the request itself. 400 Bad Request means the server cannot process malformed syntax. 401 Unauthorized requires authentication, while 403 Forbidden means the client lacks permission even with valid credentials. 404 Not Found is the well-known code for missing resources, and 422 Unprocessable Entity indicates semantic errors in the submitted data.

**5xx (Server Error)** codes denote that the server failed to fulfill a valid request. 500 Internal Server Error is a generic catch-all for unexpected failures. 502 Bad Gateway indicates a problem with an intermediate server, while 503 Service Unavailable means the server is temporarily overloaded or down for maintenance. 504 Gateway Timeout signals that an intermediate server did not receive a timely response.

## Related

- [[HTTPS]] — Secure version of HTTP with TLS encryption
- [[REST API]] — Architectural style for designing networked applications using HTTP
- [[tcp-ip]] — The underlying transport and network protocol suite
- [[URL]] — Uniform Resource Locator, the address system for web resources
- [[WebSocket]] — Protocol for persistent full-duplex communication
- [[API]] — Application programming interfaces that often use HTTP
- [[JSON]] — Common data format for HTTP API responses
