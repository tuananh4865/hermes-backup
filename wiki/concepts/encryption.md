---
title: Encryption
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [encryption, security, cryptography, tls]
---

## Overview

Encryption is the process of converting readable data, known as plaintext, into an unreadable format called ciphertext. This transformation uses mathematical algorithms and cryptographic keys so that only authorized parties who possess the correct decryption key can reverse the process and access the original information. The primary purpose of encryption is to protect data confidentiality, ensuring that sensitive information remains private even if it is intercepted or accessed by unauthorized individuals.

Encryption has been used for centuries in various forms, from ancient cipher systems to modern computational algorithms. In contemporary computing, it serves as the foundation for securing communications, protecting stored data, and verifying identity across networks. When you send a message, make an online purchase, or access your bank account, encryption works behind the scenes to safeguard your personal information from eavesdroppers, hackers, and other malicious actors.

The strength of encryption relies on the complexity of the algorithm and the length of the cryptographic key. Modern encryption standards use mathematical operations that are computationally infeasible to reverse without the key, even with significant computing power. This mathematical hardness forms the basis of digital security and enables trust in electronic transactions and communications worldwide.

## Types

Encryption methods are broadly categorized into symmetric and asymmetric encryption, each with distinct characteristics and use cases.

### Symmetric Encryption

Symmetric encryption uses the same key for both encrypting and decrypting data. The sender and receiver must both possess and protect the shared secret key, requiring secure key exchange before communication can occur. Symmetric algorithms are generally fast and efficient, making them suitable for encrypting large volumes of data such as file storage and database contents.

Common symmetric encryption algorithms include the Advanced Encryption Standard (AES), which is widely adopted as the gold standard for government and commercial security, and the Triple Data Encryption Algorithm (3DES), which applies the older DES algorithm three times for enhanced security. ChaCha20 is another modern stream cipher known for its speed and resistance to timing attacks, particularly valuable in mobile and resource-constrained environments.

### Asymmetric Encryption

Asymmetric encryption, also called public-key cryptography, uses a pair of mathematically related keys: a public key for encryption and a private key for decryption. The public key can be freely distributed, while the private key must remain confidential. This eliminates the need to share secret keys and enables secure communication between parties who have never interacted before.

The most widely used asymmetric algorithm is RSA (Rivest-Shamir-Adleman), which bases its security on the mathematical difficulty of factoring large prime numbers. Elliptic Curve Cryptography (ECC) provides equivalent security with smaller key sizes, making it popular for mobile devices and environments with limited computational resources. Asymmetric encryption is essential for digital signatures, key exchange, and establishing secure sessions in protocols like TLS.

## TLS/SSL

Transport Layer Security (TLS) and its predecessor Secure Sockets Layer (SSL) are cryptographic protocols that provide secure communication over networks. TLS establishes an encrypted connection between two endpoints, typically a client such as a web browser and a server, protecting all data transmitted during the session from interception or tampering.

The TLS handshake process involves several steps that establish a secure session. The client and server exchange cryptographic capabilities, verify each other's identities using digital certificates, and negotiate the encryption algorithms to be used. Once the handshake completes, both parties possess session keys for symmetric encryption, and all subsequent communication is protected by this encrypted tunnel.

TLS is fundamental to web security, powering the HTTPS protocol that secures online banking, e-commerce, email, and virtually all sensitive communications on the internet. TLS 1.3, the latest version, offers improved performance, reduced latency, and stronger security guarantees by eliminating outdated cryptographic algorithms and simplifying the handshake process. Proper TLS configuration and certificate management are critical for maintaining security in production environments.

## Related

- [[Cryptography]] - The broader science of securing communication through codes and ciphers
- [[Public Key Infrastructure]] - The systems and frameworks supporting digital certificates and asymmetric encryption
- [[tls-ssl]] - Digital certificates used to verify identity and enable encrypted connections
- [[AES Encryption]] - The prevalent standard for symmetric encryption in modern systems
- [[End-to-End Encryption]] - Encryption that ensures only communicating users can read messages
- [[Key Exchange]] - Protocols for securely sharing cryptographic keys between parties
