# Session 2026-07-24 Lessons — Verification + Root Cause Discoveries

5 corrections từ Tuấn Anh + 2 root cause investigations từ session này. Embed these lessons in any future OmniVoice session.

---

## Correction #1: "voice ref" terminology — SAI

**Verbatim:** *"Lúc nãy anh có nói lưu cách dùng voice ref là sai rồi, đúng phải là cách dùng file voice clone"*

**Em đã sai:** Ghi trong memory fact 10 là "voice ref usage" → gợi ý raw audio cần import mỗi lần.

**Đúng:** "file voice clone `.pt`" = VoiceClonePrompt đã encode từ ref audio + ref_text. File `.pt` được LOAD, raw audio KHÔNG được re-encode.

**Codified:** SKILL.md "TERMINOLOGY GHI NHỚ" block, L1 lesson.

---

## Correction #2: Bỏ scope "TikTok" — chỉ cần "tạo voice"

**Verbatim:** *"Bỏ chữ tiktok đi chỉ cần anh nói tạo voice là em dùng omnivoice tạo voice cho anh"*

**Em đã sai:** SKILL description focus vào TikTok content, trigger quá hẹp.

**Đúng:** Trigger "tạo voice" tổng quát. Use case phổ biến: TikTok, YouTube, podcast, audiobook, narration, video voiceover.

**Codified:** Description mở rộng + "When to use" table row 1.

---

## Correction #3: Emotion tags BẮT BUỘC (không optional)

**Verbatim:** *"Emotion tag cũng phải bắt buộc"*

**Em đã sai:** Ghi emotion tags là "nên thêm" (optional suggestion).

**Đúng:** Mỗi segment PHẢI có ≥1 emotion tag. Voice TikTok mặc định có emotion. Baseline phẳng = chưa đạt chuẩn.

**Mapping chuẩn:**
- HOOK = `[surprise-oh]` + `[laughter]` (dừng scroll)
- PROBLEM = `[sigh]` (empathy, chạm pain point)
- SOLUTION = (không tag, authoritative)
- USP = `[question-ah]` (engaging)
- CTA = `[laughter]` + `[confirmation-en]` (friendly call action)

**Codified:** SKILL.md L4 + "When to use" row 6, Recipe 12.

---

## Correction #4: Test với script ĐƠN GIẢN trước

**Verbatim:** *"Test với script đơn giản nào đó đi"*

**Em đã sai:** Default test luôn dùng 6-câu TikTok review script (phức tạp).

**Đúng:** Test 1 câu ngắn trước → A/B 4 file voice clone cùng script → biết file nào work tốt nhất trước khi scale lên 6 câu.

**Result 24/07 (real example):** 1 câu "Chào mọi người, hôm nay mình sẽ chia sẻ về cách sử dụng OmniVoice." → 4/4 file voice clone CLEAN (no leak), Whisper transcript chính xác. Trước đó với 6-câu script thì 2/4 có leak.

**Codified:** SKILL.md L7.

---

## Correction #5: Root cause ngắt quãng giọng — `layer_penalty_factor=5.0`

**Verbatim:** *"Em prompt kiểu gì mà voice đầu ra tệ quá vậy? Giọng thì rõ nhưng ngắt quãng rất khó chịu"*

**Em đã sai:** Apply default config mà không verify output quality. Whisper transcript "dòng colo" (sai) thay vì "giọng clone" (đúng).

**Root cause (verified 7 variants A/B test):**
- `layer_penalty_factor=5.0` (default) → model OVER-PENALIZE tokens → prosody jerky + Whisper transcript sai
- `layer_penalty_factor=1.0` → voice mượt + Whisper transcript chính xác

**Fix:** `OmniVoiceGenerationConfig(layer_penalty_factor=1.0, position_temperature=3.0)`, plus `model.generate(speed=0.95)`.

**Codified:** SKILL.md "BẮT BUỘC — Default smooth config" block + L5.

---

## Root Cause Investigation #1: Tại sao voice clone leak ref text?

**User asked:** "Check kĩ lại cách clone voice của omnivoice đi"

**Hypothesis tested (6 variants):**
1. `default` (denoise=True) → CLEAN
2. `denoise=False` → **LEAK** (output echo ref text đầu)
3. `preprocess_prompt=False` → CLEAN
4. `postprocess_output=False` → CLEAN
5. `denoise=False + preprocess_prompt=False` → LỖI NẶNG (à lặp vô tận)
6. `all_off` → LEAK

**Root cause:** `denoise=True` prepend `<|denoise|>` token → NGĂN leak. Model architecture:
```
Input:  [<|denoise|>] + ref_audio_tokens + ref_text + target_text
Output: target_text audio (với <|denoise|>)
        ref_text echo + target_text audio (KHÔNG <|denoise|>)
```

**Fix:** LUÔN giữ `denoise=True` (Pitfall #9 added).

**Codified:** SKILL.md L3 Pitfall #9.

---

## Root Cause Investigation #2: Tại sao voice ref lặp lại vẫn leak?

**User clarification:** *"Voice này anh ghi âm lặp là do anh muốn thể hiện nhiều biểu cảm khác nhau!"*

**Em đã sai assume:** Voice ref lặp = lỗi ghi âm, phải chọn clip khác.

**Đúng:** User CỐ Ý lặp để model học emotion range. Vẫn leak cụm, NHƯNG model capture emotion tốt hơn.

**Workaround:** Dùng emotion tags + instruct "vui vẻ, nhiều cảm xúc" để đè cảm xúc. Hoặc chọn clip khác đa dạng câu hơn.

**Codified:** SKILL.md L3 Pitfall #8 (distinct from #7).

---

## Critical Reminders for Future Sessions

1. **"File voice clone" terminology** — KHÔNG nói "voice ref" (gợi ý raw audio)
2. **Trigger "tạo voice"** — bao gồm MỌI use case, không giới hạn TikTok
3. **Emotion tags BẮT BUỘC** — mỗi segment ≥1 tag
4. **Smooth config mặc định** — layer_penalty=1.0, position_temp=3.0, speed=0.95
5. **denoise=True không bao giờ tắt** — Pitfall #9
6. **Test 1 câu đơn giản trước** — trước khi scale lên 6-12 câu
7. **A/B test khi có bug** — 7 variants, 9 anti-patterns, là khung tiêu chuẩn
8. **Denoise + amplify ref audio** — chain trước khi save .pt
9. **Không re-encode ref audio** — load .pt đã save (5x speedup)
