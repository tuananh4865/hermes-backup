---
title: "Tools"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [tools, ai-agents, function-calling, tool-use]
---

# Tools

## Overview

In the context of AI agents, tools are structured mechanisms that enable language models to interact with external systems, retrieve information, and perform actions beyond their base training data. Rather than generating static responses, AI agents leverage tools to access real-time data, execute code, call APIs, and manipulate external resources. This capability bridges the gap between a model's knowledge cutoff and the dynamic, ever-changing nature of the real world.

Tool use fundamentally changes how AI systems operate. Instead of relying solely on parametric memory (information learned during training), agents can supplement their responses with real-time information retrieved through [[function-calling]] mechanisms. When an AI agent encounters a query it cannot answer from training data alone—such as current weather conditions, live stock prices, or code that requires execution—it invokes a tool, receives the result, and incorporates that information into its response.

The tool use workflow typically follows a structured pattern: the model receives a user prompt, determines which tool(s) to invoke, generates a properly formatted tool call request, waits for the external system to return results, and then synthesizes those results into a coherent final response. This creates a dynamic, multi-turn interaction where the AI actively reasons about when and how to use external resources.

## Tool Types

### Web Search

Web search tools enable AI agents to query search engines and retrieve current information from the internet. These tools are essential for questions requiring up-to-date facts, news, or information beyond a model's training cutoff. Agents can specify search parameters, parse results, and synthesize findings into natural language responses.

### Code Execution

Code execution tools allow AI agents to run programming code in sandboxed environments. Whether Python, JavaScript, or other languages, these tools enable agents to perform calculations, process data, run simulations, or test hypotheses programmatically. This is particularly valuable for tasks involving mathematics, data analysis, or generating executable outputs.

### API Calls

API call tools let AI agents interact with external services and databases. Agents can query REST APIs, GraphQL endpoints, or custom service interfaces to fetch structured data, trigger actions in other systems, or integrate with third-party platforms. This enables integration with calendars, email systems, databases, and countless other external resources.

### File System Operations

File system tools permit AI agents to read from and write to local or remote storage systems. Agents can access documents, parse configuration files, log information, or manage data persistence across interactions.

### Custom Tools

Organizations often define custom tools tailored to specific domains or workflows. These might include internal database queries, proprietary system interactions, or specialized business logic implementations.

## Definition Patterns

Tool definitions typically follow structured schemas that specify the tool's name, description, parameters, and expected output format. In function calling implementations, tools are defined as JSON objects containing:

- **name**: A unique identifier for the tool
- **description**: Human-readable explanation of the tool's purpose
- **parameters**: A schema defining required and optional inputs, including data types and constraints

This standardized format allows models to understand tool capabilities through prompting and generate correctly structured calls. Different platforms (OpenAI, Anthropic, Google) use slightly varying schemas, but the core concept remains consistent: provide enough metadata for the model to intelligently select and invoke tools when appropriate.

## Related

- [[function-calling]]
- [[ai-agents]]
- [[self-healing-wiki]]
