# False-Positive Triage Recipes (H5/H10 codified)

Patterns that look like pending tasks/handoffs but are static documentation.

## H5 — `pending*` File Matches

`find ~/.hermes/profiles -type f -name "pending*"` returns:

### FALSE POSITIVE: `coder/skills/hermes-github-backup/references/wiki-independence-pending.md`

- **Path:** under `skills/*/references/` → static ref doc indicator
- **mtime:** 2026-05-18 (>30 days old)
- **Content:** "Operation Status: PENDING EXECUTION" but is documentation about wiki independence migration, NOT an active handoff
- **Triage:** FALSE POSITIVE per H5 recipe

**Rule:** If path matches `skills/*/references/*` AND mtime >30 days AND content is documentation-style (mentions "status: pending" as part of narrative) → FALSE POSITIVE.

## H10 — `handoff` Directory Matches

`find ~/.hermes/profiles -type d \( -name "pending*" -o -name "handoff*" -o -name "inbox" -o -name "queue" \)` returns:

### FALSE POSITIVE: `coder/skills/handoff/`

- **Path:** under `skills/handoff/` → static skill bundle directory
- **Contents:** only `SKILL.md` (mtime 2026-05-19, static skill definition)
- **NOT a task queue:** No subdirectories per task, no JSON/YAML handoff manifests
- **Triage:** FALSE POSITIVE per H10 directory branch

**Rule:** If directory matches `skills/*/handoff/` OR `skills/*/pending/` AND contains only `.md` files (no handoff manifests, no per-task subdirs) AND mtime >30 days → FALSE POSITIVE.

## Real Handoff Indicators

A REAL pending task or handoff would have:
- JSON/YAML manifest files (not just `.md`)
- Per-task subdirectories with timestamps matching recent activity
- Active file mtimes (within 24h)
- References to specific task IDs or goals

If ALL 4 indicators are absent → FALSE POSITIVE.

## Triage Decision Tree

```
Match found → Is path under skills/*/references/ or skills/*/handoff/?
  ├─ YES → Check mtime
  │   ├─ >30 days → FALSE POSITIVE
  │   └─ <30 days → Investigate content
  └─ NO → Check content type
      ├─ Documentation (.md with narrative text) → FALSE POSITIVE
      ├─ Manifest (.json/.yaml with task IDs) → INVESTIGATE
      └─ Binary/script → INVESTIGATE
```

## Audit Recommendation

Always run the full `find` scan, but apply triage BEFORE counting matches in the "Pending QA" metric. An audit that reports 1 pending without triage is misleading.
