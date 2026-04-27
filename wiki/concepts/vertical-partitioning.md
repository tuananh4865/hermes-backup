---
title: "Vertical Partitioning"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, partitioning, schema-design, performance, database-design]
---

# Vertical Partitioning

## Overview

Vertical partitioning is a database design technique that divides a table's columns into separate partitions, placing infrequently accessed or large data types onto different storage media or even separate database instances. Unlike [[Horizontal Partitioning]] (which splits rows), vertical partitioning splits columns—keeping related, frequently accessed fields together while isolating bulky or rarely queried data. This reduces I/O for typical queries since applications read only the data they actually need.

The canonical example is splitting a `users` table: basic profile fields (id, username, email, created_at) stay in a "hot" partition optimized for fast reads, while profile images, bio text, or JSON preferences move to a separate "cold" partition. Queries that only need user identity and email never load the large blob data, dramatically reducing disk reads and memory consumption.

Vertical partitioning predates modern distributed databases but remains relevant in [[Sharding]] strategies, [[NoSQL]] data modeling, and performance optimization for both relational and document databases. It's particularly important in [[Column-Oriented Databases]] where entire columns are stored contiguously for analytics workloads.

## Key Concepts

**Normalized vs Denormalized Partitioning** — Vertical partitioning can mirror database normalization (extracting repeating groups into separate tables) or denormalize intentionally (splitting a heavily accessed table to reduce row width). The key difference from normalization is that vertical partitions typically remain tightly coupled at the application layer and may be co-located on the same database server.

**Column Families** — In [[NoSQL]] databases like [[Cassandra]] or [[HBase]], vertical partitioning is expressed through column families. Related columns are grouped together, and each column family is stored separately. This allows frequently accessed columns to be read without touching large text or blob columns in other families.

**Storage Tiering** — Vertical partitions can be placed on different storage media. Hot data (frequently accessed) goes on fast SSDs; cold data (archives, logs, old documents) on cheaper spinning disks or object storage. This is a form of [[Caching]] at the storage level.

**Sparse Columns** — Some columns contain NULL for most rows (e.g., a `middle_name` column). Storing these in a separate partition avoids wasting space on null values in the main table. Columnar databases compress sparse columns extremely well.

**Wide Columns** — The opposite extreme: tables with hundreds of optional columns, most of which are null for any given row. Wide column stores (Cassandra, HBase, [[Google Bigtable]]) model this naturally as column families, effectively implementing vertical partitioning as a core architectural pattern.

**JOIN Avoidance** — Vertical partitioning across separate tables can introduce cross-partition queries that require [[Join]] operations. Careful design keeps related data co-located in the same partition, or denormalizes to eliminate joins at the cost of update complexity.

## How It Works

In a relational database, vertical partitioning is implemented by splitting a single table into multiple tables with a shared primary key:

```sql
-- Original table (before vertical partitioning)
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  username VARCHAR(50),
  email VARCHAR(255),
  avatar_url VARCHAR(500),
  bio TEXT,
  preferences JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- After vertical partitioning: hot data (frequently accessed)
CREATE TABLE users_profile (
  id BIGINT PRIMARY KEY,
  username VARCHAR(50),
  email VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Cold data (large or infrequently accessed)
CREATE TABLE users_details (
  id BIGINT PRIMARY KEY REFERENCES users_profile(id),
  avatar_url VARCHAR(500),
  bio TEXT,
  preferences JSON
);
```

When the application queries user data, it either:
1. Queries only `users_profile` for basic information
2. JOINs `users_profile` and `users_details` when full data is needed
3. Lazy-loads `users_details` only when a user views a profile page

The database may store partitions on different physical media:

```text
Table: users
├── Partition: users_profile (hot)     → SSD storage, replicated 3x
│   └── Columns: id, username, email, timestamps
└── Partition: users_details (cold)    → Spinning disk, replicated 2x
    └── Columns: avatar_url, bio, preferences
```

## Practical Applications

- **User profile systems** — As described above, separating lightweight identity data from bulky profile content (photos, long bios, JSON settings) dramatically improves query performance for the common case (listing usernames and emails).
- **Time-series data** — Separating metric values (float arrays) from metadata (tags, timestamps) allows querying metadata without loading large value arrays. This is standard practice in [[Time-Series Database]] design.
- **E-commerce product catalogs** — Product name, price, and SKU go in a fast-access partition; long descriptions, specifications, and images in a separate partition loaded only on detail pages.
- **Log and event data** — Separating fixed-structure log fields (timestamp, level, source) from variable-length payload text enables efficient querying without loading full message bodies.
- **Compliance and data retention** — Personally identifiable information (PII) may be legally required to be stored separately with stricter access controls, more encryption, and different retention policies.

## Examples

**Cassandra Column Families** — Cassandra's architecture is fundamentally based on vertical partitioning. A table definition in Cassandra is actually a column family:

```sql
CREATE TABLE users (
  user_id uuid PRIMARY KEY,
  username text,
  email text,
  created_at timestamp
) WITH comment = 'User profile - frequently accessed';
```

For the details, a separate column family:
```sql
CREATE TABLE user_details (
  user_id uuid PRIMARY KEY,
  avatar blob,
  bio text,
  preferences map<text, text>
) WITH comment = 'User details - loaded on demand';
```

**PostgreSQL Column Storage** — PostgreSQL's `ALTER TABLE ... SET TABLESPACE` can move specific columns to different storage. PostgreSQL 11+ also supports `ALTER TABLE ... DETACH PARTITION` for true vertical splits:

```sql
-- Detach large columns into separate tables
CREATE TABLE users_details (LIKE users INCLUDING ALL);
ALTER TABLE users_details ADD COLUMN avatar BYTEA, ADD COLUMN bio TEXT;
INSERT INTO users_details SELECT id, avatar, bio FROM users;
ALTER TABLE users DROP COLUMN avatar, DROP COLUMN bio;
```

**MongoDB Document Design** — While MongoDB stores documents (not columns), vertical partitioning in MongoDB means splitting one collection into multiple collections with explicit references:

```javascript
// users collection (lean)
{ _id: ObjectId, username: "alice", email: "alice@example.com" }

// user_details collection (separate, loaded on demand)
{ _id: ObjectId, user_id: ObjectId, avatar: Buffer, bio: "..." }
```

## Related Concepts

- [[Horizontal Partitioning]] — Splitting rows (contrast with splitting columns)
- [[Sharding]] — Horizontal partitioning across database instances
- [[Database Normalization]] — Structuring data to reduce redundancy
- [[Denormalization]] — Intentionally adding redundancy for read performance
- [[Column-Oriented Database]] — Storage layout optimized for column access
- [[NoSQL]] — Databases that often implement vertical partitioning as a core pattern
- [[Cassandra]] — Wide column store with explicit column family support
- [[Join]] — Cross-partition queries that vertical partitioning may introduce

## Further Reading

- "SQL Performance Explained" by Winand Marcus — Covers column-oriented storage and partition pruning.
- "Bigtable: A Distributed Storage System for Structured Data" — Google's paper on wide column stores.
- PostgreSQL Documentation on Table Partitioning — Modern approaches to vertical and horizontal partitioning.
- "Schema Design for Time Series Data" — How time-series databases use vertical partitioning patterns.

## Personal Notes

Vertical partitioning is often overlooked in favor of horizontal partitioning (sharding) when scaling, but it's frequently the higher-leverage optimization for real-world workloads. The gains from not reading 500KB of avatar data when listing 100 users add up quickly. The main danger is over-fragmenting—there becomes a combinatorial explosion of partitions that complicates application code. I aim for at most 2-3 partitions per table: hot vs. cold data, or small frequently-joined fields vs. bulky rarely-needed fields. Also consider whether the database already handles this internally through columnar storage or compression before manually partitioning.
