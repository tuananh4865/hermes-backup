---
title: PITFALL #38 — Audio Fade Check Workflow Integration
created: 2026-07-18
updated: 2026-07-18
type: reference
tags: [pitfall-38, audio-fade, tiktok-pipeline-studio, stage-5, hard-rule]
confidence: high
relationships: [audio-fade-check-pitfall-38-2026-07-18, tiktok-video-editor, browser-use-video-use]
---

# PITFALL #38 — Audio Fade Check Workflow Integration

> **Source:** anh yêu cầu 18/07 sau khi `check_audio_fade.py` phát hiện bug nghiêm trọng.
> **Apply:** Mọi Stage 5 verify của `tiktok-pipeline-studio` từ 18/07.

## 🎯 Tại sao PITFALL #38 ở Stage 5 (không phải Stage 3)

Audio fade là **production correctness** (HARD RULE), KHÔNG phải taste call. Lý do đặt ở Stage 5:

1. **Stage 3 (EDIT)** chỉ build `edl.json` → render draft.mp4 KHÔNG có audio fade
2. **Stage 4 (MOTION)** thêm glass cards / PIP / text → KHÔNG apply audio fade (HyperFrames composition)
3. **Stage 5 (VERIFY + SHIP)** = nơi cuối cùng trước khi ship → BẮT BUỘC check audio fade
   - Nếu fail → re-render ở Stage 3 với `afade` filter
   - Pattern: render → verify → fail → fix → re-verify → ship

## 📋 Workflow chi tiết trong Stage 5

```
[Stage 3 render] → [Stage 4 motion graphic] → 
   ↓
Stage 5 verify (5 calls):
1. python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py output.mp4
   ├─ exit 0 = PASS → tiếp step 2
   └─ exit 1 = FAIL → RE-RENDER ở Stage 3 với afade filter → loop lại
2. python3 scripts/verify_clip.py (5 layers: FILLER/TREO/LẶP/HOOK LẶP)
3. python3 scripts/check_anchor_lap.py (Pitfall #21 FALSE START scan)
4. ffprobe spec TikTok (1080×1920, AAC 44100Hz, ≥30fps)
5. Ship to pipeline/output/_shipped/<DATE>/
```

## 🛠️ Script: check_audio_fade.py

**Location:** `~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py` (7.7 KB)

**Usage:**
```bash
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py <video.mp4>
```

**Output:**
```
🎯 PITFALL #32 - AUDIO FADE CHECK
📂 Video: clip_xxx.mp4
⚙️  Fade expected: 30ms

📊 Step 1: Extract audio...
   Duration: 82.0s
📊 Step 2: Detect cut boundaries (silence gaps)...
   Found 52 cut boundaries
📊 Step 3: Check fade at each boundary...

  ✅ Cut #1 at 0.00s (269ms silence): fade-in, NO fade-out
  ❌ Cut #3 at 4.71s (68ms silence): NO fade-in, NO fade-out
  ...
  
✅ PASS - All 52 cut boundaries have audio fade
# OR
❌ FAIL - 50/52 boundaries missing audio fade
```

## 🔧 Re-render workflow khi FAIL

```bash
# Step 1: Detect fail
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py output.mp4
# → exit 1, hiển thị "N/M boundaries missing audio fade"

# Step 2: Re-render Stage 3 với afade filter
ffmpeg -y -ss $start -to $end -i SOURCE \
  -af "afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03" \
  segment_NN.mp4

# Step 3: Concat demuxer
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4

# Step 4: Re-verify
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py final.mp4
# → exit 0 = PASS → ship
```

## 🎓 Lessons vĩnh viễn

1. **3-layer enforcement** (tool + checklist + script) - KHÔNG chỉ dặn nhắc
   - Tool: `check_audio_fade.py` (executable)
   - Checklist: Stage 5 add item
   - Script: exit 0/1 → agent không bỏ qua được

2. **Audio fade là HARD RULE** (production correctness) - KHÔNG phải taste call
3. **Mọi cut boundary** đều cần fade - KHÔNG skip dù chỉ 1 take
4. **Verify sau MỖI render** - KHÔNG batch verify cuối ngày
5. **Re-render khi FAIL** - KHÔNG bỏ qua vì "có thể OK"

## 📊 Real case 18/07 (clip V78)

| Metric | Value |
|---|---|
| File | clip0003_V78_82s_FINAL_with_audio.mp4 |
| Status | SHIPPED 13/07 |
| Audio fade check 18/07 | **50/52 boundaries missing 30ms fade** ❌ |
| Action | Cần re-render với `afade` filter để ship production-ready |

## 📚 Related

- `references/audio-fade-check-pitfall-38-2026-07-18.md` (master reference)
- `~/.hermes/skills/media/tiktok-video-editor/SKILL.md` v3.35.0 (PITFALL #38)
- `browser-use/video-use` HARD RULE #3 (audio fades)
- `~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py`

---

*Created 2026-07-18 - tích hợp PITFALL #38 vào Stage 5 workflow sau khi phát hiện bug nghiêm trọng trên shipped clip V78.*
