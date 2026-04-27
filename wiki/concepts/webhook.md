---
title: "Webhook"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [webhook, api, event, http, integration, event-driven]
---

# Webhook

## Overview

A webhook is an HTTP-based callback mechanism that allows one software system to notify another system when a specific event occurs. Unlike traditional API calls where a client polls a server to check for new data, a webhook inverts the flow—the server pushes data to the client automatically the moment an event fires. This event-driven pattern reduces latency, eliminates wasteful polling, and enables loosely coupled integrations between services.

When an event occurs in the source system (e.g., a payment is processed, a user signs up, a file is uploaded), the system makes an HTTP POST request to a pre-registered URL belonging to the consuming system, sending a payload that describes the event. The consumer processes the payload and returns an HTTP response (typically 200 OK) to acknowledge receipt. This simple request-response contract is the backbone of countless integrations across the web.

## Key Concepts

**Endpoint Registration**

The consumer registers a webhook URL with the provider. This is typically done through a provider's UI (e.g., GitHub webhooks settings, Stripe dashboard) or API. The provider stores the URL and associates it with the account or resource.

**Event Types**

Providers define a catalog of events that can trigger webhooks: `user.created`, `payment.succeeded`, `file.uploaded`, `deployment.completed`. Consumers subscribe to the specific events they care about. Some providers support filtering via wildcard patterns or payload path expressions.

**Payload Format**

Payloads are almost always JSON (or XML in older systems). They contain a description of the event: what happened, when, and what resources are affected. Most providers include a header indicating the event type (`X-Event-Type`, `Stripe-Event`, etc.) so consumers can route handling logic.

**Signature Verification**

Since webhook endpoints are publicly accessible URLs, providers typically sign each request using a shared secret (HMAC-SHA256). The consumer verifies the signature before processing, preventing spoofed webhook deliveries. This is critical for security.

**Retry and Delivery Guarantees**

Providers generally guarantee "at-least-once" delivery: if the consumer's endpoint returns a non-2xx response or times out, the provider retries with exponential backoff over hours or days. Consumers must handle duplicate deliveries idempotently.

**Idempotency**

Because webhooks may be delivered more than once, consumers must process events idempotently—applying the same event multiple times has the same effect as applying it once. This is typically achieved by tracking already-processed event IDs.

## How It Works

```
# Typical webhook flow
# 1. Provider has a configured webhook URL: https://api.example.com/webhooks/stripe
# 2. User pays via Stripe
# 3. Stripe detects payment success event
# 4. Stripe POSTs to https://api.example.com/webhooks/stripe

# Example webhook payload (Stripe)
POST /webhooks/stripe HTTP/1.1
Host: api.example.com
Content-Type: application/json
Stripe-Signature: t=1614556800,v1=5257a869e7ecebeda32affa62cdca3fa
X-Stripe-Event: payment_intent.succeeded

{
  "id": "evt_123",
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_456",
      "amount": 2000,
      "currency": "usd"
    }
  }
}

# 5. Consumer verifies signature, processes event, returns 200 OK
```

```python
# Flask webhook endpoint example (Python)
from flask import Flask, request, abort
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "whsec_your_secret"

@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    event = None

    # Verify signature
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError:
        abort(400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        abort(400)  # Invalid signature

    # Handle event idempotently
    if event['id'] in processed_event_ids:
        return '', 200

    event_type = event['type']
    if event_type == 'payment_intent.succeeded':
        handle_payment(event['data']['object'])
    elif event_type == 'customer.subscription.deleted':
        handle_cancellation(event['data']['object'])

    processed_event_ids.add(event['id'])
    return '', 200
```

## Practical Applications

Webhooks are the integration fabric of modern software:

- **Payment processing** — Stripe, PayPal, Square send webhooks for payment events to update order status, issue receipts, trigger fulfillment
- **Version control** — GitHub, GitLab, Bitbucket send webhooks on push, pull request, and merge events to trigger CI/CD pipelines
- **SMS/Notification platforms** — Twilio, Vonage send webhooks for inbound messages and delivery receipts
- **E-commerce platforms** — Shopify sends webhooks for orders, fulfilled shipments, and inventory changes
- **Monitoring and alerting** — PagerDuty, OpsGenie can send webhooks to invoke custom remediation scripts

## Examples

- **GitHub Webhooks** — POST to configured URL on push, PR, issue, release events; used for CI/CD, chat notifications, automated code review
- **Stripe** — Comprehensive webhook system for payment lifecycle events; well-documented with SDK support for signature verification
- **Twilio** — HTTP callbacks for incoming SMS/MMS/voice calls
- **SendGrid** — Event webhooks for email deliverability events (bounce, spam, unsubscribe)
- **Slack** — Incoming webhooks (one-way) and event subscriptions (bidirectional) for building integrations

## Related Concepts

- [[web-api]] — Webhooks are a specific pattern within the broader [[API]] landscape
- [[http]] — Webhooks are fundamentally HTTP POST requests; understanding HTTP headers, status codes, and TLS is essential
- [[callbacks]] — Webhooks are a specific form of callback (an HTTP-reverse callback) for event notification
- [[idempotency]] — Critical concept for reliable webhook processing
- [[Serverless-Functions]] — Webhook endpoints are commonly implemented as serverless functions (AWS Lambda, Cloudflare Workers) that scale to zero and handle intermittent traffic

## Further Reading

- Stripe Webhooks Documentation — gold standard for webhook API design
- GitHub Webhooks Documentation — comprehensive guide to repository event webhooks
- "Webhook Best Practices" — Postman's guide to designing and consuming webhooks reliably

## Personal Notes

The two biggest webhook gotchas I've encountered: (1) processing logic that isn't idempotent, leading to double-charges or duplicate records when a provider retries after a timeout, and (2) firewalls or load balancers that have idle connection timeouts shorter than the retry interval, silently dropping webhooks. Always verify webhook signatures, always return 200 fast (do async processing), and always track event IDs to detect duplicates. For production systems, a webhook processing queue (SQS, Kafka) between the endpoint and your business logic is a worthwhile buffer.
