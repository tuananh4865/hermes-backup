---
title: Android Runtime
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [android, mobile-development, runtime-environment, dalvik, art]
---

# Android Runtime

## Overview

The Android Runtime (ART) is the managed runtime environment used by Android applications. It executes DEX (Dalvik Executable) bytecode, providing the core services that allow Android apps to run: memory management, thread management, security enforcement, and interoperability between Java/Kotlin code and native libraries. ART replaced the original Dalvik virtual machine as the default runtime starting with Android 5.0 Lollipop.

Android apps are compiled to DEX bytecode, which is designed to be efficient on memory-constrained devices. The runtime then interprets or compiles this bytecode to native machine code at installation time (AOT compilation) or runtime (JIT compilation). This two-tier approach balances startup time against ongoing performance.

Understanding ART is essential for Android developers, especially when debugging performance issues, memory leaks, or working with native code via JNI (Java Native Interface).

## Key Concepts

### DEX Bytecode

Android does not use standard Java bytecode (.class files). Instead, the SDK tools compile Java/Kotlin source to DEX format (.dex), which packages multiple classes into a single file optimized for size and execution speed. DEX files are smaller and designed for the Android runtime's memory model.

### Ahead-of-Time (AOT) Compilation

AOT compilation converts DEX bytecode to native machine code at app installation time. This eliminates interpretation overhead during execution, resulting in faster app startup and more consistent performance. However, it increases installation time and storage requirements.

### Just-in-Time (JIT) Compilation

JIT compiles bytecode to native code at runtime, profile-guided. It allows the runtime to adapt optimizations based on actual execution patterns. Android 7.0 introduced JIT into ART, combining it with AOT for optimal results—AOT for stable, startup code, and JIT for less-frequently-used code paths.

### Garbage Collection

ART manages memory through garbage collection, automatically reclaiming objects no longer referenced by the application. Android's GC is designed to minimize pause times and avoid jank. Key improvements over Dalvik include parallel GC and more efficient object allocation.

### Memory Management

The runtime maintains separate heap spaces for different object types, uses thread-local allocation buffers for speed, and provides profiling tools for developers to identify memory issues.

## How It Works

When you install an Android app:

1. Package Manager extracts the APK and verifies signatures
2. `dex2oat` compiles DEX bytecode to native ELF binaries (AOT)
3. The compiled code is stored in `/data/dalvik-cache/`
4. At runtime, ART loads these native binaries and executes them

For apps using JIT:
1. App starts with interpreter executing DEX bytecode
2. JIT profiler identifies hot code paths
3. JIT compiler generates optimized native code
4. Hot code is executed as native, reducing interpretation overhead

```
App Launch
    ↓
ART loads compiled code from dalvik-cache
    ↓
App executes native code directly on CPU
    ↓
JIT monitors execution, compiling additional hot paths
    ↓
Runtime GC manages memory as app runs
```

## Practical Applications

### App Performance Optimization

Understanding ART helps developers identify bottlenecks. Tools like Android Profiler, `systrace`, and `perfetto` reveal GC pauses, JIT compilation overhead, and memory allocation patterns.

### Memory Leak Debugging

ART's heap dumps and allocation tracking help identify leaks. Common causes include keeping references to Context objects, anonymous inner classes capturing enclosing references, and improper use of static collections.

### Native Development (NDK)

Apps using C/C++ via JNI interact with ART through JNI bridges. The runtime handles object marshaling between managed (Java/Kotlin) and native worlds.

### App Compatibility

When switching device manufacturers or Android versions, ART ensures consistent behavior. However, differences in runtime implementation can cause subtle compatibility issues.

## Examples

Monitoring ART behavior with ADB:

```bash
# View running ART garbage collection info
adb shell dumpsys meminfo <package_name>

# Check JIT status for an app
adb shell dumpsys package <package_name> | grep -i jit

# Clear dalvik cache (forces AOT recompilation)
adb shell rm /data/dalvik-cache/*

# View runtime version info
adb shell getprop ro.build.version.sdk
adb shell getprop dalvik.vm.dex2oat-Xms
```

## Related Concepts

- [[Android Development]] - The broader practice of building Android apps
- [[Dalvik VM]] - The predecessor to ART
- [[Garbage Collection]] - Automatic memory management
- [[JNI]] - Java Native Interface for calling native code
- [[Android SDK]] - Development tools and libraries

## Further Reading

- Android Developer Documentation on ART
- "Inside the Android Runtime" presentation from Google I/O
- AOSP source code for ART implementation

## Personal Notes

ART represents Google's efforts to optimize Android for the constraints of mobile devices. The JIT + AOT combination is particularly clever—fast startup from AOT while allowing runtime optimization of less-frequently-used code. When debugging, remember that GC pause times are often invisible to users but manifest as "jank" in animations. The `systrace` tool is invaluable for seeing what's actually happening under the hood. Also, clearing dalvik-cache can be a useful troubleshooting step when facing奇怪的 runtime behavior.
