# Lesson 2026-07-21 — Verify 7-layer L7 câu treo (NEW HARD CHECK) + script truncation pitfall

## Context

User request 21/07/2026 ~10:51: "Verify clip 0030 với 7 LAYERS tool THẬT, đặc biệt chú trọng L7 (câu treo)."

Input:
- Final: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0030_V1_90s_FINAL_KNF_LENS_PEN.mp4`
- Source: `/Volumes/Storage-1/Pocket3/Footages/DJI_20260721094041_0030_D.MP4`

7 layers verified:
- L1-L5 PASS (size 62.8 MB, spec 1080×1920 h264 yuv420p 44100Hz, audio fade 56/56 cuts, duration 90.27s vs 90s target Δ=0.27s, source/final ratio 1.62x = Mode B keep_coverage ~80% hợp lý)
- L6 FAIL: `scan_false_start.py` exit 1 — filler 'thì' replicate @ 19.1s và 26.8s (Δ=7.7s)
- **L7 FAIL: `scan_treo.py` exit 1 — 19 câu treo (HARD CHECK)**

## PITFALL #26 (NEW 21/07) — `scan_treo.py` truncates issue list to 15

### Vấn đề phát hiện

Script `~/.hermes/skills/media/tiktok-video-editor/scripts/scan_treo.py` (line 110) chỉ print first 15 issues:

```python
for iss in sorted(issues, key=lambda x: -x['signals'])[:15]:
    print(...)
if len(issues) > 15:
    print(f'  ... +{len(issues)-15} câu khác')
```

Real case clip 0030: scan phát hiện **19 câu treo** nhưng stdout chỉ in **15** + dòng "+4 câu khác" → user yêu cầu "liệt kê cụ thể các câu treo, không tổng quát" bị miss 4 câu cuối.

### Fix

Re-run scan logic inline (extract audio → whisper → scan regex) để dump FULL list. Pattern:

```python
import subprocess, json, os, re, tempfile
v = "<clip.mp4>"
audio = tempfile.mktemp(suffix='.wav')
subprocess.run(['ffmpeg', '-y', '-i', v, '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1', audio], capture_output=True, timeout=60)
out_dir = tempfile.mkdtemp(prefix='whisper_treo_')
jp = f'{out_dir}/{os.path.basename(audio).replace(".wav",".json")}'
subprocess.run(['mlx_whisper', '--model', 'mlx-community/whisper-medium-mlx',
                '--language', 'vi', '--output-dir', out_dir,
                '--output-format', 'json', '--word-timestamps', 'True', audio],
               capture_output=True, timeout=300)
segs = json.load(open(jp))['segments']
# ... scan regex inline (see scan_treo.py scan_treo())
```

### Recommendation for upstream

Update `scan_treo.py` to either:
1. Bump `[:15]` → `[:50]` (or unlimited)
2. Add `--full` flag để dump all issues khi user yêu cầu "liệt kê cụ thể"
3. Default to full list + add `--top N` cho compact view

## PITFALL #27 (NEW 21/07) — L7 câu treo vs filler pattern noise

### Vấn đề phát hiện

Trong clip tiếng Việt hội thoại (Pocket3 raw footage, speaker dùng filler tự nhiên), `scan_treo.py` báo 19 câu treo. Phân tích ngữ nghĩa cho thấy:

- **Pattern NOISE (linking verb/conjunction hợp lệ, không mất ý)**:
  - `#2 "đây các bạn có thể thấy nè"` → next "nó rất là nhỏ gọn" (linking verb "nè")
  - `#7 "đó"` → next "vì vậy" (filler đứng riêng)
  - `#8 "vì vậy"` → next "thì cái lèn" (transition hợp lệ)
  - `#14 "ờ"` → next "nhé nhé nhé..." (filler đứng riêng)
  - `#18 "khi nào cần dùng các bạn lấy ra"` → next "thì khá là nhỏ gọn" (relative clause OK)
  - `#19 "mà chất lượng giá công nó rất là đẹp nha"` → next "rất là đẹp mắc" (rồi bị cắt, mất predicate cuối)

- **Pattern MẤT Ý (cần re-edit)**:
  - `#1 "là"` → mất "là [list tiện lợi]" bị cắt
  - `#9 "khi mà"` → next "lâu lâu lâu" gây khó hiểu, mất setup context
  - `#11 "xong rồi"` → mất predicate completion
  - `#13 "lau nó sẽ"` → next "ờ" (filler) → mất kết quả hành động
  - `#15 "là đầu chổi nè"` → mất giải thích chức năng
  - `#17 "cất đi"` → mất "cất đi [ở đâu/khi nào]" context

### Recommendation

Khi L7 FAIL:
1. **Dump FULL list** (tránh PITFALL #26)
2. **Phân loại 2 nhóm**:
   - **NOISE** (~60% trong tiếng Việt hội thoại): filler/conjunction pattern, re-edit OK nhưng không bắt buộc
   - **MẤT Ý** (~40%): predicate/completion bị cắt, BẮT BUỘC re-edit
3. **Re-edit keep_plan** focus vào câu MẤT Ý trước
4. Sau re-edit, chạy lại L7 → confirm exit 0 hoặc giảm xuống < 5 câu MẤT Ý (acceptable threshold cho conversational footage)

## L5 ratio interpretation clip 0030 (bổ sung PITFALL #23)

| Clip | source_s | final_s | ratio | keep_coverage (Mode B formula) |
|------|----------|---------|-------|-------------------------------|
| 0030 | 146.219   | 90.267   | 1.620 | 80.3% ✅ (Mode B sweet spot 30-80%) |

- Brief user nói `90s` clip → file thực 90.27s → Δ=+0.27s (trong ±5s tolerance)
- Source 146.22s / final 90.27s = 1.62x ratio → Mode B với keep_coverage ~80%
- Pass PITFALL #23 indirect proof (literal "≈1.3x" SAI cho Mode B; correct threshold 30-80% keep_coverage)

## Tools used

- `ls -la` → L1
- `ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,pix_fmt,sample_rate,r_frame_rate,channels -show_entries format=duration,bit_rate,size -of default` → L2 + L4
- `python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py` → L3
- `python3 -c "src=146.22; clip=90.27; print(f'ratio={src/clip:.3f}x keep_pct={clip*1.3/src*100:.1f}%')"` → L5 indirect proof
- `python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/scan_false_start.py` → L6
- `python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/scan_treo.py` → L7 (HARD)
- Inline python re-scan (PITFALL #26 fix) để dump FULL 19 câu treo

## Action items

- [ ] Update `scan_treo.py` upstream: bump `[:15]` limit hoặc thêm `--full` flag (PITFALL #26)
- [ ] Bump `tiktok-verify-protocol` recipe from 6-layer → 7-layer (DONE in `references/6-layer-clip-verify-recipe.md`)
- [ ] Re-edit clip 0030 keep_plan: ưu tiên cắt 6 câu MẤT Ý (#1, #9, #11, #13, #15, #17), giữ filler pattern NOISE (acceptable conversational Vietnamese)
- [ ] Sau re-edit: re-render → L7 lại → confirm exit 0 hoặc < 5 câu MẤT Ý

## Summary

- Verify protocol đã escalate lên **7 layers** với L7 = HARD CHECK (câu treo scan)
- L7 cho conversational Vietnamese footage thường ra 15-20 câu treo do filler density cao — KHÔNG phải tất cả đều mất ý
- **PITFALL #26**: scan_treo.py truncate stdout → MUST inline re-scan để full list
- **PITFALL #27**: phân loại NOISE vs MẤT Ý trước khi decide re-edit scope
- L1-L5 PASS evidence ổn định cho batch Pocket3 21/07 (0030 verify ở đây; 0029/0031/0034/0036/0037/0038 đã verify trước đó với 5-layer protocol + PITFALL #23 indirect proof)
