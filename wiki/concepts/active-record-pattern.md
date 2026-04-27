---
title: "Active Record Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-pattern, orm, persistence, architecture, database]
---

# Active Record Pattern

## Overview

The Active Record pattern is a design pattern introduced by Martin Fowler in his book *Patterns of Enterprise Application Architecture* (2002). In this pattern, a single class represents both the domain logic and the persistence logic for a database table row. An `ActiveRecord` object wraps a database row, exposes the row's columns as object attributes, and provides class-level methods for querying and manipulating records—all within the same abstraction.

The defining characteristic of Active Record is that the class itself is responsible for both business logic and database operations. When you create a `User` object and call `.save()`, the object knows how to insert itself into the database. When you call `User.find_by(email: "alice@example.com")`, the class constructs and executes the appropriate SQL query and returns a populated `User` instance. This is in contrast to the [[object-relational-mapping|Data Mapper]] pattern, where separate mapper classes handle persistence while domain objects remain ignorant of the database.

## Key Concepts

**Entity-Ratabase Mapping**

Each Active Record class directly corresponds to a database table. Instance variables map to columns. The class manages its own lifecycle—`new` creates an in-memory object, `save` persists it, `destroy` removes it.

**CRUD Operations**

Active Record provides Create, Read, Update, Delete operations as methods on the class and its instances. `User.create(name: "Alice")`, `user.update(email: "new@example.com")`, `user.destroy` are idiomatic usages.

**Lifecycle Callbacks**

The pattern supports hooks that fire at various points in an object's lifecycle: before/after `save`, `create`, `update`, `destroy`, `validation`. These allow developers to inject behavior—sending notifications, encrypting fields, computing derived values—without scattering logic across the codebase.

**Association Management**

Active Record classes declare relationships using keywords: `has_many`, `belongs_to`, `has_one`, `many_to_many`. The framework generates the appropriate SQL joins and manages foreign keys automatically.

**Dirty Tracking**

Before saving, the object tracks which fields have changed since loading, so only modified columns are included in the `UPDATE` statement rather than the entire row.

## How It Works

```ruby
# Ruby on Rails Active Record example
class User < ApplicationRecord
  has_many :orders, dependent: :destroy

  before_save :normalize_email

  validates :email, presence: true, uniqueness: true

  private

  def normalize_email
    self.email = email.downcase.strip
  end
end

# Usage
user = User.find_by(email: "alice@example.com")
user.orders.create!(product: "Widget", amount: 29.99)
user.update!(name: "Alice Smith")
```

```python
# Django ORM (similar Active Record-style) example
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
```

In the Rails example, `User` inherits from `ApplicationRecord`, which provides the Active Record behavior. The `has_many` declaration wires up the `orders` relationship. The `before_save` callback runs `normalize_email` automatically on every save.

Internally, the framework translates these method calls into SQL. `user.orders.create!(...)` executes an `INSERT INTO orders ...` with `user_id` set automatically. `user.update!(...)` generates an `UPDATE users SET ... WHERE id = ?` with only the changed columns.

## Practical Applications

The Active Record pattern is the foundation of model-layer logic in Ruby on Rails, Django, Laravel (Eloquent), and many other web frameworks. It excels in CRUD-heavy applications where the domain model closely mirrors the database schema—content management systems, e-commerce backends, admin panels.

It is less suited to complex domains with rich business logic that doesn't map directly to CRUD operations, where the anemic domain model anti-pattern becomes a liability. For those cases, [[hexagonal-architecture]] with a separate [[object-relational-mapping|Data Mapper]] layer is often preferable.

## Examples

- **Rails ActiveRecord** — The canonical implementation that popularized the pattern in the web development world
- **Django ORM** — While Django calls its models "Django's ORM," they follow Active Record conventions closely
- **Eloquent (Laravel)** — PHP's Active Record implementation with a beautiful, expressive query builder
- **Spring Data JPA** — Java's approach, which mixes JPA annotations with repository interfaces (partially Active Record in flavor)

## Related Concepts

- [[object-relational-mapping]] — Active Record is one specific ORM pattern; ORM is the broader category
- [[hexagonal-architecture]] — Often contrasted with Active Record; ports and adapters isolate domain logic from persistence
- [[saga-pattern]] — Distributed transactions often need to coordinate across multiple Active Record models
- [[web-api]] — Active Record models are commonly serialized and returned via REST endpoints
- [[authentication]] — User and session models in web frameworks are typically implemented as Active Record classes

## Further Reading

- Martin Fowler, *Patterns of Enterprise Application Architecture* — the original Active Record pattern description
- "Get Your ORM in the Wrong Hands" — blog post on when Active Record becomes a liability
- Ruby on Rails Active Record Documentation — comprehensive reference

## Personal Notes

I've built many applications with Rails Active Record and it truly shines for greenfield CRUD apps. The moment your domain logic outgrows simple "load from DB, modify, save" cycles, you start fighting it. I've found that mixing service objects with Active Record models—keeping models for persistence and validation while pushing business rules into dedicated classes—helps a lot without abandoning the pattern entirely. Also, never underestimate the power of `includes` (eager loading) to prevent N+1 queries in list views.
