---
title: Hash Table
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, algorithms, hash-function, computer-science, o-1]
---

# Hash Table

## Overview

A hash table (also called a hash map) is a fundamental data structure that provides associative array functionality — storing key-value pairs and enabling average-case constant time O(1) lookup, insertion, and deletion. The hash table achieves this remarkable performance by using a [[hash-function]] to compute an index into an array of buckets, directly mapping the key to a memory location. This direct addressing is what distinguishes hash tables from tree-based [[data-structures]] like binary search trees or B-trees, which require O(log n) comparisons even in the best case.

Hash tables are one of the most widely used data structures in software engineering. They underpin the dictionaries in Python and JavaScript, the maps in Java and Go, the hash maps in C++, and the associative arrays in PHP. Database systems use hash indexes for fast lookups, operating systems use hash tables for symbol tables and cache management, and network routers use them for routing tables. Understanding hash tables — their strengths, their failure modes, and the tradeoffs involved in their implementation — is essential knowledge for any software engineer.

## Key Concepts

### The Hash Function

The hash function is the heart of a hash table. It takes a key (which can be a string, number, object, or any other data type) and returns an integer called a **hash code** or simply a **hash**. This integer is then mapped to an array index through the modulo operation: `index = hash(key) % array_size`.

A good hash function has three critical properties:

1. **Deterministic**: The same key always produces the same hash code
2. **Uniform distribution**: Hash codes are evenly distributed across the possible range, minimizing collisions
3. **Fast computation**: The hash function itself should be efficient

For integer keys, a simple identity function (returning the key itself) or a multiplicative method works well. For string keys, more complex functions like DJB2, FNV-1a, or MurmurHash3 are commonly used. Modern languages typically provide built-in hash functions for their native types that are designed to be fast and produce well-distributed output.

### Collision Resolution

Since the space of possible keys is typically much larger than the array size, and the hash function is not injective (different keys can produce the same hash), **collisions** — where two different keys map to the same array index — are inevitable. Hash table implementations must handle collisions gracefully. The two primary strategies are:

**Chaining**: Each array bucket is a linked list (or more efficiently, a dynamic array) of entries that collide at the same index. When a collision occurs, the new entry is appended to the chain. Lookup requires traversing the chain at the computed index until the matching key is found. Chaining has O(n) worst-case lookup but O(1) average case with a good hash function and sufficient load factor.

**Open Addressing**: Instead of storing colliding entries elsewhere, the table probes other buckets according to a defined probe sequence until an empty slot is found. Common probe strategies include linear probing (checking consecutive slots), quadratic probing (using quadratic increments), and double hashing (using a secondary hash function for the probe step). Open addressing keeps memory usage predictable but requires careful tuning of the load factor.

### Load Factor and Resizing

The **load factor** (often denoted α) is the ratio of stored entries to the number of buckets: α = n / m, where n is the number of entries and m is the table size. The load factor directly affects collision frequency. As the table fills up, collisions become more frequent and performance degrades.

Most hash table implementations dynamically resize (rehash) when the load factor exceeds a threshold — typically 0.7. During resizing, a new, larger array is allocated and all existing entries are re-inserted (with new hash values based on the larger size). This is an O(n) operation but happens infrequently enough that the amortized cost per insertion remains O(1).

### Performance Characteristics

Under reasonable assumptions (a good hash function, a load factor kept below the resize threshold, and no adversarial input), hash tables provide:

| Operation | Average Case | Worst Case |
|-----------|-------------|-----------|
| Search     | O(1)        | O(n)      |
| Insert    | O(1)        | O(n)      |
| Delete    | O(1)        | O(n)      |

The worst case occurs when all keys hash to the same bucket (degenerates to a linked list in chaining) or when the probe sequence loops in open addressing. These pathological cases are rare in practice but can be weaponized in denial-of-service attacks, as demonstrated by the 2011 attack on Perl's hash table implementation.

## How It Works

A hash table implementation combines the above concepts into a coherent system:

1. **Key hashing**: Apply the hash function to the key, producing a hash code
2. **Index computation**: Reduce the hash code to an array index: `index = hash(key) % array_size`
3. **Collision handling**: Handle any collision at that index (chain or probe)
4. **Comparison**: Compare the search key with stored keys in the selected bucket to find the exact match
5. **Value retrieval/insertion/deletion**: Perform the requested operation

Modern implementations optimize heavily. For example, Python's dict uses open addressing with a carefully chosen probe sequence, stores both key and value together to improve cache locality, and uses a randomization seed in the hash function to prevent hash-flooding attacks. Java's HashMap uses separate chaining with tree bins (converting long chains to balanced trees when they exceed a threshold) to prevent O(n) worst cases.

## Practical Applications

Hash tables are ubiquitous in software:

**Database Indexes**: Most database systems use hash indexes as an option for equality lookups. While B-tree indexes support range queries and ordering, hash indexes provide the fastest possible point queries. Key-value stores like [[dynamodb]] and [[redis]] use hash tables (or variations like LSM trees) as their primary storage mechanism.

**Caches**: In-memory caches like [[memcached]] and [[redis]] are essentially distributed hash tables. The key maps to a value stored in memory, providing O(1) access for frequently accessed data and dramatically reducing database or API load.

**Sets**: A hash set is a hash table without values — it only stores keys and supports O(1) membership testing. This is useful for deduplication, tracking seen items, and implementing graph algorithms.

**Memoization**: Dynamic programming implementations use hash tables to cache computed results, converting recursive algorithms with overlapping subproblems into efficient iterative ones.

## Examples

A minimal hash table implementation using chaining in Python:

```python
class HashTable:
    def __init__(self, size=16, load_factor_threshold=0.75):
        self.size = size
        self.count = 0
        self.load_factor_threshold = load_factor_threshold
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        """Hash function using Python's built-in hash with modulo."""
        return hash(key) % self.size

    def _resize(self):
        """Double the table size and rehash all entries."""
        old_buckets = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)

    def insert(self, key, value):
        """Insert or update a key-value pair."""
        if self.count / self.size >= self.load_factor_threshold:
            self._resize()

        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        bucket.append((key, value))
        self.count += 1

    def get(self, key, default=None):
        """Retrieve value by key, returning default if not found."""
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return default

    def delete(self, key):
        """Remove a key-value pair by key."""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return True
        return False
```

## Related Concepts

- [[hash-function]] — The mathematical foundation enabling hash table indexing
- [[data-structures]] — The broader category of organizational schemes for data
- [[algorithm-complexity]] — The O(1) average case performance analysis framework
- [[memcached]] — Distributed hash table used for caching
- [[redis]] — In-memory hash table store with persistence
- [[database-index]] — Database structures that often use hash indexing
- [[consistent-hashing]] — Technique for distributed hash tables

## Further Reading

- CLRS (Cormen et al.), *Introduction to Algorithms* — Chapter 11 on hash tables
- "The Go Programming Language" —Effective Go's treatment of map internals
- Python's dict implementation — CPython source for a production-grade hash table
- "Hash Table Attacks" — Research on denial-of-service via hash collision

## Personal Notes

The most surprising thing about hash tables for many developers is that their O(1) performance is an average case guarantee, not a worst-case one. The worst case is O(n), and while it's rare, it can be exploited. Python's hash randomization (introduced in response to the 2011 attack) makes hash tables safe against adversarial input by default. For most everyday use, you never need to think about hash table internals — but understanding load factor tuning, the cost of resizing, and the difference between chaining and open addressing becomes important when you're building high-performance systems or tuning cache behavior.
