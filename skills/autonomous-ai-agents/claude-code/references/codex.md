# Codex CLI Reference

Formerly a standalone skill. Content absorbed into `claude-code`.

## Overview

Delegates coding tasks to OpenAI Codex CLI. Supports features, refactoring, and PR reviews.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured
- Must run inside a git repository

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

## Key Flags

| Flag | Effect |
|------|-------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes |
| `--yolo` | No sandbox, no approvals (fastest) |

## PR Reviews

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing

```
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="codex --yolo exec 'Fix issue #78: <description>'", workdir="/tmp/issue-78", background=true, pty=true)
```
