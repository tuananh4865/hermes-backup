---
title: Prisma
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [prisma, orm, database, typescript]
---

# Prisma

## Overview

Prisma is a next-generation open-source [[ORM]] (Object-Relational Mapper) designed specifically for [[Node.js]] and [[TypeScript]] applications. Unlike traditional ORMs that rely on runtime query builders, Prisma takes a schema-first approach where developers define their database schema in a declarative configuration file called the Prisma Schema. From this schema, Prisma generates a fully type-safe database client that provides end-to-end type safety from the database to the application layer. Prisma supports PostgreSQL, MySQL, SQLite, MongoDB, and SQL Server, making it a versatile choice for projects ranging from small prototypes to production-grade applications.

## Key Features

### Type-Safe Queries

Prisma's most distinctive feature is its generated client that offers complete type safety. When you define your data model in the Prisma Schema, the Prisma Client is automatically generated with TypeScript types that match your schema exactly. This means the compiler catches errors before runtime, such as querying for a field that does not exist or passing incorrect types to a query. Autocomplete support in IDEs makes database interactions more productive and less error-prone.

### Migrations System

Prisma Migrate is a migration tool that manages database schema changes through version control. Instead of manually writing SQL migration files, developers modify their Prisma Schema and Prisma generates the corresponding migration files. This approach ensures that schema changes are tracked in [[git]], reviewed via pull requests, and applied consistently across different environments. The migration system supports incremental changes, rollbacks, and baseline migrations for existing databases.

### Prisma Schema

The Prisma Schema is the central configuration file that defines your data model, database connection, and generator settings. It uses its own modeling language called PSL (Prisma Schema Language) which is human-readable and intuitive. The schema supports relations between models, validation rules, default values, and database-specific features. Changes to the schema trigger the regeneration of the Prisma Client, keeping types in sync with the database structure.

## Comparison

Compared to other [[ORM]] solutions like [[TypeORM]], [[Sequelize]], or [[Drizzle]], Prisma stands out with its schema-first philosophy and type-safe query generation. [[TypeORM]] and [[Sequelize]] use the active record pattern where models carry both data and business logic, whereas Prisma separates the data layer from application logic. [[Drizzle]] is more lightweight and SQL-like compared to Prisma's higher-level abstraction. Prisma's learning curve is gentler than [[TypeORM]] due to its simpler configuration, but it may add slight overhead in very performance-critical scenarios where raw SQL queries would be more efficient.

## Related Concepts

- [[ORM]] — Object-Relational Mapping general concept
- [[TypeScript]] — Programming language Prisma targets
- [[Node.js]] — Runtime environment Prisma runs on
- [[database]] — General database concepts
- [[postgresql]] — Popular database supported by Prisma
- [[TypeORM]] — Alternative ORM for TypeScript
- [[Drizzle]] — Lightweight SQL-like ORM alternative
