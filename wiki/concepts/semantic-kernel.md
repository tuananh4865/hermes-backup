---
title: "Microsoft Semantic Kernel"
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [microsoft, ai-sdk, python, dotnet, agent-framework, orchestrator]
related:
  - [[microsoft-autogen]]
  - [[multi-agent-systems]]
  - [[agent-orchestrator]]
  - [[mcp-model-context-protocol]]
  - [[langgraph]]
  - [[openai-agents-sdk]]
sources:
  - https://github.com/microsoft/semantic-kernel
  - https://learn.microsoft.com/en-us/semantic-kernel/overview/
  - https://www.digitalapplied.com/blog/microsoft-agent-framework-1-0-dotnet-python-guide
---

# Microsoft Semantic Kernel

Microsoft Semantic Kernel is an AI SDK for building applications that combine **LLMs with existing code** (C# and Python). Semantic Kernel provides the "glue" between AI capabilities and your business logic — enabling function calling, memory, planning, and agent orchestration.

> **2026 Update:** Semantic Kernel has been merged into **Microsoft Agent Framework 1.0** (GA April 2026), which unifies Semantic Kernel with AutoGen into a single SDK for .NET and Python.

## Core Abstractions

Semantic Kernel is built around three core concepts:

### 1. Kernel
The container that holds everything — LLM configs, plugins, and memories.

```python
# Python
from semantic_kernel import Kernel

kernel = Kernel()
kernel.add_service("openai", AzureOpenAI(config={...}))
kernel.add_plugin(MyPlugin())
```

```csharp
// C#
var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(...);
var kernel = builder.Build();
```

### 2. Plugins (Previously "Skills")
Reusable components that expose functions to the LLM.

```python
# Define a plugin
class MathPlugin:
    @kernel_function(description="Add two numbers")
    def add(self, input: str) -> str:
        a, b = map(float, input.split(","))
        return str(a + b)

kernel.add_plugin(MathPlugin(), plugin_name="math")
```

### 3. Prompts (Templates)
LLM prompts with input variables and rendering.

```python
from semantic_kernel import Kernel

prompt = kernel.add_function(
    function_name="joke",
    plugin_name="fun",
    prompt_template="""
Tell a joke about {{$topic}}.
Include exactly {{$num_jokes}} jokes.
"""
)

result = await kernel.invoke(prompt, topic="programmers", num_jokes=2)
```

## Function Calling / Tool Use

Semantic Kernel excels at connecting LLMs to real tools:

```python
# Register native functions
@kernel_function(description="Get the weather for a city")
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny and 72°F."

kernel.add_plugin(get_weather, plugin_name="weather")

# The LLM can now call this function
# Its output is passed back to the LLM for the final response
```

```python
# Function calling with OpenAI-style tools
functions = [
    {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}}
        }
    }
]

# Kernel handles the function calling loop automatically
result = await kernel.invoke(
    "Suggest activities based on weather",
    functions=functions
)
```

## Memory (RAG Made Simple)

Semantic Kernel has built-in memory abstractions:

```python
# Semantic memory with vector search
from semantic_kernel.memory import VectorStoreTextMemory

memory = VectorStoreTextMemory(vector_store=ChromaDB())
kernel.add_memory(memory)

# Remember facts
await kernel.memory.save_information(
    collection="facts",
    id="user_preference",
    text="User prefers dark mode in their IDE"
)

# Later: retrieve relevant context
memories = await kernel.memory.search(
    "what does the user prefer?",
    collection="facts",
    limit=3
)
```

## Planning

The planner takes a high-level goal and breaks it into steps:

```python
from semantic_kernel.planners import ActionPlanner

planner = ActionPlanner(kernel)

# Given: "Book a flight to NYC next week"
plan = await planner.create_plan("Book a flight to NYC next week")

# Plan might look like:
# Step 1: search_flights(destination="NYC", date="next week")
# Step 2: filter_by_price(flights, budget=$500)
# Step 3: book_flight(selected_flight)
```

## Agents (Semantic Kernel)

```python
# Agent in Semantic Kernel
from semantic_kernel.agents import ChatCompletionAgent

agent = ChatCompletionAgent(
    kernel=kernel,
    name="ResearchAgent",
    instructions="You are a research assistant. Be thorough."
)

response = await agent.invoke("What are the latest AI agent trends?")
```

## Comparison with LangGraph and CrewAI

| Feature | Semantic Kernel | LangGraph | CrewAI |
|---------|----------------|-----------|--------|
| **Languages** | C# + Python | Python | Python |
| **Function calling** | ✅ Native | ⚠️ Manual | ⚠️ Manual |
| **Memory** | ✅ Built-in | ❌ External | ❌ External |
| **Planning** | ✅ Built-in | ⚠️ Do it yourself | ⚠️ Do it yourself |
| **Microsoft ecosystem** | ✅ Full | ❌ None | ❌ None |
| **Multi-agent** | ✅ Via Agent Framework | ✅ Graphs | ✅ Role-based |
| **Enterprise features** | ✅ (telemetry, middleware) | ❌ | ❌ |

## When to Use Semantic Kernel

**Use Semantic Kernel when:**
- You're in the Microsoft ecosystem (Azure, .NET)
- You want strong typing (C#)
- You need built-in planning and memory
- You want enterprise features (telemetry, observability)

**Use LangGraph when:**
- You want fine-grained control over agent graphs
- You're building complex, custom orchestration
- You prefer Python-only

**Use CrewAI when:**
- You want simple role-based agents
- Quick prototyping is priority

## Installation

```bash
# Python
pip install semantic-kernel

# .NET
dotnet add package Microsoft.SemanticKernel
```

## Microsoft Agent Framework 1.0 (2026)

As of April 2026, Semantic Kernel and AutoGen have merged into **Microsoft Agent Framework**:

```python
# Unified SDK (2026)
from microsoft_agent_framework import Agent, Kernel

# Works like Semantic Kernel (C#-first API)
kernel = Kernel()
kernel.add_service(AzureOpenAI())

# But also supports AutoGen-style group chat
group_chat = GroupChat(agents=[researcher, writer, critic])
```

See [[microsoft-autogen]] for the full comparison.

## Limitations

- **Complexity** — Semantic Kernel has a steep learning curve, especially C#
- **AutoGen merger** — The 2026 merger means some APIs are in transition
- **Python 3.12+** — May have compatibility issues with older Python versions
- **Documentation churn** — APIs changed significantly between 2024-2026

## Related Concepts

- [[microsoft-autogen]] — Now unified into Microsoft Agent Framework
- [[multi-agent-systems]] — Multi-agent architecture
- [[agent-orchestrator]] — Orchestration patterns
- [[mcp-model-context-protocol]] — Tool calling protocol
- [[langgraph]] — Alternative graph-based agent framework
- [[openai-agents-sdk]] — OpenAI's agent SDK

## Further Reading

- [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel) — Official repo
- [Semantic Kernel Docs](https://learn.microsoft.com/en-us/semantic-kernel/overview/) — Microsoft Learn
- [Microsoft Agent Framework 1.0](https://www.digitalapplied.com/blog/microsoft-agent-framework-1-0-dotnet-python-guide) — Unified SDK guide
