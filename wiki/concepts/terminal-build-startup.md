---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 deep-research (extracted)
  - 🔗 autonomous-wiki-agent (extracted)
  - 🔗 agentic-workflows-agentic-graphs (extracted)
  - 🔗 terminal-build-workflow (extracted)
relationship_count: 4
---

# Build Startup bằng Terminal

> Nguồn: Bài viết anonymous trên X/Twitter về việc dùng coding agents trên Terminal để build startup từ ý tưởng đến MVP có người dùng trong 1 ngày.

---

## Case Study: Kyma API

**Timeline:**
- **12h55 trưa thứ 7**: Commit đầu tiên
- **Tối hôm đó**: API server, landing page, dashboard, auth, docs 28 trang, Stripe, referral system
- **Ngày thứ 2**: 700+ users đăng ký
- **Ngày thứ 3**: 7,900 users, 63.7M tokens
- **4 ngày**: 280 commits, build một mình

---

## Core Flow

```
IDEA → RESEARCH (15 phút) → SDD → BUILD → DEPLOY → ITERATE
```

### Phase 1: Research (30% thời gian)

**Mục tiêu:** Hiểu thị trường, đối thủ, khoảng trống

1. Phân tích đối thủ: ai đang làm gì, mô hình kinh doanh, điểm yếu
2. Xác định USP (Unique Selling Point)
3. Tìm khoảng trống chưa ai làm

**Output:** Bản phân tích đủ chi tiết để ra quyết định

> "15 phút có bản phân tích đủ chi tiết để ra quyết định"

### Phase 2: SDD - System Design Document (Bước quan trọng nhất)

**Mục tiêu:** Thiết kế hệ thống hoàn chỉnh TRƯỚC khi build

1. Kiến trúc hệ thống
2. Database schema
3. API endpoints
4. Tech stack
5. Fallback strategies

**Output:** SDD rõ ràng → agent build nhanh và đúng

> "Có SDD rõ ràng thì agent build nhanh và đúng. Không có thì nó build lung tung."

### Phase 3: Build

**Mục tiêu:** Đưa SDD cho agent, để nó đọc hiểu và build

1. Backend (Bun/Next.js)
2. Frontend (Dashboard, landing page)
3. Auth, thanh toán, referral
4. Rate limiting
5. Fallback 4 lớp

**Nguyên tắc:**
- SQLite ban đầu → migrate khi cần scale
- Build tất cả trong 1 buổi chiều

### Phase 4: Deploy

**Mục tiêu:** Lên production nhanh nhất

1. Push lên Railway + Vercel
2. Config domain
3. SSL tự động
4. Docs trên Mintlify

> "Toàn bộ trên Terminal, không mở trình duyệt"

### Phase 5: Iterate

**Mục tiêu:** Fix nhanh, launch sớm

1. Monitor error rate
2. Fix ngay trên production
3. Email outreach cho power users

> "49% error rate ngày đầu nghe kinh, nhưng nhờ vậy mình biết provider nào không ổn định ở quy mô thật"

---

## Key Principles

### 1. Research quyết định 80% kết quả

```
Research 30% thời gian → 80% kết quả
Nếu không phân tích đối thủ trước → build sai hướng hoàn toàn
```

### 2. Launch sớm > Launch hoàn hảo

- Error rate ngày đầu = 49% → vẫn launch
- Fix trên production (48 commits/ngày)
- Ngày thứ 3: error rate = 0%

### 3. Terminal = Context switching gần bằng 0

```
Research → Code → Deploy → Email → Fix bug (lúc 2h sáng)
Tất cả trong 1 cửa sổ Terminal
```

### 4. AI = Builder, Human = Decision Maker

| Human làm | AI làm |
|-----------|--------|
| Chọn thị trường | Research theo chỉ đạo |
| Xác định USP | Build theo SDD |
| Quyết định pivot | Deploy, fix bugs |
| Chọn feature nào bỏ | |

---

## Karpathy's Wisdom

> "Thay vì chia sẻ code, hãy chia sẻ ý tưởng. Trong thời đại AI agents, mỗi người tự build phiên bản riêng từ cùng một ý tưởng."

**Điều này có nghĩa:**
- Không có repo/template chuẩn
- Chỉ có flow
- Ai cũng build từ cùng ý tưởng nhưng output khác nhau

---

## Áp dụng cho công việc của chúng ta

### Current Flow (Morning Ritual)
```
Research → Plan → Execute
```

### Enhanced Flow (Terminal Startup Method)
```
1. Deep Research (15-30 phút)
   → Phân tích topic
   → Xác định insights
   → Tìm gaps

2. SDD/Wiki Structure
   → Viết SPEC cho task
   → Xác định dependencies
   → Chunk thành steps

3. Execute với delegate_task
   → Agent build theo spec
   → Monitor progress
   → Fix issues ngay

4. Deploy/Release
   → Commit + push
   → Update wiki
   → Report results
```

---

## Related

- [[deep-research]] — Research methodology
- [[autonomous-wiki-agent]] — Agent execution framework
- [[agentic-workflows-agentic-graphs]] — Node-based workflow patterns
- [[terminal-build-workflow]] — Flow cụ thể cho công việc
