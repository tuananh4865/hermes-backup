---
title: "TLS/SSL"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [security, networking, encryption]
confidence: medium
sources: []
---

# TLS/SSL

## Overview

TLS (Transport Layer Security) and its predecessor SSL (Secure Sockets Layer) are cryptographic protocols that provide secure communication over networks. TLS is the modern standard — SSL is deprecated due to security vulnerabilities.

## How TLS Works

1. **Handshake**: Client and server negotiate encryption algorithm and exchange keys
2. **Certificate Verification**: Server proves identity via X.509 certificate
3. **Encryption**: All subsequent traffic is encrypted using symmetric keys

## Related Concepts

- [[tls]] — Lower-level TLS implementation details
- [[ssl]] — Legacy SSL protocol (deprecated)
- [[https]] — HTTP over TLS
- [[x.509-certificates]] — Digital certificates used in TLS
- [[public-key-cryptography]] — Foundation of TLS encryption
