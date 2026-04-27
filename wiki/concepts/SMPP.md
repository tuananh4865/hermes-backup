---
title: SMPP
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [smpp, sms, protocol, telecommunications]
---

# SMPP

## Overview

SMPP (Short Message Peer-to-Peer) is a telecommunications industry protocol standard designed for exchanging SMS messages between Short Message Service Centers (SMSCs) and external entities such as mobile networks, application servers, and bulk SMS gateways. Originally developed in the early 1990s by Aldiscon, a company later acquired by Logica, SMPP has become the dominant protocol for SMS transmission in the global telecommunications ecosystem.

The protocol operates at the application layer and typically runs over TCP/IP connections, enabling reliable and persistent communication between SMS gateways and service providers. SMPP is notable for its flexibility, supporting both transmit and receive operations for text messages, as well as binary data for multimedia messaging services. Its peer-to-peer nature means that either party can initiate requests, making it suitable for bidirectional communication scenarios such as two-factor authentication, customer notifications, and interactive messaging services.

SMPP is defined by the SMPP specification, currently maintained as version 3.4 and extended through various addenda. The protocol operates on a client-server model where an External Short Message Entity (ESME) connects to an SMSC, establishing a session that can handle high volumes of messages efficiently. This design has made SMPP the protocol of choice for enterprises and SMS aggregators requiring direct, programmatic access to SMS infrastructure.

## How It Works

SMPP communication follows a request-response pattern over a persistent TCP connection. The protocol defines several primitive operations that govern message submission, delivery, and status reporting.

The primary operation for sending SMS messages is **submit_sm**, which an ESME uses to submit a message to the SMSC for delivery to a mobile recipient. A submit_sm request includes the destination address (typically the recipient's phone number), the source address, the message content encoded in either GSM Default Alphabet or UCS-2 for international character support, and various optional parameters such as validity periods and scheduled delivery times. The SMSC responds with a submit_sm_resp that contains a unique message identifier for tracking purposes.

For receiving messages, the **deliver_sm** operation is used. The SMSC invokes deliver_sm to push incoming messages to an ESME, whether they are mobile-originated messages from subscribers or SMSC delivery receipts confirming that a previously submitted message was successfully delivered, failed, or buffered. The deliver_sm payload mirrors the structure of submit_sm, carrying the sender address, recipient address, and message body.

Additional key operations include **query_sm** for retrieving the delivery status of a previously submitted message, **cancel_sm** for requesting deletion of a message before delivery, and **bind_transceiver** or separate bind_transmitter and bind_receiver operations for establishing the session. The bind operation authenticates the ESME using a system ID and password, negotiating supported features during the session establishment phase.

SMPP supports both synchronous and asynchronous operation modes. In synchronous mode, each request waits for its response before the next request is issued. Asynchronous mode allows multiple requests to be outstanding simultaneously, improving throughput for high-volume applications. The protocol also supports concatenated messages, enabling SMS messages longer than the standard 160-character limit to be split and reassembled transparently.

## Use Cases

SMPP powers a wide range of SMS-based services across telecommunications, financial services, healthcare, and marketing industries.

**Bulk SMS Gateways** represent the most common use case, where aggregators and service providers deploy SMPP connections to send and receive millions of messages daily on behalf of enterprises. These gateways provide the backbone for promotional campaigns, appointment reminders, and transactional notifications such as order confirmations and shipping updates.

**Two-Factor Authentication (2FA)** systems rely on SMPP to deliver time-sensitive one-time passwords (OTPs) via SMS. Organizations in banking, e-commerce, and SaaS platforms integrate with SMSCs through SMPP to deliver secure authentication codes with low latency and high deliverability rates.

**Healthcare Communications** utilize SMPP for patient engagement, including appointment scheduling reminders, prescription refill notifications, and public health alerts. The protocol's reliability and support for priority routing make it suitable for time-sensitive healthcare messaging.

**Enterprise Notification Systems** leverage SMPP for internal communications, IT alerts, and operational notifications. Banks use it for fraud alerts, airlines for flight status updates, and governments for emergency broadcasting systems.

## Related

- [[SMS]] - The underlying messaging service that SMPP transmits
- [[SMSC]] - The Short Message Service Center that manages message storage and delivery
- [[SS7]] - The signaling network underlying traditional SMS routing
- [[HTTP SMS API]] - Alternative protocols for SMS integration, often wrapping SMPP internally
- [[GSM]] - The mobile communications standard that defines SMS encoding
- [[SS7]] - The telephony signaling infrastructure used for legacy SMS routing
- [[SMS Gateway]] - The broader concept of systems that bridge SMS with other communications channels
