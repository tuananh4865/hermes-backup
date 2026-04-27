---
title: Agent Client Protocol (ACP)
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ai-agents, protocol, communication, acp]
---

## Overview

The Agent Client Protocol (ACP) is a standardized communication protocol designed to enable AI agents to interact seamlessly with any client application or development environment that supports it. By establishing a common language for agent-client exchanges, ACP prevents vendor lock-in and empowers developers to combine best-in-class AI capabilities with their preferred tools. The protocol serves as a foundational layer for node-based agentic workflows, facilitating structured communication between the various components of an AI-powered system.

ACP addresses one of the most significant challenges in modern AI-assisted software development: the fragmentation of tooling. As AI coding assistants become increasingly sophisticated, users have found themselves tied to specific platforms or editors, limiting their flexibility and choice. ACP breaks down these barriers by defining a universal interface that any compliant client or agent can implement. This standardization benefits the entire ecosystem, encouraging competition, innovation, and interoperability among AI tools.

The protocol has gained significant traction in the developer community, with major AI coding tools including Codex, Claude Code, and Goose officially adopting it as their communication standard. This broad adoption indicates industry recognition that open protocols benefit everyone involved, from individual developers to large enterprises building complex AI systems.

## Core Concepts

### Protocol Architecture

ACP operates on a request-response model layered over JSON-based message formatting. At its core, the protocol defines a set of message types that structure the interaction between an AI agent and its client. These messages cover task assignment, status updates, context sharing, result delivery, and error handling. The architecture is designed to be lightweight yet expressive, allowing for simple integrations while supporting complex multi-step workflows.

The protocol organizes communication into discrete channels, each serving a specific purpose in the agent-client relationship. Task channels carry work assignments and their results, while context channels maintain shared state and memory across interactions. This separation of concerns allows developers to reason about their agent workflows more clearly and enables sophisticated tooling around the protocol itself.

### Agent Abstraction

A fundamental concept in ACP is the clear separation between the agent's reasoning capabilities and its communication interface. The agent itself handles planning, reasoning, and action execution, while ACP provides the standardized vocabulary for expressing intentions and exchanging information with external systems. This abstraction means agents can be developed and improved independently from the specific clients they interface with, and vice versa.

Agents participating in ACP expose a capability manifest that describes their supported features, tool integrations, and operational constraints. Clients can query this manifest to understand what an agent offers and configure their interactions accordingly. This discoverability mechanism supports dynamic agent selection and composition in more advanced workflows.

### Node-Based Workflows

ACP provides the foundation for node-based agentic workflows, a paradigm where complex tasks are decomposed into interconnected processing nodes. Each node represents a discrete unit of work, whether performed by an AI agent, a human collaborator, or an automated system. ACP standardizes how these nodes communicate, share context, and coordinate their activities.

In this model, information flows through the network of nodes according to defined routing rules and transformation logic. The protocol handles message delivery, ensures ordering guarantees where needed, and supports both synchronous and asynchronous interaction patterns. This flexibility makes ACP suitable for everything from simple request-response scenarios to elaborate multi-agent pipelines spanning dozens of interconnected components.

### Client Integration

Client applications that implement ACP gain the ability to connect with any compliant agent without custom integration work. The protocol supports integration with modern code editors including Zed, Visual Studio Code, and JetBrains IDEs, making AI assistance accessible within familiar development environments. This broad editor compatibility ensures developers can adopt AI tools without changing their established workflows.

The client side of ACP is intentionally minimal, requiring only a protocol implementation rather than a full agent runtime. This design allows lightweight clients, remote interfaces, and specialized tooling to participate in agent workflows without unnecessary overhead. Clients can focus on their specific use case while relying on the protocol to handle the complexities of agent communication.

## Use Cases

### AI-Assisted Software Development

The primary application of ACP is enabling AI-assisted software development across diverse toolchains. When a developer writes code in their preferred editor, ACP allows an AI agent to provide context-aware suggestions, review changes, run tests, or refactor code segments. The agent can access project files, understand the broader codebase context, and take action through standardized interfaces—all without requiring the editor to understand the internals of the agent's operation.

This integration extends beyond simple code completion. ACP-powered workflows can automate entire development processes, from generating initial scaffolding based on requirements to running comprehensive test suites and deployment checks. Development teams can define custom workflows that match their processes, with AI agents handling routine tasks while humans focus on architectural decisions and creative problem-solving.

### Multi-Agent Collaboration

Complex tasks often benefit from multiple specialized agents working together. ACP facilitates multi-agent scenarios by providing a shared protocol that agents use to delegate work, share findings, and coordinate actions. One agent might handle initial research while a second performs implementation, with a third validating results against requirements. ACP ensures these agents communicate effectively despite potentially different underlying technologies.

In enterprise settings, multi-agent workflows can orchestrate activities across organizational boundaries. Agents from different teams or departments communicate through ACP to manage dependencies, resolve conflicts, and maintain coherent progress toward shared objectives. The protocol's standardized message formats make it possible to introduce new agents into existing workflows without disrupting the overall coordination structure.

### Tool Abstraction and Integration

Organizations frequently work with multiple AI providers simultaneously, whether for cost optimization, redundancy, or access to specialized capabilities. ACP enables a unified interface that abstracts away the differences between AI providers, allowing clients to switch between agents or use multiple agents in concert without code changes. This abstraction protects investments in workflow automation and prevents disruption when provider landscapes evolve.

The protocol also simplifies integration with external systems and services. ACP defines conventions for tool calling, resource access, and result processing that map cleanly onto REST APIs, databases, message queues, and other infrastructure components. Agents can thus serve as intelligent intermediaries, translating between natural language requests and structured system operations.

### Research and Experimentation

AI researchers and practitioners use ACP to build reproducible experimental setups. By standardizing how agents interact with their environment and report results, ACP makes it easier to compare agent behaviors, replicate findings, and build upon prior work. The protocol's clear semantics support rigorous evaluation methodologies and enable automated testing of agent capabilities.

Educational institutions and training programs benefit similarly from ACP's clarity and consistency. Students learning about AI agents can focus on high-level concepts without getting bogged down in implementation-specific details. The protocol provides a common vocabulary that facilitates discussion, collaboration, and the sharing of resources across different tools and platforms.

## Related

- [[Agent Frameworks]] - Development frameworks for building and deploying AI agents
- [[AI Code Assistants]] - AI-powered tools that assist with programming tasks
- [[Software Development Lifecycle]] - The process of software creation from conception to deployment
- [[API Design Patterns]] - Established patterns for designing robust programmatic interfaces
- [[Large Language Models]] - The foundational technology enabling modern AI agent reasoning
- [[Tool Use]] - How AI agents interact with external systems and APIs to extend their capabilities
