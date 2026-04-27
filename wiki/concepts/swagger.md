---
title: Swagger
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [swagger, swagger-ui, api-tools, openapi, smartbear, api-documentation]
---

## Overview

Swagger is both the original name of what is now known as the [[OpenAPI Specification]] and a suite of open-source and commercial tools for [[API documentation|designing]], building, and documenting REST APIs. The Swagger project began in 2010 as an open-source framework created by Reverb Technologies (later SmartBear Software) and quickly became the most widely adopted tooling for API documentation. In 2015, SmartBear donated the Swagger Specification to the Linux Foundation's newly formed OpenAPI Initiative, at which point the specification was officially renamed the OpenAPI Specification. Despite this rename, "Swagger" persists colloquially as shorthand for the entire ecosystem — the tools, the community, and sometimes the specification itself.

Understanding Swagger requires distinguishing between three distinct but related things: the Swagger Specification (the original name for OpenAPI 2.0), the Swagger tooling ecosystem (Swagger UI, Swagger Editor, Swagger Codegen), and the broader Swagger brand/community. Today, SmartBear continues to maintain and commercialize the Swagger brand tools while the specification itself is governed by the OpenAPI Initiative.

## Key Concepts

**Swagger UI** is an open-source, HTML/JavaScript-based interactive documentation viewer that renders OpenAPI (and legacy Swagger 2.0) specifications as browsable, try-it-out web pages. When you open an API's documentation and can make live requests directly from the browser, you are almost certainly using Swagger UI. It remains the most recognizable piece of the Swagger ecosystem and is deployed by thousands of organizations. Swagger UI reads the specification file (YAML or JSON) and generates an interface that lists all endpoints, shows schemas, and allows developers to fill in parameters and execute real API calls without writing any code.

**Swagger Editor** is a browser-based YAML editor specifically designed for writing OpenAPI/Swagger specifications. It provides real-time validation, error highlighting, and a live preview of the rendered documentation. It is an excellent tool for getting started with API design and for prototyping API contracts before implementation begins.

**Swagger Codegen** (now largely replaced by the community-maintained openapi-generator) is a templating engine that reads an OpenAPI spec and generates client SDKs in dozens of programming languages, server stubs for various frameworks, and API documentation in multiple formats. Codegen dramatically accelerated API adoption by removing the boilerplate of writing HTTP client code from scratch.

**SmartBear SwaggerHub** is the commercial platform offering from the company behind Swagger. It provides a hosted collaborative environment for designing, versioning, and publishing OpenAPI specifications, with features like mocking, access control, and integration with CI/CD pipelines. SwaggerHub is particularly valuable for teams that want the Swagger tooling ecosystem without self-hosting infrastructure.

## How It Works

Swagger tools operate on the principle of a machine-readable API contract as the single source of truth. The typical development workflow using Swagger tools looks like this:

First, an API designer or developer writes the API specification in YAML or JSON using Swagger Editor (or any text editor). The editor validates the spec in real-time, catching syntax errors and flagging semantic issues like missing required fields or invalid schema references.

Once the spec is written, Swagger UI reads it and generates the interactive documentation portal. Developers exploring the API can see every endpoint, understand its parameters and request bodies, view example responses, and execute live test calls — all from within the browser. This "try it out" capability is Swagger UI's most impactful feature, as it collapses the time between "reading about an API" and "successfully calling an API."

```javascript
// Swagger UI embedding example (standalone HTML)
const ui = SwaggerUIBundle({
  url: "https://petstore.swagger.io/v1/swagger.json",
  dom_id: '#swagger-ui',
  presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
  ],
  layout: "BaseLayout",
  deepLinking: true
});
ui.initOAuth({
  clientId: "your-client-id",
  scopes: "openid profile email"
});
```

Swagger Codegen consumes the spec and applies mustache templates to generate artifacts. A typical generation command looks like:

```bash
# Generate a Python client SDK from an OpenAPI spec
swagger-codegen generate \
  -i openapi.yaml \
  -l python \
  -o ./generated/python-client
```

Modern teams often prefer openapi-generator (the community fork of swagger-codegen) for its more active maintenance and broader language support.

## Practical Applications

**Interactive API Documentation** is Swagger's most visible application. By deploying Swagger UI for a public or internal API, teams provide developers with self-service, exploratory access to the API. This reduces support burden and accelerates integration. Stripe's API documentation, Twilio's docs, and hundreds of other major API providers use Swagger UI or derivatives.

**API Design and Contract-First Development** — Teams practicing contract-first API design use Swagger Editor to design the API surface before writing any implementation code. This allows stakeholders, product managers, and frontend teams to review and approve the API contract early. The implementation then follows the contract, ensuring alignment.

**SDK Generation for API Consumers** — Instead of manually maintaining client libraries, API providers run Swagger Codegen or openapi-generator in their CI/CD pipeline to produce and publish SDKs for every supported language whenever the spec changes.

**Internal and External Developer Portals** — Modern developer portals (like Stoplight, Rapido, or custom Docusaurus-based portals) often embed Swagger UI or its components to provide the interactive reference documentation layer.

## Relationship to OpenAPI

The distinction between Swagger and OpenAPI is important but often blurred in practice. OpenAPI is the specification — the JSON/YAML format that describes an API. Swagger is the tooling ecosystem built around that specification (originally built for Swagger 2.0, now supporting OpenAPI 3.x). When the specification was donated to the OpenAPI Initiative and renamed, SmartBear retained the Swagger brand for its commercial tools while the specification itself became an open industry standard.

This means:
- An API described with OpenAPI 3.1 is still often said to have "Swagger documentation"
- Swagger UI renders OpenAPI specs, not just legacy Swagger 2.0 specs
- The terms are not interchangeable (specification vs. tooling) but the overlap is enormous

## Related Concepts

- [[OpenAPI Specification]] — The formal standard that succeeded the Swagger Specification
- [[API Documentation]] — The broader discipline of documenting APIs that Swagger tools enable
- [[REST API]] — The API style that Swagger/Swagger UI specializes in documenting
- [[openapi-generator]] — The community-maintained successor to Swagger Codegen
- [[SwaggerHub]] — SmartBear's commercial platform for API design and hosting
- [[Contract Testing]] — Testing practice complementary to Swagger-generated documentation

## Further Reading

- [Swagger.io](https://swagger.io/) — Official SmartBear Swagger website with docs and tools
- [Swagger UI on GitHub](https://github.com/swagger-api/swagger-ui) — Open-source documentation viewer
- [Swagger Editor](https://editor.swagger.io/) — Free online editor for OpenAPI/Swagger specs
- openapi-generator on GitHub — Community SDK/server generator (recommended over legacy swagger-codegen)

## Personal Notes

The Swagger → OpenAPI transition created lasting confusion in the community because the tooling and the specification are both called Swagger in everyday speech. When evaluating tools, always clarify whether a "Swagger" tool supports OpenAPI 3.x (current standard) or only Swagger 2.0 (legacy). Most modern tooling supports both, but legacy systems still exist. The Swagger UI/Swagger Editor ecosystem remains excellent and actively maintained — they are not deprecated despite the rename. The quality of these free, open-source tools has set a high bar that commercial documentation platforms still compete against.
