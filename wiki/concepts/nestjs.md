---
title: "Nestjs"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nodejs, backend, framework, typescript, api, microservices]
---

# Nestjs

## Overview

NestJS is a progressive Node.js framework for building efficient, scalable, and maintainable server-side applications. Created by Kamil Myśliwiec and first released in 2017, NestJS takes inspiration from Angular's architecture—relying heavily on decorators, dependency injection, and modular organization—while adapting these patterns for server-side development. The framework runs on TypeScript by default, though plain JavaScript remains compatible. Its opinionated structure makes it particularly well-suited for building enterprise-grade REST APIs, GraphQL services, WebSocket applications, and microservices architectures.

The framework positions itself as the evolution of Express, adding architectural constraints and conventions that large teams need while preserving Node.js's characteristic speed and flexibility. Unlike Express or Fastify, which provide minimal middleware scaffolding, NestJS offers an integrated solution with built-in support for authentication, validation, caching, logging, and async operations. This reduces boilerplate and enforces consistency across projects, though it introduces a steeper initial learning curve.

## Key Concepts

**Modules** are the fundamental organizational unit in NestJS. Each application consists of one root module (typically `AppModule`) that imports child modules, creating a dependency graph. A module is a class decorated with `@Module()` that declares its controllers, providers, and imported modules. This structure enforces separation of concerns—related business logic, persistence, and external integrations cluster within a single module rather than scattered across files.

**Controllers** handle incoming requests and return responses to the client. Decorated with `@Controller()`, they define route paths and delegate to provider methods for business logic. Method handlers are decorated with HTTP verb decorators (`@Get()`, `@Post()`, `@Put()`, `@Delete()`) to map to specific endpoints. Controllers remain thin—delegating work to injected services rather than containing business logic themselves.

**Providers** (also called Services) are classes annotated with `@Injectable()` that encapsulate business logic, data access, and external service communication. They inject other providers through constructor parameters, leveraging NestJS's built-in dependency injection container. Providers are singletons by default, ensuring a single instance serves all requests—useful for caching and maintaining stateful data.

**Dependency Injection** is foundational to NestJS's architecture. The framework's inversion of control container automatically resolves and injects dependencies, following the strategy pattern where the framework manages object lifecycle. Constructor injection is the primary mechanism, though property injection is supported for specific cases. This design enables loose coupling—classes depend on abstractions (interfaces) rather than concrete implementations.

## How It Works

NestJS sits atop Express (or optionally Fastify) as an HTTP server adapter, wrapping the underlying platform with a structured application framework. When a request arrives, the router maps it to the appropriate controller method based on route definitions. Before the handler executes, a pipeline of middleware, guards, interceptors, and pipes process the request—enabling cross-cutting concerns like authentication, logging, validation, and transformation to execute consistently.

Guards determine whether a request should proceed, typically checking for valid authentication or appropriate permissions. Pipes transform and validate input data, converting raw request payloads into strongly-typed DTOs with automatic validation against schemas. Interceptors wrap the request-response cycle, enabling response mapping, caching, and error handling. Exception filters provide centralized error processing, ensuring consistent error responses regardless of where exceptions originate.

The module system compiles into a dependency graph that NestJS uses to bootstrap the application. The `main.ts` file typically creates the application instance, applies global middleware and pipes, and starts listening. During bootstrap, the framework resolves all dependency chains, throws errors for missing dependencies, and configures the middleware pipeline.

## Practical Applications

**REST APIs** are the most common NestJS use case. The framework's @Body, @Query, and @Param decorators extract request data, while class-validator and class-transformer provide declarative validation and transformation. Swagger documentation auto-generates from decorators, providing interactive API exploration. Guards handle authentication (JWT, OAuth), while interceptors handle response serialization.

**Microservices** leverage NestJS's transport layer abstraction to communicate via TCP, Redis pub/sub, gRPC, or message brokers like RabbitMQ. The @MessagePattern decorator designates handlers for specific message types, while controllers use @Client() proxies to invoke remote services. This enables a hybrid architecture where some services expose HTTP APIs while others communicate exclusively via messages.

**GraphQL APIs** use the @Resolver decorator to define query and mutation handlers. NestJS integrates with Apollo Server, accepting schema-first or code-first approaches. The resolver hierarchy mirrors the module structure, with DataLoader integration preventing N+1 query problems. Subscriptions enable real-time updates over WebSocket.

## Examples

A minimal NestJS controller demonstrating REST patterns:

```typescript
import { Controller, Get, Post, Body, Param, UseGuards } from '@nestjs/common';
import { AppService } from './app.service';
import { CreateUserDto } from './dto/create-user.dto';
import { JwtAuthGuard } from './auth/jwt-auth.guard';

@Controller('users')
export class UsersController {
  constructor(private readonly appService: AppService) {}

  @UseGuards(JwtAuthGuard)
  @Get()
  findAll() {
    return this.appService.getUsers();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.appService.getUserById(id);
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.appService.createUser(createUserDto);
  }
}
```

This controller defines a nested resource with authentication-protected routes, parameter extraction, and body parsing.

## Related Concepts

- [[Node.js]] - The JavaScript runtime NestJS runs on
- [[TypeScript]] - The primary language for NestJS development
- [[Express]] - The underlying HTTP framework NestJS often uses
- [[Dependency Injection]] - Core architectural pattern
- [[Microservices]] - Architecture style NestJS supports

## Further Reading

- [NestJS Documentation](https://docs.nestjs.com/)
- [NestJS GitHub Repository](https://github.com/nestjs/nest)
- [Angular Architecture Patterns Applied to Node.js (NestJS Blog)](https://nestjs.com/blog/)

## Personal Notes

NestJS's steep learning curve pays off for larger teams where consistent structure matters more than flexibility. The CLI (nest new, nest generate) accelerates scaffolding significantly. For microservices specifically, NestJS's abstraction over transport layers simplifies switching between RabbitMQ and gRPC without rewriting business logic. Consider starting with Fastify adapter for performance-critical APIs, but be aware that some community modules assume Express semantics.
