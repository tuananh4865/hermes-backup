---
title: "Memory Hierarchy"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [computer-architecture, memory, performance, caching]
---

# Memory Hierarchy

The memory hierarchy is a concept in computer architecture that organizes different types of memory into levels based on trade-offs between speed, size, and cost. Modern computers use multiple levels of memory storage, from fast but small registers close to the CPU to slow but large storage devices like SSDs and hard drives, creating a pyramid-like structure where data moves between levels to balance performance and capacity requirements.

## Overview

The memory hierarchy exists because no single memory type simultaneously offers the best speed, lowest cost, and maximum capacity. CPU registers provide the fastest access (sub-nanosecond latency) but can hold only a few dozen bytes. Meanwhile, main memory (RAM) offers megabytes to gigabytes of capacity but with higher latency. Disk storage provides terabytes of space but operates orders of magnitude slower.

The key insight is that programs exhibit locality—temporal locality (recently accessed items are likely to be accessed again) and spatial locality (items near recently accessed data will likely be accessed soon). The memory hierarchy exploits this by keeping frequently accessed data in faster, smaller caches while less-used data remains in slower, larger storage.

Each level in the hierarchy serves as a cache for the level below it, transparently moving data when needed. Understanding this hierarchy is critical for writing performant code, as memory access patterns can determine whether an algorithm runs in microseconds or milliseconds.

## Key Concepts

**Cache Levels (L1, L2, L3)**: Modern CPUs include multiple cache levels. L1 is smallest and fastest (typically 32-64KB per core), L2 is larger but slower (256KB-1MB), and L3 is shared across cores (several MB to tens of MB). Each level is measured by hit rate and miss penalty.

**Cache Hit/Miss**: A cache hit occurs when the requested data is found in cache (fast). A cache miss means the data must be fetched from a slower level (expensive). The miss penalty is the additional time required to retrieve data from lower memory levels.

**Temporal Locality**: The tendency for previously accessed memory locations to be accessed again soon. This is why keeping loops small and avoiding unnecessary memory clears improves performance.

**Spatial Locality**: The tendency for memory locations near recently accessed locations to be accessed. This is why iterating through arrays sequentially is faster than random access.

**Cache Line**: The minimum unit of data transferred between cache and main memory, typically 64 bytes. When you access one byte, an entire cache line is loaded into cache.

**Write Policy**: Determines how writes to cache are propagated to lower levels—write-through (immediate) or write-back (deferred until eviction).

## How It Works

The memory hierarchy operates through a hierarchical lookup and data transfer mechanism:

1. **CPU Request**: When the CPU needs data, it first checks the TLB (Translation Lookaside Buffer) for the physical address, then requests data from L1 cache.

2. **Cache Lookup**: The cache controller checks if the requested data is in L1. If found (hit), data returns to the CPU in 1-2 cycles. If not (miss), the request proceeds to L2.

3. **Hierarchy Traversal**: The request continues through L2, then L3, then main memory (DRAM), each level adding latency. Modern DRAM has 50-100ns latency.

4. **Data Transfer**: When data is found at a lower level, it's not just returned—it's also copied into all upper levels for future access (cache fill).

5. **Eviction**: When cache is full, the controller must evict existing data to make room. Common eviction policies include LRU (Least Recently Used) and random eviction.

```c
// Example demonstrating cache-conscious programming
// This loops cache-friendly (spatial locality)
int sum = 0;
int array[1000];
for (int i = 0; i < 1000; i++) {
    sum += array[i];  // Sequential access - cache friendly
}

// vs. strided access which is cache-unfriendly
for (int i = 0; i < 1000; i += 10) {
    sum += array[i];  // Strided access - may miss cache each time
}
```

## Practical Applications

- **Database Performance**: Database engines implement their own buffer pools that act as caches for disk pages, working in conjunction with CPU caches and OS page cache to minimize disk I/O.

- **Compiler Optimization**: Modern compilers reorder code and restructure loops to improve cache utilization, taking advantage of known cache sizes and line sizes.

- **Game Development**: Game engines use data-oriented design, organizing memory in Structure of Arrays (SoA) rather than Array of Structures (AoS) to improve cache efficiency during rendering.

- **Scientific Computing**: Matrix multiplication algorithms are blocked/tiled to keep working sets in cache, dramatically improving performance over naive implementations.

- **Web Servers**: Content delivery networks and reverse proxies implement multi-tier caching (L1 memory, L2 SSD, L3 spinning disk) to serve static content at high throughput.

## Examples

**Cache Line Impact on Struct Layout**:
```c
// Poor cache utilization - data scattered across cache lines
struct PointBad {
    float x;
    float y;
    float z;
    char name[64];  // Pushes next point to different cache line
};

// Good cache utilization - keep related data together
struct PointGood {
    float x, y, z;
};  // 12 bytes fits cleanly in cache line with padding
```

**Measuring Cache Performance**:
```bash
# Use perf to analyze cache misses
perf stat -e cache-references,cache-misses ./program
```

## Related Concepts

- [[CPU Cache]] — Hardware cache memory (L1/L2/L3)
- [[Virtual Memory]] — Memory management that uses disk as extension of RAM
- [[Locality of Reference]] — The principle that makes caching effective
- [[DRAM]] — Dynamic RAM used for main memory
- [[SSD Storage]] — Solid-state storage bridging memory and disk
- [[Cache Coherency]] — Protocol for maintaining consistency across CPU caches in multiprocessors

## Further Reading

- [What Every Programmer Should Know About Memory](https://people.freebsd.org/~ lstewart/articles/cpumemory.pdf) — Classic paper by Ulrich Drepper
- [CPU Cache Explained](https://www.youtube.com/watch?v=WDIkqP4t1Sc) — Visual explanation of cache behavior
- [Memory Hierarchy Design](https://arxiv.org/abs/1903.02728) — Academic survey on modern memory hierarchies

## Personal Notes

Understanding the memory hierarchy fundamentally changed how I think about performance. The 1000x latency difference between register access and DRAM access means that algorithmic complexity alone doesn't determine real-world performance—memory access patterns matter equally. Profile before optimizing: cache misses are often the bottleneck, and visualizing your data layout with cache lines in mind can yield 10x improvements without changing algorithmic complexity.
