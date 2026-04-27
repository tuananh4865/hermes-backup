---
title: "JMH"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [java, benchmarking, performance, jvm, microbenchmark]
---

# JMH (Java Microbenchmark Harness)

## Overview

JMH is a Java harness for building, running, and analyzing microbenchmarks written in Java and other JVM languages. Developed as part of the OpenJDK project, JMH addresses the fundamental challenge of measuring JVM performance: the JVM is a complex runtime with adaptive compilation, garbage collection, and speculative optimizations that can produce wildly inconsistent results if benchmarks are not properly controlled.

Microbenchmarking on the JVM is notoriously difficult. Naive benchmarks often measure the wrong thing— JVM warmup effects, dead code elimination, loop unrolling, and OSR (On-Stack Replacement) transitions can skew results in ways that have nothing to do with the code being tested. JMH provides the infrastructure to handle these complexities automatically.

## Key Concepts

**Warmup Iterations** are runs performed before measurement begins to trigger JIT compilation. The JVM doesn't execute optimized machine code immediately; it starts interpreted and progressively compiles hot paths. JMH runs a configurable number of warmup iterations so that the benchmark measures steady-state performance, not the transient compilation phase.

**Measurement Iterations** are the actual benchmark runs that produce data. JMH runs multiple iterations and computes statistics (mean, median, stddev) to account for variance.

**Forking** is the practice of running each benchmark in a fresh JVM process. This prevents state from one benchmark (e.g., JIT-compiled code, loaded classes) from influencing another. JMH forks by default, isolating benchmarks completely.

**Benchmark Modes** control what is measured. The main modes are:
- `Throughput`: operations per unit time (`ops/ms`)
- `AverageTime`: average time per operation (`us/op`)
- `SampleTime`: distributions with percentiles
- `SingleShotTime`: a single execution (useful for cold-start measurement)

**Benchmark Parameters** are annotated fields that allow running the same benchmark with different inputs, enabling comparative analysis across configurations.

## How It Works

A JMH benchmark is a Java class annotated with `@Benchmark` on methods that contain the code to measure. The `@BenchmarkMode`, `@Warmup`, `@Measurement`, `@Fork`, and `@OutputTimeUnit` annotations control execution. JMH uses annotation processors to generate the benchmark harness code, and the `jmh-gradle-plugin` or `maven-shade-plugin` packages everything into an executable JAR.

During execution, JMH launches forked JVM processes, runs warmup iterations, then measurement iterations, and collects results. The framework handles thread management, CPU affinity hints, and synchronization to ensure accurate timing. JMH uses `System.nanoTime()` for high-resolution timing and accounts for overhead through baseline calibration.

Blackhole consumer is a core JMH feature: results are passed to `Blackhole.consumeCPU()` or `Blackhole.consume()` to prevent the JVM from optimizing away computation as dead code, since a benchmark that computes but discards results may be entirely eliminated by the JIT compiler.

## Practical Applications

- **Hot Path Optimization**: Identify which alternative implementation of a critical algorithm is faster in a tight loop.
- **Library Comparison**: Evaluate competing libraries (e.g., JSON parsers, collection implementations) with controlled, reproducible benchmarks.
- **Regression Detection**: Integrate JMH benchmarks into CI to catch performance regressions before they reach production.
- **JVM Tuning**: Test the effect of JVM flags like `-XX:+UseG1GC` or `-Xms` on specific workloads.
- **Algorithm Analysis**: Understand the real-world complexity of data structures and algorithms beyond theoretical Big-O notation.

## Examples

A simple JMH benchmark comparing StringBuilder vs StringBuffer:

```java
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 5, time = 1)
@Fork(1)
public class StringConcatenationBenchmark {

    @Benchmark
    public void stringBuilder(Blackhole bh) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            sb.append("a");
        }
        bh.consume(sb.toString());
    }

    @Benchmark
    public void stringBuffer(Blackhole bh) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < 1000; i++) {
            sb.append("a");
        }
        bh.consume(sb.toString());
    }
}
```

Run with:
```bash
java -jar target/jmh-benchmarks.jar StringConcatenationBenchmark -f 1
```

## Related Concepts

- [[Java]] - The language JMH benchmarks run on
- [[JVM]] - The virtual machine that executes Java bytecode
- [[Performance Optimization]] - The broader discipline JMH supports
- [[Garbage Collection]] - GC behavior is a frequent confounder in benchmarks
- [[JIT Compilation]] - JIT warmup effects are why warmup iterations matter
- [[Self-Healing Wiki]] - The system that auto-created this page

## Further Reading

- [JMH official documentation](https://shipilev.net/blog/2014/nanotrusting-nanotime/) - Performance measurement fundamentals
- [JMH Samples](https://github.com/openjdk/jmh/tree/master/jmh-samples) - Extensive example benchmarks
- [Aleksey Shipilёv's Blog](https://shipilev.net/) - JVM benchmarking wisdom from the JMH author

## Personal Notes

JMH is indispensable when you need real performance data rather than guesses. I've used it to settle debates about whether `StringBuilder` or string concatenation in a loop is faster (StringBuilder, by a significant margin at scale), and to catch performance regressions in library upgrades. The biggest lesson: always profile first and benchmark only what you've identified as hot paths—benchmarking cold code is rarely worth the effort.
