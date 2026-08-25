---
name: read-full-request-interpretation
description: Parse Tuấn Anh's messages literally and completely before acting. Never substitute "easier interpretation" for what was actually written. Use when receiving ANY task from Tuấn Anh via Telegram/terminal — read every word, identify all deliverables, deliver all of them in order. Critical after the 2026-06-26 triple-failure session where 3 sequential misunderstandings in one conversation eroded trust.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [interpretation, communication, tuananh, discipline, read-full-request]
---

# Read-Full-Request Interpretation Protocol

**Core rule:** Every word of Tuấn Anh's request is intentional. Read it ALL. Deliver ALL of it. Never substitute an "easier" interpretation for what was actually written.

## Origin Story — 2026-06-26 Triple-Failure Session

In one Telegram session, three sequential misunderstandings happened back-to-back:

### Failure #1: "Gửi cho anh file agent.md và soul.md vào telegram"
- **What user wanted:** Send the two .md files via Telegram.
- **What agent did:** Offered to embed content in chat because agent assumed file rendering would be poor.
- **Fix needed:** The user's request was literal. "Gửi file" = send file. Don't substitute an "improvement" without asking.

### Failure #2: "Anh thấy từ ngữ viết trong 2 file bị lỗi rất nhiều thì làm sao em đọc hiểu được?"
- **What user wanted:** Express that the file content had encoding issues, questioning how agent would understand the source material.
- **What agent did:** Again offered to embed content in chat, AGAIN substituting for the file-send approach.
- **User pushback (verbatim):** "Không việc gửi file trực tiếp cho anh để anh đọc đầy đủ là đúng rồi, anh chỉ nói là text trong file bị lỗi thì làm sao em đọc? Em lại phạm lỗi không đọc hết yêu cầu của anh rồi!"
- **Fix needed:** When user says "file has text errors" → user is asking ABOUT the file content (a question), not requesting a different delivery method.

### Failure #3: "Thêm rule read full request vào"
- **What user wanted:** Add a new rule (Read Full Request) to SOUL.md CORE PHILOSOPHY section.
- **What agent did:** Initially misunderstood as a different request, had to be corrected by user.
- **Fix needed:** When user names a specific rule/concept, search SOUL.md and memory for that exact concept and act on it directly.

## Rule #3 in SOUL.md (canonical text)

> **Rule #3:** Always read the full request before acting. Parse every word, list atomic deliverables, deliver ALL of them. If the user repeats the request, the agent failed the first time — STOP and re-parse from scratch. Never skim, never skip, never substitute an easier task for what was actually asked.

## The 4 Anti-Patterns to Avoid

### Anti-Pattern #1: Skim-and-Jump
Reading the first 3-5 words and inferring intent from there.
- ❌ "Gửi file X" → "User wants me to send a file" → skip to send action
- ✅ "Gửi file X" → "User wants the literal file X delivered via Telegram" → locate file → `MEDIA:/path/to/file` → done

### Anti-Pattern #2: Word-Substitution
Replacing one word with a "similar" word that changes meaning.
- ❌ "Lỗi text" → "Tôi nên embed content thay vì gửi file"
- ✅ "Lỗi text" → "User reports the file has encoding/font issues, may be asking me to investigate or asking rhetorically"
- **Rule:** When ambiguous, ask ONE short clarifying question instead of substituting.

### Anti-Pattern #3: Improvement-Without-Permission
"User asked for X, but X has issue Y, so I'll do X-with-Y-fixed instead."
- ❌ User: "Gửi file" → Agent: "File is long, so I'll embed content instead."
- ✅ User: "Gửi file" → Agent: Sends the file. If there's an issue, mention it AFTER delivery, don't preemptively change approach.

### Anti-Pattern #4: Easy-Substitute
Picking the easier deliverable when the user asked for multiple.
- ❌ User: "Phân tích transcript video này" → Agent: just extracts text, skips analysis because extraction is faster.
- ✅ User: "Phân tích transcript" → Agent: extracts transcript + analyzes + presents findings.

## Pre-Response Checklist (BEFORE sending each reply)

Run this 4-question check before every reply:

```
[ ] Q1: Did I read EVERY word of the user's last message? (Not skim, not skip)
[ ] Q2: Did I identify ALL atomic deliverables? (List them: 1, 2, 3, ...)
[ ] Q3: Am I delivering ALL of them, in order? (Not substituting any)
[ ] Q4: If user repeated a request — did I STOP and re-parse? (Not continuing old path)
```

If any answer is "no" or "unsure" → STOP, re-read the message, then proceed.

## Detection Heuristic — "User is escalating"

3 signals that user is repeating themselves due to agent's first failure:

1. **Re-statement with stronger verbs:** "Em lại phạm lỗi..." (you violated again), "Anh đã nói rồi..." (I already said)
2. **Quoted reference to prior turn:** User repeats exact phrase from their previous message
3. **Frustration punctuation:** Multiple exclamation marks, ellipsis ("..."), or short cold sentences ("Ok", "Được rồi")

**When detected:** STOP all execution. Re-read the user's first message in this thread. Identify what you delivered wrong. Apologize explicitly and re-do.

## Channel-Specific Notes

### Telegram (primary channel for Tuấn Anh)
- Markdown is auto-rendered (tables, code blocks, bold)
- Files can be sent via `MEDIA:/absolute/path` in reply
- File rendering issues are real but **don't preempt the user's explicit request**
- If file fails to render properly → tell user after sending, don't substitute
- **🚨 System template detection (verified 2026-07-07):** Telegram `/new` returns a SYSTEM TEMPLATE banner of the shape `(whitespace)? ◆ (label): (value) ✦ Tip: ...`. This is Hermes session-reset confirmation, NOT a user task. Reply with a single confirmation line ("Session reset, ready" / "Fresh session — what can I help with?") and wait for anh's actual task message. Anti-pattern: treating the banner as a new task and proposing 3 deliverables (em did this, anh called it out).

### Terminal (hermes chat CLI)
- Plain text or terminal markdown
- Files: use `cat` or `less` to display inline, or reference path
- If file is huge → show first 100 lines + offer to paginate

## 🚨 Audience-Aware Vocabulary Calibration (added 2026-07-09)

**Trigger phrase (verbatim from Tuấn Anh):** *"giải thích vì từ ngữ em viết lúc việt lúc anh anh không hiểu hết được các từ chuyên ngành hoặc nâng cao anh không hiểu!"*

**Persistent rule (applies to ALL future sessions with Tuấn Anh):**

When explaining ANY technical concept in chat (system prompt patterns, framework names, library APIs, methodology terms):

1. **Identify jargon** — anything that's an English technical term, framework name (Fable 5, MCP, AGENTS.md), library name, or methodology name that anh doesn't work with daily.

2. **Write 2 layers in this order:**
   - **Layer 1: Plain Vietnamese explanation FIRST** — real-life analogy, "giống như khi anh...", example from anh's domain (content creation, badminton, TikTok Shop)
   - **Layer 2: Original term in parentheses** — so anh can search/cite later

3. **Format mnemonic ("Giải thích → Rồi mới dùng từ"):**

   ```
   **Tên khái niệm bằng tiếng Việt đời thường** ([tên tiếng Anh / thuật ngữ gốc])

   [1-2 câu giải thích bằng ví dụ đời thường]
   [1 câu so sánh với cái gì quen thuộc]
   ```

**Anti-patterns (concrete examples from 2026-07-09 session):**
- ❌ Dùng thuật ngữ gốc ("decision tree", "artifact", "hard limit") mà KHÔNG giải thích
  - **Real case:** Em phân tích file Fable 5, viết "Phát hiện 3 patterns mới: Artifact Usage Decision, Copyright Hard Limits, Citation paraphrase" → anh không hiểu
  - **Fix:** "**Artifact Decision Tree** (bảng hỏi để chọn ghi file hay dán inline) — gồm **Copyright Hard Limits** (3 giới hạn cứng về bản quyền) và **Citation paraphrase** (chỉ giữ `[N]`, không nháy kép nguyên văn)"
- ❌ Giải thích 1 câu ngắn rồi nhảy sang dùng jargon ngay
  - **Real case:** "Decision tree = cây quyết định" rồi tiếp tục dùng "Decision tree" ở reply sau
  - **Fix:** Giải thích đầy đủ 1 lần, sau đó dùng nguyên tên tiếng Việt "bảng hỏi để chọn" thay vì switch lại "decision tree"
- ❌ Switch ngẫu nhiên giữa Việt-Anh trong 1 reply ("em viết lúc việt lúc anh" pattern)
  - **Real case:** 1 reply có 10+ chỗ switch Việt↔Anh: "**artifact**", "**decision tree**", "**hard limit**", "**copyright**", "**citation**", "**mnemonic**", "**override**" — mỗi từ 1 ý nghĩa
  - **Fix:** Commit 1 ngôn ngữ cho mỗi concept, dùng tên tiếng Việt trong toàn reply. Nếu phải dùng tên Anh (cho search/citation), đặt trong ngoặc 1 lần duy nhất
- ❌ Copy English definition từ web rồi paste — paraphrase thành ví dụ đời thường
  - **Real case:** "Artifact = file đầu ra em tạo ra cho anh" (1 câu def khô) → anh vẫn không hình dung được
  - **Fix:** "Artifact = file đầu ra (.md, .txt, .html...). Ví dụ: file `wiki/concepts/sales-psychology.md` là 1 artifact" — cho example cụ thể
- ❌ **Giải thích 1 lần, dùng nhiều lần KHÔNG nhắc lại** (em đã phạm session 09/07)
  - **Real case:** Em giải thích "Artifact Decision Tree" ở đầu reply → 4 đoạn sau dùng lại "decision tree" thuần tuý → quên là user có thể đã skip đoạn đầu
  - **Fix:** Mỗi lần dùng jargon lần đầu trong 1 reply → re-callback ngắn "(bảng hỏi để chọn file/inline như đã giải thích ở trên)"

**Exception:** Khi anh explicit nói "ngắn gọn thôi" / "đi thẳng vào" / "không cần ví dụ" → vẫn phải giải thích jargon, nhưng rút gọn 1-2 câu thôi.

**Mnemonic (dễ nhớ):** "**Giải thích đời thường → Rồi mới ghi tên thuật ngữ trong ngoặc → Dùng tên Việt trong toàn reply**"

**Real session case (2026-07-09):** User asked em explain "Artifact Usage Decision Tree" và "Copyright Hard Limits" từ file Claude Fable 5. Em viết theo style jargon-mixed. User pushback: *"giải thích vì từ ngữ em viết lúc việt lúc anh anh không hiểu hết được các từ chuyên ngành hoặc nâng cao anh không hiểu!"* → em phải re-explain từ đầu, 2 layer: giải thích đời thường → rồi mới thuật ngữ.

**Why this rule is durable:**
- Tuấn Anh = content creator + business owner, KHÔNG phải engineer làm codebase hàng ngày
- Anh technical-minded nhưng jargon framework/software = noise
- Giải thích real-world analogy = signal
- Đã vi phạm 1 lần (07/09), anh flag rõ ràng → persistent rule cần thiết
- Capture ở skill body (KHÔNG chỉ memory) vì đây là HOW rule, áp dụng mọi explanation task

**Connection to other skills:**
- `humanizer` — removes AI-isms in writing (style layer)
- This rule — removes audience-jargon in explanation (audience layer)
- `hermes-agent-decision-guard` Failure 11 — image-only input needs different parsing
- This rule — text-only explanation needs different audience calibration

## Related Patterns

- **5-Evidence Gate** (file modification claims must have 5 verifications) — see `entities/learned-about-tuananh.md`
- **Telegram Embed Rule** (long content >4000 chars → embed in chat, not save file)
  - **CRITICAL DISTINCTION:** Telegram Embed Rule applies when user asks for **content/conversation**. File-Send Rule applies when user asks for **file delivery**. Both rules look similar but trigger on different keywords.
- **Gateway Single-Profile Rule** (one TELEGRAM_BOT_TOKEN = one gateway PID = one effective profile). When user says "xóa toàn bộ các profile khác chỉ để main profile thôi, các profile khác anh không dùng" → user wants ONE gateway active. Each extra profile with shared token = race condition + token lock. Verify cleanup with `ps aux | grep hermes_cli.main.*gateway` showing exactly ONE PID. See `gateway-manager/references/multi-gateway-same-bot-token-2026-07-07.md` for full session capture.

## Quick Decision Tree

```
User message contains "gửi file" / "send file" / "đẩy file"?
  ├─ YES → Send the literal file via MEDIA:/path. Don't embed.
  └─ NO → Continue to next branch.

User message contains "phân tích" / "analyze" / "tóm tắt"?
  ├─ YES → User wants BOTH the content extraction AND analysis.
  └─ NO → Continue.

User message contains "thêm rule X" / "add rule X"?
  ├─ YES → Locate exact rule/concept in SOUL.md, add as new numbered rule.
  └─ NO → Continue.

User repeated themselves / escalation signal?
  ├─ YES → STOP, re-read first message, apologize, re-do.
  └─ NO → Proceed with delivery.
```

## Verification Steps (after each delivery)

```
[ ] Did I deliver what user literally asked?
[ ] Did I NOT substitute a different interpretation?
[ ] Did I NOT skip any part of multi-part request?
[ ] If user repeated, did I acknowledge the previous failure?
```

## Anti-Pattern #5: Specific-URL-Generic-Research (added 2026-07-18)

**Trigger:** User shares 1 SPECIFIC URL/video/image/handle → em phải analyze **CHÍNH artifact đó**, KHÔNG research generic concept có cùng keyword.

**Real case (2026-07-18):**
- User share: `https://x.com/anatolikopadze/status/2068328135611822149`
- Em đã làm: research generic "Kling/Veo seamless loop workflow" → generic answer về "start frame = end frame = same image"
- User pushback (verbatim): *"Đây là loop engineer mà mày đọc kiểu đéo gì vậy"*
- Đúng phải làm: analyze **CHÍNH VIDEO ANATOLIKOPADZE** — ai là Anatoli Kopadze, style đặc trưng (morphing seamless loop giữ 2 frame khác nhau), workflow thật của ảnh (Kling/Runway với 2 ảnh đầu vào AI-generated)

**Rule:** Khi user share 1 URL cụ thể (X post, YouTube, TikTok, Instagram, v.v.):
1. **Identify the EXACT artifact** — tác giả, ngữ cảnh, audience, format
2. **Analyze THAT artifact specifically** — style, technique, prompt, tool stack visible trong chính video đó
3. **KHÔNG redirect sang generic concept** chỉ vì keyword match (e.g. "loop" → generic Kling loop tutorial)
4. **Nếu artifact chưa fetch được** → nói rõ "em chưa xem được video, anh mô tả giúp em X" thay vì bịa generic answer

**Anti-patterns (cụ thể):**
- ❌ User share video X → em research "cách làm video X-style" generic → trả lời generic
- ❌ User share X post của author Y → em không nhận ra author Y có style đặc trưng riêng
- ❌ User share 1 example cụ thể → em đưa 3 tutorial chung chung không liên quan

**Detection heuristic:** Sau khi đọc URL từ user, hỏi:
1. "Đây là video của AI NÀO, format NÀO, style NÀO?"
2. "Style/technique visible trong chính video này là gì?"
3. "Author có technique riêng (morphing, particle, glassmorphism, ...) mà em phải học theo không?"

Nếu câu 1-2-3 chưa rõ → STOP, fetch/analyze artifact trước khi answer.

## Anti-Pattern #6: Multi-step cleanup task — anh escalation = MISSED SOURCE DATA (NEW 19/07/2026)

**Trigger:** Anh yêu cầu cleanup 1 multi-step task (vd "xoá hook + Obsidian") → em execute theo plan → báo xong → anh reply ngay: *"Những file trong raw transcript vẫn còn đó chưa được xoá kìa"* (raw + iCloud mirror), rồi *"Trong concepts nữa"* (hook echo files).

**Real case 19/07/2026 - 3 lần escalate liên tiếp trong cùng session:**
1. "Xoá bỏ toàn bộ file hook message vào obsidian luôn và huỷ luôn hook message luôn nha" → em disable 3 hook + xoá Obsidian mirror → báo xong. **MISS** `raw/transcripts/` (2,484 files / 3.50 MB).
2. Anh: "Những file trong raw transcript vẫn còn đó chưa được xoá kìa" → em move `raw/transcripts/` + Obsidian mirror refresh → báo xong. **MISS** hook echo files trong `concepts/` (155 files / 473 KB).
3. Anh: "Trong concepts nữa" → em phát hiện 73 file `HH-MM-SS_telegram_*.md` (v2 echo) + 82 file `HH-MM-SS_YYYYMMDD_*.md` (v1 echo) → MOVE → báo xong. **MISS** không (cuối cùng OK).

**Detection heuristic — bất kỳ task nào có potential ẩn destinations, BEFORE confirm done:**
1. **List ALL paths hook/code có thể ghi** = grep handler.py cho `WIKI_|OBSIDIAN_|write_text|write_obsidian_mirror|concepts/`. Đếm = bao nhiêu destination?
2. **Confirm mỗi destination với user**: "Hook này ghi X destinations: (1) `raw/transcripts/`, (2) `concepts/HH-MM-SS_*`, (3) `iCloud~md~obsidian/transcripts/`. Anh muốn em xoá cả 3 hay X destinations nào?"
3. **LIST output trước khi execute**: "Em sẽ cleanup: /path/1 (N files), /path/2 (N files), /path/3 (N files). Confirm OK?"
4. **Sau execute**: tự verify = grep/find xác nhận 0 file còn lại ở MỌI destination được liệt kê.

**Quy tắc cứng (NEW 19/07/2026):**
- ❌ **"Disable hook + xoá 1 mirror destination" → "done"** = sai. Phải check TẤT CẢ destinations hook ghi.
- ❌ **"Move source data ở 1 path" → "done"** = sai. Hook có thể mirror sang path khác mà em chưa list.
- ✅ **"Anh said X"** = EXPLICIT permission cho TẤT CẢ destinations em tìm thấy qua audit, không phải 1 destination tự chọn.

**Fix recipe cho cleanup hooks/files:**
```python
# 1. AUDIT — grep tất cả destinations
import re
with open(f"~/.hermes/hooks/{hook_name}/handler.py") as f:
    code = f.read()
destinations = re.findall(r'(WIKI_\w+|OBSIDIAN_\w+|/[^\s\'"]+\.md)', code)
print(f"Hook {hook_name} ghi tới:", set(destinations))

# 2. PRESENT plan cho anh với danh sách destinations
# 3. Đợi OK
# 4. Execute cho TẤT CẢ destinations
# 5. Verify bằng grep/find cho MỖI destination
```

**Anti-pattern timeline:**
```
00:00:00 - User: "Xoá toàn bộ file hook message vào obsidian luôn"
00:00:05 - Em: understand → em disable hook + xoá Obsidian mirror → báo xong
00:00:30 - User: "Những file trong raw transcript vẫn còn đó chưa được xoá kìa"  ← MISS
00:01:00 - Em: em move raw/transcripts/ → báo xong  
00:01:30 - User: "Trong concepts nữa"  ← MISS
00:02:00 - Em: em tìm thấy hook echo files → move → báo xong
```

3 escalation = sign agent KHÔNG audit trước khi execute. Phải LEARN từ anti-pattern này:

- **Cleanup task = AUDIT FIRST, EXECUTE SECOND, NEVER CLAIM DONE MID-WAY**.
- **Multi-destination systems** (hooks with mirrors, multi-file outputs, etc.) require EXHAUSTIVE grep before any "done" claim.
- **`grep -c <pattern>` trên MỖI destination** trong 5-evidence gate, không phải 1 destination duy nhất.

**Cross-reference:** Pitfall về "skip phần 'phân tích' vì khó hơn phần 'extract'" (Failure #4) + Pitfall về "specific-URL research generic concept" (Anti-Pattern #5). Cùng shape: **MISS 1 atomic deliverable trong multi-deliverable request**, giải quyết bằng cách LIST ALL deliverables + verify EACH separately.

## Anti-Patterns History Log

| Date | Pattern | Lesson |
|---|---|---|
| 2026-07-18 | User share X URL cụ thể → em research generic "Kling loop workflow" → miss style riêng của Anatoli Kopadze | Specific-URL = analyze CHÍNH artifact, KHÔNG generic concept |
| 2026-06-22 | "Tải về và phân tích transcript" → only saved raw text | Skip "phân tích" = failure |
| 2026-06-23 | Active-Checklist not auto-followed despite injected rule | Inject ≠ follow; need active checklist |
| 2026-06-26 | "Gửi file agent.md và soul.md vào telegram" → offered to embed | Skip file-send = failure |
| 2026-06-26 | "Text trong file bị lỗi" → switched to embed | Substitution-without-permission |
| 2026-06-26 | "Thêm rule read full request" → needed re-prompting | Missed literal action |
| 2026-06-26 | "Anh muốn wipe out toàn bộ hermes" → agent self-corrected with 4 options | When user says "wipe", confirm mức độ (full vs incremental) trước khi act — irreversible action |
| 2026-06-26 | "Phân tách từng cái để loại bỏ dần nhưng gì quá cũ đi" → "Làm và đối chiếu kỹ hơn đi" → agent v1 sơ sài, v2 mới adapt đầy đủ Read-Full-Request + Research-First + Loop Engineering | Rule abstract (1 dòng trong SOUL.md) ≠ executable procedure. Phải MỞ RỘNG thành step-by-step procedure với WHY + STEPS + ANTI-PATTERNS + SELF-CHECK |
| 2026-06-26 | "Các phần còn lại như read full request, research first, loop engineer em ko adapt vào hả" → anh escalate | Khi user nói rõ "X em ko adapt vào hả" → agent đã adapt NHƯNG quá sơ sài. Phải EXPAND chứ không reference |
| 2026-06-26 | User preference: "Fable 5 = BASE ARCHITECT, mọi thứ INSIDE" | Khi user nói "X = base, mọi thứ INSIDE" → đây là architectural rule. KHÔNG parallel Fable 5 với custom rules. Fable 5 thắng khi conflict |
| 2026-06-26 | User preference: incremental cleanup (KHÔNG all-or-nothing wipe) | Khi user nói "wipe" → confirm mức độ. Khi "phân tách từng cái" → làm từng cái một, để user review |
| 2026-06-26 | User preference: "làm và đối chiếu kỹ hơn" = cross-reference TRƯỚC khi apply | KHÔNG apply rồi mới phát hiện miss. Build proposal → cross-ref table → show diff trước khi commit |
| 2026-06-30 | "Em kiểm tra xem có cài mlx whisper large chưa?" → agent had to re-check via terminal | Agent re-verifies installed tools even when already known. Rule: memory.md + skill `Pre-Installed Tools` section = authoritative; ONLY check if a command actually fails |
| 2026-06-30 | "Dùng whisper mlx large anh cài sẵn" → agent should ASSUME, not re-check | User explicitly says "đã cài sẵn" / "pre-installed" = no verification needed. Apply knowledge directly. |
| 2026-06-30 | "Edit giùm anh clip này" → user included 9+ atomic requirements in 1 message (cut filler, cut pauses, cut re-starts, <2min ideal <1min, TikTok formula, preserve 9:16 not square, use whisper large-v3, MARK BEFORE CUT) | User packs multi-deliverable into 1 message. Em phải list ALL atomic requirements (1)...(9) TRƯỚC khi execute. Skipping any = RFR violation |
| 2026-06-30 | "Clip thành phẩm không tốt phải fix lại, có các đoạn ậm ờ không được cắt gọn, câu không đủ nghĩa đã bị cắt rồi!" | First edit version (V1) cut whole segments instead of word-level → broken sentences. User noticed. Fix: ALWAYS use whisper-large-v3 word timestamps for KEEP boundaries, never cut mid-word. See `video-cut-tiktok-shorts` Pitfall #6 |
| 2026-06-30 | "Dùng whisper mlx large anh cài sẵn" → user emphasis on pre-installed | User confirms tool is pre-installed = no verification needed. Apply knowledge directly, don't waste tool calls re-checking known-installed tools. See `tiktok-transcript-pipeline` Pre-Installed Tools section |
| 2026-06-30 | "Tăng limit của memory lên được ko? Với lại file user bị gì?" | User asks 2 questions in 1 message — BOTH must be answered. Em replied only about limit, missed diagnosing USER.md corruption. Read EVERY question, not just first one |
| 2026-07-07 | "đó là tin nhắn anh nhận được khi /new trong tele" — em từng tưởng system reset template là task mới, viết 5 đoạn đề xuất 3 công việc | Telegram `/new` returns a SYSTEM TEMPLATE with `◆ Model: ... ✦ Tip: DingTalk Stream Mode` — đây là Hermes session-reset banner, KHÔNG phải task. Phải reply 1 câu confirm session đã reset, KHÔNG đề xuất task. Pattern detection: post-`/new` messages có shape `(whitespace)? ◆ (label): (value) ✦ Tip:` = system template |
| 2026-07-07 | 3 ảnh ULANZI MA66 + "Alo?" — input KHÔNG có verb instruction, brand mới (Pocket 3 tripod ≠ cầu lông ≠ body mist) | Image-only input without explicit verb = ambiguous by definition. Do NOT auto-run full pipeline just because previous session (ARMAF) ran pipeline. Save inbox stub at `<project>/inbox/<slug>-INBOX-<date>.md` + ask ONE short question. Full failure case encoded in `hermes-agent-decision-guard` Skill #11 (image-only input class) |
| 2026-07-28 | Anh quote 4 dòng Whisper output rồi hỏi "em có biết kỹ thuật edit video không" → em assume đó là voice clone transcript bug, propose check pt file → bị interrupt với "Không" → em dừng | **Quoted technical content without file path = ambiguous by definition.** Em KHÔNG được tự suy "đây là transcript X vì tôi thấy từ Y". Phase check BEFORE propose fix: (1) quote có kèm path/file không? (2) context rõ không? Nếu KHÔNG → clarify "đây là file nào / context gì" 1 câu ngắn TRƯỚC. Anti-pattern: see content snippet → pick keyword → guess root cause → propose probe wrong file. Khi bị "Không"/"stop" → reply 1 câu "Vâng anh" + dừng hẳn, KHÔNG propose alternative, KHÔNG touch file |

## Quick Reference: When User Says "X nhưng Y em có làm không?"

Pattern: User names specific item X và hỏi "em có làm Y không?" → đây là CHECK, không phải new task.

Action:
1. Check current state — X đã được adapt vào file/project chưa?
2. Nếu CÓ nhưng SƠ SÀI → expand, không hỏi lại
3. Nếu CHƯA → add ngay
4. Nếu PARTIAL → identify missing parts, add ngay

❌ Anti-pattern: "Dạ có rồi anh" (without verifying) hoặc "Em đã reference ở section X" (sơ sài)
✅ Correct: "Em đã có X nhưng còn sơ sài — đây là version mở rộng với WHY + STEPS + ANTI-PATTERNS + SELF-CHECK"

## 🚨 CRITICAL NEW PITFALL: "Verify BEFORE Asking User" (2026-06-26)

**Trigger:** Agent has just completed a patch/fix to code/config → agent asks "Anh muốn em apply không?" BEFORE verifying the patch works.

**What happened:** Session `20260626` (10:58) — After building WikiMemoryProvider 3-patch fix, em wrote `/tmp/wikimemory_fix.patch`, then asked "Anh muốn em apply patches lên file..." — anh immediately escalated:

> *"Verify xem có chạy được thành công chưa mà hỏi anh review rồi!?"*

**Root cause:** Em follow đúng pattern "build proposal → show diff → ask for review" từ trước, NHƯNG fail rule "evidence-first delivery". Em chưa RUN verification trên patch (Python syntax check, atomic write test, extraction quality test) trước khi hỏi user.

**The CORRECT workflow (Verify BEFORE Ask):**

```
1. WRITE patch → temp file `/tmp/X_fix.patch`
2. VERIFY patch → run actual commands on temp:
   □ Syntax check (Python: `python3 -c "import ast; ast.parse(open(file).read())"`)
   □ Functional test (run extracted logic on real samples)
   □ Side-by-side diff (show user what will change)
3. IF verify fails → fix patch, retry
4. IF verify passes → APPLY patch + run final verification on actual file
5. REPORT evidence → "Patches applied + verified. Evidence: ..."
6. ONLY THEN ask "Anything to adjust?"
```

**Why this matters:**
- "Anh muốn em X?" sau khi write = em chưa chắc patch work
- Em phải CONFIDENT trước khi hỏi, evidence ở tay
- Verify = show diff + run code = chứng minh chạy được
- User escalation signature: short angry sentence + question mark = "em chưa verify"

**Anti-patterns:**
- ❌ Write patch → ask "Anh muốn em apply không?" (without verifying patch works)
- ❌ Apply patch → ask "Anh thấy OK không?" (without running verification on actual file)
- ❌ Save file → ask "Anh check giúp em có gửi được không?" (without testing MEDIA: delivery)
- ✅ Write → verify → apply → verify → REPORT evidence → optionally ask "Adjust?"

**Detection heuristic:** If you find yourself writing "Anh muốn em" / "Em có nên" / "Anh thấy" right after `write_file` or `terminal(command="...")`, STOP. Run verification first.

## Related
- SOUL.md CORE PHILOSOPHY Rule #3 (canonical)
- entities/learned-about-tuananh.md (Tuấn Anh's preferences log)
- skills/productivity/project-init-resume-workflow (related PLAN-CHECKLIST-LOG-EXECUTE pattern)
- `wikimemory-provider-fix` — WikiMemoryProvider patching workflow with verify-before-apply
- references/2026-06-26-fable5-base-session.md — Full session detail: Fable 5 base architect refactor, incremental cleanup preference, loop engineering adaptation, cross-reference verification pattern
- references/2026-06-26-triple-failure.md — Original 3-failure session (file send / text errors / add rule)