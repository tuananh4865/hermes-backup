---
title: SMS (Short Message Service)
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [sms, messaging, notifications, telecom]
---

## Overview

SMS (Short Message Service) is a text messaging protocol that allows users to send and receive short text messages over cellular networks. Originally designed as part of the GSM (Global System for Mobile Communications) standard in 1984, SMS enables the exchange of messages containing up to 160 characters of text using the Signaling System 7 (SS7) network. Despite the advent of internet-based messaging applications, SMS remains a critical communication channel due to its universal reach, reliability, and independence from internet connectivity. Virtually all mobile phones support SMS, making it one of the most widely accessible communication technologies in the world.

## Protocols

SMS operates through several key protocols that facilitate message delivery across cellular networks.

**SMPP** (Short Message Peer-to-Peer) is an application layer protocol used for exchanging SMS messages between Short Message Service Centers (SMSCs) and external entities such as mobile networks, applications, and aggregators. SMPP supports both submission and delivery of messages and is the dominant protocol for high-volume SMS traffic. It operates typically over TCP/IP connections and provides features like scheduled delivery, priority messaging, and multi-part message handling.

**SS7** (Signaling System 7) is a set of telephony signaling protocols that forms the backbone of traditional telecom networks. In SMS context, SS7 handles the routing of messages between the SMSC and the recipient's mobile device through the Mobile Switching Center (MSC). SS7 manages the signaling required to locate subscribers, set up connections, and deliver SMS notifications to active handsets.

## Use Cases

SMS serves numerous practical applications across consumer, enterprise, and security domains.

**Notifications** represent one of the most prevalent uses of SMS. Financial institutions send transaction alerts, e-commerce platforms dispatch order updates, and healthcare providers deliver appointment reminders via text messages. SMS notifications are valued for their high open rates and reliability compared to email.

**Two-Factor Authentication (2FA)** relies heavily on SMS to deliver one-time passwords (OTPs) for account security. Many online services send verification codes to users' mobile numbers as a second layer of authentication, leveraging the assumption that access to a phone number indicates the user's identity.

**Marketing** is another significant use case, with businesses sending promotional offers, discounts, and loyalty program updates directly to consumers. SMS marketing achieves higher engagement rates than email due to the immediacy and personal nature of text messages.

## Alternatives

Several alternatives to traditional SMS have emerged over the years.

**MMS (Multimedia Messaging Service)** extends SMS by supporting the exchange of multimedia content including images, videos, and audio, though it maintains similar delivery infrastructure.

**RCS (Rich Communication Services)** is a protocol that provides a richer messaging experience with features like group chat, read receipts, file sharing, and high-resolution image exchange. RCS is considered the successor to SMS/MMS in modern smartphones.

**Internet-based messaging applications** such as WhatsApp, Telegram, and Signal offer free messaging using data connections, bypassing traditional cellular networks entirely.

## Related

- [[MMS]] - Multimedia Messaging Service
- [[RCS]] - Rich Communication Services
- [[SMPP]] - Short Message Peer-to-Peer Protocol
- [[SS7]] - Signaling System 7
- [[Push Notifications]] - Alternative delivery mechanism for alerts
- [[Two-Factor Authentication]] - Security concept commonly implemented with SMS
