---
title: FaaS (Functions as a Service)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [faas, serverless, cloud-computing, aws-lambda, functions, event-driven]
---

# FaaS (Functions as a Service)

## Overview

Functions as a Service (FaaS) is a cloud computing service model that enables developers to execute application code in response to events without managing the underlying server infrastructure. FaaS represents the most abstracted layer of cloud computing, where the cloud provider handles all aspects of server provisioning, scaling, and management. Developers simply write functions—small, stateless units of computation—and deploy them to the platform, which executes them on demand.

FaaS is often synonymous with [[Serverless]] computing, though serverless is a broader concept encompassing any managed service where the provider dynamically allocates resources. FaaS specifically refers to the execution model where individual functions are the unit of deployment and billing. This model has transformed application architecture, enabling event-driven designs and dramatically reducing operational overhead for many workloads.

The major cloud providers offer FaaS products: AWS Lambda, Google Cloud Functions, Azure Functions, and IBM Cloud Functions (based on Apache OpenWhisk). Each provides similar core functionality with varying capabilities around languages supported, execution environments, scaling behavior, and integration with other cloud services.

## Key Concepts

**Event-Driven Execution** is the foundation of FaaS. Functions are triggered by events from various sources: HTTP requests, database changes, queue messages, file uploads, scheduled timers, or custom events from other cloud services. This event-driven model naturally aligns with microservices architectures and enables loose coupling between system components.

**Stateless Functions** are the execution model in FaaS—each function invocation is independent and does not retain state between calls. Any required state must be retrieved from external storage (databases, caches, object storage). This constraint simplifies scaling but requires careful design when state needs to be preserved.

**Cold Starts** occur when a function is invoked after being idle, requiring the platform to initialize the execution environment. Cold start latency can range from milliseconds to seconds depending on the runtime, language, and function configuration. Warm starts reuse an already-initialized environment, providing much faster response times.

**Execution Timeout** limits how long a function can run before being terminated. Most FaaS platforms default to a few seconds to minutes, making FaaS unsuitable for long-running workloads. Extended execution requires alternative approaches like Step Functions or longer timeout configurations.

**Concurrency Limits** define how many simultaneous executions of a function are allowed. Default limits protect the platform but can be increased upon request. Understanding concurrency is essential for high-throughput applications.

**Pricing Model** in FaaS is typically based on the number of invocations and the execution duration (with granularity in milliseconds or 100ms increments). This pay-per-use model can be dramatically cheaper than always-on servers for sporadic workloads, but costs can escalate unexpectedly for high-volume, continuous workloads.

## How It Works

When a function is deployed to a FaaS platform, it is packaged with its dependencies and registered with the event sources that should trigger it. The platform prepares execution environments in a pool, ready to handle invocations.

```javascript
// Example: AWS Lambda function in Node.js
exports.handler = async (event, context) => {
  // event contains the triggering data (HTTP request, S3 object, etc.)
  // context provides information about the execution environment
  
  const { name } = event.queryStringParameters || { name: 'World' };
  
  return {
    statusCode: 200,
    body: JSON.stringify({
      message: `Hello, ${name}!`,
      timestamp: new Date().toISOString()
    })
  };
};
```

When an event occurs, the platform:
1. Selects an available execution environment from the pool (or creates a new one for cold starts)
2. Loads and initializes the function (if not already loaded)
3. Invokes the handler with the event data
4. Returns the result to the calling service
5. Returns the execution environment to the pool for reuse

Scaling happens automatically—the platform instantiates additional execution environments as needed to handle concurrent events, up to the configured concurrency limit.

## Practical Applications

**API Backends** benefit from FaaS when requests are sporadic. Each HTTP request triggers a function execution, and the platform scales automatically. Combined with API Gateway, FaaS provides a cost-effective way to expose serverless APIs.

**Data Processing Pipelines** use FaaS for tasks like image resizing, video transcoding, or log processing. Events from object storage (S3, GCS) trigger functions that process files and store results, often in a different storage location.

**Real-time File Processing** handles uploads by triggering functions that validate, transform, or extract metadata from files as they arrive. This pattern is common for handling profile photos, document uploads, and media files.

**Scheduled Tasks and Cron Jobs** replace polling loops with scheduled function invocations. Instead of a server running continuously to execute periodic tasks, a function runs on a schedule and terminates when complete.

**Webhook Handlers** receive incoming HTTP callbacks from external services (payment processors, social media, IoT devices) and process them without maintaining persistent infrastructure.

## Examples

**AWS Lambda** supports Node.js, Python, Ruby, Java, Go, .NET, and custom runtimes. It integrates deeply with AWS services and offers features like provisioned concurrency for consistent latency.

**Azure Functions** supports similar languages and provides durable functions for stateful workflows. It uses an App Service plan for consistent scaling or a consumption plan for pay-per-use.

**Google Cloud Functions** (now Cloud Run Functions) prioritizes simplicity and integrates well with Google Cloud services. Second-generation functions offer better performance and more configuration options.

```yaml
# Example: Serverless Framework configuration (serverless.yml)
service: my-function-service

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1

functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: hello/{name}
          method: get
  processUpload:
    handler: handler.processUpload
    events:
      - s3:
          bucket: uploads-bucket
          event: s3:ObjectCreated:*
```

## Related Concepts

- [[Serverless]] — Broader concept of managed, event-driven computing
- [[AWS Lambda]] — AWS's FaaS offering
- [[Event-Driven Architecture]] — Design patterns that complement FaaS
- [[Microservices]] — Architecture style often paired with FaaS
- [[Cloud Computing]] — The umbrella paradigm containing FaaS

## Further Reading

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Azure Functions Documentation](https://docs.microsoft.com/azure/functions/)
- [Serverless Framework Documentation](https://www.serverless.com/framework/docs/)

## Personal Notes

FaaS is powerful for certain use cases but has surprising costs at scale. A function running millions of times per day can exceed the cost of a small always-on server. I've found FaaS shines brightest for event-driven workloads with unpredictable traffic patterns—webhooks, file processing, scheduled tasks—rather than high-volume continuous APIs where the per-invocation overhead accumulates significantly.
