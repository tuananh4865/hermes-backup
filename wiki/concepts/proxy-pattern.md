---
title: "Proxy Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, structural-patterns, software-architecture, object-oriented, access-control]
---

# Proxy Pattern

## Overview

The Proxy Pattern is a structural design pattern that provides a surrogate or placeholder object that controls access to another object. The proxy sits between the client and the real subject, intercepting requests and deciding whether to pass them through, modify them, or reject them entirely. This intermediary role enables many useful patterns: lazy initialization, access control, logging, caching, and remote service representation.

The key insight is that clients interact with the proxy as if it were the real object—they use the same interface. This transparency allows the proxy to be inserted into any place where the real subject could be used, without changing client code. The proxy simply delegates calls to the real object, potentially adding behavior before or after the delegation.

Proxies are everywhere in software development, even when we don't call them by that name. A database connection pool is a proxy for database connections. A CDN is a proxy for origin servers. Authentication middleware is a proxy for API endpoints. Understanding the proxy pattern helps you recognize these patterns in existing systems and design better systems yourself.

## Key Concepts

**Subject** is the common interface that both the real object and proxy implement. This interface defines the methods that clients use, ensuring the proxy can be substituted for the real object transparently.

**RealSubject** is the actual object that the proxy represents. It contains the core business logic and does the "real work" that clients ultimately want to perform. The real subject might be expensive to create, located remotely, or require special access.

**Proxy** implements the same interface as the RealSubject and maintains a reference to it. The proxy adds its own logic before or after delegating to the real subject. Common proxy responsibilities include:
- **Lazy initialization**: Creating the real object only when first needed
- **Access control**: Checking permissions before allowing requests
- **Logging**: Recording method calls and their parameters
- **Caching**: Storing results that can be reused
- **Remote proxy**: Representing an object located on a different server

**Client** uses the Subject interface and is unaware whether it's working with a real object or a proxy. This lack of awareness is intentional and enables transparent substitution.

## How It Works

The proxy pattern works through interface consistency and delegated execution:

1. The client holds a reference to the Subject interface, not the concrete RealSubject
2. At runtime, either a RealSubject or Proxy is injected, depending on configuration
3. Client calls methods on the proxy using the Subject interface
4. Proxy intercepts the call, applies its additional logic, then delegates to the RealSubject
5. Results flow back through the proxy to the client

The proxy can act at various points in the request lifecycle:
- **Before delegation**: Validate inputs, check permissions, log the request
- **Instead of delegation**: Return cached results, reject unauthorized requests
- **After delegation**: Transform results, log responses, update cache

This flexibility makes proxies incredibly versatile. A single proxy might combine multiple responsibilities—lazy loading, access control, and caching—while presenting the same interface as the real object.

## Practical Applications

Proxies appear across many domains and technologies:

**Lazy Loading** - Object-relational mappers (ORMs) use proxies to defer loading related objects from the database until they're actually accessed. This avoids loading entire object graphs when only a small piece is needed.

**Access Control** - Proxies enforce authorization rules, ensuring users can only access resources they're permitted to. The proxy checks credentials before forwarding requests to protected resources.

**Remote Procedure Call (RPC)** - Client-side stubs are proxies that serialize requests, send them over the network to a server, wait for responses, and deserialize the results. Clients interact with these stubs as if they were local objects.

**Caching** - HTTP cache proxies store responses and return them for identical subsequent requests, reducing latency and server load.

**Logging and Monitoring** - Service meshes use proxies (like Envoy or Linkerd) to collect metrics, trace requests, and log traffic without modifying application code.

**Virtual Proxies** - Placeholder images in web applications that show a low-resolution placeholder until the full image loads.

## Examples

```python
from abc import ABC, abstractmethod

# Subject interface
class Image(ABC):
    @abstractmethod
    def display(self):
        pass

# RealSubject - expensive to create
class RealImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self):
        print(f"Loading high-resolution image: {self._filename}")
        # Simulate expensive operation
        import time
        time.sleep(1)
    
    def display(self):
        print(f"Displaying image: {self._filename}")

# Proxy - lazy loading
class ImageProxy(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._real_image = None
    
    def display(self):
        # Lazy initialization - only create real object when needed
        if self._real_image is None:
            print("Proxy: Creating RealImage on first access")
            self._real_image = RealImage(self._filename)
        self._real_image.display()

# Proxy with access control
class SecuredImageProxy(Image):
    def __init__(self, filename: str, user_level: int):
        self._filename = filename
        self._user_level = user_level
        self._real_image = None
    
    def display(self):
        if self._user_level < 5:
            print(f"Access denied: User level {self._user_level} cannot view {self._filename}")
            return
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        self._real_image.display()

# Usage
print("=== Lazy Loading Proxy ===")
image1 = ImageProxy("photo1.jpg")
image2 = ImageProxy("photo2.jpg")

print("Proxy created, but RealImage not loaded yet")
image1.display()  # Loads here
image1.display()  # Uses cached instance

print("\n=== Access Control Proxy ===")
secure = SecuredImageProxy("secret.jpg", user_level=3)
secure.display()  # Access denied

secure2 = SecuredImageProxy("secret.jpg", user_level=7)
secure2.display()  # Access granted
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Decorator Pattern]] - Similar structure but different purpose (adding behavior) versus proxy (controlling access)
- [[Adapter Pattern]] - Changes interface, while proxy preserves the same interface
- [[Facade Pattern]] - Simplified interface to a subsystem, not controlling a single object
- [[Remote Method Invocation]] - Uses proxies to represent remote objects locally

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Effective Java" by Joshua Bloch - discusses proxy usage in Java
- Microsoft .NET RealProxy documentation

## Personal Notes

The proxy and decorator patterns feel similar in structure but diverge in intent. A decorator adds behavior; a proxy controls access. The question I ask is: "Is this fundamentally the same object or a different one pretending to be the same?" If it's the same object but enhanced, it's decorator. If it's substituting for the real thing, it's proxy. This distinction matters for documentation and communication—if someone says "proxy," I expect access control or lazy initialization; if they say "decorator," I expect behavior augmentation.
