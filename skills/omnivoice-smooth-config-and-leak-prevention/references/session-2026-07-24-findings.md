# Session 2026-07-24 — Voice Clone Smooth Config + Workflow Simplification

## Context

User (Tuấn Anh) iteratively debugged voice clone output quality through 9 turns. Each turn produced a new finding that became a pitfall in the parent skill.

## Chronological Findings

### Turn 1-3: Voice file deletion + new file selection
- User: "Xoá voice clone này đi" → Em deleted 4 experimental files (v2, v3, v4, v5), kept PRIMARY (v1 GOOJODOQ)
- User: "Anh gửi em voice mới để clone chứ không phải text nha" → Em tìm voice message mới
- SHA256 check: discovered `audio_7b7431fcecca.ogg` == `audio_1d2f805ee2e3.ogg` (cache returned same file)

### Turn 4: User explained "tại sao voice lặp"
- User: "Voice này anh ghi âm lặp là do anh muốn thể hiện nhiều biểu cảm khác nhau!"
- → Memory fact 10 updated with "user INTENTIONAL repeat for emotion range"
- → Pitfall #8 verdict: ACCEPTABLE, not a bug

### Turn 5: Denoise options
- User: "Dùng bản aggressive để clone đi" → Generated v5_aggressive_denoise.pt
- → v5 saved OK but kept echo nhỏ ở đầu output

### Turn 6: User CHANGED MIND
- User: "lấy raw" → "lấy 10s đầu của raw" → Em extract 10s đầu, amplify peak≤0.95
- → Saved v6_raw.pt (ref_rms=0.0783, edge case)

### Turn 7: Test TikTok review
- User: "lấy một script tiktok review nào đó và test thư lại đi" → Used Recipe 12 (5-segment HOOK→PROBLEM→SOLUTION→USP→CTA)
- Voice work but có echo "Túng đây" ở 04_usp

### Turn 8: USER COMPLAINT — root cause layer_penalty
- User: "Em prompt kiểu gì mà voice đầu ra tệ quá vậy? Giọng thì rõ nhưng ngắt quãng rất khó chịu"
- → A/B test 7 variants → ROOT CAUSE: `layer_penalty_factor=5.0` (default)
- Fix: `layer_penalty_factor=1.0` + `position_temperature=3.0` + `speed=0.95`

### Turn 9: User UX preference
- User: "Không cho setting gì vào prompt hết chỉ đơn giản gọi voice clone và nội dung kèm emotion tag thôi"
- → Rewrote `generate_voice.py` với interface đơn giản (chỉ --prompt + --text)

### Turn 10: Test wiki script
- User: "Test thêm một script trong wiki" → "Script về tiktok products ấy"
- → Used `lenspen-ve-sinh-ong-kinh-problem-solution.md` (5 segments)
- 5 segments worked with Whisper sạch 100%

### Turn 11: USER COMPLAINT — trailing silence
- User: "Này là phiên bản clone mới nhất phải không? Khi ghép ffmpeg có fade không mà bị mờ ở khúc đầu và khúc cuối voice vậy?"
- → Investigated: NOT ffmpeg fade, but model auto-generates 16-35ms trailing silence
- Fix: auto-trim trailing silence >10ms trong `generate_voice.py`

### Turn 12: User confirmed save
- User: "Ok lưu lại" → Em saved wiki concept + memory fact 10 + log + skill

## Files Created/Modified in Session

### Saves (5 files)
- `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_v6_raw.pt` (current ALTERNATE)
- `/Volumes/Storage-1/Hermes/voice-compare/2026-07-24-lenspen-wiki/` (6 WAV files)
- `/Volumes/Storage-1/Hermes/voice-compare/2026-07-24-ref-audio-check/` (3 reference WAV files)
- `/Volumes/Storage-1/Hermes/wiki/concepts/omnivoice-trailing-silence-fix-2026-07-24.md`
- `/Volumes/Storage-1/Hermes/scripts/concat_segments.py` (verified NO PADDING)

### Modifications
- `~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py` (v3, 5471 bytes) — added auto-trim, hardcoded config
- `~/.hermes/skills/omnivoice-smooth-config-and-leak-prevention/SKILL.md` — added Pitfall #10, #11, #12
- `~/.hermes/skills/omnivoice-voice-clone/SKILL.md` — appended session reference
- Memory fact 10 — added trailing-silence + 10 anti-patterns

### Deletions
- 4 experimental voice clone files (v2, v3, v4, v5)

## Key Lessons (Embed in Skills)

1. **User feedback signals (FIRST-CLASS):**
   - "giọng thì rõ nhưng ngắt quãng rất khó chịu" → investigate root cause, don't add flags blindly
   - "không cho setting gì vào prompt hết" → minimal CLI interface, hardcode config
   - "khi ghép ffmpeg có fade không mà bị mờ..." → distinguish ffmpeg fade vs model-generated trailing silence

2. **Investigation discipline:**
   - Always run A/B test 7+ variants when user complains about prosody
   - Verify with Whisper transcript + audio peak (numpy first/last 10ms frames)
   - Document EVERY session finding into skill (not just memory)

3. **Workflow design:**
   - Hardcode verified config inside script (don't expose CLI flags)
   - Auto-trim trailing silence as part of generate pipeline
   - Wiki test scripts (`lenspen-ve-sinh-ong-kinh-problem-solution.md`) = reusable for future TikTok Product generations

## Verification (24/07 end-state)

| Test | Result |
|---|---|
| 5-segment TikTok Product (Lenspen) | ✅ Whisper sạch 100%, peak -1.5 dB |
| Voice quality | ✅ Smooth, no ngắt quãng, no trailing silence >15ms |
| Workflow | ✅ `--prompt --text` only, no extra flags |
| Memory fact 10 | ✅ 10 anti-patterns + 3-step workflow |
| Skill updates | ✅ 3 new pitfalls added (trailing, workflow, layer penalty) |
