---
title: Planner
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent, roles, multi-agent, planning, orchestration, coordination]
---

# Planner

## Overview

In multi-agent systems, a planner agent (also called orchestrator, coordinator, or supervisor) is a specialized agent responsible for breaking down complex tasks into subtasks and coordinating their execution across other agents. Rather than attempting to accomplish everything directly, a planner delegates to specialized agents—researchers, executors, critics—each optimized for specific aspects of the overall objective. This division of labor mirrors how human teams operate: a project manager plans and coordinates while specialists handle execution.

The planner pattern emerges naturally when addressing complex problems that require diverse capabilities. A research task might need web search, data analysis, and synthesis. A coding task might require architecture design, implementation, testing, and review. The planner provides the cognitive architecture for managing these dependencies, handling failures, and integrating partial results into coherent outcomes.

This role is fundamental to frameworks like AutoGen, LangChain's agent architecture, and custom multi-agent pipelines. Understanding planner design is essential for building robust agentic systems that scale beyond what a single agent can accomplish effectively.

## Key Concepts

### Role Specialization

Multi-agent systems divide labor through role specialization:

```python
# Conceptual multi-agent setup
class PlannerAgent:
    """Breaks down tasks and coordinates execution."""
    
    def __init__(self, agents):
        self.agents = agents  # Available specialized agents
        self.researcher = agents['researcher']
        self.executor = agents['executor']
        self.critic = agents['critic']
    
    def plan(self, task):
        # Decompose task into subtasks
        subtasks = self.decompose(task)
        
        # Assign to appropriate agents
        results = []
        for subtask in subtasks:
            agent = self.select_agent(subtask)
            result = agent.execute(subtask)
            results.append(result)
        
        # Synthesize into final response
        return self.synthesize(results)
```

### Task Decomposition

The planner's core responsibility is breaking complex objectives:

1. **Goal Analysis**: Understand the end objective and constraints
2. **Dependency Mapping**: Identify what subtasks depend on others
3. **Execution Ordering**: Determine optimal sequence considering dependencies
4. **Assignment**: Match subtasks to appropriate agents based on capabilities
5. **Result Integration**: Combine outputs into coherent whole

### Communication Protocols

Agents communicate through structured messages:

```python
# Message passing between agents
class AgentMessage:
    def __init__(self, sender, recipient, content, type):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.type = type  # 'request', 'response', 'status', 'error'

# Planner sends task to researcher
planner.send(AgentMessage(
    sender="planner",
    recipient="researcher",
    content="Find recent papers on RAG optimization techniques",
    type="request"
))
```

## How It Works

### Planning Loop

A typical planner operates in a loop:

```
┌─────────────────────────────────────────────┐
│ 1. RECEIVE: Get task from user or parent    │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 2. DECOMPOSE: Break into subtasks           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 3. ASSIGN: Delegate to specialized agents   │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│    │Research │  │ Execute │  │ Critique│   │
│    │ Agent   │  │  Agent  │  │  Agent  │   │
│    └────┬────┘  └────┬────┘  └────┬────┘   │
└─────────┼───────────┼───────────┼──────────┘
          │           │           │
┌─────────▼───────────▼───────────▼──────────┐
│ 4. COLLECT: Gather results from agents      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 5. SYNTHESIZE: Combine into final response  │
└─────────────────────────────────────────────┘
```

### Error Handling and Recovery

Planners typically implement fault tolerance:

- **Retry Logic**: Failed subtasks may be retried with different agents
- **Fallback Strategies**: If one approach fails, try alternative methods
- **Graceful Degradation**: Return partial results if complete solution isn't achievable
- **Escalation**: Surface persistent failures to human operators

## Practical Applications

### Code Generation Pipeline

```python
# Multi-agent code generation with planner
planner = PlannerAgent({
    'architect': ArchitectAgent(),
    'coder': CoderAgent(),
    'reviewer': ReviewerAgent(),
    'tester': TesterAgent()
})

task = """
Create a REST API for a todo application with:
- User authentication (JWT)
- CRUD operations for todos
- PostgreSQL database
- Docker deployment
"""

# Planner handles the orchestration
result = planner.execute(task)
# Architect designs schema and API
# Coder implements the code
# Reviewer checks for issues
# Tester validates functionality
```

### Research and Analysis

Planners excel at multi-step research:

1. **Researcher Agent**: Searches for relevant sources, papers, documentation
2. **Extractor Agent**: Pulls key facts, statistics, code snippets
3. **Synthesizer Agent**: Combines findings into coherent report
4. **Critic Agent**: Identifies gaps, questions assumptions, suggests improvements

## Related Concepts

- [[researcher]] — Researcher agent role details
- [[executor]] — Executor agent role for carrying out tasks
- [[critic]] — Critic agent for evaluation and feedback
- [[multi-agent-systems]] — Broader multi-agent architecture
- [[agent-roles]] — Agent role definitions and specializations
- [[task-decomposition]] — Breaking complex tasks into subtasks

## Further Reading

- [AutoGen Multi-Agent Framework](https://microsoft.github.io/autogen/)
- [LangChain Agent Architectures](https://python.langchain.com/docs/modules/agents/)
- [Multi-Agent Coordination Patterns](https://arxiv.org/abs/2308.10786)

## Personal Notes

The planner pattern transformed how I think about agentic systems. Early implementations tried to make single agents do everything—they became unwieldy prompt monsters. Splitting into specialized roles with a planner coordinator feels more maintainable and often produces better results. Key lesson: the planner needs to be smart about task decomposition. Bad decomposition leads to fragmented results or missed dependencies. Also consider planning depth—sometimes a two-level plan is sufficient; other times you need hierarchical planning with sub-planners.
