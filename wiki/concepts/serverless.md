---
title: "Serverless"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud, aws-lambda, functions, faas, cloud-computing]
---

# Serverless

## Overview

Serverless computing is a cloud execution model where developers write and deploy individual functions that run in stateless compute containers, managed entirely by the cloud provider. The provider handles provisioning, scaling, capacity planning, and server maintenance automatically—developers simply upload code and pay only for the compute time consumed (often measured in milliseconds), with zero cost when the function isn't running. The term "serverless" is somewhat of a misnomer—servers still exist, but the operational responsibilities shift entirely to the cloud provider.

The paradigm gained mainstream adoption with AWS Lambda in 2014, but the concept predates it in academic work on functions-as-a-service (FaaS). Serverless is particularly compelling for event-driven workloads: processing uploaded files, handling webhook payloads, running scheduled tasks, responding to database changes, or powering chatbots. These workloads are often idle most of the time, making traditional always-on servers economically inefficient.

## Key Concepts

### Function as a Service (FaaS)

FaaS is the core abstraction in serverless—the unit of deployment is an individual function rather than an application or container. Functions are triggered by events (HTTP requests, file uploads, message queue arrivals, scheduled timers) and typically run for seconds or minutes at most, with hard limits on execution duration (Lambda caps at 15 minutes).

Functions should be stateless: any state should be stored externally (database, object storage, cache). This constraint enables the provider to run functions in any container across the fleet, scaling horizontally in milliseconds as demand increases.

```javascript
// AWS Lambda function example (Node.js)
exports.handler = async (event) => {
  // Parse the incoming event
  const { action, payload } = JSON.parse(event.body || '{}');
  
  switch (action) {
    case 'processOrder':
      return await processOrder(payload);
    case 'getStatus':
      return await getOrderStatus(payload.orderId);
    default:
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Unknown action' })
      };
  }
};

async function processOrder(payload) {
  // Business logic here
  const result = await saveToDatabase(payload);
  
  return {
    statusCode: 200,
    body: JSON.stringify({ success: true, orderId: result.id })
  };
}
```

### Cold Starts and Warm Starts

Serverless functions may be terminated when idle and recreated ("cold start") when next invoked. Cold starts involve initializing the runtime, loading dependencies, and setting up the execution environment—adding latency that can range from milliseconds to seconds depending on the language runtime and function size. "Warm starts" reuse an existing container and have minimal added latency.

Providers offer provisioned concurrency options (Lambda's Provisioned Concurrency, Azure's Premium Functions) to keep functions warm and eliminate cold start latency for latency-sensitive applications.

### Serverless Backend Services

Beyond compute, serverless platforms offer managed backend services that integrate with functions:

- **Object Storage**: AWS S3, Azure Blob Storage—store files, trigger functions on upload
- **Databases**: AWS DynamoDB, Aurora Serverless, PlanetScale—serverless data storage
- **Message Queues**: AWS SQS, SNS, Azure Event Grid—decouple function invocations
- **API Gateways**: AWS API Gateway, Azure Functions HTTP trigger—HTTP frontends for functions
- **Authentication**: AWS Cognito, Auth0—identity without servers

This "serverless-first" architecture composes managed services via events, minimizing server management while maximizing managed service benefits.

## How It Works

When a function is invoked, the provider's runtime selects an appropriate container from its fleet. If no warm container exists for that function, a new one is initialized (cold start): the runtime starts, the function code loads, and any initialization code (outside the handler) executes. Then the handler runs, processes the event, and returns a response. Idle containers are eventually terminated; active ones may handle multiple invocations sequentially.

Scaling is automatic and near-instantaneous: the provider monitors concurrency and provisions additional container instances as needed, distributing invocations across the fleet. This elastic scaling handles sudden traffic spikes without manual intervention.

## Practical Applications

**Webhook Processing**: Functions are ideal for responding to third-party webhooks (payment notifications, GitHub events, Slack commands)—process the payload, trigger business logic, return acknowledgment quickly.

**File Processing Pipelines**: Upload an image to S3, trigger a Lambda to resize and watermark it, store the result back to S3. No persistent servers needed for the transformation logic.

**Scheduled Tasks and Cron**: Replace cron servers with scheduled function invocations—run daily reports, clean up stale data, send batch emails.

**API Backends**: Combine functions with API Gateway for HTTP APIs; each route can be a separate function, enabling independent deployment and scaling.

**Real-time Data Processing**: Process streams from Kinesis or Kafka, apply transformations or aggregations, and write results to a data warehouse.

## Examples

A complete serverless image processing pipeline using AWS:

```yaml
# Serverless Framework configuration (serverless.yml)
service: image-processor

provider:
  name: aws
  runtime: nodejs18.x
  memorySize: 512
  timeout: 30

functions:
  processImage:
    handler: handler.processImage
    events:
      - s3:
          bucket: uploads-bucket
          event: s3:ObjectCreated:*
          rules:
            - prefix: raw/
            - suffix: .jpg
    environment:
      OUTPUT_BUCKET: processed-bucket

resources:
  Resources:
    uploadsBucket:
      Type: AWS::S3::Bucket
      Properties:
        BucketName: my-unique-uploads-bucket
```

```javascript
// handler.js
const Sharp = require('sharp');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

const s3 = new S3Client({});

exports.processImage = async (event) => {
  const bucket = event.Records[0].s3.bucket.name;
  const key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
  
  // Only process files in raw/ prefix
  if (!key.startsWith('raw/')) return;
  
  // Download, process, upload
  const response = await s3.getObject({ Bucket: bucket, Key: key });
  const buffer = await response.Body.toBuffer();
  
  const processed = await Sharp(buffer)
    .resize(800, 600, { fit: 'inside' })
    .jpeg({ quality: 80 })
    .toBuffer();
  
  const outputKey = key.replace('raw/', 'processed/');
  await s3.putObject({
    Bucket: process.env.OUTPUT_BUCKET,
    Key: outputKey,
    Body: processed,
    ContentType: 'image/jpeg'
  });
  
  return { statusCode: 200, body: JSON.stringify({ processed: outputKey }) };
};
```

## Related Concepts

- [[AWS Lambda]] - AWS's serverless compute platform
- [[Functions as a Service]] - The FaaS paradigm underlying serverless
- [[Cloud Computing]] - The broader category of managed cloud services
- [[Event-Driven Architecture]] - Design pattern that pairs naturally with serverless
- [[Microservices]] - Architecture style often combined with serverless functions
- [[Containerization]] - Technology that serverless builds upon but abstracts away

## Further Reading

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Serverless Framework](https://www.serverless.com/) - Popular deployment framework
- [Cloudflare Workers](https://workers.cloudflare.com/) - Edge-computing serverless platform

## Personal Notes

The "pay per millisecond" model is genuinely transformative for variable workloads, but the per-invocation overhead can make serverless more expensive than containers for consistently busy services. Vendor lock-in is the elephant in the room—testing locally and understanding escape hatches (event formats, cold start behavior, timeouts) matters. I treat serverless as one tool among many, reaching for it when the workload is event-driven or bursty, and containers when I need predictable response times at constant load.
