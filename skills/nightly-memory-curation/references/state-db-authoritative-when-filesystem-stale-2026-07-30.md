# State.db is Source of Truth — when filesystem `~/.hermes/sessions/*.jsonl` is stale

Verified failure mode in the 2026-07-30 02:00 curator pass: the `~/.hermes/sessions/*.jsonl` filesystem was **60+ days out of date** (last file 2026-05-28 10:10) but `~/.hermes/state.db` (801 MB SQLite) held all 8 sessions for 2026-07-29 02:00 → 2026-07-30 02:00 window. Without `state.db` as source of truth, the curator would have run as a **noop** (zero sessions found) and silently missed 3 substantive Telegram sessions (Mì Ý Kon Tum business plan + Vui Vẻ pilot script + 6-round voice A/B test).

## Symptom

```bash
$ ls ~/.hermes/sessions/*.jsonl | wc -l
83  # files from 2026-04-21 to 2026-05-28

$ ls ~/.hermes/sessions/*.jsonl | grep -E "2026072[89]|20260730"
# ← ZERO matches — the most recent files are 2026-05-28
```

If the curator had only trusted the filesystem, it would have written a noop entry like the 2026-07-27 one and produced 0 concept pages, 0 lessons, 0 cross-refs.

## Detection

Always run **both queries** before classifying the window:

```bash
# 1. Filesystem (may be stale)
NEW_FILES=$(find ~/.hermes/sessions -name "*.jsonl" -newermt "<window_start>" 2>/dev/null | wc -l)

# 2. state.db (authoritative if filesystem is stale)
sqlite3 ~/.hermes/state.db \
  "SELECT COUNT(*) FROM sessions WHERE datetime(started_at,'unixepoch','localtime') >= '<window_start>'
   AND datetime(started_at,'unixepoch','localtime') < '<window_end>'"
```

If `NEW_FILES == 0` BUT state.db returns sessions, the filesystem is stale and **state.db is the source of truth**.

## Verified case (2026-07-30 02:00)

- Filesystem: 0 files in window 2026-07-29 02:00 → 2026-07-30 02:00
- `state.db`: 8 sessions (3 substantive Telegram + 3 subagent verifiers + 2 cron)
- Without `state.db`: would have been a noop, missed all 3 decisions (Mì Ý Kon Tum business plan + Vui Vẻ pilot + voice config chốt)

## Why filesystem can lag state.db

`~/.hermes/sessions/*.jsonl` files appear to be written by an older path or a process that doesn't run on every session. The active session lifecycle is in `state.db` (the same DB used by the gateway for routing), so any session that doesn't go through the jsonl-writer path is invisible to filesystem queries.

`~/.hermes/sessions.db` and `~/.hermes/sessions/sessions.db` are both **0-byte files** as of 2026-07-30 — empty/stale, do not query them. The real DB is `~/.hermes/state.db`.

## Pattern (codified)

**Step 0 of every curator run: classify window based on state.db, NOT filesystem:**

```python
import sqlite3
DB = "/Users/tuananh4865/.hermes/state.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# Authoritative session list for the 24h window
sessions = con.execute("""
  SELECT id, source, title, datetime(started_at,'unixepoch','localtime') AS started,
         message_count, tool_call_count
  FROM sessions
  WHERE datetime(started_at,'unixepoch','localtime') >= ?
    AND datetime(started_at,'unixepoch','localtime') < ?
  ORDER BY started_at ASC
""", (WINDOW_START, WINDOW_END)).fetchall()
```

**Filesystem is supplementary**, used only to look for transcript files outside `state.db` (e.g. watchdog transcripts in `wiki/raw/transcripts/`).

## L-number assignment

Verified 2026-07-30: this is **NEW L80** in the user's `learned-about-tuananh.md` AND **NEW lesson in this skill** (next L after L77 in this skill's anti-pattern archive). Pattern: state.db is source of truth; filesystem `~/.hermes/sessions/*.jsonl` may be 60+ days stale; `sessions.db` files (both locations) are 0-byte and useless.

## Cross-references

- L72 in this skill's archive (re-scan state.db AFTER first synthesis) is now incomplete — combine with the new lesson to form: **state.db is required Step 0 source of truth, then re-scan after first synthesis round**.
- L74 (iCloud vault root-listing hang) — orthogonal, but uses same SQLite query engine pattern (sub-query on sub-directory).
- `~/.hermes/state.db` schema: `sessions` table has `id, source, title, started_at, message_count, tool_call_count, ...`; messages table has `session_id, role, content, timestamp` for transcript-style extraction.