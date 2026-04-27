---
title: API Versioning
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [api-versioning, api-design, versioning, breaking-changes, rest-api, backward-compatibility]
---

## Overview

API Versioning is the practice of managing changes to an API over time while maintaining backward compatibility for existing clients. When an API is published and external developers or internal services begin building on top of it, the API provider faces a fundamental tension: the need to improve, fix, and extend the API conflicts with the need to avoid breaking existing integrations. API versioning provides a structured mechanism for introducing breaking changes, phasing out old functionality, and giving clients control over when they adopt new API behavior — without requiring all clients to upgrade simultaneously.

The core principle underlying all API versioning strategies is that an API is a contract. Once published and consumed, the API provider commits to maintaining that contract for some defined period. When a change cannot be made backward-compatible, the provider must either version the API (creating a new contract) or accept that existing clients will break. Versioning enables evolution while honoring that commitment.

API changes broadly fall into two categories. **Non-breaking changes** (also called additive or backward-compatible changes) include adding new optional fields to responses, adding new optional parameters to requests, adding new endpoints, and adding new enum values. These changes do not require a version bump because existing clients continue to function correctly. **Breaking changes** include removing or renaming fields, changing field types, changing the semantics of existing parameters, removing endpoints, and changing required parameters. Breaking changes require either a new API version or careful coordination with existing clients.

## Key Concepts

**API Lifecycle** — APIs move through stages: alpha (experimental, may break freely), beta (stable enough to test, changes announced), GA (general availability, backward compatibility enforced), and deprecated (will be removed, clients should migrate). Versioning enables clean transitions through this lifecycle.

**Version Identification** — A version identifier appears in the API contract and tells clients which contract they are using. Common formats include semantic version-like numbers (`v1`, `v2`, `v3`), calendar dates (`2026-01-01`), and codenames (`falcon`, `horizon`). The key is that the identifier is stable and meaningful to clients.

**Deprecation Policy** — A clear deprecation policy defines how long clients have to migrate after a version or feature is deprecated. Common policies include "minimum 12 months notice for breaking changes" (Stripe follows this), "deprecated versions live for 6 months after successor is available," or "no guarantees." Publishing a deprecation policy builds client trust.

**Changelog** — A running log of changes per version is essential. Each version's changelog should document what changed since the previous version, what is newly deprecated, and what breaking changes were introduced. This becomes the migration guide for clients upgrading.

**Pagination and Filtering Parameters** — When designing v1 of an API, decisions about pagination (page-based vs. cursor-based) and response envelope format (data array with metadata vs. linked HAL format) are already versioning decisions, because changing these in a future version would be a breaking change for existing clients.

## Common Versioning Strategies

**URL Path Versioning** embeds the version in the URL path:
```
GET /v1/users/123
GET /v2/users/123
```
This is the most common and transparent approach. Clients see the version in every request, making it self-documenting. The major drawback is that it feels less "clean" architecturally because the resource URL includes a version segment.

**Header Versioning** places the version in an HTTP header:
```
GET /users/123 HTTP/1.1
Accept: application/vnd.example.v2+json
```
This keeps URLs clean and resource-oriented. The drawback is that versions are invisible in casual debugging and require client library support to manage automatically.

**Query String Versioning** passes the version as a URL parameter:
```
GET /users/123?version=2
```
Simple to implement but pollutes the URL with a parameter that is not really a resource identifier. Generally discouraged for production APIs.

**Content Negotiation** uses the Accept header with a custom media type:
```
Accept: application/vnd.example.api.v2+json
```
More formally correct but cryptic for developers and poorly supported by debugging tools.

The industry consensus strongly favors URL path versioning for [[REST API|REST APIs]] due to its transparency, debuggability, and simplicity.

## How It Works

In practice, implementing API versioning involves several architectural decisions and operational practices.

First, the API surface must be clearly delineated per version. In a code repository, this typically means either maintaining separate route handler modules per version (`/v1/users.js`, `/v2/users.js`) or using a routing layer that dispatches to versioned handlers based on the version identifier. Many teams maintain separate deployed services per major API version, while others run a single service that multiplexes based on the incoming request's version.

```javascript
// Express.js routing example with URL path versioning
const express = require('express');
const app = express();

// v1 routes
app.get('/v1/users/:id', (req, res) => {
  res.json({
    id: req.params.id,
    name: 'Alice',
    // v1 response shape — flat, minimal fields
  });
});

// v2 routes — same resource, richer response shape
app.get('/v2/users/:id', (req, res) => {
  res.json({
    id: req.params.id,
    name: 'Alice',
    email: 'alice@example.com',       // new field
    created_at: '2024-01-15T00:00:00Z', // new field
    preferences: {                    // new nested structure
      theme: 'dark',
      notifications: true
    }
  });
});
```

Second, a mechanism for sunsetting old versions must be defined and enforced. This means setting a firm date when a version will stop being served, communicating that date well in advance (typically 6–12 months), and monitoring which clients are still on old versions before taking them offline.

Third, teams must establish a process for what constitutes a breaking vs. non-breaking change. This is surprisingly nuanced: removing an optional field from a response is technically non-breaking, but it may break clients that deserialize the response into typed objects without ignoring unknown fields. Adding a new required parameter is breaking. Changing a field name is always breaking. Having a written policy prevents disputes and surprises.

**Feature Flags** — Some teams use feature flags instead of version bumps for incremental rollouts. A feature flag enables a new behavior for a subset of users or requests without creating a new API version. This is not versioning per se but a complementary practice for safely rolling out changes to API behavior.

## Practical Applications

**Major API Providers** — Stripe, GitHub, Twilio, and AWS all maintain multiple active API versions simultaneously. Stripe famously maintains backward compatibility for years and provides migration guides for each version upgrade. Stripe's deprecation policy guarantees a minimum of three years between deprecation notice and shutdown.

**Internal API Platforms** — Large organizations with internal API platforms use versioning to allow multiple teams (consumer teams) to upgrade their API integrations on their own schedule rather than all at once with a new release. This decouples producer and consumer release cycles.

**Mobile Apps** — Mobile applications cannot be forced to update immediately when a server-side API changes. By maintaining multiple API versions, backend teams can support both the old app version and the new app version simultaneously, buying time for gradual app store rollout.

**Microservice Evolution** — In microservices architectures, API versioning at the gateway level allows individual services to evolve their internal APIs without requiring coordinated updates across all dependent services.

## Examples

GitHub's API versioning is a widely studied example. GitHub's REST API uses URL path versioning (`/v3`, `/v4` for GraphQL) and maintains comprehensive migration documentation. When GitHub deprecated `v3` in favor of `v4`, they provided a full migration guide, maintained `v3` for years, and provided tooling to help clients identify which version they were using.

Stripe's approach uses URL path versioning (`/v1`, `/v2`, `/v3`) and provides individual resource versioning for fine-grained changes. Stripe also pioneered the practice of embedding version information in API response headers (`Stripe-Version: 2024-04-10`), which tells clients exactly which API contract was applied to a particular response — useful for debugging and for testing migrations.

## Related Concepts

- [[REST API]] — The architectural context where versioning is commonly applied
- [[API Design]] — The broader practice that includes versioning decisions
- [[OpenAPI Specification]] — Specifying API versions in OAS documents
- [[Breaking Changes]] — Understanding what constitutes a breaking change
- [[API Documentation]] — Documenting version-specific behavior
- [[Deprecation]] — The practice of announcing end-of-life for API versions
- [[Microservices]] — Architectural pattern where versioning enables independent service evolution

## Further Reading

- "YouTube API versioning: lessons learned" — Google's comprehensive write-up of their versioning strategy
- Stripe API Versioning Guide — industry-standard example of versioning policy documentation
- "API Evolution" by Steve Klabnik — influential essay on RESTful versioning without version URLs (and the counterarguments)
- "RESTful Web APIs" by Richardson, Amundsen, and Ruby — Chapter on versioning strategies

## Personal Notes

The versioning strategy matters far less than having a clear, documented policy and enforcing it consistently. URL path versioning (`/v1/`, `/v2/`) is my default recommendation — it is the most transparent, easiest to debug, easiest to route at the infrastructure level, and easiest for clients to reason about. Whatever strategy you choose, publish your deprecation timeline in writing before you need it. Clients who have invested in an integration need time to plan and execute upgrades. And remember: every breaking change you avoid is a version bump you don't need to manage.
