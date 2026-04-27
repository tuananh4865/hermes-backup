---
title: SS7
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ss7, telecom, signaling, security]
---

# SS7

## Overview

SS7 (Signaling System 7) is a set of signaling protocols defined by the ITU-T that manages the setup, coordination, and teardown of telephone calls across the Public Switched Telephone Network (PSTN). Originally developed in the 1970s as a digital out-of-band signaling standard, SS7 operates separately from the voice channels it controls, enabling efficient and reliable call management across disparate telecommunications switches worldwide.

Before SS7, telephone networks relied on in-band signaling — using the same frequencies as voice traffic — which was slow, prone to interference, and offered no separation between control information and actual call content. SS7 revolutionized telecom by introducing an out-of-band network dedicated entirely to signaling. This separation allowed call setup times to drop dramatically, enabled new revenue-generating services, and laid the foundation for modern voice networking including early SMS delivery, toll-free calling, and local number portability.

SS7 forms the backbone of intellige

nt network services and sits at the core of both wireline and wireless (GSM/UMTS) infrastructure. It is responsible for translating phone numbers into routing paths, establishing connections between switches, negotiating call features, and facilitating billing record generation. Without SS7, modern telecommunications features such as call forwarding, conference calling, call waiting, and automatic roaming would not function at scale.

## Architecture

SS7 architecture consists of three primary functional components that work together to deliver signaling services across the PSTN.

**Signal Switching Points (SSPs)** are the network switches — typically telephone exchanges — that originate, terminate, or route signaling messages. An SSP detects events such as a call initiation or a subscriber going off-hook, generates SS7 messages in response, and sends them across the network to coordinate call processing with other switches. Every SSP is identified by a unique point code that allows messages to be correctly addressed and delivered.

**Signal Transfer Points (STPs)** act as packet-switching nodes in the SS7 network. Unlike SSPs, STPs do not terminate calls; instead, they route signaling messages between SSPs. STPs provide network intelligence by supporting load balancing, failover routing, and global title translation — the ability to rewrite destination addresses so messages can reach subsystems regardless of their physical location. STPs are typically deployed in mated pairs for redundancy.

**Service Control Points (SCPs)** are database nodes that provide intelligent query-and-response services. When an SSP needs to determine how to route a toll-free call, perform a lawful intercept, or query subscriber information for call forwarding, it sends an SS7 query to an SCP. The SCP consults its database and returns a response that guides the SSP's decision. Mobile networks use SCPs extensively for Subscriber Identity Modules authentication and Short Message Service Center routing.

The messages themselves are organized into a layered protocol stack similar to the OSI model, comprising MTP (Message Transfer Part) for network layer delivery, SCCP (Signaling Connection Control Part) for addressing and connectionless/connection-oriented services, and user parts such as ISUP (ISDN User Part) for call setup and management, and MAP (Mobile Application Part) for mobile network operations.

## Vulnerabilities

SS7 was designed in an era when the telecommunications network was a closed, trusted environment. The founding assumption — that only authorized carriers with physical access to the signaling infrastructure would transmit SS7 messages — turned out to be fundamentally flawed. This trust-based design has become one of the most significant sources of security weakness in modern telecommunications.

The most severe vulnerability is the absence of authentication. SS7 messages contain no cryptographic signature or verification mechanism, meaning any node that can inject messages into the SS7 network can trigger call rerouting, retrieve subscriber location data, or intercept communications without detection. This flaw has been actively exploited since at least 2008 when researchers first demonstrated practical attacks, and it remains unpatched in many carrier networks globally.

**Location Tracking** is a straightforward exploit: an attacker sends a Provide Subscriber Information message to an SSP, requesting the current cell tower of a target mobile subscriber. Because SS7 lacks authentication, the network accepts the query and returns the subscriber's location. Repeated queries enable real-time tracking of individuals without their knowledge or consent.

**Call Interception** exploits weaknesses in the call setup sequence. An attacker positioned on the SS7 network can manipulate Initial Address Messages to redirect an established call through a third-party node under their control. This allows silent eavesdropping on voice calls without alerting either party. The same technique can be used to reroute SMS messages, enabling OTP (one-time password) theft for banking fraud.

**Denial of Service** attacks can be launched by flooding a subscriber's SSP with signaling requests, causing the node to exhaust resources and drop legitimate traffic. Because SS7 lacks rate limiting or validation mechanisms, a modest number of malicious messages can disrupt service for an entire region.

Countermeasures include SS7 firewalls (deep packet inspection gateways that filter malformed or suspicious messages), GTP (an alternative protocol with stronger security for 4G/5G networks), and encryption-based protocols such as Diameter with TLS. However, legacy SS7 infrastructure persists extensively, meaning the attack surface remains large and active.

## Related

- [[PSTN]] — The Public Switched Telephone Network that SS7 operates within
- [[ISUP]] — ISDN User Part, the SS7 protocol for managing voice call setup
- [[MAP]] — Mobile Application Part, the SS7 protocol for GSM/UMTS mobile network signaling
- [[Diameter]] — A more modern AAA protocol often replacing SS7 in LTE/5G networks
- [[GTP]] — GPRS Tunneling Protocol, another mobile signaling protocol used in 3G and beyond
- [[SS7 Firewall]] — Security appliances designed to detect and block malicious SS7 traffic
- [[Signaling Protocol]] — The broader category of protocols that manage session setup in telecommunications
