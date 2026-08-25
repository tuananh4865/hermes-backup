---
name: tiktok-kinetic-liquid-glass-editor
description: Quy trình dựng video TikTok Shop / Affiliate hoàn chỉnh (Talking Head + Tái cấu trúc phi tuyến tính Problem-Solution + Cắt khoảng lặng >0.15s + Kính Lỏng Pure Liquid Glass + Dynamic Kinetic Text Animation IN/OUT + Mã hóa FFmpeg Pipe).
allowed-tools: client
---

# TikTok Kinetic Liquid Glass Product Video Editor

## Overview
Bộ quy chuẩn và kịch bản dựng video TikTok Shop / Affiliate chuyên nghiệp cho Tuấn Anh. Kết hợp Tái cấu trúc kịch bản phi tuyến tính (Problem - Solution Framework), Cắt bỏ triệt để khoảng lặng >0.15s (De-gapping), Kính Lỏng (Pure Refractive Liquid Glassmorphism), Phông chữ 100% Native Tiếng Việt, Bóng đổ đồng tâm tự nhiên (Centered Soft Shadow) và Chuyển động chữ đa dạng IN / OUT (Kinetic Text Animation).

---

## 🚀 Quy Trình Dựng Video Chi Tiết Từ Đầu Đến Cuối

### Bước 1: Trích xuất Audio từ RAW Footages
1. **Định danh Tệp RAW**: Tất cả video phải được cắt trực tiếp từ tệp gốc trong `/Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4`.
2. **Trích xuất Âm thanh Gốc**: Tách tệp WAV mono 16kHz PCM bằng FFmpeg:
   ```bash
   /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -y -i /Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/source_audio.wav
   ```

### Bước 2: Tái Cấu Trúc Phi Tuyến Tính (Problem - Solution Framework)
1. **Whisper Word-Level Timestamp Analysis**: Trích xuất tệp JSON lời thoại chi tiết đến từng từ (`start`, `end`, `word`).
2. **Sắp xếp lại Ma trận Kịch bản theo 6 Chương**:
   * **0s – 4s: SUPER HOOK**: Chọn câu giật tít / nỗi đau va chạm nhất bốc lên ngay 00:00.
   * **4s – 15s: PROBLEM / PAIN POINT**: Nêu sự bất tiện, rủi ro hay hậu quả nếu dùng cách cũ.
   * **15s – 30s: SOLUTION REVEAL**: Giới thiệu sản phẩm xuất hiện như cứu tinh.
   * **30s – 60s: USP & FEATURES**: Trình bày tính năng độc bản & trải nghiệm thực tế.
   * **60s – 70s: HONEST FLAW / HIGH TRUST**: Nhận xét chân thực tăng độ uy tín 100%.
   * **70s – 80s: STRONG CTA**: Thúc giục bấm giỏ hàng góc dưới bên trái.

### Bước 3: Cắt Sạch Khoảng Lặng > 0.15s (Strict De-Gapping Rule) & Tăng Tốc 1.3x
1. **CẮT SẠCH KHOẢNG LẶNG > 0.15s (HARD RULE)**:
   * Đo khoảng thời gian trống giữa từ trước và từ sau: `gap = start_next - end_prev`.
   * Nếu `gap > 0.15s`, cắt bỏ toàn bộ đoạn khoảng lặng thừa.
   * Giữ nhịp thoại dồn dập, liên tục, tuyệt đối không có đoạn nghỉ trống (dead air).
2. **Speed Up & Audio Fade**:
   * Tăng tốc video `setpts=PTS/1.3` và audio `atempo=1.3`.
   * Áp dụng audio fade 30ms cho từng điểm nối (`afade=t=in`, `afade=t=out`).
   * Xuất tệp base video 1080x1920 @ 30fps (`/tmp/clip_base.mp4`).

### Bước 4: Quy Chuẩn Vị Trí & Vùng Cấm Đặt Chữ (Exclusion Zone)
1. **Hook (0s – 4s)**:
   * **Kinetic Text Motion thuần túy ở Dải Trên (`top: 240px`)**. KHÔNG dùng khung Card.
2. **Thân Video & CTA (4s – 80s)**:
   * **80% Motion Text / Accent Pills đặt ở Dải Dưới (`top: 1320px..1340px`)**.
   * **Vùng Cấm Đặt Chữ Nặng (Center Exclusion Zone - `Y: 500px..1250px`)**: Giữ trống hoàn toàn dải trung tâm để hiển thị rõ ràng gương mặt và sản phẩm trên tay.
3. **Phông Chữ Native 100% Tiếng Việt**:
   * Tiêu đề chính: `Arial Bold.ttf` (`/System/Library/Fonts/Supplemental/Arial Bold.ttf`).
   * Cụm từ nhấn mạnh: `Verdana Bold.ttf` (`/System/Library/Fonts/Supplemental/Verdana Bold.ttf`).
   * Mô tả phụ: `Arial.ttf` (`/System/Library/Fonts/Supplemental/Arial.ttf`).

### Bước 5: Kính Lỏng (Pure Liquid Glass) & Bóng Đồng Tâm
1. **Pure Liquid Glass Compositing**:
   * Crop background dưới vị trí Card.
   * Áp dụng `GaussianBlur(radius=28)` (~40px CSS equivalent) + `Color Enhancer(saturate=1.60..1.80)`.
   * Phủ lên mask bo góc `radius=36px`. KHÔNG dùng viền stroke trắng hay màng đục.
2. **Bóng Đổ Đồng Tâm (Centered Shadow Mask)**:
   * Canvas đệm rộng (`pad = 200px`) chống xén mép bóng.
   * Tọa độ đồng tâm (`dy = 0`) tỏa đều 4 phía.
   * Mask hở nhẹ `outset = 12px` + `GaussianBlur(radius=24px)`, opacity ~25% (`fill=(0, 0, 0, 80)`).

### Bước 6: Dynamic Text Animation IN & OUT Patterns
Luân phiên 4 kiểu chuyển động chữ (Kinetic Text Animation) trên từng phân đoạn:
1. **Pattern 1: Pop-In Overshoot & Scale Out**: Scale `0.85 -> 1.05 -> 1.0` khi vào, `1.0 -> 0.9` khi out.
2. **Pattern 2: Slide-Up Bounce IN & Slide-Up OUT**: Slide từ dưới `+45px -> 0px` khi vào, slide `-35px` khi out.
3. **Pattern 3: Kinetic Slide Left-Right**: Slide ngang từ trái `-60px -> 0px` khi vào, slide phải `+60px` khi out.
4. **Pattern 4: Elastic Scale & Soft Fade**: Scale `0.80 -> 1.0` khi vào, mờ dần khi out.

### Bước 7: Đóng Gói & Xuất Bản qua FFmpeg Pipe
1. Render từng frame 1080x1920 @ 30fps qua luồng pipe (stdin) vào `ffmpeg-full` (`-crf 18`, `-preset fast`, `-pix_fmt yuv420p`).
2. Ghép trực tiếp âm thanh AAC gốc và xuất sang `/Volumes/Storage-1/Pocket3/Hermes-Edit/pipeline/output/_ready_to_ship/clip_<name>_V2_81s_FINAL.mp4`.

---

## 🛠️ Mã Nguồn Tự Động Hóa (Scripts)
Chạy script đính kèm tại `scripts/render_pipeline.py`:
```bash
python3 /Volumes/Storage-1/Hermes/skills/tiktok-kinetic-liquid-glass-editor/scripts/render_pipeline.py --input /Volumes/Storage-1/Pocket3/Footages/DJI_20260721094041_0030_D.MP4 --out_name clip_0030_V2_81s_FINAL.mp4
```

## Gotchas & Verification Checklist
- [ ] Cắt sạch tất cả khoảng lặng > 0.15s (de-gapping).
- [ ] Không có ký tự ô vuông (`□`) hay lỗi dấu tiếng Việt.
- [ ] Không có viền stroke trắng hay màng đục đen/xám trên card kính.
- [ ] Không bị xén mép bóng đổ (`pad = 200px`).
- [ ] Không để chữ hay card đè lên khuôn mặt hoặc tay giơ sản phẩm (`Y: 500px..1250px`).
- [ ] Tệp video xuất bản được kiểm tra qua `ffprobe` và đính kèm link `file://`.
