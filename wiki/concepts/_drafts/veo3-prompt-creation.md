---
title: VEO3 Prompt Creation
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [ai-video, prompt, veo3, frame-linking, tiktok, epoxy]
confidence: high
relationships: [tiktok-viral-script, tiktok-content-strategy, epoxy-floor-prompts]
---

# VEO3 Prompt Creation

## Executive Summary

VEO3 Prompt Creation là phương pháp tạo video prompts theo chuẩn Google VEO 3, sử dụng cấu trúc "This → Then → That" để liên kết các frame liên tiếp. Phương pháp này đảm bảo AI tạo video với sự chuyển đổi mượt mà từ frame này sang frame tiếp theo, duy trì tính nhất quán về nhân vật, ánh sáng, và các yếu tố trang trí xuyên suốt.

## Core Principle: This → Then → That

Mỗi prompt phải chứa 3 phần bắt buộc:

```
[THIS FRAME]:
→ Mô tả chính xác điểm bắt đầu (y chang ảnh trước đó)

[THEN]:
→ Hành động xảy ra — thay đổi từ THIS sang THAT

[THAT FRAME]:
→ Mô tả chính xác điểm kết thúc (y chang ảnh tiếp theo)
```

### Tại sao cấu trúc này hoạt động

| Thành phần | Vai trò |
|------------|---------|
| **THIS** | Frame bắt đầu (AI đã biết từ prompt trước) |
| **THEN** | Hành động/transition (điểm thay đổi) |
| **THAT** | Frame kết thúc (AI phải tạo ra để nối tiếp) |

### Quy tắc liên kết BẮT BUỘC

> **THAT FRAME của prompt N = THIS FRAME của prompt N+1**

Liên kết này phải khớp nhau hoàn toàn — không được sai khác dù chỉ một chi tiết nhỏ.

## 8-Component Framework

VEO3 cung cấp framework 8 thành phần để tạo prompts chuyên nghiệp:

1. **Subject** — Mô tả nhân vật (15+ thuộc tính vật lý)
2. **Action** — Hành động của nhân vật
3. **Environment/Context** — Bối cảnh, địa điểm
4. **Camera Angle** — Góc máy quay
5. **Lighting** — Ánh sáng
6. **Mood/Style** — Phong cách, cảm xúc
7. **Audio** — Âm thanh (dialogue, ambient)
8. **Temporal** — Thứ tự thời gian, chuyển động camera

## Quality Hierarchy

| Level | Mô tả |
|-------|-------|
| 🥇 MASTER LEVEL | All 8 components + advanced techniques |
| 🥈 PROFESSIONAL | 6-8 components với mô tả chi tiết |
| 🥉 INTERMEDIATE | 4-6 components với basic details |
| ⚠️ BASIC | 1-3 components (kết quả kém) |

## Frame-to-Frame Linking (V5 vs V6)

### V5 (trước)
```
IMAGE 1 → [miêu tả 1 đoạn]
VIDEO 1 → [miêu tả 1 đoạn]  
IMAGE 2 → [miêu tả 1 đoạn]
→ 3 đoạn độc lập, không thấy liên kết
```

### V6 (mới)
```
MỖI PROMPT = 3 PHẦN BẮT BUỘC:
[THIS FRAME] + [THEN] + [THAT FRAME]
→ THAT = THIS prompt tiếp theo (khớp hoàn toàn)
```

## Negative Prompting

```json
{
  "negative_prompt": "no text overlays, no watermarks, no cartoon effects, no unrealistic proportions, no blurry faces, no distorted hands, no artificial lighting, no oversaturation"
}
```

## Audio-Visual Synchronization

### Dialogue and Action Coordination
```json
{
  "prompt": "As she says 'This is our moment,' the character stands from her chair, the camera rising with her movement, while inspirational music builds to emphasize the pivotal moment."
}
```

### Environmental Audio Matching
```json
{
  "prompt": "The busy restaurant scene includes layered audio of clinking glasses, muffled conversations, kitchen sounds, and soft background music, all balanced to support the intimate conversation between the main characters."
}
```

## Related Concepts

- [[epoxy-floor-prompts]] — Ứng dụng VEO3 cho epoxy flooring TikTok
- [[tiktok-viral-script]] — Script framework cho TikTok
- [[tiktok-content-strategy]] — Chiến lược content tổng thể

## References

- VEO 3 MASTER PROMPT.pdf — Nguồn chính
- Structural Aesthetics YouTube video analysis
