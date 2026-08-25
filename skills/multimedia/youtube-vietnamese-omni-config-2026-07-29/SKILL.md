---
name: youtube-vietnamese-omni-config-2026-07-29
description: "YouTube Vietnamese voice config sweep 11 variants."
---

# YouTube Vietnamese Omni Config (29/07 sweep)

**Context:** `~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py` với 1 take full (3.032 từ, 13.6 KB text, voice clone `tuan_anh_5s_1sent_amp.pt`, ref_rms=0.1100). Mục tiêu: không filler, không cắt đầu/cuối, không bị gap khó chịu giữa câu.

**A/B sweep kết quả (11 variants trên cùng 3 câu test):**

| Variant | layer | position | pad  | fade | speed | Whisper coverage | Filler ựm/ờ | Đầu câu 1 | Đầu câu 2+ |
|---------|-------|----------|------|------|-------|------------------|---------------|-----------|------------|
| A_default | 5.0   | 5.0      | 0.1  | 0.1  | 0.95  | 95%              | có           | OK        | clip       |
| B_L2P3.5P0.2F0.1 | 2.0 | 3.5    | 0.2  | 0.1  | 0.90  | 97%              | ít           | OK        | OK         |
| C_L1.5P3.5P0.2  | 1.5 | 3.5    | 0.2  | 0.0  | 0.90  | 99%              | rất ít       | OK        | OK         |
| D_L1.5P3.5P0.2F0.1 | 1.5 | 3.5 | 0.2 | 0.1 | 0.90  | 98%              | rất ít       | OK        | OK         |
| E_L1.5P3.7P0.2  | 1.5 | 3.7    | 0.2  | 0.0  | 0.90  | 99%              | rất ít       | OK        | OK         |
| F_L4P3.5P0.05   | 4.0 | 3.5    | 0.05 | 0.1  | 0.90  | 96%              | có           | OK        | clip nhẹ  |
| G_L1.5P3.5P0.15 | 1.5 | 3.5    | 0.15 | 0.0  | 0.90  | 96%              | có           | OK        | dính câu  |
| H_L1.5P2.5P0.05 | 1.5 | 2.5    | 0.05 | 0.1  | 0.90  | 98%              | rất ít       | OK        | OK         |
| I_L1.5P3.5P0.2_full | 1.5 | 3.5 | 0.2 | 0.1 | 0.90 | 12:24 full take | 0 | clean | clean |
| J_L1.5P3.5P0.2_speed90 | 1.5 | 3.5 | 0.2 | 0.0 | 0.90 | full | 0 | clean | clean |
| K_full_speed0.90 | 4.0 | 3.5 | 0.2 | 0.0 | 0.90 | full | 0 | clean | clean |

**Verdict cuối:** Variant **C / E** (`layer=1.5, position=3.5 hoặc 3.7, pad=0.2, fade=0.0, speed=0.90`) thắng trên cả 3 tiêu chí:
- Đầu/cuối sạch (Whisper nghe đủ)
- Filler "ựm/ờ" gần như không có
- Nhịp nghỉ giữa câu tự nhiên

**Anh verdict (29/07):** "Bản số 3 OK" (tức pad=0.2, fade=0, layer=1.5, position=3.5, speed=0.90).

## Production config (verified full take 12:24)

```python
OmniVoiceGenerationConfig(
    pad_duration=0.2,            # 200ms silence model chèn đầu/cuối mỗi chunk
    fade_duration=0.0,           # NO FADE
    denoise=True,                # ngăn leak ref text
    layer_penalty_factor=1.5,    # smooth without over-merging
    position_temperature=3.5,    # natural prosody
)
# Plus: model.generate(..., speed=0.90)  # chậm 10% so với default
```

## Công thức giải thích nhanh cho user

`layer_penalty_factor`:
- Thấp (1.0 đến 2.0): các layer decoder được phép khác nhau, voice nối mượt, đỡ ngắt quãng.
- Cao (4.0 đến 5.0): các layer phải đồng thuận, voice rời rạc, Whisper hay bắt sai từ.
- Sweet spot cho narration: 1.5.

`position_temperature`:
- Thấp (nhỏ hơn 3.0): bám pattern đào tạo, an toàn nhưng phẳng.
- Cao (5.0): linh hoạt nhưng dễ thêm filler "ờm/à".
- Sweet spot: 3.5.

`pad_duration` vs `fade_duration`:
- `pad`: silence CỨNG ở 2 đầu mỗi chunk. 0.2 = 200ms đệm.
- `fade`: fade-in/fade-out mượt ở 2 đầu. 0 = tắt.
- Sweet spot cho narration: pad=0.2, fade=0, khoảng lặng cứng 200ms, không mờ.

`speed`:
- Default 1.0. 0.95 = 5% chậm. 0.90 = 10% chậm.
- Sweet spot: 0.90 (anh verdict 29/07).

## Cập nhật skill

Đã tham chiếu từ `omnivoice-smooth-config-and-leak-prevention` SKILL.md vào file này để giữ skill mẹ ngắn gọn.
