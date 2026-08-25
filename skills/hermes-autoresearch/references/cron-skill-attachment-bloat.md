# Cron Skill Attachment = Output Bloat (2026-05-08)

## Problem

Cron job `5aea298eb0a8` was created with `--skills hermes-autoresearch`. When it ran, output was 45,198 bytes of raw skill content instead of the session review.

## Root Cause

When a skill is attached to a cron via `--skills`, the skill's **ENTIRE content** gets prepended to the prompt. For `hermes-autoresearch` (~900 lines), this means the actual cron prompt becomes buried and the output echoes the skill itself.

## Fix

Only attach `hermes-autoresearch` skill to crons whose **explicit purpose** is autoresearch:
- ✅ `a4b8e528983f` — 2AM Autoresearch Nightly (has skill)
- ✅ `a5c02f2f0d87` — 7AM X Research (has skill)
- ❌ `5aea298eb0a8` — 0AM Daily Session Review (NO skill — runs prompt directly)

All other cron jobs should use `--skills []` (empty array).

## Verification

| Metric | With skill | Without skill |
|--------|-----------|---------------|
| Output size | 45,198 bytes | 3,259 bytes |
| Content | Skill markdown | Actual session review |

## Lesson

**"Attach skill" ≠ "Use skill pattern"** — Attaching a skill physically loads it into the prompt context. Only attach skills when the cron is designed to perform that skill's domain of work.
