---
title: "PSTN"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [telecommunications, networking, telephony, voip]
---

# PSTN

The Public Switched Telephone Network (PSTN) is the worldwide collection of interconnected circuit-switched telephone networks that have served as the backbone of voice communications since the late 1800s. Often called the plain old telephone service (POTS), PSTN represents the global infrastructure that enables any telephone to call any other telephone on the planet through a series of physical switches, trunk lines, and central offices. Understanding PSTN is essential for anyone working in telecommunications, VoIP integration, or legacy system modernization because it forms the foundation upon which modern voice services are built, even as they migrate to digital and IP-based technologies.

## Overview

PSTN is a network of networks operated by telecommunications carriers, governments, and private companies across the globe. At its core, PSTN provides circuit-switched connections between two endpoints for the duration of a telephone call. When you make a call, the PSTN establishes a dedicated physical circuit from your telephone through local loops, central offices, and potentially long-distance trunk lines to the recipient's line. This circuit remains open and reserved for the entire duration of the call, ensuring consistent voice quality regardless of distance.

The infrastructure includes several key components: local loops (copper lines connecting homes and businesses to central offices), switching offices (where calls are routed), trunk lines (high-capacity connections between switching offices), and various signaling systems (most notably SS7) that manage call setup, teardown, and supplementary services like caller ID and call forwarding. The network has evolved significantly over its lifetime, with fiber optic cables replacing much of the copper infrastructure, digital switches replacing mechanical ones, and packet-based transmission augmenting traditional circuit switching.

## Key Concepts

Understanding PSTN requires familiarity with several foundational concepts. **Circuit Switching** is the method PSTN uses to establish dedicated point-to-point connections for the duration of a call, reserving bandwidth regardless of whether voice data is actively being transmitted. This contrasts sharply with packet-switched networks like the internet, where data is broken into discrete packets that may take different routes and arrive out of order.

**Local Loop** refers to the final mile of the PSTN—the copper wiring that connects a subscriber's premises to the nearest central office. Despite being the oldest part of the infrastructure, local loops remain largely unchanged for many subscribers and represent a significant legacy challenge for modernizing telephone service.

**Signaling System 7 (SS7)** is the out-of-band signaling protocol used within PSTN to manage call routing, setup telephone services, and enable features like number portability and toll-free calling. SS7 operates on a separate channel from voice traffic and coordinates between network elements to ensure calls reach their intended destinations.

**Central Offices (COs)** are the switching facilities where local loops terminate and calls are routed onward. Each central office serves a defined geographic area and contains the switches that connect calls within that area or route them to other offices through trunk lines.

## How It Works

When a subscriber makes a telephone call, a carefully orchestrated sequence of events unfolds across the PSTN infrastructure. The process begins when lifting the handset creates a loop current that signals the central office that service is requested. The CO's switch then provides dial tone, confirming the line is ready to accept digits.

As the caller dials or enters numbers, the central office collects these digits and analyzes them to determine call routing. Local calls (within the same CO's service area) are switched internally, while long-distance and international calls require routing through hierarchical levels of switching offices. The switching system uses database lookups to determine the most efficient path, establishing what is known as a circuit through the network.

For long-distance calls, the call may pass through Tandem switches (which aggregate and route traffic between central offices), End Office switches (which handle the final delivery to the called party's line), and potentially international gateway switches for calls crossing borders. Each switch along the path maintains the circuit connection, and once the called party's line is located, the CO serving them sends a ringing signal to alert the subscriber of the incoming call.

When the call is answered, the circuit is complete and voice transmission begins, flowing in real-time between the two parties. When either party terminates the call, signaling messages instruct all switches along the path to release their portions of the circuit, freeing those resources for other calls.

```python
# Example: Simulating basic PSTN call routing logic
def route_call(dialed_number, calling_office, network_db):
    """Route a call through PSTN-style switching hierarchy"""
    if is_local_number(dialed_number, calling_office):
        # Same central office - local switch
        return f"CO-{calling_office['id']}:LOCAL:{dialed_number}"
    elif is_regional_number(dialed_number):
        # Different region - route through tandem office
        tandem = find_tandem_office(calling_office, network_db)
        end_office = find_end_office(dialed_number, network_db)
        return f"CO-{calling_office['id']} -> TANDEM-{tandem['id']} -> CO-{end_office['id']}:{dialed_number}"
    else:
        # Long distance/international - hierarchical routing
        return route_hierarchical(dialed_number, calling_office, network_db)
```

## Practical Applications

Despite the rise of VoIP and mobile communications, PSTN infrastructure remains critically important in numerous practical applications. Enterprise telecommunications often rely on PSTN connectivity for mission-critical voice services, particularly in environments where reliability trumps cost savings. Many businesses maintain PSTN lines for fax machines, alarm systems, point-of-sale terminals, and elevator emergency phones because these systems are designed specifically for circuit-switched voice and offer predictable, low-latency communication.

Contact centers and emergency services continue to depend heavily on PSTN. When you call 911 or other emergency services, the call typically travels over PSTN because it offers guaranteed bandwidth and precise location information tied to the physical phone line. This location data is harder to obtain reliably with VoIP calls, making PSTN the preferred choice for safety-critical communications.

Carrier interconnection and wholesale voice services represent another significant application. Even VoIP providers often terminate calls to the PSTN at some point, requiring interfaces with traditional telephone carriers. Understanding PSTN signaling and routing is essential for anyone designing systems that interact with the public telephone network, whether integrating with SIP gateways, designing number portability solutions, or building toll-free number services.

## Examples

A practical example of PSTN in action is a traditional landline telephone call between two cities. When Caller A in New York dials the number of Caller B in Los Angeles, the call might traverse the following path: Caller A's telephone connects via copper local loop to the New York Central Office, which identifies the call as long-distance based on the area code. The New York CO routes the call to a Long Distance Tandem office, which consults SS7 databases to find an available route to Los Angeles. The call might travel over fiber optic trunk lines across the country to a Los Angeles Tandem office, which then routes to the appropriate End Office serving Caller B's neighborhood. That End Office finally connects to Caller B's local loop, and ringing voltage is applied to alert them of the incoming call.

Another example involves integrating modern VoIP systems with PSTN through gateway devices. An enterprise might use a Session Border Controller (SBC) that speaks SIP on one side and connects to a PSTN gateway on the other, allowing IP phones to call traditional telephone numbers and receive calls from the PSTN network.

## Related Concepts

- [[VoIP]] - Voice over IP technology that competes with and complements PSTN
- [[SIP]] - Session Initiation Protocol used in modern voice signaling
- [[Telephony]] - The broader field of voice telecommunications
- [[SS7]] - The signaling system used within PSTN for call control
- [[Circuit Switching]] - The switching paradigm used by PSTN

## Further Reading

- "Telecommunications Switching" by J. Flood - Comprehensive coverage of PSTN architecture
- ITU-T Recommendations on PSTN - International standards for telephone network operation
- "Voice Over IP" by Kevin Wallace - Explains how VoIP interworks with traditional PSTN

## Personal Notes

PSTN represents one of the most successful engineered systems in history, achieving near-universal reach and remarkable reliability. What strikes me most is how this infrastructure designed for voice has gracefully adapted to carry data and support modern services. Even as we rapidly transition to IP-based communications, the underlying principles of PSTN—circuit switching, hierarchical routing, and signaling out-of-band—continue to influence how we design modern telecommunication systems. Understanding PSTN provides the foundation for anyone working in telecommunications, whether maintaining legacy systems or building the next generation of voice services.
