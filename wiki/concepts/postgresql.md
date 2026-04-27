---
title: PostgreSQL
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [postgresql, database, sql, backend]
---

## Overview

PostgreSQL is a powerful, open-source object-relational database management system (ORDBMS) known for its robustness, extensibility, and standards compliance. Originally developed at the University of California, Berkeley in 1986, PostgreSQL has evolved into one of the most advanced relational databases available today, supporting both SQL (relational) and JSON (document-oriented) data models. It runs on all major operating systems including Linux, macOS, and Windows, making it a versatile choice for applications of any scale.

PostgreSQL follows the client-server model where database clients connect to a server process to execute queries and manage data. Its architecture is MVCC-based (Multi-Version Concurrency Control), which allows multiple transactions to occur simultaneously without locking conflicts, significantly improving throughput in high-concurrency environments.

## Key Features

PostgreSQL provides full ACID (Atomicity, Consistency, Isolation, Durability) transaction support, ensuring that database operations complete reliably even in the event of system failures. Every query executes within a transaction context, whether explicitly defined or implicit, guaranteeing data integrity.

The database offers extensive data type support beyond traditional relational types. PostgreSQL natively supports JSON, JSONB, HSTORE (key-value stores), XML, arrays, and custom types through its type system. The JSONB format stores JSON data in a decomposed binary format with indexing support, enabling efficient querying of nested document structures without sacrificing the ability to use traditional SQL joins.

PostgreSQL includes a sophisticated full-text search engine that allows natural language querying of text content. It supports stemming, ranking, highlighting, and multilingual search without requiring external search infrastructure. Combined with tsvector and tsquery types, developers can implement powerful search functionality directly within the database.

Additional notable features include: Foreign Data Wrappers (FDW) for accessing external data sources, Window Functions for analytical queries, Common Table Expressions (CTEs) with recursive support, Point-in-Time Recovery (PITR) for granular backup restoration, Logical Replication for flexible data distribution, and Table Inheritance for object-oriented database design patterns.

## Extensions

PostgreSQL's extensibility is one of its defining characteristics. Extensions are loadable modules that add functionality without modifying the core database code. Popular extensions include:

PostGIS — adds geospatial capabilities, enabling location-aware queries and geographic information system (GIS) applications.

pgvector — provides vector similarity search capabilities for machine learning applications, supporting embedding storage and efficient nearest-neighbor queries.

pg_stat_statements — tracks query execution statistics to identify performance bottlenecks.

pg_partman — automates table partitioning management for large datasets.

pg_trgm — enables trigram-based fuzzy matching and similarity searches.

The PostgreSQL extension ecosystem is vast, with hundreds of community-contributed extensions available for specialized use cases ranging from time-series data to graph traversal.

## Related

[[SQL]] | [[MySQL]] | [[MongoDB]] | [[Database]] | [[ACID]] | [[NoSQL]] | [[Database Index]] | [[PostGIS]]
