---
title: "Active Record"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, orm, database, ruby-on-rails]
---

# Active Record

## Overview

Active Record is a foundational design pattern in software engineering that represents database tables as classes and database rows as instances of those classes. This pattern, coined by Martin Fowler in his 2003 book "Patterns of Enterprise Application Architecture," provides an object-oriented interface for relational databases, allowing developers to manipulate data without writing raw SQL queries. The pattern is named for the fact that objects carry both data (attributes) and behavior (methods), with the record being "active" within the domain model.

The Active Record pattern is the cornerstone of popular web frameworks like Ruby on Rails, where it is implemented as the `ActiveRecord::Base` class. However, the pattern itself is framework-agnostic and has been implemented across virtually all programming languages and platforms, from Django's ORM in Python to Laravel's Eloquent in PHP.

## Key Concepts

The Active Record pattern revolves around several core principles that distinguish it from other ORM approaches:

**Domain Logic Mapping**: Each Active Record class directly corresponds to a database table. The class name maps to the table name (typically pluralized), and class attributes map to table columns. This one-to-one mapping makes the mental model intuitive—working with records feels like working with ordinary objects.

**CRUD Operations**: Active Record objects inherently know how to create, read, update, and delete themselves from the database. This encapsulation means you call `record.save()` rather than constructing an INSERT statement.

**Validation**: Active Record implementations typically include validation helpers that run before records are persisted, ensuring data integrity at the application level.

**Associations**: The pattern supports relationship management through methods like `has_many`, `belongs_to`, and `has_and_belongs_to_many`, automatically handling foreign keys and join tables.

## How It Works

When you define an Active Record class, the framework uses introspection to discover the table schema and dynamically generates attribute methods for each column. Under the hood, the pattern employs the Table Data Gateway pattern, where a single instance handles SQL operations for a entire table.

```ruby
class User < ActiveRecord::Base
  validates :email, presence: true, uniqueness: true
  has_many :orders
end

user = User.create(name: "Alice", email: "alice@example.com")
user.orders.create(product: "Widget")
```

When `User.create` is called, the framework builds an INSERT statement from the attributes, executes it against the database, and returns a populated User instance. Queries return collections of these instances, each wrapping a database row.

## Practical Applications

Active Record is ideal for applications where the domain model closely mirrors the database schema—typically CRUD-heavy applications like content management systems, e-commerce platforms, and administrative dashboards. Its simplicity makes it excellent for rapid prototyping and smaller projects where the productivity gains outweigh potential performance limitations.

The pattern shines in [[Domain-Driven Design]] contexts where the domain model should be rich and expressive, not buried under repository implementations.

## Examples

Consider a blog application where posts belong to authors:

```ruby
class Author < ActiveRecord::Base
  has_many :posts

  def publish_draft_titles
    posts.where(status: 'draft').pluck(:title)
  end
end

author = Author.find_by(name: "Jane Austen")
author.posts.each { |post| post.publish! }
```

## Related Concepts

- [[Object-Relational Mapping]] - The broader category of techniques for bridging object-oriented systems and relational databases
- [[Data Mapper Pattern]] - An alternative ORM approach where objects and database schemas are independent
- [[Ruby on Rails]] - The framework that popularized the Active Record implementation
- [[Database Transactions]] - How Active Record ensures data consistency
- [[SQL Injection Prevention]] - How parameterized queries in Active Record protect against attacks

## Further Reading

- Martin Fowler's "Patterns of Enterprise Application Architecture" - The original source of the Active Record pattern
- "Agile Web Development with Rails" - Comprehensive Rails/ActiveRecord guide

## Personal Notes

Active Record's convenience comes with trade-offs. For large-scale systems with complex domain logic, the pattern can lead to "fat models" that violate the Single Responsibility Principle. In those cases, consider combining Active Record with the [[Service Layer Pattern]] to encapsulate business logic outside of model classes. The pattern remains my go-to choice for greenfield projects where database schema is still evolving.
