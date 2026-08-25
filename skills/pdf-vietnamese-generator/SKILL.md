---
name: pdf-vietnamese-generator
description: Generate PDF documents with Vietnamese text using reportlab + Arial Unicode. Use when creating any PDF output that contains Vietnamese diacritics (contracts, reports, analysis docs), OR when converting Markdown files to PDF for Telegram mobile delivery (avoids Vietnamese font breakage on Android/iOS).
version: 1.1.0
created: 2026-06-22
updated: 2026-07-25
author: Hermes Orchestrator
license: MIT
metadata:
  hermes:
    tags: [pdf, vietnamese, reportlab, font, contract, document, telegram, mobile]
    related_skills: [self-verify-after-workaround, tiktok-product-script]
    source_session: "20260622_093240_2227173d + 2026-07-25 batch scripts"
---

# Vietnamese PDF Generator (reportlab + Arial Unicode)

## When to use

Trigger this skill for ANY PDF output containing Vietnamese text:
- Contract analysis reports (OPM716, NDA, service agreements)
- Vietnamese research summaries
- Vietnamese business letters, invoices, proposals
- **MD → PDF conversion for Telegram mobile delivery (NEW 25/07/2026)** — khi user yêu cầu "gửi file qua Telegram", Markdown file `.md` trên Telegram preview có thể bị lỗi font tiếng Việt có dấu trên Android/iOS. Convert sang PDF với Arial Unicode là cách fix.
- Any user request that needs PDF output with Vietnamese content

## The problem

Reportlab's default Helvetica font is **Latin-1 only** — it lacks the combining diacritical marks needed for Vietnamese (ă, â, ơ, ư, ế, ệ, ọ, ị, etc.). PDF generated without explicit font registration renders Vietnamese as broken glyphs.

**Telegram preview của Markdown file `.md` cũng có cùng vấn đề**: system font không cover đủ 50,000+ glyphs → chữ có dấu hiển thị ô vuông trên mobile (verified case 25/07/2026 — user feedback "Lỗi font" khi em gửi `.md` 31KB).

## The fix (verified 2026-06-22 + 2026-07-25)

Use macOS's built-in **Arial Unicode**:
- Path: `/System/Library/Fonts/Supplemental/Arial Unicode.ttf`
- Covers 50,000+ Unicode glyphs (all Vietnamese + English bilingual)
- No install needed — bundled with macOS

## Working code template

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

# 1. Register font (REQUIRED)
FONT_PATH = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
pdfmetrics.registerFont(TTFont('ArialUnicode', FONT_PATH))

# 2. Create styles using the registered font
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'ArialUnicode'
styles['Normal'].fontSize = 11
styles['Normal'].leading = 15

styles.add(ParagraphStyle(
    name='VietnameseTitle',
    fontName='ArialUnicode',
    fontSize=18,
    leading=22,
    spaceAfter=12,
    textColor='#1a1a1a',
    alignment=1  # center
))

styles.add(ParagraphStyle(
    name='VietnameseHeading',
    fontName='ArialUnicode',
    fontSize=14,
    leading=18,
    spaceBefore=14,
    spaceAfter=8,
    textColor='#2c5282',
))

# 3. Build PDF
def build_pdf(output_path, sections):
    """sections = [{'type': 'title|heading|body', 'text': str}, ...]"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    story = []
    for s in sections:
        if s['type'] == 'title':
            story.append(Paragraph(s['text'], styles['VietnameseTitle']))
        elif s['type'] == 'heading':
            story.append(Paragraph(s['text'], styles['VietnameseHeading']))
        elif s['type'] == 'body':
            story.append(Paragraph(s['text'], styles['Normal']))
        elif s['type'] == 'spacer':
            story.append(Spacer(1, 0.5*cm))
        elif s['type'] == 'pagebreak':
            story.append(PageBreak())
    doc.build(story)
    return output_path

# 4. Verify (MANDATORY — never skip)
def verify_pdf(pdf_path):
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    text = r.pages[0].extract_text()
    if any(c in text for c in 'ăâêôơư'):
        return True, f"OK: {len(r.pages)} pages, Vietnamese chars detected"
    return False, "WARNING: no Vietnamese diacritics detected"
```

## MD → PDF conversion script (NEW 25/07/2026, from session 3-scripts-batch)

Khi user yêu cầu "gửi file qua Telegram" với file Markdown có tiếng Việt có dấu dài > 5KB → convert sang PDF với script auto:

**Script**: `scripts/md_to_pdf_vi.py` (đã verified 25/07/2026 — 31KB MD → 13 trang PDF, Vietnamese diacritics detected đầy đủ ă, â, ư, ế, ọ).

```bash
/Users/tuananh4865/.hermes/hermes-agent/venv/bin/python \
    /Users/tuananh4865/.hermes/skills/pdf-vietnamese-generator/scripts/md_to_pdf_vi.py \
    input.md output.pdf
```

**Output verify**:
```
✅ PDF generated:
  Pages: 13
  Vietnamese diacritics detected: True
  Size: 72,323 bytes
  Sample: "3 SCRIPTS BATCH — 25/07/2026 Công thức v0.12.0: Problem → Solution..."
```

**Features script**:
- Parse Markdown: H1-H4, bullet list, ordered list, blockquote (with colored background), table (with header style), code block (Courier font)
- Inline markdown: **bold**, *italic*, `code`, [link](url) → HTML
- Render với Arial Unicode (50,000+ glyphs) → 100% Vietnamese compatibility
- Tự động verify Vietnamese diacritics (grep 'ăâêôơưếệọịầằ' trong PDF text)

**Self-check rule khi nào convert MD → PDF:**
- File `.md` > 5KB → gửi PDF, không gửi MD
- File `.md` ≤ 5KB → có thể gửi MD trực tiếp (vẫn cảnh báo Telegram có thể lỗi font)
- Nội dung có nhiều tiếng Việt có dấu + table phức tạp → LUÔN PDF
- Wiki links `[[slug]]` → PDF sẽ hiển thị nguyên text (không clickable) → cân nhắc gửi MD nếu anh cần click links

**Workflow cho batch scripts** (verified 25/07/2026):
1. User yêu cầu viết N scripts (N≥2) theo formula Problem-Solution
2. Em viết N file `.md` riêng vào `wiki/projects/<project>/scripts/` (giữ nguyên format file gốc)
3. Gộp thành 1 file `/Volumes/Storage-1/Hermes/scratch/<N>-scripts-batch-YYYY-MM-DD.md`
4. Convert sang PDF: `python3 scripts/md_to_pdf_vi.py <file_gộp> <file.pdf>`
5. Gửi qua Telegram: `MEDIA:<file.pdf>` (KHÔNG gửi path, KHÔNG gửi MD)
6. Verify Vietnamese diacritics detected trước khi gửi

## Self-verification (REQUIRED before sending to user)

```python
ok, msg = verify_pdf('/tmp/output.pdf')
if not ok:
    raise RuntimeError(f"PDF font broken: {msg}")
print(f"OK: {msg}")
```

Or via shell:

```bash
python3 -c "
from pypdf import PdfReader
r = PdfReader('/tmp/output.pdf')
t = r.pages[0].extract_text()
assert any(c in t for c in 'ăâêôơư'), 'Font broken'
print(f'OK {len(r.pages)} pages')
"
```

## Delivery pattern

After generating PDF for Tuấn Anh:
1. Copy to `/Volumes/Storage-1/Hermes/<project-folder>/` (anh tự tạo folder theo từng dự án)
2. Send via Telegram: `MEDIA:/path/to/file.pdf`
3. Show summary of contents in chat (sections + key findings)

## Pitfalls

- **Telegram Markdown preview lỗi font tiếng Việt (NEW 25/07/2026, from user feedback "Lỗi font")**. Khi gửi file `.md` qua Telegram, anh đọc trên điện thoại có thể thấy chữ tiếng Việt có dấu bị lỗi (ô vuông, font hỏng) — đặc biệt trên Android hoặc khi system font không cover đầy đủ Vietnamese combining diacritics (ă, â, ơ, ư, ế, ệ, ọ, ị...). **Fix (HARD RULE)**: KHI file > 5KB HOẶC có nhiều tiếng Việt có dấu + table phức tạp → LUÔN convert sang PDF với Arial Unicode TRƯỚC khi gửi `MEDIA:` qua Telegram. Self-check: nếu user feedback "lỗi font" → đã gửi `.md` thay vì `.pdf` → convert lại + re-send.

- Do NOT use Helvetica/Times/Courier for Vietnamese — silent font breakage
- Do NOT skip the verification step — broken PDF looks fine in reportlab preview
- Do NOT use `Paragraph` with HTML entities without escaping `&` `<` `>` first
- Always register Arial Unicode BEFORE defining styles
- Always use `Paragraph` (not `drawString`) for text — handles encoding correctly
- For Linux: install `fonts-noto-core` or use DejaVu Sans from `/usr/share/fonts/truetype/dejavu/`

## Related

- `wiki/concepts/vietnamese-pdf-font.md` — full reference + alternatives table
- Session `20260622_093240_2227173d` — original OPM716 contract analysis where this pattern was developed
- Skill `self-verify-after-workaround` — apply verification loop for any file output
- Skill `tiktok-product-script` v0.13.1 — workflow tạo batch scripts + gửi qua Telegram PDF
- `scripts/md_to_pdf_vi.py` — auto convert MD → PDF Vietnamese (Arial Unicode)