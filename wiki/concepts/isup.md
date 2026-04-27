---
title: "Isup"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [networking, telecommunications, protocols, signaling, telephony]
---

# Isup

## Overview

ISUP (ISDN User Part) is a signaling protocol used in public switched telephone networks (PSTN) to set up, manage, and tear down telephone calls. It operates within the SS7 (Signaling System No. 7) protocol suite, which provides out-of-band signaling for telecommunications networks. ISUP defines the messages and procedures for establishing voice calls, as well as supplementary services like call waiting, call forwarding, and number translation across telephone switches.

While traditional circuit-switched telephone networks are being replaced by VoIP and modern IMS (IP Multimedia Subsystem) architectures, ISUP remains historically significant and continues to operate in legacy PSTN infrastructure worldwide. Understanding ISUP provides insight into how traditional telephony call control works and how modern protocols evolved from these foundations.

## Key Concepts

**Call Setup**: ISUP handles the exchange of IAM (Initial Address Message), ACM (Address Complete Message), and ANM (Answer Message) to establish a voice circuit between two exchanges.

**Call Teardown**: Release messages (REL) and Release Complete (RLC) messages gracefully terminate connections and free network resources.

**Circuit Identification**: Each voice channel is identified by a CIC (Circuit Identification Code) that maps to specific time slots on E1/T1 carrier systems.

**Parameter Structures**: ISUP messages contain mandatory and optional parameters carrying called/calling party numbers, call type, bearer capability, and user-to-user information.

**Variants**: Different regional variants exist—ANSI ISUP in North America, ITU-T ISUP internationally, and ETSI ISUP in Europe—though they share similar structures.

## How It Works

1. **Call Initiation**: The originating switch sends an IAM containing the called number, calling number, and selected circuit. This reserves a voice path through intermediate switches.

2. **Path Setup**: Each intermediate switch receives the IAM, reserves its outgoing circuit, and forwards the message with updated CIC information.

3. **Call Answer**: The terminating switch sends an ACM back through the path when the called party answers, then sends ANM when the call is connected.

4. **Call Release**: When either party hangs up, a REL is sent back through the path, freeing each circuit segment until an RLC confirms release.

```text
Originating                     Intermediate                  Terminating
  Switch                            Switch                         Switch
    │                                 │                               │
    │──── IAM (CIC:5, called:1234) ──►│                               │
    │                                 │──── IAM (CIC:3, called:1234) ►│
    │                                 │                               │
    │◄── ACM (CIC:5)──────────────────│◄─── ACM (CIC:3)───────────────│
    │                                 │                               │
    │◄── ANM (CIC:5)──────────────────│◄─── ANM (CIC:3)───────────────│
    │                                 │                               │
    │    Voice Path Established       │                               │
    │◄══════════════════════════════════════════════════════════════►│
    │                                 │                               │
    │──── REL (CIC:5)────────────────►│                               │
    │◄─── RLC (CIC:5)─────────────────│──── REL (CIC:3) ─────────────►│
    │                                 │◄─── RLC (CIC:3)───────────────│
```

## Practical Applications

- **Traditional PSTN Call Control**: Managing voice calls across telephone company switches
- **SS7 Network Services**: Supporting toll-free numbers, local number portability, and number portability
- **Legacy VoIP Gateways**: Interworking between PSTN and VoIP using ISUP at the boundary
- **Telecom Network Testing**: Analyzing ISUP traffic to diagnose call setup failures and network issues
- **Billing and Auditing**: Extracting call records from ISUP messages for inter-carrier settlement

## Examples

Decoding an ISUP IAM message structure:

```hex
# IAM (Initial Address Message) - Typical hex dump
03 01 0A 03 01 0A 0B 0C 00 80 01 01 
│  │  │  │  │  │  │  │  │  │  │  └── Called Party Number (variable)
│  │  │  │  │  │  │  │  │  │  └────── Calling Party Number (optional)
│  │  │  │  │  │  │  │  │  └───────── User-to-User Info (optional)
│  │  │  │  │  │  │  │  └──────────── Circuit Identification Code
│  │  │  │  │  │  │  └─────────────── Nature of Connection Indicator
│  │  │  │  │  │  └────────────────── Forward Call Indicator
│  │  │  │  │  └───────────────────── Message Type (IAM)
│  │  │  └─────────────────────────── Destination Point Code
│  └───────────────────────────────── Originating Point Code
```

Using Python to parse basic ISUP information (pseudocode):

```python
# Pseudocode for ISUP message parsing
def parse_isup_iam(hex_data):
    """Parse basic fields from ISUP Initial Address Message"""
    msg_type = int(hex_data[2], 16)  # Message type
    
    # Skip to Called Party Number parameter
    cpn_param = find_parameter(hex_data, 0x0C)  # Called Party Number tag
    cpn_length = int(cpn_param[2], 16)
    cpn_digits = cpn_param[3:3+cpn_length] & 0x7F  # Remove parity bit
    
    return {
        "message_type": "IAM",
        "called_number": digits_to_string(cpn_digits)
    }
```

## Related Concepts

- [[SS7]] - Signaling System No. 7, the transport layer for ISUP
- [[PSTN]] - Public Switched Telephone Network, traditional phone infrastructure
- [[SIP]] - Session Initiation Protocol, modern VoIP call control protocol
- [[E1 T1]] - Digital carrier systems used for voice transmission
- [[Signaling Protocols]] - Methods for exchanging call control information

## Further Reading

- [ITU-T Q.761 - ISDN User Part functional description](https://www.itu.int/rec/T-REC-Q.761/)
- [SS7 ISUP Tutorial - TelecomABC](https://www.telecomabc.com/i/isup.html)
- [ANSI ISUP Specification - ATIS](https://www.atis.org/)

## Personal Notes

Working with ISUP feels like archaeology in modern telecom—most new projects use SIP, but understanding ISUP helps when debugging legacy SS7 networks or interworking scenarios. The circuit-oriented nature of ISUP is fundamentally different from SIP's packet-based approach. I once had to trace a call setup failure through multiple SS7 nodes using hex dumps, which gave me a new appreciation for the precision required in telecom protocols.
