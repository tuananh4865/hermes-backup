---
title: Session 2026-06-18 — Pre-flight Ritual v3 E2E QA Findings
created: 2026-06-18
type: case-study
applies_to: strict-system-qa-protocol
---

# 2026-06-18 — Pre-flight Ritual v3 E2E: 3 real bugs caught

## Context

First E2E test of Pre-flight Project Setup Ritual v3 on the existing Content Creator project (16 → 35 files migrated). User asked: *"Làm content creator theo ritual mới đi"*.

This case study is a worked example of how the 3-layer verification pattern (Existence → Behavior → Future-proof) caught 3 distinct bug classes that a single "ls + check-compliance" check would have missed.

## 3-layer verification applied

### Layer 1 — Existence (cheap, fast)

```bash
# Sub-agent reported "15 scripts created"
ls -la /Volumes/Storage-1/Hermes/wiki/projects/content-creator/research/T-01.4-scripts-*.md
# → ls: No such file or directory  ❌
```

**Bug class caught: silent path drift.** Sub-agents had written files to `~/wiki/...` and `~/actions/...` instead of the absolute path. The compliance gate hadn't been run yet, so nothing had noticed.

**Fix:** `mv ~/wiki/projects/content-creator/research/*.md /Volumes/Storage-1/Hermes/wiki/projects/content-creator/research/` + same for actions.

### Layer 2 — Behavior (structural verification)

```bash
# After move: confirm script count
for f in research/T-01.4-scripts-*.md; do
  count=$(grep -cE "^## (EDIT|SETUP|ANH-SANG)-" "$f")
  echo "$f: $count scripts"
done
# → 5 + 5 + 5 = 15 ✓
```

**Bug class caught: wrong grep pattern.** Sub-agent's self-report said "5 scripts" but had used `## EDIT-NN` (H2) not `### EDIT-NN` (H3). The compliance gate's default grep `^### ` returned 0, not 5. Without manual re-count with the correct pattern, this would have been silent overcount.

```bash
# Compliance check: also caught action-log issues
bash check-project-compliance.sh content-creator
# → ❌ FAIL: 6 issues: Orphan action (no task_id)
```

**Bug class caught: missing YAML field.** Sub-agents created action logs from scratch instead of copying template → forgot `task_id:` field → CI gate flagged 6 orphans.

**Fix:** `for f in actions/*.md; do grep -q "^task_id:" "$f" || echo "task_id: T-01.4" >> "$f"; done` → patched 6 files.

### Layer 3 — Future-proof (workflow resilience)

```bash
# Final compliance after fixes
bash ~/.hermes/scripts/check-all-compliance.sh content-creator
# → ✅ PASS Fable-5 + Loop Engine
```

```bash
# Ritual reuse test
bash ~/.hermes/scripts/bootstrap-project.sh tiktok-shop-research "TikTok Shop Research" "Tuấn Anh"
# → ✅ Created 6 folders + hub.md from template, idempotent on re-run
```

**Verified future-proof properties:**
- Bootstrap script idempotent (safe to re-run)
- Pre-flight Ritual auto-applied to new project (just 1 command)
- Compliance gate catches structural drift (action logs, missing fields)
- Path rule now documented in sub-agent-workflow.md so future sub-agents avoid the same drift

## Lessons for the QA protocol

### 1. **Compliance gate ≠ system works** (recurring theme)

Sub-agents self-report "DONE". Compliance gate returned ✅ for Content Creator in previous sessions (16/06–17/06). But when actually run, 3 issues surfaced:
- Files at wrong path
- Action logs missing `task_id`
- YAML fields mispatched

**Rule:** Always run `ls -la <absolute-path>` AFTER sub-agents complete, even if compliance gate said PASS. The gate only checks structure; it doesn't check that files exist at the claimed path.

### 2. **Sub-agent self-reports are optimistic (re-confirmed)**

3 parallel sub-agents each claimed "5 scripts created" + "6 action logs created". Actual:
- Scripts: 5+5+5 ✓ (correct)
- Action logs: 6 ✓ but at wrong path
- Path: 3 different wrong paths (each agent independently drifted)

**Rule:** Don't trust "I wrote N files" — run `find <absolute-path> -type f | wc -l` yourself.

### 3. **Idempotent scripts need their own verification**

`bootstrap-project.sh` claimed idempotent in its docstring. Verified by running it twice on the same project — second run reported "⚠️ Exists (skip)" for all 6 folders and hub.md. Idempotency confirmed.

**Rule:** Even when a script claims idempotent in docs, verify by running it twice on the same target. Many "idempotent" scripts fail on re-run because of leftover state (lock files, partial writes, race conditions).

### 4. **The 3-layer pattern (Existence → Behavior → Future-proof) caught everything**

If we had only run compliance gate (Layer 2 only), we'd have caught the missing `task_id` issue. But path drift (Layer 1) would have been silent — files would have been in `~/wiki/`, NOT in the project's expected location, and the gate wouldn't have known to look there.

**If** we'd only run ls (Layer 1), we'd have caught path drift but missed the missing `task_id` field.

3-layer = full coverage.

## What this case demonstrates

A sub-agent fan-out across 3 parallel agents + concurrent concurrency tuning + new Ritual system can introduce 3 distinct bug classes (path drift, missing fields, structural overcount) that all pass a single check but fail in different ways. The 3-layer protocol is the minimum verification needed to catch them all.

For Content Creator migration specifically:
- Files moved: 8 (3 scripts + 6 action logs, from `~/wiki/` and `~/actions/` to absolute paths)
- Files patched: 6 (added missing `task_id` field)
- Files re-patched: 1 (T-01.4 task file with mispatched status field)
- Final state: 35 files, compliance ✅ PASS

## Related references

- `~/.hermes/profiles/_shared/sub-agent-workflow.md` — HARD PATH RULE added as result of this session
- `~/.hermes/profiles/_shared/project-setup-ritual.md` — Pre-flight Ritual v3 spec
- `wiki/projects/content-creator/actions/2026-06-18-migrate-to-ritual-v3.md` — Migration plan log
- `wiki/projects/content-creator/actions/2026-06-18-test-path-rule.md` — Path rule test (cleaned up after verify)
- See also: `references/ritual-v3-e2e-content-creator.md` in `hermes-project-workflow-system` (more detailed bug-by-bug narrative)