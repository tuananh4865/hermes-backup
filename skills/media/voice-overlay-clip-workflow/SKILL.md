---
name: voice-overlay-clip-workflow
title: Voice overlay for short-form clips (TTS-generated Vietnamese voice over existing video)
description: Generate Vietnamese voice via OmniVoice clone and overlay onto existing TikTok clip. Three modes - A (prepend intro voice), B (replace voice segments in-place), C (insert voice PAIN segment mid-clip with multi-segment video source).
version: 0.4.0
author: Hermes
platforms: [macos]
metadata:
  hermes:
    tags: [Voice, TTS, OmniVoice, Overlay, TikTok, Vietnamese, Translation, Emotion-Tag, Multi-Segment, Problem-Solution]
    patches:
      - v0.4.0 (28/07): V15 (Mode C insert voice PAIN mid-clip for PROBLEM to SOLUTION framework when source transcript lacks PAIN setup) + reference recipe for clip_0697
      - v0.4.0 (28/07): V15 (Mode C insert voice PAIN mid-clip for PROBLEM to SOLUTION framework when source transcript lacks PAIN setup) + reference recipe for clip_0697 + V16 (Whisper transcript coverage ≠ audio quality; emit ựm/ờ/à/ồ/ờm/ừm that Whisper DOES NOT catch; ZERO emotion tag default rule)
      - v0.3.0 (26/07): V11 (Whisper hallucinate numbers) + V12 (HOOK tag selection) + V13 (user fade rule voice NO and audio fade OK) + V14 (RMS analysis mandatory)
      - v0.2.0 (25/07): V9 (no char-repeat for keo dai) + V10 (tag mid-paragraph fails) + note on user bo tag dau then best response
---

# Voice Overlay for Short-Form Clips

Generate Vietnamese voiceover with Tuấn Anh's cloned voice (via OmniVoice) and overlay it onto an existing short-form video. Three distinct modes — pick based on Tuấn Anh's request:

- **Mode A — ADD VOICE TO EMPTY SPOT** (voice intro before existing audio): prepend voice clip at start, fade in original audio from voice end.
- **Mode B — REPLACE VOICE SEGMENTS** (translate existing voice to Vietnamese): mute original audio ONLY during voice segments, fade in/out around them.
- **Mode C — INSERT VOICE SEGMENT MID-CLIP** (NEW 28/07): when source transcript lacks emotional PAIN/setup for PROBLEM→SOLUTION framework, insert OmniVoice-generated PAIN segment between source video segments with multi-segment filter_complex.

All modes preserve the original video, the original music/sound effects, and produce an iPhone-friendly output MP4 in the canonical folder.

## When to Use

- Tuấn Anh says: "thêm voice vào đầu clip", "ghép voice vào video", "dùng omnivoice tạo voice + ghép vào video"
- Tuấn Anh says: "dịch voice trong clip sang tiếng Việt", "thay voice thoại", "replace voice", "voice bằng giọng clone"
- **Tuấn Anh says (Mode C):** "nếu không có thì sử dụng omnivoice để tạo voice chèn vào" / "sắp xếp lại nội dung theo vấn đề và giải pháp" / "voice PAIN missing then generate" / when creative arrange framework (HOOK→PAIN→SOLUTION→USP→CTA) needs PAIN segment that source transcript doesn't have
- Project: short-form vertical content (TikTok/Reels/Shorts) where Vietnamese voiceover adds value
- Source voice prompt: Tuấn Anh's pre-saved clone at `/Volumes/Storage-1/Hermes/voice-prompts/`

Trigger phrases: "dùng omnivoice dịch lại voice trong clip thành tiếng Việt", "thay voice bằng giọng clone", "ghép voice clone vào clip", "voice overlay", **"sắp xếp lại theo vấn đề giải pháp + omnivoice chèn voice", "insert voice PAIN"**.

## Prerequisites

- `yt-dlp`, `ffmpeg`, `ffprobe` on PATH (see `youtube-shorts-to-iphone-download` for download step)
- OmniVoice venv at `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python`
- OmniVoice skill at `~/.hermes/skills/omnivoice-voice-clone/scripts/` for `generate_voice.py` + `concat_segments.py`
- Voice clone prompt `.pt` file already saved (e.g. `tuan_anh_5s_1sent_amp.pt`, `tuan_anh_session_2026-07-23.pt`)
- Whisper available via `~/.hermes/scripts/whisper-transcribe` (NOT on PATH by default)
- **For Mode C:** tiktok-video-editor skill loaded (provides PITFALL #89 CREATIVE ARRANGE framework + keep_plan.json conventions)

## How to Run

Three phases — download (if needed), generate voices, mix overlay.

```bash
# Phase 1 (if source is YouTube/Facebook URL): download via youtube-shorts-to-iphone-download
# Skip if file already exists in /Volumes/Storage-1/Tiktok-Tuan-Anh/

# Phase 2: transcribe audio for timing + segments
ffmpeg -y -i <VIDEO> -ar 16000 -ac 1 -c:a pcm_s16le /tmp/audio.wav
~/.hermes/scripts/whisper-transcribe /tmp/audio.wav /tmp/transcripts/
```

Phase 3 (mode-dependent): generate + overlay.

## Quick Reference

- **Voice prompt:** `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt` (default) OR `tuan_anh_session_2026-07-23.pt` (more natural review-style)
- **Voice dir:** `/Volumes/Storage-1/Hermes/scratch/voice-clone/<clip_id>/`
- **Output:** `/Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_<mode>.mp4`
- **Mode A suffix:** `_with_voice.mp4`
- **Mode B suffix:** `_vi_voice.mp4`
- **Mode C suffix:** `_v3_<framework>.mp4` (e.g. `_v3_problem_solution.mp4`)
- **Verify:** ffprobe must show H.264 + AAC 44100Hz + STEREO + 1080×1920

## Procedure — Mode A (Voice Prepend)

1. **Generate single voice** with emotion tag from a Vietnamese text:

   ```bash
   /Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python \
     ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
     --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt \
     --text "[surprise-oh] momota đoạn này thì đại đế phải gọi bằng mồm[laughter]" \
     --output /Volumes/Storage-1/Hermes/scratch/voice-clone/<clip>_intro.wav \
     --no-verify
   ```

2. **Extract audio from video**:

   ```bash
   ffmpeg -y -i <VIDEO> -vn -c:a copy /tmp/audio.m4a
   ```

3. **Build filter chain** — voice at start (0 → VODUR), original audio mute 0 → VODUR, fade in VODUR → VODUR+FADEDUR, full after. Use `apad=whole_dur=AUDIO_DUR` for voice to match audio length.

   ```bash
   filter_complex="[0:a]aresample=44100,afade=t=out:st=2.37:d=0.03,apad=whole_dur=46.88[v]; \
   [1:a]aresample=44100,volume=enable='between(t,0,3.6)':volume=0,afade=t=in:st=3.6:d=2.0[a]; \
   [v][a]amix=inputs=2:duration=longest:dropout_transition=0[mix]; \
   [mix]loudnorm=I=-16:TP=-1.5:LRA=11[out]"
   ```

   ⚠️ See Pitfall V1 — `volume` filter with `enable` does NOT preserve audio OUTSIDE the range. Use `volume=1.0` default and use `afade` for boundaries.

4. **Combine audio mix with video** (H.264 copy, AAC re-encode stereo 44100Hz):

   ```bash
   ffmpeg -y -i <VIDEO> -i /tmp/audio_mixed.m4a \
     -map 0:v -map 1:a \
     -c:v copy -c:a aac -b:a 128k \
     -movflags +faststart \
     /Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO>_with_voice.mp4
   ```

## Procedure — Mode B (Voice Replace with Translation)

1. **Whisper transcribe** the source to get segment timestamps. Read the `.json` file for word-level timings.

2. **Translate each spoken segment** to Vietnamese. **Manually fix common Whisper errors** before generating:
   - Names of players: "Tommy Sugiyato" → "Tommy Sugiarto" (real name)
   - Vietnamese name conventions: "Lý Trong Wei" → "Lý Trọng Vĩ" (TV common name for Lee Zii Jia)

3. **Add emotion tag per segment** based on rhetorical intent:
   - Rhetorical question → `[question-ah]`
   - Awe/admiration → `[amazement-oh]`
   - Invitation to watch → `[confirmation-en]`
   - Punchline reveal → `[laughter]` appended at end

4. **Build JSONL with per-segment text** (id, text, start, end). Generate **one voice at a time** to avoid MPS batch bug (Pitfall O1):

   ```bash
   /Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python \
     ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
     --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt \
     --text "[question-ah] Đó là smash cực mạnh đúng không?" \
     --output /Volumes/Storage-1/Hermes/scratch/voice-clone/<clip>/0.wav \
     --no-verify
   # Repeat for id=1, 2, 3...
   ```

5. **Build filter chain — voice overlays at original segment start times, audio gốc muted ONLY in voice range**:

   ```bash
   filter_complex="
   [0:a]aresample=44100,afade=t=out:st=2.37:d=0.03[v0];
   [1:a]aresample=44100,afade=t=out:st=3.09:d=0.03[v1];
   [2:a]aresample=44100,afade=t=out:st=3.65:d=0.03[v2];
   [3:a]aresample=44100,afade=t=out:st=4.61:d=0.03[v3];
   [v0]adelay=3760|3760[a0];
   [v1]adelay=6160|6160[a1];
   [v2]adelay=9280|9280[a2];
   [v3]adelay=12960|12960[a3];
   [a0][a1]amix=inputs=2:duration=longest:dropout_transition=0[m01];
   [m01][a2]amix=inputs=2:duration=longest:dropout_transition=0[m012];
   [m012][a3]amix=inputs=2:duration=longest:dropout_transition=0[voices_raw];
   [voices_raw]volume=1.4,aresample=44100[voices];
   [4:a]aresample=44100,
   volume='if(lt(t,3.76),1,if(lt(t,4.26),(4.26-t)/0.5,if(lt(t,17.60),0,if(lt(t,19.60),(t-17.60)/2,1))))'
   :eval=frame[audio_muted];
   [voices][audio_muted]amix=inputs=2:duration=longest:dropout_transition=0[mix]"
   ```

6. **Combine with video** (same as Mode A step 4).

## Procedure — Mode C (Insert Voice PAIN Mid-Clip for PROBLEM→SOLUTION)

**Use when:** Creative arrange framework (HOOK→PAIN→SOLUTION→USP→CTA) needs PAIN setup but source transcript doesn't have it (e.g. clip reviews honest limitation but lacks "Apple Pencil giá cao / bút rẻ thiếu tính năng" framing).

**Pattern:** PAIN voice = synthetic (OmniVoice-generated). Video B-roll = source clip segment (any source range, typically opening where product is shown).

### Step 1: Generate PAIN voice with OmniVoice

Use a recent voice clone (e.g. `tuan_anh_session_2026-07-23.pt` — anh's natural review voice from 23/07) for authentic PAIN tone. **Emotion tag pattern: `[sigh]` opening + `[question-ah]` close.**

```bash
PAIN_SCRIPT='[sigh]Bạn nào dùng iPad mà muốn sắm bút cảm ứng thì chắc chắn là sẽ đau đầu nha. Mua Apple Pencil chính hãng thì giá cả triệu bạc, mà mua bút rẻ tiền thì sạc không dây cũng không có luôn, kết nối cũng chậm nữa. [question-ah]Vậy thì phải làm sao đây?'

/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python \
  ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_session_2026-07-23.pt \
  --text "$PAIN_SCRIPT" \
  --output /tmp/voice_pain.wav
```

### Step 2: Build keep_plan with PAIN as voice_overlay type

In `keep_plan.json`, mark PAIN segment with `type: "voice_only"` instead of `"video_audio"`:

```json
{
  "name": "PAIN_OMNIVOICE_VIS",
  "src": [4.82, 24.54],
  "duration": 19.72,
  "type": "voice_overlay",
  "voice_file": "/tmp/voice_pain.wav",
  "purpose": "PAIN OmniVoice: Apple Pencil giá triệu vs bút rẻ thiếu tính năng then user phải làm sao?"
}
```

### Step 3: Build multi-input filter_complex

For each keep in keep_plan, add 1 input per video segment. **Voice-overlay keeps add 2 inputs** (1 source B-roll + 1 voice file). Build filter chain:

```python
keeps = [
    {"name": "HOOK_PRICE",           "src": [20.36, 31.08],   "dur": 11.04},
    {"name": "PAIN_OMNIVOICE_VIS",  "src": [4.82, 24.54],    "dur": 19.72, "voice_overlay": "/tmp/voice_pain.wav"},
    {"name": "SOLUTION_FEATURES",    "src": [216.02, 251.02], "dur": 35.32},
    {"name": "CTA",                  "src": [258.94, 285.52], "dur": 26.90},
]
n = len(keeps)
inputs = []
v_parts, a_parts, v_labels, a_labels = [], [], [], []
input_idx = 0
for i, k in enumerate(keeps):
    src_start, src_end = k["src"]
    dur = src_end - src_start
    if k.get("voice_overlay"):
        # Video B-roll from source
        inputs.append(f"-ss {src_start:.3f} -t {dur:.3f} -i <source.MOV>")
        v_idx = input_idx
        # Voice overlay file
        inputs.append(f"-i {k['voice_overlay']}")
        a_idx = input_idx + 1
        v_parts.append(f"[{v_idx}:v]trim=start=0:end={dur:.3f},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30[v{i}]")
        a_parts.append(f"[{a_idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=44100[a{i}]")
        input_idx += 2
    else:
        inputs.append(f"-ss {src_start:.3f} -t {dur:.3f} -i <source.MOV>")
        v_idx = input_idx
        v_parts.append(f"[{v_idx}:v]trim=start=0:end={dur:.3f},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30[v{i}]")
        a_parts.append(f"[{v_idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=44100[a{i}]")
        input_idx += 1
    v_labels.append(f"[v{i}]")
    a_labels.append(f"[a{i}]")
v_concat = "".join(v_labels) + f"concat=n={n}:v=1:a=0[vout]"
a_concat = "".join(a_labels) + f"concat=n={n}:v=0:a=1[aout]"
filter_str = ";".join(v_parts + a_parts + [v_concat, a_concat])
```

### Step 4: Apply speed 1.3x after pre-speed render

Same as standard tiktok-video-editor workflow — render `v3_pre_speed.mp4` → speed 1.3x → `v3_final.mp4`.

### Verified reference recipe (clip_0697, 28/07)

- **Source**: DJI_20260707123724_0697_D.MP4 (bút cảm ứng iPad Gojodot Pro)
- **Source transcript**: 43 segments, 324.6s — has HOOK, PRICE, FEATURES, but NO PAIN setup (no "Apple Pencil giá cao" / "bút rẻ thiếu tính năng" framing)
- **Voice PAIN script**: `[sigh]Bạn nào dùng iPad mà muốn sắm bút cảm ứng thì chắc chắn là sẽ đau đầu nha. Mua Apple Pencil chính hãng thì giá cả triệu bạc, mà mua bút rẻ tiền thì sạc không dây cũng không có luôn, kết nối cũng chậm nữa. [question-ah]Vậy thì phải làm sao đây?`
- **Voice clone**: `tuan_anh_session_2026-07-23.pt` (ref_rms=0.1100)
- **Generated voice**: 19.72s, 24kHz mono pcm_s16le, max -0.0 dB, mean -19.6 dB
- **B-roll video**: source range [4.82, 24.54] (opening where anh shows cây bút)
- **Final keep_plan**: HOOK_PRICE → PAIN_OMNIVOICE → SOLUTION_FEATURES → 3 PROOF → CTA (7 segments)
- **Final duration**: 98.97s (Mode B 75-110s)
- **Whisper verify**: large-v3-mlx transcribes PAIN script 100% accurate
- **File output**: `clip_0697_V3_PROBLEMSOLUTION_99s_FINAL_BUT-CAM-UNG-IPAD-GOJODOT.mp4`

Reference wiki: `/Volumes/Storage-1/Hermes/wiki/queries/clip_0697_problem_solution_omnivoice_demo_2026-07-28.md`

## Pitfalls

### V1. **`volume=enable='between(t,...)':volume=0` does NOT preserve audio OUTSIDE the range**

**Symptoms:** Audio gốc bị silent hoàn toàn cả video (peak -91 dB ở cả đầu lẫn cuối), không chỉ trong range đã chỉ định.

**Root cause:** `volume` filter không có giá trị default = 1.0 ngoài `enable` range. Filter chỉ apply rule trong range, ngoài range thì output = input volume (nhưng ở đây không preserve).

**Fix:** Use piecewise `volume` expression với `:eval=frame`:

```bash
volume='if(lt(t,START_VOICE),1,if(lt(t,START_VOICE+FADE_OUT),(START_VOICE+FADE_OUT-t)/FADE_OUT,if(lt(t,END_VOICE),0,if(lt(t,END_VOICE+FADE_IN),(t-END_VOICE)/FADE_IN,1))))'
```

**Verified 2026-07-14 (ZGOu1-J8Vb0):** Sau khi fix, audio gốc peak -5.3 dB ở t=3.5s (trước voice), silent ở t=4.5-17s (trong voice), peak -0.0 dB ở t=20-24s (sau voice fade in) — đúng logic mix.

### V2. **`amix inputs=2` divides volume by 2 even when only 1 stream active**

**Symptom:** Audio gốc bị giảm ~6 dB khi chỉ mix với silence track (vì amix average 2 streams dù 1 stream silent).

**Fix:**
- `dropout_transition=0` — không fix được, chỉ giảm ramp transition
- Dùng weights: `amix=inputs=2:weights=2 2` (nhân đôi) → vẫn divide theo số input
- Cleanest: tránh amix khi chỉ 1 stream active. Dùng `concat` thay vì `amix` cho sequential voice tracks
- Hoặc accept -6dB loss + boost final mix với `volume=1.4` để compensate

**Verified 2026-07-14 (ZGOu1-J8Vb0):** Boost `volume=1.4` cho voices track trước khi mix → final peak ~-0.3 to -10 dB, nghe rõ cả voice + audio.

### V3. **Voice track duration thường dài hơn Whisper segment duration**

**Symptom:** Voice Việt có thể dài 1.5-2× transcript segment window do pace tiếng Việt + emotion tag pauses.

**Ví dụ 2026-07-14 (ZGOu1-J8Vb0):**
- Whisper detected: 4 segments × ~2s window = 9.16s total voice range
- OmniVoice generated: 2.40 + 3.12 + 3.68 + 4.64 = 13.84s total voice duration
- Difference: ~4.7s overlap giữa các segments

**Decision rule:** KHÔNG pitch-time hoặc speed-up voice (sẽ làm Tuấn Anh nghe khác lạ). Chấp nhận overlap tự nhiên — voice Việt chậm hơn transcript gốc vì pace tiếng Việt + emotion tags cần thêm pause. Align voice START theo segment start time; voice sẽ tự overlap với segment sau nếu dài hơn.

### V4. **`loudnorm` ở end of filter chain gây peak cao**

**Symptom:** Sau loudnorm, audio ở phần sau (sau voice) có peak -0.0 to -0.3 dB → gần clipping.

**Fix:** Skip loudnorm nếu không cần normalize loudness cho TikTok (TikTok đã auto-gain). Dùng `volume=1.4` để boost voice thay vì loudnorm.

**Verified 2026-07-14:** Mode B (replace) skip loudnorm → peak cuối -0.0 to -4.4 dB, nghe OK. Mode A dùng loudnorm OK vì voice đầu cần boost.

### V5. **MPS batch bug với OmniVoice JSONL mode**

**Symptom:** `generate_voice.py --jsonl` với ≥5 file có thể produce silent output (Pitfall #1 từ skill omnivoice).

**Fix:** Generate 1-by-1 với `--text` mode thay vì `--jsonl`. Mất ~12s/file vs 11s/file batch, nhưng reliable.

**Verified 2026-07-14 (ZGOu1-J8Vb0):** JSONL batch 4 files bị interrupted → orphan 2 files. Em retry sequential `--text` mode cho 2 file còn lại → 100% reliable.

### V6. **Translate Whisper names BEFORE generating voice**

**Symptom:** Voice Việt đọc sai tên cầu thủ (Whisper heard "Tommy Sugiyato" → Vietnamese voice reads "Tommy Sugiyato" theo).

**Fix:** Sau khi Whisper transcribe, đọc lại JSON, fix common errors:
- Real player names vs Whisper guess
- Vietnamese TV-name conventions
- Acronym/abbreviation spellings

### V7. **Always send the output to Telegram as MEDIA even if video is "no voice"**

If the final mix has audio issues (silent range, peak clipping), DON'T ship — re-render with fix from Pitfall V1 or V2. Tuấn Anh expects every shipped file to play correctly on iPhone first try.

### V9. **KHÔNG dùng ký tự lặp (iiii/aaaa) để "kéo dài" voice cuối câu** (USER CORRECTION 25/07)

**Symptoms:** Voice cuối câu nghe giống "goalllll" (hét kéo dài) thay vì thở dài thương xót. RMS peak ở phần cuối tăng ~2.4× so với baseline (verified 25/07: 7346 vs 3073).

**Root cause:** OmniVoice (và nhiều TTS model) KHI THẤY KÝ TỰ LẶP sẽ generate phoneme kéo dài với amplitude cao (vì model's training data có shouting/celebration có chuỗi vowel kéo dài). Kết quả là "Tộiiiiiii" → "goalllll" không phải "Tội…".

**Anh's verbatim feedback 25/07:** *"Tội là câu cảm thán kiểu thở dài thấy thương đồ á chứ hiện tại đang giống goalllll hơn"*

**Fix:** Dùng **ellipsis `…`** (Unicode U+2026) kết hợp emotion tag `[sigh]` thay vì lặp ký tự:

```text
# WRONG — ký tự lặp → "goalllll" effect:
[sigh] Tộiiiiiiii…

# CORRECT — ellipsis + sigh tag → soft thở dài tự nhiên:
[sigh] Tội…
```

**Verified 25/07 (clip VXgN3KtMt0M):**

| Pattern | Peak RMS (cuối câu) | Character |
|---|---|---|
| `Tội…` + `[sigh]` | 3073 | Thở dài, buông, soft ✅ |
| `Tộiiiiiiii…` + `[sigh]` | 7346 | Hét kéo dài (goalllll) ❌ |

→ Peak thấp hơn ~60% = voice buông = đúng emotion "thở dài thương xót".

**Generalize rule:** Bất kỳ khi nào cần voice "mềm/kéo dài/buông" ở cuối câu, dùng `[sigh]` + `…`. KHÔNG BAO GIỜ dùng `iiii`/`aaaa`/`ooo`/`eee` để mimic độ dài.

### V10. **Emotion tag KHÔNG đặt giữa segment — phải ở đầu paragraph** (VERIFIED 25/07)

**Symptoms:** Whisper transcript miss HOOK hoàn toàn (0-3.4s silent) + model đọc emotion tag thành chữ "Ô" / "Ồ" trong transcript.

**Verified transcript 25/07 (V4 với tag mid-paragraph):**

```text
# Text (tag giữa segment):
"Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà [amazement-oh]! 
Chắc là anh Ly Chong Quây ám ảnh từ đây [surprise-oh]! 
Tội [sigh]…"

# Whisper transcript (FAIL):
[0.0s - 3.4s]       ← silent (HOOK miss)
[3.4s]  "Mà Amos mình"
[4.1s]  "Ô"          ← model đọc [amazement-oh] thành "Ô"
[4.6s]  "Chắc là anh Ly Trong quay ám ảnh từ đây"
[6.4s]  "Ô"          ← model đọc [surprise-oh] thành "Ô"
[7.4s]  "Tội"
```

**Root cause:** Skill `omnivoice-voice-clone/references/punct-rule-and-longparagraph-2026-07-23.md` đã quy định rõ: **"Emotion tag đứng đầu paragraph DÀI (30-45 từ) — gộp 3-5 ý vào 1 đoạn để emotion tag tạo 1 pause DUY NHẤT, sau đó voice chạy liền mạch."** Khi tag ở giữa câu:

1. Model PAUSE toàn bộ câu trước tag → Whisper miss HOOK
2. Model đọc chữ cái trong tag (o/h/n/oh/ah) thành filler words

**Fix:** Emotion tag PHẢI ở đầu paragraph (sau khi xuống dòng hoặc sau dấu `.` cuối câu trước). Pattern đã verify PASS 25/07:

```text
# CORRECT (tag đầu paragraph):
[amazement-oh] Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà! 
[surprise-oh] Chắc là anh Ly Chong Quây ám ảnh từ đây! 
[sigh] Tội…

# Whisper transcript (PASS):
[0.0s] "Máy dập Linh Đan 2058"      ← HOOK heard đúng
[2.0s] "Dập Ly Trong Quay 2 hiệp teo người luôn mà"
[4.3s] "Ồ chắc là anh Ly Trong Quay ám ảnh từ đây"   ← "Ồ" = model đọc [surprise-oh] thành filler 1 lần, OK
[7.7s] "Tội"
```

**Anti-pattern rule:** KHÔNG BAO GIỜ đặt emotion tag giữa câu — luôn đặt ở đầu paragraph hoặc sau dấu `.` cuối câu trước.

**Khi user yêu cầu "bỏ emotion tag đầu câu":** Đây thường là nhầm lẫn do user đang nghe emotion peak quá cao (vd "goalllll" từ V9) và nghĩ tag là nguyên nhân. **Best response:** giữ tag đầu paragraph (memory rule bắt buộc), thay bằng emotion tag KHÁC phù hợp nội dung hơn:

```text
# User: "bỏ amazement-oh đi" vì "Tội" nghe "goalllll"
# Nhầm: bỏ tag → HOOK miss (V10 anti-pattern)
# Đúng: thay [amazement-oh] bằng emotion khác ([laughter], [surprise-oh]) 
#        + fix root cause (V9: bỏ ký tự lặp, dùng ellipsis)

# Verified 25/07 v5:
[laughter] Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà! 
[surprise-oh] Chắc là anh Ly Chong Quây ám ảnh từ đây! 
[sigh] Tội…   ← elllipsis, không "iiii"
```

### V8. **Paren mismatch trong piecewise volume expression → "Invalid chars ')'"**

**Symptom:** ffmpeg rejects `volume='...'` filter với error: `Invalid chars ')' at the end of expression 'if(...)'`. Filter fails to initialize, exit code 234.

**Root cause:** Nếu có N nested `if(...)`, cần đúng N closing `)` ở cuối. Viết nhầm N+1 or N+2 `)` → parser thấy extra `)` không match.

**Verified 25/07 (VXgN3KtMt0M):**

```bash
# WRONG (5 closing parens for 3 if's — mismatch):
volume='if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,8.2),0,if(lt(t,10.2),(t-8.2)/2.0,1))))'

# CORRECT (3 closing parens):
volume='if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,8.2),0,if(lt(t,10.2),(t-8.2)/2.0,1)))'
```

**Fix:** Đếm `if(` mở ngoặc → đếm `)` đóng ngoặc phải khớp. Khi viết inline dễ quên. Tip: dùng Python f-string để build:

```python
n_voice = 8.2
fade = 2.0
expr = (f"if(lt(t,0.3),(0.3-t)/0.3,"   # 1 open
        f"if(lt(t,{n_voice}),0,"         # 2 open
        f"if(lt(t,{n_voice+fade}),(t-{n_voice})/{fade},1)))\")  # 3 closing
# 3 ifs → 3 closing parens
```

Khi build piecewise volume với N=3 if (standard 4-region: pre-voice-fade / voice / post-voice-fade / full) → luôn phải có đúng 3 `)))`. Nếu filter chain fail với "Invalid chars", kiểm tra count `(` vs `)` ngay.

### V11. **Whisper hallucinate NUMBERS trong compound Vietnamese phrases** (VERIFIED 26/07 VXgN3KtMt0M)

**Symptoms:** User flag "voice nói sai số" nhưng voice thực tế đã đúng — Whisper (large-v3-mlx) hallucinate numbers:
- Voice input: `"...dập Ly Chong Quây 2 hiệp teo người luôn mà..."`
- Whisper transcript: `"...Dập Ly Trong Quay 2 không lẻ 8 teo người luôn mà..."`
- Voice thực tế vẫn đọc "2 hiệp" đúng (RMS profile confirm)

**Common hallucinations:**
- "2 hiệp" → "2 không lẻ 8"
- "100k" → "một trăm k"
- "500K" → "500 ca"

**Production rule (FIRST-CLASS):**
1. **KHÔNG regenerate voice** khi user flag "voice nói sai số" — Whisper có thể hallucinate
2. **Verify voice bằng 2 sources:**
   - Whisper transcript (có thể sai number)
   - Crop audio ở timestamp đó + RMS analysis
3. **Nếu voice thực sự sai** → fix text + regenerate

**Verified recipe (RMS analysis):**
```python
import wave, numpy as np
with wave.open("output.wav", "rb") as wav:
    frames = wav.getnframes()
    rate = wav.getframerate()
    raw = wav.readframes(frames)
audio = np.frombuffer(raw, dtype=np.int16)
samples_per_sec = rate
# Chunk analysis
chunk = int(0.1 * samples_per_sec)
for i in range(int(2.0 * samples_per_sec), int(4.0 * samples_per_sec), chunk):
    rms = np.sqrt(np.mean(audio[i:i+chunk].astype(np.float32) ** 2))
    print(f"  t={i/samples_per_sec:.2f}s: rms={rms:.1f}")
```

### V12. **HOOK emotion tag selection affects Whisper transcript start** (VERIFIED 26/07)

**Symptom:** HOOK có technical content (tên riêng, số) → emotion tag mạnh `[laughter]`/`[amazement-oh]` gây Whisper MISS phần đầu HOOK.

**Verified test 26/07 (3 variants on same text):**

| Variant | HOOK tag | Whisper HOOK | Verdict |
|---|---|---|---|
| v5 (giữ laughter, bỏ amazement) | `[laughter]` | (miss) | ❌ |
| **v6b (confirmation-en)** | `[confirmation-en]` | **"Mấy dập Linh Đan 2008"** ✅ | ✅ **CHỌN** |
| v6c (laughter + long sigh) | `[laughter]` | "Giập Linh Đan 2008" (mất "Máy") | ❌ |

**Root cause:** Emotion tags mạnh khiến model "rush" qua HOOK quá nhanh → Whisper miss. Tags nhẹ hơn (`[confirmation-en]`) cho model thời gian đọc rõ từng từ.

**Production rule:**
1. **HOOK có technical numbers/words** → dùng `[confirmation-en]` thay `[laughter]`/`[amazement-oh]`
2. **Nếu Whisper transcript bị MISS HOOK** → đổi HOOK tag theo priority: `[confirmation-en]` > `[confirmation-yi]` > `[laughter]` > `[amazement-oh]`
3. **Boost voice volume 1.4 → 1.8x** khi mix với audio gốc (vì tag nhẹ → voice start soft)

### V13. **User fade rule: voice NO afade, audio gốc FADE piecewise OK** (USER CLARIFICATION 26/07)

**Anh's verbatim 26/07:** *"Ý anh là không được fade in fade out voice thôi còn cách ghép voice vào video phải fade audio của video là đúng rồi"*

**Critical clarification:** KHÔNG hiểu nhầm "no fade = không fade gì cả". RULE THỰC TẾ:
- **Voice:** KHÔNG `afade` (peak instant ở 0.0s)
- **Audio gốc:** FADE piecewise là đúng (fade out 0.3s → mute → fade in 2s → full)

**Anti-pattern (NEVER):**
```bash
# SAI — afade voice
[1:a]aresample=44100,afade=t=in:st=0:d=0.3,afade=t=out:st=7.7:d=0.3,apad=whole_dur=20.97,volume=1.4[voice]
# → voice bị mờ đầu/cuối, không nghe rõ HOOK
```

**Correct:**
```bash
# ĐÚNG — voice NO fade, audio gốc fade piecewise
[1:a]aresample=44100,apad=whole_dur=20.97,volume=1.4[voice]
[2:a]aresample=44100,volume='if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,8.0),0,if(lt(t,10.0),(t-8.0)/2.0,1)))':eval=frame[audio]
[voice][audio]amix=inputs=2:duration=longest:dropout_transition=0[mix]
```

**Volume sampling verify:**
- t=0.0s, 0.1s: voice peak instant (-7 to -8 dB) — NO gradient
- t=8.0s: voice stopped, audio gốc vẫn mute
- t=10.0s+: audio gốc full (-9 to -10 dB)

### V14. **RMS waveform analysis MANDATORY for trailing vowel verify** (VERIFIED 26/07)

Khi user flag "Tộiiii kéo dài thành goalllll" → verify bằng RMS analysis, KHÔNG chỉ Whisper transcript.

**Recipe:** See V11 RMS analysis code.

**Threshold:**

| RMS peak | Character | Action |
|---|---|---|
| < 3000 | soft/buông (thở dài) | ✅ OK |
| 3000-5000 | medium | ✅ OK |
| 5000-7000 | high (hào hứng) | ✅ OK cho HOOK |
| > 7000 | hét | ⚠️ Cảm giác "goalllll" |

Verified: v2 (`Tộiiii`) peak 7346 = HÉT, v3 (`Tội…` + `[sigh]`) peak 3073 = thở dài soft.

### V15. **Mode C: Voice overlay PAIN setup needs OmniVoice when source transcript lacks it** (NEW 28/07)

**Trigger:** Tuấn Anh yêu cầu re-arrange content theo Problem→Solution framework (HOOK→PAIN→SOLUTION→USP→CTA), nhưng source transcript chỉ có HONEST LIMITATION review chứ KHÔNG có PAIN setup (e.g. "Apple Pencil giá triệu / bút rẻ thiếu tính năng / vậy phải làm sao?").

**Anh's verbatim 28/07:** *"Nếu không có thì sử dụng omnivoice để tạo voice chèn vào"*

**Symptoms:**
- Source transcript review sản phẩm (e.g. bút cảm ứng iPad) → chỉ list features + limitations
- KHÔNG có framing "Apple Pencil giá triệu → khó mua" hay "bút rẻ thiếu tính năng → không đáng tin"
- User yêu cầu PAIN/SOLUTION framework → PAIN setup missing
- Nếu chỉ re-arrange source transcript → PAIN segment yếu, narrative arc không punch

**Solution: Use OmniVoice generate synthetic PAIN script + overlay trên source B-roll**

**Pattern:**
1. **Analyze source transcript**: xác định segment nào là "HONEST LIMITATION" (e.g. clip_0697 segment 20-23: "Bấm 2 lần + cảm biến lực KHÔNG có") → đây là PAIN có sẵn nhưng chưa đủ framing cho Solution.
2. **Write PAIN script** mới (creative, 3-5 câu, ~15-20s):
   - Khai báo PAIN context (Apple Pencil giá cao, bút rẻ thiếu tính năng)
   - Emotion tag pattern: `[sigh]` opening + `[question-ah]` close
   - Use voice clone gần nhất của anh (e.g. `tuan_anh_session_2026-07-23.pt` — natural review voice)
3. **Generate voice** bằng OmniVoice skill:
   ```bash
   /Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python \
     ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
     --prompt /Volumes/Storage-1/Hermes/voice-prompts/<session-voice>.pt \
     --text "$PAIN_SCRIPT" \
     --output /tmp/voice_pain.wav
   ```
4. **Pick B-roll source range**: chọn source range 15-20s có visual phù hợp (e.g. opening where anh shows sản phẩm) — KHÔNG cần source audio cho range này vì voice overlay thay thế
5. **Build multi-input filter_complex** (see "Procedure — Mode C" above)
6. **Verify**: Whisper large-v3-mlx transcribe PAIN script 100% accurate (anh's voice + correct script)

**Verified recipe (clip_0697, 28/07):**
- Source: DJI_20260707123724_0697_D.MP4 (bút cảm ứng iPad Gojodot Pro)
- Source has 43 segments, 324.6s — has HOOK, PRICE, FEATURES, but NO PAIN setup
- PAIN script: `[sigh]Bạn nào dùng iPad mà muốn sắm bút cảm ứng thì chắc chắn là sẽ đau đầu nha. Mua Apple Pencil chính hãng thì giá cả triệu bạc, mà mua bút rẻ tiền thì sạc không dây cũng không có luôn, kết nối cũng chậm nữa. [question-ah]Vậy thì phải làm sao đây?`
- Generated voice: 19.72s, 24kHz mono, max -0.0 dB, mean -19.6 dB
- B-roll source range: [4.82, 24.54] (opening where anh shows cây bút)
- Final duration: 98.97s (Mode B 75-110s ✓)
- Whisper verify: PAIN script transcribe 100% accurate
- File: `clip_0697_V3_PROBLEMSOLUTION_99s_FINAL_BUT-CAM-UNG-IPAD-GOJODOT.mp4`

**Workflow decision tree:**
```
User yêu cầu re-arrange PROBLEM→SOLUTION framework
├── Source transcript HAS PAIN setup (e.g. "giá Apple Pencil chính hãng cả triệu")
│   → Standard tiktok-video-editor creative arrange (Mode 2 demo clip_0088, clip_0095)
└── Source transcript LACKS PAIN setup (chỉ review features + limitations)
    → Mode C: generate OmniVoice PAIN script + overlay on B-roll (this V15)
```

## Verification

```bash
ffprobe -v error \
  -show_entries stream=codec_name,codec_type,sample_rate,channels \
  -show_entries format=duration,size \
  -of default=nw=1 \
  /Volumes/Storage-1/Tiktok-Tuan-Anh/<OUTPUT>.mp4
```

Pass criteria:
- `codec_name=h264` for video
- `codec_name=aac` + `sample_rate=44100` + `channels=2` for audio
- Duration matches input video (Mode A/B) OR matches pre_speed duration × 1.3 (Mode C)

**Volume sampling check** (especially for Mode B):

```bash
for t in 0.5 3.5 5.0 10.0 17.0 20.0 24.0; do
  ffmpeg -y -ss $t -i <OUTPUT> -t 1.0 -vn -f wav /tmp/c.wav
  ffmpeg -i /tmp/c.wav -af volumedetect -vn -f null - 2>&1 | grep max_volume
done
```

Pass criteria:
- Before voice range: audio gốc peak > -10 dB
- During voice range: peak > -15 dB (voice)
- After voice range (post fade-in): peak > -5 dB (audio gốc full)

**Whisper full-transcript verify (Mode C):**
```bash
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --language vi \
  --output-dir /tmp/transcript_check \
  --output-format txt \
  --word-timestamps True \
  <OUTPUT>.mp4

cat /tmp/transcript_check/*.txt
# Verify PAIN script words appear in correct order
```

### V16. **Whisper transcript coverage ≠ audio quality; emotion tags emit ựm/ờ filler Whisper CANNOT catch** (NEW 29/07)

**Symptoms:** User flag "có ựm ờ trong voice" ngay cả khi Whisper transcript pass với coverage ~98.7%. Agent đã ship "đạt PASS" trước khi user nghe.

**Root cause (verified 29/07 session):**
- Whisper (large-v3-mlx, language=vi) chỉ verify **TỪ có nghĩa**, không verify **âm thanh đệm** (`ờ`, `ừm`, `à`, `ồ`, `ờm`, `ựm`)
- ASR model train để output semantic content, không output filler — Whisper skip filler thay vì transcribe
- Emotion tags (`[question-ah]`, `[surprise-oh]`, `[amazement-oh]`) prepend phoneme đơn lẻ mà Whisper map về silence hoặc text gần nhất

**Anh's verbatim 2026-07-29:**
> *"Anh thấy có ựm ờ trong voice mà"*
>
> *"Chung quy anh muốn loại bỏ hoàn toàn ựm ờ à ồ ờm ừm đi và từ nay không được phép chèn các emotional tag có thể tạo ra các từ đó nữa"*

**Emotion tag risk matrix (verified 29/07):**
| Tag | Filler risk | Note |
|---|---|---|
| `[question-ah]` | HIGH | Phoneme "à" đầu đoạn |
| `[question-oh]` | HIGH | Phoneme "ô" đầu đoạn |
| `[question-oh/ei/yi]` | HIGH | Phoneme trailing đầu đoạn |
| `[surprise-ah/oh/wa/yo]` | HIGH | Phoneme đầu đoạn |
| `[amazement-oh]` | HIGH | "ờ" filler |
| `[laughter]` | LOW-MEDIUM | Không filler thường |
| `[sigh]` | LOW | Hơi thở, acceptable |
| `[confirmation-en]` | LOW | Ngắn, không kéo dài |
| `[dissatisfaction-hnn]` | MEDIUM | "hừm" |

**Rule mới (FIRST-CLASS, codified 29/07):**
1. **Default ZERO emotion tags** cho mọi voice generation.
2. Nếu user yêu cầu emotion tag, **A/B test trên smoke 5 đoạn** trước khi render cả batch.
3. **Bắt buộc listen test** trước khi giao MP3.
4. Whisper transcript pass KHÔNG guarantee voice "sạch".

**Verification recipe bổ sung:**
```bash
# RMS scan cho filler ở first/last 0.5s segment
for f in segments/*.wav; do
  head_rms=$(ffmpeg -nostats -hide_banner -i $f -af "atrim=start=0:end=0.5,asetnsamples=1" -f null - 2>&1 | grep -oP 'rms=\K[0-9.]+' | head -1)
  echo "$f: head_rms=$head_rms (caution if >1500)"
done
```

**Anti-pattern:** Tin Whisper transcript pass → ship. Sai. Bắt buộc listen test.

**Related:** `references/06-whisper-coverage-gap-2026-07-29.md` (full session notes), Pitfall #15 (Whisper hallucinate numbers), Pitfall #16 (RMS analysis mandatory).
