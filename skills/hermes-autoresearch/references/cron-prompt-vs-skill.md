# Cron Prompt vs Skill — CRITICAL DISTINCTION

## The Problem (2026-05-06 Session)

User said "Thêm nội dung vào cron 2AM" (Add content to cron 2AM). Agent:
1. Updated the SKILL instead of the CRON PROMPT
2. User got frustrated because cron still ran old content
3. User had to explicitly say "wtf are you doing" before agent fixed cron

## The Core Rule

| User says... | Agent must use... | Tool |
|--------------|-------------------|------|
| "add to cron" | CRON prompt | `cronjob update --job_id X --prompt "..."` |
| "update skill" | SKILL | `skill_manage patch` |

**They are DIFFERENT with DIFFERENT tools.**

## Why This Matters

- **Skill** = PATTERN/DOCUMENTATION — describes general behavior
- **Cron prompt** = WHAT ACTUALLY RUNS — specific instructions at scheduled time

Updating skill does NOT change what cron executes. User controls cron prompts directly.

## "Add" Means APPEND

User said "Thêm nội dung bên dưới vào cron lúc 2AM" and "Giữ cái cũ và thêm nội dung"

This means:
1. Read current cron prompt (`cronjob list` → look at `prompt_preview`)
2. APPEND new content to existing
3. Never REPLACE unless user explicitly says "thay thế"

## Verification Steps

After ANY cron update:
```bash
cronjob list  # Confirm: same job count, new content visible in prompt_preview
```

## Cron Job IDs (as of 2026-05-08)

| ID | Name | Schedule | Skill |
|----|------|----------|-------|
| a4b8e528983f | Autoresearch Nightly | 2AM | hermes-autoresearch |
| 7cba6ba5f52a | Daily Backup | 3AM | none |
| a5c02f2f0d87 | X Research Daily | 7AM | hermes-autoresearch |
| ce3701b4dcdd | Content Creator Morning | 8AM | none |
| e4fb0c36e9f7 | Research Analyst Morning | 8:30AM | none |
| 045a44210a59 | Orchestrator Briefing | 9AM | none |
| f1584a9a1d86 | Orchestrator Agent Monitor | every 2h | none |
| 50bc2c2dfbb3 | Content Creator Evening | 6PM | none |
| 1c425ba42980 | Research Analyst Evening | 6:30PM | none |
| fc2191d508a3 | Orchestrator Nightly | 9PM | none |
| 5aea298eb0a8 | Daily Session Review | 0AM | none |

## Quick Reference

```bash
# List all cron jobs
cronjob list

# Get specific job prompt
# → Use prompt_preview from list output

# Update cron prompt (append to existing)
cronjob update --job_id a4b8e528983f --prompt "EXISTING_CONTENT + NEW_CONTENT"

# Update skill
skill_manage patch --name hermes-autoresearch --old_string "OLD" --new_string "NEW"
```
