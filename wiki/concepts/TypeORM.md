---
title: TypeORM
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [typeorm, orm, typescript, database]
---

# TypeORM

## Overview

TypeORM is a popular [[Object-Relational Mapping]] (ORM) library for TypeScript and JavaScript applications. It enables developers to work with relational databases using an object-oriented paradigm, bridging the gap between typed application code and raw SQL queries. TypeORM supports a wide range of database engines including PostgreSQL, MySQL, SQLite, MariaDB, Oracle, and Microsoft SQL Server, making it a versatile choice for projects that may need to switch database providers.

Originally inspired by the Entity Framework and Hibernate frameworks from the .NET and Java ecosystems, TypeORM was designed specifically to address the needs of TypeScript developers who wanted strong typing and decorator-based configuration for their database operations. It follows the Active Record and Data Mapper patterns, giving developers the flexibility to choose the approach that best fits their architectural preferences.

TypeORM has become a cornerstone of the [[Node.js]] ecosystem, particularly for applications built with frameworks like [[NestJS]], where it is often the default ORM choice. Its emphasis on TypeScript compatibility, combined with a rich feature set, has made it one of the most widely adopted ORMs in the JavaScript community.

## Features

TypeORM provides an extensive set of features that streamline database interactions in modern applications.

**Decorators** are central to TypeORM's configuration model. Entity classes are defined using decorators like @Entity, @Column, @PrimaryColumn, and @PrimaryGeneratedColumn to map TypeScript classes to database tables. Relationship decorators such as @OneToOne, @OneToMany, @ManyToOne, and @ManyToMany define associations between entities. This decorator-based approach provides compile-time type checking and IDE autocomplete support, reducing runtime errors and improving developer productivity.

**Migrations** in TypeORM provide a version-controlled way to manage database schema changes. The migration system automatically generates migration files based on entity changes, and developers can run or revert migrations via the TypeORM CLI. This ensures that database schemas evolve consistently across different environments and team members.

**Active Record Pattern** allows entities to have static methods for querying and instance methods for saving, updating, or deleting individual records. This pattern is intuitive for simpler applications where models directly contain their data access logic.

**Data Mapper Pattern** separates entities from repositories that handle data operations. Entities become plain objects without database logic, while dedicated repository classes manage queries and persistence. This separation is preferred in larger applications with complex business logic.

**Additional features** include support for transactions with automatic rollback, eager and lazy loading of relations, a powerful query builder for constructing complex queries, and integration with [[GraphQL]] through the TypeGraphQL library.

## Comparison

TypeORM, [[Sequelize]], and [[Drizzle]] are three prominent ORMs in the Node.js ecosystem, each with distinct philosophies and trade-offs.

TypeORM distinguishes itself with its comprehensive decorator-based configuration and extensive feature set. It offers built-in migration support, multiple database driver support, and both Active Record and Data Mapper patterns. However, TypeORM has been criticized for performance overhead, particularly in large-scale applications where query execution can be slower compared to more lightweight alternatives.

[[Sequelize]] is a mature, promise-based ORM with a longer history and broader community support. It uses a define-based approach rather than decorators, though newer versions support some decorator usage. Sequelize excels in scenarios requiring complex associations and includes built-in support for read replicas and logical deletes. Its drawback is a heavier abstraction layer that can make generated SQL less transparent.

[[Drizzle]] represents a newer generation of ORMs that prioritizes performance and SQL transparency. It uses a schema-first approach with TypeScript schema definitions and generates SQL queries that remain readable and predictable. Drizzle is significantly faster than both TypeORM and Sequelize in benchmark tests, but it offers fewer high-level abstractions and requires more manual work for complex scenarios like migrations.

## Related

- [[Object-Relational Mapping]] - The general concept of mapping object-oriented models to relational databases
- [[Sequelize]] - Another popular JavaScript ORM with promise-based API
- [[Drizzle]] - A lightweight, SQL-like ORM focused on performance
- [[NestJS]] - A progressive Node.js framework that integrates well with TypeORM
- [[TypeScript]] - The superset of JavaScript that provides typing features used by TypeORM
- [[Database Migrations]] - The practice of version-controlling database schema changes
- [[Active Record Pattern]] - The design pattern where entities contain both data and data access logic
- [[Data Mapper Pattern]] - The design pattern that separates entities from persistence logic
