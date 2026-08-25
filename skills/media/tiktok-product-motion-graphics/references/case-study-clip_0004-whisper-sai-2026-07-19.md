# CASE STUDY: clip_0004 — Whisper SAI về sản phẩm (19/07/2026)

> **Bài học lớn nhất session này:** Whisper có thể SAI về **CẢ SẢN PHẨM**, không chỉ sai brand name.
> Khi 3 nguồn disagree (Whisper + Visual + Wiki) → **DỪNG LẠI verify với anh**.

---

## 📋 Source

- **File**: `clip_0004_V3_85s_FINAL_DJI_source.mp4` (71.2 MB, 85.9s, 1080×1920)
- **Wiki đúng**: `wiki/projects/tuan-anh-review-tiktok/products/ulanzi-ma66-tripod-pocket-3.md`
- **Plan motion**: `wiki/queries/clip_0004-motion-plan-2026-07-19.md` (7,311 B)
- **Final ship**: `clip_0004_V20_85s_FINAL_ULANZI_MA66.mp4` (45.8 MB, 85s)

## 🔍 3 NGUỒN DISAGREE

| Nguồn | Output | Đúng? |
|---|---|---|
| **WIKI** (ULANZI MA66) | "Magnetic Quick Release Tripod for DJI Osmo Pocket 3/4" | ✅ ĐÚNG |
| **MẮT** (9 frames extracted) | Mặt anh cầm ULANZI MA66 tripod (logo trên thân) | ✅ ĐÚNG |
| **TAI** (Whisper mlx) | "máy hút bụi Doroto E Luxe V3" | ❌ **SAI hoàn toàn** |

## 🐛 Whisper SAI Ở ĐÂU

| Whisper nghe | Thực tế | Mức sai |
|---|---|---|
| "máy hút bụi" | tấm tháo lắp nhanh | **Sai cả sản phẩm** |
| "Doroto" | "Dodoto" hoặc "ULANZI" | Sai brand name |
| "25.000 bát canh" | "25.000 Pa" | Sai đơn vị + sai spec |
| "4000 mAh" | (có thể đúng nếu clip thật về máy hút bụi) | Có thể đúng |

## ❌ EM SAI (V19)

```bash
# V19 = Dodoto Lux Air V3 (theo Whisper)
- HOOK: "HÚT BỤI MINI - 25.000 PA"
- CHART: 25K / 17K / 13K Pa (Dodoto vs Deerma vs Shunzao)
- CTA: 495.000đ (giá Dodoto)
- PIP work, motion work, verify visually PASS
# NHƯNG SẢN PHẨM SAI → anh flag "anh nhầm"
```

## ✅ V20 (ĐÚNG - ULANZI MA66)

```bash
# V20 = ULANZI MA66 Magnetic Tripod (theo Wiki + Visual)
- HOOK: "Thay lens 1 giây không cần vặn" + "75g nhẹ như không"
- CHART: MA66 1s / Vặn 15s / Adapter 25s
- CTA: 599.000đ (giá ULANZI MA66)
- Audio TTS mới (vi-VN-HoaiMyNeural) — KHÔNG dùng audio cũ (Whisper sai)
```

## 🔄 WORKFLOW REBUILD (khi audio transcript sai)

```
1. ⚠️ Phát hiện audio transcript sai (Whisper nói SP khác wiki/visual)
2. 🗑️ Xóa version sai (V19) + cleanup Hermes-Edit
3. 🔍 Re-check wiki (Key #1) cho sản phẩm ĐÚNG
4. 📝 Viết script mới (94-180 words) dựa trên wiki specs
5. 🎤 Tạo audio mới bằng Edge TTS (vi-VN-HoaiMyNeural, rate="-10%")
6. 🔄 Stretch audio bằng atempo filter để fit video duration
7. 🚢 Ship version mới (V20) với audio mới
8. ✅ Verify visually (PNG extract + vision_analyze) từng phase
```

## 🎤 EDGE TTS RECIPE (vĩnh viễn)

```python
import asyncio
import edge_tts

script = """Anh em đang quay video bằng máy ảnh hoặc Pocket 3 mà cứ phải vặn ốc tháo lens mỗi lần mệt nha?
Hôm nay em giới thiệu tấm tháo lắp nhanh ULANZI MA66, dùng nam châm hít tự động.
Chỉ cần một giây, lens tự khớp vào. Nặng có 75 gam, nhẹ hơn cả thỏi son.
Bốn chế độ trong một: tripod, selfie stick, tay cầm, và móc treo.
Tương thích với DJI Osmo Pocket 3, Pocket 4, và nhiều máy ảnh khác.
Anh em quan tâm thì bấm vào link phía dưới nhé."""

async def gen():
    communicate = edge_tts.Communicate(script, "vi-VN-HoaiMyNeural", rate="-10%")
    await communicate.save("audio_tts.mp3")
asyncio.run(gen())
```

## 🔄 ATEMPO STRETCH RECIPE

```bash
# Khi audio TTS ngắn hơn video (61s audio vs 85s video)
ffmpeg -y -i audio_v2.aac -filter:a "atempo=0.719" -c:a aac -b:a 128k audio.aac

# Verify sau khi stretch
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 audio.aac
# Output: duration=85.000000
```

## 📊 VISUAL VERIFY V20

| Phase | t | Mặt anh | Glass card | Bars | PIP |
|---|---:|---|---|---|---|
| HOOK | 5s | ✅ Rõ | "Thay lens 1 giây" | - | - |
| CHART (PIP) | 10s | ✅ Rõ | "⏱️ Thời gian thay lens" | MA66 1s xanh / Vặn 15s cam / Adapter 25s cam | Top-left ✅ |
| PRODUCT | 15s | ✅ Rõ | "ULANZI MA66" | - | - |
| PORT (PIP) | 22s | ✅ Rõ | "🔄 3 bước thay lens nhanh" | - | Top-right ✅ |
| USP | 30s | ✅ Rõ | 4 specs grid (75g/Magnetic/4-in-1/Pocket 3/4) | - | - |
| TESTIMONIAL | 40s | ✅ Rõ | "⭐⭐⭐⭐⭐ Thay lens nhanh thật" | - | - |
| FEATURE | 55s | ✅ Rõ | countUp 0 → 1 giây | - | - |
| USECASE | 70s | ✅ Rõ | 📸Chụp ảnh / 🎬Quay vlog / ✈️Du lịch | - | - |
| CTA | 83s | ✅ Rõ | "ULANZI MA66 Magnetic Tripod" 599K + 4 specs | - | - |

## 📁 FILES

| File | Path |
|---|---|
| Source | `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V3_85s_FINAL_DJI_source.mp4` |
| Wiki | `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/ulanzi-ma66-tripod-pocket-3.md` |
| Plan | `/Volumes/Storage-1/Hermes/wiki/queries/clip_0004-motion-plan-2026-07-19.md` |
| Ship | `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V20_85s_FINAL_ULANZI_MA66.mp4` |
| Samples | `/Volumes/Storage-1/Hermes/scratch/v20_samples/` (9 PNG) |
| Audio TTS | `/Volumes/Storage-1/Hermes/scratch/hf_clip0004_V20/audio_tts_v2.mp3` |

## 🎯 BÀI HỌC VĨNH VIỄN

1. **WIKI = ground truth** (đã có citation [N])
2. **VISUAL = mắt thấy** (anh confirm)
3. **WHISPER = chỉ tham khảo audio cues** (keyword, tone, timing) — KHÔNG TIN SẢN PHẨM
4. **3 nguồn disagree** → DỪNG LẠI, HỎI ANH, KHÔNG ARGUE
5. **Audio sai** → Tạo audio mới bằng Edge TTS (KHÔNG dùng audio gốc)
6. **Khi anh flag "nhầm"** → STOP, REBUILD từ đầu, KHÔNG argue
7. **Atempo stretch** để fit audio TTS vào video duration

## 📝 ANH'S VERBATIM (19/07/2026)

> *"Anh nhầm sản phẩm rồi video này nói về tấm tháo lắp nhanh cho máy ảnh và pocket 3 làm lại giúp anh nhé!"*

→ Khi anh flag nhầm → STOP, REBUILD từ đầu, KHÔNG argue.
