---
title: Tool Use
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [tool-use, agents, llm, function-calling, ai-agents, autonomous]
sources: []
---

# Tool Use

## Overview

Tool use in AI agents refers to the capability of large language models (LLMs) to interact with external systems — calling functions, executing code, querying databases, browsing the web, reading and writing files — to accomplish tasks beyond standalone text generation. When an LLM is given the ability to use tools, it transitions from a passive generator of text to an active agent that can perceive, plan, and act in the world. This is the foundation of modern AI agent architectures and what enables systems like ChatGPT plugins, Code Interpreter, and autonomous agents that can browse the web, write and run code, and manage files.

The importance of tool use cannot be overstated. LLMs, no matter how capable, are fundamentally limited to knowledge encoded in their training data and the tokens in their input context. Tool use extends their reach to real-time information, persistent state, computational abilities, and the ability to affect change outside the model itself. An agent that can use a web search tool has access to up-to-date information. One that can run Python code can perform calculations no LLM can do accurately from memory alone. One that can read files can reason about and synthesize information from local documents.

## Key Concepts

Understanding tool use requires familiarity with these core concepts:

**Function Calling / Tool Calling** — A mechanism by which an LLM generates structured output (typically JSON) that represents a request to invoke a specific function with specific arguments. Function calling is the bridge between natural language intent and programmatic API calls. Rather than generating free-form text, the model outputs a JSON object naming the function and its parameters, which the runtime then executes.

**Tool Definition** — The structured description of a tool's interface, including its name, parameters (with types and descriptions), and return type. Tool definitions are typically provided to the model in a prompt, often using the OpenAI function calling schema or the Anthropic tool use format. A well-written tool definition is critical — it determines whether the model correctly understands when and how to call the tool.

**Tool Runtime / Executor** — The component that receives the model's function call, executes it (calling an API, running code, reading a file), and returns the result to the model. The executor handles authentication, error handling, retries, timeouts, and result formatting. Common implementations include LangChain's tool executors, the OpenAI Assistants API's tool engine, or custom agent loops.

**ReAct (Reasoning + Acting)** — A popular agent architecture pattern where the model alternates between reasoning steps ("I need to find the weather in Tokyo") and action steps ("I'll call the weather API"). ReAct combines chain-of-thought reasoning with tool actions, allowing the model to plan multi-step sequences and adapt based on tool results.

**Planning and Task Decomposition** — Advanced agents break complex goals into sub-tasks, select appropriate tools for each, execute them in sequence, and synthesize results. This is sometimes called "high-level planning" versus "low-level action execution." Frameworks like AutoGPT, BabyAGI, and LangChain agents implement variations of this.

**Tool Result Formatting** — How tool results are fed back to the model. Raw results (strings, objects, errors) are often summarized or reformatted to fit within the context window. Some systems truncate large outputs, others extract only the relevant fields, and some use the model itself to summarize results.

## How It Works

A typical tool-use loop works as follows:

1. **User Request** — The user provides a goal or question, e.g., "What's the weather in Tokyo right now?"

2. **Tool Selection** — The agent (LLM) evaluates the request, optionally thinks through the steps (in a ReAct loop), and decides to call a tool. It generates a function call JSON like `{"name": "get_weather", "arguments": {"location": "Tokyo"}}`.

3. **Execution** — The tool runtime receives the call, looks up the `get_weather` function, passes the arguments, and executes it — calling a weather API, for example.

4. **Result Injection** — The result is returned to the agent, typically formatted as a tool result message. The model sees both the tool's output and its previous reasoning.

5. **Response Generation** — The model synthesizes the tool result and generates a natural language response to the user, or decides to call another tool if the task requires multiple steps.

```python
# Example: A simple tool-use executor in Python
import json

# Tool definition
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

# Tool implementations
def get_weather(city: str) -> str:
    # In reality, call a weather API
    return f"The weather in {city} is 72°F and sunny."

# Simulated LLM decision (normally done by actual model API)
def simulate_llm_tool_call(intent: str):
    if "weather" in intent.lower():
        return {"name": "get_weather", "arguments": {"city": "Tokyo"}}
    return None

# Executor
def execute_tool(tool_call):
    tool_name = tool_call["name"]
    args = tool_call["arguments"]
    if tool_name == "get_weather":
        return get_weather(**args)

# Loop
user_intent = "What's the weather in Tokyo?"
tool_call = simulate_llm_tool_call(user_intent)
result = execute_tool(tool_call)
print(f"Tool result: {result}")
```

## Practical Applications

Tool use enables a vast array of AI agent applications:

**Research Agents** — Agents that browse the web, read documents, extract information, take notes, and synthesize findings across many sources. They can research a topic for minutes or hours, reading hundreds of pages and returning synthesized reports.

**Coding Assistants** — Agents that write, test, and debug code. Tools include REPLs for running code (Python, JavaScript), git for version control, file system access for reading and writing code, and search tools for documentation.

**Data Analysis Agents** — Agents that load datasets, run statistical analyses, generate visualizations, and produce reports. They use Python or R execution tools to perform real computations beyond what the model's math abilities can guarantee.

**Personal Assistants** — Agents that manage calendars, send emails, set reminders, search the web, and interact with productivity tools like Notion, Slack, or CRM systems via their APIs.

**DevOps and CI/CD Agents** — Agents that monitor deployments, query logs, roll back services, run tests, and respond to incidents. They interact with cloud provider APIs (AWS, GCP, Azure), Kubernetes, and monitoring tools.

## Examples

Here's a more complete example using OpenAI's function calling:

```python
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What is 15% of 840?"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

tool_call = response.choices[0].message.tool_calls[0]
print(f"LLM called: {tool_call.function.name} with {tool_call.function.arguments}")

# Execute the tool
import json
args = json.loads(tool_call.function.arguments)
result = eval(args["expression"])  # Never use eval in production!
print(f"Result: {result}")

# Feed result back to model
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

follow_up = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)
print(f"Final response: {follow_up.choices[0].message.content}")
```

## Related Concepts

- [[ai-agent]] — AI agents as the broader concept that encompasses tool use
- [[agent-frameworks]] — Frameworks that implement tool use patterns (LangChain, AutoGen, etc.)
- [[function-calling]] — The specific API mechanism for tool invocation in LLMs
- [[ReAct]] — A specific agent architecture combining reasoning and acting
- [[Prompt Engineering]] — The broader practice of crafting prompts that elicit desired behaviors

## Further Reading

- OpenAI Function Calling Guide — platform.openai.com/docs/guides/function-calling
- Anthropic Tool Use Documentation — docs.anthropic.com/claude/docs/tool-use
- "ReAct: Synergizing Reasoning and Acting in Language Models" — paper by Yao et al.
- LangChain Tools Documentation — python.langchain.com/docs/concepts/tools
- "Tool Learning with Large Language Models" — survey paper on tool-augmented LLMs

## Personal Notes

Tool use is what separates toy demos from real AI agents. A chat model that can only generate text is impressive, but an agent that can call APIs, run code, and manipulate files is genuinely useful. The function calling APIs from OpenAI and Anthropic have matured significantly — they're reliable enough for production use, with well-defined schemas and error handling. The hard part isn't the API; it's writing good tool definitions that the model understands correctly and designing the agent loop so it doesn't get stuck in infinite tool-call cycles. Start simple: give your agent one or two tools, let it prove it can use them reliably, then expand. Over-engineering the agent loop upfront is the most common mistake.
