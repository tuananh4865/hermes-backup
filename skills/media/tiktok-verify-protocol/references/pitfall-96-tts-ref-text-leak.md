# PITFALL #96 — TTS output REF-TEXT LEAK (Whisper word-level BẮT BUỘC)

**Ngày phát hiện:** 23/07/2026 (OmniVoice sequential 5 — em report "PASS" sau volumedetect check, user hỏi "Tại sao luốn có câu 'và bây giờ đang nhờ ai làm kịch bản cho tôi' ở trong các batch vậy?" → 5/5 file bị leak ref text).

## Trigger

Khi verify output từ **TTS voice-clone** (OmniVoice, ElevenLabs voice-clone, F5-TTS, CosyVoice, ...) — em hay chỉ check 2 layer:
- PITFALL #95: container valid + amplitude OK (volumedetect)
- → Em report "PASS" → user nghe thấy câu "Và bây giờ đang nhờ AI..." lẫn vào đầu output → mất trust

**Container + amplitude ĐỦ để pass check #95, NHƯNG KHÔNG ĐỦ để catch content bug.**

## Root cause

Voice-clone model output LUÔN leak 1 phần cuối của ref text vào generated audio:
- Ref audio 17s có transcript "Xin chào đây là giọng đọc của Tuấn Anh. Tôi năm nay 30 tuổi đang thất nghiệp. Và bây giờ đang nhờ AI làm kịch bản cho tôi."
- Output 6.28s "Các bạn ơi, hôm nay mình giới thiệu..." BẮT ĐẦU bằng "Và bây giờ đang nhờ AI làm kịch bản cho tôi" (câu cuối ref text)

Đây là **model bug** (OmniVoice v0.2.1 confirmed) — `denoise=True/False` flag KHÔNG ngăn được. Câu cuối ref text bị inject vào output:
- Đầu file (4/5 case) — "Và bây giờ..." ở 0.0-0.8s trước khi real text bắt đầu
- Giữa file (1/5 case) — ref leak chen vào giữa các câu

**Đây là failure mode KHÁC với PITFALL #95** (amplitude) — volumedetect thấy peak OK (-4 to -5 dB) vì audio có voice, chỉ là sai voice.

## Recipe — Whisper word-level verify (BẮT BUỘC cho TTS voice-clone)

### Step 1: Transcribe output với word timestamps
```bash
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --language vi \
  --output-format json \
  --word-timestamps True \
  --output-dir /tmp/tts_verify/ \
  output.wav
```

### Step 2: Detect ref words
Build set of ref words (lowercase, no punctuation) từ ref_text. So sánh với transcribed words.

```python
REF_TEXT = "Xin chào đây là giọng đọc của Tuấn Anh. Tôi năm nay 30 tuổi đang thất nghiệp. Và bây giờ đang nhờ AI làm kịch bản cho tôi."

# Common Vietnamese ref phrases (lowercase, no diacritics strict match)
REF_PHRASES = [
    "xin chào", "đây là giọng", "giọng đọc của",
    "tôi năm nay", "30 tuổi", "tuổi đang",
    "và bây giờ", "bây giờ đang", "đang nhờ",
    "nhờ ai", "ai làm", "làm kịch bản", "kịch bản cho tôi",
    "đang thất nghiệp", "thất nghiệp",
]
REF_WORDS = set()
for p in REF_PHRASES:
    for w in p.lower().split():
        REF_WORDS.add(w)

def is_ref_word(w):
    wl = w.lower().strip(".,!?")
    return wl in REF_WORDS
```

### Step 3: Find first non-ref word's start time
```python
import json
with open("/tmp/tts_verify/output.json") as f:
    data = json.load(f)

for seg in data.get("segments", []):
    for w in seg.get("words", []):
        wt = w.get("word", "").strip()
        if not wt:
            continue
        if not is_ref_word(wt):
            # First non-ref word = real text starts here
            trim_start = max(0, w["start"] - 0.15)  # margin 0.15s
            break
```

### Step 4: Trim leading ref leak
```python
import soundfile as sf
audio, sr = sf.read("output.wav")
start_sample = int(trim_start * sr)
trimmed = audio[start_sample:]
sf.write("output_trim.wav", trimmed, sr)
```

## Fix evidence (OmniVoice 23/07 sequential 5)

| File | Trước fix | Sau trim |
|---|---|---|
| seq_01_hook | 6.28s, "Và bây giờ..." ở 0.0s | 3.83s, "Các bạn ơi" ở 0.0s ✅ |
| seq_02_problem | 6.80s, "Và bây giờ..." ở 0.0s | 4.33s, "Nhiều anh em..." ở 0.0s ✅ |
| seq_03_solution | 8.08s, "Và bây giờ..." ở 0.0s | 6.05s, "chiếc máy hút bụi..." ở 0.0s ✅ |
| seq_04_usp | 10.28s, "Và bây giờ..." ở 8.4s (GIỮA) | 7.17s, "Điểm mình thích..." ✅ |
| seq_05_cta | 7.36s, "Và bây giờ..." ở 5.5s | 4.75s, "Anh em nào thích..." ✅ |

**Total: 38.80s → 26.13s** (loại bỏ 12.67s ref leak, content 100% real text)

## Recipe tự động — `scripts/trim_ref_leak.py`

Script Python re-runnable đã viết trong session 23/07:
- Input: folder chứa N file output TTS
- Output: N file `*_trim.wav` đã loại bỏ leading ref leak
- Auto-detect: Whisper word-level + REF_PHRASES match
- Margin: 0.15s (giữ 1 chút để tránh cắt mất âm đầu real text)

Xem `scripts/trim_ref_leak.py` để dùng.

## Verify checklist cho TTS voice-clone pipeline

MỖI khi ship TTS voice-clone output (single hoặc batch):

- [ ] PITFALL #95: `volumedetect` confirm amplitude (`max > -10dB`, `rms > -25dB`) ✅
- [ ] **#96 (NEW)**: `mlx_whisper --word-timestamps True` re-transcribe output → diff với input text → confirm KHÔNG có ref words leak
- [ ] Nếu leak detected: chạy `scripts/trim_ref_leak.py` → verify lại bằng Whisper
- [ ] Sample listen 1 file đầu tiên (anh nghe) — **human sanity check**
- [ ] Nếu batch > 3 files: spot check 2-3 file bằng Whisper word-level, không phải chỉ file đầu

## PITFALL đừng quên

- ❌ KHÔNG chỉ check volumedetect (PITFALL #95) cho TTS voice-clone. **Container + amplitude ≠ content clean.**
- ❌ KHÔNG trust `--denoise=True` flag fix ref leak. Real case 23/07: cả `denoise=True` và `denoise=False` đều leak.
- ❌ KHÔNG amplify output để "fix" ref leak — ref leak là content issue, không phải amplitude issue.
- ❌ KHÔNG dùng `remove_silence` để "fix" ref leak — ref leak có voice, không phải silence.
- ❌ KHÔNG skip Whisper verify vì "đã check volumedetect rồi". 2 layer verify BẮT BUỘC cho TTS voice-clone.
- ✅ LUÔN chạy `mlx_whisper --word-timestamps True` cho TTS output, KHÔNG chỉ `volumedetect`.
- ✅ LUÔN check cả leading (0-1s) VÀ middle/end (random position) — ref leak có thể ở bất kỳ đâu.
- ✅ Nếu ref leak detected, dùng `scripts/trim_ref_leak.py` để auto-trim — KHÔNG tự cắt tay.
- ✅ Sau khi trim, verify LẠI bằng Whisper word-level để confirm sạch.
- ✅ Nếu model thường xuyên leak, NOTE trong memory để lần sau expect + apply trim ngay khi generate.

## Cross-reference

- **PITFALL #95 TTS CONTAINER≠CONTENT** (companion) — volumedetect check. PITFALL #96 mở rộng thêm 1 layer: Whisper word-level check cho content bug mà amplitude check miss.
- **PITFALL #57 TRANSCRIPT-FIRST VERIFY** — verify clip = transcript analysis FIRST. PITFALL #96 áp dụng principle tương tự cho TTS output: transcribe trước, analyze sau.
- **PITFALL #99 (tiktok-product-motion-graphics) LUÔN DÙNG VOICE GỐC** — dùng voice gốc từ raw clip tránh được TTS bugs hoàn toàn. PITFALL #96 chỉ apply khi BẮT BUỘC dùng TTS (multi-language, cần custom voice, etc.).

## Repro recipe (OmniVoice 23/07)

Input: 5 text TikTok-style, ref audio 10s, sequential model.generate() 1-by-1
Container + amplitude (PITFALL #95):
```bash
for f in seq_results/*.wav; do
  max=$(ffmpeg -i "$f" -af volumedetect -vn -f null - 2>&1 | grep max_volume | awk '{print $5}')
  echo "$f: max=$max"  # -4.2 to -6.8 dB → ALL OK
done
# → Em report "5/5 PASS" → SAI — content có ref leak
```

Whisper word-level (PITFALL #96):
```bash
for f in seq_results/*.wav; do
  mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
    --word-timestamps True --output-format json --output-dir /tmp/check/ "$f"
  # Parse JSON, find ref words leak → 5/5 file có leak ở đầu/giữa
done
# → 5/5 FAIL — em phải report ref leak, không phải 5/5 PASS
```

Fix workflow:
```bash
python3 scripts/trim_ref_leak.py
# → 5/5 file mới, content sạch
# → Verify lại bằng Whisper: 0 ref words leak
```

## Tools

- **`scripts/trim_ref_leak.py`** — re-runnable action: input folder N file TTS output → output N file `*_trim.wav` không còn ref leak.
- Whisper CLI với `--word-timestamps True` — built-in, không cần install thêm.
