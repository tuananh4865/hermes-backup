---
name: hermes-maintenance
description: "Use when Anh asks to clean up temp files, free disk space, maintain Hermes directory, or remove old checkpoints/sessions/backups. Covers disk space audit, safe deletion, and identifying what can be cleaned."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [maintenance, disk-cleanup, hermes, temp-files, cleanup]
    related_skills: [hermes-agent, gateway-manager]
---

# Hermes Maintenance

## Overview

Regular maintenance of the Hermes working directory to reclaim disk space by removing temporary files, old session data, legacy checkpoints, and backup files created during normal operation.

**Anh's rule:** Only clean files that YOU (Hermes Agent) created. Don't touch Anh's personal files.

## When to Use

- Anh asks to "dọn dẹp", "clean up", "free disk space", "xóa file rác"
- Disk space is low and needs investigation
- Routine maintenance sessions
- After large operations that left temporary files behind

## The Maintenance Workflow

### Step 1: Audit First — Don't Delete Blindly

Before deleting anything, run a disk audit:

```bash
# Check Hermes directory size
du -sh ~/.hermes/

# List top-level contents with sizes
ls -la ~/.hermes/

# Find temp files (explicit extensions)
find ~/.hermes -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*~" -o -name "*.log" -o -name "cache_*" \) 2>/dev/null

# Check session directory (usually the biggest)
du -sh ~/.hermes/sessions/
ls ~/.hermes/sessions/ | wc -l

# Check checkpoints
du -sh ~/.hermes/checkpoints/*/

# Check logs
du -sh ~/.hermes/logs/
```

### Step 2: Categorize What You Find

Group findings into categories:

| Category | Examples | Safe to Delete? |
|----------|----------|-----------------|
| **Config backups** | `config.yaml.bak.*` | ✅ Yes — old backups from config changes |
| **Legacy checkpoints** | `checkpoints/legacy-YYYYMMDD-*/` | ✅ Yes — old session checkpoints |
| **Disk cleanup artifacts** | `disk-cleanup/cleanup.log`, `tracked.json.bak` | ✅ Yes — cleanup tracking files |
| **Old session JSONL files** | `sessions/*.jsonl` from months ago | ⚠️ Ask first — conversation history |
| **Operational logs** | `logs/gateway.log`, `logs/errors.log` | ❌ No — needed for debugging |
| **Session JSON files** | `sessions/session_*.json` | ⚠️ Keep recent — current context |
| **State databases** | `state.db`, `memory_store.db` | ❌ No — critical Hermes state |
| **DS_Store files** | `.DS_Store` scattered around | ❌ No — harmless macOS metadata |

### Step 3: Report Before Major Deletion

For anything non-trivial (>1MB total), report to Anh:
- What you found
- How much space it uses
- What you propose to delete
- Ask for confirmation before proceeding

Use Vietnamese. Be concise. State the action explicitly.

### Step 4: Execute Safe Deletions Only

**Safe to delete without asking (small, clearly temp):**
- `config.yaml.bak.*` files older than a few days
- `checkpoints/legacy-*` checkpoint folders
- `disk-cleanup/cleanup.log`, `tracked.json.bak`
- Empty marker files like `.trajectory_cleanup_flag`, `.update_check`

**Always ask first:**
- Old session `.jsonl` files (conversation history)
- Anything that might contain Anh's work or preferences
- Any folder you're unsure about

### Step 5: Verify

After deletion:
```bash
# Check Hermes directory size after cleanup
du -sh ~/.hermes/

# Verify targeted deletions succeeded
ls ~/.hermes/config.yaml.bak.* 2>/dev/null  # should be gone or fewer
```

---

## Common Pitfalls

### 1. `find -newer <date-string>` Does NOT Work on macOS

The `-newer` predicate in `find` expects a **timestamp file**, not a date string like `2025-05-01`.

**Wrong:**
```bash
find ~/.hermes/sessions/ -name "*.jsonl" ! -newer "2025-05-01" -delete
```

**Correct approaches:**
```bash
# Option A: Touch a timestamp file first
touch -t 202505010000 /tmp/cutoff
find ~/.hermes/sessions/ -name "*.jsonl" ! -newer /tmp/cutoff -delete

# Option B: Use -mtime (modification time in days)
find ~/.hermes/sessions/ -name "*.jsonl" -mtime +30 -delete

# Option C: Filter by filename date prefix directly
find ~/.hermes/sessions/ -name "*.jsonl" | grep -v "202605" | xargs rm -v
```

### 2. Deleting the Wrong Files

**NEVER delete:**
- `state.db` — critical Hermes session state
- `memory_store.db` — ByteRover persistent memory
- `.hermes_history` — conversation history index
- Any `.json` session files from the current month

**Always verify** before deleting session files:
```bash
# List recent sessions (current month)
ls -lt ~/.hermes/sessions/*.json | head -10
```

### 3. Not Checking What's Actually Big

Sessions directory can be 280MB+ with 900+ files. Old `.jsonl` files can consume 500MB+. Always run `du -sh` on the biggest directories first.

### 4. Asking Permission Incorrectly

Don't say "should I delete X or keep it?" — state what you're going to do and ask if it's OK to proceed. Example:

> "Có 3 file backup config từ ngày 15/5 (35KB). Xóa luôn không anh?"

Not:
> "Anh muốn xóa mấy file backup này hay giữ lại?"

---

## Session Cleanup Reference

Typical space breakdown in `~/.hermes/`:

| Item | Typical Size | Notes |
|------|-------------|-------|
| `sessions/` | 200-500MB | 900+ session files, many `.jsonl` |
| `state.db` | 200-300MB | **DO NOT DELETE** |
| `checkpoints/` | 10-50MB | Legacy folders safe to remove |
| `logs/` | 5-15MB | Operational, keep recent |
| `memory_store.db` | 50-100MB | **DO NOT DELETE** |
| `autoresearch/` | 50-100KB | Usually small |
| `config.yaml.bak.*` | 30-100KB total | Safe to delete old ones |
| `disk-cleanup/` | <5KB | Cleanup tracking, safe |

---

## Verification Checklist

- [ ] Ran `du -sh ~/.hermes/` before and after
- [ ] Confirmed no critical files deleted (state.db, memory_store.db)
- [ ] Reported space reclaimed to Anh
- [ ] Noted any items pending Anh's decision