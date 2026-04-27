---
title: "Diameter"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [networking, protocol, AAA, authentication, telecom, diameter]
---

# Diameter

## Overview

Diameter is a next-generation Authentication, Authorization, and Accounting (AAA) protocol widely used in telecommunications and network infrastructure. It serves as the foundation for modern services like LTE/4G voice and data, IMS (IP Multimedia Subsystem), and carrier-grade session management. The name "Diameter" is a pun on the RADIUS protocol (which Diameter was designed to replace and improve upon) — just as a diameter is "twice the radius," Diameter is essentially double the functionality of RADIUS. Diameter operates as a peer-to-peer protocol using TCP or SCTP as its transport layer, providing reliable message delivery with support for TLS security. It is defined in RFC 6733 and has become the de facto standard for AAA in 3GPP networks worldwide.

## Key Concepts

**Peer-to-Peer Architecture** — Unlike RADIUS's client-server model where network devices (NAS) act as clients talking to a RADIUS server, Diameter uses a true peer-to-peer model. Any Diameter node can act as either a client, server, or agent. This flexibility allows for complex network topologies including proxy, redirect, and relay agents.

**Avp (Attribute-Value Pairs)** — All Diameter messages are composed of AVPs, which are the fundamental building blocks of the protocol. Each AVP carries a piece of information — a user identity, an authorization result, a billing record, or any other piece of data. AVPs have a standardized header format with an AVP code, vendor ID, and data type.

**Applications** — Diameter is not a single monolithic protocol but a base protocol extended by specialized applications. Each application (e.g., NASREQ, SIP, Credit-Control) defines additional AVPs and state machines. The base protocol provides common functions like capabilities exchange and device watchdog.

**Diameter Agents** — Three types of agents extend the base protocol:

- **Relay Agents** — Forward messages based on routingAVP contents without inspecting message content
- **Proxy Agents** — Apply policy decisions, such as load balancing or access control
- **Redirect Agents** — Send clients to a specific server, acting like a DNS for Diameter

## How It Works

A typical Diameter session establishment and authentication flow:

1. **CER/CEA (Capabilities Exchange)** — Two Diameter peers exchange capabilities at TCP/SCTP connection startup to agree on supported applications and security mechanisms
2. **Device-Watchdog (DWA/DWR)** — Peers periodically exchange watchdog messages to detect connection failures
3. **Authentication Request (AAR)** — A client (e.g., LTE eNodeB) sends an authentication request to the Diameter server
4. **AAA Response (AAA)** — The server validates credentials and returns authorization result
5. **Accounting Request (ACR)** — Usage data (bytes transferred, session duration) is sent periodically to the accounting server
6. **Session Termination (STR/STA)** — When the session ends, a termination request/answer pair cleanly closes the session

## Practical Applications

- **LTE/4G Networks** — Diameter is integral to 3GPP networks, carrying authentication between the UE (User Equipment) and the HSS (Home Subscriber Server) via the S6a interface
- **VoLTE and VoWiFi** — Voice over LTE uses Diameter for call session setup and policy control
- **Roaming** — Diameter-based peering between carriers enables seamless roaming for subscribers
- **Policy and Charging Control (PCC)** — Diameter interfaces like Gx and Rx enforce quality of service and billing rules
- **Enterprise VPN** — Used in large-scale network access control systems

## Examples

A simplified Diameter authentication exchange:

```text
// AAR - Authentication Authorization Request
< AVP Code: 1 >         // User-Name = "alice@example.com"
< AVP Code: 264 >      // Host-IP-Address
< AVP Code: 257 >      // Auth-Application-Id = 4 (NASREQ)

// AAA - Authentication Authorization Answer
< AVP Code: 257 >      // Auth-Application-Id
< AVP Code: 268 >      // Result-Code = 2001 (Success)
< AVP Code: 33 >       // Framed-IP-Address = 10.0.1.45
```

## Related Concepts

- [[RADIUS]] — The predecessor protocol to Diameter with more limited capabilities
- [[AAA]] — Authentication, Authorization, and Accounting — the framework Diameter implements
- [[LTE]] — Long Term Evolution mobile network that uses Diameter extensively
- [[HSS]] — Home Subscriber Server, the LTE database that Diameter queries
- [[SIP]] — Session Initiation Protocol, often paired with Diameter in VoIP/VoLTE deployments

## Further Reading

- [RFC 6733 - Diameter Base Protocol](https://datatracker.ietf.org/doc/html/rfc6733) — The definitive specification
- [Diameter Protocol Explained](https://www.eventhelix.com/telecom/diameter/) — Practical walkthroughs
- [3GPP TS 29.229](https://www.3gpp.org/) — Cx/Dx interfaces using Diameter for IMS

## Personal Notes

Diameter clicked for me when I started thinking about it not as a single protocol but as a protocol framework with a base layer and many application-specific extensions. The AVP concept is elegant — it provides a standardized way to extend the protocol without breaking backward compatibility. In telecom networks, Diameter is everywhere, and understanding it is essential for anyone working on 4G/5G core network integration or carrier peering.
