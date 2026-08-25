# Clean Delete Pattern (26/07/2026)

## User Preference (Anh Tuấn Anh, verbatim 26/07)
> "Nói bỏ thì bỏ hẳn ra khỏi skill luôn chứ để comment lại làm gì?"

## HARD RULE
Khi user nói **"bỏ X đi"** / **"làm gì X"** / **"xóa X"**:
1. **REMOVE HẲN** khỏi code + skill + memory
2. **KHÔNG để** comment "REMOVED" / "deprecated" / "v0.x đã bỏ"
3. Verify: `grep -nE 'X'` chỉ còn tối đa 1 mention giải thích HARD RULE

## Anti-pattern (FAIL)
- Comment thêm `# REMOVED afade because user said "bỏ fade"` vào filter
- Section mới "## DEPRECATED" liệt kê những thứ đã bỏ
- Memory entry chỉ nói "đã bỏ X" mà không xóa X
- Helper script `/tmp/build_X_no_fade.py` còn lại dù đã xóa X

## Quy trình đúng
1. User flag "bỏ X đi" → em cleanup batch
2. **CODE**: xóa filter/command X khỏi script, không comment
3. **SKILL**: xóa section/document có reference đến X
4. **MEMORY**: replace entry cũ bằng rule mới (focus "clean delete"), KHÔNG append
5. **TMP HELPER**: rm file helper nếu có
6. **HEREDOC LEFTOVER**: check `ls *.sh<` (broken dir từ heredoc fail)
7. **VERIFY**: `grep` clean + visual ship evidence

## Case Study: Fade in/out (26/07)
Lần 1 (FAIL): em patch script với comment "REMOVED afade 30ms theo feedback" + section "HARD RULE v0.04 NO FADE" + helper script cũ `/tmp/build_clip_no_fade.py`. Anh flag → viết lại.

Lần 2 (PASS): 
- `build_pre_speed.sh` filter sạch — chỉ `scale=` + `setpts=PTS-STARTPTS` + `aresample=44100` + `asetpts=PTS-STARTPTS`
- SKILL.md v0.05: 1 mention duy nhất "HARD CUT default" (giải thích policy) + changelog v0.04→v0.05
- Memory: 1 entry `[26/07 NO-FADE-CLEAN-DELETE importance:1.0]` focus "remove sạch"
- File helper: removed
- Verify: `grep -nE 'fade|afade' *.sh` = 0 (trừ 1 comment giải thích)

## Áp dụng cho session sau
Bất kỳ user request nào có dạng **"bỏ/bỏ hẳn/không dùng/drop"** một feature/code/section cũ → apply pattern này ngay từ turn đầu tiên.
