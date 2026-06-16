# Quality Checker — Detailed Check Criteria

> Companion file cho `SKILL.md`. Đọc khi cần chi tiết về 6 check categories.

---

## 1. FORMAT

### Checklist

- [ ] File extension đúng (.md, .json, .yaml, .py...)
- [ ] Markdown headings hierarchy đúng (H1 > H2 > H3, không skip level)
- [ ] Code blocks có language tag (` ```python `, ` ```yaml `)
- [ ] Tables có header row + alignment
- [ ] Lists consistent (chỉ `-` hoặc chỉ `*`, không mix)
- [ ] File path references dùng backticks: `~/.hermes/...`
- [ ] Links format đúng: `[text](url)` hoặc `[[wikilink]]`
- [ ] Không có trailing whitespace
- [ ] Encoding UTF-8 (có emoji nếu cần)

### Common failures

| Failure | Severity | Fix |
|---------|----------|-----|
| Code block không có language | minor | Thêm tag sau \`\`\` |
| Heading skip level (H1 → H3) | minor | Thêm H2 hoặc đổi H3 → H2 |
| Mix tabs/spaces trong YAML | critical | Convert to spaces |
| File path không trong backticks | minor | Wrap trong \`...\` |

---

## 2. VOICE

### Rules per project

| Project | Voice | Xưng hô | CẤM |
|---------|-------|---------|-----|
| **Hermes general** | Casual, professional | "anh" + "em" | "anh ơi" lặp, "mấy con vợ" |
| **Content Creator scripts** | Trung tính, chuyên nghiệp | "các bạn" | "mấy con vợ", "mấy đứa", "mấy chị" |
| **Code comments** | Technical English | n/a | "Vietnamese slang" |
| **Research reports** | Neutral, factual | "người dùng", "khán giả" | First person |

### Detection patterns

**Banned words scan:**
```python
BANNED_PATTERNS = {
    "mấy con vợ": "content-creator",
    "mấy đứa": "all",
    "mấy chị": "all",
    "mấy má": "all",
    "quất một phát": "tiktok",
    "đỉnh nóc kịch trần": "tiktok",
    "delulu is the solulu": "general",
}
```

**Voice consistency:**
- Count 1st person usage (em/anh/tôi)
- Detect register shifts (sudden "mày" trong "anh" conversation)
- Match project voice

### Score

- 10: Perfect — voice đúng 100%
- 7-9: Minor issues (1-2 chỗ bị lẫn)
- 5-6: Mixed voices (khó đọc)
- 0-4: Voice sai hoàn toàn

---

## 3. SOURCES (cho research)

### Minimum requirements

**Mặc định (research):**
- ≥5 nguồn per output
- Mỗi nguồn có: URL + ngày truy cập + tên nguồn
- Đa dạng domain (không chỉ 1 site)

**Factual claims:**
- ≥2 nguồn cho số liệu chính
- Primary source > secondary source
- Ngày truy cập trong vòng 7 ngày (nếu là trending data)

### Source quality tiers

| Tier | Examples | Score |
|------|----------|-------|
| Primary | TikTok Shop product page, official docs, KOL review | 10 |
| Secondary | News articles, blog posts từ known sources | 7 |
| Tertiary | Forum posts, social media comments | 5 |
| Unverified | Random websites, no author | 0 |

### Source checklist

```yaml
- url: "https://..."
  name: "Tên nguồn"
  accessed: "2026-06-16"
  tier: primary | secondary | tertiary
  type: official | kol | review | news | forum
  notes: "Optional context"
```

### Common failures

| Failure | Severity |
|---------|----------|
| Data point không có URL | critical |
| URL trỏ về homepage (không phải article) | warning |
| Ngày truy cập > 7 ngày tuổi | warning |
| Chỉ dùng 1 nguồn cho mọi claim | critical |
| Nguồn là AI-generated (round-robin) | critical |

---

## 4. QUALITY BAR

### Banned patterns

```yaml
chung_chung:
  - "có thể là"
  - "thường thì"
  - "nhiều khi"
  - "một số"
  - "khá nhiều"
  - "khá tốt"
  - "tùy trường hợp"

tu_doan:
  - "em nghĩ là"
  - "theo em thấy"  # OK trong opinion, không OK trong facts
  - "có lẽ"
  - "chắc là"

so_lieu_bia:
  - Bất kỳ con số nào không có nguồn
  - Percentages không có data
  - Rankings không có methodology

template_repeat:
  - Cùng opening hook > 3 lần
  - Cùng closing CTA
  - Cùng paragraph structure
```

### Quality markers (positive)

- ✅ Specific numbers (80%, 1,500 units, etc.)
- ✅ Real examples (named KOL, named product, named place)
- ✅ Dates and timestamps
- ✅ Verifiable claims (URL trỏ về primary source)
- ✅ Trade-offs acknowledged ("nhưng cũng có nhược điểm X")

### Score

- 10: All claims specific + sourced
- 7-9: 1-2 chung chung phrases
- 5-6: Multiple vague claims
- 0-4: Quá nhiều speculation

---

## 5. PROJECT-SPECIFIC RULES

### Content Creator (TikTok)

**7 quy tắc Hiến pháp kênh:**
1. Chỉ nói/review đồ đã dùng thật
2. Mọi video bán hàng phải có ≥1 nhược điểm thật
3. Gắn nhãn tiếp thị liên kết rõ ràng (luật 1/1/2026)
4. Không vượt quá 30 giây
5. Voice: "các bạn" (trung tính, chuyên nghiệp)
6. 3 trụ nội dung: SETUP / EDIT / GEAR REVIEW
7. 70% value : 30% bán hàng

**Forbidden patterns:**
- "quất một phát" (đã OUT)
- "đỉnh nóc kịch trần" (đã OUT)
- Hook cứng nhắc ("đã X là Y")

### Research (general)

- ≥5 nguồn
- Primary source preferred
- Methodology stated
- Confidence level stated (high/medium/low)
- Date accessed cho mọi URL

### Code

- Lint pass
- No secrets in code
- Tests included
- README updated
- Commit message theo convention

---

## 6. ACTIONABILITY

### Checklist

- [ ] Output có next steps rõ ràng?
- [ ] User biết phải làm gì sau khi đọc?
- [ ] Có links/files cần thiết?
- [ ] Có timeline/priority?
- [ ] Có contact/escalation path nếu stuck?

### Actionability levels

| Level | Description | Score |
|-------|-------------|-------|
| Immediate | User có thể act ngay | 10 |
| Clear next step | "Do X, then Y" | 7-8 |
| Vague | "Consider doing X" | 5-6 |
| Informational only | No action required | 0-4 |

---

## Composite Scoring

```python
def compute_score(checks: dict) -> int:
    weights = {
        "format": 0.10,
        "voice": 0.15,
        "sources": 0.25,  # highest for research
        "quality": 0.25,
        "project_specific": 0.15,
        "actionability": 0.10,
    }
    return sum(checks[k] * weights[k] for k in weights)
```

**Verdict mapping:**
- ≥9.0: PASS
- 7.0-8.9: WARN
- 5.0-6.9: FAIL (re-run)
- <5.0: FAIL (reject)

---

## Edge Cases

### Nếu output là empty/error
- Verdict: FAIL
- Score: 0
- Issues: ["No output produced", "Check maker agent logs"]

### Nếu output quá ngắn (< 100 chars)
- Skip auto-check
- Không phải deliverable nặng

### Nếu output là Q&A đơn giản
- Skip auto-check
- Voice check only

### Nếu output có code
- Thêm check: lint pass, no secrets, no PII

---

*See also: [[Loop-Engineering-System]], [[hermes-agent-complete-guide]]*
