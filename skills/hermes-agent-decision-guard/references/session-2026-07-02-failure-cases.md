# Failure Cases & Cross-Skill Lessons (2026-07-02 update)

Updated: 2026-07-02 — added Failure 10 (ask-for-approval step).

This file aggregates new Failure cases and cross-skill lessons that extend `hermes-agent-decision-guard` SKILL.md.

## Failure 10: Adding ask-for-approval step that user didn't ask for (2026-07-02)

User: *"Trước khi cắt thì em gửi cho anh keep plan trước để anh duyệt"*

Agent's wrong sequence:
1. Wrote keep_plan
2. Stopped all rendering to "wait for anh to approve"
3. Said "Em KHÔNG render cho đến khi anh duyệt" 3 times
4. Asked "Câu hỏi cho anh: Framework OK không?"

User: *"Không cần bước gửi anh duyệt"*

Then later User: *"Sao lại có mấy con vợ ơi..."* (see Failure 11 below)

**Lesson:** The skill `tiktok-video-editor` already has TWO existing rules:
- `verify-before-done` (do the verification, then act)
- `self-review` (review your own work, don't ask user to review)

When agent adds a NEW step "Step 3.5: GỬI KEEP PLAN CHO ANH DUYỆT" — this is a NEW ask-for-approval step NOT requested by user. User's "Trước khi cắt thì em gửi cho anh keep plan trước" can mean EITHER:
- (a) Send anh a plan so anh can react BEFORE editing (interpret as: pause workflow)
- (b) Send anh the plan at the same time render starts (interpret as: transparent reporting)

But user repeatedly said "em KHÔNG cần anh duyệt" / "em OWN task" / "no follow-up". Agent SHOULD have picked interpretation (b), not invented Step 3.5 from thin air.

**Anti-pattern (NEW):**
- ❌ Adding new workflow step "wait for user approval" that wasn't explicitly requested
- ❌ Stopping execution at "X.Em chờ anh duyệt" when user has said "em tự quyết"
- ❌ Creating checkpoints that depend on user response

**Rule (NEW):**
1. **Default:** No approval checkpoint. Agent OWNs the task.
2. **Exception:** If user EXPLICITLY says "đợi em" or "đợi anh" or "chờ anh duyệt" then pause
3. **Translation heuristic for ambiguous requests:** "em gửi anh X trước khi Y" = send X AS PART OF Y (parallel), not send X THEN wait THEN do Y (sequence)
4. **Mục tiêu chính:** deliver task DONE. Keep_plan là status report, không phải approval gate.

**Detection signal:** Agent tự ý thêm "Step X.Y: chờ user approve" → user nói "không cần" / "em tự làm" → wasted turn.

---

## Failure 11: Using TikTok SCRIPT voice trong chat với user (2026-07-02)

**Chỉ tiết:** Xem `references/chat-voice-rule.md` (đã tạo).

Khi đọc rule về TikTok SCRIPT voice (mention "anh + mấy con vợ" trong content-creator-script-style), brain apply vào CHAT với anh. Vi phạm 3 lần trong session.

**Hard Rule:** SCRIPT voice ≠ CHAT voice.
- SCRIPT TikTok: check `content-creator-script-style` skill
- CHAT với anh: "anh + em" hoặc "mình + bạn" — KHÔNG "mấy con vợ"

---

## gdown workaround for Google Drive FOLDERS (2026-07-02)

Khi user share folder (không phải single file):
- `gdown URL` (không có flag) → fail "Cannot retrieve folder information"
- `gdown URL --no-check-certificate` → download được HTML folder page

```
gdown --no-check-certificate "https://drive.google.com/drive/folders/FOLDER_ID" -O /tmp/output
```

Sau đó check file output — nếu là HTML thì folder không public được dù cờ verify, cần browser thật để lấy cookies.

Alternative: `gdown "https://drive.google.com/file/d/FILE_ID/view"` cho file single trong folder — hoạt động bình thường.

---

## Self-review pitfall: không cross-check với source (2026-07-02)

Liên quan đến `tiktok-video-editor` skill v2.35.0 (Pitfall #90 SELF-REVIEW):

Khi em viết keep_plan, em PHẢI tự review TRƯỚC khi gửi (anh feedback 02/07):
1. Mỗi mute_ranges đã cross-check source word-level?
2. Có hallucinate/filler nào CHƯA skip?
3. Framework đủ 6 phases?
4. Có câu treo/lặp CÒN trong KEEP không?

Nếu 1 câu trả lời "không chắc" → FIX ngay, KHÔNG hỏi user.

Em đã viết V22 plan → gửi → user tự phát hiện 4 chỗ sai → lãng phí turn.

**Lesson applied**: Self-review TRƯỚC khi announce. V22-SELF-REVIEWED fix được 4/4 lỗi.

---

## References trong hermes-agent-decision-guard

- `references/chat-voice-rule.md` — chat voice cứng cho Tuấn Anh
