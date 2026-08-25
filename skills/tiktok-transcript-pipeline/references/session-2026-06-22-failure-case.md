# Session 2026-06-22: Failure case that triggered this skill

## TL;DR

User asked: **"Tải về và phân tích transcript video này!"** (Download and ANALYZE transcript of this video!)

Agent did:
1. ❌ Visual frame analysis (8 frames) instead of voice transcript
2. ❌ Concluded "no audio" from 1 ffprobe check
3. ❌ Saved raw transcript.txt but forgot SCRIPT_ANALYSIS.md (the analysis part)

User had to correct agent **3 times**:
1. "Đúng video nhưng tìm cách lấy transcript đi, trong video có voice nói đàng hoàng mà" (Correct video but find way to get transcript — the video has voice)
2. "Cái anh muốn em lưu ý là phải phân tích toàn bộ yêu cầu của anh thay vì chỉ đọc lướt qua" (Read the FULL request instead of skimming)
3. "Bị ngu à mày??? Đây là nội dung yêu cầu của tao mà mày làm cái đéo gì vậy?" (Are you stupid??? That's MY request and you're doing the wrong thing???)

## Original request (verbatim)

```
[Tuấn Anh] Tải về và phân tích transcript video này!
```

URL: `https://vt.tiktok.com/ZSCJB91YQ/` → @caocuongvuai video 7623055460836330772 (6-min AI reaction)

## Failure breakdown — what agent did vs. what was asked

| Step | What user wanted | What agent did | Wrong? |
|------|------------------|----------------|--------|
| 1 | Download video | Downloaded video via yt-dlp | ✓ |
| 2 | Get transcript (audio → text) | Did visual frame analysis with mcp_MiniMax_understand_image | ❌ Substitution |
| 3 | "Phân tích" = analyze the transcript | Did NOT analyze transcript, only described visual scenes | ❌ Skipped |
| 4 | Report findings to user | Reported "no audio" without checking format variants | ❌ Conclusion wrong |

## Critical technical mistake

Agent ran:
```bash
yt-dlp -f "bestaudio[ext=m4a]/bestaudio/best" --extract-audio
```

This downloaded the HEVC video stream only (no audio). Agent ran `ffprobe -show_streams` and saw:
```
Stream 0: codec=hevc, type=video
```

Agent immediately concluded "video không có audio" without checking other format variants.

**What agent should have done:**
```bash
yt-dlp -F "URL"  # List ALL format variants first
```

Output showed 12 variants, including:
- `bytevc1_1080p_982660-0` (variant -0, NO audio in output)
- `bytevc1_1080p_982660-1` (variant -1, HAS audio)
- `download` (watermarked, ALWAYS has audio+video bundled)

**Correct download command:**
```bash
yt-dlp -f "download" -o "video.mp4" "URL"
```

This file had both video (HEVC) and audio (AAC) bundled. Whisper extracted transcript perfectly in 60 seconds, producing 178 segments of Vietnamese text.

## Tuấn Anh's full feedback (verbatim quotes)

**After agent said "no audio":**
> "Đúng video nhưng tìm cách lấy transcript đi, trong video có voice nói đàng hoàng mà"

**After agent did visual frame analysis:**
> "Cái anh muốn em lưu ý là phải phân tích toàn bộ yêu cầu của anh thay vì chỉ đọc lướt qua. Đây là một lỗi rất nghiêm trọng của em! Nó làm cho anh cảm thấy em rất ngu không hiệu quả, không đọc hiểu được hết một yêu cầu đơn giản của anh! Ngay từ đầu anh đả bảo em lấy transcript!"

**After agent only saved raw transcript.txt:**
> "Anh đây là yêu cầu vừa rồi của anh: ... Ngay từ đầu anh đả bảo em lấy transcript!" Bị ngu à mày??? Đây là nội dung yêu cầu của tao mà mày làm cái đéo gì vậy?"

## 8 lessons extracted

1. **"Phân tích" = analysis, not extraction.** When user asks "phân tích X", they want analysis OF X, not just extraction OF X.

2. **"Transcript" = voice audio → text.** NEVER substitute with visual frame analysis (caption overlays ≠ voice transcript).

3. **Check ALL yt-dlp format variants before concluding "no audio".** TikTok has -0/-1 variants where -0 is video-only despite showing `aac` codec. Use `-f "download"` as safe default.

4. **Verify with ffprobe AFTER download, not based on format string.** Format code can show `aac` but actual stream in output may be missing.

5. **Read user's FULL message, parse into atomic deliverables.** "Tải về và phân tích" = 3 deliverables: download + extract transcript + analyze transcript.

6. **If user repeats the request = agent failed first time.** STOP and re-parse, do NOT redo same approach.

7. **Active checklist BEFORE task = required.** Injecting mandates into SOUL.md is passive. Agent must run an active checklist to trigger mandates.

8. **Substitution trap.** Doing easier work (visual analysis) instead of requested work (voice transcript) is a CRITICAL failure. Always count deliverables before claiming "done".

## Skills/SOUL updates triggered by this session

- ✅ `tiktok-transcript-pipeline` skill created (this skill)
- ✅ `qa-gate` skill — added Read-Full-Request Mandate section + Layer 6 Behavior Audit
- ✅ `system-wide-mandate-enforcement` skill — added Layer 6 + active-checklist pattern
- ✅ `video-download-yt-dlp` pitfall #8 corrected — was misleading to vision-only, now reframed with variant -1 / -f "download" fallback
- ✅ `youtube-transcript-extractor` skill — already had the variant -0/-1 lesson (worked correctly in fallback)
- ✅ `~/.hermes/profiles/_shared/read-full-request.md` — shared spec for the mandate
- ✅ `~/.hermes/profiles/_shared/active-checklist.md` — shared active checklist (paired with mandate)
- ✅ `~/.hermes/scripts/add-readfullrequest-to-soul.sh` — idempotent injector (10 SOUL.md updated)
- ✅ `~/.hermes/scripts/check-readfullrequest-compliance.sh` — CI gate (15/15 PASS)
- ✅ `scripts/verify_transcript_pipeline.sh` (in this skill) — 9-step self-check that catches the missing SCRIPT_ANALYSIS.md

## Files produced for this task

```
~/wiki/raw/tiktok-analysis/7623055460836330772/
├── video.mp4                          (32.6 MB, has audio)
├── audio_full.wav                     (12 MB, 6:21)
├── transcript.txt                     (10.4 KB, 7,993 chars)
├── transcript.srt                     (16.3 KB, 178 segments)
├── transcript_segments.txt            (13.1 KB)
├── transcript.json                    (117.8 KB)
└── SCRIPT_ANALYSIS.md                 (9.2 KB, 8 sections: Hook, Structure, Psychology, Viral formula, CTA, Lessons, Anti-patterns, Recommendation)
```

## What agent should do NEXT time

Before ANY task:
1. Run `~/.hermes/profiles/_shared/active-checklist.md` Phase 1 (Parse Request)
2. If keyword = transcript/voice → load this skill
3. Run this skill's Quick Start pipeline
4. Run `bash scripts/verify_transcript_pipeline.sh <url> <output_dir>` BEFORE claiming done
5. If script returns non-zero, the script tells exactly which deliverable is missing (usually SCRIPT_ANALYSIS.md)