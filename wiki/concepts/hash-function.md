---
title: "Hash Function"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cryptography, algorithms, data-structures, hashing, security]
---

# Hash Function

## Overview

A hash function is a deterministic algorithm that converts an arbitrary-sized input (called a pre-image or message) into a fixed-size output value called a hash value, digest, or checksum. The defining characteristic is consistency: the same input must always produce the same output, but even a tiny change to the input (flipping a single bit) should produce a completely different hash value. This property, known as the avalanche effect, ensures that similar inputs yield vastly different outputs, making hash functions useful for a wide range of applications from data integrity verification to cryptographic security.

Hash functions are categorized into two broad families based on their intended use case. Cryptographic hash functions are designed to resist various attacks and are used in digital signatures, password storage, and blockchain systems. Non-cryptographic hash functions prioritize speed and simplicity over adversarial security, and are used in hash tables, checksums, and Bloom filters. Both families share the core property of determinism and uniform output distribution, but cryptographic hash functions impose much stricter mathematical requirements.

The output of a hash function is typically expressed as a hexadecimal string. For example, the SHA-256 hash of the string "hello" is `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`—exactly 64 characters (256 bits), regardless of whether the input is "hello" or the complete works of Shakespeare. This fixed-length output is what makes hash functions useful as "digital fingerprints" for data of any size.

## Key Concepts

**Determinism** means that a hash function must always produce the same output for the same input. There is no randomness in a pure hash function—if you hash the same file twice, you get the same digest both times. This is essential for data integrity: if the digest of a downloaded file matches the published digest, the file was not modified in transit.

**Avalanche Effect** is a critical property where changing the input by even one bit causes approximately half of the output bits to change, in a way that appears random. This ensures that similar inputs produce uncorrelated outputs, preventing attackers from crafting inputs that produce specific hashes or finding collisions through small modifications.

**Collision Resistance** is a property where a cryptographic hash function makes it computationally infeasible to find two distinct inputs that produce the same hash output. Mathematically, collisions must exist for any fixed-size hash function (by the pigeonhole principle), but a strong hash function makes finding them astronomically difficult. A "collision attack" specifically targets the hash function's mathematical structure to find any two inputs that hash to the same value. A "second preimage attack" targets a specific input, trying to find a different input that hashes to the same value.

**Preimage Resistance** means that given a hash value `h`, it should be computationally infeasible to find any input `m` such that `hash(m) = h`. This is also called "one-wayness"—you can compute a hash easily, but you cannot reverse the operation. This property protects passwords stored as hashes: even if an attacker obtains the hash, they cannot determine the original password.

**Hash Table** — In data structures, a hash function maps keys to array indices in a hash table. The function computes an index where the value is stored or retrieved. A good hash function for hash tables distributes keys uniformly across buckets to minimize collisions. Common non-cryptographic hash functions for hash tables include MurmurHash, FNV (Fowler-Noll-Vo), and djb2.

**Merkle Tree** — A hash tree structure where each leaf node is the hash of a data block, and each non-leaf node is the hash of its children's hashes. Merkle trees enable efficient and secure verification of large datasets, and are used in Bitcoin's blockchain (to commit transactions into blocks), in distributed storage systems for consistency verification, and in content-addressed storage systems like Git.

## How It Works

Cryptographic hash functions operate through iterated compression: the input is processed in fixed-size blocks using a compression function, with the state being updated iteratively. This design, pioneered by Merkle and Damgård, provides a way to hash inputs of arbitrary length while maintaining the security properties of the compression function.

```text
Input: "hello"
       │
       ▼
[Preprocessing: Pad to multiple of block size]
       │
       ▼
[Block 1: "hell"] ──► Compression Function ──┐
       │                                     │
[Block 2: "o___"] ──► Compression Function ──┼──► Hash Value
       │                              (iterate over all blocks)
[IV: Initial Vector] ──►─┘
```

SHA-256, for example, processes input in 512-bit (64-byte) blocks using a compression function that mixes data through 64 rounds of bitwise operations, modular addition, and logical functions. The input is preprocessed with a length append and padding bits, then each 512-bit block updates a 256-bit state register through the compression rounds.

A simple non-cryptographic hash function for a hash table might work as follows:

```python
def simple_hash(key: str, table_size: int) -> int:
    """A simple polynomial rolling hash for string keys."""
    hash_value = 0
    prime = 31  # commonly used prime multiplier
    for char in key:
        hash_value = (hash_value * prime + ord(char)) % table_size
    return hash_value

# Example: hash "user:12345" into a table of size 100
bucket_index = simple_hash("user:12345", 100)  # Returns 0-99
```

In a hash table, the hash function determines which bucket a key-value pair belongs to. On insertion, the key is hashed to find the bucket; on lookup, the key is hashed again and the bucket is checked for the key. When two different keys hash to the same bucket (a collision), the hash table resolves it using chaining (storing multiple entries per bucket as a linked list) or open addressing (probing other buckets sequentially).

## Practical Applications

**Password Storage** — Websites store password hashes rather than plaintext passwords. When a user logs in, the submitted password is hashed and compared to the stored hash. Even if the database is breached, the attacker only has hashes, not actual passwords. To make brute-force attacks harder, password hashing uses deliberately slow algorithms (Argon2, bcrypt, scrypt, PBKDF2) that are expensive to compute, unlike fast general-purpose hashes like SHA-256.

**Digital Signatures and Integrity Verification** — A document is hashed, and the hash is encrypted with a private key to create a signature. Anyone with the corresponding public key can verify the signature by decrypting it, recomputing the hash, and comparing. This is how TLS certificates, software distribution signatures, and blockchain transactions work.

**Blockchain and Proof of Work** — Bitcoin and similar cryptocurrencies use SHA-256 double hashing to link blocks together. The "proof of work" requires miners to find a nonce value that, when hashed with the block's data, produces a hash with a certain number of leading zero bits. Finding such a nonce requires brute-force search but verifying it requires only one hash computation.

**Content Identification** — Hashes serve as content-addressed identifiers. Git uses SHA-1 (now migrating to SHA-256) to identify commits, trees, and blob objects. IPFS uses multihash to address content by its cryptographic hash. Anti-virus scanners hash known malicious files to detect them without scanning entire files.

**Bloom Filters** — A probabilistic data structure that uses multiple hash functions to test set membership. A Bloom filter can say "probably present" or "definitely not present" with tunable false-positive rates, using minimal memory. Used in web browsers (to quickly check if a URL is malicious), databases (to avoid unnecessary disk reads), and distributed systems (for approximate membership queries).

## Examples

Verifying file integrity after download:
```bash
# Download a file + its SHA-256 checksum file
sha256sum important-file.tar.gz
# Output: 3a7bd3e2360a3d29eea436fcfb6d1b97c2b5e44e8d5f2c8a3b9c4d2e1f0a3b4  important-file.tar.gz

# Compare against the published checksum
echo "3a7bd3e2360a3d29eea436fcfb6d1b97c2b5e44e8d5f2c8a3b9c4d2e1f0a3b4  important-file.tar.gz" | sha256sum --check
# Output: important-file.tar.gz: OK
```

Using a hash table in Python:
```python
# Python's built-in dict uses a hash table internally
user_profiles = {}

# The key "user:12345" is hashed to determine storage bucket
user_profiles["user:12345"] = {"name": "Alice", "email": "alice@example.com"}
user_profiles["user:67890"] = {"name": "Bob", "email": "bob@example.com"}

# Lookup: hash the key, find the bucket, compare the key (to handle collisions)
profile = user_profiles.get("user:67890")
```

## Related Concepts

- [[Cryptographic Hash Function]] - Hash functions designed for security-critical applications
- [[SHA-256]] - The most widely used cryptographic hash function (256-bit output)
- [[Hash Table]] - Data structure that uses hashing for fast key-value storage and retrieval
- [[Digital Signature]] - Authentication mechanism using hash functions and asymmetric cryptography
- [[Password Hashing]] - Specialized slow hashes for storing authentication credentials
- [[Merkle Tree]] - Tree structure of hashes used in blockchains and distributed systems
- [[Salting]] - Adding random data to an input before hashing to prevent rainbow table attacks
- [[Collision]] - When two different inputs produce the same hash output

## Further Reading

- [NIST SHA-3 Standard](https://csrc.nist.gov/projects/hash-functions) — Official specifications for cryptographic hash functions
- ["How Hash Functions Work"](https://youtu.be/b4b8xJ8X4uA) — Computerphile video explaining MD5, SHA-1, and SHA-256 internals
- ["The Rainbow Table Problem"](https://youtu.be/0WiM0gibE3A) — Why salting and slow hashing are essential for passwords
- Argon2 specification (RFC 9106) — The winner of the Password Hashing Competition

## Personal Notes

Hash functions are deceptively simple (input goes in, fixed-size digest comes out) but have profound implications throughout computer science. A common misconception is that any hash function is fine for security purposes—MD5 and SHA-1 were once considered secure but are now completely broken for cryptographic use due to collision attacks. Always use modern, standard algorithms (SHA-256, SHA-3, BLAKE3) for anything security-sensitive. For password storage, never use fast hashes—use Argon2id, bcrypt, or scrypt with appropriate cost parameters. Also note that hash functions are not encryption: they are one-way and lose information; you cannot recover the original input from a hash, which is exactly why they're safe for password storage but useless for storing reversible data.
