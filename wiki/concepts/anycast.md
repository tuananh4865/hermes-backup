---
title: "Anycast"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [networking, dns, cdn, routing, infrastructure]
---

# Anycast

## Overview

Anycast is a network addressing and routing methodology in which a single IP address is announced from multiple geographic locations simultaneously. When a client sends a request to an anycast address, the internet's routing infrastructure automatically directs that request to the topologically nearest or "best" location that is advertising that address. This is fundamentally different from [[unicast]] (one-to-one communication), [[multicast]] (one-to-many), and [[broadcast]] (one-to-all), where a single address maps to a single, specific destination.

The power of anycast lies in its simplicity and its profound implications for performance, reliability, and scalability. By having multiple identical endpoints share the same IP address, traffic is naturally distributed across locations without requiring the client or the application layer to know about every endpoint. If one location becomes unavailable due to network issues, hardware failure, or DDoS attack, routing automatically shifts traffic to the next nearest location within seconds, providing automatic failover at the network layer.

Anycast is a foundational technology for several of the internet's most critical services. [[DNS]] resolvers operated by Cloudflare, Google (8.8.8.8), and Quad9 use anycast to place DNS infrastructure close to end users worldwide while providing resilience against attacks. Content Delivery Networks ([[cdn]]) use anycast to serve cached content from edge servers nearest to requesting clients. DDoS mitigation services use anycast to absorb and distribute attack traffic across many points of presence, diluting its impact before it reaches the target origin.

## Key Concepts

**IP Address Space** is divided into routing announcements managed by the Border Gateway Protocol (BGP). In a traditional unicast setup, a specific IP address block is routed to a specific location. In anycast, the same IP address block is simultaneously announced from multiple Autonomous Systems (ASes) in different locations.

**BGP Routing Decisions** determine which anycast location serves a particular client. BGP selects the shortest AS path by default, but many other factors influence the decision, including path attributes like MED (Multi-Exit Discriminator), local preference, and IGP cost within an ISP's network. The result is that different clients in different geographic or network topology locations may be routed to different anycast instances of the same service.

**Latency Optimization** is achieved because routing takes the shortest network path. For a user in Tokyo, a request to an anycast address served by a Tokyo presence will traverse fewer network hops and experience lower round-trip time than if that request were routed to a server in Frankfurt. This geographic distribution of anycast endpoints is what makes [[CDN]] and DNS anycast so effective for performance.

**DDoS Mitigation** works because anycast naturally disperses incoming traffic across multiple Points of Presence (PoPs). A volumetric DDoS attack targeting an anycasted service must overwhelm all or most of the distributed locations to cause visible impact, dramatically raising the bar for attackers.

**Health Checking and Route Withdrawal** provide failover. When an anycast location experiences failure (link down, server crash, or service degradation), BGP withdraws the route announcement from that location. Within seconds to minutes (depending on BGP convergence times), traffic reroutes to the next-best location. This is the network-layer equivalent of the self-healing behavior in application-layer load balancing.

## How It Works

Implementing anycast requires careful coordination between network engineering and the application layer.

At the network layer, the same IP prefix is configured on edge routers at multiple locations. Each location announces this prefix via BGP to its upstream ISPs. Internet routers throughout the world receive these multiple route announcements and, following BGP path selection rules, select the "best" path based on shortest AS-path, local preference, and other attributes. The result is that clients in different regions naturally connect to different anycast locations.

At the application layer, each anycast location must be capable of serving identical content or handling identical requests. For [[DNS]] servers, this means maintaining synchronized zone data across all anycast instances. For a CDN, it means caching the same content at each edge location. For a load-balanced service, it means ensuring session state is handled appropriately (either stateless or shared across locations).

The key challenge is ensuring true statelessness at the application layer—if a client's request is routed to Location A and the response requires a follow-up request that gets routed to Location B, the session may be broken. Stateless protocols (like HTTP) work well with anycast. State-heavy protocols require sticky sessions or shared state management (via databases or distributed caches).

## Practical Applications

Anycast is used by many of the internet's most critical services:

- **DNS Resolution**: Google's 8.8.8.8 and Cloudflare's 1.1.1.1 DNS resolvers use anycast to provide low-latency, globally distributed name resolution with built-in DDoS resistance.
- **Content Delivery Networks**: Akamai, Cloudflare, and Fastly use anycast to route user requests to the nearest edge server holding a cached copy of content.
- **DDoS Protection Services**: Services like Cloudflare's DDoS mitigation, Akamai's Kona, and Project Shield by Google use anycast to absorb attack traffic at the network edge.
- **Global Server Load Balancing**: Large internet services use anycast as the first tier of a multi-layer distribution strategy, with geographic DNS or HTTP routing selecting among anycast endpoints.

## Examples

The BGP configuration for a simple anycast setup might look like this. This example shows the same IP prefix being announced from two different locations:

```
! Router in New York (AS65001)
router bgp 65001
 neighbor 10.0.1.1 remote-as 65000
 address-family ipv4 unicast
  network 203.0.113.0/24
  neighbor 10.0.1.1 activate
```

```
! Router in London (AS65002)
router bgp 65002
 neighbor 10.1.1.1 remote-as 65000
 address-family ipv4 unicast
  network 203.0.113.0/24
  neighbor 10.1.1.1 activate
```

Both routers announce `203.0.113.0/24` to their upstream providers. Internet routers receive both announcements and choose the best path based on BGP attributes, effectively sending each client to the nearest New York or London instance.

## Related Concepts

- [[unicast]] — One-to-one addressing (the most common internet communication model)
- [[dns]] — Domain Name System, which relies heavily on anycast for global resolvers
- [[cdn]] — Content Delivery Networks that use anycast for edge delivery
- [[bgp]] — Border Gateway Protocol, the routing protocol that enables anycast announcements
- [[ddos]] — Distributed Denial of Service, which anycast helps mitigate

## Further Reading

- [Cloudflare's explanation of Anycast](https://www.cloudflare.com/learning/cdn/glossary/anycast/) — Practical understanding of anycast in CDN context
- [BGP for Engineers](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/26666-bgp-toc.html) — Foundation for understanding anycast routing
- [RFC 4786](https://tools.ietf.org/html/rfc4786) — Best Current Practice for anycast in DNS

## Personal Notes

Anycast is one of those "simple at first glance, deep on inspection" networking concepts. The magic is that it's entirely implemented in the routing layer—applications need no special code to benefit from anycast routing. However, the operational complexity comes from ensuring all anycast locations are truly equivalent and that session state is handled appropriately. BGP convergence times (which can range from seconds to minutes) also mean anycast failover is not instantaneous, making it complementary to—but not a replacement for—application-layer health checking and failover mechanisms. Observing anycast in practice via traceroute to DNS resolvers like 8.8.8.8 from different network locations is a great way to build intuition.
