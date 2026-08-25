---
name: ocr-and-documents
description: PDF and document workflow — extract text from PDFs/scans (pymupdf, marker-pdf), edit PDFs with natural-language instructions (nano-pdf), split/merge/search, and produce clean markdown. Covers the full read-and-modify PDF lifecycle. Also covers Vietnamese bilingual contract review (extract → clean → 3-tier risk analysis → Telegram PDF delivery).
version: 2.5.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR, Editing, nano-pdf, pymupdf, marker, NL-edit, Vietnamese, Contract-Review, Telegram-Delivery]
    related_skills: [powerpoint, nano-pdf]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pypdf (~5MB) | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|--------------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ❌ | ✅ (90+ languages) |
| **Tables** | ❌ | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ❌ | ✅ |
| **Code blocks** | ❌ | ❌ | ✅ |
| **Forms** | ❌ | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ❌ | ✅ |
| **Reading order detection** | ❌ | ❌ | ✅ |
| **Images extraction** | ❌ | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ❌ | ✅ |
| **EPUB** | ❌ | ✅ | ✅ |
| **Markdown output** | ❌ | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~5MB (pure Python) | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |
| **PEP-668 friendly** | ✅ (works via `uv venv`) | ⚠️ (needs build tools) | ⚠️ (needs PyTorch) |

**Decision**:
- **pypdf** — text-only, no fancy features, zero-friction install via `uv venv` when system Python is PEP-668 locked. Use for quick contract readouts, arxiv abstracts, anything where you only need strings.
- **pymupdf** — default for text-based PDFs that need tables, images, markdown, split/merge, search. Most production work.
- **marker-pdf** — only when you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## pypdf (lightweight, PEP-668 safe)

When the system Python is locked (macOS 3.9 has no pip, and
`pip install --user` is blocked from writing to
`/Library/Python/3.9/site-packages/`) and you only need **plain text
from a text-based PDF** — no tables, no images, no markdown — `pypdf`
is the zero-friction option.

```bash
uv venv /tmp/pdfvenv --python python3.11
uv pip install --python /tmp/pdfvenv/bin/python pypdf
```

```python
from pypdf import PdfReader
r = PdfReader("contract.pdf")
for i, page in enumerate(r.pages):
    print(f"--- PAGE {i+1} ---")
    print(page.extract_text())
```

`pypdf` is pure Python, ~5MB, and `extract_text()` already returns
`str` (no `.get_text()` like pymupdf). For bilingual VN-EN legal
PDFs the raw text has spurious single-spaces between every VN
character pair — see `references/vietnamese-pdf-extraction.md` for
the cleanup regex.

**For Vietnamese-bilingual legal/contract PDFs**, use the dedicated
helper:

```bash
/tmp/pdfvenv/bin/python3 scripts/extract_vi_contract.py contract.pdf
```

This produces `<name>.full.txt` (all pages, both languages) and
`<name>.vi.txt` (VN-only, with the EN half stripped at the first
EN marker). Saves ~50% of the read cost and avoids confusing
Vietnamese contract review with English paraphrase noise.

If you need tables, images, markdown, or split/merge/search →
use **pymupdf** (next section).

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support)
- **Vietnamese bilingual PDFs**: see `references/vietnamese-pdf-extraction.md` for the cleanup regex and the 3-tier contract-review pattern (always check for: tự động gia hạn, phạt 0.05%/ngày, Bên B miễn trừ, ủy quyền không giới hạn, bonus gia hạn cộng dồn)

---

## Vietnamese contract review — trigger and output pipeline

When the user (typically Tuấn Anh) asks to "đọc hợp đồng", "review hợp đồng", "phân tích điều khoản bất lợi", or sends a VN/EN bilingual legal PDF/DOCX — this is the full pipeline:

1. **Extract with pypdf** (zero-friction venv) — see `scripts/extract_vi_contract.py`
2. **Clean bilingual** — strip EN half, collapse single-spaces between VN chars
3. **Analyze with the 3-tier review pattern** — see `references/vietnamese-pdf-extraction.md` § 3
4. **Format the user's preferred output** — see "Output format the user wants" below
5. **Deliver as Telegram PDF attachment** — see `references/markdown-to-telegram-pdf.md` for the reportlab pipeline (it produces a small, A4, monospace-friendly PDF suitable for `MEDIA:` delivery)

### Output format the user wants (Tuấn Anh's hard preference)

When reviewing a contract, the user wants **verbatim original + concrete rewrite** — not a summary. For each red flag:

| Section | What to include |
|---|---|
| **📄 Nguyên văn** | Quote the original clause verbatim (VN). Do not paraphrase. |
| **⚠️ Vấn đề cho Bên A** | 2-4 bullets explaining the specific risk in plain Vietnamese. |
| **✏️ Gợi ý sửa** | A concrete rewrite — paste-ready text, not "consider changing X". |

End with a **single summary table** sorted by risk (🔴/🟡/🟢) so the user can scan the must-fix items in 10 seconds.

**Do NOT** paraphrase the original, give "you may want to consider" hedging, or skip the rewrite step. The user wants actionable rewrites they can paste into the contract negotiation.

---

## Section: PDF Editing via Natural Language (`nano-pdf`)

The previous sections cover **reading** PDFs. This section covers **editing** them — fixing typos, swapping titles, updating dates, changing names — using natural-language instructions.

### When to Use

- "Fix the typo on page 3 of report.pdf"
- "Change the title from X to Y"
- "Update the date in the contract"
- "Replace this name throughout the document"
- Any small text edit that doesn't require rebuilding the PDF from source

For **extraction** (reading content out of a PDF), use the pymupdf / marker-pdf sections above. For **rebuilding** a PDF from scratch (e.g. programmatically generating a deck), use a library like ReportLab or WeasyPrint instead.

### Prerequisites

```bash
# Install with uv (recommended — already available in Hermes)
uv pip install nano-pdf

# Or with pip
pip install nano-pdf
```

nano-pdf uses an LLM under the hood and requires an API key. Check `nano-pdf --help` for the env var name (typically the same one your other LLM tools use).

### Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

### Examples

```bash
# Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"

# Update a date on a specific page
nano-pdf edit report.pdf 2 "Update the date from January to February 2026"

# Fix content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

### Pitfalls

- **Page numbers may be 0-based or 1-based depending on version** — if the edit hits the wrong page, retry with ±1.
- **Always verify the output PDF after editing** (use `read_file` to check file size, or open it). nano-pdf uses an LLM, so edits are not deterministic — small wording changes are possible.
- **Works well for text changes; complex layout modifications may need a different approach.** If the edit is large (paragraphs, tables, images), rebuild the PDF from source.
- **Edits are in-place by default** — back up the original first if you want to compare.

### Notes

- nano-pdf complements pymupdf / marker-pdf (which read) by adding a write/edit capability to the same PDF workflow
- **For batch edits across many pages**, run multiple `nano-pdf edit` calls rather than trying to do everything in one instruction
- This skill section was formerly a standalone `nano-pdf` skill

## Research summary as PDF (fallback for Telegram "Message delivery failed")

When research/news/comparison output > ~4000 chars and Telegram embed fails, ship as PDF via `MEDIA:/path`. Same reportlab + Arial Unicode foundation as contract review, but with image embedding (vĐV photos, product shots). User preference: *"Gửi full research bằng một file pdf cho anh đi"* when output is long.

See `references/research-summary-to-telegram-pdf.md` for the full recipe (image embedding via `RLImage`, verify recipe, naming convention).
