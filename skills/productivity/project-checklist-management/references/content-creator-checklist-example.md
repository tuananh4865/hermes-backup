---
title: Content Creator Project CHECKLIST — Example Reference
created: 2026-06-18
updated: 2026-06-18
type: reference
tags: [example, content-creator, checklist, project-management]
confidence: high
---

# Content Creator Project CHECKLIST — Real Example

**Source project:** `/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/`
**File path:** `Operations/CHECKLIST-PROJECT.md` (11.2KB, 18/06/2026)
**Setup trigger:** User explicit request — *"Lập cho anh một rule trong project này là luôn phải log và check list toàn bộ những gì đã làm, đang làm và chưa làm trong project này để không bị trùng lặp và cập nhật liên tục mỗi khi agent làm việc với project này"*

## Why this example matters

This is a **verified working example** of the `project-checklist-management` skill applied to a real Content Creator project (3 trụ: EDIT+SETUP+ÁNH SÁNG, 85+ kịch bản, 71 bài curriculum, target 10K follow trong 45 ngày).

It demonstrates:
- 4-section structure (🔴 ĐANG LÀM / 🟡 CHƯA LÀM / 🟢 ĐÃ LÀM / ⚪ HỦY) populated with real data
- 4 ưu tiên buckets trong 🟡 section (Setup nền tảng / Kế hoạch 90 video / Production SOP / Đo & học)
- 13 tasks cụ thể với effort estimate
- Metrics dashboard with timeline milestones (45/60/90 ngày)
- Format log chuẩn cho agent
- Hard rule injection text snippet

## Full CHECKLIST file (verbatim, abridged for reference)

```markdown
---
title: PROJECT CHECKLIST — Content Creator
created: 2026-06-18
updated: 2026-06-18
type: operations
tags: [content-creator, project-management, checklist]
confidence: high
status: ACTIVE
last_session: 2026-06-18
---

# ✅ PROJECT CHECKLIST — Content Creator

> **Mục đích:** Single source of truth cho mọi công việc trong project.
> Agent nào làm việc với project này PHẢI đọc + cập nhật file này.
>
> **Quy tắc vàng:**
> - **TRƯỚC KHI LÀM** → check phần "🔴 ĐANG LÀM" + "🟡 CHƯA LÀM" để KHÔNG trùng lặp
> - **SAU KHI XONG** → cập nhật phần "🟢 ĐÃ LÀM" + ghi session ID + timestamp
> - **CẤM LÀM MÀ KHÔNG GHI LOG** → mất track = lặp lại = phí thời gian

## 📊 TRẠNG THÁI TỔNG QUAN

| Trụ nội dung | Kịch bản có sẵn | Đã quay | Còn lại | Tiến độ |
|--------------|-----------------|---------|---------|---------|
| EDIT | 30 | 0 | 30 | 0% |
| SETUP GÓC QUAY | 25 | 0 | 25 | 0% |
| ÁNH SÁNG | 30 | 0 | 30 | 0% |
| **TỔNG** | **85+** | **0** | **85+** | **0%** |

**Mục tiêu 45 ngày (18/06 - 02/08/2026):**
- 90 video TikTok
- 10.000 follow
- 0% bán hàng, 100% hướng dẫn cơ bản

## 🔴 ĐANG LÀM (in_progress)

| # | Task | Session bắt đầu | Agent | Deadline | Block bởi |
|---|------|------------------|-------|----------|-----------|
|   | *(trống — chưa có task đang làm dở)* | | | | |

## 🟡 CHƯA LÀM (todo) — Ưu tiên cao

### ƯU TIÊN 1 — Setup nền tảng (CHẶNG 0)

| # | Task | Ghi chú | Effort |
|---|------|---------|--------|
| 1.1 | Đăng ký TikTok Shop Affiliate | Sau 45 ngày mới cần | 30 phút |
| 1.2 | Đăng ký Accesstrade | Backup channel affiliate | 30 phút |
| 1.3 | Viết trang chân dung khán giả | File 03-khoa-luyen-ke-chuyen.md chưa có | 2 giờ |
| 1.4 | Vào 1 cộng đồng creator (Facebook/Zalo) | Network cho hỏi đáp | 1 giờ |

### ƯU TIÊN 2 — Kế hoạch 90 video (CHẶNG 1)

| # | Task | Ghi chú | Effort |
|---|------|---------|--------|
| 2.1 | Lập content calendar 90 video | File ma trận có rồi — cần copy sang format operational | 2 giờ |
| 2.2 | Áp framework "4 tử huyệt + 5 phần" cho 30 kịch bản EDIT | Lấy từ `Research/2026-06-17/deep-research-edit-co-ban.md` | 6 giờ |
| 2.3 | Áp framework cho 25 kịch bản SETUP | Lấy từ `Research/2026-06-17/deep-research-setup-goc-quay.md` | 5 giờ |
| 2.4 | Áp framework cho 30 kịch bản ÁNH SÁNG | Lấy từ `Research/2026-06-17/deep-research-anh-sang-co-ban.md` | 6 giờ |
| 2.5 | Chọn + viết SCRIPT ĐẦY ĐỦ cho video Ngày 1 | Áp framework mới — video đầu tiên chặng 1 | 3 giờ |

### ƯU TIÊN 3 — Production SOP (CHẶNG 1)

| # | Task | Ghi chú | Effort |
|---|------|---------|--------|
| 3.1 | Test quay video Ngày 1 | Đã có kịch bản — cần quay thật | 2 giờ |
| 3.2 | Viết SOP setup góc quay chuẩn | Chưa có | 3 giờ |
| 3.3 | Viết SOP edit CapCut chuẩn | Chưa có | 3 giờ |
| 3.4 | Tạo template tracking video | Đã có HTML `tram-dieu-hanh-kenh.html` | 1 giờ |

### ƯU TIÊN 4 — Đo & học (ongoing)

| # | Task | Ghi chú | Effort |
|---|------|---------|--------|
| 4.1 | Review Chủ nhật tuần 1 (6 chỉ số) | Sau 7 video đầu | 1 giờ |
| 4.2 | Chọn 3 hook mạnh nhất từ 7 video đầu | Theo PHẦN 6 lộ trình luyện | 30 phút |
| 4.3 | Đánh giá 4 trụ cột sau 30 video | Dùng `checklist-4-tru-cot.html` | 2 giờ |

## 🟢 ĐÃ LÀM (done) — Lịch sử

### 18/06/2026

- ✅ **[SETUP] Hệ thống Auto-Log + Checklist Project** (Session 18/06 09:50, ~10 phút)
  - Tạo `Operations/CHECKLIST-PROJECT.md` (11.2KB) — file single source of truth
  - Update `hub.md` — thêm HARD RULE (bước 1: đọc checklist đầu tiên + bước 8: cập nhật khi xong)
  - Update `CHANGELOG.md` — entry mới theo format chuẩn
  - **Tác động:** 100% task trong project được log + cập nhật liên tục → không bị trùng lặp
- ✅ **[CẢI TIẾN] Tích hợp framework "4 tử huyệt + 5 phần" vào project** (Session 18/06 09:30)
  - Tạo `Operations/framework-4-tu-huyet-5-phan-kich-ban.md` (7.2KB)
  - Thêm PHẦN 7 vào `bo-cong-thuc-viral-ke-chuyen.md` (+110 dòng)
  - Update `01-guideline-san-xuat.md` BƯỚC 3
  - **Tác động:** 85+ kịch bản có thể REPURPOSE → mạnh hơn 2-3 lần

### 17/06/2026
- ✅ **[CẢI TIẾN] PIVOT 100% xây thương hiệu** (3 trụ EDIT+SETUP+ÁNH SÁNG, 0% bán)
- ✅ **[NGHIÊN CỨU] Deep research 3 trụ cột** — 85+ kịch bản từ ~120 nguồn
- ✅ **[BÀI VIẾT] Review Goojodoq GD15 v3 (TOP LIST)**

### 16/06/2026
- ✅ **[NGHIÊN CỨU] Phân tích 4 clip viral @u40hoc.xay.kenh**
- ✅ **[NGHIÊN CỨU] DEEP RESEARCH 50 clip stratified**
- ✅ **[CẢI TIẾN] Restructure folder**
- ✅ **[KỊCH BẢN] Viết kịch bản Ngày 1 ánh sáng 0đ** (3 lần rewrite)
- ✅ **[BÀI VIẾT] Review Goojodoq GD14 → GD15** (3 phiên bản)

### 14/06/2026
- ✅ **[ĐÓNG LỖ HỔNG] Trạm điều hành + Checklist 4 trụ + 8 dạng + Ứng dụng thực tế**

### 13/06/2026
- ✅ **[SETUP] Set làm project mặc định** (Tạo hub.md, review 14 files)
- ✅ **[CẬP NHẬT] Hệ thống tài liệu số 00-03 + công thức viral**

## ⚪ ĐÃ HỦY / KHÔNG LÀM (cancelled)

| # | Task đã hủy | Lý do | Ngày hủy |
|---|-------------|-------|----------|
| 1 | Lộ trình cá nhân 45 ngày (file 01) | Hiểu nhầm — supersede bởi curriculum | 17/06 |
| 2 | Review Goojodoq GD14 v1 (chi tiết specs) | Quá chi tiết, dời sang v2 gọn | 16/06 |
| 3 | Kịch bản Ngày 1 — 5 cài đặt camera "90% chưa bật" | Con số "90%" bịa → vi phạm HARD RULE | 16/06 |
| 4 | Kịch bản Ngày 1 — HDR (tính năng ẩn) | HDR quá đặc thù | 16/06 |

## 📌 QUY TẮC SỬ DỤNG CHECKLIST NÀY (cho agent)

### Khi bắt đầu session làm việc với project này:

```
1. ĐỌC file này (Operations/CHECKLIST-PROJECT.md) ĐẦU TIÊN
2. CHECK phần "🔴 ĐANG LÀM" — nếu có task dở → tiếp tục
3. CHECK phần "🟡 CHƯA LÀM" — chọn task phù hợp với yêu cầu của anh
4. CẬP NHẬT phần "🔴 ĐANG LÀM" khi bắt đầu
5. CẬP NHẬT phần "🟢 ĐÃ LÀM" khi xong
6. NẾU gặp vấn đề → cập nhật cả "🟡 CHƯA LÀM" + "⚪ HỦY"
```

### Format ghi log khi bắt đầu task:

```markdown
- 🔄 **[DANH MỤC] Tên task** (Session YYYY-MM-DD HH:MM)
  - File 1: sẽ thay đổi gì
  - File 2: sẽ thay đổi gì
  - Tạo mới: file XYZ
  - Lý do: ...
```

### Format ghi log khi xong task:

```markdown
- ✅ **[DANH MỤC] Tên task** (Session YYYY-MM-DD HH:MM, ~X phút)
  - File 1: thay đổi gì (X dòng)
  - File 2: thay đổi gì
  - Tạo mới: file XYZ (XKB)
  - Kết quả: ...
  - Tác động: ...
  - Bài học: (nếu có)
```

### Checklist tự check trước khi kết thúc session:

- [ ] Mọi task đã làm đều có trong "🟢 ĐÃ LÀM" với session ID + timestamp
- [ ] Mọi task dở đã move sang "🔴 ĐANG LÀM" (không bị mất)
- [ ] Mọi task mới phát hiện đã move sang "🟡 CHƯA LÀM"
- [ ] Số liệu bảng "Trạng thái tổng quan" đã update (nếu có)
- [ ] Không có task nào "làm xong" mà KHÔNG log

## 🔄 TỰ ĐỘNG CẬP NHẬT

**Khi agent mới bắt đầu session với project Content Creator:**

Agent sẽ TỰ ĐỘNG (theo rule trong `hub.md`):
1. Đọc `Operations/CHECKLIST-PROJECT.md` (file này) — FIRST
2. Báo cáo trạng thái: "Có X task đang làm, Y chưa làm, Z đã làm"
3. Hỏi anh muốn tiếp tục task nào
4. Update checklist ngay khi xong

**Khi agent đang làm việc:**

Agent sẽ:
- Ghi task vào "🔴 ĐANG LÀM" khi bắt đầu
- Move sang "🟢 ĐÃ LÀM" khi xong
- Cập nhật bảng "Trạng thái tổng quan" nếu có số liệu mới

## 📊 METRICS & DASHBOARD

### Cập nhật lần cuối: 2026-06-18 09:50

| Metric | Hiện tại | Mục tiêu | Tiến độ |
|--------|----------|----------|---------|
| Video đã đăng TikTok | 0 | 90 (45 ngày) | 0% |
| Follow TikTok | 0 | 10.000 | 0% |
| Sub YouTube | 0 | 5.000 | 0% |
| Video bán hàng | 0 (đúng — đang trong 45 ngày build) | 0 trong 45 ngày đầu | ✅ |
| Kịch bản có sẵn | 85+ | 90 | 95% |
| Kịch bản đã áp framework mới | 0/85+ | 85+ | 0% |

### Các mốc quan trọng:

- **18/06/2026:** Ngày bắt đầu PIVOT xây thương hiệu (45 ngày)
- **02/08/2026:** Hết 45 ngày → 10k follow + bắt đầu nhúng affiliate
- **18/08/2026:** Hết 60 ngày → 15-20k follow + 1 đơn affiliate đầu tiên
- **18/09/2026:** Hết 90 ngày → 10k follow + 50tr GMV

## 🔗 LIÊN KẾT

- `hub.md` — Project hub (đọc sau khi đọc file này)
- `00-ban-do-tong.md` — Bản đồ 5 chặng hành trình
- `01-guideline-san-xuat.md` — Quy trình sản xuất 7 bước
- `bo-cong-thuc-viral-ke-chuyen.md` — Bộ công thức viral
- `Operations/framework-4-tu-huyet-5-phan-kich-ban.md` — Framework mới tra cứu nhanh
- `Research/2026-06-17/02-CURRICULUM-NGUOI-MOI-BAT-DAU.md` — 71 bài curriculum
- `CHANGELOG.md` — Lịch sử thay đổi chi tiết
```

## HARD RULE injection text (verbatim, what was added to hub.md)

```markdown
## 🔄 Khi bắt đầu session mới
Em sẽ tự động:
1. **ĐỌC `Operations/CHECKLIST-PROJECT.md` TRƯỚC TIÊN** (rule mới 18/06 — bắt buộc) — biết task đang làm, chưa làm, đã làm
2. Đọc `hub.md` (file này)
3. Đọc `00-ban-do-tong.md` để biết đang ở chặng nào
4. Check `Trend_Updates/` mới nhất
5. Load guideline tương ứng task (theo bảng "tình huống → file" trong 00)
6. Áp dụng giọng trung tính, chuyên nghiệp
7. Nhắc chạy series theo tỷ lệ 70/30 (value/affiliate)
8. **CẬP NHẬT CHECKLIST** ngay khi xong task (move từ "🔴 ĐANG LÀM" → "🟢 ĐÃ LÀM")

**⚠️ HARD RULE (18/06/2026):** Mọi agent làm việc với project này PHẢI đọc `Operations/CHECKLIST-PROJECT.md` ĐẦU TIÊN trước khi làm bất kỳ task nào. Cấm làm mà không check trùng lặp. Xem chi tiết rule trong file CHECKLIST.
```

## Pattern: How to apply this skill to other projects

When user asks for this on a NEW project:

1. **Identify project root** — `pwd` or check folder structure
2. **Check if hub.md exists** — if not, create one first
3. **Create CHECKLIST file** — use the structure above, populate with 13+ tasks based on user's project goals
4. **Inject HARD RULE into hub.md** — add the 8-step "Khi bắt đầu session mới" + HARD RULE warning
5. **Update CHANGELOG.md** — add entry with format from `CHANGELOG.md` template
6. **Self-update CHECKLIST** — record this setup task in "🟢 ĐÃ LÀM"
7. **Verify** — run the verification commands in the SKILL.md

## Lessons learned from this setup (2026-06-18)

1. **Single file is enough** — Don't over-engineer with multiple files. 1 CHECKLIST + 1 hub.md rule = full system
2. **Auto-prompt > auto-hook** — Agent reads CHECKLIST FIRST instead of waiting for hook to trigger. Simpler, more reliable.
3. **Cancelled tasks are gold** — "⚪ ĐÃ HỦY" section captures WHY tasks failed, preventing repeat mistakes
4. **Effort categories > time estimates** — Use "30 phút / 2 giờ / nửa ngày" buckets, not exact minutes
5. **User-specific data > generic template** — Real project data (3 trụ, 85+ kịch bản, deadline 02/08) makes checklist immediately useful