---
name: hermes-project-workflow-system
description: Setup and maintain a multi-week project workflow inside Hermes — canonical folder structure, 6-step Loop Engine v2.3, action-level logging, project dashboards, CI compliance gates, and full wiring into default SOUL + sub-agent SOULs + session auto-log hooks. Load when user wants to manage long-running projects with tasks, phases, dependencies, and per-action audit trails.
version: 2.6.0
metadata:
  hermes:
    related_skills:
      - project-workflow-loop-engine
      - multi-agent-orchestrator
      - hermes-agent-decision-guard
    pitfall_warnings:
      - "Patch tool refuses to modify ~/.hermes/config.yaml — use `hermes config set` CLI instead"
      - "Hook fires on `agent:end`, NOT `on_session_end` (gateway vs hook layer)"
      - "Bash heredoc với variable interpolation fails in hook wrappers — use env vars + stdin"
      - "Skill `tiktok-viral-script` does NOT exist — substitute `tiktok-competitor-deep-analysis` + log honestly"
      - "Reopen project: RE-VERIFY existing scripts against LATEST user preferences (voice + value rule) — sessions may drift"
      - "Action log field is `task_id:` not `task:` — CI gate checks only `task_id`"
      - "Sub-agent sibling write works (timeout + sibling saves) — don't retry, verify batch rồi patch gaps"
---

# Hermes Project Workflow System

> **Class-level skill:** Setup a multi-week project workflow inside Hermes so every session + sub-agent knows exactly what to do, where to save outputs, and how to log every small action for Tuấn Anh's audit.

## When to use this skill

- User says: "setup workflow", "tạo project mới", "quản lý dự án nhiều ngày", "tôi cần workflow để biết task nào ở đâu/when/who", "log mọi action nhỏ"
- Trigger: any project that will last >2 weeks with >3 tasks
- Skip: 1-shot tasks, quick Q&A, single-file edits → use Fable-5 only

## Core architecture (4-piece enforcement)

```
1. Shared reference files  → single source of truth
2. Per-agent SOUL patches   → inject compact ref into each profile
3. CI compliance scripts   → enforce at session/audit time
4. Auto-log hooks          → capture every session end
```

Skip any piece and the system breaks within 1-2 weeks. All 4 must be wired.

## Canonical folder structure

```
/Volumes/Storage-1/Hermes/wiki/projects/
├── _template/                          # MANDATORY: starter files
│   └── task.md                         # Task template v2.2+
└── {project_id}/                       # One folder per project
    ├── hub.md                          # Read FIRST (project overview)
    ├── dashboard.md                    # Live status (orchestrator view)
    ├── dependency-graph.md             # Task → task mapping
    ├── phases/
    │   └── phase-{NN}-{name}.md        # Major milestones
    ├── tasks/
    │   └── task-{T-NN.M}-{name}.md     # One file per task
    ├── research/                       # Research outputs (YAML frontmatter required)
    │   └── T-{NN.M}-{topic}.md
    ├── actions/                        # Granular action logs (one per tool call)
    │   └── {YYYY-MM-DD}-{T-NN.M}-{action-id}.md
    └── logs/                           # Auto-populated by session-auto-log hook
        └── {YYYY-MM-DD}-sessions.md
```

## 6-step Loop Engine v2.3 (every task follows this)

```
Step 0: RESEARCH     → Read hub.md + related tasks + load skills
Step 1: PLAN         → Use _template/task.md; declare deliverables + verify criteria
Step 1.5: RESEARCH   → OPTIONAL: verify approach before execute (decision-point heavy)
Step 2: EXECUTE      → Log EVERY action to actions/ folder + save outputs to research/
Step 3: VERIFY       → Run CI compliance script + manual review
Step 4: NEXT         → Update dashboard + unblock downstream tasks
```

Retry policy v2.2: Step 6 fail → loop from Step 3, max 3 attempts → escalate orchestrator.

## Pre-flight Ritual (v3, added 18/06 — MANDATORY before project work)

**Trigger:** Any of these user messages requires running the ritual FIRST:
- "làm project X" / "tạo project X" → Phase 1 (setup) + Phase 2 (per task)
- "mở lại project X" / "tiếp tục project X" → Phase 0 (đọc) + Phase 2 (per task)
- "task T-X.Y" / "làm task X trong project Y" → Phase 2 only
- "research về Z" / "tìm hiểu về Z" → Phase 1 mini + Phase 2 (research task)
- Quick Q&A / 1-shot → SKIP ritual

**Phase 0 — Đọc existing project** (always first):
1. `ls wiki/projects/{project_id}/` — confirm structure exists
2. `cat hub.md` — read north star, team, current state
3. `cat dashboard.md` — read live status (if exists)
4. `cat dependency-graph.md` — read task deps (if exists)
5. List `tasks/`, `research/`, `actions/`, `logs/` — know what's done vs pending
6. Identify gaps: what's TODO? what's BLOCKED? what depends on what?

**Phase 1 — Setup new project** (use `bootstrap-project.sh`):
1. `bash ~/.hermes/scripts/bootstrap-project.sh {project_id} "{Name}" "{owner}"`
2. Fill `hub.md` template (north star, team, success metrics)
3. Create `phase-01-{name}.md` with timeline + KPIs
4. Run `bash check-project-compliance.sh {project_id}` to confirm structure

**Phase 2 — Per-task checklist** (before EVERY task execution):
1. RESEARCH — read task spec + research_refs + related tasks + load skill
2. PLAN — break into 3-7 sub-actions, identify blockers + risks
3. SETUP LOG — write `actions/{date}-{T-NN.M}-setup.md` with the plan
4. EXECUTE — each sub-action = 1 log file in `actions/`
5. VERIFY — self-check + run compliance + update dashboard
6. NEXT — update task status → DONE, unblock downstream

Full spec at `~/.hermes/profiles/_shared/project-setup-ritual.md` (shared reference for default + sub-agents). Auto-injected into default SOUL.md "PROJECT SETUP RITUAL" section.

**Hard rule:** Sub-agents (coder, research-lead, content-director, qa-agent, etc.) MUST load this shared reference file before executing any project task.

## Task file HARD requirements (CI gate enforces)

Every task file MUST have:
- `owner_role` field (ai chịu trách nhiệm)
- `research_refs` field (v2.1: list of research inputs)
- `verify_attempts` field (v2.2: retry counter)
- `last_failure_reason` field (v2.2: specific failure detail)
- `escalated_at` field (v2.2: timestamp when escalated)
- `depends_on` + `blocks` fields (dependency graph)
- ≥2 `[[wikilinks]]` in body
- YAML frontmatter (title, created, updated, type, tags, confidence, relationships)

## Research file HARD requirements

- YAML frontmatter đầy đủ 7 fields
- Voice: "mình"/"bạn" (research output) — NOT "anh + mấy con vợ" (banned 13/06)
- Citations: title + URL + date (every source)
- Per-item source counts (slang ≥10, sounds ≥5 — depends on task spec)
- ≥2 wikilinks in body

## Action log file template

```markdown
---
title: {action description}
created: {YYYY-MM-DD}
type: action-log
tags: [action-log, {T-NN.M}, {project_id}]
project_id: {project_id}
phase_id: {phase_id}
task_id: {T-NN.M}
agent_role: {your-role}
---

# {YYYY-MM-DD}-{T-NN.M}-{action-id}

## Context
Tại sao làm action này? Reference đến task nào?

## Action
Mô tả cụ thể hành động đã làm (≥50 từ).

## Result
Output / finding / decision.

## Next
Bước tiếp theo (nếu có).
```

## CI compliance scripts (3 layers)

```bash
# Layer 1: Fable-5 mandate (shared reference compliance)
bash ~/.hermes/scripts/check-fable5-compliance.sh

# Layer 2: Loop Engine (project workflow compliance)
bash ~/.hermes/scripts/check-project-compliance.sh {project_id}

# Layer 3: Unified (both must pass)
bash ~/.hermes/scripts/check-all-compliance.sh {project_id}
```

## Wiring checklist (7 layers — verified 17/06 pattern)

When setting up workflow for a new project, wire ALL 7 layers:

- [ ] **L1** Default SOUL.md — inject "PROJECT WORKFLOW SYSTEM" section (~90 lines)
- [ ] **L2** Shared sub-agent reference file at `~/.hermes/profiles/_shared/sub-agent-workflow.md`
- [ ] **L3** Sub-agent SOUL.md patches: coder + research-lead + content-director (+ any other active roles)
- [ ] **L4** CI compliance scripts exist + idempotent
- [ ] **L5** Hook wrapper for session-auto-log at `~/.hermes/hooks/{hook-name}/hook_wrapper.sh` (executable)
- [ ] **L6** Hook tested manually — verify per-project logs file populated
- [ ] **L7** Dashboard updated with "Workflow System Wiring" section showing all 7 layers status

## Common pitfalls (learned 17/06 from real session, expanded 23/06)

### 🚨 Pitfall #0 (NEW 23/06) — Setup project as single `.md` file instead of folder

**Symptom:** Agent creates `wiki/projects/{project_id}.md` as a single hub file, skipping the proper folder structure (hub.md + dashboard.md + dependency-graph.md + phases/ + tasks/ + research/ + actions/ + logs/). Then `check-project-compliance.sh {project_id}` either fails or silently reports a misleading "0 issues" because the project_id resolves to the wrong path.

**Root cause:** Agent remembers writing a single hub file pattern from earlier projects and skips running `init-project.sh` / `bootstrap-project.sh` (or runs them but they conflict with the pre-existing single file).

**Real session 2026-06-23:** Anh caught this when reviewing `mini-rpg-games` — em đã setup thành 1 file `.md` duy nhất, violating Fable-5 mandate + Loop Engineering. Anh's message: *"Có vẻ em quên mất không áp dụng fable 5 system và loop engineering vào rồi đúng không?"*

**Fix:**
1. **NEVER start project work without first running:**
   ```bash
   bash ~/.hermes/scripts/check-init-compliance.sh        # 8/8 system-level
   bash ~/.hermes/scripts/resume-project.sh {project_id} # load context
   ```
2. If `wiki/projects/{project_id}.md` exists (single file), **convert to folder immediately**:
   ```bash
   mv wiki/projects/{project_id}.md wiki/projects/{project_id}/_backup_old_hub.md
   mkdir -p wiki/projects/{project_id}/{phases,tasks,research,actions,logs,decisions}
   # Re-create proper hub.md + dashboard.md + dependency-graph.md
   ```
3. Run `bash ~/.hermes/scripts/check-project-compliance.sh {project_id}` BEFORE announcing done — must see `✅ PASS`.

**Lesson:** Setup script lười biếng = workflow system bị bypass silently. Always verify sau setup.

1. **`tiktok-viral-script` skill not found** — Some project specs reference skills that don't exist in `~/.hermes/skills/`. Always `ls ~/.hermes/skills/` first; if missing, substitute with closest matching skill + log the substitution honestly.

2. **Hook event mismatch** — `session-auto-log` handler.py checks `if event_type != "agent:end": return`. Wrappers MUST pass `agent:end`, not `on_session_end`. Test before declaring hook works.

3. **Wikilinks literal missing** — Sub-agents put wikilinks only in YAML `relationships:` array, not in body `[[...]]`. CI gate fails. Fix: add `> **Related pages:** [[...]] · [[...]]` blockquote after intro.

4. **Source date freshness** — Spec says ≤30 days but research only finds 60-day sources. Don't fake — disclose transparent in YAML + propose policy (default: 60-day window for trend research, override 30 days for time-sensitive content).

5. **Voice rule conflict** — `phase-01-foundation.md` says "use 'các bạn'" but learned-about-tuananh.md (13/06 update) bans "các bạn". Follow LATEST user preference → research files use "mình/bạn".

6. **Per-project log file rotates daily** — Hook creates new `{YYYY-MM-DD}-sessions.md` each day at midnight (Vietnam time). Tests during day rollover may appear to "fail" — check the correct date file.

7. **Sub-agent ghi sai absolute path** (verified 18/06, Ritual v3 E2E) — Khi delegate 3 content-director sub-agent song song để viết scripts, tất cả 3 agents ghi files vào `~/wiki/...` và `~/actions/` thay vì `/Volumes/Storage-1/Hermes/wiki/...`. Parent phải detect và move files về đúng path. **Fix:** Always specify absolute path trong `context` field của `delegate_task`: `"wiki/projects/{id}/research/T-01.4-scripts-{pillar}.md"` thay vì relative path. Verify sau khi sub-agent xong bằng `ls -la {absolute_path}/`.

8. **Action logs thiếu `task_id` field** (verified 18/06) — Sub-agent tạo action logs nhưng bỏ sót YAML field `task_id:`, làm CI gate fail với "Orphan action (no task_id)". **Fix:** Trong task spec hoặc context của sub-agent, paste luôn action log template có `task_id: {T-NN.M}` để agent copy. Hoặc parent chạy post-process: `for f in actions/*.md; do grep -q "^task_id:" "$f" || echo "task_id: T-XX.Y" >> "$f"; done`.

9. **YAML field misplacement khi patch** (verified 18/06) — Khi patch task file update `status:`, dễ patch nhầm vào `research_refs:` array (vì field position ambiguous). **Fix:** Always read file trước với `read_file offset` để biết chính xác field structure, rồi patch với context đầy đủ (kèm field name ở dòng trước).

10. **Voice + value-rule drift trên content scripts cũ** (verified 18/06, 2nd pass) — Khi reopen project, nếu scripts (research/T-XX-scripts-*.md) đã tồn tại từ session trước mà user đã update preferences sau đó, scripts có thể vi phạm. Ví dụ: 13/06 đổi voice "anh + mấy con vợ" → "mình + bạn" + 45-day value rule (0% bán hàng), nhưng scripts từ 18/06 sáng vẫn dùng "mấy con vợ" 66 lần + CTA "Mua ủng hộ anh" 23 lần. **Fix:** Sau khi check project (Phase 0), chạy thêm grep audit trên TẤT CẢ content files (research/, scripts/):
    ```bash
    # Voice check (sau 13/06: bỏ "mấy con vợ", "anh + mấy", "các bạn")
    grep -nE "mấy con vợ|anh + mấy|các bạn" wiki/projects/{id}/research/*.md

    # Value rule check (45 ngày đầu: 0% bán hàng)
    grep -nE "Mua.*ủng hộ|Mua.*combo|preset.*bán|link.*bio" wiki/projects/{id}/research/*.md

    # Banned phrases (độc lập với voice)
    grep -nE "To6|quất một phát|đỉnh nóc kịch trần" wiki/projects/{id}/research/*.md
    ```
    Nếu có match → REWRITE scripts (không patch nhỏ) với sub-agent parallel. Voice: dùng "mình"/"bạn", CTA = specific action (nhớ "Bắt đầu bằng cách", "Hãy thử"), banned list dùng semantic tokens (vd: `to6-phrase`, `quat-mot-phat-phrase`) để YAML frontmatter vẫn audit được mà grep strict pass.

11. **Sub-agent sibling write protection** (verified 18/06) — Khi 1 sub-agent trong batch `delegate_task` timeout, sibling agents có thể save files của nhau (cùng mtime, cùng project context). Pattern này OK và an toàn. **Anti-pattern cần tránh:** parent retry ngay sub-agent timeout trong cùng batch — risk double-write + waste tokens. Thay vào đó: đợi batch complete → parent verify tất cả files → fix gaps manually bằng patch (chính xác, targeted).

12. **`task:` vs `task_id:` field name** (verified 18/06) — Sub-agent tạo action logs dùng field `task: T-01.4` thay vì `task_id: T-01.4` (CI gate chỉ check `task_id`). **Fix nhanh:**
    ```bash
    for f in wiki/projects/{id}/actions/*.md; do
      grep -q "^task_id:" "$f" || sed -i '' 's/^task: \(T-[0-9.]*\)$/task_id: \1\ntask: \1/' "$f"
    done
    ```
    Hoặc tốt hơn: trong sub-agent context, paste exact action log template với `task_id:` để agent copy.

## Sub-agent role guidance

When delegating to sub-agents via `delegate_task`:
- Default role = `"leaf"` (focused worker, returns summary)
- `"orchestrator"` role requires `max_spawn_depth` increase in config — usually not needed
- Pass project context in `context` field (sub-agents have NO memory of your conversation)
- Tell sub-agent to load `~/.hermes/profiles/_shared/sub-agent-workflow.md` before acting
- Always include language directive: "Respond in Vietnamese" if relevant

## Sub-agent concurrency tuning (Tuấn Anh mandate 18/06)

Default `max_concurrent_children = 3`. For long/heavy parallel projects (Content Creator 3-trụ, multi-research, batch builds), raise to **8** sweet spot:

```bash
hermes config set delegation.max_concurrent_children 8
hermes config set delegation.subagent_auto_approve true   # Avoid manual approve bottleneck
hermes config set delegation.max_spawn_depth 1           # Keep flat, no orchestrator chain
```

Trade-off matrix + verified sweet spot for Content Creator: see `references/hermes-config-quirks.md`.

**Anti-pattern:** Setting >12 → context flood on parent thread, API cost spikes.
**Verify:** After tuning, dispatch 3+ parallel sub-agents and check total time ≈ max(individual), not sum.

## Config security guard (Hermes quirk)

**`patch` tool refuses to modify `~/.hermes/config.yaml`** (security guard):
```
Refusing to write to Hermes config file: ... Agent cannot modify security-sensitive configuration.
```

**Fix:** Always use `hermes config set <key> <value>` CLI for Hermes config. Use `patch` only for project files (SOUL.md, scripts, etc.).

See `references/hermes-config-quirks.md` for full Hermes quirks inventory (hook event names, wrapper bash heredoc pitfalls, skill drift).

## Verification pattern (Tuấn Anh's #1 preference)

Always close with evidence:
- File path(s) absolute + byte size
- grep/wc/ls output (raw command results)
- CI gate exit code + summary line
- Honest report of what didn't work + workaround applied

Anti-pattern: "xong rồi" without showing the proof.

## Related files (created 17/06 verified)

- `~/.hermes/profiles/_shared/fable5-patterns.md` — Fable-5 mandate (cốt lõi)
- `~/.hermes/profiles/_shared/project-loop-engine.md` — Loop Engine v2.3 (vũ khí)
- `~/.hermes/profiles/_shared/sub-agent-workflow.md` — Sub-agent shared ref
- `~/.hermes/scripts/check-all-compliance.sh` — Unified CI gate
- `~/.hermes/hooks/session-auto-log/` — Auto-log hook + wrapper
- `wiki/projects/_template/task.md` — Task template v2.2
- `wiki/projects/{project_id}/dashboard.md` — Live status
- `wiki/projects/{project_id}/dependency-graph.md` — Task mapping
- `references/ritual-v3-e2e-content-creator.md` — Real E2E test of Pre-flight Ritual v3 (Content Creator project, 18/06). Shows 3 honest issues found + fixes applied.
- `references/ritual-v3-e2e-content-creator-2nd-pass.md` — 2nd pass of same project (18/06 trưa): voice + value-rule drift detection, sub-agent sibling write, semantic token workaround. CRITICAL: shows why Phase 0 must re-verify existing files against LATEST user preferences.

## Pre-flight Ritual components (18/06)

When setting up the Pre-flight Ritual v3 system for new + existing projects:

- **Shared reference file:** `~/.hermes/profiles/_shared/project-setup-ritual.md` (3 phases: đọc/setup/per-task)
- **Bootstrap script:** `~/.hermes/scripts/bootstrap-project.sh` (idempotent, takes `project_id`, `name`, `owner` args)
- **Hub template:** `wiki/projects/_template/hub.md` (placeholders: `{PROJECT_NAME}`, `{project_id}`, `{YYYY-MM-DD}`)
- **SOUL injection:** Add "PROJECT SETUP RITUAL" section to `~/.hermes/SOUL.md` (~60 lines, mandatory before project work)

Verify Ritual wired correctly:
```bash
grep "PROJECT SETUP RITUAL" ~/.hermes/SOUL.md
test -f ~/.hermes/profiles/_shared/project-setup-ritual.md
test -x ~/.hermes/scripts/bootstrap-project.sh
test -f wiki/projects/_template/hub.md
bash ~/.hermes/scripts/bootstrap-project.sh test-rig "Test" "Tuấn Anh"  # verify idempotent
```

## See also

- Felix Model (memory entry 17/06) — auto-decide priority when multiple tasks pending
- `hermes-agent` skill — how Hermes itself works
- `sub-agent` tool — `delegate_task` for parallel work

## Background-review honesty note

Memory write attempt failed 3x with drift error (`USER.md` has shell-appended content not parseable by memory tool). Backup saved to `USER.md.bak.{ts}`. Drift must be resolved outside this skill workflow — either re-edit USER.md to a clean §-delimited list, or merge the new working-style entry once drift is cleared. Until then, the working-style facts in this skill's intro serve as the durable reference.