# Kon Tum Pasta Shop — Research Findings (29/07/2026)

> Case study: Anh asked "lên plan làm tiệm bán mì Ý cho anh!" với context "ở Kon Tum Việt Nam". Research-first + clarifying-questions workflow validated. Full findings file: `wiki/projects/mi-y-kontum-research/research/01-kontum-market-overview.md`.

## Why this is a reference

This case demonstrates the **"lên plan X" → research + clarify + THEN plan** workflow that was added to the skill on 2026-07-29. Anh's literal request: *"Sau khi research thu thập thông tin xong thì hỏi anh những câu hỏi gợi mở để xác định chính xác mục tiêu!"*. Honor it: research → save → ask → WAIT.

## Key research takeaways

### Market size
- TP Kon Tum: 168K dân (27% tỉnh 629K), GRDP/người 3.055 USD (dưới TB VN)
- Phân hiệu ĐH Đà Nẵng: 2.000 SV, 400-500 SV/năm
- Măng Đen: 1,2 triệu khách du lịch/năm (2024), 60km từ TP

### Direct competitors (Kon Tum City)
- **Rita's Pizza & Pasta** (42 Trần Quang Khải) — 4.2/5, 243 reviews — STRONGEST
- Paris Kon Tum (527 Nguyễn Huệ) — mì Ý + steak + pizza, French style
- Rơm Bistro (99 Ba Đình) — 70-200K, multi-cuisine
- 1998 Bakery (Măng Đen) — only option ở khu du lịch
- Mì Cay Kitachi (259 Bà Triệu) — 242 chỗ, chuỗi lớn, **mì cay KHÔNG phải mì Ý**

### Market gap identified
1. **KHÔNG có quán chuyên mì Ý giá sinh viên** (segment 25-50K)
2. KHÔNG có quán mì Ý take-away chuyên nghiệp
3. Măng Đen chỉ có 1 quán mì Ý
4. Rita's chưa dominate phân khúc giá thấp

### 5 directions proposed (Mode B output)
| # | Concept | Vốn | USP | Rủi ro |
|---|---|---|---|---|
| A | Tiệm mì Ý bình dân chuyên tại TP | 800tr-1.2 tỷ | Fill gap giá SV | Rita's ở phân khúc cao hơn |
| B | Mì Ý take-away + delivery | 200-400tr | Test nhanh | Khó build brand |
| C | Mì Ý fusion Tây Nguyên (gỏi lá mì Ý) | 1-1.5 tỷ | Differentiation viral | R&D cao |
| D | Tiệm mì Ý tại Măng Đen | 600tr-1 tỷ | Monopoly + 1.2tr khách | Mùa vụ, xa TP |
| E | Mì Ý take-away tại Phân hiệu ĐH Đà Nẵng | 200-400tr | 2.000 SV cố định | Cạnh tranh Kitachi |

### Clarifying questions asked (model for future "lên plan X" requests)
1. Vốn khả dụng? (multiple-choice)
2. Mục tiêu chính: doanh thu ổn định / scale brand / test nhanh?
3. Target khách hàng? (segment picker)
4. Đã có mặt bằng chưa?
5. Kinh nghiệm F&B?
6. Muốn em đi sâu hướng nào trước?

## Financial framework used (F&B Việt Nam)

Nguồn: bePOS, validator.vn, phuctdigital.com — verified 29/07/2026.

| Hạng mục | Range |
|---|---|
| Vốn đầu tư (100m²) | 800tr - 1.5 tỷ |
| Rent Kon Tum | 15-30 triệu/tháng (rẻ hơn SG/HN 60-70%) |
| Food cost target | 30-35% |
| Labor cost | 18-25% |
| Ticket average | 50-80K (bình dân) / 100-150K (TB) |
| Break-even revenue | 140-200 triệu/tháng |
| Hòa vốn vận hành | Tháng 4-6 |
| Payback period | 12-18 tháng |

## Tools that worked
- `mcp__exa__web_search_exa` — primary research tool (web_search backend ddgs broken)
- `web_extract` — FAILED (DuckDuckGo backend, error returned)
- Manual research folder `wiki/projects/<topic>-research/` — independent project rule (24/07)

## Phase 2 — Post-clarification (29/07/2026)

Anh chọn: vốn <30tr + scale brand + target gia đình/SV/trẻ em/VP + online trước (chưa có mặt bằng) + chưa có kinh nghiệm F&B. Em build plan chi tiết cho **Cloud Kitchen tại nhà**.

### Files produced (`wiki/projects/mi-y-kontum-research/scripts/`)
- `02-business-plan-online-kitchen.md` — P&L tháng 1-3, menu engineering, kênh bán, timeline 30 ngày
- `03-launch-checklist-30days.md` — Day 0-30 checklist với 4 phases
- `04-recipe-sop.md` — 5 món anchor + sốt cà chua cơ bản (recipe chi tiết cho người chưa có kinh nghiệm)
- `05-marketing-tiktok-zero-cost.md` — 5 trụ content TikTok + 15+ hook templates + posting schedule
- `06-equipment-list-detailed.md` — Thiết bị bán công nghiệp Priority 1/2/3 với giá + nơi mua
- `07-brand-name-suggestions.md` — 3 tên brand (Mì Ý Thắng Lợi / Spaghetti Đăk Bla / Bếp Tuấn)

### Equipment capacity lesson (CRITICAL — added 29/07)
Khi user nói "có bếp từ + nồi chảo + tủ lạnh sẵn" — KHÔNG được assume OK. Plan đầu của em đã sai lần 1, anh flag ngay: thiết bị GIA ĐÌNH không đáp ứng sản lượng kinh doanh. Rule:
- Bếp từ gia đình: công suất 2.000-2.500W, 1-2 vùng nấu → throughput thấp
- Nồi/chảo size 20-28cm: mỗi batch chỉ 1-2 phần
- Tủ lạnh 150-250L: không đủ trữ sốt nấu sẵn 1 tuần
- **MUST** ask user cụ thể thiết bị hiện có + dùng làm gì (gia đình vs kinh doanh) trước khi lên vốn thiết bị

### Cloud kitchen vs nhà hàng truyền thống (financial framework)

| Hạng mục | Cloud Kitchen (<30tr) | Nhà hàng truyền thống (800tr-1.5 tỷ) |
|---|---|---|
| Mặt bằng | 0 đ (bếp tại nhà) | 15-30 tr/tháng |
| Thiết bị | 6-10 tr (bán công nghiệp mini) | 200-500 tr (full setup) |
| Pháp lý | ĐKKD cá thể + VSATTP | + giấy phép nhà hàng, PCCC |
| Doanh thu tháng 1 | 6-12 tr | 80-150 tr |
| Lợi nhuận tháng 1 | 0-3 tr (gần BEP) | -30 đến +20 tr |
| Lợi nhuận tháng 3 | 7-15 tr | 50-100 tr |
| Break-even | 1.5-2 tháng | 12-18 tháng |
| Kênh bán | ShopeeFood + GrabFood + TikTok Shop + Zalo | Dine-in + delivery |
| Rủi ro chính | Không có đơn 2 tuần đầu | Burn tiền mặt bằng |

### 6 câu clarifying gốc + answers (template cho future)
| # | Câu | Multiple-choice options | Anh chọn |
|---|---|---|---|
| 1 | Vốn? | <500tr / 500tr-1 tỷ / >1 tỷ | <30tr (thấp hơn option thấp nhất) |
| 2 | Mục tiêu? | DT ổn định / scale brand / test nhanh | Xây brand để scale + DT ổn định |
| 3 | Target? | SV, gia đình, trẻ em, VP, du khách | Gia đình + SV + trẻ em + VP |
| 4 | Mặt bằng? | Có / Chưa / Đang tìm | Có, bán online trước |
| 5 | Kinh nghiệm? | Chưa / 1-2 năm / Nhiều năm | Chưa có |
| 6 | Timeline? | T8 / T9 / T10 | Đầu T8 (8/8 launch) |

### Files project structure (independent project rule verified)
```
/Volumes/Storage-1/Hermes/wiki/projects/mi-y-kontum-research/
├── research/01-kontum-market-overview.md    # Phase 1 research findings
├── scripts/02-business-plan-online-kitchen.md  # Phase 2 plan
├── scripts/03-launch-checklist-30days.md
├── scripts/04-recipe-sop.md
├── scripts/05-marketing-tiktok-zero-cost.md
├── scripts/06-equipment-list-detailed.md
└── scripts/07-brand-name-suggestions.md
```

Rule 24/07 (INDEPENDENT PROJECT): mỗi research = OWN project folder, KHÔNG dựa vào project khác. Verified cho Kon Tum case.

## Lessons saved to memory
- 5 directions matrix là pattern tốt cho "lên plan mở X" — cho anh pick 1 trước khi commit resource build plan
- Clarifying questions nên mix multiple-choice (cost/segment) + open-ended (experience/goal) để pin target
- **Phase 2 added 29/07**: equipment capacity check BẮT BUỘC — thiết bị gia đình ≠ thiết bị kinh doanh. Ask user cụ thể thiết bị + dùng để làm gì TRƯỚC khi lên vốn thiết bị
- **Cloud kitchen pattern** (vốn <30tr, bếp tại nhà, online-first) là một variant riêng của F&B plan — KHÔNG apply financial framework nhà hàng truyền thống (800tr-1.5 tỷ)
- **7-file project structure** là template tốt cho "lên plan mở X" — research + plan + checklist + recipe + marketing + equipment + brand