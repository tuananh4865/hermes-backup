---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 self-healing-wiki (extracted)
  - 🔗 wiki-self-evolution (extracted)
  - 🔗 wiki-master-plan (extracted)
relationship_count: 3
---

# Watchdog System

> Event-driven file watcher that triggers wiki self-healing and self-evolution on file changes.

## Overview

Watchdog replaces cron-based polling with event-driven triggers. When files change, the watchdog:
1. Debounces rapid changes (10s window)
2. Gathers context about what changed
3. Triggers self-heal or self-evolution agent
4. Reports results

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Watchdog Daemon | `scripts/watchdog_daemon.py` | Poll for file changes |
| Context Builder | `scripts/watchdog_context_builder.py` | Gather change context |
| Git Hook | `.git/hooks/post-commit` | Trigger on commit |
| Event File | `.git/WATCHDOG_EVENT` | Signal file for events |

## Architecture

```
[File Change Detected]
        ↓
[Watchdog Poll (5s)] → Debounce (10s)
        ↓
[Read watchdog_event.json]
        ↓
[hermes cron tick] → Agent gets wiki:change event
        ↓
[Context Builder] → Gathers recent changes
        ↓
[Agent decides]: Self-Heal or Self-Evolution
        ↓
[Execute] → Results
        ↓
[Notify] → Telegram if flags needed
```

## Usage

```bash
# Start watchdog daemon
python3 scripts/watchdog_daemon.py start

# Stop watchdog daemon
python3 scripts/watchdog_daemon.py stop

# Check status
python3 scripts/watchdog_daemon.py status

# Trigger manually
python3 scripts/watchdog_daemon.py trigger
```

## Events

The watchdog processes these event types:

| Event | Trigger | Action |
|-------|---------|--------|
| `wiki:change` | Any .md file changed | Run self-heal on changed files |
| `wiki:commit` | Git post-commit hook | Refresh context, check health |
| `wiki:request` | User request | Run full self-evolution |

## Configuration

```yaml
# In wiki config (future)
watchdog:
  poll_interval: 5  # seconds
  debounce_window: 10  # seconds
  auto_heal: true
  auto_evolve: false  # Requires explicit trigger
  notify_on_flags: true
```

## Related

- [[self-healing-wiki]] — Auto-fix broken links, frontmatter
- [[wiki-self-evolution]] — Gap filling, quality improvement
- [[wiki-master-plan]] — All wiki scripts listed in Phase 1-5
- [[log]] — Wiki activity log
