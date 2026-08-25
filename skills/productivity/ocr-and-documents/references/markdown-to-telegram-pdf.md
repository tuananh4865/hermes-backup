# Markdown → A4 PDF for Telegram delivery

When the user wants a long analysis (contract review, market research,
data report) delivered as a Telegram file attachment, render the
markdown to a small A4 PDF with `reportlab` and ship via
`MEDIA:<path>`.

This is the pipeline that worked for a 23-page bilingual VN-EN
property-management contract review (analysis 26 KB markdown →
29 KB PDF, scannable on phone).

## Why this pattern

- Telegram has no native markdown→PDF converter.
- Pasting long markdown into a chat breaks legibility (especially
  tables, code blocks, and the user's preferred visual hierarchy
  with `📄 Nguyên văn` / `⚠️ Vấn đề` / `✏️ Gợi ý sửa` headers).
- The user's phone is the primary review surface — they want a
  file they can open in landscape and swipe through.
- `reportlab` is pure Python, ~5 MB, works offline, no API key.

## Pipeline (3 steps)

### 1. Write the analysis in markdown

Use this heading hierarchy (matches what the user has come to expect
from contract reviews):

```
# Title
## Điều khoản N — title
### 📄 Nguyên văn
### ⚠️ Vấn đề cho Bên A
### ✏️ Gợi ý sửa
## Điều khoản N+1 — ...
```

Tables for the summary at the end:

```markdown
| # | Điều | Mức rủi ro | Hành động |
|---|------|-------------|-----------|
| 1 | ...  | 🔴 Cao     | ...       |
```

### 1.5. Vietnamese font fix (REQUIRED for any VN content)

Helvetica is the reportlab default and it does **not** include the
glyphs for Vietnamese diacritics. Add this block **before** you
build any PDF that contains Vietnamese text:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# macOS — built-in font with full Unicode coverage
pdfmetrics.registerFont(TTFont('ArialUnicode',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('ArialUnicode-Bold',
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('ArialUnicode-Italic',
    '/System/Library/Fonts/Supplemental/Arial Italic.ttf'))
pdfmetrics.registerFont(TTFont('ArialUnicode-BoldItalic',
    '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'))
registerFontFamily('ArialUnicode',
    normal='ArialUnicode', bold='ArialUnicode-Bold',
    italic='ArialUnicode-Italic', boldItalic='ArialUnicode-BoldItalic')
```

Then every `ParagraphStyle` in the script must use these fonts
instead of the defaults. Replace the style block from § 2 with:

```python
title_style = ParagraphStyle('Title', fontName='ArialUnicode-Bold',
    fontSize=15, textColor=HexColor('#1a1a1a'),
    spaceAfter=12, leading=20)
h2_style = ParagraphStyle('H2', fontName='ArialUnicode-Bold',
    fontSize=12.5, textColor=HexColor('#c0392b'),
    spaceBefore=14, spaceAfter=6, leading=16)
h3_style = ParagraphStyle('H3', fontName='ArialUnicode-Bold',
    fontSize=10.5, textColor=HexColor('#2c3e50'),
    spaceBefore=8, spaceAfter=4, leading=14)
body_style = ParagraphStyle('Body', fontName='ArialUnicode',
    fontSize=9, leading=13, spaceAfter=4)
quote_style = ParagraphStyle('Quote', fontName='ArialUnicode-Italic',
    fontSize=9, leading=13, leftIndent=15, rightIndent=10,
    textColor=HexColor('#555'), spaceAfter=4)
warn_style = ParagraphStyle('Warn', fontName='ArialUnicode',
    fontSize=9, leading=13, leftIndent=10,
    textColor=HexColor('#c0392b'), spaceAfter=4)
fix_style = ParagraphStyle('Fix', fontName='ArialUnicode',
    fontSize=9, leading=13, leftIndent=10,
    textColor=HexColor('#27ae60'), spaceAfter=4)
table_style = ParagraphStyle('Table', fontName='ArialUnicode',
    fontSize=8.5, leading=12, spaceAfter=2)
```

When you build, also fix the inline-formatter: the default
`re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)` is fine, but
`<i>“text”</i>` only works if the chosen `fontName` family has an
italic variant registered (it does — `ArialUnicode-Italic`).

**Cross-platform font paths** (use the first that exists on the
host machine):

| OS | Font path |
|---|---|
| **macOS (built-in)** | `/System/Library/Fonts/Supplemental/Arial Unicode.ttf` |
| macOS fallback | `/Library/Fonts/Arial Unicode.ttf` (older OS) |
| Linux (apt) | `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` (Bold/Italic/BoldItalic variants also exist) |
| Linux (fc-list) | `fc-match -f '%{file}\n' ':lang=vi'` to find a TTF that supports Vietnamese |
| Windows | `C:\Windows\Fonts\arialuni.ttf` (Arial Unicode MS) or `arial.ttf` (limited VN) |

If none of those exist, install one. A good always-available
fallback is `pip install fonttools` + download a TTF like
`NotoSans-Regular.ttf` from Google Fonts.

### 2. Convert to PDF with reportlab

```python
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT

# Read markdown
with open('/tmp/analysis.md') as f:
    md = f.read()

# Styles (color-code the headings for quick scanning)
styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Title'],
    fontSize=16, spaceAfter=12, alignment=TA_LEFT)
h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=13, textColor=HexColor('#c0392b'),
    spaceBefore=14, spaceAfter=6)
h3_style = ParagraphStyle('H3', parent=styles['Heading3'],
    fontSize=11, textColor=HexColor('#2c3e50'),
    spaceBefore=8, spaceAfter=4)
body_style = ParagraphStyle('Body', parent=styles['BodyText'],
    fontSize=9.5, leading=13, spaceAfter=4)
quote_style = ParagraphStyle('Quote', parent=body_style,
    leftIndent=15, textColor=HexColor('#555'),
    fontName='Helvetica-Oblique')
warn_style = ParagraphStyle('Warn', parent=body_style,
    leftIndent=10, textColor=HexColor('#c0392b'))
fix_style = ParagraphStyle('Fix', parent=body_style,
    leftIndent=10, textColor=HexColor('#27ae60'))

# Build flowables from markdown lines
doc = SimpleDocTemplate('/tmp/analysis.pdf', pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm)
flowables = []

import re
for line in md.split('\n'):
    s = line.strip()
    if not s or s == '---':
        flowables.append(Spacer(1, 0.15*cm))
        continue
    if s.startswith('# '):
        flowables.append(Paragraph(re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s[2:]), title_style))
    elif s.startswith('## '):
        flowables.append(Paragraph(re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s[3:]), h2_style))
    elif s.startswith('### '):
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s[4:])
        # Color-code the three standard VN contract headers
        if text.startswith('📄'):
            flowables.append(Paragraph(f"<b>{text}</b>", quote_style))
        elif text.startswith('⚠️'):
            flowables.append(Paragraph(f"<b>{text}</b>", warn_style))
        elif text.startswith('✏️'):
            flowables.append(Paragraph(f"<b>{text}</b>", fix_style))
        else:
            flowables.append(Paragraph(f"<b>{text}</b>", h3_style))
    elif s.startswith('> '):
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s[2:])
        flowables.append(Paragraph(f"<i>“{text}”</i>", quote_style))
    elif s.startswith('|'):
        # Render table row as a flat text line
        cells = [c.strip() for c in s.split('|')[1:-1]]
        if not all(set(c) <= set('-:') for c in cells):
            text = ' | '.join(cells)
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            flowables.append(Paragraph(text, body_style))
    elif s.startswith('- '):
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s[2:])
        flowables.append(Paragraph(f"• {text}", body_style))
    else:
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        flowables.append(Paragraph(text, body_style))

doc.build(flowables)
```

### 3. Deliver via Telegram

```python
# In the assistant response, attach the PDF:
# MEDIA:/tmp/analysis.pdf
```

The gateway converts the `MEDIA:` directive into a native Telegram
file attachment. The user can open it in any PDF viewer, swipe
through pages, and forward it to a lawyer / counterparty.

## Pitfalls

- **Tables in reportlab are awkward** — the script above flattens
  markdown table rows into ` | `-separated lines. That's good enough
  for contract review summaries where the table is short and
  scannable. For long tables (>10 rows), consider switching to
  reportlab's `Table` flowable with explicit column widths.
- **🚨 Vietnamese diacritics DO NOT render in reportlab's default
  Helvetica font.** Empirically verified 2026-06-22 — a bilingual
  VN-EN contract review came out with broken glyphs (boxes, missing
  dấu, scrambled chars) in the first Telegram delivery, and the
  user pushed back hard: *"file em viết bị lỗi font, hãy dùng
  font nào viết chuẩn tiếng Việt được!!!"*. The reference's old
  claim "Vietnamese diacritics render correctly in reportlab's
  default Helvetica font" was **wrong** — it now lives here as a
  pitfall. **Always register a TTF font with full Unicode coverage
  before building the PDF.** Use the "Vietnamese font fix" block
  below — the recipe in this file has been updated accordingly.
- **Don't use the `MEDIA:` directive with non-existent files** —
  the gateway will return an error to the user. Always verify the
  file exists with `ls -la` or `os.path.exists()` before including
  the directive.
- **Keep the PDF under 50 MB** — Telegram's bot API has a 50 MB
  upload limit. A 30-page contract review is typically 20-50 KB.
- **Also save the markdown to a stable location** (e.g.
  `/Volumes/Storage-1/Hermes/<project>/ANALYSIS.md`) so the user
  has the editable source. The PDF is for reading, the .md is for
  remixing.
