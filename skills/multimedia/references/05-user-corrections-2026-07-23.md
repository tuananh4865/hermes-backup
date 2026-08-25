# User Corrections Log — 23/07/2026

5 push-back từ anh Tuấn trong session này, mỗi cái embed trong SKILL.md + memory.

---

## Correction #1: VoiceClonePrompt save/load (EAGER LOAD — don't re-import ref mỗi lần)

**Verbatim:** *"Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu"*

**Em sai:** Default dùng `model.generate(text=..., ref_audio=ref.wav, ref_text=...)` mỗi lần → re-encode ref audio mỗi file (~5s overhead + Whisper re-run nếu thiếu ref_text).

**Anh correct:** Dùng `model.create_voice_clone_prompt()` → `prompt.save()` → `VoiceClonePrompt.load()` → 5x speedup, save 1 lần dùng mãi.

**Codified:**
- SKILL.md Lesson L1
- `references/01-api-surface.md` Section "Reusing a cloned voice across sessions"
- Script: `scripts/save_voice_prompt.py` (info + save modes)

---

## Correction #2: Fix prompt thay vì workaround output (TEST VARIANTS)

**Verbatim:** *"Tốt rồi! Nhưng Lúc em prompt omnivoice có vấn đề gì đó... chỉ cần fix prompt lại không inject câu đó vào nữa thôi!"*

**Em sai:** Default vào workaround (Whisper post-trim hack) thay vì investigate root cause ở prompt level.

**Anh correct:** Output leak câu cuối ref_text → nguyên nhân ref_text quá dài (3 câu, 122 chars). Test 4 variants ref_text → 2 câu = BEST, không cần trim hack.

**Codified:**
- SKILL.md Lesson L2 + L6
- `references/00-pitfalls.md` Pitfall #3 (ref_text leak)
- Recipe: dùng ref_text NGẮN 1-2 câu, ~100 chars

**Lesson (L6 — recurring pattern):** Khi gặp bug không rõ root cause, test ≥3 variants input trước khi conclude. 4 phút test saves hours debugging. Applied 3 lần trong session:
- ref_text: full/1-sent/2-sent/minimal
- concat method: afade/acrossfade/fade-out-only/trim-first
- amplitude: raw/amp×2.5/amp×11

---

## Correction #3: Đọc hết README + follow tất cả links (NO SILENT SKIP)

**Verbatim:** *"Đọc hết phần readme của repo chưa?"*

**Em sai:** Fetch README.md + beyond, NHƯNG skip `docs/community-projects.md` vì em focus vào inference. User phát hiện và correct.

**Anh correct:** README là gateway, mỗi link có thể chứa info quan trọng (community ecosystem, training pipeline). Skip phải explicit decision, ghi lý do rõ trong SKILL.md "Beyond" section.

**Codified:**
- SKILL.md Lesson L4
- "Beyond inference" section liệt kê 16 community projects + Top 3 đáng test (OmniVoice-MLX, omnivoice-server, pyVideoTrans)

---

## Correction #4: Concat fade PHẢI NHẸ — 30ms (USER PREFERENCE)

**Verbatim:** *"Khi em ghép batch lại với nhau thì để fadeout nhẹ thôi 30ms thôi"*

**Em sai:** Em dùng `afade=t=in:out` đối xứng (30ms fade in + 30ms fade out) → 60ms silent gap ở mỗi boundary. Anh phát hiện và correct.

**Root cause discovered (sau khi analyze):** OmniVoice mặc định `pad_duration=0.1` thêm 100ms silence đầu + cuối mỗi file output. Khi concat thẳng, mỗi boundary có 200ms silent. `afade` in+out chỉ tạo thêm fade curve, không fix root cause.

**Fix đúng (em test 4 variants concat methods):**

| Method | Boundary peak | Silent gap | Whisper hallucinate |
|---|---|---|---|
| `afade in+out` (cũ, sai) | 0.0000 (silent) | 60ms | "tuần" → "tuổi" |
| `acrossfade` chain | 0.07-0.11 | 41-13ms (mixed) | OK |
| **Trim 100ms + fade out only (MỚI)** | **0.03-0.11** | **30ms (chỉ fade)** | **OK** |

**Final recipe:**
```bash
# Đúng cho TTS audio concat:
python3 scripts/concat_segments.py --inputs-dir batch/ --output final.wav
# Script tự động:
# 1. atrim=start=0.1:end=duration-0.1 → trim 100ms lead/trail padding
# 2. afade=t=out:st=X:d=0.03 → fade out 30ms only (no fade in)
# 3. concat=n=N:v=0:a=1 → ghép thẳng
```

**Codified:**
- SKILL.md Lesson L5 (USER PREFERENCE — first-class)
- SKILL.md Pitfall #6 trong bảng tổng hợp
- `references/00-pitfalls.md` Pitfall #6 (full detail)
- Script: `scripts/concat_segments.py` đã rewrite với trim logic
- Memory: [23/07 VOICE-CLONE-OMNIVOICE importance:0.9]

---

## Correction #5: Bổ sung Non-Verbal emotion tags (USER DISCOVERY)

**Verbatim:** *"Anh thấy có phần Non-verbal & Pronunciation Control khá hay cộng thêm các key feature để thêm cảm xúc cho giọng đọc khiến cho giọng đọc giống người hơn!"*

**Em đã:** Test 10/10 emotion variants với prompt GOOJODOQ. Peak tăng rõ rệt (-2 to -3 dB vs -3.7 dB baseline).

**Codified:**
- SKILL.md Lesson L3
- `references/04-recipes.md` Recipe 11 (full list 13 tags + TikTok emotion recipe)
- Script: `scripts/test_emotion.py`
- Auto-emotion injection roadmap item

---

## Tổng kết pattern (5 corrections trong 1 session)

**User correction style:** Anh thường push back khi em:
1. Default vào workaround thay vì root cause analysis
2. Skip phần repo không "obvious" mà anh biết có giá trị
3. Apply fade/effect không match expectation
4. Không save reusable artifact (template voice)
5. Không explore feature phụ (non-verbal tags)

**Rule tổng quát:** Trước khi ship bất kỳ task nào, CHECK với anh về 3 câu:
1. "Có cần X (reusable artifact) không?" → save prompt/template, không re-import
2. "Có cách nào input-level thay vì output-level không?" → fix prompt trước, workaround sau
3. "Có feature phụ nào trong tool không?" → đọc hết README/docs, không chỉ main API
