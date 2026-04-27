---
title: "Serverless Computing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, architecture, aws-lambda, functions-as-a-service]
---

# Serverless Computing

## Overview

Serverless computing is a cloud execution model where a provider dynamically manages the allocation and provisioning of servers, charging only for the actual compute resources consumed rather than pre-purchased capacity. Despite the name, serverless does not mean there are no servers—rather, the abstraction layer is raised so that developers no longer need to think about server management, scaling, or capacity planning. The most prominent implementation of this model is Functions-as-a-Service (FaaS), where individual functions are the primary unit of deployment and execution.

The paradigm shift is fundamental: instead of deploying applications to servers, developers deploy discrete functions that are triggered by events. AWS Lambda, Google Cloud Functions, and Azure Functions are the major managed offerings, while open-source alternatives like OpenFaaS and Knative enable self-hosted serverless platforms. This model represents a move toward ultra-granular computing where resources are allocated at the function level with sub-second billing granularity.

## Key Concepts

**Stateless Functions**: Serverless functions are designed to be stateless—each invocation is independent, and any required state must be stored externally in databases, object storage, or cache layers. This constraint forces architects to think carefully about state management but also enables extreme horizontal scalability since any function instance can handle any request.

**Cold Starts**: When a serverless function hasn't been invoked recently, the provider may need to initialize a new execution environment, introducing latency called a "cold start." Warm starts reuse existing instances. Cold starts can range from milliseconds to seconds depending on the runtime and function complexity, making them a critical consideration for latency-sensitive applications.

**Event-Driven Triggers**: Functions respond to events from various sources—HTTP requests, file uploads, message queue notifications, scheduled timers, database changes, or IoT sensor data. This event-driven nature naturally aligns with microservices architectures and asynchronous workflows.

**Execution Limits**: Providers impose hard limits on function execution duration (typically 15 minutes max), memory allocation, and payload size. These constraints require architects to decompose larger workloads into smaller, composable functions.

## How It Works

When an event triggers a serverless function, the cloud provider's orchestration layer allocates resources, initializes the runtime environment, loads the function code, executes the function with the provided event data, and returns the result. The provider handles all infrastructure concerns including server provisioning, operating system maintenance, security patching, and automatic scaling from zero to thousands of concurrent executions.

```javascript
// AWS Lambda function example
exports.handler = async (event) => {
  const { userId } = event.pathParameters;
  const user = await getUserFromDatabase(userId);
  
  return {
    statusCode: 200,
    body: JSON.stringify({ user }),
    headers: { "Content-Type": "application/json" }
  };
};

async function getUserFromDatabase(userId) {
  // Simulated database query
  return { id: userId, name: "Jane Austen", tier: "premium" };
}
```

## Practical Applications

Serverless computing excels in scenarios like real-time file processing (image resizing, video transcoding), handling webhook payloads, running scheduled tasks and batch jobs, powering chatbots and conversational interfaces, backends for mobile and web applications, and processing streams of IoT data. The pay-per-invocation model is particularly cost-effective for workloads with variable or unpredictable traffic patterns.

Serverless is often combined with API Gateway services to create HTTP-accessible APIs without managing server infrastructure. This combination is a cornerstone of modern [[Microservices Architecture]] implementations.

## Examples

A common pattern is using serverless functions to handle image uploads:

```javascript
// Thumbnail generation triggered by S3 upload
exports.generateThumbnail = async (event) => {
  const srcBucket = event.Records[0].s3.bucket.name;
  const srcKey = decodeURIComponent(event.Records[0].s3.object.key);
  
  // Download, resize, and upload thumbnail
  const thumbnail = await sharp(srcKey)
    .resize(200, 200)
    .toBuffer();
    
  await s3.putObject({
    Bucket: `${srcBucket}-thumbs`,
    Key: `thumb-${srcKey}`,
    Body: thumbnail
  }).promise();
  
  return { statusCode: 200 };
};
```

## Related Concepts

- [[Functions as a Service]] - The specific category of serverless focusing on function deployment
- [[Microservices Architecture]] - Often paired with serverless for decomposing applications
- [[Cloud Computing]] - The broader context of on-demand computing resources
- [[AWS Lambda]] - The leading serverless platform
- [[Event-Driven Architecture]] - The programming model serverless naturally encourages
- [[Container Orchestration]] - Contrast with serverless for deployment models

## Further Reading

- "Serverless Architectures on AWS" by Peter Sbarski - Comprehensive guide to building serverless systems
- Martin Fowler's ServerlessArchitecting Guide - Architectural considerations and patterns

## Personal Notes

Serverless is not a silver bullet. I've seen teams struggle with debugging distributed function executions, managing complex inter-function dependencies, and controlling costs when functions are invoked millions of times daily. The approach works best for event-driven workloads with bursty traffic patterns. For long-running processes or consistent high-throughput workloads, traditional server deployments often remain more cost-effective and operationally simpler. The line between serverless and containers continues to blur with technologies like AWS Fargate and Cloud Run.
