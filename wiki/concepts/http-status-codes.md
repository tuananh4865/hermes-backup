---
title: "HTTP Status Codes"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [http, web, api, rest, networking, debugging]
---

# HTTP Status Codes

## Overview

HTTP status codes are three-digit numeric responses sent by a server to indicate the result of a client's request. They are a fundamental part of the HTTP specification (defined in RFC 2616 and updated in RFC 7231) and serve as the primary means by which servers communicate outcomes to clients — whether those clients are web browsers, mobile applications, API consumers, or automated systems.

Status codes are grouped into five classes based on the first digit, each conveying the general category of response. Understanding these codes is essential for web developers, DevOps engineers, API designers, and anyone debugging distributed systems. A developer who sees a `502 Bad Gateway` error in production should immediately understand that the problem lies in communication between servers (typically a reverse proxy or load balancer and upstream servers), not in the client or the final destination server.

Beyond the numeric code, HTTP responses include a reason phrase — a human-readable explanation like "Not Found" or "Internal Server Error" — though this phrase has no protocol-level significance and varies between servers. The critical information is in the numeric code itself.

## Status Code Categories

### 1xx — Informational

The 1xx range indicates that a request was received and the server is continuing to process it. These responses are provisional and never appear in final application logic because HTTP clients historically did not support them well.

**100 Continue** tells the client to proceed with sending the request body. This is used in "expect: 100-continue" handshakes where large uploads negotiate acceptance before transmitting data.

**101 Switching Protocols** occurs during protocol upgrades, most commonly when upgrading an HTTP connection to WebSocket. The server signals agreement to change protocols before any data is exchanged on the new protocol.

### 2xx — Success

The 2xx range indicates the request was successfully received, understood, and accepted.

**200 OK** is the generic success code. The meaning of the response body depends on the method used — GET returns the resource, POST returns the result of the action, etc.

**201 Created** signals that a new resource was successfully created, typically as a result of a POST request. The response should include a `Location` header pointing to the newly created resource.

**202 Accepted** indicates that a request has been accepted for processing but the processing has not completed. This is appropriate for asynchronous operations where the client does not wait for the final result.

**204 No Content** is used when a request succeeds but there is no content to return (common in DELETE operations). Unlike 200, a 204 response must not include a message body.

**206 Partial Content** is returned when a server delivers only part of a resource, typically in response to a Range header request. This is essential for resumable downloads and video streaming.

### 3xx — Redirection

The 3xx range indicates the client must take additional action to complete the request.

**301 Moved Permanently** tells the client the resource has a new permanent URL. All future requests should use the new URL. Search engines transfer page rank to the new location.

**302 Found** (historically "Moved Temporarily") indicates a temporary redirect. The client should continue using the original URL. This is often misused for non-redirect purposes, which led to confusion with POST operations — hence the introduction of 303 and 307.

**303 See Other** explicitly directs clients to follow the redirect with a GET request, regardless of the original method. Useful for POST-Redirect-GET patterns.

**304 Not Modified** is a conditional response that tells the client the cached version is still valid, avoiding re-downloading the resource. This relies on [[HTTP caching]] headers like `ETag` and `Last-Modified`.

**307 Temporary Redirect** guarantees the request method will not change during the redirect, unlike 302 which could be ambiguously interpreted.

**308 Permanent Redirect** combines the permanence of 301 with the method preservation of 307.

### 4xx — Client Errors

The 4xx range indicates the request contains bad syntax or cannot be fulfilled due to something the client must fix.

**400 Bad Request** is a generic error for malformed requests — invalid JSON, missing required parameters, or malformed syntax that the server cannot parse.

**401 Unauthorized** (despite the misleading name) indicates the request lacks valid authentication credentials. The server expects the client to authenticate. After successful authentication, the client may retry with proper credentials.

**403 Forbidden** indicates the server understood the request but refuses to authorize it. Unlike 401, authentication will not help. The resource exists but access is denied — perhaps due to IP blocking or permission issues.

**404 Not Found** signals the resource does not exist at the specified URL. This is the most recognized status code, frequently seen when navigating to broken links. Note that 404 does not distinguish between "resource never existed" and "resource existed but was deleted."

**405 Method Not Allowed** occurs when the HTTP method is not supported for the requested URL. The response must include an `Allow` header listing supported methods.

**409 Conflict** indicates the request conflicts with the current state of the resource — for example, attempting to create a duplicate resource or uploading a file where a newer version already exists.

**410 Gone** is like 404 but explicitly indicates the resource was permanently deleted and is not expected to return. Search engines use this to de-index content.

**422 Unprocessable Entity** (from WebDAV) indicates the request is syntactically correct but semantically wrong — valid JSON that fails validation rules.

**429 Too Many Requests** signals rate limiting. The response should include a `Retry-After` header indicating when to retry.

### 5xx — Server Errors

The 5xx range indicates the server failed to fulfill a valid request — the problem lies with the server, not the client.

**500 Internal Server Error** is the generic error when an unexpected condition was encountered. This is the fallback error; good API design uses more specific codes.

**501 Not Implemented** indicates the server does not support the functionality required to fulfill the request. The method or feature is not recognized.

**502 Bad Gateway** occurs when a gateway or proxy server received an invalid response from an upstream server. This typically indicates a problem in the server-to-server communication chain, often a failed service or misconfigured proxy.

**503 Service Unavailable** signals the server is temporarily unable to handle requests — usually due to maintenance or overloading. The `Retry-After` header indicates when to retry.

**504 Gateway Timeout** is like 502 but specifically indicates the upstream server did not respond in time.

## Practical Applications

In [[REST API]] design, status codes are the primary mechanism for communicating outcomes. A well-designed API uses the full range of appropriate codes rather than returning 200 for everything and 500 for all errors. This enables client libraries, middleware, and automated tooling to handle responses intelligently.

HTTP clients and reverse proxies use status codes for routing, retries, and circuit breaking. Tools like [[nginx]] and HAProxy treat 5xx errors as signals to trigger failovers or degrade gracefully.

## Code Example

A simple Python HTTP client that handles status codes appropriately:

```python
import requests
from requests.exceptions import HTTPError

def fetch_user(user_id: int) -> dict:
    response = requests.get(
        f"https://api.example.com/users/{user_id}",
        timeout=10
    )

    try:
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            return {"created": response.json()}
        elif response.status_code == 204:
            return {"deleted": True}

    except HTTPError as e:
        if response.status_code == 401:
            raise AuthenticationError("Invalid or missing API key")
        elif response.status_code == 404:
            raise NotFoundError(f"User {user_id} not found")
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After', 60)
            raise RateLimitError(f"Rate limited. Retry after {retry_after}s")
        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code}")
        raise

def fetch_all_users():
    page = 1
    while True:
        resp = requests.get(f"https://api.example.com/users?page={page}")
        if resp.status_code == 200:
            data = resp.json()
            if not data:
                break
            yield from data
            page += 1
        elif resp.status_code == 206:
            yield from resp.json()
            break
        else:
            resp.raise_for_status()
```

## Related Concepts

- [[REST API Design]] - Best practices for HTTP API design
- [[HTTP Caching]] - Using headers to reduce unnecessary requests
- [[WebSocket]] - Real-time communication using HTTP protocol upgrade
- [[Authentication]] - How HTTP interacts with auth mechanisms
- [[Load Balancing]] - How proxies interpret status codes for health checks

## Further Reading

- [RFC 7231 — HTTP/1.1 Semantics and Content](https://tools.ietf.org/html/rfc7231) — Official specification
- [Mozilla MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — Comprehensive reference
- [HTTP API Design Best Practices](https://developer.github.com/v3/#http-errors) — Practical guide from field experience

## Personal Notes

The 401/403 confusion in HTTP is one of the most persistent usability failures in the spec. 401 means "you need to authenticate" (authentication), while 403 means "you don't have permission" (authorization). If you have credentials but they are insufficient, you get 403. If you have no credentials, you get 401. Almost everyone gets this backwards the first few times.

429 (Too Many Requests) is increasingly important in modern API design with rate limiting becoming standard. Always check for the `Retry-After` header rather than blindly retrying with fixed backoff.
