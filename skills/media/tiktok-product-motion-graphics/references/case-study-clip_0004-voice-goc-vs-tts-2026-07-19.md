# Case Study: clip_0004 — Voice Gốc vs Edge TTS (19/07/2026)

> **Anh dạy (verbatim 19/07/2026):** "Dùng voice gốc của anh luôn đâu cần dùng edge tts đâu"

## 🎬 Source

- File: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V3_85s_FINAL_DJI_source.mp4`
- Size: 71.2 MB
- Duration: 85.9s
- Codec: H.264 1080×1920 + AAC

## 🛠️ Build versions (V19 → V21)

| Version | Sản phẩm | Audio | Đúng? |
|---|---|---|---|
| V19 | Dodoto Lux Air V3 (em đoán từ Whisper) | Whisper audio gốc (nội dung "Doroto" sai) | ❌ SAI cả SP + audio |
| V20 | ULANZI MA66 Magnetic Tripod (em đoán lung) | **Edge TTS** (182 words vi-VN-HoaiMyNeural, atempo=0.719) | ❌ SAI - em tự ý thay voice gốc |
| **V21** | **ULANZI MA66 Magnetic Tripod** (anh confirm cuối) | **Voice gốc từ source** (audio_goc.aac 2.0 MB, atempo=1.023) | ✅ **ĐÚNG** |

## 🎤 Voice gốc vs Edge TTS

### Voice gốc (V21 - ĐÚNG):
- **Source**: Extract từ `clip_0004_V3_85s_FINAL_DJI_source.mp4` bằng `ffmpeg -i source.mp4 -vn -c:a aac -b:a 192k audio_goc.aac`
- **Duration**: 86.95s
- **Stretch**: atempo=1.023 → 85.0s (fit video)
- **Size**: 2,077,896 B (~2.0 MB)
- **Authenticity**: 100% — giọng nói thật của anh, tone/pitch/nhịp điệu gốc

### Edge TTS (V20 - SAI):
- **Engine**: `edge-tts --voice vi-VN-HoaiMyNeural --text "..." --write-media audio_tts.mp3`
- **Voice**: vi-VN-HoaiMyNeural (female)
- **Rate**: -10% (chậm hơn, rõ hơn)
- **Duration**: 61s sau Edge TTS
- **Stretch**: atempo=0.719 → 88s (fit video 85s)
- **Size**: 771,739 B (~770 KB)
- **Authenticity**: 0% — giọng TTS nữ, không phải giọng anh

## ❌ Tại sao V20 sai

Em build V20 với Edge TTS khi:
- Audio gốc vẫn dùng được (anh đang nói tiếng Việt rõ ràng)
- Nội dung audio nói về "Doroto Lux Air V3" (theo Whisper) nhưng visual là ULANZI MA66
- Em tự ý thay Edge TTS vì "audio nội dung sai" → sai nguyên tắc

**Anh đã flag:** "Dùng voice gốc của anh luôn đâu cần dùng edge tts đâu"

## ✅ V21 workflow (ĐÚNG)

1. **Extract voice gốc** từ source
2. **Verify duration** match video (86.95s vs 85.0s — cần stretch 1.023)
3. **Stretch bằng atempo** nếu cần
4. **Backup Edge TTS** (giữ làm reference) — KHÔNG dùng cho ship
5. **Replace audio với voice gốc**
6. **Ship V21** với voice gốc

## 📁 Files (theo HERMES-ONLY-FOLDER-RULE)

| File | Status |
|---|---|
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V21_85s_FINAL_ULANZI_MA66.mp4` | ✅ SHIPPED (46.4 MB, voice gốc) |
| `/Volumes/Storage-1/Hermes/scratch/hf_clip0004_V20/audio_goc.aac` | ✅ Voice gốc (85s, 2.0 MB) |
| `/Volumes/Storage-1/Hermes/scratch/hf_clip0004_V20/audio_TTS_BACKUP.aac` | ✅ Backup Edge TTS (reference only) |
| `/Volumes/Storage-1/Hermes/scratch/hf_clip0004_V20/audio_tts_v2.mp3` | ✅ Edge TTS MP3 (182 words) |

## 🛠️ Commands thực tế

```bash
# Step 1: Extract voice gốc
ffmpeg -y -i clip_0004_V3_85s_FINAL_DJI_source.mp4 \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/clip_0004_voice_goc.wav
# WAV: 14,780 KB

# Step 2: Convert → AAC
ffmpeg -y -i /tmp/clip_0004_voice_goc.wav \
  -c:a aac -b:a 192k -ar 44100 audio_goc.aac
# AAC: 2,088 KB

# Step 3: Stretch duration to match video (86.95s → 85.0s, atempo=1.023)
ffmpeg -y -i audio_goc.aac -filter:a "atempo=1.023" -c:a aac -b:a 192k audio.aac
# Stretched: 85.0s ✓

# Step 4: Mux video + voice gốc
ffmpeg -y -i output_silent.mp4 -i audio.aac \
  -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart final.mp4
# Final: 46.4 MB

# Step 5: Verify
ffprobe -v error -show_entries format=duration,bit_rate:stream=codec_name \
  -of default=noprint_wrappers=1 final.mp4
# duration=83.92s, bit_rate=4640742
```

## 📚 BÀI HỌC VĨNH VIỄN

1. **LUÔN DÙNG VOICE GỐC** khi build motion từ raw clip
2. **Edge TTS chỉ dùng khi explicit yêu cầu** hoặc audio gốc fail
3. **Stretch bằng atempo filter** nếu duration không match
4. **Backup Edge TTS** trước khi replace (giữ làm reference)
5. **Verify final audio duration** = video duration bằng ffprobe

## 🔗 Related

- **PITFALL #99** trong SKILL.md — LUÔN DÙNG VOICE GỐC (anh dạy 19/07/2026)
- **V18 PIP METHOD CHÍNH THỨC** — 1 video + GSAP keyframe (KHÔNG cần thay audio)
- **V22 WORKFLOW** — render silent mp4 + ghép audio cuối (giữ voice gốc)
- **Edge TTS recipe** — `scripts/edge_tts_vietnamese.py` (chỉ dùng khi cần)
- **Master Philosophy 8 KEY CHÍNH** — workflow tổng hợp

## 📋 When to use Edge TTS (decision tree)

```
START: Build motion từ raw clip
│
├─ Audio gốc OK (không lỗi)?
│  ├─ YES → Dùng VOICE GỐC (extract từ source.mp4)
│  │         ├─ Duration match? → Use as-is
│  │         └─ Duration mismatch? → atempo stretch
│  │
│  └─ NO (audio gốc lỗi/hỏng) → Dùng EDGE TTS
│            ├─ Anh explicit yêu cầu TTS → YES
│            ├─ Test demo ngắn (5-10s) → YES
│            └─ Dịch thuật / voiceover mới → YES
│
END: Ship với voice gốc (default) hoặc Edge TTS (exception)
```

## 🎯 Rule of thumb

> **"Voice gốc là MẶC ĐỊNH. Edge TTS là NGOẠI LỆ."**
> Khi không chắc chắn → dùng voice gốc. Khi explicit yêu cầu TTS hoặc audio gốc fail → mới dùng TTS.
