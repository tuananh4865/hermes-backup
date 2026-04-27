---
title: Pub/Sub (Publish/Subscribe)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [architecture, messaging, distributed-systems, event-driven]
---

# Pub/Sub (Publish/Subscribe)

## Overview

Pub/Sub, short for Publish/Subscribe, is a messaging pattern that enables asynchronous communication between components in a distributed system. In this pattern, message senders (publishers) don't send messages directly to specific receivers (subscribers). Instead, they publish messages to named channels or topics, and the messaging infrastructure delivers those messages to all subscribers of that topic. This decoupling is fundamental—it means publishers don't need to know who (if anyone) is listening, and subscribers don't need to know who published the messages they receive.

The publish/subscribe pattern solves several problems in distributed systems. It reduces the coupling between components, allowing them to evolve independently. It enables horizontal scaling, since publishers and subscribers can be added or removed without affecting other parts of the system. It also provides natural fan-out for messages that need to reach multiple recipients.

Modern pub/sub systems like Redis Pub/Sub, Apache Kafka, Amazon SNS/SQS, and Google Cloud Pub/Sub form the backbone of event-driven architectures in companies ranging from startups to large enterprises. They enable use cases like real-time notifications, distributed cache invalidation, microservices coordination, and data streaming pipelines.

## Key Concepts

**Topics (or Channels)**: Messages are organized into named topics that act as message categories. A publisher sends a message to a topic; subscribers receive all messages sent to topics they've subscribed to. Topic naming conventions are important—common patterns include using dots or slashes for hierarchy (e.g., `orders.created`, `user/profile.updated`).

**Publishers**: Components that produce messages and send them to the pub/sub system. Publishers don't know who's consuming their messages. They simply publish with the assurance that the infrastructure will handle delivery.

**Subscribers**: Components that express interest in one or more topics and receive messages published to those topics. Subscribers can subscribe to exact topics or use wildcard patterns to receive messages from multiple related topics.

**Message Broker**: The central infrastructure component that manages topics, handles subscriptions, and delivers messages to subscribers. Different brokers have different characteristics—some emphasize throughput, others durability, others low latency.

**Dead Letter Queues**: When messages can't be delivered or processed, they're sent to a dead letter queue for later inspection and处理. This is essential for debugging and ensuring no messages are permanently lost.

## How It Works

The pub/sub flow works like this:

1. **Subscription**: A subscriber connects to the message broker and subscribes to one or more topics. The broker records this subscription.
2. **Publication**: A publisher creates a message and publishes it to a specific topic. The message includes a payload and metadata (timestamp, message ID, optional headers).
3. **Broker Processing**: The broker receives the message and looks up all active subscriptions for that topic.
4. **Distribution**: The broker delivers the message to each subscriber, typically via a persistent connection or push mechanism.
5. **Acknowledgment**: Subscribers acknowledge receipt and processing of messages. This allows the broker to track which messages have been successfully delivered.

```python
# Example using Redis Pub/Sub (pseudocode)
import redis

# Subscriber setup
def on_order_created(message):
    print(f"New order: {message['order_id']} from {message['customer']}")
    # Process the order notification

pub-sub = redis.pubsub()
pub-sub.subscribe(**{'orders.created': on_order_created})
pub-sub.run_in_thread(sleep_time=0.001)

# Publisher setup
def publish_order_created(order_id, customer, total):
    redis.publish('orders.created', {
        'order_id': order_id,
        'customer': customer,
        'total': total
    })

# Later, when an order is placed:
publish_order_created('ORD-12345', 'Jane Developer', 99.99)
```

## Practical Applications

**Real-time Notifications**: Social media platforms use pub/sub to push likes, comments, and messages to users in real-time. When you receive an instant message, it's likely been delivered through a pub/sub system.

**Distributed Cache Invalidation**: When one service updates data, it publishes an invalidation event. Other services that cache that data subscribe to receive the event and clear their local caches, ensuring consistency without constant database queries.

**Event Sourcing**: Microservices can use pub/sub to broadcast state changes. When an entity changes, it publishes an event. Other services can maintain their own projections of that entity's state by consuming these events.

**Data Pipelines**: ETL (Extract, Transform, Load) workflows often use pub/sub for streaming data between systems. Raw events are published to a topic; transformation services subscribe, process, and publish to new topics for downstream consumers.

## Examples

**Apache Kafka Example**: Kafka's pub/sub model is optimized for high-throughput, durable event streaming:

```java
// Publishing to Kafka
Producer<String, OrderEvent> producer = new KafkaProducer<>(props);
OrderEvent event = new OrderEvent("ORD-123", "CREATED", Instant.now());
producer.send(new ProducerRecord<>("orders", event.getOrderId(), event));

// Subscribing to Kafka
KafkaConsumer<String, OrderEvent> consumer = new KafkaConsumer<>(props);
consumer.subscribe(List.of("orders", "shipments", "returns"));
while (true) {
    ConsumerRecords<String, OrderEvent> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, OrderEvent> record : records) {
        processEvent(record.topic(), record.value());
    }
}
```

**Google Cloud Pub/Sub Example**:

```javascript
// Publisher
const {PubSub} = require('@google-cloud/pubsub');
const pubsub = new PubSub();

async function publishOrder(orderId) {
    const topic = pubsub.topic('orders');
    const publisher = topic.publish({
        data: { orderId, timestamp: Date.now() }
    });
}

// Subscriber
const subscription = pubsub.subscription('order-processor-sub');
subscription.on('message', message => {
    console.log(`Received order: ${message.data.orderId}`);
    message.ack();
});
```

## Related Concepts

- [[messaging]] — General messaging patterns in distributed systems
- [[message-queue]] — Related but typically point-to-point rather than broadcast
- [[event-driven-architecture]] — Architecture pattern that heavily uses pub/sub
- [[rabbitmq]] — Popular message broker supporting pub/sub
- [[kafka]] — High-throughput distributed event streaming platform
- [[microservices]] — Architecture style that benefits from pub/sub communication

## Further Reading

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/) — Deep dive into Kafka's design
- "Designing Data-Intensive Applications" by Martin Kleppmann — Excellent coverage of messaging patterns
- [Redis Pub/Sub Documentation](https://redis.io/docs/interactive/pubsub/) — Lightweight pub/sub usage

## Personal Notes

The elegance of pub/sub is in its simplicity—it fundamentally changes how you think about system communication. Instead of direct service-to-service calls, you have services that react to events. This makes systems more resilient (producers don't crash consumers) and more scalable (you can add subscribers without touching producers). The downside is that it introduces eventual consistency and can make debugging harder since the flow is less obvious.
