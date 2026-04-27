---
title: "Redis"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [redis, database, cache, in-memory, key-value]
---

# Redis

## Overview

Redis (Remote Dictionary Server) is an open-source, in-memory data structure store that serves as a database, cache, message broker, and queue. Created by Salvatore Sanfilippo in 2009, Redis stores data in RAM rather than on disk, delivering read and write operations measured in microseconds. This extraordinary speed makes it indispensable for applications requiring real-time responsiveness—gaming leaderboards, session management, rate limiting, and pub/sub messaging all benefit from Redis's sub-millisecond latency.

Redis persists data optionally to disk using RDB snapshots or AOF (append-only file) logs, trading some performance for durability guarantees. Its simple text-based protocol (RESP) makes it easy to integrate with any programming language through official and community clients. Redis's single-threaded event-loop architecture avoids the complexity of thread synchronization and context switching, allowing it to saturate CPU resources efficiently.

Redis has expanded well beyond simple caching into a versatile data platform. Modern deployments include Redis Cluster for horizontal sharding, Redis Streams for event sourcing, and modules that add capabilities like search (RediSearch), JSON storage (RedisJSON), and graph databases (RedisGraph).

## Key Concepts

### Data Structures

Redis distinguishes itself by offering rich data types beyond simple strings:

```bash
# Strings — binary-safe values
SET user:123:name "Alice"
GET user:123:name          # "Alice"
INCR pageviews:home        # Atomic counter

# Lists — ordered collections (linked lists)
LPUSH notifications "new message"
LRANGE notifications 0 -1   # All items
RPOP notifications         # Remove from right

# Hashes — field-value pairs (objects)
HSET user:123 email "alice@example.com" age "28"
HGET user:123 email
HGETALL user:123

# Sets — unordered unique strings
SADD tags:article:42 "redis" "database" "cache"
SMEMBERS tags:article:42
SINTER tags:article:42 tags:article:99  # Set intersection

# Sorted Sets — scored collections (rankings)
ZADD leaderboard 1500 "Alice" 1200 "Bob" 1800 "Charlie"
ZRANK leaderboard "Alice"       # 1 (0-indexed rank)
ZREVRANGE leaderboard 0 9       # Top 10
```

### Expiration and TTL

```bash
# Set expiration on keys (auto-cleanup)
SET session:abc123 "{'userId': 42}"
EXPIRE session:abc123 3600       # 1 hour TTL
TTL session:abc123               # Seconds remaining: 3600
```

### Pub/Sub Messaging

```bash
# Publisher broadcasts to channel
PUBLISH notifications "user:123 signed up"

# Subscriber listens on channel
SUBSCRIBE notifications
```

## How It Works

Redis uses a client-server model over TCP. Clients connect, send commands, and receive responses. The server processes each command atomically in a single thread. Because Redis is single-threaded, every command is inherently isolated from every other—no race conditions within a single Redis instance.

Commands are simple and follow a consistent pattern: `COMMAND KEY [ARGUMENTS]`. The server reads, parses, and executes them synchronously. For operations like `INCR`, Redis performs the operation atomically in a single step, making it safe for concurrent clients without additional locking.

For high availability, Redis Sentinel monitors master and replica instances, handling automatic failover. Redis Cluster shards data across multiple nodes, automatically redistributing keys when nodes join or leave.

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Pipeline: batch multiple commands (reduced round-trips)
pipe = r.pipeline()
pipe.set('key:a', 'value1')
pipe.get('key:a')
pipe.hset('user:1', mapping={'name': 'Alice', 'score': '100'})
pipe.zadd('leaderboard', {'Bob': 150})
pipe.zrevrank('leaderboard', 'Bob')
results = pipe.execute()

# Cache with JSON serialization
import json
cached_data = r.get('product:42')
if cached_data:
    product = json.loads(cached_data)
else:
    product = fetch_from_db(42)
    r.setex('product:42', 300, json.dumps(product))  # 5 min TTL
```

## Practical Applications

**Caching**: The dominant use case. Redis sits between your app and a slower primary database (PostgreSQL, MySQL), storing hot data in memory. Cache-aside, write-through, and write-behind patterns all work well with Redis.

**Session Store**: Web sessions (auth tokens, shopping carts, user preferences) are stored in Redis with TTLs matching session duration. Distributed sessions work across multiple app servers without sticky sessions.

**Rate Limiting**: Atomic increment operations on keys with expiration implement sliding-window rate limiting for API endpoints:

```lua
-- Lua script for atomic rate limiting
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local current = tonumber(redis.call('GET', key) or '0')
if current >= limit then
    return 0
end
redis.call('INCR', key)
if current == 0 then
    redis.call('EXPIRE', key, window)
end
return 1
```

**Real-Time Leaderboards**: Sorted sets with scores enable O(log N) ranking operations—perfect for gaming leaderboards, top-N queries, and user rankings.

**Message Queues**: Lists support LPUSH + BRPOP for a simple blocking queue. For complex use cases, Redis Streams (introduced in v5.0) provides a Kafka-like log with consumer groups.

## Examples

```python
# Simple cache implementation
def get_user_profile(user_id):
    cache_key = f"user:{user_id}:profile"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    profile = db.fetch_user(user_id)
    redis_client.setex(cache_key, 3600, json.dumps(profile))
    return profile

# Distributed lock (simplified)
def acquire_lock(lock_name, timeout=10):
    return redis_client.set(f"lock:{lock_name}", "1", nx=True, ex=timeout)

def release_lock(lock_name):
    redis_client.delete(f"lock:{lock_name}")
```

## Related Concepts

- [[Database]] — The broader category of data storage systems that Redis belongs to
- [[Caching]] — The technique of storing frequently accessed data for faster retrieval
- [[Memcached]] — Another popular in-memory caching solution
- [[Message Queue]] — Systems for asynchronous communication between services
- [[NoSQL]] — Category of databases that do not use traditional relational models
- [[Docker]] — Container platform commonly used to deploy Redis instances
- [[Kubernetes]] — Orchestrator often used to manage Redis deployments (with persistence challenges)

## Further Reading

- [Redis Documentation](https://redis.io/docs/)
- [Redis University](https://university.redis.com/) — Free Redis courses
- [The Little Redis Book](https://github.com/pcamd/redis-book) — Free comprehensive guide
- [Redis Persistence Explained](https://redis.io/docs/management/persistence/)

## Personal Notes

Redis is one of those tools that feels almost magical the first time you use it for caching—pages that took 200ms now respond in under 5ms. But the ephemeral nature of in-memory storage means you must treat Redis cache as potentially missing at any time; always have a fallback to the primary database. Redis persistence (AOF vs RDB) is a real trade-off: AOF with `fsync=everysec` gives reasonable durability at ~10% performance cost. Redis Cluster solves scaling but sacrifices `KEYS` and `SCAN` across shards.
