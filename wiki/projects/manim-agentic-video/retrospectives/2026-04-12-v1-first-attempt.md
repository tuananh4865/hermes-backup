---
title: "Retrospective v1 — Manim Agentic Video (First Attempt)"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [auto-filled]
---

# Retrospective v1 — Manim Agentic Video (First Attempt)

**Date**: 2026-04-12
**Duration of work**: ~2h
**Output**: 101s video, 6 scenes

## What Went Well
- Plan viết chi tiết 6 scenes trước
- Setup conda env + manim thành công
- Tất cả 6 scenes render được, stitch thành video hoàn chỉnh
- Subcaption timing chuẩn

## What Went Wrong (Mistakes)

### Mistake 1: CurvedArrow quá chậm
- **What**: S4 và S5 dùng CurvedArrow → render timeout 180-300s cho một scene
- **Root cause**: Manim's CurvedArrow là một mobject phức tạp, không được tối ưu cho nhiều animated arrows liên tiếp
- **Lesson**: Tránh CurvedArrow trong animation loops. Dùng Line + Create thay thế.
- **Prevention**: Kiểm tra complexity của từng mobject type trước khi viết code. Benchmark nhỏ trước.

### Mistake 2: Animation quá đơn điệu
- **What**: Video "thô sơ và nhàm chán" — chỉ có FadeIn, Write, GrowArrow
- **Root cause**: Không dùng advanced animation techniques (easing, camera movement, kinetic typography, particle effects)
- **Lesson**: Animation cần easing, stagger, camera pan/zoom, color transitions
- **Prevention**: Research kỹ technique trước, thực hành trên draft scene trước khi scale up

### Mistake 3: Script phức tạp quá mức
- **What**: Code cho S5 gây ValueError với array dimensions
- **Root cause**: Thao tác numpy vectors phức tạp không cần thiết cho vị trí đơn giản
- **Lesson**: Keep it simple. Dùng Manim's built-in positioning methods thay vì manual numpy calculations.
- **Prevention**: Test từng scene nhỏ trước khi ghép vào script lớn

### Mistake 4: Không test animation speed trước
- **What**: Một số scene chạy quá nhanh, một số quá chậm
- **Root cause**: Không có preview/check nhanh cho timing
- **Lesson**: Dùng `-ql --format=png -s` để preview stills trước render video
- **Prevention**: Render preview frame đầu tiên của mỗi scene để check visual trước

## Accomplishments
1. ✅ Setup complete Manim environment
2. ✅ 6 scenes hoàn chỉnh, stitch được thành video
3. ✅ Color palette Neon Tech applied consistently
4. ✅ Subcaption timing chuẩn
5. ✅ Script viết clean, có plan.md chi tiết

## Key Lessons for v2
1. **Easing > Linear** — always use rate_func=smooth, there_and_back, etc.
2. **Camera movement = life** — MovingCameraScene for pan/zoom/drift
3. **Kinetic typography** — animate each word/token separately
4. **Particle/flow effects** — add visual texture
5. **Test early, test often** — preview scene nhỏ trước
6. **Simplicity first** — complex mobjects = slow render

## Next Actions (v2)
- Rewrite all 6 scenes với advanced animations
- Add MovingCameraScene for camera movement
- Add kinetic typography với staggered word reveals
- Add particle effects cho visual interest
- Render ở 1080p production quality
- Add audio narration hoặc background music
