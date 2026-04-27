---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[vercel-database-persistence]]
  - [[sqlite-in-serverless-environments]]
  - [[database]]
relationship_count: 3
---

# Serverless Database Solutions

> Managed database services designed for serverless environments — eliminating instance management and scaling automatically.

## Overview

**Serverless database solutions** are managed database services that abstract away server provisioning, scaling, and maintenance. You connect to a database endpoint; the provider handles everything else.

Unlike traditional databases where you manage an instance (or cluster), serverless databases:
- Scale to zero when not in use
- Scale up automatically under load
- Charge per query/request, not per instance hour
- Require noops-style management

## Categories of Serverless Databases

### Serverless SQL

| Database | Provider | Strengths |
|----------|----------|-----------|
| **PlanetScale** | Serverless MySQL | MySQL compatible, branching |
| **Neon** | Serverless Postgres | Postgres compatible, branching |
| **Supabase** | Postgres | Real-time, edge functions |
| **Turso** | SQLite | Embedded, globally distributed |
| **AWS Aurora Serverless** | MySQL/Postgres | Auto-scaling, ACID |

### Serverless NoSQL/Document

| Database | Provider | Strengths |
|----------|----------|-----------|
| **DynamoDB** | AWS | Managed, infinite scale |
| **Cloudflare D1** | Cloudflare | SQLite at edge |
| **Upstash Redis** | Serverless Redis | Low latency, Redis API |
| **MongoDB Atlas Serverless** | MongoDB | Document model |

### Edge Databases

For applications running at the edge (Cloudflare Workers, Vercel Edge Functions):

| Database | Edge Runtime | Storage |
|----------|--------------|---------|
| **Cloudflare D1** | Workers | Durable object storage |
| **Upstash Redis** | Workers, edge | Global Redis |
| **Turso** | LibSQL | Edge replicas |
| **Neon** | Edge compatible | Postgres |

## Serverless SQL Deep Dive

### Neon (Serverless Postgres)

```python
# Python with Neon serverless Postgres
import asyncpg

async def query_neon():
    # Connection string from Neon dashboard
    conn = await asyncpg.connect(
        "postgresql://user:pass@ep-xxx.neon.tech/dbname"
    )
    
    # Simple query — no instance management
    result = await conn.fetch(
        "SELECT * FROM users WHERE active = true"
    )
    
    await conn.close()
    return result
```

**Key features:**
- **Autoscaling**: Scales from zero to thousands of connections
- **Branching**: Create database branches like git branches
- **Point-in-time recovery**: Restore to any moment
- **Pooled connections**: Connection pooler included

### PlanetScale (Serverless MySQL)

```python
# Python with PlanetScale
import mysql.connector

def query_planetscale():
    conn = mysql.connector.connect(
        host="aws.connect.psdb.cloud",
        user="user",
        password="password",
        database="dbname"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products LIMIT 10")
    results = cursor.fetchall()
    
    return results
```

**Key features:**
- **Branching**: Full database branches for development
- **Vitess-based**: MySQL protocol, horizontally scalable
- **No schema migrations**: Online schema changes

### Supabase

```python
# Python with Supabase
from supabase import create_client, Client

def query_supabase():
    supabase: Client = create_client(
        SUPABASE_URL, SUPABASE_KEY
    )
    
    result = supabase.table("users").select("*").execute()
    return result.data
```

**Key features:**
- **Real-time subscriptions**: Push updates to clients
- **Auth included**: Built-in authentication
- **Edge Functions**: Run code at the edge
- **Postgres full power**: All Postgres features

## Cost Comparison

| Database | Free Tier | Pay Per Query |
|----------|-----------|---------------|
| **Neon** | 0.5GB storage, 5 branches | ~$0.10 per GB |
| **PlanetScale** | 1 production DB, 2 branches | ~$0.20 per 1M reads |
| **Supabase** | 500MB, 2GB transfer | ~$0.25 per GB |
| **Turso** | 9GB storage, 500 req/s | ~$0.10 per GB |
| **Upstash Redis** | 10K commands/day | ~$0.10 per 100K commands |

## Cold Start Behavior

A critical consideration for serverless:

| Database | Cold Start | Warm Latency |
|----------|-----------|--------------|
| **Neon** | 500ms-2s | 10-50ms |
| **PlanetScale** | 50-200ms | 5-20ms |
| **Supabase** | 100-500ms | 10-50ms |
| **Turso** | <50ms | <10ms |
| **Upstash Redis** | <10ms | <5ms |

## Use Cases

### Use Serverless SQL When:

- Relational data with complex queries
- Need ACID transactions
- Existing Postgres/MySQL expertise
- Need JOINs and complex aggregations

### Use Serverless NoSQL When:

- Key-value access patterns
- Document storage (JSON)
- Caching layer needed
- Extreme scale requirements

### Use Edge Databases When:

- Running at Cloudflare Workers
- Need global distribution
- Ultra-low latency requirements
- Data is mostly read-heavy

## Implementation Examples

### Vercel + Serverless Database

```typescript
// Vercel Serverless Function
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  await prisma.user.findMany({
    where: { active: true },
    select: { id: true, email: true }
  })
}
```

### Cloudflare Worker + D1

```typescript
// Cloudflare Worker with D1
export default {
  async fetch(request, env) {
    const stmt = env.DB.prepare('SELECT * FROM users LIMIT 10')
    const { results } = await stmt.all()
    
    return Response.json(results)
  }
}
```

### Turso + libSQL

```python
# Python with Turso
import libsql_client

async def query_turso():
    client = libsql_client.create_client(
        url="libsql://my-db.turso.io",
        auth_token="your-auth-token"
    )
    
    result = await client.execute(
        "SELECT * FROM products WHERE price < ?",
        [100]
    )
    
    return result.rows
```

## Trade-offs

### Advantages

- **No instance management**: No SSH, no patching, no backups to manage
- **Infinite scale**: Handle traffic spikes without capacity planning
- **Cost efficiency**: Pay only for what you use
- **Global distribution**: Many offer edge replicas
- **Developer experience**: Get started in minutes

### Disadvantages

- **Connection limits**: Some have stricter connection limits
- **Vendor lock-in**: Each has proprietary APIs
- **Cold start latency**: Initial queries may be slow
- **Limited tuning**: Less control over performance
- **Cost at scale**: Can become expensive at high volume

## Related Concepts

- [[vercel-database-persistence]] — Vercel's persistence options
- [[sqlite-in-serverless-environments]] — SQLite in serverless
- [[database]] — General database concepts

## References

- [Neon Documentation](https://neon.tech/docs)
- [PlanetScale Documentation](https://docs.planetscale.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Cloudflare D1](https://developers.cloudflare.com/d1/)
