# CASE STUDY: clip_0004 — Phát hiện audio ≠ visual (file bị ghép nhầm)

> **Date**: 2026-07-19
> **Anh xác nhận**: "Em lấy sai âm thanh rồi clip một đăng âm thanh một nẻo!!!"
> **Lesson vĩnh viễn**: Khi build motion từ raw clip, **VERIFY audio + visual + wiki** trước khi ship.

---

## 🚨 VẤN ĐỀ

File `clip_0004_V3_85s_FINAL_DJI_source.mp4` đã bị ghép nhầm **audio từ clip khác** (nói về máy hút bụi Dodoto) + **visual là máy sấy tóc otobob** (logo rõ trên thân máy).

Em build sai 3 lần:
- V19 (Dodoto Luxe V3) — em đoán theo Whisper, SAI
- V20 (ULANZI MA66) — em đoán lung, SAI audio
- V21 (ULANZI MA66 + voice gốc) — đúng sản phẩm nhưng audio vẫn nói Doroto

## 🔍 CÁCH PHÁT HIỆN

### 3 nguồn disagree khi em verify bằng 3 cách độc lập:

| Nguồn | Sản phẩm | Cách check | Bằng chứng |
|---|---|---|---|
| **Whisper audio** (40 segments) | "Dodoto Luxe V3" (máy hút bụi) | `mlx_whisper --language vi --output-format json` | `/tmp/clip_0004_DJI_RAW/` |
| **Visual RAW frame t=80s** | **"otobob"** máy sấy tóc | `ffmpeg -ss 80 -i raw -frames:v 1 + vision_analyze` | `/tmp/clip_0004_RAW_frames/raw_t080s.jpg` |
| **Visual RAW frame t=200s** | **"otobob"** close-up logo | `ffmpeg -ss 200 -i raw -frames:v 1 + vision_analyze` | `/tmp/clip_0004_RAW_frames/raw_t200s.jpg` |

→ **Khi 3 nguồn disagree → DỪNG LẠI, HỎI ANH** (đã capture trong PITFALL #46)

## 📁 FILE SOURCE TÌM ĐƯỢC

| File | Path | Size | Duration |
|---|---|---:|---:|
| **SOURCE GỐC DJI RAW** | `/Volumes/Storage-1/Pocket3/Footages/DJI_20260716115435_0004_D.MP4` | 1,056 MB | **222.8s** (RAW) |
| **Final đã edit 85s** | `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V3_85s_FINAL_DJI_source.mp4` | 71 MB | 85.8s |
| **Pipeline copy** | `/Volumes/Storage-1/Pocket3/Hermes-Edit/pipeline/output/_shipped/2026-07-19/clip_0004_V3_85s_FINAL_DJI_source.mp4` | 71 MB | 85.8s |

**Verify** với MD5:
```bash
md5 /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V3_85s_FINAL_DJI_source.mp4
# 13003dc53a23031eceb6e064bc2f5018
md5 /Volumes/Storage-1/Pocket3/Hermes-Edit/pipeline/output/_shipped/2026-07-19/clip_0004_V3_85s_FINAL_DJI_source.mp4
# 13003dc53a23031eceb6e064bc2f5018 → IDENTICAL
```

## 🛠️ WORKFLOW KHI PHÁT HIỆN AUDIO ≠ VISUAL

```bash
# 1. Extract voice gốc từ source (visual = ground truth)
ffmpeg -y -i /path/to/source.mp4 -vn -c:a aac -b:a 192k -ar 44100 audio_visual_goc.aac

# 2. Visual verify bằng mắt (10+ frames)
for t in 0 10 20 30 40 50 60 70 80 90; do
  ffmpeg -y -ss $t -i source.mp4 -frames:v 1 frame_t${t}.jpg
  # → vision_analyze mỗi frame xác nhận sản phẩm
done

# 3. Nếu audio gốc KHÔNG khớp visual → DỪNG, hỏi anh
#    Có thể: (a) audio gốc lẫn clip khác, (b) dùng file RAW DJI khác, (c) bỏ clip
```

## 📚 BÀI HỌC VĨNH VIỄN

1. **VERIFY 3 NGUỒN trước khi build** (WIKI + MẮT + TAI)
2. **MẮT thấy > WHISPER nghe** khi có conflict (anh confirm visual nhiều lần hơn audio)
3. **File có thể bị ghép nhầm audio từ clip khác** — LUÔN kiểm tra visual cue (logo, hình dạng) khớp audio cue
4. **DÙNG VOICE GỐC** (anh explicit dặn) — KHÔNG TTS khi build motion từ raw clip
5. **DỪNG LẠI khi không chắc chắn** — hỏi anh, đừng đoán

## 🔗 RELATED

- `references/case-study-clip_0004-whisper-sai-2026-07-19.md` — Whisper SAI về sản phẩm
- `references/case-study-clip_0004-voice-goc-vs-tts-2026-07-19.md` — Voice gốc vs TTS
- `references/clip-analysis-protocol-19-07-2026.md` — 6 bước HARD RULE (mắt + tai + wiki)
- `SKILL.md` PITFALL #46 (Whisper SAI), #47 (Audio TTS), #48 (atempo), #49 (DỪNG khi anh không respond), #50 (file bị ghép nhầm audio)
