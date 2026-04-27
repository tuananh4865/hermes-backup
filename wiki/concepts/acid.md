---
title: ACID
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [database, transactions, acid, relational-database, data-integrity]
---

# ACID

## Overview

ACID is an acronym representing the four fundamental properties that guarantee reliable processing of database transactions: Atomicity, Consistency, Isolation, and Durability. These properties were defined by computer scientist Jim Gray in the 1980s and have become the foundational contract that relational database management systems (RDBMS) use to ensure data remains correct and consistent even in the face of hardware failures, system crashes, concurrent access, and other error conditions. When a database claims to support ACID transactions, it provides strong guarantees about what happens when data is written—guarantees that simplify application development by allowing developers to treat complex operations as single, indivisible units.

The ACID model stands in contrast to eventually consistent systems like those built on NoSQL databases or distributed systems, where perfect consistency may be temporarily sacrificed for availability and partition tolerance (as described by the CAP theorem). For applications where data correctness is paramount—financial systems, inventory management, booking systems—ACID transactions provide the safety net that prevents data corruption and integrity violations.

## Key Concepts

**Atomicity** ensures that a transaction completes in an all-or-nothing fashion. If any part of a transaction fails, the entire transaction is rolled back as if it never happened. This prevents "partial updates" where some data changes succeed while others fail, leaving the database in an inconsistent state. For example, when transferring money between bank accounts, atomicity guarantees that either both the debit and credit operations complete together, or neither occurs.

**Consistency** guarantees that a transaction transforms the database from one valid state to another, never violating any integrity constraints or business rules. Every write transaction must leave the database in a structurally valid state—foreign keys must reference valid primary keys, unique constraints must be honored, and any application-defined rules must be maintained. If a transaction would violate consistency, it is aborted and rolled back entirely.

**Isolation** controls how concurrent transactions interact with each other. Without isolation, one transaction's reads and writes could be interleaved with another's, producing results that could not occur if transactions ran sequentially. Different isolation levels (read uncommitted, read committed, repeatable read, serializable) offer different tradeoffs between performance and the anomalies they prevent, such as dirty reads, non-repeatable reads, and phantom reads.

**Durability** ensures that once a transaction commits, its effects persist even if the database system crashes immediately afterward. This typically means the transaction's results have been written to non-volatile storage (disk) rather than merely held in memory. Durability guarantees that committed data survives power failures, system reboots, and hardware problems (though catastrophic hardware destruction affecting all copies of data may still result in loss).

## How It Works

Database systems implement ACID properties through a combination of logging, locking, and concurrency control mechanisms. **Write-ahead logging (WAL)** is the primary technique for achieving atomicity and durability—before any changes are applied to the database, they are first recorded in a transaction log. If a crash occurs, the database can recover by replaying committed transactions from the log and rolling back uncommitted ones.

Isolation is typically enforced through **multiversion concurrency control (MVCC)** or **two-phase locking (2PL)**. MVCC allows readers to see a consistent snapshot of the database at a point in time without blocking writers, while writers can continue modifying data without blocking readers. 2PL provides stricter isolation by holding locks until the transaction completes, preventing many concurrency anomalies at the cost of potentially reduced throughput.

```
Transaction Processing Example:

BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
  UPDATE accounts SET balance = balance + 100 WHERE account_id = 456;
  INSERT INTO ledger (transaction_id, amount, timestamp) VALUES ('TXN001', 100, NOW());
COMMIT;

If any statement fails → ROLLBACK (all changes undone)
If system crashes before COMMIT → WAL recovery rolls back on restart
```

## Practical Applications

ACID transactions are essential in any application where data integrity cannot be compromised. Banking and financial systems rely on ACID to ensure that money transfers are atomic and consistent. E-commerce platforms depend on isolation to prevent overselling inventory when multiple customers order simultaneously. Booking systems use ACID to guarantee that reserved slots are not double-booked. Healthcare records systems maintain patient safety by ensuring medication records and treatment histories are never corrupted.

The rise of distributed systems and microservices has created pressure to operate beyond single-database transactions, leading to patterns like **saga** (which orchestrates multiple local transactions across services with compensating rollbacks) and **eventual consistency** models that accept temporary inconsistency in exchange for availability and partition tolerance.

## Examples

```sql
-- ACID transaction example in SQL
BEGIN TRANSACTION;

-- Consistency check: ensure sufficient funds
SELECT balance FROM accounts WHERE account_id = 'savings-123';
-- Suppose balance is $50, transfer amount is $100

-- Atomic operation: debit account
UPDATE accounts 
SET balance = balance - 100, 
    last_activity = CURRENT_TIMESTAMP 
WHERE account_id = 'savings-123';

-- If balance went negative, this would violate a CHECK constraint
-- The transaction would be rolled back automatically

-- Credit checking account
UPDATE accounts 
SET balance = balance + 100,
    last_activity = CURRENT_TIMESTAMP 
WHERE account_id = 'checking-456';

-- Record the transaction for audit trail
INSERT INTO transfers (from_account, to_account, amount, status)
VALUES ('savings-123', 'checking-456', 100, 'completed');

COMMIT;  -- All changes now durable
```

## Related Concepts

- [[database]] — Systems for storing and managing data
- [[sql]] — Structured query language for relational databases
- [[nosql]] — Non-relational database alternatives
- [[concurrency-control]] — Managing simultaneous database access
- [[distributed-transactions]] — Transactions spanning multiple systems

## Further Reading

- "Transaction Processing: Concepts and Techniques" by Jim Gray and Andreas Reuter | Definitive reference
- "Designing Data-Intensive Applications" by Martin Kleppmann | Excellent overview of tradeoffs
- PostgreSQL Documentation: "Transaction Isolation"

## Personal Notes

ACID properties are often treated as a binary guarantee—when your database says it supports transactions, you expect all four properties. However, the reality is more nuanced: different databases implement these properties with varying degrees of strictness, and some configurations (like setting isolation levels) allow trading off some properties for performance. Understanding the specific guarantees your database provides—and how they map to your application's consistency requirements—is essential for building reliable systems. Never assume; always verify.
