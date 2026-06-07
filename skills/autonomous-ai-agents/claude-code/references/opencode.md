# OpenCode CLI Reference

Formerly a standalone skill. Content absorbed into `claude-code`.

## Overview

Delegates coding tasks to OpenCode CLI — a provider-agnostic, open-source AI coding agent.

## Prerequisites

- OpenCode installed: `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`
- Auth configured: `opencode auth login`

## One-Shot Tasks

```
terminal(command="opencode run 'Add retry logic to API calls'", workdir="~/project")
```

## Interactive Sessions

```
terminal(command="opencode", workdir="~/project", background=true, pty=true)
```

## Key Flags

| Flag | Effect |
|------|-------|
| `run 'prompt'` | One-shot execution |
| `--continue` / `-c` | Continue last session |
| `--model provider/model` | Force specific model |
| `--file <path>` / `-f` | Attach files |

## PR Reviews

```
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

## Pitfalls

- Interactive sessions require `pty=true`
- Do NOT use `/exit` — use Ctrl+C instead
- PATH mismatch can select wrong binary
