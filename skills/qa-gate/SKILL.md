---
name: qa-gate
description: QA Gate Protocol — verify every step before proceeding. Use when starting any task, before delivering results, or when asked "are you sure?". Load when working on research tasks, API questions, or any task where accuracy matters.
---

# QA Gate Protocol — Mỗi Bước Nhỏ Đều Phải QA

## Critical Lesson (2026-05-29)

**What happened:** Said MiniMax-M2.7 doesn't support Anthropic-compatible endpoint. Was 100% wrong. Correct: `https://api.minimax.io/anthropic` supports M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2.

**Root cause:** Relied on stale memorized knowledge instead of researching current docs.

## 3 Loại QA Gate

### Gate 1: Pre-Execution QA (TRƯỚC KHI LÀM)

```
Confidence Score Check:
- Score ≥ 9 → Proceed (verify nhanh 1 nguồn)
- Score < 9 → Research BẮT BUỘC trước
- Score < 5 → Deep research bắt buộc
```

### Gate 2: Mid-Execution QA (TRONG KHI LÀM)

**Trigger:** Sau mỗi milestone nhỏ — verify output trước khi đi tiếp.

### Gate 3: Post-Execution QA (SAU KHI LÀM)

**Trigger:** Trước khi deliver result — checklist.

## Research Quality Bar (2026-06-13 — HARD RULE)

User explicit yêu cầu: **mọi thông tin em cung cấp phải qua kiểm tra kỹ lưỡng + có bằng chứng research rõ ràng**. Áp dụng MỌI response có data/research, không riêng API/model questions.

### Research checklist (áp dụng mỗi khi trả lời có data, số liệu, claim, recommendation)

```
□ Có URL nguồn chính thức không? (VD: docs provider, gov site, official blog)
□ Có ghi ngày truy cập nguồn không? (chính sách thay đổi liên tục)
□ Có đối chiếu ≥2 nguồn độc lập không? (1 chính thức + 1 bên thứ ba)
□ Nếu không chắc → NÓI THẲNG "em chưa chắc, cần research thêm" + đặt câu hỏi khai thác
```

### Pitfall — "General Knowledge Trap"

**Sai lầm cũ xảy ra trong session 13/06:** Em tự tin trả lời dựa trên general knowledge nhưng KHÔNG research lại nguồn chính thức, dẫn đến info chung chung, không có evidence.

**Cách tránh:** Khi answer về:
- Hoa hồng affiliate TikTok Shop → check TikTok Ads Help center
- Luật quảng cáo 2026 → check Cổng TTĐT Chính phủ + báo VN news gần đây
- Spec API/sản phẩm → check official docs + community forum
- Trend/algorithm → check TikTok Business Blog / YouTube Creators blog gần đây

### Câu trả lời MẪU khi không chắc

❌ SAI: "TikTok Shop hoa hồng thiết bị quay phim khoảng 5-10%."
✅ ĐÚNG: "Em chưa có số chính thức cho ngách thiết bị quay phim trên TikTok Shop VN 2026. Để em check TikTok Ads Help Center (URL) + đối chiếu 1 nguồn bên thứ ba (Accesstrade/draerp.vn) rồi báo lại với URL + ngày truy cập. Trong lúc đó, anh muốn em tập trung vào SP nào trước để giới hạn research?"

## API/Model Compatibility — ALWAYS Web-Search First

**Never answer without web search:**
- Model hỗ trợ endpoint nào
- Base URL chính xác cho provider
- Tool X có dùng được với model Y không
- API format (Anthropic vs OpenAI) cho bất kỳ provider nào

**Workflow:**
1. Web search docs của provider đó
2. Extract endpoint, base URL, model ID
3. Verify với official documentation
4. Then answer — kèm source reference

## Quick QA Rules

| Scenario | Action |
|----------|--------|
| Em muốn deliver ngay | ❌ Stop → Verify trước |
| Không chắc về fact | → Research, don't guess |
| API specs, endpoints | → ALWAYS search web first |
| Đã deliver xong thấy uncertain | → Correct ngay |

## System Prompt / SOUL.md Change Validation Workflow

**When:** After adding NEW patterns to SOUL.md, system prompt, or any identity-bearing file (HARVEST, REVERSE ENGINEER, APPLY VERBATIM from `agent-prompt-injection-defense`).

**Why:** New patterns in system prompt are easy to write but hard to verify in isolation. They look right in markdown but may not actually fire during real tasks. Without testing, the patterns sit in the file as dead text.

**4-Pattern Test Protocol:**

```
1. PICK a real task from user's current project (DON'T ask user, just choose)
   → Must be: concrete, has measurable success criteria
   → Avoid: abstract research, opinion questions
2. LOAD relevant skills BEFORE the task (Skills-First, see using-agent-skills)
   → Confirms the new pattern doesn't conflict with existing skill knowledge
3. EXECUTE the task using the 4 new patterns explicitly
   → Pattern #1: MCP Connector (use MCP tools first, not browser)
   → Pattern #2: Persistent Storage (save findings with key convention)
   → Pattern #3: Skills-First (load skill_view before complex work)
   → Pattern #4: Search Discipline (scale searches to complexity)
4. VERIFY each pattern fired correctly:
   □ Did MCP tool get called before browser? (Pattern #1)
   □ Did findings get saved to wiki with proper key? (Pattern #2)
   □ Was skill_view called before execution? (Pattern #3)
   □ Were searches parallel + paraphrased + scaled? (Pattern #4)
```

**Report format:**

| Pattern | Pass? | Evidence |
|---------|-------|----------|
| #1 MCP Connector | ✅/❌ | Tool calls in transcript |
| #2 Persistent Storage | ✅/❌ | Wiki file path + key |
| #3 Skills-First | ✅/❌ | skill_view in transcript |
| #4 Search Discipline | ✅/❌ | Search count + format |

**Pitfall — Don't trust "looks right" in SOUL.md:**

The patterns may be beautifully written but never fire because:
- Order in SOUL.md is too far down → context overflow truncates
- Trigger keywords are too narrow → real tasks don't match
- Conflict with existing skills → user override blocks them

**Real example (2026-06-16, Tuấn Anh):** After harvesting 4 patterns from CLAUDE-FABLE-5.md into SOUL.md, picked TikTok viral hooks research (from Content Creator project). All 4 patterns passed:
- `#1`: Used `mcp_MiniMax_web_search` 3x instead of browser
- `#2`: Saved findings to `/wiki/queries/tiktok-hooks-test-2026-06-16.md`
- `#3`: Loaded `last30days` + `tiktok-viral-script` BEFORE research (caught voice change 13/06)
- `#4`: 3 parallel searches, paraphrased, no long quotes

**Key insight:** Skills-First (Pattern #3) was the most critical — it caught a voice profile change in the existing skill that would have caused a wrong-voice script.

## Multi-Axis Verification — 4 Levels of "Done"

**Failure mode (2026-06-16):** After Fable-5 mandate completed (4 SOUL.md files updated, CI gate PASS, hook tested), agent reported "đã hoàn thành 100%". User asked to re-verify. On honest re-audit, agent found:
- 4/4 patterns PARTIAL (missing sub-rules)
- 7 sections of source SKIPPED without report
- Even in the verify turn, agent was PARTIAL applying patterns

**Root cause:** Agent had only 1 verification axis (CI gate = keyword marker presence). Missed 3 other axes.

**Rule:** Before claiming any mandate/pattern is "applied system-wide", verify ALL 4 axes:

| Axis | Question | What to check |
|------|----------|---------------|
| **1. Keyword presence** | Does the file mention the pattern? | `grep` for pattern name (CI gate) |
| **2. Full content** | Does the shared reference have COMPLETE detail? | Read shared ref, check against source |
| **3. Behavior change** | Did the pattern actually change agent behavior in a real task? | Self-audit transcript, cite evidence |
| **4. Source coverage** | Did you harvest ALL relevant sections from source? | List original sections, mark harvested vs SKIPPED |

**If axis 1 passes but axes 2-4 are unchecked → DON'T claim DONE. Audit first.**

**Real example (Fable-5, 2026-06-16):**

```
Axis 1: 4/4 SOUL.md files have "MCP CONNECTOR" keyword → PASS
Axis 2: Shared ref has decision tree + examples, but missing search_mcp_registry, suggest_connectors, opt-in rules → PARTIAL
Axis 3: In the verify turn itself, used curl once instead of mcp_exa_web_fetch_exa → PARTIAL
Axis 4: 4 patterns harvested, but 7 sections of original Fable-5 (memory_system, Claudeception, citation format, etc.) SKIPPED without reporting → UNREPORTED
```

**Honest report would have been:** "1/4 patterns fully applied (Persistent Storage), 3/4 PARTIAL. 4/11 source sections harvested, 7 SKIPPED. Compliance gate = axis 1 only, not full verification."

**Don't claim DONE until you have evidence for all 4 axes.** If you can't verify an axis, SAY SO — "axis 3 not yet tested" is more honest than silently skipping it.

## Case Study
- `references/minimax-api-verification-2026-05-29.md` — WRONG answer delivered without research: said M2.7 doesn't support Anthropic-compatible endpoint. Reality: it does. QA gate would have caught this.

## Examples

### Example 1: Pre-Execution QA (Score ≥ 9 → Proceed)
```
Task: "Fix the login bug"
Confidence assessment:
- Domain knowledge: 3/3 (debugged auth before)
- Past experience: 2/3 (similar bugs)
- Tool availability: 1/1 (have logs, can reproduce)
- Self-verifiable: 1/1 (can test fix)
- Known patterns: 1/2 (auth flow patterns)
Total: 8/10 → Proceed with quick verification (check git log + session DB)
```

### Example 2: Pre-Execution QA (Score < 9 → Research Required)
```
Task: "Connect to new AI provider X"
Confidence assessment:
- Domain knowledge: 1/3 (never used X)
- Past experience: 0/3 (first time)
- Tool availability: 1/1 (have curl)
- Self-verifiable: 1/1 (can test connection)
- Known patterns: 0/2 (no similar pattern)
Total: 3/10 → Deep research BẮT BUỘC
→ Web search: provider docs, API format, authentication
→ Extract: endpoint URL, required headers, model IDs
→ Verify with official docs before answering
```

### Example 3: Post-Execution QA (Deliver Checklist)
```
Before delivering result to Anh:
□ Did I verify the main claim with at least 1 source?
□ Is the API/model info from current documentation?
□ Did I avoid "Em không chắc về..."?
□ Is the deliverable complete or do I need to add context?
□ If uncertain about something, did I correct it immediately?
```

## Related
- [[hermes-agent-self-evolution]]