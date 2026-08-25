# TikTok/YouTube Link Verify Before Ref Audio (2026-07-23)

**Context:** User gửi link TikTok để extract ref audio → em download → Whisper transcribe → phát hiện clip chỉ có voice outro hook "Hãy subscribe cho kênh La La School..." lặp 7 lần qua 192s, KHÔNG phải voice review. Em đã tốn ~10 phút download + analyze trước khi phát hiện.

**Lesson:** LUÔN verify content audio TRƯỚC khi dùng làm ref. TikTok CDN có thể trả về:
- (a) audio watermark track thay vì audio gốc
- (b) voice hook outro (subscribe CTA) thay vì voice content
- (c) chỉ nhạc nền không có voice

## 2-minute verify recipe (BẮT BUỘC trước khi dùng làm ref)

```bash
# 1. Download audio (yt-dlp)
yt-dlp -f audio_best --output "ref_check.%(ext)s" "<tiktok-or-youtube-url>"

# 2. Whisper word-level detect voice segments
#    NO language hint — let model auto-detect (nếu set "vi" mà audio thực ra là music
#    sẽ miss hoặc hallucinate)
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --output-format json \
  --word-timestamps True \
  --output-dir /tmp/ref_check/ \
  ref_check.m4a

# 3. Count unique phrases (Python)
python3 << 'EOF'
import json
d = json.load(open('/tmp/ref_check/ref_check.json'))
texts = []
for s in d.get('segments', []):
    txt = s.get('text', '').strip()
    if txt:
        texts.append(txt)
seen = set()
unique = []
for t in texts:
    if t not in seen:
        seen.add(t)
        unique.append(t)
print(f"Detected language: {d.get('language', 'unknown')}")
print(f"Total segments: {len(d.get('segments', []))}")
print(f"Unique phrases: {len(unique)}")
for i, t in enumerate(unique):
    print(f"  {i+1}. {t[:100]}")
if len(unique) < 3:
    print("⚠️ LIKELY OUTRO HOOK or MUSIC ONLY — DO NOT USE AS REF")
EOF

# 4. VAD check: voice speech thường peak -3 to -10 dB
#    Music thường peak gần 0 dB (dynamic range cao)
ffmpeg -i ref_check.m4a -af "astats=metadata=1:reset=1,ametadata=mode=print:key=lavfi.astats.Overall.Peak_level" -f null - 2>&1 | grep "Peak_level" | head -3
```

## Pass criteria (đủ dùng làm ref)

| Check | Pass | Fail |
|---|---|---|
| Unique phrases | ≥ 3 | < 3 → outro hook hoặc music |
| Detected language | Match expected (vd "vi") | Mismatch (vd "en" cho content Việt) |
| Peak level | < -3 dB (voice) | > -2 dB (music) |
| Voice activity | Có segments 1-5s có energy | Chỉ có 0.1s music bursts |

## Real case @tuan_anh.review (FAIL)

- URL: `https://vt.tiktok.com/ZSXGsWrMr/` (video 7658580075805297938)
- TikTok oEmbed title: "Bài đăng 19 | Sạc dự phòng GOOJODOQ nhỏ gọn cầm tay"
- yt-dlp downloaded: 192s audio, AAC 44.1kHz stereo, 3.1MB
- Whisper detected language: **en** (mismatch — content expected Vietnamese)
- Whisper transcript: 1 câu duy nhất "Hãy subscribe cho kênh La La School..." lặp 7 lần
- Peak level: -0.02 dB (music, không phải voice)
- VAD silent regions: 15.4s, 187.5s, 191.4s (giữa là music fade)

**Conclusion:** Clip này chỉ có voice outro hook, KHÔNG có voice review. User copy nhầm link.

## What to do khi verify FAIL

ĐỪNG cố dùng file này làm ref. Hỏi user:
- "Clip này chỉ có voice outro/sound effect, không phải voice review. Anh có link clip khác không?"
- Hoặc offer option dùng ref audio cũ (ref_10s.wav đã verify work trước đó)
- Hoặc offer option user gửi voice message qua Telegram (giống cách test đầu tiên)

## Workflow 6-step đã verify hoạt động

1. ✅ Download bằng yt-dlp → `/Volumes/Storage-1/Hermes/scratch/<project>/ref_check.m4a`
2. ✅ Whisper word-level + NO language hint → JSON output
3. ✅ Python count unique phrases (script trên) → fail nếu < 3
4. ✅ VAD peak level check
5. ✅ Decision: dùng tiếp / ask user
6. ✅ Nếu user gửi link mới → lặp từ step 1

**Time:** 2 phút cho verify, save hours debugging voice clone trên audio sai.
