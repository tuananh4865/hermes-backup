# PITFALL #90 — NO FADE IN/OUT between segments (HARD CUT mandatory)

**Date:** 2026-07-26
**Discovered:** Batch re-render of 7 clips (0095, 0094, 0093, 0091, 0088, 0086, 0085) — `V1 → V2` to remove fade
**Tuấn Anh feedback (verbatim 26/07):** "Anh thấy có fade in fade out hình ảnh khi chuyển từ cảnh này sang cảnh khác! Em bỏ cái đó đi"

---

## 🔴 ROOT CAUSE — why fade was added in v0.01.1/v0.03 (and why it's WRONG now)

### Lịch sử

| Version | Date | Behavior |
|---|---|---|
| v0.01.1 / v0.03 | 23/07 | Dùng `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03` mỗi segment (PITFALL #81 fix) |
| v0.04 | **26/07** | **REMOVE fade** — anh không thích fade visually |

### Tại sao fade được add vào v0.01.1

`Concat demuxer` (`ffmpeg -f concat -safe 0`) stream-copy audio → audio cắt hard tại segment boundary. Nghe có cảm giác "speech ends too sharp, image changes instantly" + "hình đi trước tiếng". Fix bằng afade 30ms. (PITFALL #81, đã verify trên clip 0036.)

### Tại sao fade bị REMOVE ở v0.04

Anh không thích visual fade in/out. Anh muốn **HARD CUT** — chuyển cảnh TikTok style, không mềm mại.

→ Tradeoff: HARD CUT giữ nguyên semantics audio (concat trong filter_complex KHÔNG cần afade vì concat bằng `concat=n=N:v=1:a=1` filter, không phải demuxer stream-copy). Audio không bị "pop" vì concat filter smooth hơn demuxer.

---

## ✅ CORRECT FILTER (HARD CUT)

```python
# Mỗi segment CHỈ có scale+crop+setpts+aresample+asetpts, KHÔNG fade
v = f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[v{i}]"
a = f"[{i}:a]aresample=44100,asetpts=PTS-STARTPTS[a{i}]"
# concat filter cuối cùng
v_concat = "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[outv]"
a_concat = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[outa]"
```

**Verify 7/7 clip (26/07):** 0095 LENSPEN 81s · 0094 OP_FLIP 49s · 0093/0091/0085 BODY_MIST 104/101/138s · 0088 OP_FULL 74s · 0086 LENSPEN 98s — tất cả transcript clean, TikTok spec PASS, audio không pop.

---

## ⚠️ WHISPER RE-SEGMENTATION NOISE (NEW sub-pitfall)

### Symptom

Source liền mạch bị Whisper split thành 2 segments tách rời → recheck phát hiện "lặp liền kề" dù source thật không lặp.

### Case 26/07 clip_0088

**Source thật** (1 câu liền mạch):
> "...không cần phải bỏ vô trong cái túi nhỏ của pocket 3 nữa mà mình có thể bỏ vô bất cứ cái túi nào mà mình muốn..."

**Whisper re-transcript (V2 no-fade):**
```
[11] [23.32→26.52] Không cần phải bỏ vô trong cái túi nhỏ của pocket 3 nữa
[12] [26.94→29.06] Mà mình có thể bỏ vô bất cứ cái túi nào       ← lặp "cái túi nào"
[13] [29.06→36.42] cái túi nào mà mình muốn mình như cá nhân mình...
```

→ Recheck scan báo "Lặp liền kề: 'cái túi nào'" ở 29.06→29.06. Nhưng source không lặp — chỉ là Whisper tách phrase "bỏ vô bất cứ cái túi nào mà mình muốn" thành 2 segs.

### Fix: merge range trong keep_plan

```python
# TRƯỚC (bị lặp giả):
{"name": "USE_CASE", "start": 32.46, "end": 60.48, ...}

# SAU (merge INTERIOR + USE_CASE thành 1 chunk):
{"name": "INTERIOR_USE", "start": 23.04, "end": 60.48, ...}
```

Khi Whisper thấy 1 audio segment liền mạch 37s, không split → 1 segment duy nhất "mà mình có thể bỏ vô bất cứ cái túi nào mà mình muốn" → no lặp.

### Cách phân biệt Whisper re-segment vs lặp thật

| Pattern | Whisper re-segment | Lặp thật |
|---|---|---|
| Source phrase | 1 câu liền mạch có repetition (e.g. "X nào ... X nào") | 2 câu khác nhau, cùng keyword |
| Whisper output | 2-3 segs liền kề, 1 segs rất ngắn (0.5-2s) | 2 segs có gap >0.5s |
| Audio waveform | continuous | có pause ở giữa |
| Test | merge range → re-transcript lần 2 → no lặp | vẫn lặp dù merge |

→ Rule of thumb: nếu Whisper re-transcript lần đầu báo lặp giữa 2 segs mà source `transcript_full.md` KHÔNG có lặp → Whisper re-segment, merge range.

---

## 🔄 Migration recipe (V1 → V2 no-fade)

```bash
# 1. Update keep_plan.json nếu có lặp giả
# 2. Run build script
python3 /tmp/build_clip_no_fade.py <clip_id>

# 3. Re-transcript + scan false_start + lặp
ffmpeg -y -i final.mp4 -ar 16000 -ac 1 -c:a pcm_s16le -vn recheck_audio.wav
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format json --word-timestamps True \
  --condition-on-previous-text False --output-dir . recheck_audio.wav

# 4. Scan
python3 scan_lap_lien_ke.py recheck_audio.json

# 5. Ship V2 (overwrite V1)
shutil.copy('final.mp4', f'/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V2_NNs_FINAL_<sp>.mp4')
os.remove(f'/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V1_*.mp4')
```

**Time per clip:** ~3-5 phút (build 90s + re-transcript 60s + scan 5s + ship 5s).

---

## 📋 Action items for next session

1. **Khi edit clip mới:** dùng build_clip_no_fade.py từ đầu, KHÔNG dùng build_pre_speed.sh v0.03 cũ (có afade).
2. **Khi recheck phát hiện lặp:** check source `transcript_full.md` — nếu source không lặp → Whisper re-segment, merge range.
3. **Khi user feedback mới về visual:** patch HARD RULE block trong SKILL.md ngay (không đợi).

---

## References

- PITFALL #81 (afade 30ms) — DEPRECATED v0.04
- PITFALL #86 (audio-visual desync) — DEPRECATED v0.04 (concat filter KHÔNG cần afade)
- HARD RULE v0.04 (NO FADE) — SKILL.md § "HARD RULE v0.04 — NO FADE IN/OUT"
- Build script: `scripts/build_clip_no_fade.py` (skill template)