---
title: "HBase"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nosql, database, hadoop, distributed, big-data]
---

# HBase

## Overview

HBase is an open-source, distributed, versioned, column-oriented NoSQL database built on top of the Hadoop Distributed File System (HDFS). It is modeled after Google's Bigtable paper and is designed to host large tables with billions of rows and millions of columns on commodity hardware. HBase provides random, real-time read/write access to data, contrasting with HDFS's batch-processing nature. It excels at sparse data storage, where most column values in a row may be null, and maintains efficient access via column families that group related columns together. Originally developed by the Apache Software Foundation as part of the Apache Hadoop project, HBase is now a top-level project used by companies processing massive-scale data, including Facebook (for messaging), Yahoo, Twitter, and Adobe. Its data model is inspired by Bigtable: tables are sorted maps partitioned by row key, with data organized into column families and individual columns indexed by timestamps for versioning.

## Key Concepts

**Column Families**: Data in HBase is organized into column families—groups of columns that share storage, compression, and retention settings. All column family members are stored together on disk, making queries against a column family efficient. Tables must define column families at creation time, though columns can be added dynamically.

**Row Key**: The primary index for HBase tables. Row keys are byte arrays sorted lexicographically, meaning scans of contiguous key ranges are efficient. Row key design is critical for data distribution (using row key ranges to partition across region servers) and access patterns.

**Regions**: Tables are horizontally partitioned into regions, each containing a contiguous sorted range of rows. Region servers host and serve regions, automatically splitting or merging as data grows or shrinks. This automatic sharding is a core scalability feature.

**WAL (Write-Ahead Log)**: Before any write is applied to the in-memory MemStore, it is appended to the WAL for durability. If a region server crashes before the MemStore is flushed to disk, the WAL can replay the lost updates.

**MemStore**: An in-memory write buffer. Writes are first recorded in the MemStore, then periodically flushed to HDFS as immutable HFiles. Each column family has its own MemStore.

**HFiles**: The persistent storage format on HDFS. HFiles are immutable once written, and are organized by column family. Compaction processes merge smaller HFiles into larger ones to optimize read performance.

## How It Works

HBase's architecture consists of a master server that coordinates cluster operations and multiple region servers that host data:

1. **Write Path**: When a client writes a row, the data is first written to the WAL, then appended to the MemStore for the appropriate column family. Once the MemStore fills, it is flushed to disk as an HFile.

2. **Read Path**: Reads are served by checking the MemStore first, then scanning HFiles on disk. Bloom filters and block caches optimize read performance.

3. **Region Splitting**: When a region grows beyond a configurable size threshold (default 10GB), HBase automatically splits it into two smaller regions, distributing load across servers.

4. **Compactions**: Minor compactions merge small HFiles; major compactions merge all HFiles for a column family and delete expired tombstones marking deleted rows.

```java
// Example: Writing and reading from HBase using Java API
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;

Configuration config = HBaseConfiguration.create();
Connection connection = ConnectionFactory.createConnection(config);
Table table = connection.getTable(TableName.valueOf("users"));

// Write
Put put = new Put(Bytes.toBytes("user123"));
put.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("name"), Bytes.toBytes("Alice"));
put.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("email"), Bytes.toBytes("alice@example.com"));
table.put(put);

// Read
Get get = new Get(Bytes.toBytes("user123"));
get.addColumn(Bytes.toBytes("profile"), Bytes.toBytes("name"));
Result result = table.get(get);
byte[] name = result.getValue(Bytes.toBytes("profile"), Bytes.toBytes("name"));
```

## Practical Applications

HBase is purpose-built for high-throughput, low-latency workloads on very large datasets:

**Time-Series Data**: IoT sensor readings, stock ticks, and application metrics are naturally organized by timestamp and benefit from HBase's append-only storage and efficient range scans.

**User Profile Storage**: User attributes, preferences, and session data can be stored with user IDs as row keys for instant retrieval at scale.

**Messaging Systems**: Facebook Messenger originally used HBase to store message history, benefiting from its ability to handle sequential writes and random reads.

** Analytical Queries**: Combined with Apache Phoenix or Apache Drill, HBase serves as a backend for interactive SQL queries on big data.

## Examples

Creating an HBase table with two column families using the HBase shell:

```bash
hbase shell

# Create table with column families
create 'users', 'profile', 'activity'

# Insert data
put 'users', 'user001', 'profile:name', 'Alice'
put 'users', 'user001', 'profile:email', 'alice@example.com'
put 'users', 'user001', 'activity:logins', '42'

# Scan entire table
scan 'users'

# Get specific row
get 'users', 'user001'

# Get specific column
get 'users', 'user001', 'profile:name'
```

## Related Concepts

- [[Hadoop]] - The ecosystem HBase operates within
- [[HDFS]] - The distributed filesystem HBase stores data on
- [[NoSQL]] - The category of databases HBase belongs to
- [[Bigtable]] - Google's original column-oriented database that inspired HBase
- [[Apache Phoenix]] - SQL layer on top of HBase
- [[Distributed Databases]] - The broader class of scalable database systems
