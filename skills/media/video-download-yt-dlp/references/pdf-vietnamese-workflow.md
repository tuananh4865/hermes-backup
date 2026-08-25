# PDF Research Delivery Workflow — Vietnamese-Safe

Khi user yêu cầu "gửi full research bằng 1 file PDF" hoặc research content quá dài cho Telegram text (>4000 chars), dùng workflow này.

## When to use
- User explicit yêu cầu "PDF" / "file" / "document" / "report"
- Research output > 4000 chars (Telegram limit)
- User frustrated bởi "Message delivery failed after multiple attempts"
- Multi-section content (TOC + sections + images + sources)

## When NOT to use
- Content ngắn (< 2000 chars) → Telegram text đủ
- User chỉ muốn summary → trả lời trực tiếp
- Ảnh standalone (1-3 ảnh) → dùng `MEDIA:/path` riêng
- User cần editable → Markdown file (.md) thay vì PDF

## Step-by-step

### 1. Setup venv (CRITICAL — Python 3.11+ PEP 668)

```bash
uv venv /tmp/<task>-pdf-env --python 3.11
source /tmp/<task>-pdf-env/bin/activate
uv pip install reportlab pypdf Pillow
```

**Lỗi thường gặp:** `pip install --user reportlab` fail với "externally-managed-environment" trên Python 3.11+. PHẢI dùng `uv venv`.

### 2. Font setup (Arial Unicode, NOT Helvetica)

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont('Arial', os.path.join(FONT_DIR, "Arial.ttf")))
pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(FONT_DIR, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont('Arial-Italic', os.path.join(FONT_DIR, "Arial Italic.ttf")))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', os.path.join(FONT_DIR, "Arial Bold Italic.ttf")))
```

**Tại sao KHÔNG dùng Helvetica:** Helvetica (mặc định reportlab) thiếu glyph tiếng Việt. Kết quả: chữ Việt render lỗi (ô vuông, dấu hỏi, hoặc missing chars). Đã verified lỗi này 2026-06-22 với PDF hợp đồng OPM716, fix = Arial Unicode.

### 3. Custom styles

```python
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', parent=styles['Heading1'],
    fontName='Arial-Bold', fontSize=20, alignment=TA_CENTER,
    textColor=HexColor('#1a1a2e'))
h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
    fontName='Arial-Bold', fontSize=15, textColor=HexColor('#d62828'))
h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontName='Arial-Bold', fontSize=12, textColor=HexColor('#003049'))
body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontName='Arial', fontSize=10, leading=14, alignment=TA_JUSTIFY)
caption_style = ParagraphStyle('Caption', parent=body_style,
    fontName='Arial-Italic', fontSize=9, textColor=HexColor('#666666'),
    alignment=TA_CENTER)
```

### 4. Image fit helper (không vượt 12-14cm width)

```python
from PIL import Image as PILImage
from reportlab.platypus import Image

def fit_image(img_path, max_w_cm, max_h_cm=18):
    pil = PILImage.open(img_path)
    w_px, h_px = pil.size
    aspect = w_px / h_px
    if max_w_cm / aspect <= max_h_cm:
        return Image(img_path, width=max_w_cm * cm, height=(max_w_cm / aspect) * cm)
    return Image(img_path, width=(max_h_cm * aspect) * cm, height=max_h_cm * cm)
```

### 5. Build PDF

```python
output_path = "/Users/tuananh4865/Downloads/<topic>/report.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="<PDF title>",
    author="Hermes Agent"
)

story = []
# Title
story.append(Paragraph("🏸 TITLE", title_style))
story.append(Paragraph("Subtitle", caption_style))

# TOC
toc_data = [
    ["#", "Mục", "Trang"],
    ["I", "Section 1", "1"],
    # ...
]
toc_table = Table(toc_data, colWidths=[1*cm, 11*cm, 3*cm])
# Apply style
story.append(toc_table)
story.append(PageBreak())

# Sections
story.append(Paragraph("Section 1", h1_style))
story.append(Paragraph("Body text...", body_style))
story.append(fit_image("/path/to/img.jpg", 12))
story.append(Paragraph("Caption", caption_style))

# Page break
story.append(PageBreak())

doc.build(story)
```

### 6. VERIFY output (BẮT BUỘC trước khi gửi)

```python
import pypdf, os

size = os.path.getsize(output_path)
reader = pypdf.PdfReader(output_path)
num_pages = len(reader.pages)

# Extract text từ tất cả pages
all_text = ""
for p in reader.pages:
    all_text += p.extract_text() + "\n"

# Check Vietnamese diacritics (67 chars)
vietnamese_chars = "àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏọồốổỗộớờởỡợùúủũụừứửữựỳýỷỹỵ"
present = [c for c in vietnamese_chars if c in all_text]
present_pct = len(present) / len(vietnamese_chars) * 100

print(f"PDF: {output_path}")
print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")
print(f"Pages: {num_pages}")
print(f"Vietnamese: {len(present)}/67 ({present_pct:.0f}%)")

assert len(present) >= 30, f"Vietnamese rendering FAILED: only {len(present)}/67 diacritics"
assert size > 50_000, f"PDF too small: {size} bytes"
print("✅ PDF ready to send")
```

### 7. Send via Telegram

```
MEDIA:/Users/tuananh4865/Downloads/<topic>/report.pdf
```

## Common pitfalls

### ❌ Pitfall 1: Dùng Helvetica
- Triệu chứng: Text tiếng Việt render thành ô vuông hoặc missing chars
- Fix: Arial Unicode (xem Step 2)

### ❌ Pitfall 2: pip install fail với PEP 668
- Triệu chứng: `error: externally-managed-environment`
- Fix: `uv venv` (xem Step 1)

### ❌ Pitfall 3: Verify chỉ bằng file size
- Triệu chứng: PDF "OK" vì > 50KB, nhưng Vietnamese text render lỗi
- Fix: Extract text bằng pypdf + count Vietnamese diacritics (xem Step 6)

### ❌ Pitfall 4: Ảnh full-res làm PDF > 50MB
- Triệu chứng: PDF quá lớn, Telegram timeout
- Fix: `fit_image()` resize xuống 12-14cm width (~500-800px), JPEG quality 85%

### ❌ Pitfall 5: Quên PageBreak giữa sections
- Triệu chứng: Section 2 bị cắt giữa trang, layout xấu
- Fix: `story.append(PageBreak())` trước mỗi major section

## Reference: Session 2026-06-30 successful PDF

- Topic: Badminton news 23-30/06/2026
- Output: 8 pages, 502 KB, 50/67 Vietnamese diacritics verified
- 3 ảnh embed (Srikanth, An Se-young, Lee Zii Jia)
- 5 sections: Cover/TOC, Vietnam news, Intl news, BWF ranking, Images, Sources
- Script: `/tmp/build_pdf.py` (one-time use)

## Reference: Session 2026-06-22 PDF lỗi đã fix

- Topic: Hợp đồng OPM716
- Lỗi: Helvetica thiếu glyph tiếng Việt → PDF render không đúng
- Fix: Đổi sang Arial Unicode.ttf
- Lesson: Đã ghi vào memory rule "PDF Vietnamese PHẢI dùng Arial Unicode.ttf, KHÔNG dùng Helvetica"
