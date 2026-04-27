---
title: "Vercel AI SDK"
created: 2026-04-15
updated: 2026-04-19
type: entity
tags: [vercel, ai-sdk, typescript, react, nextjs, llm, agent-framework]
related:
  - [[llm-application-development]]
  - [[agent-frameworks]]
  - [[langgraph]]
  - [[vercel]]
sources:
  - https://vercel.com/docs/ai-sdk
  - https://ai-sdk.dev/docs/introduction
  - https://vercel.com/ai
  - https://vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk
  - https://www.truefoundry.com/blog/vercel-ai-review-2026-we-tested-it-so-you-dont-have-to
---

# Vercel AI SDK

> TypeScript toolkit for building AI-powered applications with streaming UI and multi-model support. The standard for Next.js AI integration.

## Overview

The **Vercel AI SDK** is an open-source TypeScript toolkit designed to help developers build AI-powered applications with React, Next.js, Vue, Svelte, Node.js, and other frameworks. It abstracts the complexity of working with Large Language Models (LLMs) and provides a unified API across multiple providers.

**Developer:** Vercel (formerly Zeit)
**First Released:** 2023
**License:** Apache 2.0
**Repository:** `vercel/ai` on GitHub
**Package:** `ai` on npm

## Core Features

### Provider Abstraction

The AI SDK provides a unified interface across multiple LLM providers:

| Provider | Model Support |
|----------|--------------|
| **OpenAI** | GPT-4o, GPT-5 series, o1, o3 |
| **Anthropic** | Claude 3.5, Claude 4 series |
| **Google** | Gemini 1.5, Gemini 2.0 |
| **AWS Bedrock** | Claude, Llama, Mistral (via Bedrock) |
| **Local Models** | llama.cpp, Ollama, MLX (Apple Silicon) |

This means you can swap providers without rewriting application code — critical for cost optimization and vendor diversification.

### Streaming UI Helpers

Vercel's secret weapon is its **streaming UI primitives**. The SDK provides React hooks that make it trivial to render streaming LLM responses as they arrive:

```tsx
import { useCompletion } from 'ai/react'

export default function Chat() {
  const { completion, input, handleInputChange, handleSubmit } = useCompletion()

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={input}
        onChange={handleInputChange}
        placeholder="Ask anything..."
      />
      <div>{completion}</div>
    </form>
  )
}
```

The `completion` variable streams in token-by-token, giving users immediate feedback without waiting for the full response.

### AI Agents with Tools

The SDK supports tool calling (function calling) and multi-step agentic workflows:

```typescript
import { agent } from 'ai-sdk/openai'

const result = await agent({
  model: openai('gpt-5'),
  system: 'You are a research assistant.',
  tools: {
    searchWeb: defineFunction({
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => webSearch(query)
    })
  },
  messages: [{ role: 'user', content: 'Research Anthropic company.' }]
})
```

## AI SDK for Agents

As of 2026, Vercel has significantly expanded agentic capabilities:

- **Multi-step agents** — Build agents that use tools over multiple turns
- **Agent memory** — Maintain conversation context across interactions
- **Streaming responses** — Agents stream their thinking and responses in real-time
- **Edge deployment** — Agents can run on Vercel Edge Functions for low latency

The `ai` package provides:
- `generateText` — Simple text generation with tool support
- `streamText` — Streaming text with tool support
- `generateObject` — Structured object generation (Zod schemas)
- `agent` — Full agentic workflow orchestration

## Deployment on Vercel

Vercel's platform provides key advantages for AI applications:

- **Automatic scaling** — Handle viral traffic without infrastructure management
- **Edge deployment** — Run AI routes geographically close to users
- **Branch-based previews** — Test AI features in isolated environments
- **Built-in streaming** — HTTP streaming works out-of-the-box on Vercel's runtime

### Deployment Guide

```bash
npm install ai @ai-sdk/openai
```

Create an AI route in Next.js:

```typescript
// app/api/chat/route.ts
import { openai } from '@ai-sdk/openai'
import { streamText } from 'ai'

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openai('gpt-5'),
    system: 'You are a helpful assistant.',
    messages
  })

  return result.toDataStreamResponse()
}
```

## Comparison with Other Frameworks

| Dimension | Vercel AI SDK | LangGraph | CrewAI |
|-----------|---------------|-----------|--------|
| **Primary focus** | LLM integration + streaming UI | Complex agent graphs | Multi-agent orchestration |
| **Learning curve** | Low | Medium-High | Medium |
| **UI framework** | React/Next.js first | Framework-agnostic | Framework-agnostic |
| **Agent orchestration** | Basic agents | Advanced graphs | Role-based agents |
| **Deployment** | Vercel-optimized | Any platform | Any platform |

## When to Use Vercel AI SDK

**Best for:**
- Next.js/React applications with AI features
- Rapid prototyping of LLM-powered UIs
- Streaming text responses
- Teams already on Vercel's platform
- Provider-agnostic LLM integration

**Consider alternatives if:**
- You need complex multi-agent orchestration (use LangGraph)
- You're building Python-first agent systems (use CrewAI or LangGraph)
- You need graph visualization and time-travel debugging

## Ecosystem

- **AI SDK UI** — React hooks for streaming chat/completion interfaces
- **AI SDK RSC** — React Server Components support for AI
- **AI SDK Edge** — Edge runtime deployment
- **Prompt management** — Integration with Vercel's KV storage for prompts
- **LangChain integration** — Can wrap LangChain chains for advanced orchestration

## Related Concepts

- [[agent-frameworks]] — Broader landscape of agent development tools
- [[llm-application-development]] — Patterns for building LLM apps
- [[langgraph]] — More advanced graph-based agent orchestration
- [[vercel]] — The platform itself
