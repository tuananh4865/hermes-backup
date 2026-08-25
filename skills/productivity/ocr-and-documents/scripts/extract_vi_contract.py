#!/usr/bin/env python3
"""Extract and clean Vietnamese-bilingual (VN/EN) legal PDFs.

Handles the two recurring problems with Vietnamese contract PDFs:
  1. `read_file` on a PDF returns raw binary stream (unusable)
  2. PDF text layer has a single space between every adjacent VN char pair
  3. Bilingual contracts print VN then EN in the same paragraph

This script writes:
  - <stem>.full.txt   : all pages, all languages (raw + cleaned)
  - <stem>.vi.txt      : VN-only (heuristic: stops at first EN marker)

The VN output is suitable for clause-by-clause legal review. EN output
is dropped because (a) it's not the legally binding version in VN
contracts, and (b) it doubles the noise.

Usage:
    # Activate pypdf venv first
    uv venv /tmp/pdfvenv --python python3.11
    uv pip install --python /tmp/pdfvenv/bin/python pypdf

    /tmp/pdfvenv/bin/python3 scripts/extract_vi_contract.py contract.pdf
    /tmp/pdfvenv/bin/python3 scripts/extract_vi_contract.py contract.pdf --out-dir /tmp
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf not installed. Run:\n"
             "  uv venv /tmp/pdfvenv --python python3.11\n"
             "  uv pip install --python /tmp/pdfvenv/bin/python pypdf\n"
             "Then re-run with: /tmp/pdfvenv/bin/python3 scripts/extract_vi_contract.py <pdf>")

# Cleanup regex from references/vietnamese-pdf-extraction.md § 2
VN_CHAR = r'[a-zà-ỹÀ-Ỹ]'
COLLAPSE_VN_SPACES = re.compile(rf'(?<={VN_CHAR})\s+(?={VN_CHAR})')

# English-half detection (stop at first English line)
EN_MARKERS = ("Pursuant to", "Independence", "Party A", "Authorized and Apartment",
              "Building/Serviced", "the Parties hereby")


def clean_vi(text: str) -> str:
    """Collapse single-spaces between VN chars, strip blank lines."""
    text = COLLAPSE_VN_SPACES.sub('', text)
    return '\n'.join(ln.rstrip() for ln in text.split('\n') if ln.strip())


def split_vi_en(text: str) -> str:
    """Cut the page at the first English-language marker (heuristic)."""
    for marker in EN_MARKERS:
        idx = text.find(marker)
        if idx > 50:    # require some VN before the switch
            return text[:idx]
    return text


def extract(pdf_path: Path, out_dir: Path) -> tuple[Path, Path]:
    reader = PdfReader(str(pdf_path))
    full_pages = []
    vi_pages = []

    for i, page in enumerate(reader.pages):
        raw = page.extract_text() or ""
        full_pages.append(f"\n\n========== PAGE {i+1} ==========\n\n{raw}")

        # Per-page bilingual split + clean
        vi = split_vi_en(raw)
        vi = clean_vi(vi)
        if vi:
            vi_pages.append(f"\n=== TRANG {i+1} ===\n{vi}")

    stem = pdf_path.stem
    full_path = out_dir / f"{stem}.full.txt"
    vi_path = out_dir / f"{stem}.vi.txt"
    full_path.write_text('\n'.join(full_pages), encoding='utf-8')
    vi_path.write_text('\n'.join(vi_pages), encoding='utf-8')
    return full_path, vi_path


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pdf", type=Path, help="Path to VN-bilingual PDF")
    p.add_argument("--out-dir", type=Path, default=Path("/tmp"),
                   help="Output directory (default: /tmp)")
    args = p.parse_args()

    if not args.pdf.exists():
        sys.exit(f"File not found: {args.pdf}")

    full, vi = extract(args.pdf, args.out_dir)
    print(f"Full text: {full} ({full.stat().st_size} bytes)")
    print(f"VN-only:   {vi} ({vi.stat().st_size} bytes)")
    print(f"Pages:     {len(PdfReader(str(args.pdf)).pages)}")


if __name__ == "__main__":
    main()
