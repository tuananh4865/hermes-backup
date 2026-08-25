# ⭐ MASTER PHILOSOPHY — 8 KEY CHÍNH (anh đã dạy 19/07/2026)

> **Anh đã dạy 2 lần trong cùng session:** (1) "Face zone, safe zone, card zone, PIP method + HyperFrames+ffmpeg là các key chính" → 5 KEY kỹ thuật. (2) "Wiki Product Research FIRST + Card content từ transcript + Sáng tạo không lặp lại" → 3 KEY chất lượng content. Tổng cộng: **8 KEY CHÍNH**.

## 🎯 8 KEY CHÍNH (BẮT BUỘC — KHÔNG ĐƯỢC THAY ĐỔI)

### CONTENT KEYS (anh dạy 19/07 — chất lượng content)

| # | Key | Source | Quy tắc cứng |
|---|---|---|---|
| **1** | **WIKI PRODUCT RESEARCH FIRST** | `wiki-product-ground-truth` skill | TRƯỚC khi viết motion/card: check `wiki/projects/tuan-anh-review-tiktok/products/[name].md` → lấy specs/giá/brand chính xác. Citation `[N]` map về wiki. **KHÔNG bịa thông tin** → sai specs = customer trust violation. |
| **2** | **CARD CONTENT TỪ TRANSCRIPT** | Anh dạy 19/07 | KHÔNG dùng template "mọi clip đều có CHART/PORT/USP/TESTIMONIAL". Mỗi card phải xác định từ transcript: cần USP nào? Pain point nào? Bước nào? Test case nào? Pop up ở đoạn nào? |
| **3** | **SÁNG TẠO + ĐA DẠNG** | Anh dạy 19/07 | Dùng **MẮT** đọc visual cues (mặt anh cầm gì, chỉ đâu), **TAI** nghe audio cues (keyword, nhấn mạnh), **TƯ DUY** hỏi "đoạn này nên show gì". Mỗi clip phải có **1-3 điểm sáng tạo** riêng. **KHÔNG popup card ở thời điểm + vị trí giống nhau** cho mọi clip → nhàm chán. |

### TECHNICAL KEYS (5 KEY kỹ thuật từ V78-V96)

| # | Key | Source | Quy tắc cứng |
|---|---|---|---|
| **4** | **FACE ZONE** (vùng cấm mặt) | V85 RECAP | y=547-1140, x=308-1526 (1920×1920). KHÔNG card trừ khi có PIP background. |
| **5** | **SAFE ZONE 10%** mỗi cạnh | V83 RECAP | top/bottom 192px, left/right 108px (1080×1920). Mọi element bounds trong margin. |
| **6** | **CARD ZONE** (vị trí glass card) | V82 + V84 | HOOK/PROBLEM/PRODUCT/USP → bottom (y > 1280). TESTIMONIAL/FEATURE → top (y < 547). CHART/PORT → giữa (y = 966). CTA → center 80%. |
| **7** | **PIP METHOD** (V18/V13 chính thức) | V96 | 1 video + GSAP keyframe `scale: 0.42, x: ±222, y: -540, borderRadius: 28`. CHART top-left, PORT top-right. |
| **8** | **QUY TRÌNH HYPERFRAMES + FFMPEG** | V22 + V96 | (a) HyperFrames render silent mp4 → (b) ffmpeg ghép audio cuối. KHÔNG `format=yuva420p` overlay cho glass. |

## 🎨 OPTIONAL (anh đã explicit — CÓ THỂ THAY ĐỔI)

| Thứ | Ai quyết | Ví dụ |
|---|---|---|
| **Số phase** (HOOK/PROBLEM/CHART/PORT/USP/TESTIMONIAL/FEATURE/USECASE/CTA) | **Transcript video** | 5/7/11 phase tùy clip. Bỏ phase nếu transcript không có content liên quan. |
| **Thứ tự phase** | **Transcript + sáng tạo** | Bỏ STAMP, thêm USE-CASE, swap order. KHÔNG theo template cứng. |
| **Loại card** (chart/port/testimonial/feature/usecase/cta) | **Transcript + sáng tạo** | Clip có spec → chart. Clip có testimonial → testimonial card. Clip ngắn → 2-3 card. |
| **Pop up timing** | **Transcript cues** | Đoạn nào có keyword → pop up. KHÔNG đặt cứng t=7-13s. |
| **Content card** | **Wiki + sáng tạo** | Citation từ wiki + paraphrase hay, không bịa. |
| **Màu glass** (opacity, border) | Anh | V7.1 (0.15) → V7.2 (0.18) → DEFAULT. |
| **Glass recipe** (blur, shadow, radius) | Edit style | Nate Herk style analysis có thể tweak. |
| **Font** | Anh / brand | Default SF Pro. |
| **Easing** | Edit style | Default `power2.out`. |
| **PIP scale** (0.42) | Edit style | 0.35-0.5 tùy PIP size. |
| **PIP position** (x ±222, y -540) | Edit style | Có thể đổi nếu transcript yêu cầu. |

## 🚦 DECISION TREE (clip mới)

```
Anh gửi clip raw + brief
    ↓
1. ⭐ CHECK WIKI PRODUCT RESEARCH (Key #1)
   - Sản phẩm gì? → check wiki/products/[name].md
   - Specs/giá/brand chính xác?
    ↓
2. ⭐ ĐỌC TRANSCRIPT (Key #2)
   - MẮT: mặt anh cầm gì? chỉ đâu?
   - TAI: keyword nào? nhấn mạnh chỗ nào?
   - TƯ DUY: đoạn nào cần card? pop up khi nào?
    ↓
3. Source video có talking head motion?
   - CÓ → V22 workflow
   - GẦN static → slow zoom Ken Burns / AI inject motion
    ↓
4. ⭐ ĐỀ XUẤT PLAN MOTION (Key #3 - sáng tạo)
   - Cần spec → CHART (khi transcript có spec)
   - Cần quy trình → PORT (khi transcript có steps)
   - Cần feedback → TESTIMONIAL (khi transcript có feedback)
   - Cần context → USECASE
   - KHÔNG ép tất cả phase vào 1 clip
    ↓
5. VẼ layout timeline (anh duyệt)
    ↓
6. Build HTML + GSAP với 8 CHECK:
   Key #1 Wiki, Key #2 Transcript, Key #3 Sáng tạo
   Key #4 Face zone, Key #5 Safe zone, Key #6 Card zone
   Key #7 PIP method, Key #8 HyperFrames+ffmpeg workflow
    ↓
7. Render silent → ffmpeg ghép audio → ship
```

## 🎯 ANH DẠY (trích nguyên văn)

> *"Trước khi làm motion cho clip thì phải xác định nội dung của nó nói về sản phẩm nào và vào wiki/projects/tuan anh review tiktok/products để check thông tin chính xác của sản phẩm để lên plan làm motion cho đúng!"*

> *"Các card cũng không phải clip nào cũng làm như nhau mà phải được xác định rõ từng đoạn transcript video nội dung như thế nào để biết nên làm gì... hãy đề cao sự sáng tạo lên hàng đầu!"*

> *"Đề cao sự sáng tạo và dùng đồng thời cả mắt, tai và tư duy... đảm bảo mọi thứ không lặp lại nhàm chán!"*

> *"Face zone, safe zone, card zone, PIP method + HyperFrames+ffmpeg là các key chính. Tất cả những thứ khác đều có thể thay đổi tuỳ thuộc vào ý muốn của anh hoặc nội dung của video cần làm motion!"*

## ❌ Anti-patterns (cấm vĩnh viễn)

- ❌ Tự suy đoán specs/giá/brand khi KHÔNG check wiki (Key #1 fail)
- ❌ Dùng template card giống nhau cho mọi clip (Key #2 fail)
- ❌ Popup card ở cùng thời điểm + vị trí mọi clip (Key #3 fail → nhàm chán)
- ❌ Bỏ qua face zone (Key #4 fail → che mặt anh)
- ❌ Card tràn safe zone 10% (Key #5 fail)
- ❌ Card ở sai vị trí zone (Key #6 fail)
- ❌ Dùng clipPath/2-video wrapper cho PIP (Key #7 fail)
- ❌ Dùng ffmpeg format=yuva420p overlay cho glass (Key #8 fail)
