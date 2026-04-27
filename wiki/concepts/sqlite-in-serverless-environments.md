---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[serverless-database-solutions]]
  - [[database]]
  - [[ephemeral-vs-persistent-storage]]
relationship_count: 3
---

# SQLite in Serverless Environments

> Using SQLite as a lightweight, embedded database in serverless functions and edge runtimes.

## Overview

**SQLite** is typically embedded in applications, not associated with serverless. However, new approaches are bringing SQLite to serverless environments — including Cloudflare D1, Turso, and local development patterns that mirror production serverless setups.

This page covers using SQLite in serverless contexts, including traditional AWS Lambda, Cloudflare Workers, and edge runtimes.

## Why SQLite in Serverless?

### Traditional Serverless Database Limitations

Typical serverless functions can't run a traditional database server:

- **No persistent process**: Each invocation may be a new container/VM
- **Ephemeral filesystem**: Local storage is lost between invocations
- **Connection limits**: Databases have connection pool limits
- **Cold starts**: Database connections add latency

### SQLite Solutions

Two patterns emerge:

1. **Ephemeral SQLite**: SQLite file on ephemeral storage, good for development/testing
2. **Durable SQLite**: SQLite stored in durable object storage (Cloudflare D1, Turso)

## Serverless SQLite Solutions

### Cloudflare D1

**D1** is SQLite at the edge — stored in Cloudflare's durable storage, accessible from Workers.

```typescript
// Cloudflare Worker with D1
export default {
  async fetch(request, env) {
    // Create D1 database client
    const db = env.DB
    
    // Run queries
    const { results } = await db
      .prepare('SELECT * FROM users WHERE active = ?')
      .bind(1)
      .all()
    
    return Response.json(results)
  }
}
```

**Setup with Wrangler:**

```bash
# Create a D1 database
wrangler d1 create my-database

# Bind in wrangler.toml
# [[d1_databases]]
# binding = "DB"
# database_name = "my-database"
# database_id = "abc-123"

# Run migrations
wrangler d1 execute my-database --file=./schema.sql

# Query from Worker
const { results } = await env.DB.prepare(
  'INSERT INTO users (name, email) VALUES (?, ?)'
).bind('Alice', 'alice@example.com').run()
```

### Turso (Distributed SQLite)

**Turso** is libSQL (SQLite-compatible) with edge replicas globally distributed.

```python
import libsql_client

async def query_turso():
    client = libsql_client.create_client(
        url="libsql://my-db.turso.io",
        auth_token="your-token"
    )
    
    result = await client.execute(
        "SELECT * FROM products WHERE price < ?",
        [100]
    )
    
    return result.rows
```

**Key features:**
- Embedded SQLite at the edge
- Global replication
- Free tier: 9GB storage
- Multi-tenancy support

### Local Development with SQLite

For local development that mirrors serverless patterns:

```bash
# Using wrangler d1 locally
wrangler d1 create dev-db --local
wrangler d1 execute dev-db --local --file=./schema.sql

# Or using SQLite directly for testing
sqlite3 dev.db < schema.sql
```

## SQLite File on Ephemeral Storage

For development or short-lived functions, SQLite on `/tmp`:

```python
import sqlite3
import os

def get_db():
    """Get or create SQLite database on ephemeral storage."""
    db_path = "/tmp/app.db"
    
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                expires_at INTEGER
            )
        """)
        return conn
    
    return sqlite3.connect(db_path)

def lambda_handler(event, context):
    db = get_db()
    
    # Cache lookup
    cursor = db.execute(
        "SELECT value FROM cache WHERE key = ? AND expires_at > ?",
        [event['key'], event['timestamp']]
    )
    
    result = cursor.fetchone()
    return {"cached": result[0] if result else None}
```

**⚠️ Warning**: Data in `/tmp` is lost when the Lambda execution environment is recycled. Use for development only.

## SQLite Limitations in Serverless

### Concurrency

SQLite has write limitations:
- Single writer at a time
- WAL mode helps readers, but writes still serialize
- Not suitable for high-write workloads

**Workaround**: Use Turso with embedded replicas or accept eventual consistency.

### Connection Handling

Each function invocation may be a new process:

```python
# WRONG: Module-level connection (fails on cold start)
conn = sqlite3.connect("/tmp/app.db")  # Global — bad idea

# RIGHT: Create connection per invocation
def handler(event, context):
    conn = sqlite3.connect("/tmp/app.db")  # Per-invocation — safe
    try:
        result = conn.execute("SELECT * FROM items").fetchall()
        return {"items": result}
    finally:
        conn.close()
```

### File Size Limits

| Platform | Ephemeral Storage | D1/Turso Limits |
|----------|-------------------|-----------------|
| AWS Lambda | 512MB-10GB | N/A (use RDS) |
| Cloudflare Workers | 0.5MB-5GB | 50MB per database |
| Vercel | 500MB | N/A (use Turso) |

## Comparison Table

| Aspect | Cloudflare D1 | Turso | Ephemeral SQLite |
|--------|---------------|-------|------------------|
| **Durability** | Durable | Durable | Lost on restart |
| **Edge** | Yes (Workers) | Yes | No |
| **Replication** | Cloudflare global | Multi-region | None |
| **Free tier** | 5GB | 9GB storage | Unlimited |
| **SQLite compat** | SQLite (WASM) | libSQL | SQLite |
| **Write scale** | Moderate | Moderate | Low |

## Use Cases

### D1/Turso Appropriate For:

- Read-heavy applications (blogs, portfolios)
- User-generated content with moderate writes
- Caching and key-value data
- Global applications needing low latency

### D1/Turso NOT Appropriate For:

- High-write workloads (thousands/sec)
- Complex transactions spanning multiple writes
- Real-time analytics
- Applications requiring PostgreSQL features

## Migration from Other Databases

### From PostgreSQL to SQLite

```sql
-- PostgreSQL syntax
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- SQLite equivalent
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Key Differences

| PostgreSQL | SQLite |
|------------|--------|
| `SERIAL` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `TIMESTAMP DEFAULT NOW()` | `DATETIME DEFAULT CURRENT_TIMESTAMP` |
| `VARCHAR(n)` | `TEXT` |
| `NOW()` | `CURRENT_TIMESTAMP` |
| Schema migrations | D1 migrations via Wrangler |

## Performance Tuning

### Indexes

```sql
-- Always index foreign keys and frequent query columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
```

### WAL Mode for Reads

```sql
-- Enable WAL for better concurrent read performance
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

## Related Concepts

- [[serverless-database-solutions]] — Overview of serverless databases
- [[database]] — General database concepts
- [[ephemeral-vs-persistent-storage]] — Understanding storage types

## References

- [Cloudflare D1 Documentation](https://developers.cloudflare.com/d1/)
- [Turso Documentation](https://turso.tech/docs)
- [libSQL GitHub](https://github.com/tursodatabase/libsql)
- [SQLite Serverless Patterns](https://blog.cloudflare.com/d1/)
