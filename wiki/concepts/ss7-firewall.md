---
title: "SS7 Firewall"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [telecommunications, ss7, network-security, firewall, signaling]
---

# SS7 Firewall

## Overview

An SS7 firewall is a specialized network security device that monitors, filters, and controls SS7 (Signaling System No. 7) traffic flowing between telecommunication networks. SS7 is the protocol suite used globally for setting up and tearing down telephone calls,SMS messaging, and prepaid billing transactions across carrier networks.

SS7 was designed in the 1970s-80s with trust assumptions that no longer hold. Original implementations assumed carriers would only connect to trusted partners via dedicated lines. Modern interconnection through IP-based transport and peering exchanges breaks those assumptions, exposing vulnerabilities that SS7 firewalls exist to mitigate.

The firewall sits at the boundary between networks (or between a carrier and third-party service providers), inspecting SS7 messages against security policies, blocking malformed or suspicious traffic, and logging events for compliance and forensic analysis.

## Key Concepts

### SS7 Protocol Suite

SS7 consists of multiple layers: Message Transfer Part (MTP) handles low-level packet delivery, SCCP (Signaling Connection Control Part) provides routing and global title translation, TCAP (Transaction Capabilities Application Part) enables application-layer transactions, and MAP (Mobile Application Part) carries mobile-specific messages like location updates and SMS delivery.

Each layer presents different attack surfaces. SS7 firewalls must understand this entire stack to detect threats that span multiple layers.

### SS7 Attack Types

Several attack categories threaten SS7-connected networks:

**Location Tracking**: Attackers send queries disguised as legitimate network messages to determine a subscriber's location. This enables physical surveillance without the target's knowledge.

**Call Interception**: Through manipulation of call routing messages, attackers can redirect calls or capture call setup details, enabling [[man-in-the-middle]] attacks.

**SMS Interception**: Prepaid systems and two-factor authentication codes sent via SMS can be intercepted, enabling financial fraud and account takeover.

**Denial of Service**: Malformed or flood messages can disrupt network elements, causing service outages.

### Firewall Capabilities

Modern SS7 firewalls provide:

- Deep packet inspection of SS7 messages
- Protocol anomaly detection
- Rate limiting per source/destination
- Whitelist and blacklist management
- Real-time alerting and logging
- Integration with [[security-information-and-event-management]] (SIEM) systems

## How It Works

An SS7 firewall operates at the [[network-layer]] of the SS7 stack, intercepting messages before they reach protected network elements:

```bash
# Simplified SS7 message flow with firewall
[External Network] --> [SS7 Firewall] --> [Protected Network Elements]
                           |
                           v
                    Policy Evaluation:
                    - Source identity verified
                    - Message type allowed
                    - Rate limits checked
                    - Anomalies detected
                           |
                           v
                    [Pass] --> Forward to destination
                    [Block] --> Log and alert
```

The firewall maintains state about established sessions and can correlate messages across a transaction to detect multi-step attacks.

## Practical Applications

### Mobile Carriers

Mobile Network Operators (MNOs) deploy SS7 firewalls at the boundary between their network and external carriers or MVNOs. This protects subscribers from location tracking and interception while enabling legitimate inter-carrier services.

### Messaging Aggregators

Companies that send SMS at scale must connect to carrier networks via SS7. Firewalls protect these connections and ensure compliance with carrier requirements.

### Fraud Management

SS7 firewalls feed data to [[fraud-detection]] systems that identify suspicious patterns—unusually high location query rates, unexpected message types, or traffic from known-bad sources.

## Examples

A basic SS7 firewall rule configuration:

```yaml
ss7_firewall:
  rules:
    - name: block-location-services-from-untrusted
      match:
        message_type: [ATIFLM, ATIGM]  # Location services
        source_trust_level: low
      action: block
      log: true
      
    - name: allow-sms-from-known-aggregators
      match:
        message_type: [MTF, MOF]  # SMS messages
        source: known_sms_aggregators
      action: pass
      rate_limit: 1000/minute
      
    - name: detect-anomaly-rate-limiting
      match:
        opc: any  # Originating Point Code
      action: monitor
      threshold: 5000/minute
      alert: true
```

## Related Concepts

- [[signaling-system-7]] — The protocol SS7 firewalls protect
- [[telecom-security]] — Broader security concerns in telecommunications
- [[network-firewall]] — General firewall concepts
- [[ intrusion-detection-system]] — Complementary security technology
- [[gsm]] — The mobile network standard that uses SS7

## Further Reading

- [SS7 Vulnerability Overview - SS7 Attack](https://www.ss7.computer) — Security research on SS7 weaknesses
- [Global Cyber Alliance SS7 Protection](https://www.globalcyberalliance.org/ss7) — Industry guidance on SS7 security
- [3GPP SS7 Security Standards](https://www.3gpp.org/) — Official protocol specifications

## Personal Notes

The tension in SS7 security is that the protocol's openness enables valuable services—roaming, number portability, prepaid billing—while its security model doesn't support the trust relationships those services require. SS7 firewalls are a band-aid on a fundamentally broken design, but they're necessary band-aids. The eventual solution—SS7 over Diameter with [[diameter-security]] and [[tls]]-like mutual authentication—will take decades to deploy given the installed base of legacy equipment.
