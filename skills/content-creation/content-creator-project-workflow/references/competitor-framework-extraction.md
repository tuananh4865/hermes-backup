---
title: Competitor Framework Extraction — Phân tích video viral để rút framework
created: 2026-06-18
updated: 2026-06-18
type: reference
tags: [competitor-analysis, framework-extraction, tiktok, content-creator]
applies_to: content-creator-project-workflow
---

# Competitor Framework Extraction — Workflow chuẩn

## Khi nào dùng

Khi anh gửi link TikTok video + nói "phân tích đi" / "lấy framework này" / "rút bài học":
1. Dùng pipeline `youtube-transcript-extractor` skill (TikTok full video path) để extract transcript
2. Phân tích framework theo 5 phần dưới đây
3. Áp dụng vào 15-20 scripts tương tự trong project

## 5 phần phân tích (template từ session 18/06 với video "ánh sáng 0đ")

### 1. HOOK (0-3s)
- **Voiceover mở đầu**: ghi chính xác 1-2 câu đầu
- **Text overlay**: chính xác text xuất hiện 3s đầu
- **Hook template** (chọn 1 trong 5):
  - **Contradiction** (X vs Y) ← mạnh nhất
  - **Number hook** (con số cụ thể)
  - **POV/Relatable** (audience nhận ra mình)
  - **Confession/Thú nhận** (auth = trust)
  - **Proof Drop** (show kết quả trước)
- **Visual hook**: layout/filter/effect đặc biệt

### 2. BODY (3-40s) — Framework phổ biến
- **Show 3 cases trong 1 video** ← framework mạnh nhất cho ÁNH SÁNG niche
  - Case 1 (❌ cách sai #1) → visual + voiceover mô tả
  - Case 2 (❌ cách sai #2) → visual + voiceover mô tả
  - Case 3 (✅ cách đúng) → visual + voiceover mô tả
- **Kỹ thuật storytelling**: dùng chính gương mặt mình làm A/B/C → retention cao hơn 2 video riêng

### 3. PERSUASION (nếu có, 20-30s)
- **Con số định lượng** cực mạnh:
  - "100 video cùng chủ đề"
  - "Lướt qua trong 0,5 giây"
  - "Quyết định 80%..."
- Mỗi claim kèm 1 con số = persuasion +5x

### 4. CTA (cuối video)
- **Specific action thuần value** (KHÔNG bán hàng):
  - "Đặt 1 chiếc bàn cạnh cửa sổ"
  - "Thử ngồi nghiêng 45 độ và quay 1 video"
- **Có tease cho ngày mai** → retention cho series:
  - "Ngày 2 sẽ là 1 mẹo không đồng khác"
- **Slang Gen Z ở CTA** (1 từ duy nhất) — ví dụ: "Flow ngay"

### 5. VOICE & STYLE
- **Xưng hô**: "tôi" + "các bạn" HOẶC "mình" + "bạn" (trung tính)
- **Tone**: calm + confident + storytelling
- **Text overlay**: xuất hiện 1 từ/cụm ngắn theo từng bước, fade in/out
- **B-roll**: 0% (chỉ talking head) HOẶC dùng sparingly
- **Slang**: TIẾT CHẾ (1-2 từ/cả video), KHÔNG spam

## Đánh giá (scoring 0-10)

| Tiêu chí | Điểm | Note |
|----------|-------|------|
| Voice match với voice profile project | /10 | Có trung tính không? Có calm không? |
| Cấu trúc học được | /10 | Framework rõ ràng? Replicable? |
| CTA quality | /10 | Specific action? 0% bán hàng? |
| Visual simplicity | /10 | Có cần thiết bị đắt? |
| Slang usage | /10 | Tự nhiên hay spam? |
| **45-day value rule** | /10 | 100% value, 0% bán? |
| **TỔNG** | **/10** | ≥9 = "template vàng", copy framework |

## Actions cho project (output phần quan trọng nhất)

Sau khi phân tích, **luôn** output 1 bảng:

| Script hiện tại | Áp dụng framework | Hook mới |
|-----------------|-------------------|----------|
| ANH-SANG-01 | "Show 3 cases" | "0Đ = Đèn 5TR" |
| ANH-SANG-02 | "Con số cụ thể" | "3 khung giờ, 1 video" |
| ... | ... | ... |

## Reference example (session 18/06)

- Source: https://vt.tiktok.com/ZSQt1SY3m/ ("ánh sáng 0đ" 43s)
- Output: `wiki/projects/content-creator/research/competitor-anh-sang-0d-tiktok-2026-06.md` (9.8KB)
- Framework extracted: "Contradiction + Con số cụ thể + Show 3 cases + Specific CTA + Tease ngày mai"
- Voice: trung tính "tôi" + "các bạn" (gần với "mình + bạn" của project)
- 9.5/10 score → template vàng → áp dụng vào 5 ÁNH SÁNG scripts + brainstorm thêm 11 hooks mới

## Liên kết

- SKILL.md: `content-creator-project-workflow` (Content Calendar section trigger)
- Skill: `youtube-transcript-extractor` (TikTok full video path)
- Skill: `tiktok-competitor-deep-analysis` (batch analysis 50+ clips)
