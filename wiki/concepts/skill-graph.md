---
title: Skill Graph
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent, memory, knowledge-base, content-automation]
confidence: high
sources: [raw/articles/deronin-skill-graph-content-team.md]
relationships: [[harrison-chase]], [[karpathy-llm-wiki]], [[hermes-agent]], [[obsidian-skills]]
---

# Skill Graph

A **skill graph** is a folder of interconnected Markdown files that transforms a generic AI agent into a specialized expert system — without fine-tuning or RAG.

Instead of one giant instruction file, you create many small files where each holds one job, one rule, one voice guide, one workflow, one audience profile, or one platform style.

## Core Idea

The agent reads the graph (a folder of .md files linked via `[[wikilinks]]`), follows the connections, and executes tasks as a specialized team.

- **One flat .md file** = a TOOL (a reference doc)
- **30+ interconnected .md files** = a full TEAM that's read your entire playbook

## How It Works

1. **Create nodes** — Each .md file is one knowledge node (brand voice, platform style, audience profile, hooks, workflows)
2. **Link with wikilinks** — `[[brand-voice]]`, `[[hooks]]`, `[[linkedin-post]]` connect nodes
3. **Agent traverses** — The AI reads the index, follows links, loads what's relevant
4. **Output is specialized** — One idea → 10 platform-native posts, each "thinking" differently

## Tools

| Tool | Purpose |
|------|---------|
| [[obsidian-skills]] | Build + visualize the graph |
| @arscontexta | Claude plugin for traversing skill graphs |
| @obsdmd | Write and visualize the graph |
| Any AI agent (Claude, ChatGPT, Cursor) | Execute the graph |

## DeRonin's Content System

Running 10 social accounts with NO manual posting:

- 1 idea → 10 platform-native posts
- 30+ .md files = content team member per platform/account
- No $8-12k/mo agency retainer
- No rewriting the same post 10x

## Related Concepts

- [[harrison-chase]] — "Your Harness Your Memory" — LangChain's memory-centric agent approach
- [[karpathy-llm-wiki]] — Karpathy's wiki-as-LLM-memory pattern
- [[hermes-agent]] — Hermes skill system uses similar graph-like structure
- [[obsidian-skills]] — kepano's Obsidian skills pattern for markdown knowledge management
