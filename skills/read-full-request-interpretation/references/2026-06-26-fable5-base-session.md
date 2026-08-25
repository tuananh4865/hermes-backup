# 2026-06-26 — Fable 5 Base Architect Session

**Session ID:** 2026-06-26 (Telegram)
**Source:** `/Users/tuananh4865/.hermes/cache/documents/doc_83470efc63cd_CLAUDE-FABLE-5.md` (anh uploaded)
**Outcome:** SOUL.md restructured into 4-layer architecture with Fable 5 = BASE

## What Happened

Anh uploaded Claude Fable 5 system prompt (123 KB, 1597 lines) và muốn restructure SOUL.md theo pattern "Fable 5 = base architect".

### Phase 1: Initial Intent Confusion
- Anh: "Anh muốn wipe out toàn bộ hermes và trả về cài đặt gốc"
- Agent: Asked 4 options (full wipe / wipe ~/.hermes / reset config / backup + wipe) — anh no response
- Anh: "Thôi giờ phân tách từng cái để loại bỏ dần nhưng gì quá cũ đi. Bât đầu với file soul trước!"
- **Lesson:** "wipe" ≠ wipe all-or-nothing. Anh prefer incremental cleanup. Phải confirm mức độ trước khi act.

### Phase 2: Fable 5 Base Architect Refactor
- Anh uploaded file Fable 5 → anh: "Hiện tại anh muốn fable 5 làm nền tảng tổng quát cho hermes như file anh gửi. Mọi thứ còn lại phải hoạt động trên fable 5 bao gôm cả loop engineer"
- Agent: Filtered 20 sections incompatible với Hermes (product_info, child_safety, user_wellbeing, anthropic_reminders, memory_system, persistent_storage, computer_use paths, file_handling, sharing_files, artifact_usage, package_management, image_search, Tool Definitions, Identity Preamble, anthropic_api_in_artifacts, citation_instructions, network_configuration, filesystem_configuration, available_skills)
- Agent: Kept 7-12 sections compatible (refusal, legal/financial, tone, evenhandedness, mistakes, mcp_apps, skills-first, file_creation, producing_outputs, search, copyright, user_context)
- **Lesson:** Fable 5 designed for Claude Code → phải lọc bỏ sections không tương thích Hermes TRƯỚC khi adapt.

### Phase 3: Goal Clarification
- Anh: "Goal của em là làm cho fable 5 trở thành base architect của Hermes mọi thứ còn lại phải hoạt bên trong cái fable 5 này"
- **Key insight:** Đây là architectural rule, không phải parallel. Fable 5 thắng khi conflict.
- Agent: Wrote SOUL.md v1 với 4 layers (Fable 5 base + Hermes identity + mandates + wiki session).

### Phase 4: Cross-Reference Verification
- Anh: "Làm và đối chiếu kĩ hơn đi"
- Agent: Built cross-reference table — show what overlaps, what conflicts, what to keep/drop.
- **Lesson:** Khi user nói "làm và đối chiếu kỹ hơn" → must cross-reference TRƯỚC khi apply, build proposal → cross-ref table → show diff.

### Phase 5: Quality Gap Escalation
- Anh: "Các phần còn lại như read full request, research (web search and file search) first, loop engineer em ko adapt vào hả"
- **CRITICAL:** Agent đã adapt nhưng QUÁ SƠ SÀI:
  - "READ-FULL-REQUEST" → chỉ 1 dòng reference
  - "RESEARCH-FIRST" → Rule #1 chỉ 1 dòng abstract
  - "LOOP-ENGINEERING" → Task Lifecycle chỉ 6-step sơ sài
- Agent v2: MỞ RỘNG thành full procedures với WHY + STEPS + ANTI-PATTERNS + SELF-CHECK
- **Lesson:** Rule abstract ≠ executable procedure. Mỗi Core Rule phải có (1) WHY root cause từ past failure, (2) STEP-BY-STEP PROCEDURE, (3) ANTI-PATTERNS concrete examples, (4) SELF-CHECK cuối.

## Lessons Captured

### L1: Cross-Reference Before Apply
- Khi user nói "làm và đối chiếu kỹ hơn" → cross-ref table TRƯỚC khi commit
- Build proposal → identify overlaps/conflicts/missing → show diff cho user review

### L2: Expand Abstract Rules Into Procedures
- Khi user escalate "X em ko adapt vào hả" → check current state, expand sơ sài thành full
- Rule format = WHY + STEPS + ANTI-PATTERNS + SELF-CHECK (not just 1 dòng)

### L3: Fable 5 = Base Architect Rule
- Fable 5 designed for Claude Code → 20 sections incompatible Hermes
- Filter TRƯỚC: product_info, child_safety, user_wellbeing, anthropic_reminders, memory_system, persistent_storage, paths Linux, present_files, artifact_usage, package_management, image_search, Tool Definitions, Identity Preamble, anthropic_api_in_artifacts, citation_instructions, network_configuration, filesystem_configuration, available_skills
- Keep 7-12 sections: refusal, legal/financial, tone, evenhandedness, mistakes, mcp_apps, skills-first, file_creation, producing_outputs, search, copyright, user_context
- All Hermes rules INSIDE Fable 5 base, không parallel
- Conflict → Fable 5 wins

### L4: Incremental Cleanup Preference
- Khi user nói "wipe" → confirm mức độ (full wipe vs incremental cleanup)
- "Phân tách từng cái" → làm từng cái một, user review từng bước
- KHÔNG all-or-nothing

### L5: Loop Engineering Adapted from Project Workflow Loop Engine Skill
- Source: `~/.hermes/skills/planning-and-task-breakdown/project-workflow-loop-engine/SKILL.md`
- 6-step loop + Foundation Layer (Honest reporting, Evidence-based, Source citation, Independent verification)
- Felix Model Self-Decision matrix (impact × risk)
- Anti-patterns table + mapping to Fable 5 BASE sections

### L6: Research-First Protocol 3-Layer Search Ladder
- Layer 1: Wiki search (`/Volumes/Storage-1/Hermes/wiki/`)
- Layer 2: File search (local Mac configs)
- Layer 3: Web search (MCP first: mcp_MiniMax_web_search, mcp_exa_web_search_exa)
- 4-step workflow + Decision Tree + Anti-patterns

### L7: Read-Full-Request 3-Step Procedure
- Step 1: PARSE FULL (atomic deliverables)
- Step 2: VERIFY UNDERSTANDING (1 câu hỏi nếu ambiguous)
- Step 3: DELIVER ALL (không skip phần nào)
- Self-check checklist 4 items
- Khi user nhắc lại → STOP + re-parse

## Files Created/Modified

- `/tmp/soul-backup-20260626-093457.md` — Backup SOUL.md cũ (26.6 KB)
- `/tmp/soul-new.md` — SOUL.md v1 (sơ sài, 14 KB)
- `/tmp/soul-new-v2.md` — SOUL.md v2 (full adaptation, 22 KB)

## Files Pending Apply

- `/tmp/soul-new-v2.md` → `~/.hermes/SOUL.md` (anh review xong mới apply)

## Related Skills Referenced

- `read-full-request-interpretation` (this skill) — patched 2026-06-26
- `project-workflow-loop-engine` — source cho Loop Engineering section
- `active-checklist` — reference cho 3-phase checklist
- `fable-5-patterns` — current 4 patterns, expanded in v2
- `hermes-config-edit` — for `hermes config set` operations