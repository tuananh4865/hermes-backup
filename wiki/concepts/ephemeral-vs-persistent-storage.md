---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[vercel-database-persistence]]
  - [[serverless]]
  - [[sqlite-in-serverless-environments]]
relationship_count: 3
---

# Ephemeral vs Persistent Storage

> Two fundamental paradigms for data storage in cloud and serverless environments.

## Overview

**Ephemeral storage** is temporary, instance-local storage that exists only for the lifetime of a compute instance. **Persistent storage** is durable storage that survives beyond any single compute instance.

Understanding when to use each is fundamental to building reliable cloud applications.

## Ephemeral Storage

### What It Is

Ephemeral storage is attached to a specific compute instance (VM, container, serverless function instance). When that instance is terminated or restarted, all data is lost.

Examples:
- `/tmp` directory in a Docker container
- Instance-local filesystem on an EC2 instance
- Local variables in a serverless function execution
- Scratch disks on cloud VMs

### Characteristics

| Property | Description |
|----------|-------------|
| **Lifetime** | Tied to instance lifecycle |
| **Location** | Instance-local or container-local |
| **Performance** | Very fast (local SSD) |
| **Cost** | Usually included with instance |
| **Data Loss** | Complete on instance termination |

### Use Cases

```python
# Ephemeral: Processing temporary data in a serverless function
def process_image(event, context):
    # Download to ephemeral /tmp
    temp_file = "/tmp/input_image.jpg"
    download_file(event['image_url'], temp_file)
    
    # Process (local SSD is fast)
    result = apply_filters(temp_file)
    
    # Upload result
    upload_to_s3(result)
    
    # Data lost when function terminates
    return result
```

### Risks

```
Instance terminates → /tmp data gone
Function cold start on NEW instance → Previous /tmp empty
Container restart → Ephemeral storage wiped
```

## Persistent Storage

### What It Is

Persistent storage exists independently of compute instances. Data survives instance terminations, restarts, and scaling events.

Examples:
- Amazon S3 (object storage)
- Cloud databases (RDS, DynamoDB, PlanetScale)
- Network filesystems (EFS, Azure Files)
- Object storage buckets
- Managed databases (Neon, Supabase, PlanetScale)

### Characteristics

| Property | Description |
|----------|-------------|
| **Lifetime** | Indefinite |
| **Location** | Network-attached or managed service |
| **Performance** | Network latency (usually slower than local) |
| **Cost** | Pay per usage (usually higher) |
| **Data Loss** | None (designed for durability) |

### Use Cases

```python
# Persistent: Storing user data in a database
async def save_user_preference(user_id: str, preference: dict):
    # Data persists across all instances
    await db.execute(
        "UPDATE users SET preferences = %s WHERE id = %s",
        preference, user_id
    )
    return {"success": True}

# Or using object storage
async def upload_user_avatar(user_id: str, image_data: bytes):
    key = f"avatars/{user_id}.jpg"
    await s3.put_object(Bucket="my-bucket", Key=key, Body=image_data)
    # Survives instance termination
    return f"https://my-bucket.s3.amazonaws.com/{key}"
```

## Key Differences

| Aspect | Ephemeral | Persistent |
|--------|-----------|------------|
| **Durability** | Lost on instance termination | Survives indefinitely |
| **Access** | Single instance | Any instance |
| **Performance** | Very fast (local) | Network latency |
| **Cost** | Included with compute | Separate pay |
| **Scaling** | State confined to instance | Shared across instances |
| **Use Case** | Temporary processing | Long-term storage |

## Storage Patterns in Practice

### Pattern 1: Pure Serverless (All Persistent)

```python
# Serverless function with no local state
def handler(event, context):
    user_id = event['user_id']
    
    # Read from persistent storage
    data = db.fetch_one("SELECT * FROM users WHERE id = %s", user_id)
    
    # Process
    result = transform(data)
    
    # Write to persistent storage
    db.execute("UPDATE users SET result = %s WHERE id = %s", result, user_id)
    
    return result
```

### Pattern 2: Hybrid (Ephemeral Cache + Persistent Store)

```python
# Using ephemeral for caching expensive computation
def handler(event, context):
    cache_key = f"compute:{event['input']}"
    
    # Check ephemeral cache first
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Expensive computation
    result = expensive_calculation(event['input'])
    
    # Cache result in ephemeral Redis (will be lost on restart)
    redis.setex(cache_key, 3600, json.dumps(result))  # 1 hour TTL
    
    # Also save to persistent storage for durability
    db.execute("INSERT INTO results %s", result)
    
    return result
```

### Pattern 3: Local SSD for Temporary Files

```python
# Large file processing with ephemeral storage
def process_large_file(event, context):
    # Download to local ephemeral SSD
    input_path = "/tmp/large_file.csv"
    output_path = "/tmp/processed.csv"
    
    download_from_s3("bucket", event['file_key'], input_path)
    
    # Process locally (very fast on ephemeral SSD)
    df = pandas.read_csv(input_path)
    result = heavy_transform(df)
    result.to_csv(output_path)
    
    # Upload result to persistent storage
    upload_to_s3(output_path, f"processed/{event['file_key']}")
    
    # Cleanup
    os.remove(input_path)
    os.remove(output_path)
```

## Ephemeral Storage Limits

### Serverless Function Limits

| Platform | Ephemeral Storage | Notes |
|----------|-------------------|-------|
| AWS Lambda | 512MB–10GB | `/tmp` directory |
| Vercel Functions | 500MB | Ephemeral disk |
| Cloudflare Workers | 0.5MB–5MB | Memory (not disk) |
| Google Cloud Functions | 512MB-2GB | `/tmp` |

### Docker Container Limits

- Default: Ephemeral overlay filesystem
- Volume mounts: Can persist specific paths
- Bind mounts: Host filesystem access

## Related Concepts

- [[vercel-database-persistence]] — Vercel's database patterns
- [[serverless]] — Serverless architecture overview
- [[sqlite-in-serverless-environments]] — SQLite as ephemeral storage

## References

- [AWS Lambda: Ephemeral Storage](https://docs.aws.amazon.com/lambda/)
- [Docker: tmpfs mounts](https://docs.docker.com/storage/tmpfs/)
