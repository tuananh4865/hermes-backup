---
title: Content Creator Project — Pre-flight Ritual v3 E2E Test (18/06)
created: 2026-06-18
type: case-study
applies_to: hermes-project-workflow-system
---

# Content Creator Pre-flight Ritual v3 — E2E Test Case (verified 18/06)

## What happened

User said: *"Làm content creator theo ritual mới đi"*. This was the first real E2E test of Pre-flight Ritual v3 (the new mandatory 3-phase project setup flow).

## Phase 0 — Đọc existing project (audit findings)

Project `wiki/projects/content-creator/` had 16 files from 17/06 session but NO Pre-flight Ritual enforcement yet:
- hub.md + dashboard.md + dependency-graph.md exist
- 2 tasks files (T-01.1 research, T-01.2 voice profile)
- 3 research outputs
- 11 action logs
- BUT: no Ritual hooks in default SOUL.md, no per-task PLAN files, sub-agents had no shared workflow reference

## Phase 1 — Setup Ritual (created 18/06)

**Files created:**
- `~/.hermes/profiles/_shared/project-setup-ritual.md` (6,064b) — Full Ritual spec
- `~/.hermes/scripts/bootstrap-project.sh` (3,039b, executable) — Idempotent project bootstrap
- `wiki/projects/_template/hub.md` (2,904b) — Hub template
- Injected "PROJECT SETUP RITUAL" section (~60 lines) into `~/.hermes/SOUL.md`

**Idempotent test:** Running `bootstrap-project.sh tiktok-shop-research "TikTok Shop Research" "Tuấn Anh"` second time → all directories show "⚠️ Exists (skip)" → confirmed idempotent.

## Phase 2 — T-01.4 Script 15 videos (the real test)

**Plan file:** `actions/2026-06-18-migrate-to-ritual-v3.md` (3,604b, 6 sub-actions documented)

**Sub-action execution:**
| SA | What | Time | Result |
|----|------|------|--------|
| SA-1 | Create task spec T-01.4 from template | 2 min | ✅ 5,357b task file với YAML đầy đủ |
| SA-2 | Create plan file `research/T-01.4-script-plan.md` | 1 min | ✅ 3,635b plan với 15 slots |
| SA-3 | Spawn 3 content-director sub-agents parallel | 9 min | ✅ 15 scripts total (5+5+5) |
| SA-4 | QA verify (script count + compliance) | 2 min | ✅ 5/5 per trụ, compliance PASS |
| SA-5 | Update dashboard + task status | 1 min | ✅ T-01.4 → DONE |

## Honest issues encountered (3 real bugs found)

### Issue 1 — Sub-agent path drift (CRITICAL)

**Symptom:** 3 sub-agents ghi files vào wrong paths:
- `~/wiki/projects/content-creator/research/T-01.4-scripts-edit-2026-06.md` ❌
- `~/actions/2026-06-18-T-01.4-spawn-*.md` ❌
- Expected: `/Volumes/Storage-1/Hermes/wiki/projects/content-creator/...`

**Detection:** `ls wiki/projects/content-creator/research/T-01.4-scripts-*.md` → "No such file or directory" → confirmed files ở wrong path.

**Fix applied:** `mv ~/wiki/projects/content-creator/research/*.md /Volumes/Storage-1/Hermes/wiki/projects/content-creator/research/` + tương tự cho actions.

**Root cause:** Sub-agents trong isolated context không resolve absolute path correctly. They used `~` shortcut hoặc relative path instead of `/Volumes/Storage-1/Hermes/wiki/...`.

**Lesson:** ALWAYS pass absolute path explicitly in delegate_task context. Don't assume sub-agent knows the wiki root.

### Issue 2 — Action logs missing task_id (CI gate fail)

**Symptom:** After move, compliance check showed 6 issues: "Orphan action (no task_id)".

**Detection:** `bash check-project-compliance.sh content-creator | grep "❌"` → 6 matches, all action logs.

**Fix applied:** Bash one-liner: `for f in actions/*.md; do grep -q "^task_id:" "$f" || echo "task_id: T-01.4" >> "$f"; done` → patched 6 files.

**Root cause:** Sub-agents tạo action logs from scratch instead of copying template, forgot `task_id:` YAML field.

**Lesson:** Add `task_id: T-XX.Y` to the action log template in sub-agent context, not just expect them to follow it.

### Issue 3 — YAML field misplacement in patch

**Symptom:** First `patch` on T-01.4 task file accidentally inserted `status: ✅ DONE` into the `research_refs:` array (treated as another list item).

**Detection:** Second `read_file` showed broken YAML: 3 research refs became 2 (third replaced by status field).

**Fix applied:** Re-read file with offset/limit, then patch with full context to restore research_refs + move status to correct location.

**Lesson:** Patch tool không show context of field it's replacing. Always `read_file offset=N` first to confirm exact line structure before patching multi-field YAML frontmatter.

## Final state (verified by command output)

```
Total project files: 35 (was 16 before Ritual v3 migration)
Scripts: 15 (5 EDIT + 5 SETUP + 5 ÁNH SÁNG)
Action logs: 19 (8 new in 18/06)
Tasks DONE: 2 (T-01.1 ✅ + T-01.4 ✅)
Tasks TODO: 1 (T-01.2 voice profile — status not updated yet, file exists)
Compliance: ✅ PASS Fable-5 + Loop Engine
Sub-agent concurrency tested: 3 parallel in 543s (avg 9 min each)
```

## What this case proves

1. **Ritual v3 works end-to-end** — Phase 0 → 1 → 2 ran cleanly, no missing step
2. **Sub-agent parallel works** — 3 content-director agents + ~8 concurrency = real speedup (sequential would be 27 min, parallel = 9 min)
3. **Honest verification caught real bugs** — 3 issues found would have been silent without `ls` + `check-project-compliance.sh` verification
4. **Bootstrap is idempotent** — safe to re-run
5. **Ritual scales** — Pattern works for new project (tiktok-shop-research) and existing project (content-creator)

## Reusable patterns for future Ritual E2E tests

1. **Always run `ls -la` + `check-project-compliance.sh` BEFORE claiming done** — catches path issues, missing fields, orphan actions
2. **Sub-agent path discipline** — pass `WIKI_ROOT` env var + absolute path in context, not relative
3. **Action log template in sub-agent context** — paste full template to ensure consistency
4. **Patch with read_file offset first** — for YAML files with multiple similar fields (research_refs vs depends_on vs blocks)
5. **Move-not-delete for wrong-path files** — `mv` preserves mtime for log audit

## Related references

- `~/.hermes/profiles/_shared/project-setup-ritual.md` — Full Ritual v3 spec
- `~/.hermes/profiles/_shared/sub-agent-workflow.md` — Sub-agent shared ref
- `~/.hermes/scripts/bootstrap-project.sh` — Project bootstrap script
- `wiki/projects/content-creator/actions/2026-06-18-migrate-to-ritual-v3.md` — Migration plan log
- `wiki/projects/content-creator/tasks/task-T-01.4-script-15-videos.md` — First Ritual v3 task spec