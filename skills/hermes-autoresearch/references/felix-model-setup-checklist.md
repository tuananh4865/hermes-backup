# Felix Model Setup Verification Checklist

> Updated 2026-05-06: Workers created, but cron prompts still wrong

## Current Status (2026-05-06)

| Component | Created | Working |
|-----------|---------|---------|
| content-creator SOUL.md + HEARTBEAT.md + outputs/ | ✅ | ❌ (cron uses wrong prompt) |
| research-agent SOUL.md + HEARTBEAT.md + outputs/ | ✅ | ❌ (cron uses wrong prompt) |
| orchestrator SOUL.md + HEARTBEAT.md | ✅ | ❌ (cron uses wrong prompt) |
| memory/MEMORY.md + PENDING_TASKS.md + daily/ | ✅ | ✅ |
| Worker cron jobs | ✅ | ❌ Wrong prompt = runs autoresearch not worker task |

## What Was Done (2026-05-06)

1. Created worker structure:
```
~/.hermes/workers/
├── content-creator/     ✓ SOUL.md + HEARTBEAT.md + outputs/
├── research-agent/       ✓ SOUL.md + HEARTBEAT.md + outputs/
├── orchestrator/        ✓ SOUL.md + HEARTBEAT.md
└── memory/              ✓ MEMORY.md + PENDING_TASKS.md + daily/
```

2. Removed duplicate cron (90c50d1a2d3c) — same content as a4b8e528983f

3. Verified: `ls -la ~/.hermes/workers/*/` shows files exist

## Still Broken

**Worker cron jobs use `hermes-autoresearch` skill** — WRONG.
- ce3701b4dcdd should run Content Creator morning brief
- e4fb0c36e9f7 should run Research Analyst morning brief
- But they invoke `hermes-autoresearch` skill, so they run self-improvement instead

**FIX NEEDED:** Update cron job prompts to be worker-specific, not autoresearch.

## Correct Architecture (Felix Model)

```
Hermes (Orchestrator)
├── cron: autoresearch 2AM          → Self-improvement
├── cron: X research 7AM            → Market intelligence
├── cron: Content Creator 8AM        → TikTok scripts [PROMPT WRONG]
├── cron: Research Analyst 8:30AM   → Product research [PROMPT WRONG]
├── cron: Orchestrator 9AM          → Daily briefing [PROMPT WRONG]
├── cron: Monitor every 2h          → Worker health [PROMPT WRONG]
├── cron: Content Creator 6PM       → Evening report [PROMPT WRONG]
├── cron: Research Analyst 6:30PM  → Evening report [PROMPT WRONG]
└── cron: Orchestrator 9PM          → Consolidation [PROMPT WRONG]
```

## Checklist to Complete Setup

### Phase 1: Worker Files ✅ DONE 2026-05-06
- [x] content-creator/SOUL.md
- [x] content-creator/HEARTBEAT.md
- [x] research-agent/SOUL.md
- [x] research-agent/HEARTBEAT.md
- [x] orchestrator/SOUL.md
- [x] orchestrator/HEARTBEAT.md
- [x] memory/MEMORY.md
- [x] memory/PENDING_TASKS.md
- [x] memory/daily/
- [x] outputs/ directories

### Phase 2: Fix Cron Prompts ❌ NOT DONE
- [ ] ce3701b4dcdd — update prompt to Content Creator specific
- [ ] 50bc2c2dfbb3 — update prompt to Content Creator specific
- [ ] e4fb0c36e9f7 — update prompt to Research Analyst specific
- [ ] 1c425ba42980 — update prompt to Research Analyst specific
- [ ] 045a44210a59 — update prompt to Orchestrator specific
- [ ] f1584a9a1d86 — update prompt to Orchestrator specific
- [ ] fc2191d508a3 — update prompt to Orchestrator specific

### Phase 3: Verify End-to-End ❌ NOT DONE
- [ ] Run each cron manually
- [ ] Check output in `~/.hermes/cron/output/{job_id}/`
- [ ] Verify output matches expected worker task
- [ ] Confirm delivers to correct Telegram thread
