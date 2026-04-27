---
confidence: low
last_verified: 2026-04-10
relationships:
  - ❓ hermes-agent (ambiguous)
  - ❓ autonomous-wiki-agent (ambiguous)
  - ❓ agentic-graphs (ambiguous)
  - ❓ acpx (ambiguous)
relationship_count: 4
---

# Agentic Workflows — Agentic Graphs

**Author:** Onur Solmaz (creator of acpx)  
**Source:** X/Twitter Post  
**Date:** April 10, 2026  
**URL:** https://x.com/onusoz/status/2038565725690900992

---

## Post Content

acpx v0.4 ships Agentic Workflows, or as I like to call them **"Agentic Graphs"**

It let's you create **node-based workflows** on top of ACP (Agent Client Protocol), to drive any coding agent (Codex, Claude Code, pi) through **deterministic steps**. This lets you automate routine, mechanical legwork like triaging incoming PRs, bugs in error reporting, and so on...

## PR Triage Example

OpenClaw receives **300~500 new PRs per day**. A lot of them are low quality, but they still relate to real issues, so you have to address them somehow.

You need to:
1. Extract the intent
2. Cluster them based on intent
3. Figure out if proposed changes are legit, or whether they are slop
4. If PR is too low quality or intent unclear → close them
5. Run AI review and address any issues
6. Refactor if changes are half-baked
7. Resolve conflicts
8. And so on...

**Result:** When PR reaches maintainer, all routine legwork is done. Only decisions remain:
- (a) merge
- (b) give feedback to PR author
- (c) take over the PR work yourself

## Key Insights

### Why Not a Single Prompt?

> "I claim that putting all steps in the same prompt at the beginning of the context will generally give **suboptimal results**, compared to **revealing the intention to the model step by step**"

**LLMs are prone to PRIMING.** Like humans, if you give them all steps upfront, they get biased/confused.

### Benefits of Step-by-Step Workflow

1. **OBSERVABILITY** — Each step generates JSON, easy to monitor thousands of agents on a dashboard
2. **Better Quality** — Model focuses on one step at a time
3. **Deterministic** — Repeatable, auditable

### Similar Tools

- n8n, langflow have similar features
- But they're not integrating ACP
- acpx built a fresh API approach

## Workflow Tuning Process

1. Start from a **Markdown file with Mermaid chart** of the flow
2. The Markdown file acts as a **spec for the flow**
3. Build workflow through **trial and error**
4. Tune the flow one by one, slowly scaling to more PRs
5. When confident, run in **parallel** over all PRs

## Results

> "I believe it already **saved me hours this week**"

Next goal: Set up on cloud agent to process 300~500 PRs/day in real time.

---

## Key Takeaways

1. **Node-based workflows > single prompt** — Avoids LLM priming
2. **Deterministic steps** — Each step produces structured JSON
3. **Observability** — Easy to monitor thousands of agents
4. **Workflow as code** — Markdown/Mermaid spec → TypeScript API
5. **Incremental tuning** — Start small, scale gradually
6. **ACP (Agent Client Protocol)** — Standard protocol for driving coding agents

## Related Concepts

- [[hermes-agent]] — Hermes uses ACP-like protocol
- [[autonomous-wiki-agent]] — Our autonomous agent implementation
- [[agentic-graphs]] — Node-based agent workflow patterns
- [[acpx]] — Agent Client Protocol extensions
