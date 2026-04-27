---
title: "Java"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [programming, java, jvm, object-oriented, enterprise]
---

# Java

## Overview

Java is a high-level, object-oriented programming language developed by Sun Microsystems (now owned by Oracle) and released in 1995. It was designed with the principle of "Write Once, Run Anywhere" (WORA)—Java code compiles to bytecode that runs on the Java Virtual Machine (JVM), enabling execution on any platform with a JVM implementation without recompilation.

Java is one of the most widely used programming languages in the world, particularly in enterprise software, Android app development (historically), web applications, and large-scale distributed systems. Its popularity stems from its stability, strong ecosystem, mature tooling, and extensive library support.

## Key Concepts

**Java Virtual Machine (JVM)**: The runtime engine that executes Java bytecode. The JVM provides platform independence, memory management through garbage collection, and security features. Key components include the class loader, bytecode verifier, and execution engine.

**Garbage Collection (GC)**: Automatic memory management that reclaims memory used by objects no longer referenced by the program. Java's GC implementations (Serial GC, Parallel GC, G1 GC, ZGC) offer different trade-offs between throughput and latency.

**Bytecode**: The compiled output of Java source code. Unlike native machine code, bytecode is platform-independent and requires the JVM for execution.

**JIT Compilation**: The Just-In-Time compiler inside the JVM compiles frequently executed bytecode to native machine code at runtime for improved performance.

**Classpath**: The path the JVM uses to locate user-defined classes and packages at runtime.

## How It Works

Java development and execution follows this workflow:

1. **Source Code**: Developer writes `.java` files containing class definitions
2. **Compilation**: `javac` compiler transforms source to `.class` bytecode files
3. **Class Loading**: The JVM class loader loads bytecode into the runtime
4. **Bytecode Verification**: The verifier ensures bytecode safety and validity
5. **Execution**: The JVM interprets or JIT-compiles bytecode for the host platform

```java
// Example Java program
public class HelloWorld {
    public static void main(String[] args) {
        String message = "Hello, World!";
        System.out.println(message);
        
        // Object-oriented example
        Calculator calc = new Calculator();
        int result = calc.add(5, 3);
        System.out.println("5 + 3 = " + result);
    }
}

class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
}
```

```bash
# Compile and run
javac HelloWorld.java
java HelloWorld
```

## Practical Applications

**Enterprise Software**: Java EE (now Jakarta EE) powers mission-critical business applications in finance, healthcare, and government sectors.

**Android Development**: Java was the primary language for Android apps before Kotlin's rise.

**Web Applications**: Frameworks like Spring, Struts, and Hibernate enable rapid web development.

**Big Data**: Hadoop and many big data processing frameworks are written in Java.

**Microservices**: Spring Boot and Quarkus make Java popular for cloud-native microservices.

## Examples

```java
// Modern Java with streams and lambdas
import java.util.List;
import java.util.stream.Collectors;

public class StreamExample {
    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        List<Integer> evenSquares = numbers.stream()
            .filter(n -> n % 2 == 0)
            .map(n -> n * n)
            .collect(Collectors.toList());
        
        System.out.println(evenSquares); // [4, 16, 36, 64, 100]
        
        int sum = numbers.stream()
            .reduce(0, Integer::sum);
        System.out.println("Sum: " + sum); // 55
    }
}
```

```java
// Concurrency with ExecutorService
import java.util.concurrent.*;

public class ConcurrentExample {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " running on " 
                    + Thread.currentThread().getName());
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
    }
}
```

## Related Concepts

- [[JVM]] - The virtual machine that runs Java bytecode
- [[Garbage Collection]] - Automatic memory management in Java
- [[Spring Framework]] - Popular enterprise Java framework
- [[Kotlin]] - Modern JVM language interoperable with Java
- [[Bytecode]] - The intermediate representation Java compiles to
- [[Concurrency]] - Multi-threading and parallel processing in Java

## Further Reading

- "Effective Java" by Joshua Bloch
- "Java: The Complete Reference" by Herbert Schildt
- [Oracle Java Documentation](https://docs.oracle.com/javase/)

## Personal Notes

Java's longevity is remarkable. While syntax has evolved (lambdas, records, pattern matching), the core promise of platform independence and robust tooling remains. For large teams and long-lived projects, Java's maturity and vast ecosystem are significant advantages.
