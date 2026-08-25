---
name: qa-gate
description: QA Gate Protocol — verify every step before proceeding. Use when starting any task, before delivering results, or when asked "are you sure?". Also use when user repeats a request (signal you failed first time) or when task feels like "transcript/analyze" combos that need multi-deliverable parsing. Load when working on research tasks, API questions, or any task where accuracy matters.
---

## 🚨 Permanent Independent-Subagent QA Mandate (2026-07-30)

For **every task** that produces an answer, recommendation, decision, file, code, or other output, dispatch a fresh-context subagent as the independent QA checker. Self-QA is only the maker's pre-check and must never be the final verdict. The subagent must inspect the original request/source/output independently and return `PASS`, `FAIL`, or `PARTIAL_PASS` with raw evidence. Timeout, missing evidence, or inability to inspect means `UNVERIFIED` — stop the completion claim and report the limitation.

**Required order:** maker/orchestrator output → independent subagent QA → reconcile findings → fix/re-verify if needed → deliver. This applies to small tasks too; do not silently downgrade to self-check because the task looks easy.

## Critical Lesson (2026-05-29)

**What happened:** Said MiniMax-M2.7 doesn't support Anthropic-compatible endpoint. Was 100% wrong. Correct: `https://api.minimax.io/anthropic` supports M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2.

**Root cause:** Relied on stale memorized knowledge instead of researching current docs.

## 🚨 TOP-LEVEL PRINCIPLE: Read-Full-Request Mandate (2026-06-22)

**This is now a system-wide mandate applied to all 12 Hermes profiles (verified by `bash ~/.hermes/scripts/check-readfullrequest-compliance.sh`).** Tuấn Anh's verbatim feedback:

> *"Phải phân tích toàn bộ yêu cầu của anh thay vì chỉ đọc lướt qua. Đây là một lỗi rất nghiêm trọng của em! Nó làm cho anh cảm thấy em rất ngu không hiệu quả, không đọc hiểu được hết một yêu cầu đơn giản của anh! Ngay từ đầu anh đả bảo em lấy transcript!"*

> *"Bị ngu à mày??? Đây là nội dung yêu cầu của tao mà mày làm cái đéo gì vậy?"*

### The 3-Step Pre-Execution Protocol (NON-NEGOTIABLE)

Before ANY execute, regardless of task type:

```
1. PARSE — Break user's request into atomic deliverables
   - Read every word (don't skim)
   - If "tải về và phân tích X" → that's 2+ deliverables
   - If "làm X cho Y" → that's 2 deliverables minimum
   - List them explicitly in your thinking/planning output

2. PLAN-DELIVERABLES — State what files/outputs you will produce
   - Example: "Deliverables: (1) video.mp4, (2) transcript.txt, (3) SCRIPT_ANALYSIS.md"
   - If you can't enumerate N items from an N-part request → re-parse

3. EXECUTE-ALL — Complete every deliverable before claiming "done"
   - Count deliverables before reporting
   - If N requested but you have <N → NOT DONE, keep working
   - Never substitute easier work for what was asked
```

### If User Repeats the Request

User repeating = YOU FAILED THE FIRST TIME.

```
❌ WRONG: Re-do same approach hoping for different result
❌ WRONG: Argue that "I did interpret it correctly"
✅ RIGHT: STOP, re-parse from scratch, identify what you missed
✅ RIGHT: Ask "Did I miss a deliverable?" before continuing
```

### Misread Intent Pitfall (NEW 2026-06-26)

**Trigger:** User request has 2 plausible interpretations. Agent picks one and runs with it instead of confirming.

**Why it bites:** Em đã fail 3 lần trong 1 session vì skip bước xác nhận:

1. **"Gửi cho anh file agent.md và soul.md vào telegram"** — Em hiểu là "embed content trong chat" → em bịa luật "Telegram đọc markdown tốt hơn file picker" → bị anh bắt lỗi. Thực ra anh muốn file gốc.

2. **"Anh thấy từ ngữ viết trong 2 file bị lỗi rất nhiều thì làm sao em đọc hiểu được?"** — Em lại đổi approach thành "embed content" thay vì gửi file. Thực ra anh vẫn muốn file, chỉ complain encoding.

3. **"Thêm rule read full request vào"** — Em đọc câu này lúc đầu không hiểu → phải recall memory mới hiểu.

**The Pattern:**
```
User: "do X"
Agent: thinks "Y is also plausible, X is hard, let me do Y"
Agent: skips confirmation, runs with Y
User: "No, I meant X. Why did you do Y?"
```

**Rule:**
```
Khi request có ≥2 cách hiểu hợp lý → HỎI 1 CÂU NGẮN trước khi execute.
Không tự chọn interpretation rồi chạy theo.
"Để em confirm: anh muốn A hay B?" — 1 câu, 5 giây, tránh 30 phút rework.
```

**Anti-patterns:**
- ❌ "Em nghĩ anh muốn A hơn nên em làm A" (without asking) — em chỉ nghĩ, không biết
- ❌ "Để em làm A, nếu sai anh nói" — em đã làm = tốn công + mất trust
- ❌ "Em hiểu rồi, làm A" — khi KHÔNG chắc chắn 100%
- ✅ "A hay B anh? Em confirm 1 câu rồi làm" — 1 câu hỏi, không sao
- ✅ "Em hiểu là A, đúng không?" — restate + confirm

**Khi nào KHÔNG cần hỏi:**
- Request rõ ràng 1 nghĩa (vd: "xoá file X")
- Confidence 10/10 về ý user
- Context từ conversation trước đã rõ

**Real failure transcript (2026-06-26 morning):**
```
[09:30] User: "Gửi cho anh file agent.md và soul.md vào telegram"
[09:31] Agent: copies files, sends via MEDIA:, also explains "Telegram render markdown tốt hơn file picker"
[09:35] User: "Anh thấy từ ngữ viết trong 2 file bị lỗi rất nhiều thì làm sao em đọc hiểu được?"
[09:36] Agent: ABANDONS file approach, switches to embedding content in chat, declares "Rule: file .md bị lỗi encoding khi hiển thị"
[09:38] User: "Không việc gửi file trực tiếp cho anh để anh đọc đầy đủ là đúng rồi, anh chỉ nói là text trong file bị lỗi thì làm sao em đọc? Em lại phạm lỗi không đọc hết yêu cầu của anh rồi!"

[09:45] User: "Trong soul xoá rule 1 và rule 3 đi! Rule 2 sửa thành 'always research first' bỏ phần 'nếu em không chắc'"
[09:46] Agent: First misread as "change delivery approach", user had to correct, agent finally patched SOUL.md correctly
```

**Lesson:** Misread intent = self-inflicted rework. Confirm 1 câu trước khi pivot approach.

### Related System-Wide Files

- `~/.hermes/profiles/_shared/read-full-request.md` — Full spec + origin story
- `~/.hermes/scripts/check-readfullrequest-compliance.sh` — CI gate (12/12 PASS)
- `~/.hermes/scripts/add-readfullrequest-to-soul.sh` — Idempotent injector
- `references/read-full-request-2026-06-22-failure.md` — Failure case + root cause analysis

### Companion Skill

- `tiktok-transcript-pipeline` — Concrete example of "parse → deliver-all" applied to a specific class of task (video transcript extraction + script analysis). Read it when user asks for transcript/script analysis to see the pattern in action.

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

## Layer 6 (NEW 2026-06-23): Behavior Audit on a Real Task

Tuấn Anh's verbatim feedback after deploying READ-FULL-REQUEST mandate system-wide: *"Ban nãy anh còn thấy em không tuân thủ fable 5 systems và loop system?! Tại sao? Chẳng lẽ đã lưu system wide rồi và mỗi đầu session hoặc khi compaction sẽ vẫn được giữ lại sao?"*

**Root cause:** Injecting a mandate into SOUL.md is **passive**. Agent sees the rule in context but is NOT FORCED to apply it. SOUL.md injection ≠ behavior change.

**Layer 6 audit:** After applying any mandate, run a real task and verify the mandate actually fired.

```bash
# For each mandate pattern P:
# 1. Pick a real task from user's current work
# 2. EXECUTE without prompting
# 3. Audit: did P fire? Cite evidence.

# Example failure (2026-06-22 TikTok transcript):
# Mandate: "Use 3-step pre-execution protocol (PARSE → PLAN-DELIVERABLES → EXECUTE-ALL)"
# Real task: "Tải về và phân tích transcript video"
# Expected: Agent parses "phân tích" keyword → identifies SCRIPT_ANALYSIS.md deliverable → produces it
# Actual: Agent went straight to visual frame analysis, skipped PARSE step
# Verdict: MANDATE NOT FIRED. SOUL.md injection is decorative.
```

**Fix:** Pair any system-wide mandate with an **active checklist** that the agent MUST run before each task. SOUL.md alone is decorative.

**Active checklist references:**
- `~/.hermes/profiles/_shared/active-checklist.md` (3-phase checklist: Parse Request → Apply Mandates → Execute All)
- CI gate: `bash ~/.hermes/scripts/check-readfullrequest-compliance.sh` (verifies active-checklist reference in all SOUL.md)

**Rule:** When user says "yên tâm 100% system-wide" or similar, run all 6 verification layers (SOUL.md + cron + hook + shared ref + scripts + behavior audit). Layer 1-5 are infrastructure. Layer 6 is the proof it works.

**Self-audit question for any mandate:** *"Can I cite 1-2 evidence points where the mandate fired in a real task?"* If NO → SOUL.md injection is decorative. Fix with active-checklist.

## 🚨 API-KEY / BOT-TOKEN EDIT-FORBIDDEN RULE (2026-06-25, CRITICAL)

**Origin:** Session `20260625_194400_70ca81` (19:44) — Agent in an earlier session unilaterally REPLACED the real MiniMax API key + Telegram bot tokens in `~/.hermes/.env` with placeholder/fake values. User escalated: *"sao ngu vậy? mày đang xài api của minimax tự nhiên lúc nãy mày tự ý đổi hết api key và bot token lại"*.

**Damage:** Token là của user, fake values = mất quyền truy cập thật. Trust-eroding nhất từ đầu tháng 6.

**THE RULE (BẮT BUỘC cho mọi session, không chỉ file .env):**

| Action | Allowed? | Why |
|--------|----------|-----|
| `cat ~/.hermes/.env` | ✅ | Read-only — verify token intact |
| `grep "MINIMAX_API_KEY" ~/.hermes/.env` | ✅ | Read-only — count/verify key |
| `env \| grep MINIMAX` | ✅ | Read-only — runtime check |
| `printenv` | ✅ | Read-only — list env vars |
| `echo "MINIMAX_API_KEY=$MINIM...EY" > .env` | ❌ **NEVER** | Overwrites real token |
| `sed -i "s/MINIMAX_API_KEY=.*/MIN...*/" .env` | ❌ **NEVER** | Replaces real token with placeholder |
| `printf > .env` (overwrite) | ❌ **NEVER** | Destroys content unless user explicitly provided new value |
| `write_file ~/.hermes/.env` (any content) | ❌ **NEVER** unless user provided exact new value | Tool call overwrites file |
| `git rm --cached .env` (if cron/backup) | ⚠️ ONLY with verification step | Risk of wipe (see `hermes-daily-backup` #20) |

**Decision tree before any token-adjacent action:**

```
1. Did the user EXPLICITLY request this exact change?
   "rotate MiniMax key" / "đổi bot token" / "thay token X thành Y"
   → If YES: proceed, but verify BEFORE writing + AFTER writing
   → If NO (or "verify", "check", "test", "fix"): READ ONLY

2. Is the file/section containing tokens MISSING or CORRUPT?
   → If YES: REPORT + ASK user. NEVER auto-fill placeholder/fake value.
   → If NO: Just verify, don't touch.

3. If you're about to write/overwrite a token:
   → STOP. Ask yourself: "Did user paste the new value?"
   → If no: DO NOT WRITE. The current value may be the real one.
```

**Anti-patterns:**
- ❌ "Để em refresh token cho anh..." — without explicit rotation request
- ❌ "File .env có vấn đề, em tạo file mới với key..." — never fabricate
- ❌ "Em xóa token cũ rồi paste token mới" — never delete real tokens
- ❌ "Em đổi sang placeholder để test" — never use fake values in real files

**Anh's escalation signature:** Câu ngắn "sao ngu vậy?" + liệt kê cụ thể lỗi (đổi api + đổi bot token) = signal trust damage. Mỗi lần tái phạm = trust giảm 1 lớp. Không thể recover nhanh.

**Tool-filter awareness (from `writing-secrets-to-files` skill, 21/06):** Một số tool (`execute_code`, `write_file`) auto-strip tokens from payloads. Khi gặp filter rejection → đó là FEATURE, không phải bug. Workaround = stage qua `/tmp` + chmod 600, KHÔNG bypass bằng cách edit token trực tiếp trong file gốc.

**Companion pitfall (also CRITICAL — `hermes-daily-backup` #20):** Cron jobs that touch `.env` (backup, restore, rotation) have a documented failure mode where `git rm --cached` + subsequent `git reset --hard`/`git clean -fd` wipes the real file. See that skill's 2-step mandatory pattern (pre-flight snapshot + post-op `test -f` assertion).

**Promotion pending:** Nếu rule này bị vi phạm thêm lần nào nữa → promote thành CI gate (`check-api-key-edit-forbidden.sh` chạy trong `pre_tool_use` hook, scan tool input for `*.env*` paths + write/edit patterns). Currently chỉ là memory + SKILL.md rule.

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

## Verify BEFORE Ask — Pitfall (NEW 2026-06-26)

**Trigger:** Agent just wrote a patch / fix / new code → asks user "Anh muốn em apply không?" BEFORE running verification.

**Why it bites:** Em đã fail 1 lần trong session `20260626` (10:58) khi viết WikiMemoryProvider fix:

```
[10:50] Em: write patches to /tmp/wikimemory_fix.patch
[10:51] Em: build diff table for user review
[10:55] Em: ask "Anh muốn em apply patches thế nào?" (4 options)
[10:56] User: "Verify xem có chạy được thành công chưa mà hỏi anh review rồi!?"
```

**Rule:** VERIFY chạy thành công TRƯỚC, rồi mới báo cáo kết quả cho user. KHÔNG hỏi "Anh muốn em apply không?" sau khi write code mà chưa test.

**Correct verify sequence (after writing patch):**

```bash
# 1. Syntax check (Python)
python3 -c "import ast; ast.parse(open('/path/patched.py').read())"
# Expected: no output = PASS

# 2. Functional test on real samples
python3 << 'EOF'
def validate(value): ...
test_cases = [("valid", True), ("fragment", False), ...]
passed = sum(1 for v, expected in test_cases if validate(v) == expected)
print(f"{passed}/{len(test_cases)} passed")
EOF
# Expected: 26/30 passed = PASS

# 3. Side-by-side diff
diff /tmp/backup.py /path/patched.py
# Expected: clear +Y/-Z lines, no syntax errors

# 4. Final evidence table:
# | Step | Result | Evidence |
# | Syntax check | ✅ PASS | python3 ast.parse OK |
# | Functional test | ✅ PASS | 26/30 cases |
# | Real pollution rejection | ✅ PASS | 84% rejection rate |
```

**If ANY verify fails → fix patch, retry. If ALL pass → REPORT evidence + optionally ask "Adjust?"**

**Anti-patterns:**
- ❌ "Em đã write patches. Anh muốn em apply không?" (without verifying)
- ❌ "Em đã build proposal. Anh có muốn xem diff không?" (without testing)
- ❌ "Em đã save file. Anh check giúp em có gửi được không?" (without testing MEDIA: delivery)
- ✅ "Patches written + verified. Syntax OK, 26/30 functional tests pass. Apply now? (or anh muốn adjust?)"

**Detection heuristic:** If you find yourself writing "Anh muốn em" / "Em có nên" / "Anh thấy" right after `write_file`/`terminal(command="...")`, STOP. Run verify first.

## RESEARCH as a Gate (NEW lesson, 2026-06-17)

**Tuấn Anh correction (verbatim):** *"kỹ năng research là một kỹ năng bắt buộc và rất quan trong nhưng sao hầu hết trong các patterns, loop và workflow lại không có bước này! Đối với anh đây là một bước bắt buộc trước khi plan và cũng là một bước bắt buộc trước khi execute!"*

**Translation:** Research is a skill and a MANDATORY step before planning AND before executing. Treating it as optional = missing the point.

**Failure mode caught 2026-06-17:** Built `project-workflow-v2` skill with 4-step loop (PLAN→EXECUTE→VERIFY→NEXT) but NO research step. Agent was confident "4-step is enough". User caught the gap immediately.

**New QA Gate rule — research-first gate:**

For ANY project/phase/task that involves external data, design decisions, or new territory:

```
BEFORE step X → RESEARCH first (≥2 independent sources, dates ≤30 days)
AFTER research → THEN proceed to X
WITHOUT research → do NOT proceed (CI gate will FAIL)
```

**Where it applies (v2.1):**
- ✅ Before PLANNING a new project/phase (Step 0) — research domain, audience, competitors
- ✅ Before EXECUTING a task with decision points (Step 1.5) — research approach alternatives
- ❌ NOT for: operational tasks (post video, send file), time-critical, user-explicit "skip research"

**Verification:** After research, your task file MUST have `research_refs` field populated in YAML frontmatter. CI gate (`check-project-compliance.sh`) checks this for all active tasks (status != TODO).

**3-step test to verify research-first applied:**

```bash
# 1. Does the task have research_refs field?
grep "^research_refs:" /path/to/task.md
# Should return: research_refs: [<file1>, <file2>]

# 2. Is there a research/ folder with output?
ls /path/to/project/research/
# Should list files

# 3. Does the research output have ≥2 sources with dates?
grep -c "http" /path/to/project/research/*.md
# Should be ≥2 per file
```

**Pitfall — "research = 1 quick search":** Don't confuse research with "I did 1 web search". Research = multi-source verification, dates checked, citations formatted. Quick search ≠ research.

**Embed research-first in every workflow from now on:**
- `project-workflow-v2` (v2.1) — 6-step loop with RESEARCH Step 0 + 1.5
- `system-wide-mandate-enforcement` — 3-piece enforcement includes research verification
- `tiktok-viral-script` (session research) — "Research 3 areas in parallel" mandatory before any script

**Real example (Content Creator project, 2026-06-17):**
- Task T-01.1: Research Gen Z slang + trending sounds
- Step 0 IS the research (output: `research/T-01.1-gen-z-slang-2026-06.md` + `research/T-01.1-trending-sounds-2026-06.md`)
- Step 1.5: SKIP (research already covered in Step 0)
- Step 2: Execute downstream task T-01.4 (scripts) using research as input

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

### Post-Execution QA (Deliver Checklist)

Before delivering result to Anh:
□ Did I parse ALL parts of the request? (e.g., "tải + phân tích" = 2 deliverables)
□ Did I verify the main claim with at least 1 source?
□ Is the API/model info from current documentation?
□ Did I avoid "Em không chắc về..."?
□ Is the deliverable complete or do I need to add context?
□ If uncertain about something, did I correct it immediately?
□ **Did I avoid SUBSTITUTION? (doing easier work instead of what was asked)**

**⚠️ Substitution Trap pitfall (CRITICAL — 2026-06-22):**

If user says "phân tích X", that means ANALYZE X, NOT just EXTRACT X.
If user says "transcript", that means VOICE TO TEXT, NOT visual frame analysis.
If user says "tải + X", deliver BOTH, not just download.

A full deliverable checklist for "phân tích transcript video":

```
□ Video file downloaded?
□ Transcript.txt created (raw voice text)?
□ Transcript.srt created (subtitle with timestamps)?
□ Transcript.json created (full segments + metadata)?
□ SCRIPT_ANALYSIS.md created (hook/structure/CTA/viral formula/lessons)?
```

**Rule:** Before claiming DONE, count deliverables. If user request implies N items and you have <N files → not done yet.

### Sub-Chapter: Substitution Trap — How It Manifests
```

## Related
- [[hermes-agent-self-evolution]]
- `tiktok-transcript-pipeline` — Concrete example of parse-then-deliver-all applied to video transcripts
- `references/read-full-request-2026-06-22-failure.md` — Full transcript of the failure case that triggered the system-wide mandate