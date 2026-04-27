---
title: "Object Relational Mapping"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [orm, database, persistence, sql, software-patterns]
---

# Object Relational Mapping

## Overview

Object-Relational Mapping (ORM) is a programming technique that bridges the gap between relational databases (which store data in tables with rows and columns) and object-oriented programming languages (which represent data as interconnected objects). Instead of writing raw SQL queries, developers interact with the database through code—creating, reading, updating, and deleting objects directly, while the ORM framework translates these operations into the appropriate SQL statements.

ORMs exist because relational databases and object-oriented languages have fundamentally different data models. A database organizes data in flat tables; objects in Python, Ruby, Java, or C# form rich graphs with inheritance, encapsulation, and references. The ORM layer mediates between these two worlds, letting developers work in the idiom of their language while still leveraging the power of SQL and relational algebra for data storage and querying.

## Key Concepts

**Entity and Model**

An entity (or model) is a programmatic representation of a database table. Each attribute of the entity maps to a column. For example, a `User` entity might have fields `id`, `email`, `created_at`. ORM frameworks provide conventions—often through class decorators or schema definitions—for specifying column types, constraints, relationships, and indexes.

**Relationship Mapping**

ORMs handle one-to-one, one-to-many, and many-to-many relationships between entities. A `User` might have a one-to-many relationship with `Order` objects, or a many-to-many relationship with `Product` through an associative table. These relationships are expressed in code through property declarations and translate into SQL `JOIN` queries or separate queries with relationship loading strategies.

**Unit of Work and Identity Map**

A sophisticated ORM tracks all changes made to objects within a "unit of work" and flushes them to the database in a single transaction, preventing inconsistent states. The identity map ensures that each database row is represented by a single in-memory object instance, avoiding duplicate objects for the same entity.

**Migration System**

Many ORMs include schema migration tools that evolve the database schema as the domain model changes. Migrations are versioned, reversible scripts that modify tables, columns, indexes, and constraints incrementally.

## How It Works

When a developer queries for entities, the ORM constructs and executes the appropriate SQL. Results are then mapped to instances of the entity classes, populating their fields from the result set. Lazy loading defers relationship fetching until accessed; eager loading fetches relationships upfront via `JOIN`s or sub-queries. Change tracking monitors modifications to loaded objects so the ORM can compute `UPDATE` statements on commit.

```python
# SQLAlchemy ORM example (Python)
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Integer)

    user = relationship("User", back_populates="orders")

# Usage
with Session(engine) as session:
    user = session.query(User).filter_by(email="alice@example.com").first()
    user.orders  # lazily loaded
```

## Practical Applications

ORMs are used in virtually every web application that uses a relational database. Web frameworks like Rails (ActiveRecord), Django (ORM), Laravel (Eloquent), and ASP.NET (Entity Framework) all ship with built-in ORMs. They're also critical in domain-driven design, where the domain model and persistence model are kept separate but synchronized through mapping layers.

## Examples

- **Hibernate** — The dominant Java ORM, providing JPA (Java Persistence API) implementation
- **SQLAlchemy** — Python ORM known for its compositional query API and flexibility
- **Active Record (Rails)** — Convention-over-configuration ORM built into Ruby on Rails
- **Entity Framework** — Microsoft's ORM for .NET, supporting both code-first and database-first approaches
- **Prisma** — Modern TypeScript ORM with a type-safe query builder and migrations

## Related Concepts

- [[active-record-pattern]] — The design pattern that inspired Rails' ActiveRecord ORM implementation
- [[web-api]] — ORMs often sit behind REST or GraphQL APIs that serve frontend clients
- [[authentication]] — User credentials and sessions are often stored and queried via ORM models
- [[json-schema]] — Schema definitions used by some ORMs for validation
- [[storage]] — ORM is a specific approach to data persistence within the broader storage landscape

## Further Reading

- "Patterns of Enterprise Application Architecture" by Martin Fowler — covers Identity Map, Unit of Work, Data Mapper
- SQLAlchemy Documentation — comprehensive reference for Python ORM concepts
- Hibernate ORM Documentation — Java persistence landscape

## Personal Notes

ORMs are powerful but can be a source of N+1 query problems if relationships are not properly loaded. Learning to inspect the generated SQL is essential—tools like Django's `queryset.query`, SQLAlchemy's echo flag, or Rails' `active_record.logger` are invaluable for performance tuning. Also, not every problem needs a relational database; some data is naturally document-shaped, graph-shaped, or key-value shaped, where an ORM would fight the natural model rather than help.
