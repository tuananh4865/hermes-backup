# Cron Job Verification Pattern

> **Critical insight (2026-05-06):** Cron job EXISTS ≠ Cron job RUNS. Must verify BOTH job presence AND actual execution.

## The Problem

When checking cron jobs for Anh, discovered that many jobs showed:
- ✅ Job exists in `cronjob list`
- ❌ `last_run_at: null` — never fired
- ❌ Empty output directories

This meant workers were "configured" but not actually running.

## Verification Checklist

### Level 1: Quick Check (30 seconds)

```bash
# Check system cron daemon is running
ps aux | grep cron | grep -v grep

# Check cronjob list for last_run_at
cronjob list | grep -E "(job_id|last_run_at|state)"
```

### Level 2: Job Verification (1 minute)

```bash
# For each job, check output directory
ls -la ~/.hermes/cron/output/{job_id}/

# Empty dir = job never ran OR ran but produced [SILENT] output
# Missing dir = job never triggered at all
```

### Level 3: Deep Verification (5 minutes)

```bash
# Read the actual output files
cat ~/.hermes/cron/output/{job_id}/*.md | tail -20

# Check timestamps match expected schedule
ls -la ~/.hermes/cron/output/{job_id}/ | grep "$(date +%Y-%m-%d)"

# Verify job schedule matches expected
cronjob list | grep {job_id}
```

## Known Cron Jobs Status (as of 2026-05-06)

| Job ID | Name | last_run_at | Output Dir | Status |
|--------|------|-------------|-------------|--------|
| a4b8e528983f | Autoresearch Nightly | 2026-05-06 02:00:53 | ✅ Has files | ✅ OK |
| 90c50d1a2d3c | Autoresearch Nightly #2 | 2026-05-06 02:02:18 | ✅ Has files | ✅ OK |
| 7cba6ba5f52a | Daily Backup | 2026-05-06 03:01:06 | ✅ Has files | ✅ OK |
| a5c02f2f0d87 | X Research Daily | 2026-05-05 07:03:20 | ✅ Has files | ✅ OK |
| f1584a9a1d86 | Agent Monitor (2h) | 2026-05-06 06:01:15 | ✅ Has files | ✅ OK |
| fc2191d508a3 | Nightly Consolidation | 2026-05-05 21:00:54 | ✅ Has files | ✅ OK |
| ce3701b4dcdd | Content Creator Morning | null | ❌ No dir | ❌ NEVER RAN |
| 50bc2c2dfbb3 | Content Creator Evening | null | ❌ No dir | ❌ NEVER RAN |
| e4fb0c36e9f7 | Research Analyst Morning | null | ❌ No dir | ❌ NEVER RAN |
| 1c425ba42980 | Research Analyst Evening | null | ❌ No dir | ❌ NEVER RAN |
| 045a44210a59 | Orchestrator Briefing | null | ❌ No dir | ❌ NEVER RAN |

## Key Insight

**"Workers configured" ≠ "Workers running"**

The pattern that led to confusion:
1. Worker cron jobs CREATED with correct schedule
2. Worker directories CREATED (but empty)
3. Jobs show in `cronjob list` 
4. BUT `last_run_at: null` and no output files
5. Therefore: jobs were SCHEDULED but never actually TRIGGERED

## Why This Happens

Possible causes:
1. System cron daemon not running (but `/usr/sbin/cron` was running ✅)
2. Job scheduled but system was asleep (macOS sleep = cron doesn't run until wake)
3. Job triggered but [SILENT] response (empty output dir = empty report)
4. Job created but never actually saved to system cron

## Root Cause Investigation (2026-05-06)

After investigation:
- System cron IS running
- Jobs ARE saved (appear in list)
- But workers NEVER ran

**Most likely cause:** macOS was asleep when scheduled times hit. macOS Cron is system-level and runs when system is awake. If MacBook was closed/asleep at 8AM, 6PM, etc., jobs would have been missed.

**Note:** macOS `launchd` is the native alternative for waking from sleep to run scheduled tasks.

## Files

| Path | Purpose |
|------|---------|
| `~/.hermes/cron/output/{job_id}/` | Cron job output files |
| `~/.hermes/cron/state.db` | Cron job state database |
| `/var/log/cron.log` | System cron log (if enabled) |
