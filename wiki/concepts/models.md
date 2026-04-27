---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 wiki (extracted)
  - 🔗 lm-studio (extracted)
  - 🔗 lm-studio (extracted)
  - 🔗 lm-studio (extracted)
  - 🔗 local-llm (extracted)
relationship_count: 5
---

# Models

## Overview

Các LLM models được sử dụng trong [[wiki]] và  system.

## Local Models (LM Studio)

### Primary Model
- **qwen3.5-2b-mlx** — Default copyist model
  - Role: Content transcription, formatting
  - Provider: [[lm-studio]]
  - Location: 192.168.0.187:1234

### Reasoning Model
- **mlx-qwen3.5-0.8b-claude-4.6-opus-reasoning-distilled**
  - Role: Reasoning tasks (note: NOT for copyist work)
  - Issue: Output goes to reasoning_content field

## Model Selection Guidelines

| Task Type | Recommended Model | Why |
|-----------|-------------------|-----|
| Copy/transcribe | qwen3.5-2b-mlx | Stable output, no reasoning overhead |
| Code generation | Codex/Claude Code | Specialized for code |
| Reasoning | opus-reasoning-distilled | Thinking tokens |

## Model Philosophy

> Local models are for **COPYIST tasks ONLY** — reformat/transcribe content provided by user. NOT for reasoning or searching information.

## Related

- [[lm-studio]] — Local model serving
- [[lm-studio]] — Alternative local model runner
- [[local-llm]] — Local LLM usage patterns
- Hub — Model hub
