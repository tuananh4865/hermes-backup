---
title: "SQLite"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [sqlite, database, sql, embedded]
---

# SQLite

## Overview

SQLite is a lightweight, embedded relational database engine that stores data in a single disk file. Unlike traditional client-server databases such as [[PostgreSQL]] or [[MySQL]], SQLite operates without a separate server process—it runs directly within the application. This makes it exceptionally well-suited for embedded systems, mobile applications, local development environments, and scenarios where simplicity and portability matter more than distributed scalability.

SQLite follows the [[ACID]] (Atomicity, Consistency, Isolation, Durability) properties, ensuring that database transactions are reliable even in the event of system crashes or power failures. The entire database resides in one file, typically using the `.db` or `.sqlite` extension, which can be easily copied, moved, or versioned like any other file.

## Key Features

**Serverless Architecture**: SQLite does not require a database server to run. The library is compiled into the application, and all database operations occur directly against the file system. This eliminates network overhead and simplifies deployment.

**Zero Configuration**: There is no configuration file to manage, no server to start, and no user accounts to set up. Simply create or open a database file and begin querying.

**ACID Transactions**: Full transaction support ensures data integrity. SQLite uses [[WAL]] (Write-Ahead Logging) mode by default in recent versions, allowing concurrent reads while maintaining write safety.

**Cross-Platform**: The single-file format works identically across operating systems—Windows, Linux, macOS, Android, and iOS all support SQLite without modification.

**Small Footprint**: The entire SQLite library is under 1MB, making it ideal for mobile devices and embedded environments with limited storage.

## Use Cases

**Mobile Applications**: SQLite is the primary database engine for [[Android]] and [[iOS]] apps. It handles local storage for contacts, messages, and app data on billions of devices.

**Embedded Systems**: IoT devices, set-top boxes, and automotive systems use SQLite for structured data storage without the complexity of running a database server.

**Testing and Development**: Developers frequently use SQLite for local testing because it requires no setup and mirrors production SQL semantics without the overhead of a full database server.

**Desktop Applications**: Applications like [[Firefox]], [[Chrome]], and [[skype]] use SQLite for local caching and configuration storage.

## Comparison

| Feature | SQLite | PostgreSQL | MySQL |
|---------|--------|------------|-------|
| Server Required | No | Yes | Yes |
| Concurrency | Single writer | Multi-writer | Multi-writer |
| Max Database Size | 281 TB | Unlimited | TB-level |
| Setup Complexity | None | High | Medium |
| Ideal Use | Embedded, local | Enterprise, distributed | Web applications |

SQLite excels in read-heavy, single-user scenarios but is not designed for high-concurrency client-server workloads where [[PostgreSQL]] or [[MySQL]] remain the standard choices.

## Related

- [[database]] — General database concepts
- [[PostgreSQL]] — Client-server relational database
- [[MySQL]] — Popular open-source database
- [[ACID]] — Transaction properties guarantee
- [[SQL]] — Query language used by SQLite
- [[embedded-systems]] — Related domain where SQLite thrives
