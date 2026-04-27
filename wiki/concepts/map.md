---
title: "Map"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, programming, collections, computer-science]
---

# Map

## Overview

A Map (also known as a dictionary, associative array, hash table, or symbol table) is an abstract data type that stores key-value pairs, allowing efficient retrieval of values based on their associated keys. Unlike arrays that use numeric indices, Maps use keys of any data type—strings, numbers, objects, or functions—to directly access values. This makes Maps essential for scenarios requiring fast lookups, caching, counting, and organizing data by unique identifiers.

Maps are fundamental to computer science and appear in virtually every programming language. They provide an intuitive way to model relationships between entities and enable O(1) average-case lookup time when implemented with hash functions. Understanding Maps is crucial for software development, algorithm design, and system programming.

## Key Concepts

**Key-Value Pairing**: Each entry in a Map consists of a unique key and an associated value. Keys must be unique within a Map, but values can be duplicated across different keys.

**Hash Functions**: Most Map implementations use hash functions to compute an index (bucket) for each key, enabling constant-time average access. The quality of the hash function directly impacts performance.

**Collision Handling**: When two keys hash to the same bucket, collision resolution strategies like chaining (linked lists) or open addressing (linear/quadratic probing) are used.

**Load Factor**: The ratio of entries to the number of buckets. A high load factor increases collision probability and can degrade performance, triggering automatic rehashing.

**Immutability of Keys**: Keys are typically required to be immutable (hashable) types. Using mutable objects as keys can lead to unpredictable behavior.

## How It Works

When storing a value:

1. The key is passed through a hash function, producing a hash code
2. The hash code is compressed to determine the bucket index
3. The key-value pair is stored in that bucket (handling collisions if needed)

When retrieving a value:

1. The key is hashed to find the target bucket
2. If collisions exist, the bucket is searched to find the exact key
3. The corresponding value is returned

```text
Insert("name", "Alice")
    │
    ▼
hash("name") → 42
    │
    ▼
bucket[42] → [("name", "Alice")]
    │
    ▼
Value stored successfully

Retrieve("name")
    │
    ▼
hash("name") → 42
    │
    ▼
bucket[42] → [("name", "Alice")]
    │
    ▼
Return "Alice"
```

## Practical Applications

- **Caching**: Storing computed results keyed by input parameters for fast retrieval
- **Counting Occurrences**: Tracking frequency of elements in collections
- **Configuration Storage**: Managing application settings as key-value pairs
- **Memoization**: Caching expensive function results in dynamic programming
- **Lookup Tables**: Precomputing and storing results for fast access

## Examples

JavaScript Map operations:

```javascript
const userMap = new Map();

// Setting and getting values
userMap.set("id1", { name: "Alice", age: 30 });
userMap.set("id2", { name: "Bob", age: 25 });

// O(1) lookup
const user = userMap.get("id1");
console.log(user.name); // "Alice"

// Checking existence
console.log(userMap.has("id1")); // true

// Iteration
for (const [id, user] of userMap) {
  console.log(`${id}: ${user.name}`);
}

// Deletion
userMap.delete("id2");
```

Python dictionary operations:

```python
word_counts = {}

# Counting word frequencies
text = "the quick brown fox jumps over the lazy dog"
for word in text.split():
    word_counts[word] = word_counts.get(word, 0) + 1

print(word_counts)
# {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, ...}
```

## Related Concepts

- [[Hash Function]] - Functions that map keys to bucket indices
- [[Hash Table]] - The underlying data structure implementing Maps
- [[Set]] - Collection of unique elements without associated values
- [[Array]] - Sequential data structure with numeric indices
- [[Trie]] - Tree data structure used for string keys

## Further Reading

- [Hash Tables - CLRS Introduction to Algorithms](https://en.wikipedia.org/wiki/Hash_table)
- [Python dict Implementation](https://docs.python.org/3/library/stdtypes.html#dict)
- [JavaScript Map Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)

## Personal Notes

Maps are my go-to data structure when I need to associate unique identifiers with data or track frequencies. The JavaScript Map vs plain object debate is real—Maps preserve insertion order and allow non-string keys, making them superior for most use cases. I've found that visualizing hash collisions helps understand why choosing good hash functions matters for performance in production systems.
