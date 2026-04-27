---
title: "Dynamodb"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, nosql, aws, key-value, serverless]
---

# DynamoDB

## Overview

Amazon DynamoDB is a fully managed NoSQL database service provided by Amazon Web Services. It offers single-digit millisecond latency at any scale by leveraging solid-state drives (SSDs) and distributes data across multiple facilities and servers automatically. DynamoDB was designed to handle high-throughput, mission-critical applications at massive scale, and it serves as the backbone for numerous AWS services and customer applications worldwide.

DynamoDB's data model is simple yet powerful: tables contain items, and items have attributes. Unlike traditional relational databases, DynamoDB is schema-less beyond the primary key definition—items in the same table can have completely different attributes. This flexibility makes it ideal for use cases where data structures evolve over time or where heterogeneous data needs to be stored efficiently.

The service offers two capacity modes: provisioned capacity, where you specify the read and write throughput you need, and on-demand capacity, where AWS automatically scales based on actual usage. This flexibility allows developers to optimize costs for predictable workloads or embrace serverless patterns for unpredictable traffic patterns.

## Key Concepts

**Tables, Items, and Attributes**: The core data structure in DynamoDB. A table is a collection of items, and each item is a collection of key-value pairs called attributes. Unlike rows in relational databases, items can have varying numbers of attributes.

**Primary Key**: Every DynamoDB table must have a primary key that uniquely identifies each item. DynamoDB supports two types of primary keys:
- **Partition Key (Simple Primary Key)**: A single attribute that determines the partition where the item is stored
- **Partition Key + Sort Key (Composite Primary Key)**: The combination allows multiple items with the same partition key, enabling hierarchical data organization

**Partitioning**: DynamoDB automatically partitions your data across multiple servers based on the partition key. The partition key value is hashed, and the result determines which partition stores the item. This hashing enables horizontal scaling and uniform data distribution.

**DynamoDB Streams**: A feature that captures item-level changes in a table, enabling event-driven architectures and real-time data processing pipelines.

## How It Works

DynamoDB stores data in partitions, with each partition containing items whose partition key hashes to the same value. The partition key hash function distributes items across partitions, ensuring that items with adjacent partition key values aren't stored together—a common misconception that can lead to performance issues.

When you perform a read or write operation, DynamoDB routes the request to the appropriate partition(s) based on the primary key. For queries with both partition and sort keys, DynamoDB can efficiently retrieve a range of items within a single partition.

DynamoDB replicates data synchronously across multiple Availability Zones within a region, providing high availability and durability. There's no mechanism for multi-region replication built into the core service (for that, you'd use Global Tables), but within a region, your data is automatically replicated.

```python
# Example: DynamoDB operations using boto3
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Put an item
table.put_item(
    Item={
        'user_id': '123',
        'name': 'Alice Smith',
        'email': 'alice@example.com',
        'orders': ['order-1', 'order-2']
    }
)

# Get an item
response = table.get_item(Key={'user_id': '123'})
item = response.get('Item')

# Query items with a sort key condition
response = table.query(
    KeyConditionExpression='user_id = :uid AND begins_with(order_date, :year)',
    ExpressionAttributeValues={
        ':uid': '123',
        ':year': '2024'
    }
)
```

DynamoDB's conditional writes enable powerful patterns: you can specify that an item should only be written if a condition is met (e.g., version number matches, attribute doesn't exist), preventing race conditions in distributed systems without requiring transactions.

## Practical Applications

DynamoDB excels in several scenarios:

**Web Applications**: Session storage, user profiles, and shopping carts benefit from DynamoDB's single-digit millisecond latency and automatic scaling. Netflix, Airbnb, and Samsung all use DynamoDB for core platform components.

**Gaming Backends**: Leaderboards, player state, and in-game inventory management require low-latency reads and writes at massive scale. DynamoDB handles spikes during game releases without manual intervention.

**Internet of Things (IoT)**: Time-series data from sensors can be stored efficiently using the partition key (device ID) and sort key (timestamp) pattern.

**Metadata and Configuration Stores**: Applications requiring fast access to configuration data, feature flags, or AB test parameters use DynamoDB for its simplicity and reliability.

## Examples

The single-table design pattern is a DynamoDB best practice where you store multiple entity types in one table using a composite primary key:

```python
# Single-table design pattern example
# PK (Partition Key) and SK (Sort Key) encode entity relationships

# User entity
{'PK': 'USER#123', 'SK': 'PROFILE', 'name': 'Alice', 'email': 'alice@example.com'}

# Order entity
{'PK': 'USER#123', 'SK': 'ORDER#2024-001', 'amount': 99.99, 'items': 3}

# Product entity
{'PK': 'PRODUCT#SKU-001', 'SK': 'METADATA', 'name': 'Widget', 'price': 29.99}

# Query all orders for a user
response = table.query(
    KeyConditionExpression='PK = :pk AND begins_with(SK, :prefix)',
    ExpressionAttributeValues={
        ':pk': 'USER#123',
        ':prefix': 'ORDER#'
    }
)
```

## Related Concepts

- [[NoSQL Databases]] - The category DynamoDB belongs to
- [[AWS]] - The cloud platform DynamoDB runs on
- [[Key-Value Store]] - DynamoDB as a key-value store
- [[CAP Theorem]] - Understanding DynamoDB's consistency tradeoffs
- [[Serverless]] - DynamoDB's fit in serverless architectures
- [[Consistent Hashing]] - The partitioning strategy underlying DynamoDB

## Further Reading

- Amazon DynamoDB Developer Guide - Official AWS documentation
- "Amazon DynamoDB: A Scalable, Predictably Performant, and NoSQL Database" (Selvaggio et al.) - AWS whitepaper
- Alex DeBrie's "The DynamoDB Book" - Comprehensive resource on data modeling

## Personal Notes

DynamoDB's single-table design pattern is powerful but requires careful upfront modeling. Unlike SQL databases where you can perform ad-hoc queries, DynamoDB demands that you know your access patterns before designing your table. The access patterns drive the key structure, not the entity relationships. This is a fundamental shift in thinking for developers coming from relational backgrounds.

Also remember that DynamoDB charges for reads and writes, not storage. This means your capacity unit calculations should focus on request volume, not data volume. On-demand capacity mode is excellent for unpredictable workloads but can be expensive for sustained high-throughput scenarios.
