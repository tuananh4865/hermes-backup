# Denoise Flag Investigation — 2026-07-24

**Context:** Anh hỏi "Tại sao dùng file clone để tạo voice lại bị leak ref vậy? Check kĩ lại cách clone voice của omnivoice đi" — em đã A/B test 6 variants để tìm root cause.

**Root cause:** `OmniVoiceGenerationConfig.denoise=True` (default) prepend `<|denoise|>` token NGĂN leak ref text. `denoise=False` → model echo ref text đầu output.

## A/B Test Setup

- **Voice ref:** `tuan_anh_v5_aggressive_denoise.pt` (10s aggressive denoise)
- **Target text:** "Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng OmniVoice trên máy Mac nhé."
- **Ref text trong .pt:** "Xin chào, tôi là Tuấn Anh đây. Tôi là Tuấn Anh đây nè."
- **Config NGUYÊN THỦY:** chỉ thay đổi 1 flag/turn, giữ nguyên 2 flag còn lại

## Results (6 variants)

| Variant | denoise | preprocess | postprocess | Whisper transcript | Has Target | Has Ref Leak | Verdict |
|---|---|---|---|---|---|---|---|
| A_default | True | True | True | "Trài Trồi Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng OmniVoice trên máy mát nhé" | ✅ | ❌ | ✅ CLEAN |
| B_no_denoise | False | True | True | "Trời ơi là Tuấn Anh đây Trời ơi Tôi là Tuấn Anh đây nè Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng Omnivoice trên máy mát nhé" | ✅ | ⚠️ LEAK | ❌ |
| C_no_preprocess | True | False | True | "Mình sẽ hướng dẫn chi tiết cách sử dụng Omni Voice trên máy mát nhé." | ✅ | ❌ | ✅ CLEAN |
| D_no_postprocess | True | True | False | "Chào! Anh Mắc đây nè! Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng Omni Voice trên máy mát nhé!" | ✅ | ❌ | ✅ CLEAN |
| E_no_denoise_preproc | False | False | True | "à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à" | ❌ | ❌ | ❌ NO TARGET |
| F_all_off | False | False | False | "Tui Tuấn Ao, tui là Tuấn Anh đây nè. Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng Omnivoice trên máy Mac nhé." | ✅ | ⚠️ LEAK | ❌ |

## Cơ chế

OmniVoice architecture prepends `<|denoise|>` token khi `denoise=True` (default). Token này signal cho model:
- **CÓ denoise token** → model "biết đây là denoise mode" → chỉ generate target text, KHÔNG echo ref text
- **KHÔNG có denoise token** → model echo ref text đầu output, rồi mới target text

```
Input:  [<|denoise|>] + ref_audio_tokens + ref_text + target_text
Output: target_text audio (khi CÓ denoise token)
        ref_text echo + target_text audio (khi KHÔNG CÓ denoise token)
```

## Default config RECOMMENDED

```python
gc = OmniVoiceGenerationConfig(
    pad_duration=0.0,        # NO PADDING (Pitfall #6)
    fade_duration=0.0,       # NO FADE
    denoise=True,            # ← EXPLICIT (Pitfall #9) — prevent ref leak
    preprocess_prompt=True,  # standard
    postprocess_output=True, # standard
)
```

## Test với script đơn giản (1 câu) — 4 voice clone variants

Sau khi tìm root cause, em test lại 4 file voice clone với script ĐƠN GIẢN:

| Version | Duration | Peak (dB) | Whisper (target) | Ref Leak? |
|---|---|---|---|---|
| v1 GOOJODOQ | 3.44s | -4.5 | ✅ Đúng 100% | ✅ CLEAN |
| v3 voice_msg_10s | 6.40s | -3.4 | ✅ Đúng | ✅ CLEAN |
| v4 voice_msg_clean | 12.66s | -4.1 | ✅ Đúng (có "Về" echo 1 từ) | ✅ CLEAN |
| v5 aggressive | 8.41s | **-0.3** | ✅ Đúng (có "Nè" echo 1 từ) | ✅ CLEAN |

**Kết luận:** Với script đơn giản + denoise=True explicit → 4/4 phiên bản CLEAN. V1 GOOJODOQ là tốt nhất (không có echo).

## Echo 1-2 từ ở đầu là BÌNH THƯỜNG

Với `denoise=True`, Whisper có thể detect "Nè" hoặc "Túng đây" ở đầu output (1-2 từ cuối ref_text echo). Đây là **behavior bình thường** của OmniVoice, KHÔNG phải leak. Leak THẬT là cả câu ref text lặp lại (variant B, F).

## Lessons learned

1. **Test đơn giản trước, phức tạp sau** — Anh explicit 24/07: "Test với script đơn giản nào đó đi". Script 1 câu → clean hơn 6 câu.
2. **A/B test khi có bug** — 6 variants × 1 target = 6 lần generate, save hours debugging.
3. **Default config không luôn work** — `denoise=True` default work, NHƯNG phải explicit set để guard rail.
4. **Echo 1-2 từ ≠ leak** — Whisper detect được không có nghĩa là model leak.

## Anti-patterns

- ❌ KHÔNG tắt `denoise=False` nếu không có lý do đặc biệt
- ❌ KHÔNG tắt cả `preprocess_prompt=False` + `denoise=False` (variant E = lặp vô tận)
- ❌ KHÔNG assume "echo 1 từ" = leak cả câu
- ❌ KHÔNG test script phức tạp (6 câu) khi script đơn giản (1 câu) chưa work
