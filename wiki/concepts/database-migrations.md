---
title: "Database Migrations"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, schema, migrations, devops, schema-management, version-control]
---

# Database Migrations

## Overview

Database migrations (also known as schema migrations or database schema migrations) are the practice of evolving a database's structure over time in a controlled, versioned, and repeatable manner. As applications evolve, their data models must change—new tables are added, columns are modified, indexes are created for performance, and legacy structures are deprecated. Database migrations provide a systematic framework for making these changes without data loss, service interruption, or inconsistency between the application code and the database schema.

Migrations emerged as a response to the challenges of managing database changes in teams and production environments. Without a structured approach, developers might apply manual changes to local databases that never get documented or replicated to other environments. Production changes might cause downtime if not carefully planned. Rollbacks become difficult or impossible when changes aren't tracked.

Modern database migration tools treat migrations as first-class citizens in the development workflow. Each migration is a discrete, atomic change that can be applied (migrate up) or reversed (migrate down/rollback). Migrations are stored in version control alongside application code, ensuring that the complete history of database changes is preserved and reproducible.

## Key Concepts

### Migration Files

A migration is typically represented as a pair of files—one for applying the change (up) and one for reversing it (down), or as a single file with both directions expressed. Migration frameworks have different conventions:

```sql
-- Example: Migration files in Rails-style naming
-- 20260413120000_add_users_table.sql (up)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- 20260413120000_add_users_table.sql (down)
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
```

```python
# Example: Migration in Alembic (SQLAlchemy)
# versions/001_add_users.py
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email', 'users')
    op.drop_table('users')
```

### Schema Versioning

Migration tools maintain a version table within the database itself that tracks which migrations have been applied. This allows the tool to determine which migrations need to run (those not yet applied) and in what order. Common tools include Flyway, Liquibase, Alembic (Python/SQLAlchemy), Rails ActiveRecord Migrations, and Prisma Migrate.

### Atomicity

Each migration should be atomic—either it fully succeeds or it fully fails. If a migration partially executes and then fails, the database should be returned to its previous state. Most migration tools handle this by wrapping each migration in a transaction (though this isn't always possible for certain operations like adding columns with concurrent constraints).

### Idempotency

Migration scripts should ideally be idempotent—running them multiple times should produce the same result as running them once. This prevents issues when migrations are accidentally run twice or when deployment pipelines retry operations.

## How It Works

The database migration workflow follows a structured process:

**1. Create Migration**
When a developer needs to change the database schema, they create a new migration file. The naming convention typically includes a timestamp or sequential version number to ensure ordering. The migration contains both the upgrade (apply) and downgrade (rollback) operations.

**2. Review and Test**
Migrations should go through code review like any other code change. Before applying to production, migrations are tested in development and staging environments. This includes verifying the migration itself works and that the application functions correctly with the new schema.

**3. Execution**
When deploying, the migration tool checks the current schema version in the database, compares it to the migration files in the codebase, and applies any pending migrations in order.

```bash
# Example: Running migrations with Flyway
$ flyway migrate

Flyway Community Edition 9.22.3 by Redgate
Database: jdbc:postgresql://localhost:5432/myapp (PostgreSQL 15.2)
Successfully applied 3 migrations (execution time 0.8s)
```

**4. Verification**
After migration completes, verify the expected schema changes are in place. This might include checking that new tables/columns exist, that indexes were created, or that data was transformed correctly.

**5. Rollback (if needed)**
If issues are discovered post-deployment, the migration can be reversed using the downgrade path. However, data-destructive migrations (DROP TABLE, ALTER TABLE DROP COLUMN) cannot always be safely rolled back since data may have been lost.

## Practical Applications

**Zero-Downtime Deployments**: Modern applications deploy frequently, often multiple times per day. Traditional "big bang" database changes that require exclusive locks cause unacceptable downtime. Migration strategies like expand-contract patterns (add new column → deploy new code → migrate data → drop old column) enable continuous deployment without maintenance windows.

**Blue-Green Deployments**: Two identical production environments are maintained. Database migrations run against both databases (or against a shared database before the cutover). Traffic switches from blue to green once everything is ready. If issues arise, traffic switches back to blue.

**Feature Flags Combined with Migrations**: Deploy a migration that adds a new column (nullable initially). Deploy code that writes to both old and new columns. Deploy code that reads only from new column. Backfill data. Make new column NOT NULL. This staged approach avoids locking operations.

**Cross-Database Compatibility**: When supporting multiple database backends (PostgreSQL, MySQL, SQLite), migrations must be written carefully to handle dialect differences. Some frameworks use abstraction layers; others maintain separate migration paths per database.

**Data Warehouse Evolution**: Data warehousing environments use migrations to evolve schemas for analytics—adding new tables for new data sources, modifying columns to accommodate new transformations, and maintaining compatibility with reporting tools.

## Examples

Consider evolving a simple blog application from version 1 to version 2:

**v1 Schema**:
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP
);
```

**Migration 1: Add author tracking**:
```sql
ALTER TABLE posts ADD COLUMN author_id INTEGER REFERENCES authors(id);
CREATE INDEX idx_posts_author ON posts(author_id);
```

**Migration 2: Add tags support**:
```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (post_id, tag_id)
);
```

**Migration 3: Denormalize for performance**:
```sql
ALTER TABLE posts ADD COLUMN tag_list VARCHAR(500);
UPDATE posts SET tag_list = (
    SELECT string_agg(t.name, ',')
    FROM post_tags pt JOIN tags t ON pt.tag_id = t.id
    WHERE pt.post_id = posts.id
);
CREATE INDEX idx_posts_tag_list ON posts USING gin(to_tsvector('english', tag_list));
```

Each migration is a discrete, reversible step that moves the schema from one well-defined state to another.

## Related Concepts

- [[Schema Design]] - The practice of structuring database tables and relationships
- [[Version Control]] - Storing migration files alongside application source code
- [[ci-cd-pipelines]] - Automating migration execution in deployment workflows
- [[Rollback Strategies]] - Techniques for recovering from failed migrations
- [[Flyway]] - Popular database migration tool
- [[Liquibase]] - Open-source database schema change management tool
- [[Schema Evolution]] - The broader concept of how database schemas change over time
- [[Data Integrity]] - Ensuring accuracy and consistency of data through schema constraints

## Further Reading

- "Database Migrations: The Lonely Way" — philosophical overview of why migrations matter
- Flyway Documentation — practical guide to database migration patterns
- "Migrating the Phoenix" — patterns for zero-downtime database migrations
- Martin Fowler's article on Evolutionary Database Design

## Personal Notes

Database migrations are often treated as an afterthought, but they're one of the most impactful DevOps practices. A team with good migration discipline can ship changes faster and with more confidence. A few lessons I've learned: always test migrations against a production-sized dataset in staging, never skip the rollback path even if you think you won't need it, and use the expand-contract pattern for any change that requires modifying a column rather than adding one. The biggest mistake is treating migrations as purely technical—when a migration takes 30 minutes in production due to table locks, the business impact is immediate and visible.
