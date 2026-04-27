---
title: "Cache Coherence"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [computer-architecture, multiprocessing, memory-systems, concurrency]
---

# Cache Coherence

Cache coherence addresses a fundamental problem in symmetric multiprocessing (SMP) and multi-core systems: ensuring that multiple processors sharing a common memory bus maintain consistent views of shared data. When two cores have cached copies of the same memory location, and one modifies it, the other must eventually see that update—or behavior becomes unpredictable.

## Overview

Modern CPUs include multiple levels of private caches (L1, L2, sometimes L3) between the processor cores and main memory. Each core can read and write its local cache independently, dramatically speeding up memory access. However, when multiple cores access the same memory location concurrently, writes by one core can invalidate stale copies held by others.

Cache coherence protocols solve this by defining rules about when writes become visible to other processors and how conflicts are resolved. The goal is the **coherence property**: any read of a memory location returns the value of the most recent write to that location, regardless of which core performed it.

The challenge scales with core count. With N cores, there are N copies of each potentially-shared cache line. The protocol must guarantee that modifications propagate correctly and that memory operations appear to happen in a globally consistent order.

## Snooping vs. Directory Protocols

There are two primary approaches to maintaining coherence:

**Snooping protocols** assume a shared medium (typically a bus) where all cache controllers can observe all memory transactions. Each cache line is tagged with a state, and every transaction is broadcast to all controllers. When a core writes to a line other cores hold, those copies are invalidated.

The widely-used **MESI protocol** (Modified, Exclusive, Shared, Invalid) defines four states per cache line:
- **Modified**: The line is dirty—this core has written to it, and main memory is stale
- **Exclusive**: The line is clean and only this core holds it
- **Shared**: The line is clean but other cores may also hold it
- **Invalid**: The line is not present or is stale

Transitions between states happen in response to processor loads/stores and bus transactions. The "Modified" state eliminates the need to write to memory immediately, while "Shared" allows multiple cores to hold read-only copies efficiently.

**Directory protocols** scale better for larger systems. A central directory tracks which cores have copies of each cache line and whether they're clean or modified. Before a write occurs, the directory invalidates other copies. This avoids broadcast traffic but introduces lookup latency for the directory itself.

More advanced variants like **MOESI** add an "Owned" state to further reduce memory traffic by allowing a core to retain a stale copy while serving other processors.

## Memory Barriers and Ordering

Coherence protocols operate at the cache-line level, but programmers and compilers often assume stronger memory ordering than hardware provides. Without explicit memory barriers (fences), a processor may reorder memory operations for performance, breaking assumptions in concurrent code.

x86 provides strong ordering (stores don't reorder with later loads), while ARM and RISC-V provide weaker ordering where memory reordering is visible to other cores. Writing correct lock-free code requires understanding both the coherence protocol and the memory model.

```c
// Memory barrier example
volatile int flag = 0;
int data = 0;

// Thread A (writer)
data = 42;
__asm__ __volatile__("mfence" : : : "memory"); // Full memory barrier
flag = 1;

// Thread B (reader)
while (flag == 0) { /* spin */ }
__asm__ __volatile__("mfence" : : : "memory");
assert(data == 42); // Without barriers, this could fail on weak-ordering CPUs
```

## False Sharing

Even when different cores access unrelated variables, they can interfere if those variables share the same cache line (typically 64 bytes). One core's frequent writes to its variable invalidate the other core's entire cache line, causing performance collapse.

Detecting false sharing requires profiling tools (perf on Linux, Instruments on macOS). Solutions include padding structures to separate variables across cache lines, or redesigning data structures to avoid concurrent access to adjacent memory.

## Practical Applications

Cache coherence is invisible to most application programmers thanks to operating system synchronization primitives (mutexes, semaphores) and language-level constructs (atomic operations, concurrent data structures). However, understanding it matters when:

- Writing high-performance concurrent code (lock-free algorithms)
- Debugging performance issues in NUMA systems
- Designing operating system kernels and device drivers
- Working with RDMA and distributed shared memory

Database systems and in-memory caches (Redis, Memcached) face analogous coherence challenges when replicating data across nodes, though at a higher level of abstraction.

## Related Concepts

- [[MESI Protocol]] - Four-state cache coherence protocol
- [[Memory Barrier]] - Instructions enforcing memory ordering
- [[False Sharing]] - Performance issue in concurrent code
- [[NUMA]] - Non-uniform memory access architecture
- [[Snooping Protocol]] - Bus-based coherence mechanism
- [[Directory Protocol]] - Scalable coherence for many-core systems

## Further Reading

- Hennessy, J. L., & Patterson, D. A. "Computer Architecture: A Quantitative Approach"
- Sorin, D. J., Hill, M. D., & Wood, D. A. "A Primer on Memory Consistency and Cache Coherence"
- Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 3A

## Personal Notes

Cache coherence is one of those topics where the gap between theory and practice is enormous. The protocols themselves are elegant, but real implementations add complexity for performance (write buffers, speculation, non-blocking caches). When debugging mysterious performance issues on multi-core systems, false sharing is often the culprit—worth remembering before profiling more sophisticated problems.
