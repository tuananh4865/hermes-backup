# Vietnamese & Bilingual PDF Extraction

Reference for the **post-extraction cleanup pipeline** that turns a raw
`pypdf` / `pymupdf` dump into clean, readable Vietnamese text, plus a
reusable pattern for reviewing Vietnamese legal/contract PDFs.

---

## 1. `pypdf` as a zero-friction alternative to pymupdf

On macOS / Linux boxes where the **system Python is PEP-668 locked**
(Python 3.9 on macOS doesn't have pip, and `pip install --user` is
blocked from writing to `/Library/Python/3.9/site-packages/`), use
`pypdf` via `uv` in a throwaway venv instead of fighting pip:

```bash
uv venv /tmp/pdfvenv --python python3.11
uv pip install --python /tmp/pdfvenv/bin/python pypdf
```

Then extract:

```python
from pypdf import PdfReader
r = PdfReader("contract.pdf")
for i, p in enumerate(r.pages):
    print(p.extract_text())   # already returns str, no .get_text() call
```

`pypdf` is smaller than pymupdf (~5 MB vs ~25 MB), pure Python, and
handles text-based Vietnamese PDFs fine. The trade-off: no
`pymupdf4llm` markdown conversion, no native image extraction. For
"just give me the text" use cases it's faster to spin up than pymupdf.

**When to prefer pypdf over pymupdf:**
- Need text only, no tables / images / OCR
- Sandbox without `pip` but with `uv`
- Small ad-hoc task, don't want to load pymupdf's compiled deps

**When to stay on pymupdf:** everything else (the umbrella skill's
default).

---

## 2. The "spurious spaces" problem in bilingual VN-EN contracts

PDFs generated from bilingual Vietnamese-English legal templates
(Google Docs exports, contract-management software) render with a
**single space between every adjacent character pair** because the
PDF text layer stores characters as positioned glyphs, not as text
runs. The result is:

```
Hợp  đồng  ủy  quyền  quản  lý
```

Not a string with intentional spaces — it's `H`, `ợ`, `p`, ` `, `đ`,
`ồ`, `n`, `g`, ` `, `ủ`, `y`, ... The `read_file` tool returns this
raw, and it looks like broken Vietnamese even though the document is
fine.

**Cleanup regex (run after any extraction):**

```python
import re

text = page.extract_text()
# Collapse "H" + space + "ợ" → "Hợ"
# Pattern: VN letter, optional space, VN letter (no space)
text = re.sub(r'(?<=[a-zà-ỹÀ-Ỹ])\s+(?=[a-zà-ỹÀ-Ỹ])', '', text)
# Strip blank lines
text = '\n'.join(ln.rstrip() for ln in text.split('\n') if ln.strip())
```

The lookbehind/lookahead anchors prevent eating real spaces in
identifiers like "ACB 345958" or "300.000 VNĐ". Apply per-page,
then concatenate.

**Pro tip — strip the English half to halve the read cost:**
Bilingual contracts print VN then EN in the same paragraph. Split on
the first English sentence (heuristic: line containing `Pursuant to` /
`Independence` / `Party A`):

```python
def split_vi_en(text: str) -> str:
    for marker in ("Pursuant to", "Independence", "Party A",
                   "Authorized and Apartment"):
        idx = text.find(marker)
        if idx > 50:    # require some VN before the switch
            return text[:idx]
    return text
```

The Vietnamese half is the legally binding one anyway (most VN
contracts state "Vietnamese version prevails" in the language clause).

---

## 3. Vietnamese legal-contract review pattern

After clean extraction, structure the review as a **3-tier risk
table** with concrete rewrites. The format that worked for a 23-page
bilingual VN-EN property-management contract:

### Tier 1 — table of red flags (rủi ro cao)

For each red flag, cite the **specific Điều khoản** number, quote
the exact phrase, and propose a concrete rewrite. Example:

| # | Điều khoản | Mức rủi ro | Hành động |
|---|------------|-------------|-----------|
| 1 | Phí 300k + bonus gia hạn 15% | 🔴 Cao | Thêm trần tổng phí môi giới/năm |
| 2 | Độc quyền 12 tháng + tự động gia hạn | 🔴 Cao | Bỏ tự động gia hạn, hoặc đàm phán lại phí |

The table makes the user scan the worst 5-7 items in 10 seconds, then
expand into prose for each.

### Tier 2 — prose explanation per red flag

For each item, structure the explanation as:

1. **Quote the clause** in Vietnamese (verbatim from PDF).
2. **Explain the risk in 1-2 sentences** — what specifically can go wrong.
3. **Give a concrete rewrite** — "Thêm điều khoản: 'tổng phí môi giới + bonus gia hạn không vượt quá X% doanh thu năm'".

The rewrite step is critical. Just listing risks is not actionable.

### Tier 3 — green flags (điểm tốt)

Mention 3-5 things the user got right or that protect them. This
builds trust that the review is balanced, not just a hit piece
against the counterparty. Users who see only red flags assume the
agent is being alarmist.

### Tier 4 — summary action table

End with a single "Anh cần sửa gì trước khi ký" table that lists
all the rewrites, sorted by risk level. This becomes the user's
negotiation checklist.

---

## 4. Common clauses to ALWAYS flag in VN contracts

These patterns appear in 80%+ of Vietnamese service contracts and
almost always favor the drafter (Bên B) over the signer (Bên A):

- **Phạt chậm thanh toán 0.05%/ngày** (≈18%/năm) — high, should be 0.03%.
- **Tự động gia hạn** with 30-day notice — easy to forget, locks the user in another 12 months.
- **Bên B miễn trừ trách nhiệm gần hết** (Disclaimer clauses) — flag every "Bên B không chịu trách nhiệm" item.
- **Bên B được ủy quyền ký HĐ thuê** — limit to template pre-approved by Bên A.
- **Phí môi giới + bonus gia hạn cộng dồn** — request a cap.
- **Bảng giá sửa chữa "theo giá thị trường"** — request price ceiling or pre-approval.
- **Phạt đơn phương chấm dứt nếu chậm 30 ngày** — asymmetric, should require longer cure period.

When reviewing any VN contract, scan for these first. If 4+ appear,
the contract is heavily Bên B-skewed regardless of industry.
