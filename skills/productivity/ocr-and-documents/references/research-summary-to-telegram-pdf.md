# Research Summary → Telegram PDF (fallback for long embed failures)

When research output > ~4000 chars and Telegram returns **"Message
delivery failed after multiple attempts"**, the fix is to ship the
research as a PDF attachment via `MEDIA:/path` instead of trying to
embed the full markdown in chat.

The user (Tuấn Anh) explicitly requested this format: *"Gửi full
research bằng một file pdf cho anh đi"* — preferred when output is long
enough that chat legibility breaks down (multi-section research,
news roundup, comparative analysis).

## When to use

- Telegram delivery failure for messages > 4000 chars
- User asks for "full research as PDF" / "gửi bằng file PDF"
- Research has 4+ sections (TOC-style structure benefits from PDF)
- Output includes tables, ranked lists, or images that get mangled in
  chat (tables become unreadable when truncated)

## When NOT to use

- Output < 2000 chars → just send inline (chunks work fine)
- Output is pure text without tables/images → user can read in chat
- User explicitly asks for chat reply (e.g. "trả lời nhanh")

## Pipeline (mirrors contract-review pipeline)

Same as `references/markdown-to-telegram-pdf.md` (reportlab + Arial
Unicode) but the source is **research summary** not contract review.
Differences:

| Aspect | Contract review | Research summary |
|---|---|---|
| Source content | Legal clauses + risk analysis | News, facts, comparison tables |
| Heading style | Điều khoản N + 3-tier (Nguyên văn/Vấn đề/Gợi ý) | Phần/Section + topic headers |
| Color coding | 🔴/🟡/🟢 for risk | 🇻🇳/🌍/📊/📸/📚 for topic |
| Tables | Short summary at end | BWF ranking, top-5 lists, comparison |
| Images | None (text-only legal) | VĐV photos, product photos — **embed as `Image()` flowable** |

## Image embedding (additions vs contract review)

```python
from reportlab.platypus import Image as RLImage
from PIL import Image as PILImage

def fit_image(img_path, max_w_cm, max_h_cm=18):
    """Resize to fit within max bounds, keep aspect ratio."""
    pil = PILImage.open(img_path)
    w_px, h_px = pil.size
    aspect = w_px / h_px
    if w_cm_target / aspect <= h_cm_target:
        final_w = w_cm_target
        final_h = w_cm_target / aspect
    else:
        final_h = h_cm_target
        final_w = h_cm_target * aspect
    img = RLImage(img_path, width=final_w * cm, height=final_h * cm)
    img.hAlign = 'CENTER'
    return img

# In story:
story.append(Paragraph("Photo caption", h2_style))
story.append(fit_image("/path/to/image.jpg", max_w_cm=12, max_h_cm=14))
story.append(Paragraph("Nguồn: Wikimedia Commons — 960x1440 px", caption_style))
```

**Rule:** vision-verify each image BEFORE adding to PDF (see
`media/video-download-yt-dlp` SKILL.md pitfall I7 — filename lies,
content must be verified).

## Verify recipe (before sending)

```python
import pypdf
reader = pypdf.PdfReader(pdf_path)
print(f"Pages: {len(reader.pages)}")
print(f"Size: {os.path.getsize(pdf_path):,} bytes")

# Vietnamese chars sanity check
all_text = "".join(p.extract_text() for p in reader.pages)
vn_chars = ['à', 'á', 'ả', 'ã', 'ạ', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ',
            'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'ề', 'ế', 'ể', 'ễ', 'ệ',
            'ì', 'í', 'ỉ', 'ĩ', 'ị', 'ò', 'ó', 'ọ', 'ồ', 'ố',
            'ù', 'ú', 'ủ', 'ũ', 'ụ', 'ừ', 'ứ', 'ử', 'ữ', 'ự',
            'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'Ă', 'Â', 'Đ', 'Ê', 'Ô', 'Ơ', 'Ư']
found = sum(1 for c in vn_chars if c in all_text)
print(f"Vietnamese diacritics found: {found}/{len(vn_chars)}")
if found >= 40:
    print("✅ Vietnamese rendering OK")
```

## Naming convention

`<Topic>-<Date>-<Type>.pdf` — e.g. `Tin-the-thao-cau-long-tuan-23-30-Jun-2026.pdf`

Save to: `/Users/tuananh4865/Downloads/<topic>/<pdf-filename>.pdf`

## Delivery

```
MEDIA:/Users/tuananh4865/Downloads/<topic>/<pdf-filename>.pdf
```

Telegram renders the PDF as a native file attachment. User can swipe
through pages on phone, share to lawyer/colleague, save to Drive.

## Reference

Recipe adapted from `references/markdown-to-telegram-pdf.md` (contract
review origin). Both share the same reportlab + Arial Unicode
foundation. Use this file for research/news/comparison content; use
the contract review file for legal/3-tier risk analysis.
