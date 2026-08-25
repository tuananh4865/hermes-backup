---
name: deep-research-multi-pillar
description: Deep research workflow cho dự án có nhiều trụ cột (multi-pillar / multi-domain). Dùng khi user yêu cầu "research sâu về X trụ" và cần tổng hợp thành lộ trình/kế hoạch. Song song subagent + fallback khi timeout + ma trận tổng hợp + sắp xếp theo logic người mới.
trigger: Khi user yêu cầu "deep research", "research toàn bộ X trụ", "khai thác sâu chuyên đề có nhiều pillar"
category: research
---

# Deep Research Multi-Pillar Workflow

> **Source pattern:** Tuấn Anh session 2026-06-17 — research 3 trụ cột EDIT + SETUP GÓC QUAY + ÁNH SÁNG cho kênh TikTok giáo dục, kết hợp thành lộ trình 45 ngày.

## Trigger conditions

**Dùng skill này KHI:**
- User yêu cầu "deep research" + danh sách ≥2 chủ đề/trụ cột liên quan
- Cần tổng hợp thành ma trận/kế hoạch hành động (lộ trình, content calendar, roadmap)
- Quy mô lớn: ≥3 file research, mỗi file 30KB+, tổng hợp > 100KB
- Output cần được sắp xếp theo "logic người mới học" (dễ → khó, quen → lạ)

**KHÔNG dùng KHI:**
- Chỉ 1 chủ đề → dùng web search trực tiếp, không cần skill
- Cần fact nhanh (<5 phút) → web search trực tiếp
- User chỉ muốn tóm tắt 1 bài viết → dùng web_extract

## Workflow 5 bước

### Bước 1: Scope (auto-detect khi user đã rõ deliverables)

**Auto-skip confirm** KHI user đã chỉ rõ:
- Số trụ rõ ràng ("4 trụ", "3 pillar")
- Source minimum rõ ràng ("200+ URLs", "trên 100 nguồn")
- Domain rõ ràng (tên lĩnh vực cụ thể: "tâm lý bán hàng", "viral mechanics")
- Channel hints ("báo + X/Twitter", "academic papers only")

**CẦN confirm** KHI:
- "Research về X cho anh" không rõ số trụ
- Không biết cần depth hay breadth
- Output format chưa rõ (báo cáo? video script? checklist?)
- Nhiều cách hiểu khác nhau

**Verified case (2026-07-07, session "tìm và học về nghệ thuật bán hàng..."):** User đã chỉ rõ 4 trụ + 200+ URLs + báo + X/Twitter. Em skip confirm, dispatch 4 subagents ngay, không waste 30s hỏi lại. Anh escalate-style khi đã clear deliverables = muốn execute, không muốn clarify.

**Lý do confirm-skip:** Tránh research 4 trụ nhưng user chỉ cần 2. Nhưng nếu user đã rõ → đi thẳng vào Bước 2.

### Bước 2: Launch song song subagent

Dùng `delegate_task` với batch mode:

**Concurrent limit:**
- 3 subagents = default (theo config `delegation.max_concurrent_children`)
- 4-5 subagents = OK nếu tasks độc lập + không cần output của nhau
- 6+ = split thành 2 waves

**Verified case (2026-07-07, session "nghệ thuật bán hàng"):** Em dispatch 4 subagents song song (trụ 1: sales, trụ 2: crowd, trụ 3: consumer, trụ 4: behavioral) → cả 4 chạy OK, không queue. Tasks độc lập hoàn toàn (mỗi trụ research 1 domain khác nhau, output file khác nhau). Khi tasks độc lập → parallel scale up OK, không cần giới hạn 3.

**Khi nào KHÔNG scale up:**
- Tasks có dependency (B cần output của A)
- Tasks share state/files (cùng ghi vào 1 file)
- Tasks cùng hit rate-limited API (vd: 4 subagents cùng search Google → quota)

```
delegate_task(tasks=[
    {goal: "Deep research TRỤ 1: ...", context: "..."},
    {goal: "Deep research TRỤ 2: ...", context: "..."},
    {goal: "Deep research TRỤ 3: ...", context: "..."},
    {goal: "Deep research TRỤ 4: ...", context: "..."}  // OK nếu độc lập
])
```

**Mỗi subagent PHẢI có trong context:**
- Background dự án + đối tượng + mục tiêu
- Danh sách cụ thể cần tìm (8-10 items, có số liệu)
- Output format (markdown size, sections bắt buộc)
- Quy tắc: KHÔNG bịa số, có trích dẫn nguồn URL + ngày
- Đường dẫn file output

### Bước 3: Handle timeout (CRITICAL)

**Subagent có thể timeout 1/3 do web search chậm.** Đây là chuyện BÌNH THƯỜNG, không phải fail.

**Khi timeout:**
1. KHÔNG hủy các subagent còn lại
2. **VERIFY file thực tế đã được ghi TRƯỚC KHI retry** (xem Verify Command bên dưới)
3. Nếu CHƯA ghi → restart subagent đó (KHÔNG dùng web_extract, chỉ dùng mcp_MiniMax_web_search)
4. Nếu ĐÃ ghi → chấp nhận, dùng kết quả có

**Pitfall:** web_extract hay timeout 600s vì backend limit. LUÔN chỉ định "chỉ dùng mcp_MiniMax_web_search với 8-10 query chất lượng, lấy snippet + description + title thay vì full page extract" trong context của subagent.

### 🚨 Verify Command — timeout ≠ file không tồn tại (Pitfall #7, verified 2026-06-25)

**Vấn đề thực tế:** Sub-agent báo `status=timeout, api_calls=25, 600.09s` → parent tưởng mất, retry ngay. Nhưng file 35KB đã được ghi xong trước khi timeout. Retry = waste 10 phút + duplicate content.

**Verify command (chạy NGAY khi sub-agent timeout):**

```bash
# 1. Check file exists + size (size > 0 = sub-agent đã ghi)
ls -la /Volumes/Storage-1/Hermes/wiki/{path}/{expected-filename}.md

# 2. Check content actually there (frontmatter + sections)
head -30 /Volumes/Storage-1/Hermes/wiki/{path}/{expected-filename}.md

# 3. Count sections + URLs (sanity check chất lượng)
grep -c "^## " /Volumes/Storage-1/Hermes/wiki/{path}/{expected-filename}.md
grep -c "http" /Volumes/Storage-1/Hermes/wiki/{path}/{expected-filename}.md

# 4. Compare với sibling files (nếu có) để estimate size chuẩn
wc -l /Volumes/Storage-1/Hermes/wiki/{path}/sibling-*.md
```

**Decision matrix:**

| Verify result | Action |
|---------------|--------|
| File KHÔNG tồn tại (ls fail) | Restart sub-agent với scope GIẢM (xem Scope Rule bên dưới) |
| File < 1KB (chỉ có YAML header) | Restart sub-agent |
| File 1-5KB (partial) | Patch gaps manually (đọc file → identify missing sections → viết thêm) |
| File ≥ expected size + content đầy đủ | **CHẤP NHẬN, KHÔNG RETRY** — sub-agent hoàn thành công việc trước khi API timeout báo cáo |

**Verified case (2026-06-25, session psychology-viral-content):** Sub-agent "Hook Psychology" báo timeout 600s với 25 API calls. Verify `ls -la` → file 35,360 bytes (35KB) đã có. `head -40` → YAML frontmatter + Section 1 (Cognitive Load Theory) + Nature 2025 citations đầy đủ. **Không retry, dùng luôn.** Retry với scope nhỏ hơn chỉ cần khi file thực sự thiếu.

### Scope Rule — tránh timeout do quá nhiều API calls (Pitfall #8, verified 2026-06-25)

**Nguyên tắc:** Mỗi sub-agent PHẢI có `max API calls ≤ 15`. Nếu task scope yêu cầu >15 items × sources, CHIA NHỎ.

**Ngưỡng timeout quan sát được:**
- 8-10 API calls → an toàn, thường xong 8-10 phút
- 15-20 API calls → ranh giới, có thể timeout
- 25+ API calls → **gần như chắc chắn timeout 600s**

**Scope sizing guide:**

| Sub-agent task scope | Max API calls | Risk timeout |
|----------------------|---------------|--------------|
| 5-7 items × 2 sources/item | 10-14 | Thấp |
| 8-12 items × 2-3 sources/item | 18-25 | Trung bình |
| 12+ items × 3+ sources/item | 30+ | **Cao** |

**Khi task scope >20 items:** CHIA thành 2-3 sub-agents nhỏ hơn (3-4 items each), hoặc giảm sources/item xuống 1.

**Anti-pattern:** "Research 12 cognitive biases với mỗi cái 2 studies + 3 sources = 60+ API calls" → timeout guaranteed. Fix: "Research 12 principles với mỗi cái 1 study + 1 source = 24 API calls" vẫn risk, tốt hơn là "6 principles × 2 sources = 12 API calls" (chia thành 2 sub-agents).

**Retry với scope GIẢM khi file không tồn tại:**
- Lần 1: scope đầy đủ → timeout
- Lần 2 (retry): scope GIẢM 50% + CHỈ DÙNG `mcp_MiniMax_web_search` (KHÔNG `web_extract`) + CHỈ viết từ knowledge đã có (Wikipedia URLs có sẵn), KHÔNG research thêm
- Lần 3 (nếu vẫn fail): bỏ qua pillar đó, ghi note trong synthesis "pillar N: data thiếu do timeout, cần research riêng"

### Bước 4: Tổng hợp ma trận (sau khi tất cả subagent xong)

Tạo file tổng hợp (file `00-TONG-HOP-...md`):
- Tóm tắt key insights từ mỗi trụ
- Bản đồ 3 trụ (visual diagram)
- Ma trận content (số lượng kịch bản × trụ × giai đoạn)
- KPI checkpoints
- Risks & mitigations
- Action items ngay

### Bước 5: Sắp xếp theo logic người mới (BẮT BUỘC)

User thường muốn output cuối = lộ trình/kế hoạch, không phải research dump.

**Logic sắp xếp (5 giai đoạn mẫu):**
1. **GĐ 1 (1-7 ngày):** Làm quen — 1 video/task/ngày, chỉ 1 trụ nền tảng
2. **GĐ 2 (8-14):** Mở rộng — 2 task/ngày, thêm trụ 2
3. **GĐ 3 (15-21):** Tăng tốc — 2 task/ngày, thêm trụ 3
4. **GĐ 4 (22-35):** Vào nhịp — 2 task/ngày, kết hợp cả 3
5. **GĐ 5 (36-45):** Thành thói quen — 2-3 task/ngày + cá nhân hóa

**Nguyên tắc sắp xếp:**
- Trụ nào dùng cho MỌI thứ → học trước (VD: EDIT dùng cho mọi video)
- Trụ nào thấy kết quả tức thì → học tiếp (motivation cao)
- Trụ nào cần material đã có → học cuối
- Volume: tăng dần theo giai đoạn (1 → 2 → 3 task/ngày)
- Xen kẽ F-series (câu chuyện cá nhân) từ giai đoạn 3+

### Bước 6: Update project artifacts

- Update CHANGELOG của project
- Update hub.md (link tới file mới + brief description)
- Update memory (decision-style preference nếu có)
- (Optional) Update wiki index.md nếu là project lớn

### Bước 7: ⚠️ DELIVER QUA TELEGRAM — không chỉ ghi file (Pitfall #9, verified 2026-06-25)

**Vấn đề thực tế:** Tuấn Anh đang làm việc qua Telegram trên điện thoại, KHÔNG ngồi trước Mac. Khi em save file vào `/Volumes/Storage-1/Hermes/wiki/concepts/` rồi báo "xong research 5 file" → anh KHÔNG có cách nào đọc file từ Telegram. Anh phải nhắn lại *"không gửi file qua tele cho anh đọc thì làm sao anh đọc được!!"*

**Rule MỚI (BẮT BUỘC khi user đang ở Telegram/remote):**
1. **Sau khi research xong → KHÔNG chỉ báo "file đã save"** mà phải **EMBED content trực tiếp trong reply Telegram**
2. **Cấu trúc reply:**
   - **Phần A:** Tóm tắt 1-paragraph (master insight / one-liner)
   - **Phần B:** Synthesis framework (bảng + checklist) — Markdown tables, headers, code blocks đều OK trên Telegram
   - **Phần C:** Liệt kê file paths để anh bookmark/lưu trên Mac sau
   - **Phần D:** Nếu có >20KB content → chia thành 2-3 reply, mỗi reply ≤ ~4KB Markdown (Telegram render limit)
3. **Sau khi embed xong → check `MEDIA:` tag cho file binary** (nếu user cần file PDF/MD để lưu): `MEDIA:/Volumes/Storage-1/Hermes/wiki/concepts/file.md`
4. **Telegram hỗ trợ Markdown** — leverage: `**bold**`, `*italic*`, `[links](url)`, code blocks, tables (pipe syntax), task lists. KHÔNG cần escape.

**Anti-pattern cần tránh:**
- ❌ Save 5 file rồi báo "Done, file ở /Volumes/.../concepts/X.md, /Y.md, /Z.md" — user đọc được KHÔNG? KHÔNG.
- ❌ Chỉ gửi tóm tắt ngắn kiểu "5 file research, 152 KB, 176 citations" — không embed framework
- ❌ Gửi raw markdown từ file (quá dài, Telegram cắt 4096 chars)
- ✅ **ĐÚNG:** Reply 1: Master framework embed đầy đủ + Reply 2: Deep-dive file 1, 2... + Reply 3: File paths cho bookmark

**Verified case (2026-06-25, session psychology-viral-content):** Em save 5 file vào `/Volumes/Storage-1/Hermes/wiki/concepts/` tổng 152 KB. Anh phản hồi *"anh đang làm việc với em trên telegram mà có phải trên máy mac của anh đâu!"*. Fix: phải reply Master Framework (~12 KB) embed đầy đủ trong Telegram, chia làm 2 reply nếu cần, KÈM file paths để anh có thể tự mở Mac xem sau.

**Channel-aware rule:**
- Nếu user dùng **Telegram** (anh Tuấn Anh): embed content trong reply, KHÔNG chỉ save file
- Nếu user dùng **terminal/cli**: ok ghi file + `cat` summary
- Nếu user dùng **Obsidian GUI**: ok ghi file + `open` command

**Cách kiểm tra user đang ở channel nào:**
- Xem session metadata `platform: telegram` → Telegram mode
- User gửi message qua Telegram = embed content
- User gửi message qua Hermes CLI = save file OK

## Decision: Subagent vs In-line Batch (Pitfall #11, verified 2026-07-07)

**Khi nào dùng `delegate_task` (PILLAR MODE - default):**
- Research rộng, không giới budget API calls
- User muốn nhiều subagent chạy độc lập
- File output ≥30KB mỗi pillar
- Scope > 14 items × multiple sources

**Khi nào dùng IN-LINE BATCHED CALLS (BOUNDED MODE - new):**
- User đã chỉ rõ budget: "max 15 API calls", "≤10 queries", budget cứng
- User đã liệt kê 8-14 sub-topics cụ thể trong prompt
- File output muốn 1 file duy nhất tổng hợp tất cả sub-topics (KHÔNG phải tách thành 4 files riêng)
- Output path là file wiki concept cụ thể (KHÔNG phải `Research/<date>/`)

**Verify case (2026-07-07, Trụ 1 "Sales psychology + classic sales art"):** *(FIRST in-line batched case — session of origin)*
- User constraint: max 15 API calls, chỉ `mcp__MiniMax__web_search`, output single file `/Volumes/Storage-1/Hermes/wiki/concepts/research-sales-psychology-2026-07-07.md`
- 7 sub-topics + 6 specific Twitter creators (@AlexHormozi, @JFischerOfficial, @KevinDurant, @SamOvens, @DanLokOfficial, @DonaldMiller)
- Required: ≥50 URLs, 25–40 KB target file size, YAML frontmatter, paraphrase <15 từ/source, citation format `[N] Author. Title. Source. Date. URL`
- **Decision: chạy in-line, 3 batch parallel (5 + 4 + 5 = 14 calls), 1 file output** → hit 65 URLs / 35.8 KB / 7 sections + exec + application + insights + 2 appendices, budget còn 1 call dự phòng
- **1 query hit 1027** (`Bencivenga "Bullseye" copywriting`) — KHÔNG có `site:` operator, chỉ là keyword combination bị flag. Fix: chuyển sang dialogue hoàn toàn dựa trên widely-documented industry knowledge, ghi gap acknowledgement vào Appendix A. Xem [[mcp-search-workarounds]] để biết operator-less 1027 pattern.
- **KEY INSIGHT (Pillar 1 — VERIFIED)** — Trụ này khẳng định bổ sung rule:
  - Khi user phân biệt rõ `input budget` vs `output budget` (cụ thể: max 15 INPUT calls, nhưng 50+ URLs OUTPUT), **KHÔNG scale agent output bằng cách delegate** — vẫn dùng in-line batched calls và leverage **cross-source citation**: mỗi Organic search result ≈ 1 URL. 5 in-line calls × ~5 results/call = ~25 raw URLs; user target 50 đạt được tự nhiên vì miniMax search thường trả 8-10 results/call.
  - **Single-query hit rate vs multi-query coverage**: 1 query strategic ("Cialdini 7 principles") = 9 results mỗi nội dung = cite từng source. KHÔNG cần 14 query riêng cho 14 sub-topic.
  - **Appendix A transparency rule**: nếu query fail (1027) hoặc creator có search-hits thin (Twitter handles ít hit-able), KHÔNG bịa — ghi gap trong Appendix A, dùng documented industry knowledge paraphrase-only. Verify case: trụ này ghi thẳng "Bencivenga: section written from widely-documented industry knowledge, paraphrase only" — không bao giờ fake URL.
- Output → `references/session-2026-07-07-tru1-sales-psychology.md`

**Verify case (2026-07-07, Trụ 2 "Tâm lý học đám đông + Viral mechanics"):**
- User constraint: max 15 calls, chỉ `mcp__MiniMax__web_search`, output `/Volumes/Storage-1/Hermes/wiki/concepts/research-crowd-psychology-2026-07-07.md`
- 14 sub-topics được liệt kê explicit trong prompt
- **Decision: chạy in-line, 2 batch parallel (8 calls + 7 calls), 1 file output** → xong trong ~2 round trips, không cần delegate_task
- Kết quả: 56 URLs, 18 mechanisms, 5 master insights — đạt mọi yêu cầu user

**Anti-pattern (verify bị fail):**
- ❌ Tự động dispatch 14 subagents mỗi cái search 1 topic khi user đã nói "max 15 calls TỔNG" → vượt budget 14 lần
- ❌ Bỏ constraint "không delegate", vẫn delegate vì skill nói "default là delegate" → user phải nhắc lại

**Rule:** Default vẫn là `delegate_task` cho research rộng, NHƯNG ngay khi user đưa hard budget (≤20 calls) HOẶC chỉ định single output path → IN-LINE BATCHED CALLS, không delegate.

## Master Framework Synthesis (Step 4.5 — Pitfall #12, verified 2026-07-07)

**Khi nào cần synthesis file riêng (ngoài N file trụ):**
- User yêu cầu research về multi-domain knowledge mà cần 1 unified action framework
- Kết quả của các trụ KHÔNG đứng riêng, mà phải compose thành công cụ dùng được
- VD verified: 4 trụ (sales + crowd + consumer + behavioral) → 1 master framework dùng cho content TikTok bán hàng

**Master Framework structure (8 sections, mỗi section ≤ 2KB Markdown):**

| Section | Purpose | Source |
|---|---|---|
| 1. N-trụ table (1 trụ/dòng) | Quick overview | Subagent summary |
| 2. Nền tảng khoa học (ASCII diagram) | Visual mental model | Synthesis |
| 3. **N "armed" principles** (N=7 verified) — mỗi principle = synthesis từ ≥2 trụ | Core actionable insights | Cross-pillar |
| 4. **Content blueprint** (timeline phases × principles) | Action template | Synthesis |
| 5. **Customer journey** (5-stage table) | Where principles apply | Trụ 3 + 4 |
| 6. **90-day action plan** (theo tuần) | Execute immediately | Synthesis |
| 7. **N "DON'Ts"** (anti-patterns) | Failure avoidance | Cross-pillar |
| 8. **1-line summary** | Memorize | Synthesis |

**Anti-pattern cần tránh (Pitfall #12):**
- ❌ Synthesis chỉ dựa vào subagent summary text (5 insights/trụ) → quá mỏng, không đủ actionable
- ✅ **ĐÚNG:** Sau khi N subagents xong → ĐỌC LẠI N FILE thật (grep `## Top 5` section) → cross-pollinate principles từ ≥2 trụ → mới viết master framework
- Lý do: Subagent summaries dài 100-200 dòng, parent đọc qua trong 10s. Synthesis chất lượng yêu cầu đọc kỹ `## Top 5 Master Insights` section từ MỖI file.

**Verified case (2026-07-07, sales-psychology 4-trụ):**
- 4 files returned (35KB / 23KB / 27KB / 32KB)
- Em đọc 4 files bằng regex `## \d+\.?\s*.{0,80}(Master Insights|Top 5|Key Insights)` → extract top 5 từ mỗi file
- Cross-pollinate: principles xuất hiện ở ≥2 trụ → promote lên "armed principle" trong master framework
- Ví dụ verified: "Hook 3s thắng hay thua" (Trụ 3 System 1 + Trụ 1 AIDA) → Principle #1. "Free > discount" (Trụ 4 Ariely + Trụ 1 Reciprocity) → Principle #2.
- Kết quả: 7 armed principles, mỗi cái = synthesis từ ≥2 trụ, content blueprint 11 phases, 90-day plan, 319 unique URLs tổng.

**Verify command sau synthesis:**
```bash
# Count wikilinks giữa master file + N trụ files
grep -c "research-" /path/to/master-framework.md  # phải có ≥N references
# Cross-check: principle #N trong master → tìm được trong ≥2 source files
grep -l "loss aversion" /Volumes/Storage-1/Hermes/wiki/concepts/research-*.md  # phải match ≥2 files
```

## Citation Discipline (research output format convention)

Khi user yêu cầu research output có format citations rõ ràng:

**Source citation format chuẩn:**
```
[N] Author. Title. Source. Date. URL
```
- `[N]` = số thứ tự, dùng trong toàn bài khi reference (ví dụ: `[1]`, `[5][6]`)
- `Author` = tác giả chính hoặc "Wikipedia" nếu không rõ
- `Title` = tiêu đề bài viết
- `Source` = tên publication/site (Wikipedia, SSRN, Nature, ...)
- `Date` = ngày publish/accessed (verified: 2026-07-07)
- `URL` = link đầy đủ

**Quote/paraphrase rule:**
- Mỗi quote/paraphrase **≤ 15 từ/source** (verified: standard pattern 2026-07-07)
- Nếu cần dài hơn → viết paraphrase của mình, đặt `[N]` ở cuối

**Output location:** Toàn bộ URL list đặt ở **CUỐI file** dưới heading "Nguồn tham khảo" — KHÔNG xen vào body. Body chỉ dùng inline reference `[N]`.

**YAML frontmatter chuẩn cho wiki/concepts/*.md:**
```yaml
---
title: "<tên trụ/topic>"
date: YYYY-MM-DD
author: "Hermes Agent (subagent/method)"
topic: <topic-slug>
tags: [<tag1>, <tag2>, <tag3>]
target_user: "<ai sẽ dùng file này>"
total_urls: <number>
total_mechanisms: <number>
master_insights: <number>
source_format: "[N] Author. Title. Source. Date. URL"
---
```

**Top-of-reply counts (synthesis convention):**
User luôn muốn reply bắt đầu với:
```
- **Tổng URLs:** <number>
- **Tổng mechanisms identified:** <number>
- **Master insights:** <number>
- **API calls used:** <number>/<budget>
- **File created:** `<path>`
```
Đặt NGAY đầu reply (sau khi write_file xong) — user scan trong 3s có overview. Verified case 2026-07-07 — pattern này được user explicit yêu cầu trong prompt.

## Common pitfalls

1. **Quên confirm scope trước** → research 3 trụ nhưng user chỉ cần 1
2. **Dùng web_extract trong subagent** → timeout toàn bộ batch
3. **Hủy các subagent khi 1 timeout** → mất 30+ phút research đã chạy
4. **Output research dump** không qua bước 5 → user phải tự sắp xếp
5. **Không update CHANGELOG/hub.md** → user quên mất có file mới
6. **Không có checkpoint KPI** → user không biết đang ở đâu
7. **Timeout ≠ file không tồn tại** (verified 2026-06-25) → retry khi file đã ghi xong, waste 10 phút. Fix: chạy `ls -la` + `head -30` + `wc -l` NGAY khi sub-agent timeout. Nếu file ≥ expected size + content đầy đủ → CHẤP NHẬN, không retry. Chi tiết: xem Bước 3.
8. **Scope rộng → timeout** (verified 2026-06-25) → task "12 items × 2-3 sources = 24-36 API calls" gần như chắc chắn timeout 600s. Fix: chia sub-agent scope ≤ 15 API calls, hoặc chia thành 2-3 sub-agents nhỏ. Chi tiết: xem Scope Rule.
9. **Telegram embed rule** (verified 2026-06-25) — embed content trong reply, không chỉ save file. Chi tiết: xem Bước 7.
10. **Poll subagent status instead of waiting** (verified 2026-07-07) → sau khi `delegate_task` xong, KHÔNG gọi `process.poll()` hoặc sleep loop để check. Background mode = kết quả tự re-enter conversation khi tất cả xong. Poll = waste tool calls + gây flood control. Fix: dispatch xong → update todo → báo user "đang đợi kết quả" → đợi. Chi tiết: xem Bước 8.
11. **Tự động delegate khi user đã set hard API budget** (verified 2026-07-07, Trụ 2 + Trụ 4) → user constraint max 15 calls nhưng skill mặc định dispatch 14 subagents → vượt budget 14×. Fix: khi user đưa hard budget (≤20 calls) HOẶC chỉ định single output path → IN-LINE BATCHED CALLS, không delegate_task. Chi tiết: xem "Decision: Subagent vs In-line Batch" + 2 session references (Trụ 2 + Trụ 4).

### Bước 8: KHÔNG POLL SUBAGENT (Pitfall #10, verified 2026-07-07)

**Anti-pattern:**
```python
delegate_task(...)  # returns immediately
while not done:
    process.poll()  # ❌ waste tool calls
    sleep(30)
```

**ĐÚNG:**
```python
delegate_task(...)  # returns ngay, count=4
# CẬP NHẬT TODO: "đợi kết quả"
# BÁO USER: "đang chạy 4 subagent, sẽ có kết quả trong X phút"
# KHÔNG LÀM GÌ — kết quả sẽ tự re-enter conversation
```

**Lý do:** `delegate_task` background mode = system tự quản lý lifecycle. Khi tất cả subagents xong → kết quả re-enter như 1 message mới. Poll chỉ waste tool calls + gây context overflow.

**Edge case:** Nếu user yêu cầu wait chủ động (vd: "em đợi xong rồi báo anh") → vẫn không poll, vẫn đợi background message. "Đợi" = "đợi tự nhiên", không phải "poll actively".

## Output checklist

Mỗi lần chạy workflow này, đảm bảo:
- [ ] ≥3 file research riêng (mỗi file 30KB+)
- [ ] 1 file tổng hợp ma trận (file 00)
- [ ] 1 file lộ trình/kế hoạch (file 01) — có logic cho người mới
- [ ] CHANGELOG.md updated
- [ ] hub.md (hoặc index) updated với link mới
- [ ] Memory updated với user preference mới (nếu có)
- [ ] Có checkpoint KPI rõ ràng
- [ ] **NẾU user ở Telegram: embed Master Framework + checklist trong reply, không chỉ save file** (xem Bước 7)

## Verification

Sau khi deliver, check:
- File size: mỗi file research ≥ 30KB?
- Subagent đã cite nguồn URL + ngày đầy đủ?
- Lộ trình có dễ→khó, 1→2 video/ngày progression?
- User hiểu phải làm gì NGÀY MAI cụ thể không?

## Related

- [[mcp-search-workarounds]] — khi mcp_MiniMax_web_search fail
- [[social-media-research]] — research TikTok/social platform cụ thể
- [[llm-wiki]] — nếu cần lưu findings vào wiki KB

## Session references

Detailed verification + lesson captures from real sessions:

- `references/session-2026-06-17-content-creator.md` — Original 3-pillar case (delegated subagent mode, EDIT + SETUP + ÁNH SÁNG)
- `references/session-2026-07-07-tru1-sales-psychology.md` — **First** verified case of in-line batched mode (Trụ 1, sales psychology, 14 calls → 65 URLs, hit 1027 mid-session with no operator — see [[mcp-search-workarounds]] for the operator-less failure pattern)
- `references/session-2026-07-07-tru2-crowd-psychology.md` — Second verification of Pitfall #11 (in-line batched mode, viral mechanics)
- `references/session-2026-07-07-behavioral-science-pillar4.md` — Second verification of Pitfall #11 (in-line batched mode, 19 topics in 15 calls)
- `references/session-2026-07-07-sales-psychology-4-pillars.md` — NEW: 4-pillar parallel dispatch + Master Framework Synthesis (Pitfall #12, 319 URLs in 4m24s, 4 research + 1 master framework)
- `references/session-2026-07-11-youtube-niche-benchmark.md` — NEW VARIANT: single-niche benchmark → single consolidated strategy report (NOT multi-pillar). Cross-vertical format import (badminton channel researched against edutainment formula); 2-tier structure (primary niche deep + adjacent proven-format benchmark); 30/60/90 roadmap template. Trigger: "research top [N] channels of [niche] for [purpose]".

## Niche Subsidiary Product Catalog Variant (NEW, verified 2026-07-16)

A new sub-pattern emerged distinct from primary trend research: **catalog research** for TikTok Shop niche subsidiary products (companion/secondary items, not headline trending products).

**Trigger:** User provides a list of 3-7 niche product groups with optional brand hints, asks for JSON output where each product carries ≥1 citation URL. Examples:
- "3 nhóm: bộ vệ sinh ống kính DJI Pocket 3 (brand PocketBar TQ?), đèn LED dán tường mini remote, Lemony Body Mist (brand nào?)"
- "Phụ kiện cho DJI Pocket 3: filter, ốp, gimbal lock, microphone — JSON có giá + brand + link Shopee"

**Differs from primary trend research (table):**

| Aspect | Primary trend research | Niche subsidiary catalog |
|---|---|---|
| Products per group | 1-2 hero products | 4-6 alternatives per group |
| Citations per product | 5-15 (deep) | 1-3 (light) |
| Total product count | 3-5 | 12-20 |
| Output structure | Per-group deep markdown file | 1 JSON file with `groups[].products[]` |
| Synthesis needed | Yes (master framework) | No (catalog only) |
| API budget | 30-50 calls | 15-25 calls |
| Risk of brand mismatch | Low | **HIGH** (Pitfall #19) |

**Workflow (5 steps):**

1. **Brand-name verification first** — for any brand hint in the brief, run `mcp__MiniMax__web_search("<brand> <category>")` early. If returns 0 hits OR returns off-category product, see [[mcp-search-workarounds]] Pitfall #16 (typo) or Pitfall #19 (category mismatch). Document mismatch with `note_<brand>_brand` field at top of JSON.
2. **Parallel backend mix** — dispatch both `mcp__MiniMax__web_search` (for blogs/news/VN sources) and `mcp__exa__web_search_exa` (for spec tables + structured data) in same round-trip. Avoid `web_extract` (DuckDuckGo backend fails consistently).
3. **Group-by-group research, not parallel subagents** — since each group only needs 4-6 products with light citations, in-line batched calls beat `delegate_task`. Subagent overhead > research work for this size. Hit ≤20 calls per group.
4. **JSON output schema** — verify with this structure:
   ```json
   {
     "research_date": "YYYY-MM-DD",
     "note_<brand>_brand": "...",          // optional, document mismatches
     "groups": [
       {
         "group": "Tên nhóm",
         "products": [
           {
             "name": "...",
             "brand": "...",
             "origin": "...",
             "specs": {...},
             "price_vnd": <number>,
             "price_range_vnd": "...",
             "usp": "...",
             "competitors": ["..."],
             "citations": ["https://..."]   // ≥1 URL REQUIRED
           }
         ]
       }
     ],
     "summary_insights": ["..."]
   }
   ```
5. **Final verification** — run `python -c "import json; d=json.load(open('output.json')); [assert len(p['citations'])>=1 for g in d['groups'] for p in g['products']]"` to enforce citation rule. Also count total citations: should be ≥ total products × 1.

**Verified case (2026-07-16):** 3 groups × 5-6 products × 1-7 citations = 13 products + 60+ citations, 19.9 KB JSON. Triggered Pitfall #19 (PocketBar = Swedish crowbar, not camera cleaning; "Lemony" = variant name across multiple brands). Mismatch documented in `note_pocketbar_brand` + `note_lemony_brand` fields. Final output substituded 6 alternatives for PocketBar (Lenspen, VSGO, FB generic, Hoodman, Zeiss) + 6 Lemony alternatives (Sapital Lemony, BODYMISS Funky Fresh, Sol de Janeiro Limonada Gelada, Lush Lemony Flutter, VS Capri Lemon Leaves, BBW White Citrus). User received actionable catalog with every product ≥1 verified URL.

**Anti-patterns:**
- ❌ Silently substituting the off-category brand result (e.g. "PocketBar = mini crowbar" delivered as answer) — user gets wrong product.
- ❌ Delegating to 3 subagents for 3 groups — overhead exceeds work; in-line batched is faster.
- ❌ Skipping citation verification — output JSON with `citations: []` breaks user's hard requirement.
- ❌ Heavy synthesis (master framework, 5-stage progression) — over-engineering for a catalog. Output stays a JSON array, not a markdown report.
