---
title: "Executor"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent, roles, multi-agent, task-execution, automation]
---

# Executor

In multi-agent systems, an executor is a specialized agent responsible for carrying out tasks assigned by other agents—typically planners, coordinators, or orchestrators. The executor takes high-level directives and converts them into concrete actions, returning results for further processing or synthesis.

## Overview

Modern AI systems increasingly use multiple specialized agents working together rather than a single monolithic agent. This multi-agent architecture mirrors human organizations where different roles (planner, executor, reviewer) collaborate to achieve complex goals.

The executor role emerged from the recognition that planning and execution have different requirements. A planner agent might excel at reasoning about goals, breaking down complex objectives, and generating task sequences, but be inefficient at the actual work of running commands, calling APIs, or manipulating files. An executor agent focuses on reliable, efficient task completion with appropriate error handling and retry logic.

This separation of concerns enables specialization. Executors are optimized for throughput and reliability on specific task types (shell commands, code execution, API calls), while planners are optimized for reasoning about what tasks to perform.

## Key Responsibilities

**Task Execution**: The core function—taking a defined task and completing it. Tasks arrive with varying specificity: from "run this exact shell command" to "find and fix the bug in module X."

**Tool Operation**: Executors typically have access to a set of tools (bash, Python interpreter, file operations, HTTP clients) they can invoke to accomplish tasks. Managing tool execution, handling timeouts, and processing outputs is central to the role.

**Error Handling and Recovery**: When a tool call fails, executors must decide whether to retry, try an alternative approach, or propagate the failure. This requires understanding which errors are transient (network timeout → retry) versus fatal (invalid input → report failure).

**Progress Reporting**: Executors communicate their status back to the calling agent—started, in progress with partial results, completed, or failed. This allows orchestrators to track long-running tasks and aggregate results.

**Result Formatting**: Raw tool outputs (exit codes, stdout/stderr, HTTP response bodies) are often reformatted into structured results the orchestrator can process programmatically.

## Architecture Patterns

**Pipeline Pattern**: Tasks flow through a linear sequence of specialized executors, each handling a specific stage. Output from one executor feeds into the next.

```
Planner → Executor1 → Executor2 → Executor3 → Synthesizer
```

**Fan-Out/Fan-In**: A task is split across multiple executors working in parallel, then results are aggregated. Useful for parallel data processing or testing multiple branches simultaneously.

```
         ┌─ Executor A ─┐
Planner ─┼─ Executor B ─┤→ Aggregator
         └─ Executor C ─┘
```

**Hierarchical**: Higher-level executors decompose tasks and delegate to lower-level executors, forming a tree. The top-level executor handles coordination; leaf executors perform atomic operations.

**Observer Pattern**: An executor operates alongside other agents that monitor its work, providing checkpoints, validation, or intervention points.

## Implementation in Agent Frameworks

In the Hermes multi-agent framework, the executor role is implemented as a [[subagent]] with specific capabilities:

```python
class Executor(Subagent):
    """Agent specialized in task execution."""
    
    def __init__(self, tools: List[Tool], config: ExecutorConfig):
        super().__init__(role="executor", tools=tools)
        self.max_retries = config.max_retries
        self.timeout = config.default_timeout
    
    async def execute(self, task: Task) -> ExecutionResult:
        """Execute a single task with retry logic."""
        for attempt in range(self.max_retries):
            try:
                result = await asyncio.wait_for(
                    self._run_task(task),
                    timeout=self.timeout
                )
                return ExecutionResult(status="success", result=result)
            except RetryableError as e:
                await self._backoff(attempt)
                continue
            except FatalError as e:
                return ExecutionResult(status="failed", error=str(e))
        
        return ExecutionResult(status="exhausted", error="Max retries exceeded")
```

## Executor vs. Related Roles

**Executor vs. Planner**: The planner reasons about what to do; the executor does it. Planners work with abstractions and task graphs; executors work with concrete actions and tools.

**Executor vs. Researcher**: Researchers gather information through queries, searches, and document analysis. Their output is findings. Executors take actions that change system state—running code, creating files, calling APIs.

**Executor vs. Critic**: Critics evaluate outputs (code quality, reasoning steps, factual accuracy). Executors produce the outputs being evaluated.

**Executor vs. Orchestrator**: Orchestrators manage workflow across multiple agents, deciding which agents handle which tasks and when. Executors are one type of agent that orchestrators may invoke.

## Error Handling Strategies

Executors must handle failures gracefully. Common strategies:

**Retry with Backoff**: Transient failures (network timeouts, rate limits) are retried with exponential backoff to avoid overwhelming services.

**Fallback Execution**: If primary execution fails, attempt alternative approaches. If `curl` fails, try `wget`; if API v1 fails, try API v2.

**Graceful Degradation**: When full execution isn't possible, return partial results with clear indication of what couldn't be completed.

**Circuit Breaking**: If a remote service is failing repeatedly, stop attempting for a cooldown period to allow the service to recover.

## Practical Applications

Executor agents appear in:

- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Data Processing**: ETL jobs where tasks are decomposed and distributed
- **Research Automation**: Parallel literature review, data collection, and synthesis
- **DevOps Automation**: Infrastructure provisioning, deployment, and monitoring

## Related Concepts

- [[Planner Agent]] - Agent role focused on task decomposition and planning
- [[Researcher Agent]] - Agent role focused on information gathering
- [[Multi-Agent Systems]] - Architecture where executors operate
- [[Task Queue]] - Mechanism for distributing work to executors
- [[Tool Use]] - How executors interact with external systems
- [[Agent Roles]] - Overview of specialized agent roles

## Further Reading

- "Building Effective Agents" - Anthropic's guide to multi-agent design
- Hermes Agent Framework documentation on agent roles
- "Programming Distributed AI Agents" literature

## Personal Notes

The executor role is deceptively simple—looks like "just run the commands." But designing a reliable executor requires careful attention to error handling, timeout management, and resource cleanup. I've seen executor implementations that work perfectly until the first network hiccup, then hang indefinitely. The backoff and circuit-breaking patterns are essential for production systems. Also worth noting: executors need good observability. When a task fails, the orchestrator needs enough context to understand what happened and decide whether to retry, skip, or escalate.
