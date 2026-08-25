# TTS Providers Comparison for Vietnamese TikTok Content

> Verified 2026-07-22. Cập nhật khi có thay đổi từ Microsoft/CapCut API.

## TL;DR

| Provider | Default? | Giọng VN | Setup | Limit/req | Khi nào dùng |
|---|---|---|---|---|---|
| **Edge TTS (Microsoft)** | ✅ MẶC ĐỊNH | `vi-VN-HoaiMyNeural`, `vi-VN-NamMinhNeural` | `brew install edge-tts` | ~10k safe / ~31k max chars | Demo, teaser, audio mới, voice gốc fail |
| **CapCut TTS API** | ❌ Alternative | Có nhưng chưa document rõ | Clone repo + fake device | Không rõ | Voice CapCut đặc trưng (chấp nhận rủi ro bị block) |
| **Voice gốc từ raw clip** | ✅ MẶC ĐỊNH cho motion graphic | — | Whisper extract audio | Không giới hạn | Build motion graphic từ raw clip |

---

## Edge TTS (Microsoft) — DEFAULT

**Command:**
```bash
edge-tts --voice vi-VN-HoaiMyNeural --text "..." --write-media out.mp3
```

**Character limits (verified 2026-07-22, sources: official README rany2/edge-tts + community wrapper tutorial):**

| Range | Status |
|---|---|
| < 5,000 chars | ✅ An toàn 100% |
| 5,000 - 10,000 chars | ⚠️ Thường OK, thỉnh thoảng network chập chờn |
| 10,000 - 31,000 chars | 🚫 Thường fail hoặc tự cắt |
| > 31,000 chars | 🚫 CHẮC CHẮN fail |

**Quy đổi cho clip TikTok hiện tại:**
- Script 90-120s đọc chậm ≈ 200-300 từ ≈ **1,200-1,800 ký tự** (safe)
- Script 3 version dài nhất anh từng viết ≈ 5,000-7,000 ký tự (vẫn OK)
- → Mọi script TikTok hiện tại của anh **cách giới hạn 10k còn rất xa**, KHÔNG cần lo

**Pros:**
- Sync, 1 lệnh ra MP3 ngay
- Nhiều voice VN: `vi-VN-HoaiMyNeural` (nữ), `vi-VN-NamMinhNeural` (nam)
- Không cần API key, không cần auth, không cần fake device
- Microsoft ổn định lâu dài (Edge browser vẫn dùng TTS này)

**Cons:**
- Giọng nghe "AI" hơn voice gốc TikToker
- Phải convert MP3 → AAC 192k cho video editing pipeline
- Tiếng Việt đôi lúc phát âm sai dấu (ít gặp)

**Khi nào dùng:**
- Demo 5-10s teaser cho script
- Test giọng trước khi record voice gốc
- Edit lại audio cho content khác (dịch thuật, voiceover mới)
- Audio gốc fail / unavailable

---

## CapCut TTS API (K07VN/capcut-tts-api)

**Repo:** https://github.com/K07VN/capcut-tts-api

**Setup:**
```bash
git clone https://github.com/K07VN/capcut-tts-api
cd capcut-tts-api
python3 -m pip install requests
```

**Usage:**
```bash
python3 capcut_common_task_client.py tts-new --text "..." --voice BV074_streaming
python3 capcut_common_task_client.py tts-query --task-id ID --token TOKEN
```

**Pros:**
- Voice CapCut (giọng "TikToker" đặc trưng, kiểu trong app CapCut)
- API internal nên free

**Cons:**
- **Cần fake device profile** (`device_id`, `iid`, `tdid`, `appvr`, `version_name`, `lan=vi-VN`, `loc=VN`, `region=VN`) → rủi ro bị CapCut block bất cứ lúc nào
- **Async workflow**: tạo task → poll → query (2 bước), không sync như Edge TTS
- **Voice VN chưa document rõ**: README chỉ show voice EN `BV074_streaming`. Phải tự sniff từ CapCut app để tìm voice VN
- **CapCut có thể đổi API internal** → script die bất cứ lúc nào (CapCut update app = API change)
- **TOS vi phạm**: gọi internal API bằng fake device = reverse-engineering có thể vi phạm Terms of Service CapCut
- AWS SigV4 + RSA signature phức tạp → debug khó khi fail

**Khi nào dùng:**
- Anh muốn voice CapCut cụ thể (giọng "đầu lạnh", "ấm" kiểu TikToker) mà Edge TTS không có
- Anh chấp nhận rủi ro bị CapCut block + phải tự maintain khi API đổi
- **KHÔNG dùng** cho production pipeline chính (rủi ro cao)

---

## Decision Tree: Chọn provider nào?

```
Cần audio cho clip TikTok?
  ├─ Build motion graphic từ RAW clip có voice gốc?
  │   └─ ✅ DÙNG VOICE GỐC (extract audio từ source.mp4)
  │       → stretch bằng atempo nếu cần
  │       → xem memory [19/07 USE-ORIGINAL-VOICE-CLIP-EDIT]
  │
  ├─ Demo / teaser ngắn 5-10s cho script?
  │   └─ ✅ Edge TTS (sync, nhanh, đủ dùng)
  │
  ├─ Edit lại audio (dịch thuật, voiceover mới)?
  │   └─ ✅ Edge TTS (giọng rõ, ổn định)
  │
  ├─ Audio gốc fail / unavailable?
  │   └─ ✅ Edge TTS (fallback)
  │
  └─ Cần voice CapCut đặc trưng (giọng "TikToker" trong app CapCut)?
      └─ ⚠️ CapCut TTS API (chấp nhận rủi ro bị block)
          → Verify giọng VN có thật trong app CapCut trước
          → Backup bằng Edge TTS phòng khi CapCut API die
```

---

## Rule vĩnh viễn

**LUÔN dùng voice gốc khi build motion graphic từ raw clip** — extract audio từ source.mp4, stretch bằng atempo filter nếu cần. Edge TTS chỉ dùng cho:
1. Demo / teaser ngắn
2. Edit lại audio cho content khác (dịch thuật, voiceover mới)
3. Audio gốc fail / unavailable

**Voice gốc = authenticity cho TikTok.** Khán giả quen voice TikToker của anh hơn voice AI.

→ Cross-reference: memory `[19/07 USE-ORIGINAL-VOICE-CLIP-EDIT]` trong learned-about-tuananh.

---

## Update Checklist

Khi update file này:
- [ ] Verify Edge TTS limits (test với text 5000, 10000, 15000 chars)
- [ ] Check CapCut TTS API repo có còn active không (commit cuối + stars)
- [ ] Test voice VN mới của Edge TTS nếu Microsoft release (xem `edge-tts --list-voices`)
- [ ] Verify CapCut voice list có voice VN không (sniff từ CapCut app hoặc community wiki)

Last verified: 2026-07-22 (sources: github.com/rany2/edge-tts README + dev.to wrapper tutorial + Microsoft Azure quotas docs)
