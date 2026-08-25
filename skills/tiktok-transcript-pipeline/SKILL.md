---
name: tiktok-transcript-pipeline
description: Extract voice transcripts from TikTok/YouTube videos AND produce a full script analysis (hook, structure, CTA, viral formula, actionable lessons). Use when user says "transcript", "phụ đề", "lời thoại", "voice nói", "phân tích transcript", "phân tích script", "phân tích video". NEVER do visual frame analysis as a substitute — caption text is NOT a transcript.
---

# TikTok/YouTube Transcript + Script Analysis Pipeline

## ⚠️ CRITICAL: Lessons from 2026-06-22 failure

Tuấn Anh asked: **"Tải về và phân tích transcript video này!"**

What I did wrong (3 levels of fail):
1. ❌ Did visual frame analysis instead of voice transcript
2. ❌ When corrected "có voice nói đàng hoàng", still concluded "no audio" from 1 ffprobe check
3. ❌ When finally extracted transcript, only saved raw text — forgot to ANALYZE it as requested

**The actual task was always 3 parts:**
1. Download video
2. Extract voice transcript
3. ANALYZE the transcript (hook, structure, viral formula, CTA, lessons)

Anh had to repeat request 3 times. THIS MUST NEVER HAPPEN AGAIN.

## Deliverables Checklist

When user asks for "phân tích transcript" or "phân tích script video", MUST produce ALL of these:

| # | File | Required content |
|---|------|-----------------|
| 1 | `transcript.txt` | Raw voice text |
| 2 | `transcript.srt` | Subtitle with timestamps |
| 3 | `transcript_segments.txt` | Format `[start-end] text` |
| 4 | `transcript.json` | Full segments + metadata |
| 5 | **`SCRIPT_ANALYSIS.md`** | **Hook + Structure + Psychology + Viral formula + CTA + Lessons** ← THE ACTUAL "PHÂN TÍCH" |

The 5th item is what most agents miss. "Phân tích" = analysis, not just extraction.

## Quick Start Pipeline

```bash
# Step 1: ALWAYS list all formats first (NEVER skip)
yt-dlp --no-warnings --no-playlist -F "<video_url>"

# Step 2: Download "download" format (watermarked, ALWAYS has audio on TikTok)
yt-dlp --no-warnings --no-playlist \
  -f "download" \
  -o "/tmp/video.mp4" \
  "<video_url>"

# Step 3: Verify audio stream present
ffprobe -v error -show_streams -of json "/tmp/video.mp4"

# Step 4: Extract audio to WAV (16kHz mono for Whisper)
ffmpeg -y -i "/tmp/video.mp4" -vn -ar 16000 -ac 1 -c:a pcm_s16le "/tmp/audio.wav"

# ✅ ALIGNED with SOUL.md MODEL REGISTRY (updated 22/07/2026): 
# - `whisper-transcribe` wrapper (auto large-v3 + medium fallback) is now the system-wide default
# - Per-skill override still works via `MLX_WHISPER_MODEL=...` env var or Python module call below

# Step 5: Transcribe with mlx-whisper (Apple Silicon)
# IMPORTANT: use whisper-env path (NOT default `mlx_whisper` which has broken shebang)
#
# ✅ WHISPER IS ALWAYS INSTALLED — never check, just use it.
# This is pre-installed, persistent, and verified. Em does NOT need to
# re-check installation status before each transcript task.
#
# Preferred path (aligned with system-wide wrapper, see SOUL.md MODEL REGISTRY):
#   ~/.hermes/scripts/whisper-transcribe /tmp/audio.wav
# This auto-uses large-v3-mlx + falls back to medium if loop hallucinate detected.
#
# Direct large-v3 path (if calling without wrapper):
#   /Users/tuananh4865/whisper-env/bin/mlx_whisper \
#     --model mlx-community/whisper-large-v3-mlx \
#     --language vi --output-format all \
#     /tmp/audio.wav
#
# Default model: mlx-community/whisper-large-v3-mlx (2.9GB, Vietnamese optimized)
# Already downloaded at: ~/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-mlx
# Only one model is installed — large-v3 is the only option.
/Users/tuananh4865/whisper-env/bin/python3 -c "
import mlx_whisper, json
result = mlx_whisper.transcribe(
    '/tmp/audio.wav',
    path_or_hf_repo='mlx-community/whisper-large-v3-mlx',
    language='vi',
    task='transcribe'
)
with open('/tmp/transcript.txt', 'w') as f: f.write(result['text'])
with open('/tmp/transcript.json', 'w') as f: json.dump(result, f, ensure_ascii=False, indent=2)
# Build SRT
def fmt(t):
    h,m,s = int(t//3600), int((t%3600)//60), int(t%60)
    ms = int((t%1)*1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
with open('/tmp/transcript.srt','w') as f:
    for i, seg in enumerate(result['segments'], 1):
        f.write(f'{i}\\n{fmt(seg[\"start\"])} --> {fmt(seg[\"end\"])}\\n{seg[\"text\"].strip()}\\n\\n')
"

# Step 6: READ transcript.txt + WRITE SCRIPT_ANALYSIS.md
# This is the part I missed — actually analyze the content
```

## Script Analysis Template (SCRIPT_ANALYSIS.md)

Every analysis MUST include these 8 sections:

1. **Hook Analysis** — Quote the actual hook, break down 3-4 persuasion layers
2. **Script Structure** — Map A/B/C/D sections with timestamps + % of total
3. **Psychology Techniques** — List 5-7 persuasion patterns used
4. **Viral Formula** — Extract the repeatable pattern
5. **CTA Analysis** — Every call-to-action with timestamp + effectiveness
6. **Actionable Lessons for User's Niche** — 5-8 patterns to copy
7. **Anti-patterns to NOT Copy** — 3-5 patterns that don't fit user's niche
8. **Recommendation** — Suggest 1 concrete video to test the pattern

## When This Skill Loads

Trigger words ANY of these in user message:
- "transcript" / "phụ đề" / "lời thoại" / "voice nói"
- "phân tích transcript" / "phân tích script" / "phân tích video"
- "lấy transcript" / "tải về và phân tích"
- URL + "transcribe" / "trích xuất"
- "cách làm video viral" + need example breakdown

## Hard Rules

❌ **NEVER** do visual frame analysis as substitute for voice transcript
❌ **NEVER** conclude "no audio" from a single ffprobe check
❌ **NEVER** save raw transcript without writing SCRIPT_ANALYSIS.md
❌ **NEVER** check only one format from `yt-dlp -F` output — try AT LEAST 3 if first has no audio
❌ **NEVER** use default `python3` for mlx-whisper (Xcode stub broken). USE THIS PATH (verified 2026-06-18):
```bash
# ❌ BROKEN (Xcode CLT python3 missing)
/Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper
/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/Current/bin/python3

# ✅ WORK (whisper-env has Python 3.11)
/Users/tuananh4865/whisper-env/bin/mlx_whisper
# OR via Python module:
/Users/tuananh4865/whisper-env/bin/python3 -m mlx_whisper
```

Diagnostic reflex when "bad interpreter" error fires: `head -1 $(which mlx_whisper)` — if shebang points to missing Python, switch to whisper-env path immediately.

## General Principle (Load qa-gate for full context)

This skill is a concrete instantiation of the **Read-Full-Request Mandate** in `qa-gate`. The general rule:

> When user says "phân tích X", deliver BOTH extraction AND analysis. Counting deliverables before reporting "done" prevents the substitution trap.

This skill applies that rule to the specific class of "TikTok/YouTube video transcript" tasks. For other task classes, load `qa-gate` and apply the same 3-step pre-execution protocol (PARSE → PLAN-DELIVERABLES → EXECUTE-ALL).

## Related

- `qa-gate` — General principle + system-wide mandate context
- `references/session-2026-06-22-failure-case.md` — Full failure transcript that triggered this skill

## Support Files

- `references/session-2026-06-22-failure-case.md` — Full transcript excerpts from the failure conversation, all 3 corrections verbatim, root cause analysis, 8 lessons extracted
- `scripts/verify_transcript_pipeline.sh` — 9-step self-check script that runs the full pipeline AND verifies ALL 7 deliverables exist (incl. `SCRIPT_ANALYSIS.md` which agent missed last time). Usage: `bash scripts/verify_transcript_pipeline.sh <url> <output_dir>`

## Self-Verification Before Delivering

**MUST run this script BEFORE telling user "done":**

```bash
bash ~/.hermes/skills/tiktok-transcript-pipeline/scripts/verify_transcript_pipeline.sh \
  "<video_url>" \
  "<output_dir>"
```

If script exits non-zero → there are missing deliverables (usually `SCRIPT_ANALYSIS.md`). The script will tell you exactly what's missing.

**Why this matters:** Last session, agent reported "done" 3 times. Each time user had to correct. The 9-check script would have caught all 3 failures (missing analysis, missing audio, missing deliverable list).

## ⚠️ Anti-Over-Engineering Note (added 2026-06-23)

When patching skills for "read-full-request" lesson, do NOT create extra infrastructure:

❌ **DON'T** create `add-readfullrequest-to-soul.sh` injector scripts
❌ **DON'T** create `check-readfullrequest-compliance.sh` CI gates
❌ **DON'T** create separate `active-checklist.md` shared files
❌ **DON'T** inject the same mandate into 10 sub-profile SOUL.md files
❌ **DON'T** write a "Cross-Reference: System-Wide Mandates" section pointing to all of the above

✅ **DO** put the rule in default SOUL.md (Slot 1 — auto-injected every session, survives compaction)
✅ **DO** put the rule in the skill body where the work happens
✅ **DO** put the rule in the user's wiki (`learned-about-tuananh.md`) if it's a behavioral preference

Tuấn Anh's actual feedback: *"Nghe có vẻ hơi over engineering quá! System prompt import vào đầu session và giữ qua compaction là chỗ nào?"* — the answer is **Slot 1 of the context priority list in default SOUL.md**. That's enough.

If the lesson is "agent skipped 'analysis' step when user said 'phân tích'", put it HERE in this skill — don't build new infrastructure to enforce it.

## 🧠 Pre-Installed Tools (Default Knowledge — 2026-06-26)

**These tools are PERMANENTLY INSTALLED on Tuấn Anh's Mac. Em does NOT need to check or verify before each use. If a command fails, it's a real error — not "tool not installed".**

### mlx-whisper (Apple Silicon, Vietnamese)
- **Binary PATH**: `/Users/tuananh4865/whisper-env/bin/mlx_whisper`
- **Python env**: `/Users/tuananh4865/whisper-env/bin/python3` (3.11)
- **Model**: `mlx-community/whisper-large-v3-mlx` (2.9 GB) — **THE ONLY model installed**
- **Model path**: `~/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-mlx`
- **Version**: mlx_whisper 0.4.3, mlx 0.31.2, mlx_metal 0.31.2
- **Default language**: `vi` (Vietnamese)
- **DO NOT** check `pip list`, `find` for models, or `mlx_whisper --version` before each transcript — just use it.
- **DO NOT** install other whisper models (medium, base, small, tiny) — only large-v3 is approved.
- **BROKEN PATH** (do NOT use): `/Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper` (Xcode stub shebang)

### yt-dlp
- Already installed, supports TikTok/YouTube/Facebook/Instagram/X
- Use `--no-warnings --no-playlist -F <url>` to list formats first
- Use `-f "download"` for TikTok (watermarked, ALWAYS has audio)

### ffmpeg / ffprobe
- Already installed system-wide
- Use for audio extraction: `-i input.mp4 -vn -ar 16000 -ac 1 -c:a pcm_s16le output.wav`

### Memory rule
**When user says "transcribe this video" / "phân tích transcript" / "lấy voice nói"**:
- Skip "is whisper installed?" checks
- Skip "which model?" thinking
- Just go straight to the pipeline: yt-dlp → ffmpeg → mlx_whisper with large-v3
- Only check installation IF a command actually fails with "command not found" or "No such file"

## Origin

Created 2026-06-22 after Tuấn Anh said *"Bị ngu à mày??? Mày làm cái đéo gì vậy?"* — agent did visual frame analysis instead of voice transcript, then only extracted raw text without writing `SCRIPT_ANALYSIS.md`. Lesson: this skill embeds the full-request-parsing rule so the next transcript task starts already knowing to deliver all 5 files (incl. the analysis).
