---
title: "TikTok CAPTCHA Solver — Miễn Phí 100%"
created: 2026-04-28
updated: 2026-04-28
type: concept
tags: [auto-filled]
---

# TikTok CAPTCHA Solver — Miễn Phí 100%

> Toolkit miễn phí hoàn toàn để bypass TikTok CAPTCHA: puzzle slider, rotate, 3D shapes.

## Giới thiệu

TikTok có 4 loại CAPTCHA chính:
1. **Puzzle Slider** — kéo puzzle piece vào đúng vị trí
2. **Rotate** — xoay ảnh để khớp với reference
3. **3D Shapes** — chọn object cùng hướng
4. **Object Verification** — chọn đúng object theo yêu cầu

Toolkit này giải tất cả **miễn phí** — không cần API key, không cần trả tiền.

## Cài đặt

```bash
pip install opencv-python numpy pillow
```

Hoặc cài tất cả cùng lúc:
```bash
pip install opencv-python numpy pillow requests
```

## Các module

| File | Mô tả |
|------|--------|
| `puzzle_solver.py` | Puzzle Slider — OpenCV template matching |
| `rotate_solver.py` | Rotate CAPTCHA — HoughCircles + template matching |
| `shapes_solver.py` | 3D Shapes — MiniMax Vision |
| `human_drag.py` | Human-like slider movement |
| `stealth_browser.py` | Stealth browser wrapper (playwright-stealth) |
| `tiktok_solver.py` | Orchestrator — gọi đúng solver theo loại CAPTCHA |

## Cách sử dụng

```python
from tiktok_solver import TikTokCaptchaSolver

solver = TikTokCaptchaSolver()

# Hoàn thành CAPTCHA với human-like movement
solver.solve_and_drag(page, captcha_type="puzzle")
```

## Cấu trúc project

```
tiktok-captcha-solver/
├── README.md
├── puzzle_solver.py
├── rotate_solver.py
├── shapes_solver.py
├── human_drag.py
├── stealth_browser.py
├── tiktok_solver.py
└── examples/
    └── demo.py
```

## Cách hoạt động

### Puzzle Slider
1. Extract ảnh background và puzzle piece từ DOM
2. OpenCV `matchTemplate()` tìm vị trí khớp
3. Tính khoảng cách cần kéo
4. Human-like drag

### Rotate
1. Extract inner circle và outer image
2. HoughCircles tìm tâm
3. Template matching tìm góc lệch
4. Tính pixel cần kéo

### 3D Shapes
1. Chụp ảnh CAPTCHA
2. Gửi cho MiniMax Vision API
3. Nhận hướng xoay
4. Tính pixel

### Human-like Drag
- Bezier curve thay vì đường thẳng
- Random pause + speed variation
- Không đi quá "hoàn hảo"

## Lưu ý

- **verify_fp token** vẫn cần hoàn thành CAPTCHA 1 lần bằng tay
- Proxy giảm 50% CAPTCHA rate
- Stealth browser giảm 80% CAPTCHA rate
- Không hoạt động nếu IP bị TikTok ban hoàn toàn
