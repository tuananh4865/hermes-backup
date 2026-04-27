---
title: "Fastify"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nodejs, javascript, web-framework, http, api]
---

# Fastify

Fastify is a modern, high-performance web framework for Node.js that emphasizes developer experience, schema validation, and raw speed. Created by Matteo Collina and others and first released in 2016, Fastify has rapidly gained popularity as an alternative to Express.js, offering significantly better throughput while maintaining a familiar, plugin-based architecture. The framework is designed around the principle that a web framework should be fast not just in execution, but in development velocity—providing helpful error messages, TypeScript support, and a cohesive plugin system that makes building web services enjoyable and maintainable.

## Overview

Fastify positions itself as a developer-friendly framework that doesn't sacrifice performance for ergonomics. The framework achieves remarkable benchmark results—often handling two to three times more requests per second than Express—through its unique architecture that minimizes overhead and maximizes efficiency. Fastify achieves this by using a两层路由 system where routes are compiled into a Radiate tree for fast lookup, avoiding the middleware chain that Express uses.

The framework is built around four core principles: least overhead (minimal memory and CPU usage), powerful plugin architecture (encapsulated and hierarchical), schema validation (JSON Schema support for request/response validation), and developer experience (helpful errors, TypeScript support, and sensible defaults). These principles guide every design decision and make Fastify particularly well-suited for building APIs, microservices, and serverless functions where performance and maintainability are both critical.

Fastify's plugin system is one of its most distinctive features. Plugins encapsulate functionality into reusable units that can declare their own dependencies, establish isolated contexts, and be composed together to build complex applications. This approach encourages code reuse and separation of concerns while preventing unintended interactions between plugins—a common source of bugs in Express applications.

## Key Concepts

Understanding Fastify requires grasping several key architectural concepts that differentiate it from other Node.js frameworks.

**Plugins** are the fundamental building blocks in Fastify. A plugin is a function that receives the Fastify instance and optional options, and registers routes, decorators, or hooks. Plugins create encapsulated contexts—changes made to the Fastify instance within a plugin are scoped to that plugin by default, preventing cross-plugin contamination. This encapsulation ensures that plugins are truly reusable and composable.

**Decorators** extend the Fastify instance with custom methods or properties. The `decorate` method adds instance-level functionality, while `decorateRequest` and `decorateReply` add properties to request and reply objects respectively. Decorators enable powerful patterns where plugins can add capabilities that subsequent plugins or routes can use.

**Schemas** in Fastify use JSON Schema to validate incoming requests and serialize outgoing responses. Fastify compiles schemas into highly optimized validation functions that run before route handlers execute, catching invalid input early and providing clear error messages. Schemas can validate query strings, URL parameters, request headers, and request bodies, providing comprehensive input validation.

**Hooks** provide lifecycle points where custom logic can execute—onRequest, preParsing, preValidation, preHandler, onResponse, and onSend hooks run at specific times during request processing. Hooks enable cross-cutting concerns like authentication, logging, and error handling to be implemented as reusable units.

## How It Works

Fastify's request lifecycle follows a carefully designed path optimized for performance while maintaining extensibility. When a request arrives, Fastify's router matches it against registered routes using a tree-based lookup algorithm that efficiently finds the correct handler. This lookup is O(log n) rather than iterating through middleware, providing consistent performance even with thousands of routes.

Once a route is matched, Fastify executes a series of hooks in order: onRequest, preParsing, preValidation, preHandler, and then the route handler. Each hook receives the request and reply objects and can either pass control to the next hook, terminate the request early by sending a response, or throw an error that triggers the error handling path.

Request validation happens early in this lifecycle using JSON Schema schemas compiled into fast functions. If validation fails, Fastify immediately returns a 400 Bad Request response with detailed information about what validation failed, without executing the route handler. This early rejection prevents malformed requests from consuming resources in business logic.

```javascript
// Example: Fastify server with plugins, schemas, and hooks
const fastify = require('fastify')({ logger: true });

// Register a plugin with encapsulation
fastify.register(async function databasePlugin(fastify, opts) {
  // Create a database connection - isolated to this plugin
  fastify.decorate('db', createDatabaseConnection(opts.connectionString));
  
  // Add a decorator other plugins can use
  fastify.decorateRequest('session', null);
});

// Define route with full schema validation
fastify.post('/users', {
  schema: {
    body: {
      type: 'object',
      required: ['email', 'password'],
      properties: {
        email: { type: 'string', format: 'email' },
        password: { type: 'string', minLength: 8 }
      }
    },
    response: {
      201: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          email: { type: 'string' }
        }
      }
    }
  },
  preHandler: async (request, reply) => {
    // Authentication check
    if (!request.headers.authorization) {
      throw { statusCode: 401, message: 'Unauthorized' };
    }
  }
}, async (request, reply) => {
  const { email, password } = request.body;
  const user = await fastify.db.createUser(email, password);
  reply.code(201).send({ id: user.id, email: user.email });
});

// Start server
const start = async () => {
  try {
    await fastify.listen({ port: 3000 });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};
start();
```

## Practical Applications

Fastify excels in scenarios where performance is critical but developer experience shouldn't suffer. REST API development is the most common use case—Fastify's speed and low overhead make it ideal for high-traffic APIs, microservices, and serverless functions where every millisecond and memory allocation matters. Companies building real-time systems, data ingestion pipelines, and high-frequency trading backends have adopted Fastify for its consistent low-latency performance.

The framework's strong TypeScript support makes it popular for teams building type-safe applications. Fastify includes official TypeScript types and provides excellent type inference for route handlers, schemas, and configuration. Combined with tools like tRPC, Fastify enables end-to-end type safety from database to API to client.

Plugin ecosystem expansion has made Fastify suitable for diverse applications. The platform supports WebSocket connections, GraphQL queries, OpenAPI documentation generation, and authentication schemes through community and official plugins. This extensibility means teams can start with a minimal core and add capabilities as needed without the overhead of features they don't use.

Serverless deployments benefit particularly from Fastify's fast startup time and efficient request handling. In environments like AWS Lambda or Google Cloud Functions where cold starts and memory limits matter, Fastify's lightweight architecture performs better than heavier frameworks while providing a familiar API for developers.

## Examples

A practical Fastify example involves building a user authentication service with JWT tokens. The implementation uses a plugin to encapsulate database access, decorators to add user-related methods, and hooks to protect routes that require authentication. The schema validation ensures only properly formatted requests reach the route handlers, reducing error handling complexity in business logic.

Another example demonstrates building a file upload endpoint with streaming. Fastify's support for streams allows handling large files without loading them entirely into memory, making it suitable for media processing services. The route handler can pipe incoming file streams directly to storage services like S3 while providing immediate feedback to users about upload progress.

## Related Concepts

- [[Express.js]] - The most popular Node.js framework that Fastify often replaces
- [[Node.js]] - The JavaScript runtime Fastify runs on
- [[REST API]] - Common architecture pattern built with Fastify
- [[JSON Schema]] - Validation technology used by Fastify
- [[TypeScript]] - Typed superset of JavaScript with excellent Fastify support
- [[Microservices]] - Architecture style Fastify is well-suited for

## Further Reading

- Fastify Official Documentation - Comprehensive guides and API reference
- "Node.js Design Patterns" - Covers web frameworks and Fastify architecture
- Fastify Plugin Registry - Community plugins extending framework capabilities

## Personal Notes

Fastify represents a thoughtful approach to web framework design, prioritizing both runtime performance and developer experience rather than treating them as trade-offs. What stands out is how the plugin system encourages modularity—building an application as a composition of focused plugins leads to naturally testable and maintainable code. The schema validation integration feels particularly well-designed, catching invalid input at the framework level rather than requiring developers to write defensive checks in every handler. For teams coming from Express, Fastify offers a comfortable migration path with better performance and structure, making it easy to adopt incrementally. I recommend Fastify for any new Node.js API project where performance matters or where the team values maintainable code organization.
