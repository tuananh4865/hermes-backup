---
title: "AWS Lambda"
created: 2026-04-15
updated: 2026-04-19
type: concept
tags: [aws, serverless, cloud, computing, aws-lambda, backend]
related:
  - [[serverless-computing]]
  - [[cloud-computing]]
  - [[vercel]]
  - [[cloudflare-workers]]
  - [[ai-backend]]
sources:
  - https://aws.amazon.com/lambda/
  - https://docs.aws.amazon.com/lambda/
---

# AWS Lambda

> Serverless compute service that runs code in response to events and automatically manages compute resources. The foundational service of AWS serverless architecture.

## Overview

**AWS Lambda** is Amazon Web Services' serverless compute platform that lets you run code without provisioning or managing servers. You pay only for the compute time consumed — there is no charge when your code is not running.

**Launched:** November 2014
**Provider:** Amazon Web Services (AWS)
**Languages supported:** Node.js, Python, Ruby, Java, Go, .NET, Custom Runtime (Rust, C++)

## How AWS Lambda Works

Lambda follows an **event-driven execution model**:

1. **Upload code** — Package your code as a deployment package or container image
2. **Set triggers** — Define event sources (API Gateway, S3, DynamoDB, SQS, CloudWatch, etc.)
3. **Lambda provisions** — AWS automatically provisions the right amount of compute
4. **Code executes** — Your function runs in response to events
5. **Scale automatically** — Lambda runs your code in parallel for each event

## Lambda Function Anatomy

A Lambda function consists of:

### Handler Function
```python
import json

def lambda_handler(event, context):
    # event: dict containing trigger data
    # context: runtime information (request ID, timeout, etc.)

    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, {name}!')
    }
```

### Configuration
- **Memory:** 128MB to 10,240MB (1MB increments)
- **Timeout:** 1 second to 15 minutes
- **Concurrency:** Up to thousands of parallel executions
- **Layers:** Reusable code layers that can be shared across functions

## Pricing

Lambda uses a **pay-per-use** pricing model:

| Dimension | Free Tier | Paid |
|-----------|-----------|------|
| **Requests** | 1M/month | $0.20 per 1M requests |
| **Compute time** | 400,000 GB-seconds/month | $0.0000166667 per GB-second |

**Example cost for AI agent backend:**
- 1M function invocations at 500ms each with 512MB memory
- Compute: 500ms × 0.5GB × 1M = 250,000 GB-seconds
- Cost: ~$4.17/month (within free tier for most users)

## Common AI/LLM Integration Patterns

### API Backend for AI Agents
```python
def lambda_handler(event, context):
    # Parse request
    body = json.loads(event['body'])
    user_message = body['message']

    # Call LLM API (OpenAI, Anthropic, etc.)
    response = call_llm(user_message)

    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
```

### Processing AI Agent Tool Calls
Lambda functions can execute tool calls made by AI agents:
- Web searches
- Database queries
- File operations
- External API calls

### Stream Responses with Lambda

Lambda + API Gateway v2 supports HTTP streaming:
```python
def lambda_handler(event, context):
    return StreamingResponse(
        generate_streaming_response(),
        media_type='text/event-stream'
    )
```

## Lambda Limits

| Resource | Default Limit |
|----------|--------------|
| **Concurrent executions** | 1,000 (soft limit, can request increase) |
| **Deployment package size** | 50MB (compressed) / 250MB (uncompressed) |
| **Execution timeout** | 15 minutes |
| **Memory** | 128MB to 10,240MB |
| **/tmp directory storage** | 512MB |

## Advantages

- **No server management** — Zero infrastructure overhead
- **Automatic scaling** — From 0 to thousands of parallel executions
- **Cost efficiency** — Pay only for actual compute used
- **Integration** — Native connection to 200+ AWS services
- **High availability** — Runs across multiple AZs automatically
- **Cold start optimization** — Graviton2 processors provide better price-performance

## Limitations

- **Cold starts** — First invocation after inactivity has latency overhead
- **Execution time limit** — 15 minutes maximum (insufficient for very long tasks)
- ** Stateless** — Must use external storage for persistent state
- **Package size limits** — Large dependencies are problematic
- **Vendor lock-in** — Tied to AWS ecosystem

## Comparison with Alternatives

| Dimension | AWS Lambda | Vercel Edge | Cloudflare Workers |
|-----------|-----------|-------------|-------------------|
| **Cold start** | 100-500ms | <5ms | <5ms |
| **Max execution** | 15 minutes | 50ms-30s | 50ms-30s |
| **Edge network** | Regional | Global 100+ locations | Global 300+ locations |
| **AI/LLM use** | Great for API backends | Excellent for streaming | Good for lightweight tasks |
| **Pricing model** | Requests + compute | Included in hosting | 10M requests free |

## Best Practices for AI Agents

1. **Use Provisioned Concurrency** — Pre-warm functions for latency-sensitive AI responses
2. **Connection pooling** — Reuse database/API connections across invocations
3. **Layer dependencies** — Put large ML libraries in layers to manage cold starts
4. **Separate concerns** — Keep LLM calls in dedicated functions, not mixed with business logic
5. **Stream responses** — Use API Gateway v2 streaming for real-time AI output

## Related Concepts

- [[serverless-computing]] — Broader serverless architecture patterns
- [[cloud-computing]] — Cloud infrastructure overview
- [[ai-backend]] — Using cloud services for AI agent backends
- [[cloudflare-workers]] — Edge computing alternative
- [[vercel]] — Frontend deployment platform (often used alongside Lambda)
