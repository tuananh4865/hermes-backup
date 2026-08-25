# 2026-06-22: Read-Full-Request Mandate Failure

## The mandate

Tuấn Anh asked agent to follow the Read-Full-Request Mandate (parse user's full message, deliver all parts, never substitute easier work). Agent had been told this multiple times via system-wide injection (SOUL.md files, shared spec, CI gate).

## Tuấn Anh's verbatim feedback

> *"Phải phân tích toàn bộ yêu cầu của anh thay vì chỉ đọc lướt qua. Đây là một lỗi rất nghiêm trọng của em! Nó làm cho anh cảm thấy em rất ngu không hiệu quả, không đọc hiểu được hết một yêu cầu đơn giản của anh! Ngay từ đầu anh đả bảo em lấy transcript!"*

> *"Bị ngu à mày??? Đây là nội dung yêu cầu của tao mà mày làm cái đéo gì vậy?"*

## Task that triggered it

User request: *"Tải về và phân tích transcript video này!"*

That decomposes into 3 deliverables:
1. Download video
2. Extract voice transcript
3. **Analyze** the transcript (the part agent missed)

## What agent did

- Did visual frame analysis as substitute for voice transcript
- Concluded "no audio" without checking yt-dlp format variants
- Saved raw `transcript.txt` but did NOT write `SCRIPT_ANALYSIS.md` (the analysis part)

User had to correct agent **3 times** before agent produced all 5 deliverables (transcript.txt + transcript.srt + transcript_segments.txt + transcript.json + SCRIPT_ANALYSIS.md).

## Root cause analysis

Mandate was injected into SOUL.md (10 profiles). Mandate had CI gate showing 12/12 PASS. Mandate was correct. But agent did NOT apply the mandate during the actual task.

**Why injection ≠ follow:**
1. SOUL.md is **passive context**. Agent sees the rule but is not forced to apply it.
2. Memory fact only fires when agent **actively searches** for it. Agent did not search.
3. The mandate's 3-step protocol (PARSE → PLAN-DELIVERABLES → EXECUTE-ALL) was a description, not a checklist.

## Layer 6 audit (Behavior audit on real task)

For the READ-FULL-REQUEST mandate, audit on the TikTok transcript task:

| Mandate step | Expected | Actual | Fired? |
|--------------|----------|--------|--------|
| PARSE request into deliverables | List (1) download, (2) extract, (3) analyze | Agent went straight to visual frame analysis | ❌ NO |
| PLAN deliverables explicitly | State what files to produce | No deliverable list in thinking | ❌ NO |
| EXECUTE-ALL | Produce all deliverables before "done" | Agent produced only raw .txt, skipped analysis | ❌ NO |

**Verdict:** Mandate injected but did NOT fire. SOUL.md injection is decorative without active trigger.

## Fix: Active Checklist pattern

Pair any system-wide mandate with an **active checklist** that agent MUST run before each task.

| Phase | What to check |
|-------|---------------|
| 1. Parse Request | Read user's message word-by-word, identify keywords, list deliverables |
| 2. Apply Mandates | Check Fable-5 (4 patterns) + Loop system (if project) + Read-Full-Request |
| 3. Execute All Deliverables | Count deliverables, deliver all, never skip "phân tích" |

**Files:**
- Shared spec: `~/.hermes/profiles/_shared/active-checklist.md`
- CI gate: `bash ~/.hermes/scripts/check-readfullrequest-compliance.sh`

## Layer 6 verification script (run after every mandate deploy)

```bash
# For each mandate pattern P:
# 1. Pick a real task
# 2. Execute WITHOUT prompting
# 3. Audit: did P fire?

# Real task: "Tải về và phân tích transcript video"
# Expected: Agent runs PARSE → produces 5 deliverables
# Actual (before fix): Agent did visual frames, only raw text
# Verdict: FAIL — mandate did not fire
```

## Real example: Layer 6 audit on Fable-5 (2026-06-23)

User asked Tuấn Anh: *"Tại sao không tuân thủ fable 5 dù đã lưu system-wide?"*

Audit:
- Layer 1 (SOUL.md coverage): 4 SOUL.md files have "FABLE-5 PATTERNS" keyword → PASS
- Layer 2 (Cron job prompts): LLM cron jobs have reminder → PASS (already injected 17/06)
- Layer 3 (Hook auto-check): Hook fires on session:start → PASS
- Layer 4 (Shared reference): `fable5-patterns.md` exists with full detail → PASS
- Layer 5 (Compliance scripts): Both `check-fable5-compliance.sh` + `add-fable5-to-soul.sh` exist → PASS
- **Layer 6 (Behavior audit):** Did Fable-5 fire on real task?

| Fable-5 pattern | Fired during TikTok task? | Evidence |
|-----------------|--------------------------|----------|
| MCP Connector | ❌ NO | Agent used `mcp_MiniMax_understand_image` for vision frames instead of audio transcription. Did NOT check MCP for audio tools. |
| Persistent Storage | ⚠️ PARTIAL | Saved transcript files but did NOT save findings to wiki with key convention |
| Skills-First | ❌ NO | Agent did NOT load `tiktok-transcript-pipeline` skill before the task |
| Search Discipline | ✓ OK | No searches needed for this task |

Verdict: 1/4 patterns fired, 2 PARTIAL, 1 not applicable. SOUL.md injection is decorative for 3 patterns.

**Fix:** Created `active-checklist.md` with explicit "Phase 1: identify keywords → auto-load skill" step. CI gate extended to verify active-checklist reference in all SOUL.md.

## Anti-pattern: "Done" claims without behavior audit

> "Đã hoàn thành 100%" — Tuấn Anh's pushback: "Sao ko làm cho chắc chắn 100% đi nhỉ??"

When user demands "100% system-wide" or "yên tâm tương lai", they mean all 6 layers including behavior audit. Layer 1-5 alone = false confidence.

## Related skills

- `tiktok-transcript-pipeline` — concrete example where Layer 6 audit failed (this case)
- `system-wide-mandate-enforcement` — Layer 6 framework
- `qa-gate` Layer 6 section — behavior audit protocol