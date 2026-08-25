---
name: project-checklist-management
title: Project Checklist & Auto-Log System
description: Set up and maintain a single-source-of-truth CHECKLIST for any multi-day user project (Content Creator, app build, course creation, etc.). When user has a long-running project and explicitly asks to "log", "checklist", "track progress", "avoid duplication", "update continuously", or wants agents to know what's been done/doing/todo. Use a 4-section checklist file (🔴 ĐANG LÀM / 🟡 CHƯA LÀM / 🟢 ĐÃ LÀM / ⚪ ĐÃ HỦY) plus HARD RULE in hub, agent must read first when entering project.
created: 2026-06-18
updated: 2026-06-18
version: 1.0
type: skill
tags: [project-management, checklist, auto-log, knowledge-base, productivity]
confidence: high
related_skills:
  - hermes-project-workflow-system
  - multi-agent-orchestrator
  - self-verify-after-workaround
---

# Project Checklist & Auto-Log System

> **Class-level skill:** Setup a lightweight checklist + auto-log system for any user-facing project (Content Creator, app build, course creation, business workflow). Distinct from `hermes-project-workflow-system` which is heavy 6-step Loop Engine + CI gates for SYSTEM-level multi-week infra projects. **This skill is for USER-level projects where the user wants visibility into what's happening without Hermes infrastructure complexity.**

## When to use this skill

**Trigger phrases from user:**
- "log toàn bộ những gì đã làm, đang làm và chưa làm"
- "tránh trùng lặp + cập nhật liên tục"
- "tạo checklist cho project"
- "agent nào vào project cũng phải biết đang ở đâu"
- "đừng làm lại việc đã làm"

**Use when:**
- User has a multi-day project (Content Creator, course, app, business)
- Multiple sessions/agents will touch the project
- User wants visibility + tracking WITHOUT heavy Hermes infra (no sub-agent orchestration, no research phases, no CI gates)
- Existing project files already use a hub.md + folder structure

**Do NOT use when:**
- Project is 1-shot task → use Fable-5 only
- Project needs full Hermes infra (multi-agent, compliance gates, hooks) → use `hermes-project-workflow-system`
- Project has < 5 tasks total → overkill, use todo list

## Core architecture (3-piece enforcement)

```
1. CHECKLIST file         → single source of truth (Operations/CHECKLIST-PROJECT.md)
2. HARD RULE in hub.md    → agent reads FIRST when entering project
3. Agent auto-prompt      → "Có X đang làm, Y chưa làm, Z đã làm"
```

3 pieces, not 4 (skip the CI gate layer — that's for Hermes system projects, not user projects).

## Canonical CHECKLIST file structure

**Path:** `{project_root}/Operations/CHECKLIST-PROJECT.md` (or any path user specifies)

**4 sections + 4 support sections:**

```markdown
# ✅ PROJECT CHECKLIST — {Project Name}

> **Mục đích:** Single source of truth cho mọi công việc trong project. Agent nào làm việc với project này PHẢI đọc + cập nhật file này.

## 📊 TRẠNG THÁI TỔNG QUAN
| Trụ/Phase | Có sẵn | Đã xong | Còn lại | Tiến độ |
|-----------|--------|---------|---------|---------|
| ...       | ...    | ...     | ...     | ...%    |

**Mục tiêu / Deadline:** ...

## 🔴 ĐANG LÀM (in_progress)
| # | Task | Session bắt đầu | Agent | Deadline | Block bởi |
|---|------|------------------|-------|----------|-----------|
|   | (trống — chưa có task dở) | | | | |

## 🟡 CHƯA LÀM (todo) — Ưu tiên cao
### ƯU TIÊN 1 — ...
| # | Task | Ghi chú | Effort |
|---|------|---------|--------|
| 1.1 | ... | ... | ... |

## 🟢 ĐÃ LÀM (done) — Lịch sử
### YYYY-MM-DD
- ✅ **[DANH MỤC] Tên task** (Session YYYY-MM-DD HH:MM, ~X phút)
  - File 1: thay đổi gì
  - File 2: thay đổi gì
  - Kết quả: ...
  - Tác động: ...

## ⚪ ĐÃ HỦY / KHÔNG LÀM (cancelled)
| # | Task đã hủy | Lý do | Ngày hủy |
|---|-------------|-------|----------|
|   | ... | ... | ... |

## 📌 QUY TẮC SỬ DỤNG CHECKLIST NÀY (cho agent)
### Khi bắt đầu session:
1. ĐỌC file này ĐẦU TIÊN
2. CHECK "🔴 ĐANG LÀM" → nếu có task dở → tiếp tục
3. CHECK "🟡 CHƯA LÀM" → chọn task phù hợp với yêu cầu của anh
4. CẬP NHẬT "🔴 ĐANG LÀM" khi bắt đầu

### Khi xong task:
- Move "🔴 ĐANG LÀM" → "🟢 ĐÃ LÀM" với format chuẩn
- Update "📊 TRẠNG THÁI TỔNG QUAN" nếu có số liệu mới

## 🔄 TỰ ĐỘNG CẬP NHẬT
**Khi agent mới bắt đầu session:**
1. Đọc CHECKLIST FIRST
2. Báo cáo: "Có X đang làm, Y chưa làm, Z đã làm"
3. Hỏi user muốn tiếp task nào

## 📊 METRICS & DASHBOARD
| Metric | Hiện tại | Mục tiêu | Tiến độ |
|--------|----------|----------|---------|
| ...    | ...      | ...      | ...%    |

## 🔗 LIÊN KẾT
- hub.md
- ...
```

## HARD RULE injection in hub.md

Add this block to `hub.md` of the project (immediately after "Khi bắt đầu session mới" section):

```markdown
## 🔄 Khi bắt đầu session mới
Em sẽ tự động:
1. **ĐỌC `Operations/CHECKLIST-PROJECT.md` TRƯỚC TIÊN** (rule mới YYYY-MM-DD — bắt buộc)
2. Đọc `hub.md` (file này)
3. ...
8. **CẬP NHẬT CHECKLIST** ngay khi xong task

**⚠️ HARD RULE (YYYY-MM-DD):** Mọi agent làm việc với project này PHẢI đọc `Operations/CHECKLIST-PROJECT.md` ĐẦU TIÊN trước khi làm bất kỳ task nào. Cấm làm mà không check trùng lặp.
```

## Format log chuẩn (cho agent)

**Khi bắt đầu task:**
```markdown
- 🔄 **[DANH MỤC] Tên task** (Session YYYY-MM-DD HH:MM)
  - File 1: sẽ thay đổi gì
  - File 2: sẽ thay đổi gì
  - Lý do: ...
```

**Khi xong task:**
```markdown
- ✅ **[DANH MỤC] Tên task** (Session YYYY-MM-DD HH:MM, ~X phút)
  - File 1: thay đổi gì (X dòng)
  - File 2: thay đổi gì
  - Kết quả: ...
  - Tác động: ...
  - Bài học: (nếu có)
```

## Workflow setup (5 steps)

```bash
# 1. Identify project root + check existing structure
ls "{project_root}/"
cat "{project_root}/hub.md" | head -50

# 2. Create CHECKLIST file
mkdir -p "{project_root}/Operations/"
# Write checklist using template (see structure above)

# 3. Inject HARD RULE into hub.md
# Add "Đọc CHECKLIST-PROJECT.md TRƯỚC TIÊN" + HARD RULE block

# 4. Update CHANGELOG.md
# Add entry: "[YYYY-MM-DD] — SETUP Hệ thống Auto-Log + Checklist Project"

# 5. Self-update checklist (record this setup task)
# Move from "🔴" (planning) → "🟢" with log
```

## When to use which project management skill

| Class of project | Use this skill | Use `hermes-project-workflow-system` |
|------------------|----------------|--------------------------------------|
| User content creation (TikTok, YouTube, blog) | ✅ | ❌ overkill |
| Personal app build with 5-30 tasks | ✅ | ❌ |
| Multi-week course creation | ✅ | ❌ |
| Hermes system infrastructure (multi-agent, CI, hooks) | ❌ | ✅ |
| Complex project with research phases + dependency graph + multiple agents | ❌ | ✅ |
| Project needs CI compliance gates | ❌ | ✅ |

**Rule of thumb:** If user said "checklist" or "log đầy đủ" → this skill. If user said "system" or "infra" or "compliance" → `hermes-project-workflow-system`.

## Common pitfalls

1. **Don't duplicate with `hermes-project-workflow-system`** — that skill is for SYSTEM-level infra (research phases, action logs, CI gates, hook wrappers). This skill is lightweight — single CHECKLIST file + hub.md rule. Pick one based on project class.

2. **CHECKLIST grows stale fast** — Agent MUST update after every task. If agent claims "xong" without updating checklist, the next session will redo work. HARD RULE in hub.md enforces this.

3. **"🔴 ĐANG LÀM" column can become a graveyard** — If a task moves to "🟢 ĐÃ LÀM", delete it from "🔴". Don't leave stale rows.

4. **Cancelling without recording loses learning** — Always log in "⚪ ĐÃ HỦY" with reason. The reasons are gold for future projects (e.g., "Hiểu nhầm — supersede bởi curriculum" → don't repeat the mistake).

5. **Effort estimates lie** — Don't optimize for accuracy. Use rough categories (30 phút / 2 giờ / nửa ngày). The point is prioritization, not forecasting.

6. **Memory drift blocks writes** (NEW 2026-06-18) — If memory tool returns "Refusing to write USER.md: file on disk has content that wouldn't round-trip through the memory tool", the file has been edited externally (by shell append, patch tool, or concurrent session). The tool saves a `.bak.<timestamp>` snapshot. To resolve: (1) read the .bak file to see missing entries, (2) integrate them into memory tool one at a time via `memory(action=add, content=...)`, (3) rewrite original file to clean §-delimited state, (4) retry. This guard prevents silent data loss (issue #26045).

## Verification pattern

After setup, verify with:
```bash
# Check checklist exists
test -f "{project_root}/Operations/CHECKLIST-PROJECT.md" && echo "✅ exists"

# Check 4 sections present
grep -E "^## (🔴|🟡|🟢|⚪)" "{project_root}/Operations/CHECKLIST-PROJECT.md"

# Check hub.md has HARD RULE
grep -A 1 "HARD RULE" "{project_root}/hub.md"

# Check CHANGELOG has entry
grep "Auto-Log + Checklist Project" "{project_root}/CHANGELOG.md"
```

## Example: Content Creator project (verified 2026-06-18)

User explicit request: *"Lập cho anh một rule trong project này là luôn phải log và check list toàn bộ những gì đã làm, đang làm và chưa làm"*

**Setup actions (10 phút):**
1. Tạo `Operations/CHECKLIST-PROJECT.md` (11.2KB) — 4 sections + bảng trạng thái + metrics dashboard
2. Inject HARD RULE vào `hub.md` — bước 1 + bước 8 + cảnh báo cuối
3. Update `CHANGELOG.md` — entry mới theo format chuẩn
4. Self-update checklist (ghi log task này vào "🟢 ĐÃ LÀM")

**Impact:**
- 100% task trong project được log liên tục
- Agent mới biết ngay đang ở đâu
- Không bao giờ trùng lặp
- Có thể đo lường tiến độ

## Reference files

- `references/content-creator-checklist-example.md` — Full CHECKLIST-PROJECT.md example (11KB) for Content Creator project, 2026-06-18. Shows all 4 sections with real data, metrics dashboard, link relationships.

## See also

- `hermes-project-workflow-system` — Heavy 4-piece for Hermes system infra
- `multi-agent-orchestrator` — Decomposition + delegation patterns
- `self-verify-after-workaround` — When user demands strict QA, run tool-based checks