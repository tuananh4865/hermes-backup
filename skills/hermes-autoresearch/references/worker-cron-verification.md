# Worker Cron Verification Pattern

> Created: 2026-05-06  
> Purpose: Verify whether worker crons are producing correct output or still misconfigured

## The Problem

Worker cron jobs were created with SOUL.md files, but the cron prompts were never actually updated — they still ran `hermes-autoresearch` instead of worker-specific prompts. The fix claimed to work in one session, but subsequent sessions showed the crons still misconfigured.

## Verification Checklist

Run ALL three checks — all three must pass for crons to be "working":

### Check 1: Output Content

```bash
# Check content of most recent cron output
head -10 ~/.hermes/cron/output/{job_id}/*.md | head -20

# Expected (GOOD): Worker SOUL.md content
# - Content Creator: "mấy con vợ", Gen Z slang, TikTok script
# - Research Analyst: "TikTok Shop", product trends
# - Orchestrator: "Hoàn thành | Đang làm | Cần quyết định"

# Bad (WRONG): hermes-autoresearch content
# - Starts with "title: Hermes Autoresearch"
# - Mentions "Skills_Score", "Hermes_Score"
# - Mentions "SHS = stale × 10"
```

### Check 2: Cron Skills Column

```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list

# Expected (GOOD): Skills column shows "none" or empty
# Wrong: Skills column shows "hermes-autoresearch"
```

### Check 3: Worker Output Directories

```bash
# Content Creator outputs
ls -la ~/.hermes/workers/content-creator/outputs/

# Research Analyst outputs  
ls -la ~/.hermes/workers/research-agent/outputs/

# Expected (GOOD): .md files dated today with actual script/research content
# Wrong: Empty directories (workers never produced anything)
```

## Known Worker Cron Jobs

| Job ID | Name | Worker | Expected Output |
|--------|------|--------|-----------------|
| ce3701b4dcdd | Content Creator Morning | content-creator | TikTok script in outputs/ |
| 50bc2c2dfbb3 | Content Creator Evening | content-creator | Script summary in outputs/ |
| e4fb0c36e9f7 | Research Analyst Morning | research-agent | Research in outputs/ |
| 1c425ba42980 | Research Analyst Evening | research-agent | Research in outputs/ |
| 045a44210a59 | Orchestrator Morning | orchestrator | Briefing for Anh |
| f1584a9a1d86 | Orchestrator Monitor | orchestrator | Worker nudge if stalled |
| fc2191d508a3 | Orchestrator Nightly | orchestrator | Consolidation report |

## If Verification Fails

### Step 1: Read Current Cron Prompt

```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list
# Copy the prompt_preview for the broken job
```

### Step 2: Read Worker's SOUL.md

```bash
cat ~/.hermes/workers/{worker}/SOUL.md
```

### Step 3: Compare

If prompt_preview matches SOUL.md → cron is correctly configured, problem is elsewhere.

If prompt_preview shows `hermes-autoresearch` content → cron needs fixing.

### Step 4: Fix Attempt (VERIFIED 2026-05-07)

⚠️ **`--prompt-file` does NOT exist** — the CLI only has `--prompt`. Shell expansion `$(cat ...)` also fails.
✅ **CORRECT pattern: Python subprocess with explicit prompt string:**

```python
import subprocess, sys

with open('/Users/tuananh4865/.hermes/workers/{worker}/SOUL.md', 'r') as f:
    prompt = f.read()

result = subprocess.run(
    [sys.executable, '-m', 'hermes_cli.main', 'cron', 'edit',
     job_id, '--prompt', prompt, '--clear-skills'],
    cwd='/Users/tuananh4865/.hermes/hermes-agent'
)
```

**Do NOT use:**
- ❌ `cron edit --prompt "$(cat SOUL.md)"` — shell expansion fails
- ❌ `cron edit --prompt-file /tmp/prompt.txt` — `--prompt-file` doesn't exist

### Step 5: Verify Fix

Re-run all three checks above.

## Key Insight

**"Workers configured" ≠ "Workers running"**

Even if SOUL.md files exist and cron jobs exist, the crons may be running the WRONG prompt (hermes-autoresearch instead of worker-specific content). Must verify actual output, not just configuration files.

## Session Continuity Issue

This verification session (the one reading this file) ran as a cron but the crons themselves are still misconfigured. The session found that:
- All 7 worker crons still output `hermes-autoresearch` content
- Worker output directories remain empty
- The "fix applied" claim from 2026-05-06 was premature

This suggests the `cron edit` command may not persist prompt changes correctly, or there's a shell expansion issue with `$(cat ...)` in the prompt string.
