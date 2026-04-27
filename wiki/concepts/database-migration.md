---
title: Database Migration
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, migrations, schema, version-control, SQL, DevOps]
---

## Overview

Database migration (also called schema migration or database schema evolution) is the process of modifying the structure of a database over time—adding or removing tables and columns, changing data types, splitting or merging tables, creating or dropping indexes, and more—while preserving existing data and maintaining application compatibility. As applications evolve, their data models must evolve too, and database migrations provide a controlled, repeatable, and often reversible way to make those changes.

Migrations sit at the intersection of database engineering, application development, and DevOps practices. They require careful planning because a poorly executed migration can cause data loss, application downtime, or corruption. Modern teams treat database schema as code: version-controlled, reviewed via pull requests, tested in staging, and deployed through CI/CD pipelines. This approach, sometimes called **database-as-code**, contrasts with the older practice of manually applying changes through a DBA console.

## Key Concepts

**Migration Files** are the atomic units of schema change. Each migration has an **up** operation (apply the change) and ideally a **down** operation (revert the change). Migrations are numbered or timestamped sequentially, ensuring they apply in a consistent order across all environments. For example, a Rails migration might be named `20260413120000_add_indexes_to_users.rb`; a Flyway migration might be `V4__create_orders_table.sql`.

**State-Based vs. Migration-Based** are two approaches to database deployment:

- **Migration-based** (most common): You write explicit migration scripts that describe each step of the change. Tools include Flyway, Liquibase, Rails ActiveRecord Migrations, Alembic (Python), and goose (Go).
- **State-based**: You define the desired final state of the schema (often as a SQL DDL file or model definition), and a tool computes the diff to generate migration scripts automatically. Prisma Migrate and SQLMesh use this approach.

**Zero-Downtime Migrations** are migrations that can be applied to a production database without taking the application offline. This requires careful techniques: adding a column as nullable first, deploying the application code that writes to both old and new columns, backfilling data, then finally making the column non-nullable and removing the old column. Tools like GitHub's `gh-ost` (online schema changes for MySQL) and `pt-online-schema-change` automate this process.

**Seed Data** refers to initial or reference data that an application needs to function (country codes, permission roles, feature flags). Seed data is separate from migration scripts and should be managed carefully—some teams put seeds in migrations for initial setup, while others maintain a separate seed management process.

## How It Works

A typical migration workflow with Flyway (Java/SQL ecosystem):

```bash
# Directory structure expected by Flyway
# db/migration/
#   V1__create_users_table.sql
#   V2__add_email_index.sql
#   V3__add_roles_table.sql

# Flyway automatically applies pending migrations in version order
flyway -url=jdbc:mysql://localhost:3306/mydb -user=root migrate

# Check current migration status
flyway info

# Revert to a specific version (applies down migrations)
flyway undo -target=2

# Repair (cleans up corrupted checksum metadata)
flyway repair
```

A typical Alembic (Python/SQLAlchemy) migration:

```bash
# Auto-generate a migration from model changes
alembic revision --autogenerate -m "add user preferences table"

# Apply migrations
alembic upgrade head

# Show current version
alembic current

# Show migration history
alembic history
```

The auto-generated migration file contains both `upgrade()` and `downgrade()` functions:

```python
def upgrade():
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(length=20), nullable=True),
        sa.Column('language', sa.String(length=5), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('user_preferences')
```

## Practical Applications

**Expanding a Column** is a common zero-downtime migration pattern. Suppose you need to change a `VARCHAR(50)` column to `VARCHAR(255)`:

1. Write a migration to add a new temporary column (`email_temp`).
2. Deploy code that writes to both `email` and `email_temp`.
3. Backfill `email_temp` from `email`.
4. Deploy code that reads from `email_temp`.
5. Drop the `email` column and rename `email_temp` to `email`.

**Adding a NOT NULL Column** requires careful handling: you must provide a default value, backfill existing rows, and ensure the application always provides the value going forward. Adding a NOT NULL constraint without a default on a large table can lock the table for minutes or hours—a production outage.

**Renaming a Column** is almost never zero-downtime compatible if you need to preserve both old and new column during the transition. The expand-contract pattern (add new column → dual-write → backfill → switch reads → drop old column) is the safest approach, taking weeks to months for large tables.

**Partitioning Large Tables** is a migration often done in stages to avoid locking. Tools like `gh-ost` can restructure large MySQL tables under active load.

## Examples

A complete SQL migration adding a table with a foreign key and an index:

```sql
-- V5__create_orders_table.sql (Flyway naming convention)

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for common query patterns (orders by user, orders by status)
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Comment for documentation
COMMENT ON TABLE orders IS 'Customer orders with line items stored separately';
COMMENT ON COLUMN orders.status IS 'pending, confirmed, shipped, delivered, cancelled';
```

## Related Concepts

- [[SQL]] — The language used to define and manipulate database schemas
- [[schema-design]] — Principles for designing database structures
- [[database-transactions]] — ACID guarantees that affect migration safety
- [[flyway]] — A popular SQL-based migration tool
- [[prisma]] — A state-based ORM with migration capabilities
- [[database-normalization]] — Principles for organizing relational data

## Further Reading

- Flyway's documentation at flywaydb.org — excellent getting started guide
- "Refactoring Databases" by Scott Ambler and Pramod Sadalage — classic on evolutionary database design
- GitHub's `gh-ost` project for MySQL online schema changes
- Shopify's "Migrating Millions of Rows" blog posts on large-scale migrations

## Personal Notes

The biggest mistake I've seen teams make is treating database changes as less risky than code changes. A bad deploy can be rolled back in seconds; a bad migration on a 100-million-row table can cause hours of downtime. I've adopted a strict rule: any migration that modifies a table with more than 1 million rows must be reviewed by someone who has run the same migration on a production-size data snapshot. I also keep a "migration runbook" document for each non-trivial migration, including the rollback procedure, estimated time, and the exact command to kill it if something goes wrong.
