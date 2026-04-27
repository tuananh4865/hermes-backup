---
title: WAL (Write-Ahead Logging)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [wal, database, postgresql, durability, recovery, logging]
---

# WAL (Write-Ahead Logging)

## Overview

Write-Ahead Logging (WAL) is a fundamental database logging technique that ensures durability and atomicity of database transactions. The core principle is elegantly simple: before any change is made to the database itself, the change must first be written to a log file stored on durable storage. This log records enough information to redo or undo the transaction in case of a system failure. If the database crashes before all changes are persisted to the main data files, the WAL can be used to recover to a consistent state, ensuring that no committed transaction is lost and no partially completed transaction is applied.

WAL is the foundation of crash recovery in most modern relational database systems, including PostgreSQL, Oracle, MySQL (with InnoDB), and SQLite. Each of these implements WAL with slightly different characteristics and optimizations, but the underlying concept remains consistent. PostgreSQL's implementation, in particular, is well-documented and serves as a reference implementation for understanding WAL in practice. The technique was popularized in the 1980s and has become a standard feature of enterprise database systems due to its reliability guarantees and performance benefits.

## Key Concepts

### Core Principles

**Atomicity** - All changes in a transaction are recorded in the log before being applied to the database. If a transaction commits, all its operations will be recovered. If it doesn't commit, none will be.

**Durability** - Once the log record is safely on disk (fsynced), the transaction is considered committed, even if the actual database files haven't been updated yet.

**Write-Ahead Property** - The "write-ahead" aspect means the log must be flushed before the actual database pages. This ordering guarantees that if a crash occurs, the log can reconstruct what was happening at the time.

### WAL Components

**Log Sequence Number (LSN)** - A monotonically increasing identifier for each WAL record, representing the position in the WAL stream. Every page in the database header contains the LSN of the most recent WAL record affecting that page.

**WAL Segments** - WAL is typically divided into files (segments) of a fixed size (commonly 16MB in PostgreSQL). When one segment fills, another is created.

**Checkpoints** - Periodic points where the database ensures all modified pages are written to disk. After a checkpoint, the corresponding WAL segments can potentially be recycled or removed.

**WAL Writer** - A background process that periodically writes WAL buffers to disk, optimizing performance by batching writes.

### WAL vs. Shadow Paging

Two primary approaches exist for ensuring atomicity:

| Aspect | Write-Ahead Logging | Shadow Paging |
|--------|---------------------|---------------|
| Overhead | Log writes on every update | Copy-on-write for affected pages |
| Space | Log can grow large | No additional log storage |
| Performance | Sequential log writes | Random I/O for page copies |
| Recovery | Can be slow (replay) | Typically faster recovery |
| Hot Backup | More complex | Simpler to implement |

## How It Works

### The Write Path

1. **Transaction Begins** - A transaction ID is assigned, and the system begins recording operations.

2. **Operations Logged** - As the transaction modifies pages, each modification generates a WAL record containing:
   - Transaction ID
   - Page identifier (table/row)
   - Old data (for undo)
   - New data (for redo)
   - LSN of previous record in same transaction

3. **WAL Flush** - Before returning "commit success" to the client, the WAL subsystem ensures the log records are flushed to disk (typically via `fsync()`).

4. **Background Write** - The actual database pages are modified in memory (buffer pool). A separate process writes dirty pages to disk, often much later.

### The Recovery Path

When a database restarts after a crash:

1. **Locate Checkpoint** - The recovery process locates the most recent checkpoint in the WAL.

2. **Redo Phase** - Starting from the checkpoint, WAL records are replayed. All committed transactions are reapplied to bring the database to the correct state.

3. **Undo Phase** - Incomplete transactions (those that didn't commit) are rolled back using the undo information in the WAL.

```sql
-- PostgreSQL: Monitoring WAL usage
SELECT 
    pg_current_wal_lsn() AS current_lsn,
    pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0') AS bytes_between IS
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0')) AS size_between;
    
-- Check WAL archive status
SELECT * FROM pg_stat_archiver;

-- Force a checkpoint (for testing/admin)
CHECKPOINT;
```

## Practical Applications

### Configuration Tuning

WAL behavior can be tuned for different workloads:

**WAL Level** - Controls how much information is written:
- `minimal` - Only information needed for crash recovery
- `replica` - Adds information needed for logical replication
- `logical` - Full information for logical decoding

**WAL Buffers** - Memory for WAL data before writing to disk:
```ini
# postgresql.conf
wal_buffers = 16MB    # Default 4MB, increase for heavy write workloads
```

**Checkpoint Tuning** - Balance between recovery time and write amplification:
```ini
# postgresql.conf
checkpoint_timeout = 10min    # How often to checkpoint
max_wal_size = 1GB            # Maximum WAL size before forced checkpoint
min_wal_size = 80MB           # Minimum WAL to keep for recycling
```

### Performance Implications

WAL introduces overhead but also optimization opportunities:

- **Sequential I/O** - WAL writes are sequential, making them fast even on spinning disks
- **Batching** - Group commits allow multiple transactions to share a single disk sync
- **Hot Standby** - WAL enables read replicas with minimal overhead
- **Point-in-Time Recovery** - WAL archives enable恢复到任意时间点

## Examples

### Simulating WAL Behavior (Conceptual)

```python
import os
import struct
from datetime import datetime

class WALEntry:
    def __init__(self, txn_id, table_id, page_id, old_data, new_data):
        self.txn_id = txn_id
        self.table_id = table_id
        self.page_id = page_id
        self.old_data = old_data
        self.new_data = new_data
        self.lsn = self._generate_lsn()
    
    def _generate_lsn(self):
        # Simplified LSN: timestamp + sequence
        timestamp = int(datetime.now().timestamp() * 1000000)
        return timestamp
    
    def serialize(self):
        return struct.pack('>IIIIII', 
            self.lsn, self.txn_id, self.table_id, 
            self.page_id, len(self.old_data), len(self.new_data))

class SimpleWAL:
    def __init__(self, path):
        self.path = path
        self.fp = open(path, 'ab')
        self.txn_log = {}  # In-progress transactions
    
    def begin_txn(self, txn_id):
        self.txn_log[txn_id] = []
    
    def write_entry(self, txn_id, table_id, page_id, old_data, new_data):
        entry = WALEntry(txn_id, table_id, page_id, old_data, new_data)
        self.fp.write(entry.serialize())
        self.fp.flush()  # Ensure write-ahead
        os.fsync(self.fp.fileno())  # Force to disk
        self.txn_log[txn_id].append(entry)
        return entry.lsn
    
    def commit_txn(self, txn_id):
        # Write commit record - flush happens automatically
        commit_record = struct.pack('>II', self.txn_log[txn_id][-1].lsn + 1, txn_id)
        self.fp.write(commit_record)
        self.fp.flush()
        os.fsync(self.fp.fileno())
        del self.txn_log[txn_id]
    
    def close(self):
        self.fp.close()
```

## Related Concepts

- [[postgresql]] — PostgreSQL's specific WAL implementation
- [[acid]] — How WAL enables atomicity and durability
- [[crash-recovery]] — Database recovery mechanisms
- [[redo-log]] — The redo portion of WAL
- [[undo-log]] — The undo portion for rollback
- [[replication]] — Using WAL for streaming to replicas

## Further Reading

- [PostgreSQL WAL Documentation](https://www.postgresql.org/docs/current/wal.html)
- [CMU Database Systems - WAL](https://www.youtube.com/watch?v=twYFW5pdozo)
- [Database Systems: The Complete Book - Logging chapter](https://example.com)

## Personal Notes

WAL is one of those concepts that feels complex until you grasp the core insight: separate what's hard to lose (durable log) from what's hard to compute (actual data). I remember when I first understood why WAL makes random I/O sequential and enables features like point-in-time recovery. For production PostgreSQL, I always recommend setting up WAL archiving to object storage (S3) - it costs very little and provides insurance against catastrophic storage failure. Also, monitoring `pg_stat_archiver` and `checkpoint_write_time` metrics has saved me several times from performance issues before they became outages.
