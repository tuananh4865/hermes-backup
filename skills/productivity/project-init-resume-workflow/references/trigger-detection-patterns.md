---
title: Trigger Detection Patterns — Init/Resume Project
created: 2026-06-18
type: reference
tags: [trigger-detection, regex, vietnamese, english, edge-cases]
---

# Trigger Detection Patterns

> **Goal:** Phát hiện intent của user (INIT/RESUME/STATUS) từ message qua Telegram/terminal.
> **Source:** Tuấn Anh mandate 18/06 — em phải tự detect trigger, không hỏi.

---

## Pattern matching (Vietnamese + English)

### INIT patterns (project mới)

```python
INIT_PATTERNS = [
    # Vietnamese
    r"tạo\s+(?:project|dự\s+án)\s+(\S+)",
    r"khởi\s+tạo\s+(\S+)",
    r"setup\s+(\S+)",
    r"mở\s+project\s+mới[:\s]+(\S+)",
    r"init\s+(\S+)",

    # English
    r"create\s+project\s+(\S+)",
    r"new\s+project[:\s]+(\S+)",
    r"initialize\s+(\S+)",
]
```

**Test cases PASS:**
- ✅ "tạo project tiktok-affiliate-q3" → match → project_id="tiktok-affiliate-q3"
- ✅ "tạo dự án content-creator-v2" → match → project_id="content-creator-v2"
- ✅ "khởi tạo my-new-project" → match → project_id="my-new-project"
- ✅ "init project X" → match → project_id="X"
- ✅ "create project blog-2026" → match → project_id="blog-2026"

**Test cases FAIL (false positive):**
- ❌ "tạo project thì cần làm gì?" → match "thì" → bug
- ❌ "tôi muốn tạo project nhưng chưa biết tên" → match "nhưng" → bug

**Mitigation:** Nếu project_id chứa stop words ("thì", "nhưng", "cần", "làm") → skip match hoặc ask user.

### RESUME patterns (project cũ)

```python
RESUME_PATTERNS = [
    # Vietnamese
    r"mở\s+(?:lại\s+)?project\s+(\S+)",
    r"vào\s+project\s+(\S+)",
    r"resume\s+(\S+)",
    r"tiếp\s+tục\s+project\s+(\S+)",
    r"tiếp\s+tục\s+(\S+)",
    r"làm\s+tiếp\s+(?:project\s+)?(\S+)",
    r"làm\s+(?:việc\s+)?trong\s+project\s+(\S+)",
    r"làm\s+trên\s+project\s+(\S+)",

    # English
    r"resume\s+project\s+(\S+)",
    r"open\s+project\s+(\S+)",
    r"continue\s+project\s+(\S+)",
    r"work\s+on\s+project\s+(\S+)",
]
```

**Test cases PASS:**
- ✅ "mở project content-creator" → match → project_id="content-creator"
- ✅ "mở lại project tiktok-affiliate" → match → project_id="tiktok-affiliate"
- ✅ "vào project X" → match → project_id="X"
- ✅ "resume project Y" → match → project_id="Y"
- ✅ "tiếp tục project Z" → match → project_id="Z"
- ✅ "tiếp tục A" → match (nếu "A" là project đã tồn tại) → project_id="A"
- ✅ "làm tiếp project B" → match → project_id="B"

### STATUS patterns (báo cáo)

```python
STATUS_PATTERNS = [
    r"(?:project|dự\s+án)\s+(\S+)\s+(?:đang\s+)?(?:đến\s+đâu|tình\s+hình|status)",
    r"status\s+(?:of\s+)?(?:project\s+)?(\S+)",
    r"(\S+)\s+(?:đang|hiện\s+tại)\s+(?:ở\s+đâu|như\s+thế\s+nào)",
]
```

---

## Edge cases đã biết

### 1. Project ID chứa stop words

**Example:** "tạo project thì cần 5 ngày"
- Match: project_id = "thì"
- Bug: "thì" là stop word, không phải project_id thật

**Mitigation:**
```python
STOP_WORDS = {"thì", "nhưng", "cần", "làm", "có", "không", "để", "với", "từ", "trong"}

if project_id.lower() in STOP_WORDS:
    # Fallback: use full message as context, ask user via clarify
    return ("AMBIGUOUS", full_message)
```

### 2. Project ID có số và dấu gạch ngang

**Example:** "tạo project tiktok-q3-2026"
- Match: project_id = "tiktok-q3-2026"
- ✅ OK — id hợp lệ, không có stop word

**Example:** "mở project content-creator-v2-final"
- Match: project_id = "content-creator-v2-final"
- ✅ OK

### 3. User nói tên project trong câu dài

**Example:** "Anh muốn mở lại project content-creator để xem hub.md"
- Match: project_id = "content-creator"
- ✅ OK — extract được ID chính xác

### 4. Multiple projects trong 1 message

**Example:** "So sánh project A và project B"
- Match: project_id = "A" (first match)
- Bug: Có thể user muốn so sánh cả 2

**Mitigation:** Trigger RESUME cho cả 2 projects, gộp output.

### 5. User typo project name

**Example:** "mở project content-creater" (sai "creator")
- Match: project_id = "content-creater"
- Bug: Project không tồn tại → error

**Mitigation:**
```bash
if [ ! -d "$PROJECTS_DIR/$PROJECT_ID" ]; then
    # Suggest similar names
    ls "$PROJECTS_DIR/" | grep -i "$PROJECT_ID"
    exit 1
fi
```

### 6. INIT trong session đang RESUME project khác

**Example:** Session đang RESUME "A", user nói "tạo project B"
- → Switch context: chạy init-project.sh B (KHÔNG resume A nữa)
- → Update log: ghi "session switched from A → B"

---

## Context detection (advanced)

Ngoài pattern matching, có thể detect intent qua **context clues**:

| Clue | Intent |
|------|--------|
| User paste link YouTube/TikTok | → KHÔNG phải init/resume, là analyze |
| User gõ file path `/Volumes/Storage-1/...` | → KHÔNG phải init/resume, là file edit |
| User nói "checklist" / "log" | → project-checklist-management skill |
| User nói "default" | → default-project-hub-pattern skill |
| User nói "phases" / "milestones" | → hermes-project-workflow-system skill |

---

## Khi nào KHÔNG dùng trigger detection

- Khi user CHAT bình thường ("anh nghĩ sao về X?")
- Khi user hỏi factual question
- Khi user share link mà KHÔNG kèm action word

**Rule of thumb:** Trigger detection chỉ dùng khi user **explicit muốn act** (tạo/mở/làm). Nếu user chỉ mention tên project trong câu hỏi → KHÔNG auto-trigger.

---

*Pattern created: 2026-06-18 by Hermes*
*Source: Tuấn Anh mandate 18/06 — em phải tự detect trigger*
