# Telegram Video Analysis — Output Format Examples

Real-world output examples from session 2026-06-18, to anchor Pitfall #31 (batch N video → file MD) and Pitfall #32 (frustration signals → deliver fast).

---

## Example A: Batch 17 video transcripts (2026-06-18)

**Trigger:** User gửi 16 video qua Telegram trong 1 batch + nói "transcript toàn bộ".

**Wrong approach (frustrated user):**
- Transcribe 17 file OK
- Gửi 4 Telegram messages dài lần lượt với transcript + phân tích từng video
- User phải nhắc "Alo Alo / Chưa thấy em gửi / Sao rồi / Gửi file md cũng được"
- Phải redo → 1 file MD tổng hợp

**Correct approach (after fix):**
1. Transcribe batch → `/tmp/videos-batch-18-06/<vid>/compressed.{mp4,srt}`
2. Copy SRT files to wiki: `cp /tmp/videos-batch-18-06/<vid>/compressed.srt /Volumes/Storage-1/Hermes/wiki/raw/transcripts/2026-06-18-batch/`
3. **TẠO 1 FILE MD TỔNG HỢP** ngay:
   - Path: `/Volumes/Storage-1/Hermes/wiki/queries/2026-06-18-batch-17-video-transcript-analysis.md`
   - Structure: Overview table (VID / Duration / Cues / Topic) + Phân tích chi tiết từng video + Phân loại theo 4 tử huyệt + Top 3 viral tiềm năng + 5 ý tưởng kịch bản mới
4. **GỬI NGAY** qua Telegram: `MEDIA:/path/to/file.md` + 1-3 bullet tóm tắt
5. KHÔNG gửi từng video riêng lẻ

**Sample deliverable message:**
```
MEDIA:/Volumes/Storage-1/Hermes/wiki/queries/2026-06-18-batch-17-video-transcript-analysis.md

## ✅ Đã xong — 17 video

File MD tổng hợp 13.7KB (overview 17 video + phân tích + top 3 + 5 ý tưởng)

## 🎯 Highlight
- 5 video "Đừng mua X" (anti-selling pattern)
- 6 video DANH trigger (sợ mất/u tín) — mạnh nhất
- 3 video nổi bật: #13 setup đèn iPhone, #2 nước giặt vlogger, #5 bóng đèn 2 ly trà sữa
```

---

## Example B: SRT file naming convention (used in batch)

**Pattern:** `<video-id>-<topic-slug>.srt`

**Real examples from 2026-06-18 batch:**
```
477dec0b1d18-Đừng-bao-giờ-mua-5-thứ-này-khi-xây-kênh..srt
727b66ac978c-Nguy-hiểm-nhất-trong-ba-lô-của-những-anh-em-đi-qua.srt
22a0e70409f3-Hãy-subscribe-cho-kênh-Ghiền-Mì-Gõ-Để-không-bỏ-l.srt
50b50b578f07-Hướng-dẫn-set-up-đèn-để-quay-nét-căng-bằng-con.srt
```

**Why:** Easy to find file theo chủ đề, không cần nhớ VID. Vietnamese OK trong filename (macOS HFS+ supports Unicode).

**Topic source:** Lấy cue đầu tiên của SRT, truncate 60 chars, thay space bằng `-`, loại bỏ `:` `?`.

```bash
topic=$(awk '/^[0-9]+$/{c++} c==1 && !/^[0-9]+$/ && !/^$/ && !/-->/{print; exit}' "$srt" | head -c 60)
safe_topic=$(echo "$topic" | tr ' ' '-' | tr -d ':?')
```

---

## Example C: Overview table format (in MD file)

**Header của MD file:**
```markdown
| # | VID | Duration | Cues | Chủ đề |
|---|-----|----------|------|---------|
| 1 | `477dec0b1d18` | 0:38 | 25 | Đừng mua 5 thứ này khi xây kênh |
| 2 | `727b66ac978c` | 0:49 | 25 | Nguy hiểm nhất trong ba lô vlogger |
| ...
```

**Generate with Python:**
```python
import re
from pathlib import Path

WIKI_DIR = Path("/Volumes/Storage-1/Hermes/wiki/raw/transcripts/2026-06-18-batch")
files = sorted(WIKI_DIR.glob("*.srt"))

for f in files:
    text = f.read_text(encoding='utf-8', errors='replace')
    cues = len(re.findall(r'^\d+$', text, re.MULTILINE))
    topic = ""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == '1':
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip() and '-->' not in lines[j]:
                    topic = lines[j].strip()[:80]
                    break
            break
    # ... print row
```

---

## Example D: Anti-pattern (wrong output)

**What NOT to send:**

❌ Telegram message dài 500+ từ với transcript + analysis inline
❌ "Để em kiểm tra lại nhé" (anh muốn file, không phải lời hứa)
❌ 17 Telegram messages riêng (anh phải scroll)
❌ "Em xin lỗi anh, em chưa gửi được" (giải thích thất bại)

**What to send:**

✅ 1 file MD tổng hợp qua MEDIA
✅ 1-3 bullet tóm tắt NGAY SAU file
✅ Path absolute `/Volumes/Storage-1/Hermes/wiki/queries/...`
✅ KHÔNG giải thích dài dòng — output tự nó nói lên tất cả

---

## When to skip the MD file

- N=1 single video (gửi analysis inline là OK)
- User explicit request "gửi qua Telegram" (không cần MD)
- Quick research (chỉ tóm tắt 1-3 dòng, không cần file)

**When to ALWAYS create MD file:**

- N>3 video + "transcript toàn bộ" / "phân tích tất cả"
- User research session (multi-video research)
- User explicit request "gửi file md cũng được"
- User nhắn "Alo" / "Sao rồi" / "đâu?" — frustration signal → GỬI NGAY file MD