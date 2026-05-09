# Hermes Agent v0.13.0 — "The Tenacity Release" (May 7, 2026)

> Researched: 2026-05-09 | Source: X/Twitter community, GitHub releases, news aggregators

## Release Overview

**Hermes Agent v0.13.0 (v2026.5.7)** — Released May 7, 2026
- 864 commits · 588 merged PRs · 829 files changed
- 128,366 insertions · 282 issues closed (13 P0, 36 P1)
- 295 contributors (including co-authors)

**Tag:** Signed with verified Nous Research GPG key.

---

## Major Features

### Durable Kanban Multi-Agent Board
- **Heartbeat** — agents send keepalive signals
- **Reclaim** — stale tasks returned to board
- **Zombie detection** — identifies dead/stuck agents
- **Auto-block on incomplete exit** — prevents partial completion
- **Per-task retries** — automatic retry on failure
- **Hallucination recovery** — detect and recover from confabulation

### `/goal` Persistent Command
- Locks agent on a target across session turns (Ralph loop)
- Survives context changes and session context switches
- Enables long-running task completion without drift

### Checkpoints v2
- Real pruning for state persistence
- Solves checkpoint bloat problem
- Better session continuity

### Gateway Auto-Resume
- Interrupted sessions auto-resume after restart
- No lost work from unexpected disconnections

### Cron Watchdog Mode
- New `no_agent` watchdog for cron jobs
- Better reliability for scheduled tasks

### Security Wave (8 P0s Fixed)
- **Redaction ON by default** — sensitive data automatically redacted
- **Discord role-allowlists** now guild-scoped
- **WhatsApp rejects strangers** by default
- **TOCTOU windows** vulnerabilities closed

### Other Additions
- **Video analyze tool** — new capability
- **xAI Custom Voices TTS** — xAI integration
- **7-language i18n** — internationalization
- **Google Chat** — 20th platform supported

---

## Community Sentiment (X/Twitter)

### Positive
- 691 likes on NousResearch v0.13 announcement
- "Hermes Agent emerges as faster open-source rival to OpenClaw"
- "Set up in less than 1 hour even if you never touched terminal"
- 6,605 members in X community (growing)
- $3,000/month monetization case study on YouTube

### Concerns
- **Provider auth complexity** — "hardest part is provider authentication" (19 providers, 3 auth paths)
- **Memory skepticism** — "Every agent tool claims 'memory' but does it really work?"
- **GPT-5.5 instability** — "goblins and gremlins are with me"

### Use Cases Mentioned
1. Personal automation (salary doubling, research automation)
2. Multi-agent workflow orchestration
3. Self-improving assistant with memory
4. Developer tool (code tasks, API integrations)
5. Content creation pipelines

---

## Competitive Landscape

| vs OpenClaw | Hermes seen as faster, lighter, more reliable |
|---|---|
| vs Claude Code | Different focus — Hermes for persistence/memory, Claude for pure coding |
| vs Agent Zero | Docker setup gives "full AI agent army with one command" |

---

## Action Items for Anh's System

1. **Update Hermes to v0.13.0** — major stability + security improvements, especially redaction ON by default
2. **Explore Kanban multi-agent** — aligns with Felix Model orchestrator pattern
3. **Test `/goal` for long-running tasks** — could improve worker task completion
4. **Verify checkpoint v2** — better state persistence for session continuity
5. **Security audit** — confirm redaction is protecting sensitive data

---

## Key Stats

| Metric | Value |
|---|---|
| GitHub stars | Growing (significant) |
| X Community members | 6,605 |
| Release size | 864 commits, 588 PRs |
| Security P0s fixed | 8 |
| Contributors | 295 |

---

## Related

- `references/self-improving-agents-may-2026.md` — 10 new AI agent techniques
- `references/x-research-methodology.md` — X research methodology
