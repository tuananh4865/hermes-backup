---
title: "X.509 Certificates"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cryptography, security, TLS, PKI, certificates]
---

# X.509 Certificates

## Overview

X.509 is an ITU-T standard format for public key certificates, which digitally bind a public key to an identity such as an individual, organization, or server hostname. These certificates form the backbone of modern Transport Layer Security (TLS/SSL), code signing, and document signing infrastructure. An X.509 certificate contains the public key, identity information, a validity period, the digital signature of a Certificate Authority (CA), and various metadata that enable relying parties to verify the certificate's authenticity.

The X.509 standard has evolved through several versions (v1, v2, v3), with v3 introducing extensions that allow certificates to carry additional constraints and usage policies. Today, X.509 certificates underpin HTTPS, secure email (S/MIME), document signatures, VPN authentication, and IoT device identity verification.

## Key Concepts

**Certificate Structure**: An X.509 certificate contains these core components:
- **Version**: Indicates v1, v2, or v3 format
- **Serial Number**: Unique identifier assigned by the CA
- **Signature Algorithm**: The algorithm used to sign the certificate (e.g., SHA-256 with RSA)
- **Issuer**: The Certificate Authority that issued and signed the certificate
- **Validity Period**: Not Before and Not After dates defining the certificate's active window
- **Subject**: The entity the certificate represents (CN, O, L, ST, C fields)
- **Subject Public Key Info**: The public key and its algorithm
- **Extensions**: Additional metadata (key usage, SAN, etc.)
- **Signature**: The CA's digital signature over the certificate contents

**Certificate Chains**: Certificates are organized in chains from an end-entity certificate up to a root CA. Each certificate is signed by the next higher certificate in the chain. Browsers and operating systems ship with built-in root certificates from trusted CAs.

**Subject Alternative Names (SAN)**: Extensions that allow a single certificate to secure multiple domain names or IP addresses. This replaced the older Common Name (CN) field which could only hold a single hostname.

**Key Usage and Extended Key Usage**: Extensions that constrain how a certificate's private key can be used— например, only for server authentication (TLS) or only for code signing.

## How It Works

The X.509 certificate lifecycle involves several stages:

1. **Key Generation**: The entity requesting a certificate generates an asymmetric key pair (typically RSA, ECDSA, or Ed25519). The private key remains securely on the server; the public key goes into the certificate request.

2. **Certificate Signing Request (CSR)**: The entity creates a CSR containing its public key and identity information, then signs it with its private key. The CSR is submitted to a CA.

3. **Verification**: The CA validates the requestor's identity through some verification process (domain validation, organization validation, or extended validation). This step varies based on certificate type.

4. **Certificate Issuance**: The CA creates the X.509 certificate, signs it with the CA's private key, and returns it to the requestor.

5. **Certificate Deployment**: The certificate is installed on the server (for TLS) or integrated into the signing infrastructure.

6. **Certificate Revocation**: If a private key is compromised or a certificate is no longer needed, it can be revoked. Clients check revocation status via CRL (Certificate Revocation Lists) or OCSP (Online Certificate Status Protocol).

## Practical Applications

X.509 certificates are essential in numerous security contexts:

- **TLS/HTTPS**: Every secure web connection uses X.509 certificates to authenticate servers and establish encrypted sessions
- **Code Signing**: Software publishers sign binaries with X.509 certificates to prove authenticity
- **Document Signing**: PDFs and Office documents can be signed with X.509 certificates for legal validity
- **Client Authentication**: Smart cards and client certificates use X.509 for mutual TLS authentication
- **VPN and WiFi Enterprise**: 802.1X authentication often relies on X.509 certificates
- **IoT Device Identity**: Certificates provide hardware-level identity for connected devices

## Examples

A typical X.509 certificate viewed with `openssl`:

```bash
openssl x509 -in server.crt -text -noout
```

Output excerpt:
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 04:3A:1C:82:8B:A2:...
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=US, O=Let's Encrypt, CN=R3
        Validity
            Not Before: Jan 15 00:00:00 2026 GMT
            Not After: Apr 15 00:00:00 2026 GMT
        Subject: CN=example.com
        Subject Alternative Name:
            DNS:example.com
            DNS:www.example.com
```

## Related Concepts

- [[Public Key Infrastructure]] - The ecosystem of CAs, Registration Authorities, and policies
- [[tls]] - The protocol that uses X.509 certificates for secure communications
- [[Certificate Authority]] - Entities that issue and sign X.509 certificates
- [[Public Key Cryptography]] - The asymmetric encryption underlying X.509 certificates
- [[OCSP]] - Online Certificate Status Protocol for revocation checking

## Further Reading

- RFC 5280 - The definitive X.509 PKIX specification
- Mozilla CA Certificate Policy - Practical policy constraints for trusted CAs
- OWASP Transport Layer Protection Cheat Sheet - TLS deployment best practices

## Personal Notes

Working with X.509 certificates in production taught me to automate renewal well before expiration. I once inherited a project where certificates were renewed manually—until they weren't, and a critical API went down on a Friday evening. Now I treat certificate management as code, using tools like cert-manager for Kubernetes and ACME/Let's Encrypt for automated issuance. The SAN extension is non-negotiable for any modern deployment; single-CN certificates are a relic that cause unnecessary headaches.
