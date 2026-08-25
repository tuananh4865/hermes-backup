# Cron Management Patterns

## The Core Rule

| User says | You do |
|-----------|--------|
| "add to cron" | `~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit {job_id} --prompt "existing + new"` |
| "update skill" | `skill_manage patch skill-name` |
| "create new cron" | `cronjob create` (AFTER `cronjob list` to check no duplicate) |

**NEVER confuse these.** Skill = pattern doc. Cron prompt = what actually runs.

**CRITICAL:** The command is `cron edit`, NOT `cron update`. `cron update` does not exist.

## Cron Job Lifecycle

### Before Creating ANY Cron
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list  # Check: does similar job already exist?
```
If YES → EDIT existing. If NO → CREATE new.

### Reading Cron Prompt
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list  # Shows prompt_preview, not full prompt
# Full prompt stored in: ~/.hermes/cron/output/{job_id}/
```

### Updating Cron Prompt (ADD, not REPLACE)
```bash
# Step 1: Read current prompt from cron output
cat ~/.hermes/cron/output/{job_id}/*.md | head -100

# Step 2: Append new content to existing
# DO NOT just replace - user said "thêm" = ADD

# Step 3: Update with ADDED content
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit {job_id} --prompt "FULL PROMPT WITH NEW CONTENT ADDED"
```

### Verifying Cron Update
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list  # Check prompt_preview shows new content
ls -la ~/.hermes/cron/output/{job_id}/  # New run should appear at next scheduled time
```

## Worker Cron Jobs (FIXED 2026-05-06)

**Status: All 7 jobs FIXED.** They were running `hermes-autoresearch` instead of worker-specific prompts.

**How to fix a drifted worker cron:**
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit {job_id} --prompt "$(cat ~/.hermes/workers/{worker}/SOUL.md)" --clear-skills
```

**Verify:**
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list
# Worker jobs should show: Skills: none
```

## ⚠️ CRITICAL: Skill Override Bug

**Symptom:** Created cron with `--skills ["hermes-autoresearch"]`, but it runs skill content instead of your custom prompt.

**Root cause:** Attaching a skill to a cron causes the FULL SKILL CONTENT to be loaded into the prompt, overriding whatever you wrote.

**Fix:** When creating a cron with a custom prompt, use `--skills []` (empty array):
```bash
cronjob create --name "..." --prompt "MY CUSTOM PROMPT" --skills [] --schedule "..." ...
```

**When to use `--skills`:**
- ONLY when you want the skill to RUN (e.g., `hermes-autoresearch` skill should run its own loop)
- When you just want a prompt without any skill behavior → `--skills []`

**Verification after create:**
```bash
cronjob list  # Check Skills: should be [] or correct skill name
head -20 ~/.hermes/cron/output/{job_id}/*.md  # Should show YOUR prompt, not skill content
```

## Common Mistakes

1. **"cron update" doesn't exist** — Use `cron edit`
2. **Duplicate cron** — Created new instead of editing existing
3. **Updated skill instead of cron** — User sees no change in behavior
4. **Replaced instead of added** — "thêm" means APPEND
5. **Didn't verify** — Said "done" without checking files exist
6. **Attached skill overrides custom prompt** — Use `--skills []` for pure prompt crons

## Session Log Analysis — Where to Find Things

| What | Where |
|------|-------|
| Today's sessions | `~/Library/Application Support/hermes-agent/sessions/` |
| Cron outputs | `~/.hermes/cron/output/{job_id}/` |
| Worker outputs | `~/hermes/workers/{worker}/outputs/` |
| Daily memory | `~/hermes/workers/memory/daily/[YYYY-MM-DD].md` |
| Pending tasks | `~/hermes/workers/memory/PENDING_TASKS.md` |

## Session Log Analysis Steps

```bash
# 1. Find today's session logs
ls -lt ~/Library/Application\ Support/hermes-agent/sessions/ | head -10

# 2. Read session summaries (each session has summary field)
# Look for: decisions, revenue, learnings, blockers

# 3. Update knowledge graph
# ~/hermes/workers/memory/MEMORY.md
# ~/hermes/workers/memory/daily/[YYYY-MM-DD].md

# 4. Index extracted info
# Tag by type: product, content, technical, strategy
# Add to relevant wiki pages
```
