---
title: Agent Frameworks
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [agent-frameworks, langgraph, crewai, autogen]
---

# Agent Frameworks

## Overview

Agent frameworks are software libraries and platforms that provide abstractions for building autonomous AI agents — systems capable of planning, using tools, maintaining memory, and executing tasks with minimal human intervention. Unlike simple large language model (LLM) API calls, agents built on these frameworks can break down complex goals into steps, iterate on their approach, and interact with external systems through tools and APIs.

The core capabilities that agent frameworks provide include planning (decomposing goals into actionable steps), tool use (calling external APIs, reading files, executing code), memory (tracking state and context across interactions), and orchestration (managing multi-agent collaboration and complex workflows). These frameworks abstract away the boilerplate of building such systems, allowing developers to focus on defining agent behavior and logic rather than reinventing infrastructure.

The agent framework landscape in 2026 is defined by several key shifts. First, multi-agent-native design has become the default — most new frameworks assume you'll be building systems with multiple interacting agents from day one. Second, supervisor and hierarchical patterns have replaced flat agent teams as the dominant orchestration approach, with a supervising agent delegating to specialist sub-agents. Third, the Model Context Protocol (MCP) has emerged as the standard for tool integration, enabling agents to discover and use tools across different frameworks with a unified interface.

## Key Frameworks

### LangGraph

LangGraph is a graph-based framework from the LangChain ecosystem designed for building complex agents and multi-agent systems. Its defining characteristic is native support for cyclic graphs — agents can loop back on themselves, enabling reflection and self-correction patterns that linear frameworks cannot express. This makes LangGraph particularly powerful for tasks requiring iterative refinement.

In version 0.3 and later, LangGraph offers a Checkpointing API for built-in state persistence across sessions, a new LangGraph SDK with cleaner primitives, stable supervisor pattern support for hierarchical agent orchestration, improved multi-agent messaging via shared StateGraph with message passing, first-class streaming across all node types, and LangGraph Studio for web-based visualization and debugging.

LangGraph integrates deeply with the LangChain ecosystem, giving access to over 400 pre-built tools. Its primary trade-off is a steeper learning curve compared to more opinionated frameworks, and it can be verbose for simple tasks due to the flexibility of its graph-based approach.

### CrewAI

CrewAI takes a role-based approach to agent design, defining agents with specific roles (like "Researcher" or "Writer") that collaborate to complete tasks. This natural division of labor makes CrewAI especially well-suited for research pipelines, content creation workflows, and business automation where different specialists need to contribute their expertise in a coordinated manner.

Version 0.40 and later brings persistent memory via shared crew-level memory, a stable hierarchical process mode for supervisor-style coordination, a callback system for observability at task and agent levels, cleaner decorator-based tool registration, CrewAI Studio for visual workflow design, and automatic context window optimization through summarization of long contexts.

CrewAI's strengths include its intuitive design, rapid prototyping capability, and active development with frequent releases. Its limitations include less flexibility for complex branching logic compared to LangGraph, and newer memory features that are less battle-tested than LangGraph's checkpointing.

### Microsoft AutoGen

AutoGen, developed by Microsoft Research, centers on multi-agent conversations where agents chat with each other to collaborate. The framework excels at conversational workflows, code generation tasks, and scenarios requiring human-in-the-loop involvement. AutoGen 0.4 and later features a production-grade AutoGen Studio GUI, a unified agent abstraction replacing the older AssistantAgent and UserProxyAgent classes, Docker-based sandboxed code execution for secure code running, first-class streaming support, improved group chat with better speaker selection, and direct OpenAI-compatible API support.

AutoGen's strengths include Microsoft backing, robust code execution capabilities validated on SWE-bench benchmarks, flexible conversation patterns, and strong human-in-the-loop features. Its limitations include complex setup for simple tasks, less mature memory management compared to LangGraph, and group chat implementations that can become noisy with many agents.

### LlamaIndex

LlamaIndex is purpose-built for agents that need to retrieve and reason over knowledge bases. While primarily known as a retrieval-augmented generation (RAG) framework, LlamaIndex has expanded into a full agent platform with the AgentWorkflow system supporting ReAct, Plan-and-Execute, and Reasoning agent patterns. It offers first-class function calling with tool retry and fallback, an AgentRouter for routing queries to specialized sub-agents, a visual query pipeline builder, and LlamaCloud for managed index hosting.

LlamaIndex is the go-to choice when knowledge RAG is the primary use case, particularly for document question-answering over private data.

### Mastra

Mastra is a TypeScript-first agent framework that has emerged as the strongest option for TypeScript developers building production agents. It offers native TypeScript support, excellent developer experience, built-in observability, and production-ready patterns. Mastra is ideal for teams already in the JavaScript/TypeScript ecosystem who want to build agents without switching to Python.

### Flowise and n8n AI

Flowise provides a low-code visual drag-and-drop interface for building LangChain JS workflows, making it accessible to non-technical users who want to prototype agent workflows without writing code. n8n's AI nodes support multi-agent orchestration integrated with over 400 application integrations, positioning it as the best choice when connecting AI agents to existing automation workflows is the primary goal.

## Comparison

When comparing agent frameworks, several dimensions matter for decision-making. LangGraph offers the highest flexibility with cyclic graph support and built-in checkpointing, making it the strongest choice for complex multi-step workflows requiring reflection loops. CrewAI prioritizes rapid prototyping with intuitive role-based agent design. AutoGen excels at conversational and code generation tasks with robust Docker-based code execution. LlamaIndex dominates for knowledge-intensive RAG applications. Mastra serves TypeScript teams, while Flowise and n8n serve low-code and integration-focused use cases.

| Framework | Language | Primary Use Case | Complexity | Production Ready | Multi-Agent | Memory | Code Execution |
|-----------|----------|------------------|------------|-----------------|-------------|--------|----------------|
| LangGraph | Python | Complex workflows, supervisor patterns | High | Yes | Supervisor | Checkpointing | External |
| CrewAI | Python | Team collaboration, business automation | Low | Yes | Hierarchical | v0.40+ | Via LangChain |
| AutoGen | Python | Code generation, conversations | Medium | Yes | Group chat | Basic | Docker |
| LlamaIndex | Python | Knowledge RAG | Medium | Yes | AgentRouter | Index-based | External |
| Mastra | TypeScript | TypeScript production agents | Medium | Yes | Yes | Built-in | External |
| Flowise | JS/TS | Low-code visual | Low | Partial | Partial | Partial | Partial |

## When to Use

Choose LangGraph when you need supervisor or hierarchical agent patterns, complex branching with reflection loops requiring agents to self-correct, production-grade deployments with checkpointing for long-running tasks, or when you're already invested in the LangChain ecosystem with its 400+ tools.

Choose CrewAI for rapid prototyping of multi-agent systems with clear role separation, business automation pipelines involving research, writing, and analysis, teams wanting visual workflow design through CrewAI Studio, or when you want the fastest path from concept to working agent system.

Choose AutoGen for code generation and software engineering benchmark tasks, conversational multi-agent debugging workflows, human-in-the-loop scenarios where humans need to approve or guide agent actions, or when operating within the Microsoft ecosystem with tight Azure OpenAI integration.

Choose LlamaIndex when knowledge retrieval and question-answering over private documents is the primary requirement, when you already use LlamaIndex for indexing and want to add agentic capabilities, or for research synthesis pipelines that need to pull from large document collections.

Choose Mastra for TypeScript-first development teams, production JavaScript/TypeScript agents requiring excellent developer experience, or when you want native TypeScript types and patterns throughout your agent code.

Choose Flowise or n8n when your team includes non-technical members who need to design agent workflows visually, when integrating AI agents with existing automation and workflow tools is more important than custom agent logic, or when you need rapid prototyping without writing code.

## Related

- [[coding-agents]] — AI agents specialized in writing and debugging code, often built on these frameworks
- [[multi-agent-systems]] — Deep dive on patterns for coordinating multiple agents together
- [[llamaindex]] — Framework for building knowledge-augmented agents with RAG capabilities
- [[mastra]] — TypeScript-first agent framework alternative
- [[flowise]] — Low-code visual agent builder
- [[n8n-ai]] — Workflow automation platform with AI agent nodes
- [[mcp]] — Model Context Protocol, emerging as the standard for tool integration across frameworks
- [[rag]] — Retrieval-augmented generation, the foundation of LlamaIndex's approach
