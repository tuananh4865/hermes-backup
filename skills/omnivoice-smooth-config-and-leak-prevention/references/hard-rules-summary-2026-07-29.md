---
title: Hard Rules 29/07 — Tóm tắt cho future sessions
created: 2026-07-29
updated: 2026-07-29
type: reference
tags: [omnivoice, hard-rule, vĩnh-viễn, filler, youtube]
relationships: [pitfall-20, pitfall-21, pitfall-23]
---

# Hard Rules 29/07 — Tóm tắt cho future sessions

**Why this file exists:** Session 29/07 đã settle được 5 hard rules quan trọng cho OmniVoice YouTube narration. Skill chính đã có pitfalls #19-#24 ở body, nhưng file này tóm tắt TL;DR ở ngay đầu.

---

## 🚨 5 Hard Rules (FIRST-CLASS, vĩnh viễn, 29/07)

### 1. ZERO emotion tag mặc định (Pitfall #21)

```python
# ❌ SAI
{"id": "001", "text": "[question-ah] Hố đen có lẽ là vật thể...", "language": "vi"}

# ✅ ĐÚNG
{"id": "001", "text": "Hố đen có lẽ là vật thể...", "language": "vi"}
```

**Why:** `[question-ah]`, `[confirmation-en]`, `[confirmation-yi]` đều prepend vocalization "ờ/ựm/ừm" đầu câu. Whisper hallucinate hoặc bỏ sót → user nghe "ờ" mà transcript sạch.

**Override:** chỉ dùng khi user EXPLICITLY yêu cầu emotion + A/B test an toàn.

### 2. YouTube voice = native speed, NO atempo (Pitfall #20)

```python
# ❌ SAI — YouTube narration
ffmpeg ... -af "atempo=1.2" ...   # → voice 20 phút thành 16.7 phút, bể pitch

# ✅ ĐÚNG
ffmpeg ... -c:a libmp3lame ...    # native speed, ship ngay
```

**Why:** YouTube/podcast/audiobook = narration → giữ tốc độ model output.

**Exception:** TikTok Shop Mode B 75–110s clip → atempo=1.3x via `tiktok-video-editor` skill, KHÔNG phải OmniVoice workflow.

### 3. 1 call > merge chunks cho long narration (Pitfall #23, supersedes #22)

```python
# ❌ SAI — Plan C: 17 chunks mỗi 25s, model drop âm đầu/cuối mỗi chunk
chunks = [" ".join(items[i:i+5]) + " … " for i in range(0, len(items), 5)]
for chunk in chunks: generate(chunk)

# ✅ ĐÚNG — Plan A: 1 call full 3 032 từ
full = " ".join(text.strip() for text in paragraphs)
audio = model.generate(text=full, ...)
sf.write("full.wav", audio, model.sampling_rate)
```

**Why:** OmniVoice 0.2.1 có internal warm-up/cool-down. Plan C vẫn mất âm đầu/cuối mỗi chunk. Plan A (1 call) cho clean voice 12:24 phút.

**When to use Plan C (fallback):** model OOM, hoặc user muốn QA từng chapter. KHÔNG dùng chunks < 25s.

### 4. Padding silence ≠ head/tail fix (Pitfall #22)

```python
# ❌ SAI — pad silence NGOÀI file WAV không recover âm đã drop TRONG model
silence = generate_silence(0.4)  # 400ms
concat([silence, voice, silence])

# ✅ ĐÚNG — sửa từ source (chunk lớn hơn hoặc 1 call)
```

**Why:** Model trả về audio tensor đã cắt 100-400ms đầu/cuối. Silence pad bên ngoài không tạo lại âm đã lost IN the model.

### 5. `import os` + non-zero exit guard trong wrapper (Pitfall #19)

```python
# Sửa trong generate_voice.py:
code = '''
import sys, json, time, torch, os   # ← thêm os
...
'''
result = subprocess.run([python, "-c", code], capture_output=False)
if result.returncode != 0:
    raise SystemExit(result.returncode)  # ← surface lỗi
```

**Why:** Nếu `os` không import trong heredoc → NameError ở `print(f"✅ Saved {os.path.getsize(...)}")`. Không raise → wrapper exits 0 nhưng file WAV không được tạo đúng.

**Smoke test trước khi batch:**

```bash
python3 scripts/generate_voice.py --prompt <pt> --text "Test" --output smoke.wav
python3 scripts/verify_audio.py smoke.wav --whisper
# Expect: codec=pcm_s16le, volumedetect max > -10 dB, Whisper OK
```

---

## Quick config picker

| Use case | Config | Reference |
|---|---|---|
| **YouTube long-form 15-25 phút (CHỐT 29/07)** | `pad=0.15, fade=0.02, denoise=True, layer=2.0, pos=2.5, speed=0.90` + 1 call full 3 032 từ | `references/youtube-long-narration-final-config-2026-07-29.md` |
| YouTube long-form 15-25 phút (cũ) | `pad=0.1, fade=0, denoise=True, layer=1.5, pos=3.5, speed=0.90` + 1 call full | `references/youtube-long-narration-config-grid-2026-07-29.md` |
| TikTok Shop clip 75-110s | `pad=0, fade=0, denoise=True, layer=1.0, pos=3.0, speed=0.95` + 5-segment loop + atempo=1.3x ở stage 2 | `omnivoice-voice-clone` skill recipes |
| Audiobook / podcast | YouTube config trên + 1 call full | same as YouTube |

---

## Phrases to look for in user feedback (FIRST-CLASS signals)

| User nói | Em phải làm |
|---|---|
| "ờ/ựm/à/ồ" trong voice | Strip tất cả emotion tag (Pitfall #21) |
| "giọng hơi nhanh" | Giảm `speed` 0.05 (e.g. 0.95 → 0.90) |
| "câu đầu bị cắt / khuyết" | Dùng Plan A (1 call) thay vì merge chunks |
| "fade in/out voice" | Từ chối — voice NO fade, audio gốc mới fade (Pitfall #18 trong skill) |
| "đừng tăng speed YouTube" | Bỏ atempo, ship native speed (Pitfall #20) |
| "voice nghe flat / không hào hứng" | Tăng `position_temperature` thay vì thêm emotion tag (Pitfall #21) |
| "dùng mặc định" cho YouTube | Dùng config verified trong file grid |
| "hú lên từ ư a à" | Root cause = tag emotion prepend vocalization, KHÔNG phải lỗi prompt |
| "test với config X" | 3-segment test trước (segments 001, 027, 080), wait verdict, rồi full render |
| "Pad 0.X" / "fade 0.X" | Chỉnh pad/fade tham số trong OmniVoiceGenerationConfig |
| "Layer Y" / "Position Z" | Layer/position tham số, A/B test 3 câu |

---

## Related files

- SKILL.md (skill này) — full body với Pitfall #6 → #24
- references/youtube-long-narration-final-config-2026-07-29.md — A/B matrix chi tiết + verified config L2P2.5P0.15F0.02
- references/youtube-long-narration-config-grid-2026-07-29.md — A/B matrix cũ 9 variant
- references/session-2026-07-24-findings.md — original 24/07 findings
