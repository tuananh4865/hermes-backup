---
title: Epoxy Floor Prompts
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [ai-video, prompt, epoxy, tiktok, timelapse, frame-linking, veo3]
confidence: high
relationships: [veo3-prompt-creation, tiktok-viral-script, tiktok-content-strategy]
---

# Epoxy Floor Prompts

## Executive Summary

Epoxy Floor Prompts là bộ templates để tạo TikTok video prompts cho nội dung epoxy flooring (sàn đá phủ epoxy). Hệ thống đã phát triển qua 6 phiên bản (V1→V6), từ basic prompts đến professional-grade với frame-to-frame linking theo chuẩn VEO3 "This → Then → That".

## Evolution Timeline

| Version | Key Change |
|---------|------------|
| V1 | Initial basic prompts |
| V2 | Frame-to-video linking formula |
| V3 | Added worker identity consistency |
| V4 | Structural Aesthetics formula — 8-stage timelapse |
| V5 | Explicit frame-to-frame labels [START/END/TYPE] |
| V6 | "This → Then → That" chaining — mandatory THIS=THAT matching |

## 8-Stage Timelapse Workflow

Đây là narrative sequence chuẩn cho epoxy flooring video:

```
Stage 1: Pour pebbles/mortar onto floor
Stage 2: Spread evenly  
Stage 3: Pour epoxy/resin
Stage 4: Self-level (NO workers present)
Stage 5: Polish/final touches
Stage 6: Empty completed floor surface
Stage 7: Install hero furniture (floating bed)
Stage 8: Final reveal (NO workers present)
```

## V6 Prompt Structure (This → Then → That)

Mỗi prompt gồm 3 phần bắt buộc:

```
[FRAME NUMBER]: N
[FRAME TYPE]: THIS FRAME — Starting point
[CAMERA]: Fixed wide corner angle, static, eye-level

[THIS FRAME]:
Mô tả chính xác điểm bắt đầu (y chang ảnh trước đó)

[THEN]:
Hành động xảy ra — thay đổi từ THIS → THAT

[THAT FRAME]:
Mô tả chính xác điểm kết thúc (y chang ảnh tiếp theo)
```

### Quy tắc liên kết BẮT BUỘC

> **THAT FRAME của prompt N = THIS FRAME của prompt N+1**

## Consistency Rules

### Worker Identity
- **2-4 workers** với **cùng outfit** xuyên suốt tất cả stages
- **Dark colors only**: black, grey, navy — KHÔNG bright colors
- Workers enter/exit at appropriate stages
- White caps và gloves acceptable

### Mandatory Visual Elements
| Element | Requirement |
|---------|-------------|
| **Decorative Chain** | Black iron chain hanging from ceiling trong TẤT CẢ frames |
| **Lighting** | Natural window light from left (KHÔNG fluorescent) |
| **Camera** | Completely static wide-angle corner view |
| **Hero Item** | Floating bed with black chains as final reveal |

## V5 vs V6 Comparison

| Aspect | V5 (trước) | V6 (mới) |
|--------|-----------|----------|
| IMAGE/VIDEO | Viết riêng | THIS/THEN/THAT trong 1 prompt |
| Liên kết | Ngầm | Rõ ràng: THAT = THIS prompt tiếp |
| Worker | Worker sheet riêng | Mô tả TRONG từng transition |
| Chain | Nhắc riêng | Trong TỪNG frame |

## Files Created

- `learning/epoxy-floor-content/epoxy-floor-prompt-template-v6.md`
- `learning/epoxy-floor-content/examples/living-room-v6/test-run-v6.md`

## References

- **Video reference**: "Stunning Epoxy River Stone Floor with Suspended Bed" by @Structural.Aesthetics
- **YouTube**: https://www.youtube.com/shorts/ll9aQM6_w_c
- **Concept**: [[veo3-prompt-creation]] — VEO3 framework cơ bản
