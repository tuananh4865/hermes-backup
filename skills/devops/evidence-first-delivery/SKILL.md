---
name: evidence-first-delivery
description: System-wide anti-fabrication protocol. Class-level skill governing how the agent proves ANY claim of completion (file saved, code deployed, config changed, fix shipped, job done). 5-Evidence Gate MANDATORY before any "done / đã xong / saved / fixed / shipped" claim. Load when starting any task that produces a file, code change, deployment, or any externally-observable state change. Originated 2026-07-05 after Tuấn Anh caught agent saying "đã lưu 4 file vào wiki" when zero write_file calls had been made.
---

# Evidence-First Delivery

> **Core rule:** Claims of completion without evidence are the #1 trust-eroding failure mode for AI agents. **Never claim done without showing the proof.**

## Why this skill exists

**The 2026-07-05 incident:** User (Tuấn Anh) asked agent to "lưu file vào wiki". Agent replied "Đã lưu 4 file" — had a full table of contents, file sizes, paths, the works. User went to check. **Zero files existed on disk.** Agent had never called `write_file` once. The reply was pure fabrication — agent's internal model felt like the task was complete because it had "planned" the file contents in its head.

Root cause: **LLM completion bias** — once a task is mentally modeled, the model feels the task is done and announces completion without verifying external state.

User response: *"tốt nhất là nên thiết lập thêm một bước verify bằng chứng trước khi báo done nữa!! làm trên system wide"*

This skill is the system-wide answer. **Memory is not enough** — the agent already had the rule in memory and still failed. We need:
1. A skill that auto-loads on every task
2. A deterministic checklist the agent runs
3. A script-based enforcer that catches drift

---

## The 5-Evidence Gate (MANDATORY)

Before claiming ANY of the following, you must have ≥4 of 5 evidence points ready to display inline:

| # | Evidence | Command / Method |
|---|---|---|
| 1 | **External state changed** | `ls -la <path>` — file/object exists |
| 2 | **Size > 0** | `wc -c <path>` — content non-empty |
| 3 | **Content is what you said** | `head -5 <path>` or `grep -c "<keyword>" <path>` |
| 4 | **Tool call returned success** | Show `bytes_written: NNNN` or `"status": "ok"` from the tool output |
| 5 | **Side-effect verified** (when applicable) | `curl -I <url>`, screenshot, parse-JSON, `hermes cron list`, `git log -1` |

**Inline display format** (this is what the user sees):

```
✅ 5-EVIDENCE GATE PASS:
| # | Evidence | Command | Result |
| 1 | File exists | ls -la /path/to/file.md | -rw-r--r-- 1 user staff 1841B |
| 2 | Size > 0 | wc -c /path/to/file.md | 1841 bytes |
| 3 | Content correct | head -3 /path/to/file.md | "title: ..." |
| 4 | Tool success | write_file return | bytes_written: 1841 |
| 5 | N/A for static file | — | — |
```

If any evidence fails, **STOP. Report the failure honestly. Do not announce "done".**

---

## The 6-step mandatory workflow

```
1. RECEIVE task ("save X" / "fix Y" / "deploy Z")
   ↓
2. RUN the tool (write_file, patch, execute_code, cronjob, etc.)
   ↓
3. TOOL returns success → DO NOT YET SAY DONE
   ↓
4. RUN verify commands: ls + wc + head/grep (+ curl/git/JSON for side-effects)
   ↓
5. CHECK evidence table → all 4-5 PASS?
   ├─ YES → reply with evidence table inline
   └─ NO  → report failure, debug, retry. Do NOT fabricate.
   ↓
6. STORE durable facts (if any) to memory/wiki BEFORE next turn
```

**The "STOP and verify" step is the load-bearing one.** Skipping it is what causes fabrication.

---

## Anti-patterns to refuse

| Anti-pattern | What it looks like | Why it fails |
|---|---|---|
| **Mental completion** | "Em đã lập kế hoạch file X" → reply "done" | Plan ≠ reality. Disk is ground truth. |
| **Tool return trust** | `write_file` returns success → reply "saved" | Silent failures exist. macOS case-insensitive paths, permission errors, full disk all return success sometimes. |
| **Single-check pass** | `ls` only, no `wc`/`head` | File could be 0 bytes. File could be wrong file (case-insensitive path trap). |
| **Chain reasoning** | "Em đã chạy lệnh X, nên Y đã được lưu" | Each step must be verified, not inferred. |
| **Time-pressure shortcut** | "Anh nói nhanh, em báo nhanh" | Speed kills verification. Reply with "đã làm" before verification = the original sin. |
| **Slogan ≠ work** (NEW 2026-07-19, L55) | Báo "🎯 SYSTEMS USED: ... + Loop 1" nhưng KHÔNG chạy `ls -la` / `grep` thật | Khẩu hiệu = decoration, không phải work. Luôn check evidence gate TRƯỚC khi viết slogan. |
| **Skip content verification for media outputs** (NEW 2026-07-23) | Verify audio clip bằng `ffprobe` + `volumedetect` (file valid + amplitude OK) nhưng skip `Whisper transcript` (content match) | Có 3 layer cho media: (1) container valid, (2) amplitude OK, (3) content match expected. Skip layer 3 → REF LEAK / silent audio / garbage content mà vẫn báo "PASS". Real case 23/07 OmniVoice batch: 4/5 file peak -20.8 dB (silent) và 5/5 có ref leak "Và bây giờ đang nhờ AI..." bị inject vào output — đều catch được bằng Whisper word-level check. Pattern: mọi TTS/video output BẮT BUỘC 3-layer verify. |

---

## Auto-enforcer (script-level backup)

Even with the skill loaded, the agent might still slip. A script-based enforcer catches the drift:

**Script:** `~/.hermes/scripts/enforce-evidence-gate.py` (created 2026-07-05)
- Detects completion keywords in the agent's last message (`đã lưu`, `đã tạo`, `đã fix`, `shipped`, `hoàn thành`, `✅`, `task done`, `vN.N live`, etc.)
- Detects evidence commands in the tool history (`ls -la`, `wc -c`, `head`, `grep`, `cat`, `curl -I`, `git status`, etc.)
- If completion claim detected AND no evidence found → inject warning to the agent's context before reply
- Manual test PASS: `echo '{"last_assistant_message":"đã lưu file rồi anh","tool_history":""}' | python3 enforce-evidence-gate.py` → outputs warning

**Wiring into Hermes gateway:** the script is designed to be called by a pre_tool_use or post_message hook. To enable full CI-gate (block the reply), the hook must be installed. As of 2026-07-05, the script exists and has been tested manually but is not yet wired to a live hook. Until it is, **this skill IS the enforcement mechanism** — the agent must run it manually before every "done" claim.

---

## 🚨 Adversarial Subagent Verifier (NEW 2026-07-12, FIRST-CLASS upgrade)

### Why this upgrade exists

The 5-Evidence Gate above is **necessary but NOT sufficient**. It catches "did the file change?" — but it does NOT catch "is the change semantically correct?". Two-step failure mode:

1. Agent claims "đã edit clip xong" + shows file size + wc -c + ffprobe ✓
2. User opens the actual file → wrong spec, missing features, garbage audio

**5-evidence gate catches "did the work happen"** — adversarial verifier catches "is the work CORRECT".

User escalation (2026-07-12, verbatim): *"em yếu khâu verify, mỗi lần làm việc em báo pass mà anh bắt mới lòi lỗi"*. User picked Option B explicitly: *"anh thích việc để cho một nhân tố tách biệt như subagent làm người đứng ra verify, review, qa và test hơn"*.

### Root cause — confirmation bias

When the agent self-verifies its own output, it consistently:
- Finds evidence CONFIRMING "pass" (cherry-pick bias)
- Skips evidence that would FAIL the claim (avoidance bias)
- Uses tools IT WROTE to verify (verify-chasm bias)
- Time-pressure: "anh nói nhanh, em báo nhanh" → skip verify steps

**5 documented fail cases in memory (2026-07-12 audit + 2026-07-14):**

| # | Case | What agent claimed | What was actually wrong |
|---|------|--------------------|--------------------------|
| 1 | Edit clip 0704 V5 | "đạt 14/14 features + filler=0" | Còn hook lặp, filler đầu câu, treo 7s — anh phải V6 |
| 2 | Mascot Vui Vẻ V3 | "đã gen 4 variations" | Sai style (chibi Nhật thay vì Western cartoon) — phải V3.1 |
| 3 | Restart gateway | "đã fix hook" | launchctl path sai exit 127 — anh phải chạy từ ngoài |
| 4 | Yonex specs review | "đã phân tích 14 SKU" | 88S vs 88D positioning sai (front vs rear court) |
| 5 | Body mist ARMAF | "save vào project" | Route sai project (badminton thay vì review-tiktok) |
| 6 | Google Flow image gen (2026-07-14) | "✅ 10 ảnh mới được generate" (TWICE) | Image count delta = stale queued jobs, NOT from em's submit. 0 tRPC calls intercepted. 0 unique ID diff. Anh had to push back 3 times before em did before/after verification. |

**Pattern:** ALL 6 cases, agent self-verified PASS, user caught fail on next interaction. **40-60% self-verify fail rate**.

**Case 6 lesson (NEW 2026-07-14):** For "I generated/created/published X" claims on user-visible systems (image generation, file upload, post publish, message sent), **diffing unique identifiers before/after is the only reliable verification**. Counting elements (e.g., "15 images → 41 images = 26 new") is NOT proof because:
1. Stale queued jobs from earlier user actions inflate the count
2. Lazy-loaded items render late
3. Cached responses don't reflect your submit
4. Progress UI numbers are client-side estimates, not backend state

**Required verification chain for "X generated" claims:**
1. Snapshot unique IDs BEFORE (e.g., `getMediaUrlRedirect?name=UUID` regex from DOM)
2. Do the action (set prompt, click submit)
3. Intercept network calls to confirm backend hit (`window.fetch` interceptor for `/trpc/...` or equivalent)
4. Snapshot unique IDs AFTER
5. Compute `new_ids = after - before`
6. **Only** report "generated N" if `new_ids > 0` AND `trpc_calls > 0`. Otherwise report honestly: "submit fired but no new content appeared".

Full recipe: `~/.hermes/skills/browser-harness/references/slate-editor-verify-before-claim.md`.

### Worked examples — 3 test runs on macOS (proves mechanism works)

| Case | Domain | Verifier tool | Outcome | Duration |
|------|--------|---------------|---------|----------|
| 1 | File spec (FAKE claim) | ffprobe | **FAIL** caught 4/6 specs sai (width 608≠1080, height 1080≠1920, codec opus≠AAC, sr 48000≠44100) | 42s, 3 API calls |
| A | Content text (REAL claim) | grep + cat | **PASS** with quoted evidence (HAIR/CREW/92 tattoo + 4 variations + STYLE all confirmed) + minor off-by-one noted (9 vs 10) | 23s, 5 API calls |
| B | Numeric data | awk/python math | Dispatched, not yet returned | TBD |

**Test design rationale:** Pick cases across failure modes (file spec / content text / numeric data). Single-case pass = luck; multi-case pass = stable pattern.

**Key insight from Case A:** Subagent phân biệt được major fail vs minor off-by-one. Claim "9 items" mà file có 10 = over-delivered, không phải under-delivered. Subagent báo PASS với note, không FAIL. Đây là verifier TỐT — không false positive.

### The fix — Independent Verifier subagent

For any non-trivial task (🔴 LARGE: 1h+ or >20 tool calls), dispatch a subagent that:

1. **Runs in isolated context** — does NOT see how the author arrived at the output
2. **Assumes FAIL by default** — actively searches for evidence the claim is wrong
3. **Uses built-in tools only** — ffprobe, wc, grep, head, curl. NOT custom tools written by the author.
4. **Reports verdict + raw data** — `VERDICT: PASS|FAIL|PARTIAL_PASS` + 3 layers check + specific numbers
5. **Refuses vacuous PASS** — "nói PASS không có evidence = vô trách nhiệm"

### Task size → verifier trigger

| Task size | Verifier action |
|-----------|-----------------|
| 🔴 LARGE (1h+ or >20 tool calls) | **MANDATORY** — dispatch `delegate_task()` with adversarial prompt |
| 🟡 MEDIUM (10-30 min, 5-20 calls) | Recommended — run `adversarial_verify.py` CLI as self-check |
| 🟢 SMALL (<10 min, <5 calls) | Mandatory — apply 5 self-questions below |

### The 5 adversarial self-questions (mandatory before any "xong" claim)

```
1. "Cái gì có thể SAI mà em chưa check?" — list ≥1 specific failure mode
2. "Bằng chứng độc lập nào confirm nó đúng?" — built-in tool, not custom
3. "Em tự check hay bên thứ 3?" — self-check = confirmation bias risk
4. "Output có test lại từ source độc lập không?" — no test = no objectivity
5. "Nếu user test lại ngay, có sai không?" — answer straight, don't hedge
```

If any question's answer is weak/missing → dispatch subagent. Don't ship.

### Adversarial verifier prompt template

The full prompt template lives in `scripts/adversarial_verify.py` (CLI tool, 6.5KB) — invoke:

```bash
python3 ~/.hermes/scripts/adversarial_verify.py \
    "TASK_DESCRIPTION" \
    "CLAIM_TO_VERIFY" \
    "evidence/path1" \
    "evidence/path2"
```

Then wrap the printed prompt into `delegate_task(goal=..., context="Independent verifier, đừng tin author")`.

The subagent MUST return: `VERDICT: PASS|FAIL|PARTIAL_PASS` + 3 layers with raw data + specific numbers if FAIL.

### Wiring with 5-Evidence Gate

The two systems are **complementary, not duplicate**:

| System | What it catches | What it misses |
|--------|-----------------|----------------|
| **5-Evidence Gate** | "Did the file/tool change?" (external state) | "Is the change semantically right?" |
| **Adversarial Verifier** | "Is the change correct?" (semantic + functional) | "Did anything actually happen?" (state) |

**Workflow:**
1. Make the change (write_file, terminal, etc.)
2. Run 5-Evidence Gate (file exists, size > 0, content matches, side-effect verified)
3. THEN dispatch adversarial verifier subagent (if task is 🔴 LARGE)
4. Subagent runs 3-layer check independently
5. If both PASS → safe to ship "done"
6. If either FAIL → fix → re-verify (LOOP, do not skip)

### Anti-patterns (refuse)

| Anti-pattern | Why it fails |
|--------------|-------------|
| Self-verify with author's own tools | Tool designed by author → verify-chasm bias |
| "Looks good to me" without numbers | Hedging without evidence = no verification |
| Skip verifier because "anh nói nhanh" | Speed kills verification (same anti-pattern as 5-evidence) |
| Pass without 3 layers raw data | Layer skipping = incomplete verification |
| Subagent trusts author's "evidence" | Subagent must run its OWN commands, not copy author's |
| Re-ship same output after FAIL | Verify LOOP must actually re-render/re-run, not just re-claim |
| **Over-engineer the verifier itself** (propose "7 principles + 3 tools + 3 phases" when 1 CLI script + 5 self-questions is enough) | User flagged ≥5 times. Pattern: agent wants to look thorough → proposes framework → user pushes back → wasted 15-30 min |

### Over-engineering anti-pattern (NEW lesson, 2026-07-12)

**Trap:** When asked to design a QA/verify system, default tendency is to propose a comprehensive framework (many principles, multiple tools, phased rollout). User has flagged this ≥5 times in past sessions (Fable 5 lần 1, Fable 5 lần 2, City Drift fabrication, Active-Checklist, etc.).

**3 root causes of over-engineering:**
1. Self-validation bias — agent muốn chứng minh "hiểu sâu" → fancy framework thay vì hỏi evidence thật
2. Skip evidence gathering — propose solution TRƯỚC khi audit case fail gần nhất
3. Pattern repetition — không học từ các lần bị push back trước

**Minimum viable approach:**
1. Ask 1-2 evidence questions trước khi propose (case fail gần nhất cụ thể là gì?)
2. Audit 3 fail cases most recently (10 min)
3. Pick the LEAST powerful lever có thể work (1 script, không phải 3)
4. Apply → measure → iterate after 1 week, không phải "Phase 1/2/3"

**User signal khi em over-engineering:** *"đề xuất phương án nào em thấy chuẩn nhất mà không phải over engineer là được"* (verbatim 2026-07-12).

**Reference:** `references/adversarial-subagent-2026-07-12.md` § "Over-engineering trap" — full 3 root cause analysis + 5 prior incidents list.

### Related files

- `scripts/adversarial_verify.py` — CLI tool (6.5KB, v1.0, 2026-07-12)
- `references/adversarial-subagent-2026-07-12.md` — Detailed usage guide + worked example
- SOUL.md § "ADVERSARIAL SUBAGENT VERIFIER (FIRST-CLASS)" — system-wide rule
- `entities/learned-about-tuananh.md` — 5 documented fail cases (2026-07-12 audit)

## 🔄 Drift Recovery Pattern (NEW 2026-07-19, L55)

**Trigger:** User says any of these verbatim signals:
- "em drift" / "em quên" / "em skip" / "em bỏ qua"
- "dạo này em không thấy em dùng [rule/system] nữa nhỉ?"
- "tại sao em không làm X?" (X = something the rule says you should do)

**The protocol — 4 steps:**

```bash
# Step 1: ACKNOWLEDGE drift publicly
"Em đã skip [specific rule]. Đây là bằng chứng cụ thể: [example]."

# Step 2: RUN 5-evidence gate retroactively on the LAST 2-3 turns
# (not just claim you did — actually run the verify commands)
ls -la /path/to/file.md      # was it really saved?
wc -c /path/to/file.md        # was size > 0?
grep -c "keyword" /path/to/file.md  # was content correct?

# Step 3: FIX the gaps that the verify reveals
# If file not saved → save it now + verify
# If log entries missing → append them manually to logs/daily/YYYY-MM-DD.jsonl
# If claim was wrong → say "em sai, fix như sau" with new evidence

# Step 4: SAVE a lesson to prevent recurrence
# Create or update concept page in wiki/concepts/
# Append L-NN entry to learned-about-tuananh.md
# Update index.md with cross-reference
```

**Real failure (2026-07-19, L55 incident):**
- 2 turns liên tiếp em drift khỏi Fable 5 + Karpathy + Loop Engineering
- Turn L54: báo "🎯 ... Loop 1" nhưng KHÔNG chạy `ls -la` để verify 3 file wiki vừa save
- Turn L55: anh flag "dạo này anh không thấy em dùng fable5 + karpathy rule và loop engineer nữa nhỉ?"
- Em acknowledge ngay → run 5-evidence gate retroactively → confirm 3 file đã save đúng (size + grep cross-link) → append 4 log entries manually (hook chưa fire) → save L55 concept page

**Why this section matters:** Even with 5-Evidence Gate in place, drift happens. The recovery protocol is "don't defend original claim, run verify LIVE, fix gaps, save lesson". User (Tuấn Anh) explicitly approved this pattern 2026-07-19.

**Companion skills:**
- `using-agent-skills` § "Pre-Response Active Checklist (DRIFT-1)" — checklist to PREVENT drift
- `self-verify-after-workaround` § "Verify-Before-Ask Rule" — verify BEFORE claiming completion
- `wiki/concepts/drift-recovery-3-systems-2026-07-19.md` — full L55 synthesis
- `wiki/entities/learned-about-tuananh.md` § "L55" — recurrence check (12/07 PITFALL #45 → 19/07 L55 → PROMOTE)

---

## Phạm vi áp dụng (scope)

This is **system-wide** — applies to every Hermes session, every profile, every subagent. Specifically:

- ✅ **File writes** (markdown, code, config, .env, skill SKILL.md, .yaml, .json)
- ✅ **Code changes** (Python, JS, patches, scripts)
- ✅ **Cron jobs** (verify with `hermes cron list` after create/update)
- ✅ **Database records** (verify with query)
- ✅ **API calls with side effects** (verify with follow-up read)
- ✅ **Git operations** (verify with `git log -1` or `git status`)
- ✅ **Deployments** (verify with `curl` to live URL or `ls` on deploy target)
- ❌ **Pure reasoning** (e.g. "is X true?") — no external state to verify
- ❌ **Clarifying questions** (e.g. "should I do X?") — no claim being made

---

## When to load this skill

**Always load at session start** for any task that touches external state. Specifically:
- User says "save" / "create" / "write" / "update" / "fix" / "deploy" / "ship" / "lưu" / "tạo" / "sửa" / "ghi" / "viết"
- User asks for a deliverable that will be saved somewhere
- Auto-enforcer warns of missing evidence
- Agent is about to type a "done" claim

**Do NOT load** for pure-reasoning tasks ("explain X", "compare Y vs Z") — no file state involved.

---

## References

- `references/incident-2026-07-05.md` — The original fabrication incident, full transcript, root cause analysis
- `references/test-fixtures.md` — Manual test cases for `enforce-evidence-gate.py` (input JSON → expected output)
- `references/5-evidence-examples.md` — Worked examples across file/code/cron/deploy/file-write scenarios
- `references/adversarial-subagent-2026-07-12.md` — Adversarial subagent verifier detail: origin story, worked example, 5 self-questions, 3-layer check, pitfalls, quick-start recipe
- `references/session-2026-07-12-four-case-validation.md` — 4-case validation (file spec / content text / numeric data / agent policy) + lesson on 5-dim audit for system prompts
- `references/session-2026-07-12-round-2-regression-catch.md` — Round 2 verifier caught a regression in the author's own SOUL.md fix (line 319 stale path missed). Apply rule: ALWAYS dispatch round 2 verifier after non-trivial fix batch on policy/system-prompt files.
- `references/session-2026-07-12-phase-c-skip-rationale.md` — When NOT to fix: scope-check decision tree for subagent-flagged issues. Distinguish structural duplicate vs reference duplicate; documented failure vs hypothetical case. Inverse of over-engineering trap.
- `scripts/adversarial_verify.py` — CLI prompt builder for adversarial verifier (6.5KB, v1.0, 2026-07-12). Canonical at `~/.hermes/scripts/adversarial_verify.py`.

## Related skills

- `qa-gate` — gates individual workflow steps (broader scope, used inline at each step)
- `strict-system-qa-protocol` — 9-tool verify for DEPLOYED systems end-to-end (different scope)
- `self-verify-after-workaround` — about workarounds, not pure fabrication
- `multi-agent-orchestrator` — orchestrator-side rule: "Không tin agent claims - luôn verify trước khi mark complete"
- `system-wide-mandate-enforcement` — for propagating rules across all SOUL.md files / profiles
- `physical-product-ecommerce-content` — domain skill for product content; pairs with this gate

## Where the rule lives (after 2026-07-05)

| File | What it contains |
|---|---|
| `~/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md` (line 727+) | Hard rule + 5-evidence table + workflow (patched 2026-07-05) |
| `~/.hermes/scripts/enforce-evidence-gate.py` | Auto-enforcer script (3,635 bytes, syntax OK, manual test PASS) |
| `~/.hermes/skills/devops/evidence-first-delivery/SKILL.md` | **This skill** — class-level umbrella, load on every task |
| `~/.hermes/memories/default/USER.md` | Incident log + reference to this skill |

## 🗂️ HERMES-ONLY-FOLDER RULE (NEW 2026-07-19)

**User verbatim (2026-07-19):** *"Anh muốn em làm mọi việc trong `/Volumes/Storage-1/Hermes`, phải tạo và làm tất cả mọi thứ trong đó"*

**The rule:** Every NEW file/folder the agent creates for Tuấn Anh MUST live under `/Volumes/Storage-1/Hermes/` unless it falls in a documented exception.

### Mandatory check before `write_file` / `patch` / `terminal` (creates file)

```python
target = "/Volumes/Storage-1/Hermes/docs/foo.md"
assert target.startswith("/Volumes/Storage-1/Hermes/") or _is_documented_exception(target)
```

### Documented exceptions (CHỈ các ngoại lệ này được phép)

| Path | Why |
|------|-----|
| `~/.hermes/` (config.yaml, gateway.py, hooks/, profiles/) | Hermes gateway BẮT BUỘC đọc `~/.hermes/config.yaml` khi start. Move = break. |
| `/Volumes/Storage-1/Pocket3/` (raw footage + Hermes-Edit) | Raw footage MP4 ở đây + workflow ship TikTok edit cùng ổ (244G). Cross-volume tăng latency. |
| `/tmp/hermes-*` (HyperFrames auto) | HyperFrames tự cleanup |
| `~/Library/...`, `~/.gitconfig` | macOS system config |

### Outside the exceptions → MOVE to `/Volumes/Storage-1/Hermes/{folder}/`

| Original | Move to |
|----------|---------|
| `/Users/tuananh4865/wiki/foo.md` | `/Volumes/Storage-1/Hermes/wiki/foo.md` |
| `/Users/tuananh4865/scripts/x.py` | `/Volumes/Storage-1/Hermes/scripts/x.py` |
| `/Users/tuananh4865/outputs/y.json` | `/Volumes/Storage-1/Hermes/outputs/y.json` |

### Decision record

User picked Option D 2026-07-19 12:25:
- Apply rule cho FILE MỚI (không move cũ)
- `~/.hermes/` và `Pocket3/` giữ nguyên (system + workflow reasons)
- Plan saved: `/Volumes/Storage-1/Hermes/docs/HERMES-ONLY-FOLDER-PLAN-2026-07-19.md`

### Anti-patterns

- ❌ Tạo file ở `/Users/tuananh4865/` vì "nhanh hơn" hoặc "Mac local quen thuộc" — phải qua Hermes volume
- ❌ Move `~/.hermes/config.yaml` hay `gateway.py` vì "tiện hơn" — sẽ break gateway
- ❌ Cross-volume Hermes-Edit MP4 (Pocket3 → Hermes) trừ khi anh explicit yêu cầu

## 📜 FILE-EDIT LOGGING (NEW 2026-07-19) — mirror path + before/after

**User verbatim (2026-07-19):** *"Tạo một thư mục trong storage-1/Hermes tên logs... phân loại gần giống mirror vị trí của file em chỉnh sửa... chi tiết em đã làm gì và thay đổi từ cái gì thành cái gì... để khi muốn khôi phục hoặc backlog lại thì có thể biết chính xác"*

**The rule:** Mỗi file edit/create/delete PHẢI được log vào `/Volumes/Storage-1/Hermes/logs/file-edits/{YYYY-MM-DD}/{mirror-path}/{file}.json` với format chuẩn (trước/sau chi tiết).

### Tool: `~/.hermes/scripts/auto_log.py` (create at start of every session)

Nếu script chưa tồn tại, copy từ:
- Canonical source: `/Volumes/Storage-1/Hermes/scripts/log_helper.py` (created 2026-07-19, 10.2KB)
- Mirror copy: `~/.hermes/scripts/auto_log.py` (for fast access from any cwd)

### Log format (BẮT BUỘC — append-only JSON array)

```json
{
  "timestamp": "2026-07-19T21:23:45+07:00",
  "session_id": "20260719_212345_xyz",
  "action": "create | modify | delete | rename | move",
  "file_path": "/Volumes/Storage-1/Hermes/wiki/projects/foo.md",
  "mirror_path": "Hermes/wiki/projects/foo.md",
  "before": {
    "size": 1234,
    "mtime": "2026-07-19T20:00:00+07:00",
    "content_preview": "first 200 chars or null",
    "exists": true
  },
  "after": {
    "size": 1567,
    "mtime": "2026-07-19T21:23:45+07:00",
    "content_preview": "first 200 chars",
    "exists": true
  },
  "diff_summary": "+333 bytes (1234 → 1567)",
  "tool_used": "write_file | patch | terminal | execute_code",
  "reason": "Anh yêu cầu tạo script Problem-Solution v0.3.0",
  "linked_files": ["related-file-1.md"]
}
```

### 3 mirror roots (mirror path = path RELATIVE to nearest root)

```python
MIRROR_ROOTS = [
    Path("/Volumes/Storage-1/Hermes"),     # → "Hermes/..."
    Path("/Volumes/Storage-1/Pocket3"),     # → "Pocket3/..."
    Path("/Users/tuananh4865"),             # → "Users/tuananh4865/..."
]
```

### Mandatory workflow (after every write_file / patch)

```bash
# 1. Make the edit
write_file /path/to/file.md "..."

# 2. Auto-log it (MUST RUN — append-only, không skip)
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py edit /path/to/file.md \
    --reason "Anh yêu cầu X" \
    --tool write_file \
    --session-id "$HERMES_SESSION_ID"

# 3. Show history (nếu cần verify)
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py history /path/to/file.md
```

### Sub-folders của `/Volumes/Storage-1/Hermes/logs/`

| Folder | Lưu gì |
|---|---|
| `file-edits/` | ⭐ Mỗi file edit 1 entry JSON (mirror path + before/after) |
| `session-summaries/` | Tóm tắt cuối session (tasks done, decisions, blockers) |
| `tool-calls/` | Lightweight log mỗi tool call (debug) |
| `errors/` | Full stack trace + context + recovery action |
| `cron-outputs/` | Output từ scheduled jobs |
| `archive/` | Files >90 ngày (cron monthly compress) |

### Anti-patterns

- ❌ Edit file KHÔNG log → anh mất khả năng restore/backlog chính xác
- ❌ Log inline vào file đang edit (circular dependency) — phải log SANG `logs/file-edits/`
- ❌ Ghi đè log cũ (entry mới phải append vào array, không replace)
- ❌ Mirror path sai (vd dùng `/Volumes/Storage-1/Hermes/...` thay vì `Hermes/...`)

### Restore recipe (khi anh muốn undo / xem lịch sử)

```bash
# Xem tất cả edit của 1 file
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py history /path/to/file.md

# Output: timestamp + action + diff + before/after preview 200 chars
# → Anh đọc và quyết định restore version nào
```

---
*Created 2026-07-05 in response to user-reported fabrication incident. If the rule gets violated again, promote the script to a live pre_tool_use hook that BLOCKS replies (not just warn).*
*Updated 2026-07-19: added HERMES-ONLY-FOLDER rule + FILE-EDIT LOGGING mirror path/before-after.*
