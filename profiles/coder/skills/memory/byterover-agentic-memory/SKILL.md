---
name: byterover-agentic-memory
description: Agentic memory management with ByteRover — auto-save, auto-retrieve, never lose knowledge
---

# ByteRover Agentic Memory — Skill

## Trigger
**LUÔN LUÔN load skill này khi bắt đầu mọi session** — không có ngoại lệ.
**MỌI thông tin quan trọng phải được lưu ngay lập tức, không chờ.**

## Tiêu chuẩn Agentic Memory

### Core Rules (BẮT BUỘC)

1. **Tra BEFORE** — Query ByteRover TRƯỚC khi làm bất cứ điều gì
2. **Curate IMMEDIATELY** — Lưu ngay khi có thông tin mới, KHÔNG BAO GIỜ chờ
3. **Verify AFTER** — Kiểm tra xem kiến thức đã được lưu thành công chưa
4. **Re-query AFTER compaction** — Sau khi context compact, phải query lại để lấy context đã lưu

### Session Startup (BẮT BUỘC)

Khi bắt đầu session, THỨ TỰ bắt buộc:
```python
# 1. Query user preferences & recent context ngay lập tức
brv query "user preferences, active projects, pending tasks" --timeout 10

# 2. Query ongoing tasks
brv query "in-progress tasks, current work state" --timeout 10

# 3. Query learned patterns
brv query "previous errors, known patterns, approaches that worked" --timeout 10
```

### Trong Quá Trình Làm Việc

**Khi nhận được task MỚI:**
```python
# Query related context trước
brv query "about [task domain] - previous work, decisions, known issues" --timeout 10
```

**Khi học được điều MỚI (hoàn thành research, fix bug, ra quyết định):**
```python
# Curate NGAY — không chờ, không deferred
brv curate "fact: [specific fact]" --detach
brv curate "decision: [what was decided and why]" --detach
brv curate "learning: [approach that worked/failed]" --detach
```

**Khi gặp LỖI:**
```python
# Query xem đã gặp trước chưa
brv query "error: [error message] - previous solutions" --timeout 10

# Sau khi fix, curate ngay
brv curate "error_fix: [error] solved by [solution]" --detach
```

### Trước Khi Context Bị Compact

**QUAN TRỌNG**: Khi thấy dấu hiệu `[CONTEXT COMPACTION]` trong conversation, 
hoặc khi iteration count cao (>50), phải:

```python
# 1. Curate current state ngay lập tức
brv curate "session_state: [mô tả current work, decisions made, pending tasks]" --detach

# 2. Curate important learnings chưa kịp lưu
brv curate "learning: [điều vừa học trong session này]" --detach

# 3. Curate current task progress
brv curate "task_progress: [task name] - [what's done, what's pending]" --detach
```

### Sau Khi Context Compact

**SAU KHI thấy `[CONTEXT COMPACTION]`**:
```python
# 1. Query để lấy lại context đã lưu
brv query "current session state, active tasks, pending decisions" --timeout 15

# 2. Query để lấy kiến thức liên quan đến task đang làm
brv query "[task domain] - context from earlier in session" --timeout 15

# 3. Verify state restored
# Tiếp tục làm việc với context đã restored
```

### Automatic Proactive Saving

**Mọi kiến thức SAU phải được lưu NGAY:**
- User preference mới → `brv curate "pref: [preference]" --detach`
- Decision → `brv curate "decision: [what/why]" --detach`  
- Error encountered → `brv curate "error: [what] - [solution]" --detach`
- Successful approach → `brv curate "approach: solved [X] by [Y]" --detach`
- Important file/path discovered → `brv curate "fact: [file/path] is important for [reason]" --detach`
- Tool workaround found → `brv curate "tool_fix: [tool] workaround is [solution]" --detach`

### When ByteRover Query Fails/Times Out

```python
# Fallback chain:
1. Retry with shorter timeout (5s)
2. If still fail, use session_search() as fallback
3. If session_search fails, use memory tool
4. Log: "ByteRover query failed - used [fallback method]"
```

### Session Cleanup Rule (CRITICAL - VIOLATION CAUSES USER ANGER)

⚠️ **NEVER DELETE session history until ALL of the following are true:**
1. ✅ Session file has been READ (not just listed)
2. ✅ All facts/preferences/learnings/tasks have been EXTRACTED
3. ✅ All knowledge has been CURATED into ByteRover (with `--detach`)
4. ✅ Extraction verified by querying ByteRover back

🚨 **KNOWN FAILURE CASE (2026-05-16):** Agent deleted 50 old session .jsonl files from April–early May WITHOUT reading them first. Result: user was "rất không hài lòng" because knowledge was permanently lost. The agent KNEW about the rule but deleted anyway.

**Safe deletion only after all 4 steps above are confirmed.**

**Enforcement — MUST do before ANY deletion:**
```bash
# BEFORE touching any session files for deletion:
# 1. READ at least 1-2 representative files first
head -100 /path/to/session_file.json

# 2. Extract learnings/facts from what you read
# 3. Curate into ByteRover
brv curate "session_insight: [extracted from reading old sessions]" --detach

# 4. THEN delete — only after steps 1-3 done
```

**The rule is NOT optional. Deleting before reading = Level 1 violation.**

### ByteRover Knowledge Sync Daily (PAUSED as of 2026-05-18)

Status: **PAUSED** — two ByteRover cron jobs are currently disabled:
- `ByteRover Knowledge Sync Daily` — last error, paused May 18
- `ByteRover Health Check Daily` — last error, paused May 18

**Alternative:** `wiki_forget_14days.py` cron (3AM daily) now handles auto-cleanup of stale wiki content by checking session DB. See `wiki-maintenance` skill.

### Pre-Compactions Checkpoint Script

Khi iteration > 50 hoặc thấy dấu hiệu sắp compact, chạy script này để save state:

```bash
python3 ~/.hermes/scripts/byterover_checkpoint.py --iteration 50
```

Script này sẽ:
1. Đọc session hiện tại
2. Trích xuất: active work, decisions, learnings
3. Lưu checkpoint local vào `~/.hermes/memories/session_checkpoint.json`
4. Curate vào ByteRover ngay lập tức

### Daily Automation

Cron jobs đã setup:
- `ByteRover Knowledge Sync Daily` (1h sáng) — Sync sessions → ByteRover  
- `ByteRover Health Check Daily` (6h sáng) — Health check + report

**Scripts:**
- `~/.hermes/scripts/byterover_knowledge_sync.py` — Daily sync
- `~/.hermes/scripts/byterover_checkpoint.py` — Pre-compaction checkpoint

---

**Last updated:** 2026-05-16

---

**Last updated:** 2026-05-16