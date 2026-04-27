---
title: "Compiled Languages"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [programming-languages, compilers, binary, machine-code, build-process]
---

# Compiled Languages

## Overview

Compiled languages are programming languages whose source code is translated (compiled) into machine code or an intermediate representation by a compiler before execution. This compilation step produces standalone executable files or libraries that can be run directly by the operating system without requiring an interpreter. The compilation process typically happens once during development, after which the program can be executed repeatedly without recompilation.

Examples of compiled languages include C, C++, Rust, Go, Fortran, COBOL, and Assembly. Some languages like Java and C# compile to an intermediate bytecode (rather than native machine code), which is then executed by a virtual machine—this hybrid approach retains many benefits of compilation while enabling platform portability.

The compiled approach contrasts with interpreted languages like Python, JavaScript, and Ruby, where source code is translated and executed line-by-line at runtime by an interpreter.

## Key Concepts

**Compiler**: A program that translates source code from a high-level language into machine code or an intermediate form. Modern compilers perform multiple stages: lexical analysis, parsing, semantic analysis, optimization, and code generation. Examples include GCC (GNU Compiler Collection), LLVM/Clang, and MSVC.

**Machine Code**: The binary instruction set understood by a specific CPU architecture (x86-64, ARM, RISC-V). Machine code is the lowest-level programming representation, directly executable by hardware without translation.

**Linker**: After compilation produces object files (.o, .obj), the linker combines them with libraries to produce a final executable. It resolves cross-file references, performs address binding, and handles symbol tables.

**Static vs Dynamic Linking**: Static linking embeds library code into the executable at compile time, producing larger files but self-contained programs. Dynamic linking loads shared libraries (.dll, .so, .dylib) at runtime, saving memory and allowing library updates without recompilation.

**Ahead-of-Time (AOT) Compilation**: Traditional compilation done before execution. In contrast, Just-In-Time (JIT) compilation occurs during runtime (as in Java's JVM or .NET's CLR).

## How It Works

The compilation pipeline transforms human-readable source code into executable machine instructions through several phases:

```c
// Example C program
#include <stdio.h>

int square(int x) {
    return x * x;
}

int main() {
    int result = square(5);
    printf("Result: %d\n", result);
    return 0;
}
```

**Compilation stages**:

1. **Preprocessing**: The preprocessor handles `#include` directives, macro expansion, and conditional compilation. The single source file expands into a larger translation unit.

2. **Compilation**: The compiler parses the C code, builds an Abstract Syntax Tree (AST), performs type checking and semantic analysis, applies optimizations (constant folding, loop unrolling, inlining), and generates assembly or intermediate representation (IR).

3. **Assembly**: The assembler converts assembly instructions into binary object files containing machine code and relocatable symbols.

4. **Linking**: The linker combines object files, resolves external symbols (like `printf`), performs address relocation, and produces the final executable.

```
source.c → [preprocessor] → translation unit
         → [compiler] → assembly (.s)
         → [assembler] → object file (.o)
         → [linker] → executable
```

## Practical Applications

- **Systems programming**: C, C++, and Rust are preferred for operating systems, device drivers, embedded systems, and performance-critical applications where direct hardware access and minimal runtime overhead are essential.
- **Game development**: AAA titles use C++ for engine development due to its performance characteristics and fine-grained control over hardware resources.
- **Compiled languages enable optimization**: Because compilation happens before runtime, compilers can perform aggressive whole-program optimizations that interpreters cannot, resulting in faster execution.
- **Distribution**: Executables can be distributed without exposing source code, providing intellectual property protection.

## Examples

**C Compilation Walkthrough**:

```bash
# Compile C program with GCC
gcc -O2 -o program source.c

# The -O2 flag enables optimization
# Result: a native executable optimized for the host machine

# For multiple source files:
gcc -O2 -o myapp main.c utils.c -lm  # -lm links math library
```

**Rust Compilation**: Rust uses LLVM as its backend compiler. `cargo build` triggers the Rust compiler (rustc) which performs monomorphization of generics, borrow checking, and LLVM optimization passes:

```bash
cargo build --release  # Produces highly optimized executable
```

## Related Concepts

- [[Interpreted Languages]] - Execute code line-by-line without prior compilation
- [[C Programming Language]] - The quintessential compiled language
- [[Linker]] - Combines object files into executables
- [[Assembly Language]] - Low-level symbolic representation of machine code
- [[Just-in-Time Compilation]] - Hybrid approach used by JVM and .NET

## Further Reading

- Aho, Lam, Sethi, Ullman. "Compilers: Principles, Techniques, and Tools" (The Dragon Book)
- Warren, Henry S. "Hacker's Delight" - Bit manipulation and optimization tricks
- LLVM Documentation: https://llvm.org/docs/

## Personal Notes

The distinction between compiled and interpreted languages has blurred over time. JavaScript engines like V8 use JIT compilation to achieve performance that rivals ahead-of-time compiled languages. Similarly, PyPy uses JIT compilation for Python. When choosing a language for a project, the compilation model matters less than the ecosystem, tooling, and performance characteristics. For systems where latency is critical (game engines, trading systems, operating systems), compiled languages remain the default choice.
