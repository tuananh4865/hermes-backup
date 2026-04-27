---
title: "Harrison Chase — Your Harness, Your Memory"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [auto-filled]
---


---
title: Harrison Chase — Your Harness, Your Memory
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [agent, memory, harness, blog-post]
---

# Harrison Chase — Your Harness, Your Memory

## Summary
Harrison Chase argues that agent harnesses are now the dominant method for building agents, but memory ownership is essential. However, closed harnesses have lost control over long-term context, while model providers are creating lock-in through memory retention mechanisms.

## Key Insights
1. Harnesses act as the foundational layer for memory, but closed implementations like Claude Agent SDKs result in complete loss of user control over long-term context.
2. Model providers are utilizing memory to create proprietary datasets and lock-in, even when they don't control the underlying storage infrastructure.
3. The current MVP often lacks long-term memory, meaning users cannot build a data flywheel until the foundational harness architecture is established.

## Analysis
The article highlights that while agents are dominated by harnesses, the mechanics of memory management have shifted significantly. First, it reveals that most stateful APIs—such as Anthropic's server-side compaction—are internal tools orchestrated by the harness, meaning memory is technically managed by LangChain rather than directly by the model. This creates a paradox: while models are transparent, memory components often remain opaque to users, preventing them from understanding or switching. The text emphasizes that transitioning from stateless models to stateful ones is difficult because memory becomes a barrier rather than an enabler, reinforcing the need for open architectures. Furthermore, by aligning memory with user preferences and interactions, harnesses are establishing a data landscape that creates value beyond basic functionality. Ultimately, the goal is to move away from third-party locks toward a transparent system where users can define their own memory context, turning memory into a competitive advantage over time.

## Related
- [[karpathy-llm-wiki-architecture]] — Wiki-based memory = open, owned memory
- [[agentic-graphs-workflows]]
- [[ai-agent-trends-2026-04-12]]
- [[ai-agent-infrastructure-2026]]