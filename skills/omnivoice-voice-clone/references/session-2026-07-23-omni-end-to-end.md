# Session 23/07 — End-to-end corrections & lessons captured

**Session date:** 2026-07-23
**Duration:** ~3 hours of OmniVoice testing
**Outputs:** 5 working production files + 1 shippable TikTok clip (28s)

## 9 user push-backs in this session — embedded into SKILL.md User Preferences table

| # | Verbatim | Lesson |
|---|---|---|
| 1 | "Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu" | **Save .pt, don't re-encode.** VoiceClonePrompt 5x speedup. |
| 2 | "Tốt rồi! Nhưng Lúc em prompt omnivoice có vấn đề gì đó... chỉ cần fix prompt lại không inject câu đó vào nữa thôi!" | **Test variants, don't workaround.** 4 ref_text variants > Whisper trim hack. |
| 3 | "Đọc hết phần readme của repo chưa?" | **Skip = explicit decision.** Enumerate all README links; silent skip = bug. |
| 4 | "Anh thấy có phần Non-verbal & Pronunciation Control khá hay cộng thêm các key feature để thêm cảm xúc cho giọng đọc khiến cho giọng đọc giống người hơn!" | **Emotion tags = free voice quality.** 10/10 PASS, peak -2 dB vs baseline -4 dB. |
| 5 | "Khi em ghép batch lại với nhau thì để fadeout nhẹ thôi 30ms thôi" | **Concat fade CHỈ 30ms.** No fade-in. |
| 6 | "Không fade không trim luôn audio bỏ padding 100ms luôn" | **Disable padding from generate** (`pad_duration=0`). Don't trim/fade after. |
| 7 | "Emotion tag cũng phải bắt buộc" | **Emotion tags BẮT BUỘC mỗi segment.** Voice phẳng = chưa đạt chuẩn. |
| 8 | "Bỏ chữ tiktok đi chỉ cần anh nói tạo voice là em dùng omnivoice tạo voice cho anh" | **Trigger "tạo voice" = any purpose** (podcast, audiobook, narration, v.v.). Not just TikTok. |
| 9 | "Lúc nãy anh có nói lưu cách dùng voice ref là sai rồi, đúng phải là cách dùng file voice clone" | **Terminology:** "file voice clone (.pt)" NOT "voice ref". The .pt is the encoded artifact, not raw audio. |

## Meta-pattern (codified as class-level lesson)

Anh's correction pattern across all 9 push-backs:
1. **Root-cause fix, not workaround** — never defend current approach
2. **Precise terminology** — naming matters, vague terms hide misunderstandings
3. **Mandatory rules** — when anh says "BẮT BUỘC", it's not optional
4. **Embed corrections into SKILL.md body**, not just memory — skills capture "how to do this class of task", memory captures "who + state"

## 6 pitfalls caught during this session

| # | Pitfall | Status |
|---|---|---|
| 1 | MPS batch bug ≥5 text | Documented, workaround: sequential 1-by-1 |
| 2 | ref_rms < 0.1 amplitude bug | Fixed in skill — amplify before save |
| 3 | ref_text > 120 chars → leak | Fixed in skill — ref_text ≤ 100 chars |
| 4 | TikTok CDN may return watermark audio | Documented in pitfall #4 |
| 5 | HiggsAudioV2Tokenizer MPS crash | Auto-handled by OmniVoice |
| 6 | Concat gap 100ms lead/trail silent | **Resolved** — disable padding from generate (`pad_duration=0, fade_duration=0`) |

## Production artifacts

- `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt` (9.9KB) — current voice clone template
- `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/tiktok_VIDEO_REF_FINAL_EMO.wav` (28.04s, max -2.4 dB) — shippable TikTok clip with emotion tags

## Key insight for next session

When user says "tạo voice" → follow SKILL.md workflow:
1. **Check** `/Volumes/Storage-1/Hermes/voice-prompts/` — file .pt có sẵn chưa?
2. **NẾU CÓ** → load + generate với emotion tags
3. **NẾU CHƯA** → ref audio → amplify → save .pt → generate

**Never re-encode ref audio mỗi lần** — load file .pt đã save.

**Never skip emotion tags** — voice mặc định có emotion, baseline phẳng = chưa đạt chuẩn.

**Never call it "voice ref"** — it's a "file voice clone (.pt)" (encoded VoiceClonePrompt).
