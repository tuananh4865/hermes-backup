---
title: "Data Mapper"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [architecture, design-patterns, orm, database, persistence]
---

# Data Mapper

## Overview

The Data Mapper pattern is an architectural pattern that handles bidirectional transfer of data between an in-memory object representation and a relational database. As one of the patterns described in Martin Fowler's "Patterns of Enterprise Application Architecture," Data Mapper separates domain logic from database concerns, keeping the object model completely ignorant of how it persists.

In this pattern, a mapper class (often called a Data Access Object or DAO) handles the translation between relational rows and domain entities. When you load an entity from the database, the mapper populates its fields from the result set. When you save, the mapper generates the appropriate INSERT or UPDATE statement. The domain objects remain "POCOs"—Plain Old CLR/Cocoa Objects—unaware that persistence exists.

This isolation provides enormous flexibility. You can test domain logic without a database connection, change your persistence layer without touching business code, and maintain multiple representations of the same data across different contexts.

## Key Concepts

### The Impedance Mismatch

Relational databases organize data in tables with fixed schemas and foreign key relationships. Object-oriented programs organize data in interconnected object graphs with inheritance, encapsulation, and arbitrary references. This fundamental mismatch—called object-relational impedance mismatch—makes data mapping complex.

Data Mapper acknowledges this mismatch and provides a dedicated layer to bridge it. Unlike [[active-record]], where domain objects carry their own persistence logic, Data Mapper externalizes that responsibility.

### Unit of Work

The [[unit-of-work]] pattern often accompanies Data Mapper. It tracks changes to domain objects within a business transaction and commits them all at once. This batching reduces database round-trips and ensures consistency—if any change fails, all roll back together.

### Identity Map

An identity map ensures each database row corresponds to exactly one in-memory object. Without this guarantee, two code paths might load the same record twice, creating two distinct objects where changes to one don't reflect in the other.

## How It Works

A typical Data Mapper implementation follows this flow:

```python
# Domain object - completely persistence-ignorant
class User:
    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name
    
    def rename(self, new_name):
        self.name = new_name
        # No knowledge of persistence

# Data Mapper - handles all database interaction
class UserMapper:
    def find(self, user_id):
        row = self.db.query("SELECT * FROM users WHERE id = ?", user_id)
        if not row:
            return None
        return User(row['id'], row['email'], row['name'])
    
    def insert(self, user):
        self.db.execute(
            "INSERT INTO users (email, name) VALUES (?, ?)",
            user.email, user.name
        )
        user.id = self.db.last_insert_id()
    
    def update(self, user):
        self.db.execute(
            "UPDATE users SET email = ?, name = ? WHERE id = ?",
            user.email, user.name, user.id
        )
```

The service layer coordinates mappers:

```python
class UserService:
    def __init__(self, mapper):
        self.mapper = mapper
    
    def register_user(self, email, name):
        user = User(None, email, name)
        self.mapper.insert(user)
        return user
```

## Practical Applications

### Enterprise Applications

Large applications with complex domain logic benefit most from Data Mapper. The [[domain-driven-design]] philosophy explicitly recommends Data Mapper over Active Record for entities with rich behavior. Banks, ERPs, and healthcare systems typically use this pattern to keep business rules isolated and testable.

### ORM Frameworks

Most [[object-relational-mapping]] frameworks implement Data Mapper internally. Hibernate (Java), Entity Framework (C#), and SQLAlchemy (Python) provide mapper functionality, though they often expose Active Record-like interfaces for convenience.

### Microservices

Each service can have its own Data Mapper, persistence technology, and database schema. This [[microservices-architecture]] allows services to evolve independently—service A might use PostgreSQL while service B uses MongoDB.

## Related Concepts

- [[object-relational-mapping]] — Broader category containing Data Mapper
- [[active-record]] — Alternative pattern where models know their persistence
- [[unit-of-work]] — Companion pattern for transactional consistency
- [[domain-driven-design]] — Methodology that pairs well with Data Mapper
- [[repository-pattern]] — Similar abstraction that hides data source details

## Further Reading

- [Patterns of Enterprise Application Architecture: Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html) — Fowler's original description
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) — Eric Evans on keeping domain models pure
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html) — Python implementation of Data Mapper

## Personal Notes

I've seen teams overengineer persistence layers with elaborate mapper hierarchies when simpler approaches suffice. Data Mapper shines when domain complexity genuinely justifies the abstraction. For CRUD applications with anemic domain models, Active Record or even raw SQL is more appropriate. The pattern's complexity should match the problem's inherent complexity—not the perceived complexity of the team.
