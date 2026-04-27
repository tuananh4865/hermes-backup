---
title: TCP Congestion Control
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [TCP, congestion-control, networking, protocols, internet]
---

# TCP Congestion Control

## Overview

TCP Congestion Control is a set of algorithms and mechanisms that TCP uses to regulate the rate at which it sends data into the network, preventing overwhelming the network with too much traffic. Since the internet is a shared packet-switched network where many flows compete for finite bandwidth, link capacity, and router buffers, congestion control is essential for maintaining stability and fairness.

Without congestion control, a sender could transmit at the full rate its endpoint can handle, ignoring network conditions. If many flows did this simultaneously, routers would become overloaded, buffers would fill and overflow, packets would be dropped, and throughput would collapse—a phenomenon called congestion collapse. TCP's congestion control prevents this by having senders dynamically adjust their sending rate based on network feedback.

Congestion control operates alongside TCP's flow control (which prevents overwhelming the receiver) but addresses a different problem: the network itself rather than the endpoints.

## Key Concepts

**Congestion Window (cwnd)**: The fundamental variable controlling TCP's sending rate. It represents the number of bytes the sender can transmit without receiving acknowledgment. The effective sending rate is roughly `cwnd / RTT` (round-trip time).

**Slow Start**: TCP begins with cwnd at a small value (typically 1-10 MSS, Maximum Segment Size) and increases it exponentially until a congestion event occurs or cwnd reaches the slow-start threshold (ssthresh). This quickly discovers the available bandwidth without initially overwhelming the network.

**Congestion Avoidance**: After slow start, TCP transitions to linear increase of cwnd (additive increase). This phase gradually probes for more bandwidth without causing sudden congestion.

**Fast Retransmit**: When the sender receives duplicate ACKs (indicating a dropped segment), it retransmits the missing segment without waiting for a timeout. This is triggered after typically 3 duplicate ACKs.

**Fast Recovery**: After fast retransmit, TCP enters fast recovery where it briefly reduces cwnd and continues sending new segments. This avoids the drastic slowdown of going back to slow start.

**Timeout and Slow Start Recovery**: If an ACK never arrives (timeout), TCP assumes severe congestion and resets cwnd to 1 MSS and ssthresh to half the previous cwnd. This is the most conservative response.

## How It Works

TCP congestion control operates in cycles:

1. **Connection Start**: Begin in slow start with small cwnd
2. **Exponential Growth**: cwnd doubles each RTT until reaching ssthresh or detecting loss
3. **Linear Growth**: Transition to congestion avoidance; cwnd increases by ~1 MSS per RTT
4. **Loss Detection**: Either timeout (severe) or duplicate ACKs (mild)
5. **Response**: Reduce cwnd and either restart from slow start (timeout) or use fast recovery (duplicate ACKs)
6. **Repeat**: Continue probing for bandwidth, responding to loss

```python
# Simplified TCP congestion control state machine
class TCP CongestionControl:
    def __init__(self):
        self.cwnd = 1  # Initial window in MSS
        self.ssthresh = float('inf')  # Slow start threshold
        self.state = 'slow_start'
    
    def on_ack(self, acked_bytes):
        if self.state == 'slow_start':
            self.cwnd += acked_bytes  # Exponential: roughly double per RTT
            if self.cwnd >= self.ssthresh:
                self.state = 'congestion_avoidance'
        elif self.state == 'congestion_avoidance':
            # Additive increase: ~1 MSS per RTT
            self.cwnd += (acked_bytes * (acked_bytes / self.cwnd))
    
    def on_timeout(self):
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1
        self.state = 'slow_start'
    
    def on_duplicate_ack(self):
        # Mild congestion signal
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = self.ssthresh
        self.state = 'fast_recovery'
```

## Key Algorithms

**Tahoe**: Early TCP congestion control (1988). Includes slow start, congestion avoidance, fast retransmit, and timeout-based recovery. Always resets to slow start after any loss.

**Reno**: Added fast recovery to Tahoe. After 3 duplicate ACKs, enters fast recovery, retransmits lost segment, and returns to congestion avoidance (not slow start). Better handling of single packet loss per window.

**NewReno**: Improved Reno to handle multiple packet losses in one window. Doesn't exit fast recovery until all outstanding data is ACKed.

**CUBIC**: Default in Linux since 2.6.19. Uses a cubic function of time since last loss for window growth, providing more stable behavior and better scalability in high-bandwidth networks.

**BBR (Bottleneck Bandwidth and Round-trip propagation time)**: Google's congestion control algorithm (2016). Instead of using loss as congestion signal, BBR models the bottleneck bandwidth and RTT to maintain optimal operating point. Better for high-speed, long-delay networks and low-latency applications.

## Practical Applications

**Internet Stability**: TCP congestion control is fundamental to internet stability. Without it, the internet would regularly experience congestion collapse. It's one of the most important protocols never discussed in mainstream tech.

**Video Streaming**: While streaming protocols often run over UDP, TCP-based streaming still uses congestion control. HLS and DASH streams adapt quality based on measured throughput, which implicitly relies on TCP's congestion control behavior.

**Cloud Networking**: Data center networks tune TCP congestion control for low latency (DCTCP), high throughput (HPCC), or specific hardware (RoCE). Cloud providers offer tuning options for different workloads.

**Satellite and Wireless**: Traditional TCP was designed for wired networks. Satellite and wireless links have high latency and lossy characteristics, requiring specialized congestion control (e.g., RFC 5681).

## Examples

**Bandwidth Delay Product**: The maximum amount of data "in flight" (unacknowledged) equals cwnd. For high-bandwidth, high-latency links (e.g., satellite), you need large cwnd. BDP = bandwidth * RTT. A 100 Mbps link with 500ms RTT has BDP of 50 Mbps = ~6 MB.

**Bufferbloat**: Router buffers that are too large can cause long queuing delays even when no actual congestion (packet loss) occurs. Modern congestion controls like BBR attempt to operate at the bandwidth-delay product without filling buffers.

**Measuring TCP Throughput**:
```
Throughput ≈ cwnd / RTT

For cwnd of 65,535 bytes and RTT of 100ms:
Throughput ≈ 65535 * 8 / 0.1 = 5.2 Mbps

To achieve 10 Gbps with RTT of 10ms:
cwnd ≈ bandwidth * RTT = 10 Gbps * 10ms = 100 Mbps = 12.5 MB
```

## Related Concepts

- [[TCP]] — Transport control protocol, congestion control is part of TCP
- [[Networking]] — General networking concepts
- [[Bandwidth]] — Network throughput capacity
- [[Latency]] — Network delay
- [[Protocols]] — Communication protocols
- [[HTTP]] — Application protocol running on top of TCP

## Further Reading

- RFC 2581: TCP Congestion Control — Classic specification
- RFC 5681: TCP Congestion Control — Updated specification
- "TCP/IP Illustrated" by W. Richard Stevens — Deep TCP explanation
- BBR paper: "BBR: Congestion-Based Congestion Control" (ACM 2016)

## Personal Notes

TCP congestion control is a beautiful example of distributed coordination without central control. No router tells senders to slow down; the algorithm infers congestion from losses and delays. What strikes me is how the "hard" problem of fair resource allocation is solved by simple rules that have proven remarkably robust at internet scale. The transition from loss-based (Reno, CUBIC) to model-based (BBR) congestion control feels like a paradigm shift—we're finally challenging the assumption that loss equals congestion, which held since Jacobson's 1988 paper.
