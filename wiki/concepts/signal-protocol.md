---
title: "Signal Protocol"
created: 2026-04-20
updated: 2026-04-20
type: concept
tags: [cryptography, end-to-end-encryption, secure-messaging, signal]
sources: [https://signal.org/docs/specifications/signal/, https://eprint.iacr.org/2016/1013.pdf]
---

# Signal Protocol

The Signal Protocol (formerly known as the TextSecure Protocol) is a leading end-to-end encryption protocol for secure asynchronous messaging. Developed by Open Whisper Systems and now maintained by Signal Messenger LLC, it provides strong forward secrecy and break-in recovery properties. The protocol powers Signal Messenger, WhatsApp, iMessage (partially), and several other messaging platforms, making it the most widely deployed E2EE protocol for consumer messaging.

## Overview

The Signal Protocol was designed to solve a fundamental problem in secure messaging: achieving both forward secrecy (compromising current keys shouldn't reveal past messages) and break-in recovery (future messages should remain secure even after a key compromise) while maintaining efficient asynchronous communication between clients that may be offline for extended periods.

The protocol combines several cryptographic primitives into a cohesive system. At its core, it uses the Extended Triple Diffie-Hellman (X3DH) key agreement protocol for initial session establishment, followed by the Double Ratchet algorithm for ongoing message encryption. These components work together to provide protection against passive and active adversaries, including nation-state level attackers.

## X3DH Key Agreement (Extended Triple Diffie-Hellman)

X3DH establishes a shared secret between two parties who have not previously communicated, using a combination of long-term identity keys, medium-term signed prekeys, and one-time prekeys. This key agreement protocol enables asynchronous key exchange—critical for messaging applications where recipients may be offline.

### Key Components

Each user maintains three types of key pairs:

1. **Identity Key Pair (IK)**: A long-term Curve25519 key pair, unique per user device, generated at install time
2. **Signed Prekey Pair (SPK)**: A medium-term key pair, rotated periodically (typically weekly), signed by the identity key to prove authenticity
3. **One-Time Prekey Pair (OPK)**: Single-use key pairs, generated in batches (hundreds or thousands) and consumed as they are used

### Protocol Flow

When Alice wants to initiate a secure session with Bob (who may be offline):

1. Alice retrieves Bob's public keys from the server: identity key, signed prekey, and a one-time prekey (if available)
2. Alice generates an ephemeral key pair (EK) for this session
3. Alice computes four Diffie-Hellman operations:
   - DH1 = DH(IK_A, SPK_B) — between her identity key and Bob's signed prekey
   - DH2 = DH(EK_A, IK_B) — between her ephemeral key and Bob's identity key
   - DH3 = DH(EK_A, SPK_B) — between her ephemeral key and Bob's signed prekey
   - DH4 = DH(EK_A, OPK_B) — between her ephemeral key and Bob's one-time prekey (if used)
4. These four DH outputs are combined using a Key Derivation Function (KDF) to produce the initial shared secret
5. Alice sends her public keys (IK_A, EK_A, OPK_A reference) to Bob, along with the identity key signature

Bob, upon coming online, performs the corresponding DH calculations to derive the same shared secret. If no one-time prekey was used (because none was available), the protocol falls back to a three-key variant using only DH1, DH2, and DH3.

The X3DH design ensures that compromising any single key (or even many keys) does not reveal past session keys, because each DH operation involves fresh randomness from the ephemeral key.

## Double Ratchet Algorithm

The Double Ratchet algorithm maintains forward secrecy and break-in recovery through two nested ratchet mechanisms: a symmetric-key ratchet and a Diffie-Hellman ratchet.

### Symmetric-Key Ratchet

Each message is encrypted with a unique message key, derived from a chain key using HKDF. After encryption, the chain key is updated via a one-way function, ensuring the previous chain key cannot be recovered from subsequent ones. This provides forward secrecy: losing the current message key doesn't expose past messages because past message keys have already been deleted.

### Diffie-Hellman Ratchet

The DH ratchet operates on a pair of key pairs (chain key and DH key) that are exchanged with each message. When a new DH key arrives, a fresh DH output is computed, mixed into the chain key, and a new DH key pair is generated. This ensures break-in recovery: even if an attacker compromises current keys, they cannot decrypt future messages after the next DH ratchet step because they lack the resulting DH private key.

The Double Ratchet proceeds as follows:

1. **Initialization**: Using the shared secret from X3DH, both parties initialize their sending and receiving chain keys and DH ratchet key pairs
2. **Message Encryption**: Each message encrypts plaintext using the current message key, then advances the symmetric ratchet to derive the next message key
3. **DH Ratchet Step**: When a new DH public key arrives from the remote party, a new DH output is computed, mixed into the chain key, and a new DH key pair is generated
4. **Response**: The remote party similarly advances their ratchet in response messages

This dual ratcheting means that each message exchange potentially advances both the symmetric and DH ratchets, continuously refreshing keys and maintaining cryptographic independence between message streams.

### Prekey Messages

For initial messages to a new session (before a full Double Ratchet is established), the protocol supports "prekey messages" that include the sender's ephemeral key and optionally one-time prekey data. This allows message delivery even when the recipient is offline initially.

## Sealed Sessions

Sealed Sessions (introduced around 2016-2017) enhance the Signal Protocol's metadata minimization properties. Traditional Signal Protocol messages reveal the sender's identity to the recipient's server and to some extent to the recipient themselves. Sealed Sessions encrypt the sender's identity to only the recipient using a sender key derived from the initial X3DH handshake.

Specifically, Sealed Sessions use a "sender key" mechanism where:
- The sender's identity is encrypted with a key derived from the session's chain
- The recipient can still verify the message's authenticity but cannot learn the sender's identity from message metadata alone
- This reduces metadata leakage to passive server observers

However, Sealed Sessions have a limitation: the receiving client still needs to know who sent the message for display purposes, so some metadata remains visible to the recipient's device.

## Forward Secrecy and Break-in Recovery

The Signal Protocol achieves forward secrecy through the symmetric-key ratchet. Message keys are derived one-way from chain keys; once a message key is used and deleted, it cannot be recovered from subsequent chain keys. Compromising the current state of a session does not reveal past message keys, assuming they were properly deleted.

Break-in recovery (also called future secrecy or post-compromise security) is achieved through the DH ratchet. Even if an attacker obtains all current session keys and chain state, they can only read messages until the next DH ratchet step occurs. At that point, a fresh DH key pair (whose private material the attacker doesn't have) is incorporated into the chain, effectively "healing" the session. The attacker would need to compromise the session again for each subsequent DH ratchet step.

Importantly, Signal Protocol sessions are designed so that break-in recovery requires only a single outbound message from the uncompromised party. When Alice sends a message to Bob using her current session state, that message already incorporates a new DH ratchet step. If Bob's session state was compromised but Alice's was not, Bob will receive the new DH public key and can advance his ratchet to secure future messages.

## Implementation in Signal, WhatsApp, and iMessage

### Signal Messenger

Signal uses the Signal Protocol as its primary encryption mechanism for all messages, voice calls, and video calls between Signal users. The Signal client implements the full protocol stack including X3DH, Double Ratchet, Sealed Sessions, and additional protocol extensions for group messaging (Sender Keys).

### WhatsApp

WhatsApp (owned by Meta) integrated the Signal Protocol into its platform starting in 2016. The implementation uses the Signal Protocol's libsignal library for end-to-end encryption of all messages, voice notes, media, and calls between WhatsApp users. WhatsApp's implementation covers both individual and group chats, using a variation of Sender Keys for group encryption.

### iMessage

Apple's iMessage uses a proprietary E2EE system that shares some design goals with Signal Protocol (notably X3DH-style key exchange and a form of Double Ratchet), but details of the full protocol remain proprietary. Apple's documentation indicates they use a combination of RSA, ECDSA, and AES-GCM, with a key exchange mechanism that provides forward secrecy. However, because iMessage's full protocol specification is not publicly documented, independent security researchers cannot fully verify its security properties.

## Comparison to Other E2EE Protocols

### Signal Protocol vs. OTR (Off-the-Record Messaging)

OTR was a pioneering E2EE protocol for synchronous chat, designed in 2004-2005. Key differences:

| Property | Signal Protocol | OTR |
|----------|-----------------|-----|
| **Key Exchange** | X3DH (asynchronous) | Diffie-Hellman with authentication |
| **Ratchet** | Double Ratchet | None (uses fresh keys per message but no ratchet) |
| **Forward Secrecy** | Yes (symmetric ratchet) | Yes (deniable auth, per-message keys) |
| **Break-in Recovery** | Yes (DH ratchet) | Limited (requires re-keying) |
| **Async Support** | Full | Poor (requires both parties online) |
| **Use Case** | Asynchronous messaging | Synchronous chat |
| **Maturity** | Active development | Largely historical |

OTR's lack of a ratchet mechanism means it achieves forward secrecy but not break-in recovery. Additionally, OTR was designed for synchronous conversations where both parties are online—a requirement that makes it unsuitable for modern asynchronous messaging.

### Signal Protocol vs. MLS (Messaging Layer Security)

MLS is a newer IETF-standardized protocol (RFC 9420) designed to address some limitations of Signal Protocol, particularly for large group chats. MLS uses a "tree-based" ratchet that is more efficient for large groups and supports sender key encryption rather than individual encryption per recipient. However, MLS is newer and less widely deployed than the Signal Protocol.

## Metadata Minimization

The Signal Protocol addresses metadata minimization at multiple layers:

- **Message Content**: End-to-end encrypted; servers cannot read content
- **Sender Identity**: Hidden from server (Sealed Sessions encrypt sender identity to recipient)
- **Recipient Identity**: Known to server (required for message delivery)
- **Timing**: Metadata about when messages are sent may be visible to servers
- **Read Receipts**: Optional feature that reveals when messages are read

Signal Messenger's "Sealed Sender" feature (when enabled) hides the sender's identity from the Signal server, showing only that a message was delivered to a recipient without revealing who sent it. However, some metadata remains: the server knows which device received a message and approximately when.

## Limitations and Considerations

The Signal Protocol is not a panacea for all security problems:

- **Metadata remains**: While message content is protected, significant metadata (recipient identity, timing patterns, IP addresses during registration) may still be collected
- **Implementation bugs**: The protocol specification is sound, but implementation vulnerabilities have occurred in various clients
- **Key management**: Users who lose their identity keys cannot decrypt old messages, but new sessions will work normally
- **Group messaging**: Uses Sender Keys, which trades some security properties for efficiency in large groups
- **Server trust**: While encrypted, the server still manages key bundles and message delivery; a compromised server could disrupt service or enable denial of attacks

## Related Concepts

- [[end-to-end-encryption]] — the broader concept of encrypting data between endpoints
- [[double-ratchet]] — the specific ratchet algorithm used in Signal
- [[x3dh]] — the key agreement protocol used for session establishment
- [[forward-secrecy]] — the property of ensuring past sessions remain secure
- [[otr]] — a predecessor E2EE chat protocol with different trade-offs
- [[metadata-minimization]] — reducing metadata exposure in communication systems
- [[signal-messenger]] — the application built on this protocol

## Further Reading

- [Signal Protocol Documentation](https://signal.org/docs/specifications/signal/)
- [The X3DH Key Agreement Protocol](https://signal.org/docs/specifications/x3dh/)
- [The Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/)
- [ Marlinspike & Perrin, "The X3DH Key Agreement Protocol" (2016)](https://eprint.iacr.org/2016/1013.pdf)
- [Gaži, Peyroun & Schwoebel, "The Static Diffie-Hellman Protocol"](https://eprint.iacr.org/2018/1173.pdf)
- [Signal Messenger Blog - Sealed Sender](https://signal.org/blog/sealed-sender/)
- [WhatsApp Encryption Overview](https://www.whatsapp.com/security/WhatsApp-Security-Whitepaper.pdf)

## Personal Notes

> The Signal Protocol represents a remarkable achievement in practical cryptography—bridging academic rigor (formal security proofs exist for both X3DH and Double Ratchet) with real-world deployability at massive scale (billions of users). The design philosophy of prioritizing break-in recovery through the DH ratchet, rather than just forward secrecy, was a significant innovation that influenced subsequent protocols like MLS.
