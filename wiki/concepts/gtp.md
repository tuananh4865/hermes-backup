---
title: "GTP (GPRS Tunneling Protocol)"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [networking, protocol, telecom, mobile, gprs]
---

# GTP (GPRS Tunneling Protocol)

## Overview

GPRS Tunneling Protocol (GTP) is a group of IP-based communication protocols used primarily in 2G, 3G, and 4G mobile networks to tunnel data packets between base stations (Radio Access Network) and core network elements. GTP enables the transport of user data packets (as defined by the Internet Protocol) over the mobile backbone, and it plays a critical role in mobility management, session management, and quality of service enforcement. The protocol operates at the GTP level within the GPRS Core Network architecture, specifically on the Gn and Gi interfaces. There are two main variants: GTP-U (User Plane) for transporting user data, and GTP-C (Control Plane) for signaling and session management. GTP is defined by the 3GPP (3rd Generation Partnership Project) and has evolved through multiple versions, with GTPv1 and GTPv2 being the most widely deployed.

## Key Concepts

**GTP-U (User Plane Tunnel)**: Transports actual end-user data packets between the Serving GPRS Support Node (SGSN) and Gateway GPRS Support Node (GGSN), as well as between other network elements. Each user data flow is associated with a unique Tunnel Endpoint Identifier (TEID) that identifies the GTP tunnel.

**GTP-C (Control Plane Tunnel)**: Handles control signaling including session creation, modification, and deletion. GTP-C messages manage tunnel establishment, PDP (Packet Data Protocol) context operations, and path management between network elements.

**TEID (Tunnel Endpoint Identifier)**: A 32-bit identifier assigned by the receiving GTP node to uniquely identify a specific tunnel. Every GTP packet contains a TEID field that allows the receiver to route the packet to the correct context.

**GTP' (GTP Prime)**: A variant used for charging data transport, forwarding billing records from the GGSN to the Charging Gateway Function (CGF).

**GTP-C and Diameter**: In modern 4G LTE networks (EPC architecture), GTP is often compared or interworked with Diameter protocol for AAA (Authentication, Authorization, and Accounting) signaling.

## How It Works

In a typical GPRS/UMTS network, when a mobile device initiates a data session, the following occurs:

1. The mobile sends an Activate PDP Context Request to the SGSN
2. The SGSN creates a session and sends a Create PDP Context Request to the GGSN via GTP-C
3. The GGSN allocates resources, assigns an IP address to the mobile, and creates a GTP tunnel
4. A TEID is assigned and communicated back to the SGSN
5. User data flows through the established GTP tunnel between SGSN and GGSN using GTP-U

```text
Mobile Device <--Radio--> NodeB/BTS <--Gb--> SGSN <--Gn--> GGSN <--Gi--> Internet
                                    ^                      ^
                                    |                      |
                                  GTP-C/GTP-U            GTP-U
```

GTP operates over UDP (port 2123 for GTP-C, port 2152 for GTP-U) on IPv4 or IPv6 transport networks. The protocol header includes a TEID, sequence number, and message type, allowing reliable delivery and proper context lookup.

## Practical Applications

GTP is fundamental to all cellular data networks. In 4G LTE networks, GTP-v2-C is used on the S5/S8 interfaces between the MME/S-GW and P-GW for session management. GTP tunnels enable:

**Mobile Data Offloading**: Telecom operators use GTP to route data traffic between network elements, applying QoS policies based on subscription tiers and service type.

**Roaming**: When a mobile device roams to a visited network, GTP tunnels carry user data back to the home network or locally toward the internet.

**Lawful Interception**: GTP interfaces can be tapped by authorized agencies to monitor communications for security purposes.

**Network Virtualization**: In modern architectures like mobile edge computing (MEC), GTP-U is used to steer traffic to local breakout points for low-latency applications.

## Examples

A GTP-C Create Session Request message structure:

```text
Version: 1
Message Type: Create Session Request (0x20)
TEID: 0x00000001
Sequence Number: 0x00 01 02
Message: Create Session Request
  - IMSI: 001001123456789
  - MSISDN: 1234567890
  - RAT Type: EUTRAN
  - PDN Type: IPv4
  - APN: internet
```

## Related Concepts

- [[GPRS]] - The network architecture where GTP is used
- [[4G LTE]] - Modern network using GTP-v2
- [[SGSN]] - The Serving GPRS Support Node
- [[GGSN]] - The Gateway GPRS Support Node
- [[Diameter Protocol]] - Alternative AAA protocol in LTE
- [[Mobile Core Network]] - The broader system GTP operates within
