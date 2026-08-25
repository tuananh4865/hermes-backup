# Content Creator Project — Live Example (v2.1 → v2.4)

> Real example of project-workflow-v2 applied to a multi-month project.
> Use as reference when creating your own project structure.
> **Updated 17/06 22:18**: After successful E2E test of T-01.1 + dashboard + dependency graph.

## Project Setup

- **Project ID:** `content-creator`
- **Path:** `/Volumes/Storage-1/Hermes/wiki/projects/content-creator/`
- **KPI:** 10K TikTok followers / 45 ngày
- **Started:** 2026-06-17
- **Orchestrator:** Hermes (default profile)
- **Pivot 17/06:** 100% hướng dẫn cơ bản, mẹo, câu chuyện cuộc sống — 0% bán hàng trong 45 ngày đầu. 3 trụ: EDIT + SETUP GÓC QUAY + ÁNH SÁNG.

## Folder Structure (v2.4 — full)

```
content-creator/
├── hub.md                                   # 4,097b — KPIs, team, current status
├── dashboard.md                             # 6,050b — v2.4: live status (NEW)
├── dependency-graph.md                      # 7,558b — v2.4: task-level graph (NEW)
├── phases/
│   └── phase-01-foundation.md               # 2,582b — Phase 01 (0-15 ngày)
├── research/                                # v2.1: BẮT BUỘC layer
│   ├── T-01.1-gen-z-slang-2026-06.md        # 10,447b, 11 terms (6 HOT/4 RISING/1 DEAD)
│   └── T-01.1-trending-sounds-2026-06.md    # 8,560b, 6 sounds (4 HIGH/2 MED risk)
├── tasks/
│   └── task-T-01.1-research-slang-sounds.md # 5,317b, status: ✅ DONE
├── actions/                                 # v2.2: 9 files (1 load-skill + 6 search + 2 save)
│   ├── 2026-06-17-T-01.1-load-skill.md
│   ├── 2026-06-17-T-01.1-search-slang-1.md
│   ├── 2026-06-17-T-01.1-search-slang-2.md
│   ├── 2026-06-17-T-01.1-search-slang-3.md
│   ├── 2026-06-17-T-01.1-search-sounds-1.md
│   ├── 2026-06-17-T-01.1-search-sounds-2.md
│   ├── 2026-06-17-T-01.1-search-sounds-3.md
│   ├── 2026-06-17-T-01.1-save-slang.md
│   └── 2026-06-17-T-01.1-save-sounds.md
├── decisions/                               # (empty)
└── logs/                                    # (empty — hook v2 chưa trigger trong session này)
```

## Team Assignment (Dùng profiles có sẵn, KHÔNG tạo mới)

| Role | Profile | Used in Content Creator |
|------|---------|------------------------|
| Orchestrator (Em) | `default` | Coordinate, verify gate, report |
| Research Lead | `research-lead` | T-01.1 ✅ DONE |
| Content Director | `content-director` | T-01.2 (next), T-01.4 |
| Coder | `coder` | (planned) T-01.6 automation scripts |
| Memory Curator | `memory-curator` | Daily log review |
| QA Agent | `qa-agent` | T-01.3 (next) |

## Phase 01 Spec (excerpt)

**Goal:** Setup kênh @hi.imdung style với 3 trụ content
**Duration:** 15 days (2026-06-17 → 2026-07-02)
**KPIs:**
- 500+ followers
- 15+ videos
- 1 video hit 5K views
- Voice compliance 100%
- 0 TRÁHN violations

## 6-Step Loop (v2.1 — RESEARCH BẮT BUỘC) — T-01.1 trace

```
0. RESEARCH  ← Step 0 for T-01.1 = the research itself (output: research/ folder) ✅
1. PLAN      ← T-01.1 planned with research_refs field (even if empty since Step 0 IS research) ✅
1.5 RESEARCH ← SKIP for T-01.1 (research covered in Step 0) ✅
2. EXECUTE   ← research-lead did 3 MCP searches + saved to research/ ✅
3. VERIFY    ← qa-agent checks (pending — T-01.3 next)
4. NEXT      → Start T-01.2 (Voice profile) using T-01.1's research outputs
```

## E2E Test Results (17/06 22:14) — VERIFIED

| Deliverable | Expected | Actual | Status |
|-------------|----------|--------|--------|
| Gen Z slang terms | ≥10 | 11 (6 HOT/4 RISING/1 DEAD) | ✅ |
| Trending sounds | ≥5 | 6 (4 HIGH risk/2 MED) | ✅ |
| YAML frontmatter per file | required | all valid | ✅ |
| Wikilinks per file | ≥2 | 5 per file | ✅ |
| Action log files | ≥1 per action | 9 files | ✅ |
| Action log word count | ≥50 | ≥232 mỗi file | ✅ |
| Voice compliance | "mình"/"bạn" | confirmed | ✅ |
| Citations format | title+URL+date | 9 sources audited | ✅ |
| Top slang | Quẩy, Cà khịa, Đỉnh khoai | (recommend cho T-01.4) | — |
| Top sounds | Có Công Mài "Sắc", Big Boom | (recommend cho T-01.4) | — |

**CI Gate v2.4:**
```bash
$ bash ~/.hermes/scripts/check-all-compliance.sh content-creator
✅ Fable-5 compliance: PASS
✅ Loop Engine compliance: PASS
✅ All tasks have owner_role field
✅ All active tasks have research_refs field (v2.1)
✅ All tasks have verify_attempts field (v2.2)
✅ PASS: content-creator complies with workflow v2
```

## Sub-agent Honest Report (PITFALLS caught 17/06 22:14)

Sub-agent `research-lead` trả về 3 vấn đề thật (KHÔNG giấu):

1. **Skill mismatch** — T-01.1 spec referenced `tiktok-viral-script` nhưng skill KHÔNG tồn tại. Sub-agent dùng `tiktok-competitor-deep-analysis` fallback, log honest trong `2026-06-17-T-01.1-load-skill.md`.
2. **`web_extract` tool fail** — Backend limitation. Workaround: dùng `web_search` với query specific hơn.
3. **Sample bias VPop** — 4/6 sound là VPop remix, không cover K-pop/US-UK. Sub-agent note rõ trong `## Transparency` section của sounds file.

**Pattern captured:** Sub-agent PHẢI flag sample bias + tool failures ngay trong output. Orchestrator cần decide có retry/round search bổ sung hay accept.

## Lessons Learned (v2.1 → v2.4)

1. **Default profile path confusion** — `~/.hermes/profiles/default/` folder exists but is NOT used by default profile. Default uses `~/.hermes/SOUL.md`. Always check with `hermes profile show default`.

2. **Task file needs verify criteria** — qa-agent needs objective checklist, not vibes. List 5-10 specific criteria per task.

3. **Hook auto-detect from message** — Session-auto-log v2 reads `project: {id}`, `T-XX.X`, `phase: {id}` from user message. No manual tagging needed.

4. **YAML frontmatter is not optional** — Every file (hub/phase/task/action/decision/research) must have frontmatter with `type`, `project_id`, `status`, `owner_role`, `research_refs` (v2.1). CI gate fails without.

5. **RESEARCH-first mandate (v2.1)** — User explicit feedback 17/06 10:50: research is MANDATORY before plan AND before execute. v2.0 loop missed this — v2.1 fixed with Step 0 + Step 1.5.

6. **Idempotent injector for new tasks** — When creating new task, run `add-fable5-to-soul.sh` style idempotent injection to ensure YAML fields (status, owner_role, research_refs) are present.

7. **Skill reference verification (v2.4)** — Before delegating task that references a skill, `ls ~/.hermes/skills/{name}/SKILL.md` để confirm skill tồn tại. Sub-agent sẽ fallback tốt, nhưng tốt hơn là catch trước khi delegate.

8. **Sub-agent transparency section (v2.4)** — Encourage sub-agent include `## Transparency` section listing: tool failures, sample bias, data source limitations, alternative approaches considered. Better than silent success.

9. **Dashboard + dependency graph are NOT optional (v2.4)** — Tuấn Anh needs 1-page view of project status. Without dashboard, phải `ls -R` + `cat hub.md` + `cat phase-01.md` + `cat task-T-XX.X.md` mỗi lần muốn check. With dashboard = 1 read.

10. **E2E test first, scale after (v2.4)** — Don't scale workflow to project #2 until you've proven it works on project #1. Caught 3 issues (skill mismatch, sample bias, hook silent) during T-01.1 E2E that would have propagated to project #2.

## Next Steps

1. **T-01.3** — qa-agent reviews T-01.1 output (CI gate already pass, nhưng cần human-style content review)
2. **T-01.2** — content-director tạo voice profile cho 3 trụ (parallel với T-01.3, save 3h)
3. **T-01.4** — content-director viết 15 video scripts dùng research từ T-01.1
4. **Fix skill mismatch** — update T-01.1 spec hoặc tạo alias `tiktok-viral-script` → `tiktok-competitor-deep-analysis`
5. **Daily dashboard refresh** — sau mỗi task status change → update dashboard.md

## Cross-Reference

- `project-workflow-v2` skill → v2.4 specs
- `tiktok-competitor-deep-analysis` skill → sub-agent fallback (T-01.1)
- `system-wide-mandate-enforcement` skill → 3-piece enforcement pattern
- `multi-agent-orchestrator` skill → PITFALL 13 (v2.1 reference)
- `qa-gate` skill → RESEARCH-as-Gate section
- `self-verify-after-workaround` skill → evidence pattern (v2.4 alignment)
- `strict-system-qa-protocol` skill → 9 verifies for deployed system