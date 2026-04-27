---
title: "Perf"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [linux, performance-analysis, profiling, performance, benchmarking]
---

# Perf

## Overview

Perf is a powerful performance profiling tool for Linux systems, part of the Linux kernel tools suite. It provides hardware and software event sampling, performance counter monitoring, cache analysis, and call graph profiling. Perf helps developers identify performance bottlenecks, understand CPU utilization, and optimize system and application performance.

Originally merged into the Linux kernel in 2009, perf has become an essential tool for systems programmers, kernel developers, and performance engineers. It can profile both kernel-level and user-level code, making it versatile for understanding system behavior at all levels.

## Key Concepts

**Performance Counters**: CPU hardware registers that count specific events like CPU cycles, instructions retired, cache misses, and branch mispredictions. The kernel exposes these through the perf_event_open system call.

**Hardware Events**: Events from CPU hardware counters, such as `cpu-cycles`, `instructions`, `cache-references`, `cache-misses`, `branch-instructions`, and `branch-misses`. These require hardware support (Intel PEBS/LT, AMD IBS).

**Software Events**: Kernel-generated events like context switches, page faults, CPU migrations, and minor faults. These don't require special hardware support.

**Sampling**: Rather than counting every event, perf periodically interrupts execution to record which code was running. The sampling interval (e.g., every 1000 instructions) determines overhead vs. resolution.

**Call Graph**: Records the execution stack when samples are taken, enabling visualization of where time is spent across function call hierarchies.

**perf.data**: The binary data file where perf stores collected profiling data. It can be analyzed after collection without keeping the system under load.

## How It Works

Perf uses the kernel's perf_event subsystem to collect performance data:

1. **Counter Setup**: perf opens file descriptors for the requested events via `perf_event_open()`
2. **Event Counting/Sampling**: Depending on mode, perf either counts events or sets up overflow interrupts for sampling
3. **Data Collection**: The kernel records event data per CPU in a ring buffer
4. **Data Aggregation**: perf reads and aggregates data from all CPUs
5. **Symbol Resolution**: Addresses are mapped to function names using debug symbols (DWARF) and binary symbol tables

```bash
# Basic perf commands
perf record -g ./my_program          # Record profile with call graphs
perf record -e cycles ./my_program   # Record specific hardware events
perf stat -e cycles,instructions ./my_program  # Just count, no sampling

# Analyzing recorded data
perf report                         # Interactive report
perf report --stdio                 # Non-interactive report
perf annotate                       # Show per-instruction annotation
perf script                         # Dump raw samples

# System-wide profiling
perf top                            # Real-time system-wide profile
perf record -a -g sleep 10          # Profile entire system for 10 seconds
```

## Practical Applications

**CPU Profiling**: Identify which functions consume the most CPU cycles and why.

**Cache Analysis**: Understand cache miss patterns to optimize memory access.

**Branch Prediction Analysis**: Identify poorly predicted branches that cause pipeline stalls.

**Kernel Profiling**: Profile kernel code to find bottlenecks in system calls, scheduler, or drivers.

**Counterintelligence**: Compare performance profiles before and after changes to validate optimizations.

**Flame Graphs**: Generate flame graphs from perf data to visualize CPU usage patterns visually.

## Examples

```bash
# Profile a running process by PID
perf record -p 1234 -g -- sleep 30

# Profile specific hardware events
perf stat -e cycles,instructions,cache-references,cache-misses ./benchmark

# Example output:
#  Performance counter stats for './benchmark':
#      1,234,567,890 cycles                       # 3.2 GHz
#        567,890,123 instructions                  # 0.46 insns per cycle
#         12,345,678 cache-references              
#          1,234,567 cache-misses                  # 10.0% miss rate
#            234,567 branch-instructions
#             23,456 branch-misses                # 10.0% miss rate
#          0.385342 seconds time elapsed
```

```bash
# Generate a flame graph from perf data
perf record -F 99 -a -g -- sleep 60
perf script | stackcollapse-perf.pl | flamegraph.pl > perf.svg

# Hardware event sampling with precise addressing
perf record -e cycles:pp -a ./program
perf annotate --stdio
```

```c
// Using perf_event_open directly in code
#include <linux/perf_event.h>
#include <sys/syscall.h>
#include <unistd.h>

static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
                            int cpu, int group_fd, unsigned long flags) {
    return syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
}

int main() {
    struct perf_event_attr pe;
    long long count;
    
    memset(&pe, 0, sizeof(pe));
    pe.type = PERF_TYPE_HARDWARE;
    pe.size = sizeof(pe);
    pe.config = PERF_COUNT_HW_CPU_CYCLES;
    pe.disabled = 1;
    pe.exclude_kernel = 1;
    
    int fd = perf_event_open(&pe, 0, -1, -1, 0);
    read(fd, &count, sizeof(long long));
    
    // ... do work ...
    
    read(fd, &count, sizeof(long long));
    printf("Used %lld CPU cycles\n", count);
    close(fd);
    return 0;
}
```

## Related Concepts

- [[Flame Graphs]] - Visualization technique often used with perf data
- [[Profiling]] - The broader practice of measuring program performance
- [[Performance Analysis]] - Systematic approach to understanding system performance
- [[CPU Architecture]] - Understanding CPU internals helps interpret perf data
- [[Linux]] - The operating system where perf runs
- [[eBPF]] - Extended BPF, often used alongside perf for custom tracing

## Further Reading

- [Perf Wiki](https://perf.wiki.kernel.org/)
- "Systems Performance: Enterprise and the Cloud" by Brendan Gregg
- [Perf Examples](https://www.brendangregg.com/perf.html)
- Linux kernel documentation: `Documentation/perf/`

## Personal Notes

perf is incredibly powerful but has a steep learning curve. The `perf top` command is my go-to for quick system exploration—gives you real-time visibility into what's running. For deeper analysis, recording with call graphs and then using `perf report` or generating flame graphs provides excellent visualization. Always compile with debug symbols (-g) for user-space profiling, and use `-F 99` for high-resolution sampling.
