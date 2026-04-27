---
title: Denial of Service (DoS)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [security, dos, ddos, attack, web-security, rate-limiting]
---

# Denial of Service (DoS)

## Overview

Denial of Service (DoS) attacks are malicious attempts to disrupt the normal functioning of a service, making it unavailable to legitimate users. The attacker overwhelms the target with requests, exploits vulnerabilities that cause crashes, or consumes resources in ways that prevent legitimate access. DoS attacks are among the oldest and most persistent categories of cyberattacks, and understanding them is essential for anyone building or securing internet-facing services.

The impact of a successful DoS attack can range from minor inconvenience to business-critical. E-commerce sites lose direct revenue during outages. SaaS companies may trigger SLA breaches with their customers. News sites can be silenced during breaking events. In extreme cases, extended outages can damage reputation irreparably and cause customer attrition that persists long after the attack ends.

Modern DoS attacks have evolved beyond simple flood attacks from single sources. Distributed Denial of Service (DDoS) attacks leverage botnets—networks of compromised computers—to generate attack traffic from thousands or millions of IP addresses, making source-based blocking ineffective. These volumetric attacks can exceed terabits per second, requiring massive infrastructure to absorb.

## Key Concepts

**Volumetric Attacks** aim to consume all available bandwidth between the target and the internet. By sending massive amounts of traffic, the attack saturates the pipe so legitimate requests cannot get through. UDP floods and ICMP floods are classic examples. Modern variants use amplification techniques—exploiting open DNS resolvers, NTP servers, or memcached instances—to multiply the attack traffic by factors of 10-100x.

**Protocol Attacks** exploit characteristics of network protocols to exhaust server resources. SYN floods exploit the TCP handshake by sending SYN packets without completing the handshake, leaving the server with half-open connections that consume memory. HTTP floods send seemingly legitimate GET or POST requests that consume application resources.

**Application Layer Attacks** target specific applications or services, often with fewer requests but more sophisticated payloads. Slowloris keeps connections open by sending partial HTTP requests slowly. HTTP POST floods send legitimate-looking POST requests with large headers or slow-moving bodies. These attacks are harder to detect because individual requests look normal.

**Botnets** are networks of compromised computers (bots or zombies) controlled by attackers. The attacker coordinates the botnet to send traffic to the target simultaneously. Major botnets like Mirai (Internet of Things devices) have been responsible for some of the largest DDoS attacks in history.

**Reflection and Amplification** techniques make attacks harder to trace and more powerful. The attacker sends requests with the target's IP address as the source to open DNS servers, NTP servers, or other services that respond with much larger packets. The large responses flood the target, while the actual attack traffic appears to come from legitimate services.

## How It Works

DoS attacks exploit the fundamental asymmetry between attacking and defending. An attacker with modest resources can generate enough traffic to overwhelm a target if the attack is effectively amplified. Defenders must provision capacity for legitimate traffic plus attack traffic, while attackers only need to exceed the legitimate traffic threshold.

```bash
# Example: Simple SYN flood attack (educational - for understanding only)
# NEVER use against systems you don't own
hping3 -S -p 80 --flood target.example.com

# Example: Slowloris-style attack (educational)
# Opens many connections and holds them open
while :
do
  echo -e "POST / HTTP/1.1\r\n"
  echo -e "Host: target.example.com\r\n"
  echo -e "Content-Length: 1000\r\n"
  sleep 15
done | nc target.example.com 80
```

Modern DoS mitigation involves multiple layers:

1. **Edge Protection**: Content Delivery Networks (CDNs) and DDoS mitigation services (Cloudflare, Akamai, AWS Shield) absorb attack traffic at the network edge before it reaches origin servers
2. **Rate Limiting**: Limiting requests per IP, per endpoint, or per API key prevents abuse and reduces impact
3. **Traffic Scrubbing**: Proactively filtering malicious traffic patterns while allowing legitimate requests
4. **Anycast Routing**: Distributing traffic across multiple geographic PoPs so attacks are absorbed globally

## Practical Applications

**Rate Limiting** is the first line of defense against application-layer DoS attacks. Implementing per-IP and per-API-key rate limits prevents any single source from overwhelming the service:

```python
# Example: Token bucket rate limiter
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_second=10, burst=20):
        self.rate = requests_per_second
        self.burst = burst
        self.tokens = defaultdict(lambda: burst)
        self.last_update = defaultdict(time.time)
    
    def allow_request(self, client_id):
        now = time.time()
        elapsed = now - self.last_update[client_id]
        self.last_update[client_id] = now
        
        # Replenish tokens
        self.tokens[client_id] = min(
            self.burst,
            self.tokens[client_id] + elapsed * self.rate
        )
        
        if self.tokens[client_id] >= 1:
            self.tokens[client_id] -= 1
            return True
        return False

# Usage in API middleware
limiter = RateLimiter(requests_per_second=100, burst=200)

@app.middleware
def rate_limit(request, call_next):
    if not limiter.allow_request(request.client_ip):
        return Response(status_code=429, body="Rate limit exceeded")
    return call_next(request)
```

**CAPTCHA Integration** distinguishes human users from automated bots. CAPTCHAs add friction but can be effective against bot-driven attacks.

**Challenge-Response Systems** like CAPTCHA, JavaScript challenges, or browser fingerprinting can filter out automated traffic before it reaches application logic.

## Examples

**Cloudflare 1.1.1.1 Attack (2020)**: A massive memcached amplification attack generated approximately 330 Gbps of attack traffic. The attacker spoofed DNS queries to memcached servers, which responded with large packets to the spoofed target address.

**GitHub Attack (2018)**: GitHub was hit with a 1.35 Tbps DDoS attack using exposed memcached instances. This attack demonstrated how amplification can generate unprecedented attack volumes.

**Dyn DNS Attack (2016)**: The Mirai botnet targeted DNS provider Dyn, taking down Twitter, Reddit, Netflix, and dozens of other major sites for hours. This attack highlighted the cascading effects possible when core internet infrastructure is targeted.

## Related Concepts

- [[web-security]] — General web security principles
- [[rate-limiting]] — Rate limiting as a DoS mitigation technique
- [[api-gateway]] — API gateways often include DoS protection
- [[adversarial-robustness]] — Related to adversarial aspects of security
- [[backup-and-recovery]] — Recovery procedures after DoS attacks

## Further Reading

- OWASP Denial of Service Cheat Sheet
- Cloudflare DDoS Protection Documentation
- "The Mirai Botnet and the Importance of IoT Security"
- US-CERT Guidelines on DDoS Attacks

## Personal Notes

DoS mitigation is one of those areas where you really don't want to learn by doing. Practice your response procedures in advance through chaos engineering and game days. Know who to call at your CDN provider at 3 AM. Implement rate limiting before you need it—adding it during an attack is painful. And remember that most DoS attacks are economically motivated; understanding attacker economics helps prioritize defenses.
