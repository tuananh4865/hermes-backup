---
title: "Webhooks"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [webhooks, events, api, http]
---

# Webhooks

## Overview

Webhooks are a lightweight HTTP-based mechanism for event-driven communication between applications. Unlike traditional API polling, where a client repeatedly requests updates from a server, webhooks enable servers to proactively push notifications to clients when specific events occur. This pattern is often described as "reverse API" or "HTTP callbacks" because the server initiates the request to the client's endpoint rather than waiting for the client to ask for data.

Webhooks are fundamental to modern distributed systems, enabling loose coupling between services and real-time data synchronization across platforms.

## How It Works

The webhook workflow follows a straightforward request-response cycle:

1. **Registration**: The client application registers a publicly accessible URL endpoint with the source service. This endpoint is typically an HTTPS URL on the client's server.

2. **Event Trigger**: When a defined event occurs in the source service (such as a payment being processed, a file being uploaded, or a user updating their profile), the service prepares an HTTP POST request.

3. **Payload Delivery**: The source service sends an HTTP POST to the registered endpoint containing a JSON or XML payload with event data. The request includes headers such as `Content-Type` and often a signature header for verification.

4. **Processing**: The receiving server processes the payload, performs necessary actions, and returns an HTTP status code (typically `200 OK` or `201 Created`). If the endpoint returns an error status code, the source service may retry delivery based on its retry policy.

## Use Cases

Webhooks power a wide range of real-world applications:

- **Payment Processing**: Services like Stripe and PayPal send webhooks to notify merchant systems when payments succeed, fail, or require disputed action.
- **Version Control**: GitHub and GitLab dispatch webhooks to trigger CI/CD pipelines, notify external systems of code pushes, or update project management tools.
- **Communication Platforms**: Slack and Discord use webhooks to post messages from bots and external services into channels.
- **E-commerce**: Online stores receive instant notifications when orders are placed, shipped, or delivered.
- **Automation Workflows**: Tools like Zapier and IFTTT rely heavily on webhooks to connect disparate applications and automate repetitive tasks.

## Security

Webhook endpoints are publicly exposed, so implementing proper security measures is critical:

- **Signature Verification**: Most providers include a cryptographic signature in the request header (such as `X-Hub-Signature-256`). The receiving server recomputes the signature using a shared secret and compares it to detect tampering.
- **HTTPS Endpoints**: Always serve webhook endpoints over HTTPS to encrypt data in transit and prevent man-in-the-middle attacks.
- **Idempotency**: Design handlers to handle duplicate deliveries gracefully, as source services may retry failed deliveries.
- **Input Validation**: Validate all incoming payload fields and reject malformed requests before processing.

## Related

- [[API]] — Webhooks are often used to supplement traditional REST APIs
- [[HTTP]] — The protocol that powers webhook communication
- [[Event-Driven Architecture]] — The broader architectural pattern webhooks exemplify
- [[JSON]] — The common data format for webhook payloads
