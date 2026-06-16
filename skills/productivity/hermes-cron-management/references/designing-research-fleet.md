# Designing a Research Cron Fleet — Step-by-Step

> Proven workflow from Content Creator fleet design (2026-05-02).
> Use when user asks "thiết lập cron jobs để research chủ đề X" hoặc "tạo fleet cron cho niche Y".

---

## Phase 1: Clarify (BẮT BUỘC — không bước qua)

Đừng assume. Hỏi 5 câu tối thiểu:

### Câu 1: Sub-niche cụ thể
- (a) Single niche (chỉ mic thu âm)
- (b) Multiple niche xoay vòng (mic → đèn → gimbal → lens → ...)
- (c) Tất cả, không rotation

→ Nếu (b): xác nhận rotation plan (mỗi ngày trong tuần = 1 niche)

### Câu 2: Audience mục tiêu
Liệt kê 3-5 persona segments. Mỗi persona cần:
- Độ tuổi
- Budget
- Mục đích sử dụng

### Câu 3: Platform priority
- TikTok-first / YouTube-first / 50-50
- Output: video ngắn hay dài?

### Câu 4: Tiêu chí "uy tín" đo bằng gì
- Test thực tế + review từ người mua
- Hoặc: data thị trường + so sánh giá
- Hoặc: KOL uy tín + engagement metrics

### Câu 5: Data sources / Affiliate channels
- Shopee, TikTok Shop, Amazon, Accesstrade, ...
- **Quan trọng:** xác định nguồn nào KHÔNG chặn automation crawl (Shopee OK, TikTok Shop chặn nặng)

---

## Phase 2: Quality Bar Confirmation

| Setting | Default | Lưu ý |
|---------|---------|-------|
| Sources/claim | ≥5 | User có thể yêu cầu ≥10 nếu nghiêm túc |
| Source priority | User-specified | VD: Shopee #1 vì không chặn bot |
| Data freshness | 7 days trending, 30 days policy | |
| Output format | full .md file + Telegram summary | |
| Routing bot | Yes, threshold >10 sản phẩm | Specify bot handle (VD: @Researcher_Clawd_Bot) |

---

## Phase 3: Fleet Design (5-7 jobs)

Phân bổ schedule theo thời gian trong ngày:

| Slot | Job Type | Output |
|------|----------|--------|
| 0:00 - 1:00 | Session/Internal review | Tổng hợp context hôm qua |
| 2:00 - 3:00 | Self-improvement/Backup | Infrastructure |
| 3:00 - 4:00 | Backup + cleanup | Infrastructure |
| 4:00 - 5:00 | Wiki health / Internal audit | Infrastructure |
| 7:00 - 8:00 | **Trending #1** (TikTok Shop) | Top 5 products |
| 7:30 - 8:30 | **Trending #2** (Shopee Affiliate) | Top 5 deals |
| 8:00 - 9:00 | **Trending #3** (YouTube Search) | Top 10 videos |
| 23:00 - 0:00 | **Algorithm watch** (TikTok policy) | Policy update |

Mỗi research job PHẢI có sub-niche rotation theo ngày trong tuần (tránh trùng).

---

## Phase 4: Propose to User

Show bảng trước khi apply:

```
| # | Job | Schedule | Mục đích | Output |
|---|-----|----------|----------|--------|
| 1 | TikTok Shop Trending | 7:00 | Top 5 mic/đèn/gimbal trending | .md + Telegram |
| 2 | Shopee Affiliate | 7:30 | Top 5 deals hot | .md + Telegram |
| ... | ... | ... | ... | ... |
```

Wait for user confirm. Nếu user chỉnh gì → update bảng rồi mới apply.

---

## Phase 5: Apply in Parallel

```python
# Apply song song tất cả jobs
for job in fleet:
    cronjob action='update' job_id=job.id prompt=job.prompt deliver=target schedule=job.schedule
```

**Pitfall — Schedule drift:** Khi rename job (VD: "Hermes Autoresearch" → "TikTok Shop Trending"), PHẢI update `schedule` nếu muốn đổi giờ chạy. Nhiều khi user đổi job name mà quên đổi schedule → cron chạy sai giờ.

---

## Phase 6: Verify

```bash
cronjob action='list'
```

Check:
- Tất cả `deliver` đúng target
- Tất cả `schedule` đúng giờ mới
- Tất cả `prompt_preview` khớp với nội dung đã update

Nếu có job nào sai → `cronjob action='update'` lại, đừng `action='remove'` rồi tạo mới (mất lịch sử).

---

## Phase 7: Save Template

Tạo file `~/.hermes/cron/templates/research-job-template.md` với:
- Mission/Context/Scope/Research Rules/Routing/Deliverable/Anti-patterns/Verification Checklist

Dùng làm base cho fleet sau.

---

## Anti-patterns to Avoid

| ❌ Đừng | ✅ Làm thế này |
|---------|-----------------|
| Assume user muốn "research trending" chung chung | Hỏi 5 câu clarify trước |
| Apply tất cả jobs cùng lúc không confirm | Propose bảng → wait confirm → apply |
| Update prompt mà quên update schedule | Verify schedule sau mỗi update |
| Dùng template cũ không customize | Mỗi job có scope rotation riêng |
| Skip verification | `cronjob list` để confirm |
| Bỏ qua anti-patterns section | Anti-patterns giúp job chạy đúng, không drift |
