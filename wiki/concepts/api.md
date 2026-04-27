---
title: API
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [api, web, integration, rest, http, client-server]
---

# API

## Overview

An API (Application Programming Interface) is a specification that defines how software components interact—whether across processes, across machines, or across the internet. APIs establish the contracts: what operations are available, what inputs they accept, what outputs they return, and what errors might occur. By defining clear interfaces, APIs enable modularity, interoperability, and abstraction—developers can use complex systems without understanding their internal implementation.

In modern software, APIs are ubiquitous. When a mobile app displays weather data, it calls a weather service's API. When you "Sign in with Google," that app uses Google's API to authenticate you. When AI agents like [[ai-agents]] take actions in the world, they typically do so by calling APIs. The rise of [[large-language-models]] has also introduced the concept of "API-style" interfaces for model inference—developers send prompts and receive completions via HTTP requests.

Understanding APIs is foundational to software integration. Whether you're building a service that exposes its own API, integrating third-party services, or designing systems that communicate internally, the concepts and patterns of API design apply broadly.

## Key Concepts

**Endpoint**: A specific URL at which an API can be accessed. For example, `https://api.example.com/users` might be the endpoint for user-related operations. Each endpoint supports specific HTTP methods.

**HTTP Methods**: Standard verbs that define the operation:
- `GET`: Retrieve data (read-only)
- `POST`: Create new resource
- `PUT`: Replace/replace a resource
- `PATCH`: Partially update a resource
- `DELETE`: Remove a resource

**Request and Response**: The client sends a request (headers, parameters, body) and receives a response (status code, headers, body). APIs typically exchange data in JSON format, though XML and other formats exist.

**Status Codes**: Numeric codes indicating the result:
- `2xx`: Success (200 OK, 201 Created, 204 No Content)
- `3xx`: Redirection
- `4xx`: Client error (400 Bad Request, 401 Unauthorized, 404 Not Found)
- `5xx`: Server error (500 Internal Server Error)

**Authentication/Authorization**: APIs need to verify who's making the request:
- **API Keys**: Simple tokens passed in headers
- **OAuth 2.0**: Token-based authorization (see [[OAuth-2.0]])
- **JWT**: Self-contained tokens with claims (see [[jwt]])

**Rate Limiting**: APIs restrict how many requests a client can make, typically expressed as requests per minute or per day. Exceeding limits returns `429 Too Many Requests`.

**Pagination**: Large result sets are returned in chunks via pagination patterns like cursor-based or offset-based pagination.

## How It Works

REST (Representational State Transfer) is the most common API architectural style for web APIs. A RESTful API structures interactions around resources (nouns) rather than actions (verbs):

**URL Structure**: Resources are identified by URLs:
```
GET    /users          - List all users
POST   /users          - Create a new user
GET    /users/123      - Get user with ID 123
PUT    /users/123      - Replace user 123
PATCH  /users/123      - Update user 123
DELETE /users/123      - Delete user 123
```

**Statelessness**: Each request contains all information needed to process it. The server maintains no session state between requests.

**Resource Representation**: Resources are transferred in representations—typically JSON containing the resource's data and possibly links to related resources (HATEOAS).

**HTTP Semantics**: REST leverages HTTP semantics properly: GET is idempotent and cacheable, POST creates resources, PUT replaces, DELETE removes, etc.

**Beyond REST**: Other API styles exist:
- **GraphQL**: Query language allowing clients to request exactly the data they need
- **gRPC**: High-performance RPC framework using Protocol Buffers
- **Webhooks**: Event-driven callbacks rather than request-response
- **WebSockets**: Bidirectional persistent connections for real-time data

## Practical Applications

**Third-Party Integrations**: Most modern services expose APIs for integration. Payment processing (Stripe), mapping (Mapbox), communication (Twilio), and countless other services are API-first.

**Microservices Architecture**: Large applications are decomposed into services that communicate via internal APIs. This enables independent scaling and deployment of components.

**AI Agent Tool Use**: AI agents interact with external systems through APIs. The agent determines which API to call, formats the request, interprets the response, and incorporates it into reasoning.

**Mobile Applications**: Mobile apps are essentially thin clients—their functionality comes from backend APIs. This separation enables consistent experiences across platforms.

**Internal Tooling**: Internal teams expose APIs for their services, enabling other teams to build on their work without tight coupling.

## Examples

```python
# Example: Python client for a REST API
import requests

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get_user(self, user_id: int) -> dict:
        response = self.session.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    def list_users(self, page: int = 1, per_page: int = 20) -> dict:
        response = self.session.get(
            f"{self.base_url}/users",
            params={'page': page, 'per_page': per_page}
        )
        response.raise_for_status()
        return response.json()
    
    def create_user(self, name: str, email: str) -> dict:
        response = self.session.post(
            f"{self.base_url}/users",
            json={'name': name, 'email': email}
        )
        response.raise_for_status()
        return response.json()
    
    def update_user(self, user_id: int, **fields) -> dict:
        response = self.session.patch(
            f"{self.base_url}/users/{user_id}",
            json=fields
        )
        response.raise_for_status()
        return response.json()

# Usage
client = APIClient("https://api.example.com", api_key="your-api-key")
user = client.get_user(123)
print(user['name'])

new_user = client.create_user(name="Alice", email="alice@example.com")
client.update_user(new_user['id'], name="Alice Smith")
```

```bash
# Example: Making API requests with curl
# GET request
curl -X GET "https://api.example.com/users/123" \
  -H "Authorization: Bearer $API_KEY"

# POST request with JSON body
curl -X POST "https://api.example.com/users" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "email": "bob@example.com"}'

# Handling pagination
curl -X GET "https://api.example.com/users?page=2&per_page=50" \
  -H "Authorization: Bearer $API_KEY"
```

**API Error Response Format**:
```json
{
  "error": {
    "code": "user_not_found",
    "message": "No user with ID 123 exists",
    "status": 404,
    "details": {
      "requested_id": 123,
      "available_at": "/users?page=1"
    }
  }
}
```

## Related Concepts

- [[rest-api]] — REST architectural style for APIs
- [[http]] — Underlying protocol for web APIs
- [[webhooks]] — Event-driven callback pattern
- [[graphql]] — Alternative query-based API approach
- [[OAuth-2.0]] — Common authorization framework for APIs
- [[jwt]] — Token format for API authentication
- [[api-gateway]] — Central entry point for API management
- [[rate-limiting]] — Controlling API usage frequency

## Further Reading

- [REST API Tutorial](https://restfulapi.net/) — Comprehensive REST concepts
- [API Design Guide](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design) — Microsoft best practices
- [JSON:API Specification](https://jsonapi.org/) — Standard format for APIs
- [OpenAPI Initiative](https://www.openapis.org/) — API description standard

## Personal Notes

I've built and consumed many APIs over the years. Good API design is hard—naming endpoints, structuring responses, handling errors, versioning without breaking clients. I've come to appreciate the value of REST's resource-oriented thinking, but GraphQL solves real problems when clients need flexible data shapes. The HTTP basics are non-negotiable to understand before diving into "higher-level" API concepts. One thing I wish more APIs did: provide SDKs in multiple languages and comprehensive sandboxes for testing. Stripe and Twilio set the bar here. The AI agent angle is interesting—when agents call APIs, we need to think about how they understand error responses and decide when to retry.
