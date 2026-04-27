---
title: ACPX
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ai-agents, protocol, acp, tooling]
---

# ACPX (Agent Client Protocol Extensions)

## Overview

ACPX stands for Agent Client Protocol Extensions, a protocol specification designed to extend and enhance the way AI agents communicate, coordinate, and collaborate with one another. While the foundational Agent Client Protocol (ACP) establishes the baseline mechanisms for agent-to-client and agent-to-agent interactions, ACPX builds upon this foundation to enable richer, more sophisticated forms of communication that support complex multi-agent workflows, advanced state management, and nuanced coordination patterns.

The need for ACPX arises from the limitations of basic request-response interaction models. As AI agents become more capable and are deployed in increasingly complex scenarios, simple message passing is often insufficient for expressing the full range of agent behaviors, intentions, and state transitions that modern agentic systems require. ACPX addresses this gap by introducing an extended message taxonomy, structured negotiation protocols, and enhanced context sharing mechanisms that allow agents to engage in more meaningful and productive collaborations.

ACPX is particularly relevant in environments where multiple agents operate concurrently, whether in cooperative problem-solving scenarios, hierarchical command structures, or competitive optimization contexts. By providing a standardized framework for these extended interactions, ACPX helps ensure that agents from different developers or platforms can interoperate effectively, reducing fragmentation in the agent ecosystem and enabling more seamless integration between agentic systems.

## Key Features

ACPX introduces several important capabilities that distinguish it from basic agent communication protocols.

**Extended Message Types**: Beyond simple text or指令 payloads, ACPX supports rich message types including declarative state updates, conditional commitments, hierarchical goals, and annotated reasoning traces. This allows agents to communicate not just what they are doing, but why, and what they intend to do next.

**Coordination Protocols**: ACPX includes built-in support for common coordination patterns such as request-acknowledge-commitConfirm sequences, enabling agents to establish reliable contracts for action rather than relying on best-effort message passing alone.

**Context Propagation**: Agents operating in ACPX environments can share and synchronize context windows, allowing information discovered by one agent to immediately benefit others working on related tasks without explicit copying or summarization.

**Structured Negotiation**: When agents have conflicting goals or need to allocate shared resources, ACPX provides negotiation frameworks that allow agents to reach mutually beneficial agreements through a defined process rather than ad-hoc bargaining.

**Capability Discovery**: ACPX includes mechanisms for agents to advertise their capabilities, tools, and limitations, enabling dynamic task allocation and routing based on actual availability rather than hard-coded assumptions.

## How It Extends ACP

The relationship between ACP and ACPX can be understood as a layered architecture where ACP provides the foundational transport and message envelope, while ACPX adds semantic richness on top.

In the base ACP model, agents communicate through a relatively simple interface: send a message, receive a response. This is sufficient for straightforward task execution but breaks down when agents need to maintain shared state, coordinate on long-running processes, or handle failures gracefully. ACPX addresses these gaps by adding extension fields to standard ACP messages, introducing new message types for specific coordination needs, and defining state machines that govern how agent relationships evolve over time.

Where ACP treats each interaction as independent, ACPX introduces the concept of sessions—persistent connections between agents that carry forward context, track commitments, and enable recovery from interruptions. This session model is particularly valuable for agents engaged in multi-step workflows where intermediate results must be preserved and referenced across multiple exchanges.

ACPX also extends ACP's error handling capabilities. Rather than treating errors as simple failure notifications, ACPX defines structured error categories that allow receiving agents to understand the nature of a problem and respond appropriately—whether by retrying, escalating, or adjusting their own behavior to work around the issue.

## Related

- [[agentic-graphs]] - Graph-based representations of agent relationships and dependencies
- [[agentic-workflows-agentic-graphs]] - Workflow patterns that leverage graph structures for agent coordination
- [[llm-agents]] - Large language model-powered agents that often utilize protocols like ACPX for communication
- [[communication]] - The broader study of how agents and systems exchange information
- [[tool-use]] - How agents interact with external tools and systems, often coordinated through communication protocols
