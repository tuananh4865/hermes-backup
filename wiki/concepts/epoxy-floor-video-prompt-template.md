---
title: EPOXY FLOORING Video Prompt Template
created: 2026-04-20
updated: 2026-04-20
type: concept
tags: [tiktok, ai-video, prompt-template, epoxy, timelapse, frame-linking, veo3]
confidence: high
relationships: [tiktok-content-strategy, tiktok-viral-script, video-prompt-engineering]
---

# EPOXY FLOORING Video Prompt Template

**Nguồn:** Conversation with Tuấn Anh about EPOXY FLOORING TikTok video prompt creation workflow
**Reference Video:** "Stunning Epoxy River Stone Floor with Suspended Bed" by @Structural.Aesthetics — https://www.youtube.com/shorts/ll9aQM6_w_c

## Overview

Framework for creating high-quality vertical TikTok videos showing epoxy flooring installation using AI video generation (VEO 3). The template evolved through 6 versions to address consistency, frame-linking, and timelapse structure issues.

## Key Concepts

### 8-Stage Timelapse Sequence

| Stage | Action | Workers Present |
|-------|--------|-----------------|
| 1 | Pour pebbles/mortar | ✅ |
| 2 | Spread evenly | ✅ |
| 3 | Pour epoxy/resin | ✅ |
| 4 | Self-leveling | ❌ (无人) |
| 5 | Polish/final touches | ✅ |
| 6 | Empty completed surface | ✅ |
| 7 | Install hero furniture | ✅ |
| 8 | Final reveal | ❌ (无人) |

### Worker Consistency Rules

- **Count:** 2-4 workers, same outfit throughout ALL stages
- **Colors:** Dark only — black, grey, navy. NO bright colors
- **Entry/Exit:** Workers enter/exit at each stage (except self-level and final reveal)
- **Camera:** Static wide-angle corner, eye-level, 25mm equivalent

### Decorative Elements

- **Black iron chain:** Hangs from ceiling center in EVERY frame — visual anchor
- **Lighting:** Natural window light (NOT fluorescent)
- **Hero furniture:** Floating bed/sofa — carried in, positioned, installed with visible labor

## Template Evolution

| Version | Key Change |
|---------|------------|
| V1 | Initial template |
| V3 | Added frame-to-video linking + worker consistency |
| V4 | Based on real video analysis (Structural Aesthetics) |
| V5 | Explicit frame-to-frame linking |
| V6 | **"This → Then → That" chaining** (VEO 3 standard) |

## VEO 3 "This → Then → That" Structure

Each prompt = 3 mandatory parts:

```
[THIS FRAME]:
→ Mô tả chính xác điểm bắt đầu (y chang ảnh trước đó)

[THEN]:
→ Hành động xảy ra — thay đổi từ THIS sang THAT

[THAT FRAME]:
→ Mô tả chính xác điểm kết thúc (y chang ảnh tiếp theo)
```

### Critical Rule

> **THAT FRAME của prompt N = THIS FRAME của prompt N+1**
> 
> Liên kết này **BẮT BUỘC** phải khớp nhau hoàn toàn.

### Why "This → Then → That" Works

- THIS = Frame bắt đầu (cái AI đã biết từ prompt trước)
- THEN = Hành động/transition (cái thay đổi)
- THAT = Frame kết thúc (cái AI phải tạo ra để nối tiếp)

## VEO 3 MASTER PROMPT Rules

From PDF extraction:

1. **All prompts in CODE BLOCK, one prompt per line, separated by newline**
2. **Each prompt has scene number** corresponding to SCENE number
3. **Each prompt is INDEPENDENT** — no cross-referencing
4. **Prompts are like CODE** — need exact precision, 100% copy-paste

## Common Issues Fixed

| Problem | Solution |
|---------|----------|
| No connection between frames | V5 frame-to-frame linking |
| Workers inconsistent | Worker identity sheet with exact outfits |
| Furniture appears magically | Workers carry/position/install with visible labor |
| Not timelapse | Stage-by-stage with workers entering/exiting |
| V6 format still wrong | User feedback — needs clarification on scene numbering, format, THIS/THEN/THAT |

## Current Status

- **Latest:** V6 with This → Then → That chaining
- **Blocker:** User says V6 format still doesn't match VEO 3 standards
- **Pending:** Clarification on scene numbering, code block format, IMAGE/VIDEO order

## Related Concepts

- [[tiktok-content-strategy]]
- [[tiktok-viral-script]]
- [[video-prompt-engineering]]
