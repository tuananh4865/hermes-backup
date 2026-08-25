---
title: Audio Fade Check PITFALL #38 — 30ms HARD RULE
created: 2026-07-18
updated: 2026-07-18
type: reference
tags: [pitfall-38, audio-fade, hard-rule, workflow-check, tiktok, video-use-pattern]
confidence: high
relationships: [tiktok-video-editor, browser-use-video-use, hermes-edit-folder-pattern]
---

# Audio Fade Check PITFALL #38 — 30ms HARD RULE

> **Source:** anh yêu cầu 18/07 sau khi `check_audio_fade.py` phát hiện bug nghiêm trọng trên clip V78 đã SHIP.

## 🚨 Vấn đề thực tế

**Clip `clip0003_V78_82s_FINAL_with_audio.mp4` (đã SHIPPED 13/07):**
- File size: 41.9 MB
- Duration: 82s
- Cut boundaries: 52
- **`check_audio_fade.py` phát hiện: 50/52 boundaries KHÔNG có 30ms fade** ❌
- 96% boundaries = 50 chỗ "pop" / "click" trong 82s = KHÔNG production-ready

→ **Bug nghiêm trọng** đã ship mà không ai check audio fade.

## 🎯 HARD RULE mới (PITFALL #38)

**Mọi clip TikTok Mode B PHẢI có 30ms audio fade in/out ở MỌI cut boundary:**

```bash
# Per-segment extract (PITFALL #30 đã require):
ffmpeg -y -ss $start -to $end -i SOURCE \
  -af "afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03" \
  segment_NN.mp4

# Concat demuxer (no re-encode):
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4

# Verify NGAY:
python3 scripts/check_audio_fade.py <final>.mp4
# → exit 0 = PASS, exit 1 = FAIL → re-render với afade
```

## 📋 Pattern from `browser-use/video-use` (HARD RULE #3)

```python
# Repo này enforce 12 hard rules, rule #3:
# "30ms audio fades ở MỌI cut boundary 
#  (afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03). 
#  Nghe nhỏ nhưng là rule sống còn để tránh pop. 
#  → Bake vào helper, không bao giờ skip."
```

## 🔄 Workflow bắt buộc (added 18/07 theo anh yêu cầu)

```
Stage 3: Render .mp4 với afade filter trong per-segment extract
   ↓
Concat demuxer
   ↓
Stage 5: Verify:
   ├─ Run check_audio_fade.py
   │  ├─ exit 0 = PASS → ship
   │  └─ exit 1 = FAIL → re-render với afade → check lại
   ├─ Run verify_clip.py (5 layers: FILLER/TREO/LẶP/HOOK LẶP)
   └─ Ship to pipeline/output/_shipped/<DATE>/
```

## 🛠️ Tool

**`scripts/check_audio_fade.py`** (7.7 KB) - Phase 1 #3 trong series 9 improvements:

```bash
python3 scripts/check_audio_fade.py <video.mp4>
```

**Output mẫu (50/52 missing fade trên V78):**
```
🎯 PITFALL #32 - AUDIO FADE CHECK
📂 Video: clip0003_V78_82s_FINAL_with_audio.mp4
⚙️  Fade expected: 30ms

📊 Step 2: Detect cut boundaries (silence gaps)...
   Found 52 cut boundaries

📊 Step 3: Check fade at each boundary...

  ✅ Cut #1 at 0.00s (269ms silence): fade-in, NO fade-out
  ✅ Cut #2 at 2.61s (59ms silence): fade-in, NO fade-out
  ❌ Cut #3 at 4.71s (68ms silence): NO fade-in, NO fade-out
  ...
  ❌ Cut #52 at 80.62s (66ms silence): NO fade-in, NO fade-out

❌ FAIL - 50/52 boundaries missing audio fade

🔧 FIX: Apply 30ms fade to each cut boundary in render script:
[0:v]atrim=start=SEG_START,asetpts=PTS-STARTPTS,
    afade=t=in:st=0:d=0.03,
    afade=t=out:st={dur-0.03}:d=0.03[a]
```

## 🔧 Backward fix - clip đã ship

Có thể re-render clip đã SHIP với audio fade enable:
- Dùng `scripts/render_quality_ladder.py` (Phase 2 #5) - auto extract per-segment với afade
- Verify lại bằng `check_audio_fade.py`

**Real case cần fix:**
- `clip0003_V78_82s_FINAL_with_audio.mp4` (50/52 missing)
- Bất kỳ clip nào ship trước 18/07 đều có thể thiếu afade

## 🎓 Lessons vĩnh viễn

1. **30ms audio fade là production correctness** (HARD RULE) - KHÔNG phải taste call
2. **Mọi cut boundary** đều cần fade - KHÔNG skip dù chỉ 1 take
3. **Bake vào render helper** - KHÔNG để LLM tự ý add (vì LLM không tự ý)
4. **Verify sau MỖI render** - KHÔNG batch verify cuối ngày
5. **Workflow bắt buộc = tool + checklist + script** (3-layer enforcement)
   - Tool: `check_audio_fade.py <output>`
   - Checklist: stage 5 add item `audio fade check`
   - Script: tự động exit 0/1 → không bỏ qua được

## 📚 Related

- `tiktok-video-editor` skill v3.35.0 - PITFALL #38 section (đã patch 18/07)
- `tiktok-pipeline-studio` skill - Stage 5 verify (sẽ patch thêm audio fade check)
- `browser-use/video-use` HARD RULE #3 (audio fades)
- Real case: clip V78 (50/52 missing fade → detected by `check_audio_fade.py`)

---

*Created 2026-07-18 - workflow rule mới apply sau khi phát hiện bug audio fade trên shipped clip.*
