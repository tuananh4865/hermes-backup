---
title: "Rubber Duck Debugging"
description: "The practice of explaining code line-by-line to an inanimate object (or AI) to systematically identify bugs and solve problems through forced articulation."
tags: [debugging, problem-solving, solo-dev, ai-pair-programming, llm]
created: 2026-04-12
updated: 2026-04-20
type: concept
sources:
  - https://en.wikipedia.org/wiki/Rubber_duck_debugging
  - https://blog.pragmaticengineer.com/rubber-duck-debugging/
related:
  - [[problem-solving]]
  - [[llm-reasoning]]
  - [[solo-dev-ai]]
  - [[debugging]]
  - [[self-improving-ai]]
---

# Rubber Duck Debugging

Rubber duck debugging is a deceptively simple technique: you explain your code line-by-line to a rubber duck (or any inanimate object, or an AI assistant) as if teaching it how the program works. The act of verbalizing your reasoning forces you to confront the gap between what you *think* your code does and what it actually *does*.

## How It Works

The core insight is that code often fails not because of syntax errors — those the compiler catches — but because of **assumption errors**: the programmer believes the code works a certain way, but the actual execution path reveals a different truth. Explaining your logic to someone (even a rubber duck) makes these mismatches impossible to hide.

1. **Describe the intent** — "This function should take a list of numbers and return the sum"
2. **Walk the execution** — "First we iterate through each element, then we add it to the accumulator"
3. **Confront the gap** — At some point, you say "and here the variable should be..." and realize it isn't

The technique is so effective that some developers keep an actual rubber duck on their desk. In 2026, AI coding assistants like Claude Code and ChatGPT have become the "rubber duck" of choice — explaining code to an LLM often surfaces the exact bug before you even finish typing the prompt.

## Why It Works: The Feynman Technique

Richard Feynman learned by explaining topics to others (and to himself). The same mechanism applies here:

- **Passive reading** lets your brain glide over gaps in understanding
- **Active explanation** forces each assumption to be stated explicitly
- **Externalization** creates a "conversation partner" that can't nod along — it doesn't understand, so it can't fill in the blanks

This is fundamentally the same reason [[llm-reasoning]] works: LLMs that explain their reasoning step-by-step catch errors they would miss in a single pass.

## AI as Rubber Duck

In 2026, explaining code to AI assistants has become the most scalable form of rubber duck debugging. The pattern that works:

> "I'm trying to do X, here's my code: [paste]. The expected output is Y but I'm getting Z. Walk through my logic and tell me where I'm wrong."

The AI doesn't have your mental model, so it asks clarifying questions. The act of answering those questions — even just formulating the response — often reveals the bug. This is one reason AI coding assistants have become indispensable for [[solo-dev-ai]] workflows.

## Key Principles

- **Be specific** — "explain this function" vs. "explain what happens at line 47 when the list is empty"
- **State assumptions aloud** — "I assume this variable is in scope here..."
- **Don't skip the "obvious" parts** — bugs hide in the parts you think you understand
- **Use the AI as a questioning partner** — ask it to find where your logic might break

## Related Concepts

- [[debugging]] — broader category of finding and fixing bugs
- [[llm-reasoning]] — LLMs reason better step-by-step, same principle
- [[solo-dev-ai]] — AI as always-available debugging partner for solo developers
- [[problem-solving]] — the meta-skill rubber duck debugging exercises
