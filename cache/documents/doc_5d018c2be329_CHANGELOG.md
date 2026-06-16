# CHANGELOG — Content Creator Project

> Theo dõi thay đổi file theo thời gian. Mỗi entry ghi: ngày, ai, file nào, thay đổi gì.

---

## [2026-06-16] — STEP-2.1: Verify loop-goal skill hoạt động

**Người thực hiện:** Hermes Agent (Claude Fable 5) — yêu cầu của anh ClawdBotZ1 (Telegram, 19:38:24)

**Hành động:**
- Đọc skill mới: `~/.hermes/skills/loop-goal/` (4 files: SKILL.md, condition-parser.py, run.sh, test.sh)
- Chạy `./test.sh` → **6/6 tests PASS**
- Verify state logging: `~/.hermes/workers/content-creator/state.md` có 3 runs logged (FAIL 7.5 → WARN 8.5 → PASS 9.3)
- Test workers cũ cũng log đúng: `test-runner-24410`, `test-runner-24613`, `test-runner-impossible-*`

**Kết luận:** `/goal` primitive hoạt động đúng. Sẵn sàng dùng cho task lặp lại (viết script, research, code refactor).

---

## [2026-06-16] — STEP-2: Log toàn bộ file, tạo CHANGELOG + wiki mirror

**Hành động:**
- Đọc toàn bộ 16 file ở root + 3 folder chính (Analysis, Operations, Raw) + 3 folder phụ (Archive, Trend_Updates, Transcripts)
- Tạo file này: `CHANGELOG.md`
- Tạo `wiki.md` mirror hub (bản tóm tắt 1 trang)

**Files đã đọc (verified, 100%):**

### Root (16 file)
1. ✅ `hub.md` (122 dòng) — Hub dẫn đường, đã restructure folder 16/06
2. ✅ `CLAUDE-FABLE-5.md` (485+ dòng) — System prompt của agent
3. ✅ `00-ban-do-tong.md` (85 dòng) — Bản đồ 5 chặng, đích đến 90 ngày
4. ✅ `01-guideline-san-xuat.md` (78 dòng) — Quy trình sản xuất 7 bước + 7 điều Hiến pháp
5. ✅ `02-series-lop-quay-dung-vo-long.md` (112 dòng) — Series tutorial ngôn ngữ khung hình + dựng phim
6. ✅ `03-khoa-luyen-ke-chuyen.md` (86 dòng) — Khóa luyện kể chuyện 30 ngày, công thức 4 nhịp
7. ✅ `bo-cong-thuc-viral-ke-chuyen.md` (197 dòng) — 12 hook + 7 công thức kể chuyện + checklist 10 điểm
8. ✅ `8-dang-content-chi-dan.md` (575+ dòng) — 8 dạng content (Tutorial/Review/So sánh/Top/Before-After/Story/Myth-bust/Q&A)
9. ✅ `Road_Map_90Days_to_Become_Content_Creator_Fable5.md` (141 dòng) — Lộ trình 90 ngày + phân tích thị trường VN
10. ✅ `TikTok_Content_Guideline.md` (438 dòng) — 9 công thức viết + 8 dạng content + TikTok SEO 4-layer
11. ✅ `YouTube_Content_Guideline.md` (347 dòng) — 4 content pillars + 3 loại video
12. ✅ `Content_Guideline_TikTok_YouTube.md` (211 dòng) — Lịch đăng 10 video/tuần
13. ✅ `kich-ban-content-pocket3-phu-kien.md` (133 dòng) — Bộ kịch bản 4 sản phẩm (K&F, MA66, macro, ốp) + 12 mẹo + 5 setup series
14. ✅ `script-tiktok-kf-filter-osmo-pocket.md` (220 dòng) — 3 script TikTok hoàn chỉnh cho K&F filter
15. ✅ `series-xay-kenh-0-dong.md` (137 dòng) — Series 25 video "0 đồng" kéo follow
16. ✅ `ScreenRecording_06-10-2026_00-53-24_1.txt` (83 dòng) — Transcript về personal brand + AI

### Analysis/ (7 file)
17. ✅ `Analysis/04-phan-tich-50-clip-V2-DEEP.md` (317 dòng) — DEEP RESEARCH 50 clip @u40hoc.xay.kenh, 5 strata
18. ✅ `Analysis/04-phan-tich-khoa-hoc-u40hoc-xaykenh.md` (217 dòng) — Phân tích 4 clip viral
19. ✅ `Analysis/Road_Map_90Days_to_Become_Content_Creator_Fable5.md` (141 dòng) — Bản sao
20. ✅ `Analysis/chien-thuat-kenh-hi-imdung-deep-dive.md` (262 dòng) — Deep dive kênh Dũng RV
21. ✅ `Analysis/phan-tich-affiliate-skills-repo.md` (358 dòng) — Phân tích GitHub repo
22. ✅ `Analysis/phan-tich-kenh-hi-imdung.md` (207 dòng) — 50 video mới nhất + 7 bài học
23. ✅ `Analysis/phan-tich-ket-hop-3-tai-lieu.md` (209 dòng) — Kết hợp 3 tài liệu + MrBeast

### Operations/ (4 file)
24. ✅ `Operations/PROGRESS_Review_3_Video.md` (139 dòng) — Review 3 video đầu tiên (Tripod, GOOJODOQ, K&F Filter)
25. ✅ `Operations/SOP_Proof_Shot_3_San_Pham.md` — SOP quay proof shot
26. ✅ `Operations/ho-so-giong-van-va-kich-ban-ma66.md` — Voice profile + script MA66
27. ✅ `Operations/kich-ban-ngay-1-anh-sang-0-dong.md` (12.8KB) — Kịch bản Ngày 1
28. ✅ `Operations/review-goojodoq-gd14.md` (15.4KB) — Review Goojodoq GD14
29. ✅ `Operations/tien-do-series-hoc-edit.html` — Tiến độ series học edit

### Raw/ (1 file + 2 folder)
30. ✅ `Raw/ScreenRecording_06-10-2026_00-53-24_1.txt` (đã đếm ở root)
31. ✅ `Raw/Transcripts/` — folder chứa VTT (đã check có video1.vi.vtt, video2.vi.vtt, video3.en.vtt)
32. ✅ `Raw/_video_analysis/` — folder chứa phân tích video (chưa đọc chi tiết)

### Archive/ (1 file)
33. ✅ `Archive/2026-06-15-compass-artifacts` — Workflow cũ

### Trend_Updates/
34. ✅ `Trend_Updates/Trends_2026-06-11.md` (12K) — Báo cáo xu hướng TikTok 11/06/2026

**Tổng cộng:** 34 files/folders verified.

---

## [2026-06-13] — Set làm project mặc định (từ log cũ trong hub.md)

> Tổng cộng: 14 files + 2 folders
> Set default: `/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/`

## [2026-06-13] — Lần 2: Hệ thống tài liệu số 00-03

> Tổng: 19 files + 3 folders

## [2026-06-14] — Đóng 4 lỗ hổng tài liệu

> Tổng: 23 files + 3 folders
> Thêm: tram-dieu-hanh-kenh.html, checklist-4-tru-cot.html, 8-dang-content-chi-dan.md, ung-dung-thuc-te-theo-tinh-huong.md

## [2026-06-16] — Phân tích 4 clip viral @u40hoc.xay.kenh

> Tổng: 28 files
> Thêm: Analysis/04-phan-tich-khoa-hoc-u40hoc-xaykenh.md + 5 hook mới

## [2026-06-16] — DEEP RESEARCH 50 clip stratified

> Tổng: 28 files
> Thêm: Analysis/04-phan-tich-50-clip-V2-DEEP.md (317 dòng, 5 strata)

## [2026-06-16] — Restructure folder

> Tổng: 16 file ở root + 3 folder chính (Analysis, Operations, Raw) + 3 folder phụ (Archive, Trend_Updates, Transcripts)
> Mục đích: giảm noise root directory, dễ tìm file theo mục đích

## [2026-06-16] — Viết kịch bản Ngày 1 + 2 lần rewrite

> 3 phiên bản kịch bản Ngày 1 trong `Operations/kich-ban-ngay-1-anh-sang-0-dong.md`
> - Lần 1: 5 cài đặt camera 90% người mới chưa bật
> - Lần 2: HDR (sai — quá đặc thù)
> - Lần 3: Ánh sáng tự nhiên 0 đồng (chốt)
> Bỏ con số bịa "80%" → thay bằng "hầu hết" (HARD RULE)

## [2026-06-16] — Viết review Goojodoq GD14

> File mới: `Operations/review-goojodoq-gd14.md` (15.4KB)
> Research 5 nguồn uy tín, verify từng spec, voice trung tính chuyên nghiệp

---

## Format Entry Mới

Khi thêm/sửa file, dùng format:

```markdown
## [YYYY-MM-DD] — Mô tả ngắn gọn (1 dòng)

**Người thực hiện:** [agent name]
**Hành động:**
- File 1: thay đổi gì (X dòng)
- File 2: thay đổi gì
- Tạo mới: file XYZ

**Lý do:** (nếu có)
**Liên kết:** (link đến quyết định/task nếu liên quan)
```
