# Two-Mode Agent Coordination — Verified 2026-05-05

## Overview

Tuấn Anh's Hermes setup uses TWO distinct coordination modes:

## Mode 1: Cron-Based Workers (Business Automation)

**Architecture:**
```
User (Tuấn Anh)
    ↓
Hermes (Orchestrator) — Cron-driven
    ├── 9AM: Morning Briefing
    ├── Every 2h: Agent Monitor
    ├── 8AM/6PM: Workers trigger via cron
    └── 9PM: Nightly Consolidation
    ↓
Workers (content-creator, research-agent)
    ↓
Outputs → memory/ → Report to Anh
```

**Workers have:**
- `SOUL.md` — Identity, voice, style
- `HEARTBEAT.md` — Schedule (30min/2h/6h/daily)
- `outputs/` — Completed work

**Best for:** TikTok content, market research, daily reporting

## Mode 2: Tmux Pane Agents (Complex Coding)

**Architecture:**
```
tmux pipeline session (4 panes)
├── Pane 0: pi-coding-agent (Mario's coding agent)
├── Pane 1: smartapp-ui (project build)
├── Pane 2: crashed (TUI error)
└── Pane 3: smartapp-infra (docker-compose)
```

**Agents have:**
- Persistent terminal state
- Real-time output visible
- Direct human monitoring possible

**Best for:** Building apps, complex debugging, parallel coding

## Current State (2026-05-05)

| Mode | Status | Running |
|------|--------|---------|
| Cron Workers | ✅ Configured | 8 cron jobs active |
| Tmux Coding | ⚠️ Demo | smartapp project (not business) |

## Key Insight

**"Workers configured" ≠ "Workers running"**

Creating SOUL.md + HEARTBEAT.md + cron jobs = automation ACTIVE

BUT:
- tmux pipeline currently running DEMO project (smartapp), not business workflow
- Content pipeline has crons but no real content tasks executed yet
- Revenue: $0 (no product sold yet)

## Felix Model Checklist (For Future)

- [x] Workers: SOUL.md + HEARTBEAT.md + memory structure
- [x] Orchestrator: SOUL.md + HEARTBEAT.md + crons
- [ ] tmux: Running actual business workflow (not demo)
- [ ] Revenue: Real product being sold
- [ ] Content: Real scripts executed
