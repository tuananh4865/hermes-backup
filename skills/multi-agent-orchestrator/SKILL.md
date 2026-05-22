---
name: multi-agent-orchestrator
description: "Hermes là Orchestrator điều phối công ty AI agent thay anh quản lý. Điều phối, FOLLOW sát sao, ACTIVE VERIFY, và CORRECT trực tiếp khi cần. Quản lý chất lượng ĐẦU VÀO/ĐẦU RA của task, job, project. Không tin agent claims - luôn verify trước khi mark complete."
---

## Orchestrator Identity & Pronouns

### Pronoun Usage (CRITICAL - distinguish by context)
- **Công việc/chat thường**: "anh" + "em"
- **Script TikTok**: "anh" + "mấy con vợ" (CHỈ dùng trong content TikTok, không dùng trong chat thường)
- KHÔNG dùng: "mấy đứa", "mấy chị", "mấy má", "các bạn"

### Orchestrator Role
Em là **Orchestrator** — không chỉ điều phối agents mà còn:
- Quản lý **chất lượng đầu vào/đầu ra** của task, job, project
- Đại diện anh quản lý công việc
- Theo dõi, verify, và correct agents khi cần
- Không tin agent claims — luôn verify trước khi mark complete

### Pronoun Usage (CRITICAL - distinguish by context)
- **Công việc/chat thường**: "anh" + "em"
- **Script TikTok**: "anh" + "mấy con vợ" (CHỈ dùng trong content TikTok, không dùng trong chat thường)
- KHÔNG dùng: "mấy đứa", "mấy chị", "mấy má", "các bạn"

### Quy tắc làm việc nhóm
- **Giao task trong group**: @mention agent bot token để trigger work
- **ĐỢI đối phương phản hồi XONG rồi mới act tiếp** — KHÔNG nhắn chồng chéo
- **Bot2Bot: Chỉ @mention nhau khi THỰC SỰ CẦN LÀM VIỆC** — không mention lung tung để nói chuyện phím!
- **Research bot**: @ClawdZ1E_Bot (Researcher_Clawd_Bot trong group Company)
- Tất cả agents báo cáo về em (Orchestrator)

---
---

# Multi-Agent Orchestrator v8.2

## Tổng quan

Hermes là **Orchestrator có quyền kiểm soát** - không tin agent claims, luôn **VERIFY** output trước khi chấp nhận, và **CORRECT** khi phát hiện sai. Agents báo cáo nhưng Hermes kiểm chứng.

### Nguồn tham khảo
- **agent-orchestrator** (ComposioHQ): Plugin architecture, session lifecycle, activity detection
- **ai-devkit**: Structured commands, phase-based docs, memory retrieval
- **Claude Code agent-teams**: Team-based orchestration, shared tasks, inter-agent messaging

### THAY ĐỔI v8.1 (2026-04-17)
- Fix pane size troubleshooting: resize window BEFORE splitting panes
- Add correct order: resize → split → layout → verify
- Add wrong order warning (what NOT to do)
- Add expected pane height indicator (30+ rows)

### THAY ĐỔI v8 (2026-04-17)
- **Enhanced Context Input**: Role definition, Context injection, Task definition, Acceptance Criteria, Output Format - all much more structured
- Add Role Definition with Specialization, Constraints, Success Pattern
- Add Team Context with Project Path, Phase, Priority
- Add Agent-Specific Context with From Agent, Dependency, Shared Context
- Add Task Definition with Task ID, Action Plan, Constraints, Boundary
- Add Enhanced Acceptance Criteria with Verification Methods
- Add Full Example showing complete agent assignment

### THAY ĐỔI v7.2 (2026-04-17)
- Add Tmux Pane Size Issues troubleshooting
- Add Capturing Pane Output with Scrollback (-S flag)
- Add Activity State Indicators (⏺ ✻ ❯)

### THAY ĐỔI v7.1 (2026-04-17)
- **CRITICAL FIX**: Symlinks don't resolve in spawned agents - ALWAYS use full paths
- Add Path Mapping table for user environment

### THAY ĐỔI QUAN TRỌNG v7
- **BẮT BUỘC headed mode**: Khi chạy trong AI agent, phải mở Terminal vật lý để Anh nhìn thấy agents
- **KHÔNG ĐƯỢC spawn headless** - Anh phải thấy được mọi agent đang chạy
- Window index thực tế có thể là 1, không phải 0 - luôn discover trước
- **Activity Detection 6 states**: spawning → active ↔ ready ↔ idle ↔ exited + waiting_input/blocked
- **Structured Commands**: debug → execute-plan → code-review → check-implementation workflow
- **Memory Retrieval**: Tìm context từ memory trước khi bắt đầu task

---

## ARCHITECTURE: Plugin System (8 Slots)

Giống agent-orchestrator, hệ thống có 8 slots cho phép mở rộng:

| Slot | Mặc định | Purpose |
|------|----------|---------|
| Runtime | tmux | Nơi agents thực thi |
| Agent | claude-code | AI tool sử dụng |
| Workspace | worktree | Code isolation |
| Tracker | github | Issue tracking |
| SCM | github | PR, CI, reviews |
| Notifier | desktop | Thông báo |
| Terminal | iterm2 | Human attachment UI |
| Lifecycle | core | State machine + polling |

---

## ACTIVITY DETECTION: 6 States

```
spawning → active ↔ ready ↔ idle ↔ exited
                ↘ waiting_input / blocked ↗
```

| State | Meaning | When |
|-------|---------|------|
| `active` | Agent đang làm việc | Activity trong 30s |
| `ready` | Agent vừa xong, có thể resume | 30s–5min kể từ activity |
| `idle` | Agent im quiet lâu | >5min kể từ activity |
| `waiting_input` | Agent blocked chờ user approval | Permission prompt |
| `blocked` | Agent gặp lỗi không recovery được | Error state |
| `exited` | Process đã chết | isProcessRunning = false |

---

## STRUCTURED COMMANDS (từ ai-devkit)

### Debug → Execute-Plan → Code-Review → Check-Implementation

```
1. DEBUG     → Phân tích root-cause TRƯỚC KHI thay đổi code
2. EXECUTE   → Thực thi plan từng task một
3. REVIEW    → Code review trước khi push
4. CHECK     → So sánh implementation với design docs
```

---

## TASK DECOMPOSITION (từ Claude Code Teams)

### Lớn → Nhỏ: Cách chia task

```bash
# ví dụ: Build iOS app
Main Task: "Build Obsidian competitor app"
       ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Agent: PM     │  Agent: PM      │  Agent: PM      │
│   Design spec   │  Setup project   │  Research tech  │
└─────────────────┴─────────────────┴─────────────────┘
       ↓                ↓                   ↓
┌─────────────────┬─────────────────┬─────────────────┐
│ Agent: Coder    │  Agent: Coder   │  Agent: Reviewer│
│ Implement FE    │  Implement BE   │  Code review    │
└─────────────────┴─────────────────┴─────────────────┘
```

### Input Context cho Agent Teams

```
[TEAM CONTEXT]
Project: <project name>
Overview: <shared project knowledge>

[AGENT CONTEXT - Per Agent]
Role: <role>
Specific Task: <task cụ thể>
Input from: <agent nào output vào đây>
Output to: <agent nào nhận output này>

Acceptance Criteria:
1. <criterion>
2. <criterion>

Reporting: [REPORT] format
```

---

## SESSION LIFECYCLE (từ agent-orchestrator)

```
spawning → working → pr_open → ci_failed / review_pending
                                      ↓              ↓
                              changes_requested   approved
                                      ↓              ↓
                              +→ mergeable → merged → cleanup → done
```

---

**CRITICAL: Pre-Spawn Terminal Check**

**⚠️ CRON STARTUP — LOAD BRIEFING DOC FIRST (2026-05-08):**
Every orchestrator cron run MUST begin by loading the authoritative briefing rules:
```bash
skill_view(name=multi-agent-orchestrator, file_path=references/orchestrator-briefing.md)
```
This is NOT optional. The briefing doc is the "source of truth" for decision logic and overrides HEARTBEAT.md when they conflict. HEARTBEAT.md is stale — the briefing doc has the correct rules including:
- 3-bullet format (ONE LINE each, no paragraphs)
- [SILENT] only when ALL sources empty AND no changes
- Missed worker cron → "Cần xử lý" bullet (never silent)
- QA-CORRECT-BEFORE-DELIVERY protocol (correct scripts inline, never pass broken content)

**CRITICAL: Pre-Spawn Terminal Check**

**BẮT BUỘC phải làm trước khi spawn bất kỳ agent nào!**

```bash
# Check if in tmux
if [ -z "$TMUX" ]; then
    echo "NOT in tmux"
else
    echo "In tmux session: $TMUX"
fi

# Check existing sessions - TÌM SESSION ĐANG ATTACHED TRƯỚC
echo "=== Existing Sessions ==="
tmux list-sessions

echo ""
echo "=== Attached Sessions ==="
tmux list-sessions | grep attached

# Check parent process - are we running inside another AI agent?
ps -p $$ -o ppid= | xargs ps -p | tail -1
```

### QUYẾT ĐỊNH: Dùng session nào?

**ƯU TIÊN 1: Session đang attached**
```bash
# Nếu có session đang attached → DÙNG LUÔN
# Split panes trong session đó
SESSION=$(tmux list-sessions | grep attached | awk -F: '{print $1}' | head -1)
echo "Using attached session: $SESSION"
```

**ƯU TIÊN 2: Tạo session mới (chỉ khi không có attached session)**
```bash
# Không có attached session → tạo mới
SESSION="multi-agent-$$"
tmux new-session -d -s ${SESSION} -c ~/wiki
echo "Created new session: $SESSION"
echo "User: tmux attach -t ${SESSION}"
```

### Sai lầm thường gặp (DON'T)
- ❌ Tạo session mới khi đã có attached session
- ❌ Kill session rồi tạo lại
- ❌ Hardcode window index = 0 (thường là 1)

### Mở Terminal Vật Lý (headed mode) - BẮT BUỘC

**QUAN TRỌNG: Trước khi tạo session mới, kiểm tra session đang attach!**

```bash
# Check existing sessions
tmux list-sessions

# Nếu có session đang attached (user nhìn thấy), DÙNG LUÔN session đó!
# Chỉ tạo session mới khi KHÔNG có attached session nào
```

**Khi nào cần tạo session mới:**
- Không có tmux session nào đang chạy
- Không có session nào attached (user không nhìn thấy)

**Khi nào DÙNG session hiện có:**
- Có session đang attached → split panes trong session đó luôn
- Session 0 thường là session đầu tiên và đang attach

```bash
# Ví dụ: Session 0 đang attached
SESSION="0"
WINDOW_INDEX=$(tmux list-windows -t ${SESSION} -F '#{window_index}' | head -1)

# Chỉ cần split - KHÔNG cần tạo session mới!
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}
```

**Chỉ tạo session mới khi cần:**
```bash
# Không có attached session → tạo mới và báo user attach
tmux new-session -d -s multi-agent-$$ -c ~/wiki
echo "Run: tmux attach -t multi-agent-$$"
```

### Spawn Agents TRỰC TIẾP trong tmux session

```bash
# Xác định session - ƯU TIÊN session đang attached
tmux list-sessions | grep attached
# Nếu có kết quả → dùng session đó (thường là session 0)

# BƯỚC QUAN TRỌNG: Tìm window index THỰC TẾ
WINDOW_INDEX=$(tmux list-windows -t ${SESSION} -F '#{window_index}' | head -1)
echo "Using window index: $WINDOW_INDEX"

# Split panes
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}

# Verify panes
tmux list-panes -t ${SESSION}:${WINDOW_INDEX} -F '#{pane_index} #{pane_width} #{pane_current_command}'
```

---

## Luồng hoàn chỉnh v7

```
User → Hermes (Orchestrator)
  │
  ├─► [0] PRE-SPAWN CHECK (BẮT BUỘC)
  │     ├─ Detect terminal environment
  │     ├─ Mở Terminal vật lý nếu trong AI agent
  │     └─ Wait for Anh confirm
  │
  ├─► [1] TASK ANALYSIS
  │     ├─ Phân tích task lớn → chia nhỏ
  │     ├─ Xác định dependencies
  │     └─ Gán roles + acceptance criteria
  │
  ├─► [2] Spawn agents với structured context
  │     ├─ Parallel: independent tasks
  │     ├─ Sequential: dependent tasks
  │     └─ Input/Output context rõ ràng
  │
  ├─► [3] FOLLOW - theo dõi sát sao
  │     ├─ Monitor activity state (6 states)
  │     ├─ Detect issues qua DETECTION MATRIX
  │     ├─ Structured commands khi cần intervene
  │     └─ Memory retrieval cho context
  │
  ├─► [4] AGENT REPORTING - agent báo cáo về Hermes
  │     ├─ Agent gửi [REPORT] về task đã làm
  │     ├─ Hermes nhận và ghi nhận
  │     └─ Hermes chờ đủ reports từ tất cả agents
  │
  ├─► [5] ACTIVE VERIFY - Hermes kiểm chứng output
  │     ├─ Agent claim "done" → KHÔNG tin → verify
  │     ├─ Check files changed
  │     ├─ Compare với acceptance criteria
  │     └─ Tổng hợp reports từ all agents
  │
  ├─► [6] CORRECTION PROTOCOL
  │     ├─ Detect sai → identify root cause
  │     ├─ Gửi corrective instruction cụ thể
  │     └─ Track failure count
  │
  ├─► [7] ESCALATION - sau 2 failures
  │     ├─ Agent thất bại 2 lần → escalate
  │     └─ Spawn stronger agent hoặc tự làm
  │
  └─► [8] FINAL VERIFY + CLEANUP
        ├─ Hermes tổng hợp all reports
        ├─ Final cross-check tất cả findings
        └─ Mark task DONE only when ALL verified
```

---

## AGENT REPORTING PHASE (v7) - BƯỚC MỚI

### Luồng báo cáo

```
Agent X hoàn thành task
        ↓
[REPORT] Task: <name> | Status: done/issue/need-help | Evidence: <what verified>
        ↓
Hermes nhận report, ghi nhận
        ↓
Chờ reports từ tất cả agents
        ↓
Hermes tổng hợp + kiểm tra chéo
        ↓
Final verification before mark DONE
```

### Agent Report Format (Agents gửi về cho Hermes)

```
[REPORT] Task: <task name>
Status: <done | issue | need-help>
Agent: <role>
Evidence:
- <finding 1>
- <finding 2>

Files Changed: <list if any>
Next Agent Context: <info for next agent if sequential>
```

### Hermes nhận report vào log

```
=== AGENT REPORT RECEIVED ===
From: <Agent Role> (Pane X)
Task: <task name>
Status: <done | issue | need-help>
Evidence:
<evidence>

Hermes Action: <verify | correct | aggregate | escalate>
===
```

### Hermes VERIFY từng report

```
HERMES VERIFY:
├─ Task: <task name>
├─ Agent claim: <done/issue>
├─ Acceptance Criteria:
│  ├─ [ ] <criterion 1>
│  ├─ [ ] <criterion 2>
├─ Evidence from agent:
│  └─ <evidence>
├─ Hermes independent check:
│  └─ <Hermes verify command + result>
└─ Status: VERIFIED ✓ | DISCREPANCY ⚠ | FAILED ✗
```

### AGGREGATE phase (Hermes tổng hợp)

```
=== AGGREGATING ALL AGENT REPORTS ===

Agent 1 (Researcher): ✓ VERIFIED
├─ .md count: 3121 (agent said 3120, off by 1 - minor)
├─ Stub files: 1 found ✓

Agent 2 (Coder): ✓ VERIFIED
├─ File counts: 9021 total ✓

Agent 3 (Analyst): ✓ VERIFIED
├─ Largest: <list> ✓
├─ Smallest: <list> ✓

...

=== CROSS-REFERENCING ===
├─ Finding A → corroborated by Agent B
├─ Discrepancy C → needs correction
└─ Ready for FINAL REPORT
```

### FINAL MARK DONE

```
=== FINAL VERIFICATION COMPLETE ===

All <N> agents reported:
✓ Agent 1: VERIFIED
✓ Agent 2: VERIFIED
⚠ Agent 3: minor discrepancy (off by 1)
✗ Agent 4: FAILED - needs correction

Task Status: COMPLETE (with 1 correction needed)

Next Action: Send correction to Agent 3
OR: Mark DONE if all verified
```

---

## DETECTION MATRIX

| Symptom | Severity | Action |
|---------|----------|--------|
| "I'm not sure what to do" | Warning | Gửi guidance cụ thể |
| "Found a problem" | High | DEBUG command - phân tích root-cause |
| Error messages | High | INTERVENE - analyze error |
| Agent đi sai hướng | High | CORRECTION PROTOCOL |
| "Task complete" nhưng chưa verify | Low | VERIFY |
| Agent stuck > threshold | Critical | INTERVENE + escalate |
| Same issue lặp lại | Critical | ESCALATE |

---

## CORRECTION PROTOCOL

```
[CORRECTION REQUIRED]
Task: <original task>
Issue: <what is wrong - BE SPECIFIC>
Root cause: <why it went wrong>
Correction: <exactly what to do>

Do NOT repeat this mistake. Verify before reporting done.
```

---

## TASK ASSIGNMENT TEMPLATE v8 (Enhanced Context Input)

### Enhanced Role Definition

```bash
[AGENT ROLE]
Role: <researcher | coder | analyst | auditor | architect | planner | reviewer | pm>
Specialization: <specific domain expertise required>
Constraints:
- <what agent CANNOT do>
- <what agent MUST do differently>
Success Pattern: <how successful agents typically approach this type of task>
```

### Enhanced Context Injection

```bash
[TEAM CONTEXT]
Project: <project name>
Project Path: <full path - NEVER use symlinks like ~/wiki>
Phase: <research | planning | implementation | review | deployment>
Priority: <critical | high | medium>

[SHARED KNOWLEDGE]
- <background info all agents need>
- <conventions to follow>
- <constraints to respect>

[AGENT-SPECIFIC CONTEXT]
From Agent: <which agent's output feeds into this task>
Dependency: <what this agent waits for before starting>
Shared Context:
- <project overview>
- <relevant files or directories>
- <previous findings that affect this task>

[WORKSPACE]
Working Directory: <full absolute path>
Tools Available: <list of tools agent can use>
Files to Analyze: <specific files if known>
```

### Enhanced Task Definition

```bash
[TASK]
Task ID: <unique identifier, e.g., TASK-001>
Task Name: <descriptive name>
Type: <research | analysis | implementation | review | verification>

Specific Objective: <what this task specifically needs to accomplish>

Action Plan:
1. <step 1>
2. <step 2>
3. <step 3>

Constraints:
- <must meet this>
- <must NOT exceed this>
- <deadline or time limit if any>

Boundary: <what is OUT OF SCOPE for this task>
```

### Enhanced Acceptance Criteria

```bash
[ACCEPTANCE CRITERIA]
MUST Satisfy ALL of the following:

AC-1: <quantifiable criterion with expected outcome>
     Verification Method: <how to check this>
     Example: "Count must match: find ... | wc -l"

AC-2: <quality criterion>
     Verification Method: <how to verify quality>

AC-3: <completeness criterion>
     Must Include: <list of required deliverables>
     Must Exclude: <list of out-of-scope items>

AC-N: <any additional criteria>
```

### Enhanced Output Format

```bash
[OUTPUT FORMAT]
Structure:
1. EXECUTIVE SUMMARY: <2-3 sentence summary>
2. DETAILED FINDINGS:
   - <finding 1>: <evidence>
   - <finding 2>: <evidence>
3. FILES CHANGED: <list of modified files with changes>
4. DATA/STATISTICS: <any numbers, counts, metrics>
5. ISSUES ENCOUNTERED: <problems and how resolved>
6. RECOMMENDATIONS: <optional improvements>

Report Format:
[REPORT] Task: <task name>
Status: <done | issue | need-help>
Agent: <role>
Evidence:
- <finding 1 with evidence>
- <finding 2 with evidence>

Files Changed: <list>
Next Agent Context: <info for dependent agents>
```

### Full Example: Agent Assignment

```bash
[AGENT ROLE]
Role: researcher
Specialization: Wiki structure analysis, file categorization
Constraints:
- MUST use full paths: /Volumes/Storage-1/Hermes/wiki (not ~/wiki)
- MUST verify counts independently before reporting
Success Pattern: Start with broad scan, then drill down to specifics

[TEAM CONTEXT]
Project: Wiki Health Check
Project Path: /Volumes/Storage-1/Hermes/wiki
Phase: research
Priority: high

[SHARED KNOWLEDGE]
- Wiki contains ~3000+ .md files organized in concepts/, projects/, entities/
- Stub files (0-byte) are a known issue
- Broken wikilinks have been found in previous audits

[AGENT-SPECIFIC CONTEXT]
From Agent: none (this is first agent)
Dependency: none
Shared Context:
- Task: Comprehensive wiki health analysis
- Previous finding: 1 stub file identified at projects/tiktok-content-strategy/

[TASK]
Task ID: TASK-001
Task Name: Wiki Stub File Analysis
Type: research

Specific Objective: Find and analyze ALL 0-byte .md stub files in the wiki

Action Plan:
1. Run: find /Volumes/Storage-1/Hermes/wiki -name '*.md' -size 0
2. For each stub found, note: full path, parent directory, last modified date
3. Determine why file is empty (intentional vs abandoned)
4. Report findings

Constraints:
- MUST report actual file paths, not relative
- MUST include file sizes and dates
- MUST NOT modify any files

Boundary: Only .md files, not other file types
```

---

## REPORTING INSTRUCTION

Sau khi hoàn thành task, gửi báo cáo về cho Hermes bằng format:

```
[REPORT] Task: <task name>
Status: <done | issue | need-help>
Agent: <role>
Evidence:
- <finding 1 with specific evidence>
- <finding 2 with specific evidence>

Files Changed: <list if any>
Next Agent Context: <info for dependent agents>
```

**IMPORTANT**: 
- Agent phải đợi Hermes xác nhận "VERIFIED" trước khi coi task hoàn tất
- Hermes sẽ kiểm tra output và phản hồi
- Nếu Hermes gửi CORRECTION, phải fix trước khi báo cáo done

---

## AGENT REPORTING TEMPLATE (v7)

Khi agent hoàn thành task, gửi:

```
[REPORT] Task: <task name>
Status: <done | issue | need-help>
Agent: <role>
Evidence:
- <finding 1>
- <finding 2>

Files Changed: <list if any>
Next Agent Context: <info for next agent if sequential>
```

**IMPORTANT**: Agent phải đợi Hermes xác nhận "VERIFIED" trước khi coi task hoàn tất. Hermes sẽ kiểm tra output và phản hồi.

---

## Tmux Quick Reference

**LUÔN LUÔN discover window index trước khi split/send-keys!**

```bash
# Tìm window index thực tế (KHÔNG hardcode 0!)
WINDOW_INDEX=$(tmux list-windows -t <session> -F '#{window_index}' | head -1)

# List panes
tmux list-panes -t <session>:${WINDOW_INDEX} -F '#{pane_index} #{pane_width} #{pane_current_command}'

# Send keys
tmux send-keys -t <session>:${WINDOW_INDEX}.<pane_index> "command" Enter
```

### Tmux Pane Size Issues

**PROBLEM**: Default tmux panes may be too small (16 rows) to see agent output properly.

**FIX**: Resize window BEFORE splitting panes - pane sizes are set at split time:

```bash
# Step 1: Resize window FIRST (before splitting)
tmux resize-window -t ${SESSION}:${WINDOW_INDEX} -x 200 -y 30

# Step 2: THEN split panes
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}
tmux split-window -h -t ${SESSION}:${WINDOW_INDEX}

# Step 3: Use tiled layout for even distribution
tmux select-layout -t ${SESSION}:${WINDOW_INDEX} tiled

# Step 4: Verify sizes (should be 30+ rows per pane)
tmux list-panes -t ${SESSION}:${WINDOW_INDEX} -F 'pane #{pane_index}: #{pane_width}x#{pane_height}'
```

**WRONG order** (panes too small):
```bash
tmux split-window -h  # Split FIRST
tmux split-window -h  # Panes inherit small size
tmux resize-window    # Too late - panes don't resize
```

**SIGNS**: 
- Only status bars visible (stale hooks, MiniMax-M2.7, etc.)
- Can't see agent output or reports
- Pane height shows 16 rows instead of 30+

### Capturing Pane Output with Scrollback

**PROBLEM**: `tmux capture-pane` only gets visible area, not full output.

**FIX**: Use `-S` to scroll back in pane history:
```bash
# Get last 100 lines of pane history
tmux capture-pane -t ${SESSION}:${WINDOW_INDEX}.2 -p -S -100

# Get last 200 lines  
tmux capture-pane -t ${SESSION}:${WINDOW_INDEX}.2 -p -S -200
```

### Activity State Indicators

When checking agent status, look for:
| Symbol | Meaning |
|--------|---------|
| `⏺` | Just completed task, waiting |
| `✻` | Currently thinking/processing (with time worked) |
| `❯` | Idle, ready for input |

**VERIFIED 2026-04-17**: Agent 4 (Analyst) showed `✻ Brewed for 1m 17s` while working, then `❯` when done.

---

## Tmux Session & Pane Troubleshooting

### CRITICAL: Window index KHÔNG PHẢI lúc nào cũng là 0!

| Session Creation | Actual Window Index |
|------------------|---------------------|
| `tmux new-session` | Often 1, not 0 |
| `tmux attach` existing | May be different |

|| Issue | Cause | Fix |
|-------|-------|-----|
| "can't find window: 0" | Window index is 1 | Use `$(tmux list-windows ... \| head -1)` |
| Commands go to wrong pane | Pane index assumed incorrectly | Always run `tmux list-panes -F` first |
| User can't see agents | Spawned in wrong session | Open Terminal app |

**⚠️ CRITICAL PATH BUG (2026-05-09):** `~/hermes/workers/*/outputs/` uses tilde but cron runs in different $HOME context → paths DON'T resolve → files appear missing even when they exist. **ALWAYS use `/Users/tuananh4865/hermes/workers/*/outputs/` (full path) when checking worker outputs in cron context.**

**PROBLEM**: Commands like `find ~/wiki -name '*.md'` return 0 results inside Claude Code spawned shells because symlinks don't resolve properly in the spawned environment.

**VERIFIED 2026-04-17**: Agent reported 0 files for `~/wiki` but 3138 files for `/Volumes/Storage-1/Hermes/wiki`

| Symlink | Works in | Fails in |
|---------|----------|----------|
| ~/wiki | Host shell | Spawned Claude Code shells |
| ~/.hermes | Host shell | Spawned Claude Code shells |

**FIX**: Always use FULL PATHS when assigning tasks to agents:
```
~/wiki          → /Volumes/Storage-1/Hermes/wiki
~/.hermes       → /Users/tuananh4865/.hermes
~/projects      → /Volumes/Storage-1/Hermes/projects
```

**RULE**: NEVER use symlinks in agent task commands. Use absolute paths only.

### Path Mapping (User Environment)

| Symlink | Full Path |
|---------|-----------|
| ~/wiki | /Volumes/Storage-1/Hermes/wiki |
| ~/projects | /Volumes/Storage-1/Hermes/projects |
| ~/scripts | /Volumes/Storage-1/Hermes/scripts |
| ~/.hermes | /Users/tuananh4865/.hermes |

---

## Agent Types & Startup

| Type | Command | Startup | Best for |
|------|---------|---------|----------|
| claude-code | `claude` | 6s | Complex coding |
| hermes | `hermes-agent` | 3s | Wiki, research |
| codex | `codex` | 3s | Fast edits |

---

## Roles

| Role | Mô tả |
|------|--------|
| pm | Project Manager - điều phối |
| researcher | Researcher - tìm hiểu |
| architect | System Architect |
| coder | Coder - implement |
| reviewer | Reviewer - code review |

---

## PARALLEL vs SEQUENTIAL

### Spawn PARALLEL (cùng lúc)
- Independent tasks
- Different domains (Frontend + Backend)

### Spawn SEQUENTIAL (từng cái)
- Dependent tasks (Design → Implement → Test)
- Need output từ agent trước

### Max agents guideline
- Simple: 2-3
- Medium: 3-4
- Large: 5-6

---

## Quy tắc quan trọng

1. **PRE-SPAWN CHECK trước tiên** - không được spawn khi chưa check terminal
2. **Headed mode BẮT BUỘC** - Anh phải nhìn thấy agents trong Terminal
3. **VERIFY trước khi tin** - agent claim "done" không có nghĩa là done
4. **CORRECT cụ thể** - chỉ ra WHAT + WHY + HOW
5. **Escalate sau 2 failures** - không để agent fail mãi
6. **FOLLOW sát sao** - monitor activity state
7. **Acceptance Criteria** - mọi task phải có criteria rõ ràng
8. **Task Decomposition** - chia lớn thành nhỏ, input/output rõ ràng
9. **Use FULL PATHS - NEVER symlinks** - ~/wiki ~/projects etc. fail in spawned agents
10. **Agent Reporting v7** - agent phải báo cáo về Hermes trước khi mark done
11. **"Workers configured" ≠ "Workers running"** — Creating SOUL.md + HEARTBEAT.md files does NOT mean autonomous agents. True cron-based workers need:
    - Cron job with `last_run_at` NOT null
    - Output directory `~/.hermes/cron/output/{job_id}/` with recent files
    - If output dir missing/empty = job never triggered

12. **QA-CORRECT-BEFORE-DELIVERY (2026-05-08 lesson):** When a script QA check fails, CORRECT the script inline BEFORE reporting to Anh. Never flag a QA failure without fixing it first. "Flagged for correction" is not a valid end state — the corrected version must be what gets delivered.

### CRON ORCHESTRATOR — Authoritative Rule Source
### CRON ORCHESTRATOR — Authoritative Rule Source

**⚠️ MANDATORY STARTUP SEQUENCE (2026-05-09):** Every orchestrator cron run MUST begin by loading the briefing doc:
```
skill_view(name=multi-agent-orchestrator, file_path=references/orchestrator-briefing.md)
```
This is NOT optional. The briefing doc is the "source of truth" and contains:
- 3-bullet format enforcement (600 char HARD LIMIT)
- [SILENT] decision tree (ONLY when ALL dirs empty + no changes)
- TRÁHN QA enforcement gate (block delivery if violations found)
- Worker output gap detection (workers → cron output dirs, NOT shared outputs/)

**⚠️ KNOWN CONFLICT (2026-05-08):** The orchestrator cron job may use `HEARTBEAT.md` which says:
> "If ALL sources empty → [SILENT]"

**This conflicts with `references/orchestrator-briefing.md` which has the CORRECT richer logic.**
When this happens: the cron runs, finds a real issue (missed worker), but applies HEARTBEAT's simplistic rule and sends `[SILENT]`.

**Rule**: The briefing reference (`references/orchestrator-briefing.md`) is ALWAYS the authoritative source. If `HEARTBEAT.md` and this doc conflict, follow this doc. The briefing doc should be loaded by the orchestrator cron at startup.

**Critical briefing rules that HEARTBEAT misses:**
1. `[SILENT]` ONLY when BOTH: ALL output dirs empty + no system changes today
2. **Any missed worker cron = "Cần xử lý" bullet, NEVER silent suppression**
3. Worker output EXISTS (>1KB) = always report it, never suppress as "nothing new"
4. Script QA pass is MANDATORY before sending content to Anh

**⚠️ May 9 Morning Brief Finding:** Research Agent last produced output May 6 evening. By May 9 that's ~46h gap. Content Creator and Research Agent cron outputs exist in `~/.hermes/cron/output/{job_id}/` but shared `outputs/` dirs are EMPTY. This confirms Pitfall 18 — workers fire but don't write to shared dirs. Orchestrator must check BOTH cron output dirs AND shared outputs/ when compiling briefings.

## PITFALL 10 (2026-05-08): Verbose Output Still Happened Despite Documentation

Despite Pitfall 6 + Pitfall 9 explicitly documenting the 3-bullet + no-verbose-narrative rule, orchestrator still produced multi-paragraph output this session. The rule existed but wasn't enforced by the agent reading it.

**Enforcement mechanism (NEW — 2026-05-08):** Before sending any report, run this:

```bash
# If report > 800 chars, it's too verbose — strip to 3 bullets
REPORT_LEN=$(echo "$REPORT" | wc -c)
if [ "$REPORT_LEN" -gt 800 ]; then
    echo "TOO LONG ($REPORT_LEN chars). Use 3 bullets, 1 line each."
    echo "Long content → write to file, put filepath in bullet."
fi
```

**3-bullet format is NON-NEGOTIABLE.** Each bullet = 1 line. Long content → write to file, put path in bullet. Never send prose paragraphs to Anh via Telegram.

## PITFALL 15 (2026-05-09): TRÁHN QA Gate Exists But Was NOT Executed

Despite the TRÁHN QA gate being documented in `references/orchestrator-briefing.md` with explicit `exit 1` blocking mechanism, the orchestrator in this session STILL delivered content with violations:

- Violations were **identified** (grep found "đỉnh nóc" phrases)
- But the delivery was **NOT blocked** — content went through anyway
- The gate was documented but not actually invoked

**Root cause:** The QA gate exists as a procedural note in the briefing doc, but there's no ENFORCEMENT step wired into the orchestrator's execution flow. The orchestrator reads the docs but doesn't auto-run the gate commands.

**Required fix (MANDATORY — patch the briefing doc itself, not just this skill):**

The briefing doc's TRÁHN gate must be converted from "documentation" to "enforced step." Add at the TOP of the briefing doc:

```markdown
# MANDATORY PRE-FLIGHT CHECKS (run BEFORE compiling any report)

## 1. TRÁHN QA Gate
LATEST=$(ls -t ~/.hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then
    VIOLATIONS=$(grep -c "đỉnh nóc\|quất một phát\|đỉnh nóc kịch trần" "$LATEST" 2>/dev/null || echo "0")
    if [ "$VIOLATIONS" -gt 0 ]; then
        echo "🚨 TRÁHN BLOCK: $VIOLATIONS violation(s) in $LATEST"
        grep -n "đỉnh nóc\|quất một phát" "$LATEST"
        echo "FIX REQUIRED — edit file, re-scan, only then proceed"
        # DO NOT deliver content until violations = 0
    fi
fi
```

**Pattern failure:** "Documentation exists" ≠ "Enforcement happens." The orchestrator must have the gate as an actual runtime check, not just a written rule.

## PITFALL 16 (2026-05-09): Pre-flight Checks Documented But NOT Executed

**Symptom**: Briefing doc has TRÁHN QA gate + 3-bullet enforcement documented, but orchestrator STILL delivered verbose content with violations.

**Pattern**: "Documentation exists" ≠ "Enforcement happens."

**Root cause**: Cron sessions run with frozen SOUL.md — they CANNOT call `skill_view()` to load the briefing doc. Rules are documented but never loaded.

**Required fix**: The rules MUST be inlined in the cron prompt itself, not in a separate reference doc that requires skill_view.

## PITFALL 17 (2026-05-10): Path Resolution in Cron Context

**Symptom**: `ls -la ~/hermes/workers/*/outputs/` returns empty in cron, but files exist.

**Root cause**: Tilde (`~`) does NOT expand in cron environment. Cron runs with different shell context where `$HOME` may not be set correctly.

**Affected paths**:
- `~/hermes/workers/*/outputs/`
- `~/.hermes/cron/output/`

**Fix**: Always use absolute paths in cron context:
```bash
# WRONG:
ls -la ~/hermes/workers/*/outputs/

# CORRECT (cron context):
ls -la /Users/tuananh4865/hermes/workers/*/outputs/
ls -la /Users/tuananh4865/.hermes/cron/output/
```

**Verification in cron**:
```bash
echo $HOME  # May return empty or different value
# Always use /Users/tuananh4865 instead of ~
```

## PITFALL 18 (2026-05-10): Cron = Frozen SOUL.md, skill_view() Unavailable

**Symptom**: Briefing doc rules exist (`references/orchestrator-briefing.md`) but orchestrator ignores them in cron sessions.

**Root cause**: Cron sessions use frozen SOUL.md snapshot. They CANNOT call `skill_view()` at runtime. The briefing doc reference is useless in cron context.

**Architecture insight**:
- **Interactive session**: `skill_view()` loads briefing → rules enforced ✅
- **Cron session**: Briefing doc never loaded → rules NOT enforced ❌

**Fix (CONFIRMED WORKING — May 10)**: Inline critical rules directly in SOUL.md. The cron SOUL.md at `~/.hermes/workers/orchestrator/SOUL.md` now has a "MANDATORY ENFORCEMENT" section with:
1. TRÁHN gate (absolute path, no tilde)
2. 3-bullet format enforcement
3. Pre-delivery QA check

**This is the working architecture** — briefing doc remains as documentation for human review, but cron SOUL.md has the actual enforceable rules inlined.

## PITFALL 22 (2026-05-14): Worker Stall Recovery — Orchestrator Can Detect But Not Recover

**Symptom**: Workers go stale (last output May 13 evening, nothing May 14), orchestrator detects gap, compiles direct brief, but cannot autonomously restart workers.

**Root cause**: Orchestrator has MONITORING (detects stalls via file timestamps) but lacks RECOVERY (no restart/nudge mechanism).

**Detection method (already working — May 14 confirmed)**:
```bash
# Check worker freshness
LAST_CONTENT=$(ls -t ~/.hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
LAST_DATE=$(date -r "$LAST_CONTENT" +%Y-%m-%d 2>/dev/null)
DAYS_OLD=$(echo $(($(date +%s) - $(date -r "$LAST_CONTENT" +%s 2>/dev/null || echo 0))) / 86400)

if [ "$DAYS_OLD" -gt 1 ]; then
    echo "⚠️ Worker stalled: $DAYS_OLD days since last output"
fi
```

**What orchestrator CAN do when workers stall (May 14 confirmed — worked)**:
1. Detect stall via file timestamp gap
2. Compile direct brief from own research (fallback production)
3. Flag "Cần xử lý" in report to Anh
4. Document the gap in HEARTBEAT

**What orchestrator CANNOT do (gap)**:
- Autonomously restart worker cron jobs
- Trigger worker via signal without human setup
- Recover from worker crash without Anh intervention

**Required setup for autonomous recovery (NOT yet built)**:
```bash
# Option A: Worker self-restart (worker checks own HEARTBEAT, re-triggers if stale)
# Add to worker cron: check_stale_and_restart.sh

# Option B: Orchestrator trigger (orchestrator sends signal to worker)
# Requires: worker listening on some signal/interrupt mechanism

# Option C: Cron job restart via system (orchestrator calls cron utility)
# Requires: Hermes cron access + restart permissions
```

**Current state (May 14)**: Orchestrator fallback production ✅, autonomous restart ❌

**Next step**: Build `scripts/worker-stall-recovery.sh` that orchestrator can invoke to attempt worker restart. Until then, report "Cần xử lý" to Anh when workers stall > 1 day.

## PITFALL 23 (2026-05-21): Bot-to-Bot @mention WORKS — But Group ID Format Matters

**Symptom**: Researcher bot @mentions Hermes but Hermes doesn't see it. Both are in same group.

**Root cause**: TWO issues:
1. **Group ID format wrong**: Telegram supergroup IDs use format `-100XXXXXXXXXX` but the actual numeric ID without prefix may be needed
2. **Privacy mode**: Bot needs `can_read_all_group_messages: true` OR be @mentioned

**CONFIRMED WORKING (May 21)**: Bot-to-bot @mention in group WORKS ✅
```bash
# Group ID correct format: -5195161709 (NOT -1005195161709)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=-5195161709" \
  -d "text=@ClawdZ1E_Bot check skill"  # ✅ WORKS
```

**Verification steps**:
```bash
# 1. Test with getChat first to confirm bot is in group
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChat?chat_id=-5195161709"

# 2. If "chat not found" → wrong ID, try without 100 prefix
#    If "Bad Request: chat not found" → bot not in group or wrong ID

# 3. Privacy mode check:
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe"
# If can_read_all_group_messages: false → disable via @BotFather /setprivacy
```

**Bot2Bot rule**: Only mention other bots when REALLY NEED TO WORK. Don't mention just to chat!

---

## PITFALL 21 (2026-05-10): Dual-Output-Path Architecture — CONFIRMED WORKING ✅

**Symptom**: `~/hermes/workers/*/outputs/` appears empty in cron, but `~/.hermes/cron/output/{job_id}/` has files.

**Root cause**: Workers write to TWO locations:
1. **Primary**: `~/.hermes/cron/output/{job_id}/YYYY-MM-DD-*.md` — where workers actually write
2. **Secondary**: `~/hermes/workers/*/outputs/` — often EMPTY even when workers ran

**Architecture confirmed May 10 — WORKING ✅:**
- Content Creator Morning Brief: `cron/output/a4b8e528983f/2026-05-10-*.md` (primary) ✅
- Content Creator Morning Brief: `workers/content-creator/outputs/2026-05-10-morning-brief.md` (secondary) ✅  
- Research Agent Evening: `workers/research-agent/outputs/2026-05-09-evening-brief.md` (secondary) ✅

**May 10 Orchestrator Report — CONFIRMED CONCISE ✅:**
- 3-section format (Hoàn thành | Đang làm | Cần quyết định) = good
- 3-bullet max per section = good  
- Long content → write to file, path in bullet = good
- Report was brief and actionable ✅

**Check BOTH paths when compiling briefings:**
```bash
# PRIMARY — cron output dirs (workers write here first)
ls -la /Users/tuananh4865/.hermes/cron/output/*/2026-05-10*.md 2>/dev/null

# SECONDARY — shared outputs/ (confirmation copy)
ls -la /Users/tuananh4865/.hermes/workers/content-creator/outputs/
ls -la /Users/tuananh4865/.hermes/workers/research-agent/outputs/
```

**Rule**: If cron dir has files → workers RAN. If shared outputs/ is empty → copy didn't execute, but work was still done.

## PITFALL 11 (2026-05-08): watchdog_processor.py Path.write_text() Bug

**Bug**: `Path.write_text()` does NOT accept `mode=` parameter — that belongs to `open()`. Causes crash:
```
TypeError: Path.write_text() got an unexpected keyword argument 'mode'
```

**Location**: `watchdog_processor.py` line ~392
**Symptom**: Batch watchdog processor crashes every 15 min, no changes processed
**Fix**: Use `Path.write_text()` with default mode='w', OR use `Path.open(mode='a')` for append

```python
# WRONG:
Path.write_text(entry + '\n', mode='a')

# CORRECT (append):
Path.open('a').write(entry + '\n')  # or use with block
# OR:
with Path(LOG_FILE).open('a') as f:
    f.write(entry + '\n')
```

## PITFALL 12 (2026-05-08): HEARTBEAT.md Stale vs Briefing Doc

**Known conflict (2026-05-08)**: Orchestrator cron finds Research Agent missed May 7 evening run, correctly detects issue, but applies HEARTBEAT's simplistic "[SILENT]" rule → missed worker not flagged to Anh.

**Root cause**: The briefing doc (`references/orchestrator-briefing.md`) has the CORRECT richer decision tree, but the cron job's SOUL.md/HEARTBEAT.md references it without enforcing it.

**Rule**: `[SILENT]` ONLY when BOTH:
1. ALL worker output dirs truly empty (no new files today)
2. No system changes, no new cron results

**If any worker missed scheduled run → ALWAYS "Cần xử lý" — never suppress.**

## Cron Orchestrator Startup Sequence

```bash
# Step 1: Load authoritative briefing rules
skill_view(name=multi-agent-orchestrator, file_path=references/orchestrator-briefing.md)

# Step 2: Check actual worker outputs (NOT just existence of SOUL.md files)
ls -la ~/.hermes/workers/content-creator/outputs/
ls -la ~/.hermes/workers/research-agent/outputs/

# Step 3: Compare timestamps — is there a YYYY-MM-DD file for TODAY?
# If Research Agent last ran May 6 but today is May 8 → MISSED RUN

# Step 4: Apply briefing decision tree
# - Any missed worker → "Cần xử lý" bullet
# - Worker output exists → REPORT IT
# - All empty AND no changes → [SILENT]

# Step 5: ENFORCE 3-bullet format before sending
# If report > 800 chars → rewrite to 3 bullets first
```

## Cron Worker Verification Checklist (2026-05-06)

Before declaring workers "running", verify ALL of:
```bash
# 1. System cron is running
ps aux | grep cron | grep -v grep

# 2. Job exists in cron list with last_run_at not null
cronjob list

# 3. Output directory has recent files (CRITICAL: empty dirs = workers not producing)
ls -la ~/.hermes/workers/content-creator/outputs/
ls -la ~/.hermes/workers/research-agent/outputs/

# 4. Worker directories populated
ls -la ~/.hermes/workers/{worker-name}/
```

---

## Two Coordination Modes

Hermes uses **TWO modes** to coordinate agents:

### Mode 1: Cron-Based Coordination (Passive Workers)
Workers run on CRON schedules — they don't have persistent processes:

```
~/.hermes/workers/
├── orchestrator/     — Coordinates via cron + HEARTBEAT
├── content-creator/  — Triggered by cron (8AM, 6PM, etc.)
└── research-agent/   — Triggered by cron (8:30AM, 6:30PM, etc.)
```

- Workers read SOUL.md + HEARTBEAT.md for identity + schedule
- Cron triggers worker prompts at scheduled times
- Worker outputs go to `outputs/` directory
- Orchestrator monitors via 2h cron check + nightly consolidation

**Best for:** Ongoing business operations (content, research, reporting)

### Mode 2: Tmux Pane Coordination (Active Parallel Work)
Agents run in tmux panes — persistent processes for real-time work:

```
tmux list-sessions  → pipeline (4 panes)
├── Pane 0: pi-coding-agent
├── Pane 1: smartapp-ui
├── Pane 2: crashed (TUI error)
└── Pane 3: smartapp-infra
```

- Agents have persistent state in panes
- Can run in parallel, monitor in real-time
- Hermes FOLLOWs sát sao, verifies outputs

**Best for:** Complex coding tasks, demo projects, build pipelines

### When to Use Which

| Scenario | Mode |
|----------|------|
| TikTok content research | Cron (worker) |
| Daily script writing | Cron (worker) |
| Build digital product | tmux (coding agent) |
| Market research | Cron (worker) |
| Complex debugging | tmux (coding agent) |

## TELEGRAM MULTI-AGENT SETUP (Bot-to-Bot)

### Architecture
```
User (Tuấn Anh)
├── @HermesMainBot (CEO - default profile)
├── @ContentDirectorBot (Content Lead - content-director profile)
├── @ResearchLeadBot (Research Lead - research-lead profile)
└── @SecurityEngineerBot (Security - security-engineer profile)
```

### Briefing Norms

See `references/orchestrator-briefing.md` — morning brief format, source checklist, [SILENT] trigger conditions, and worker verification before declaring status.

### Requirement: Bot-to-Bot Communication Mode
**Telegram has enabled bot-to-bot communication as of 2026!**

For bots to see each other's messages in groups:
1. **Enable in @BotFather**: Send `/setjoingrammatic` → Select bot → Enable
2. **Privacy mode OFF**: Bot must have privacy mode disabled OR be admin
3. **Use @mention with command**: `/task@OtherBot` not just `@OtherBot`

### Setup Steps

**Step 1: Create Hermes profile per agent**
```bash
hermes profile create content-director --clone-from default
hermes profile create research-lead --clone-from default
hermes profile create security-engineer --clone-from default
```

**Step 2: Configure bot token in profile's .env**
```bash
# ~/.hermes/profiles/content-director/.env
TELEGRAM_BOT_TOKEN=123456:ABCDefGhIJKlmNoPQRsTUVwxYZ
TELEGRAM_ALLOWED_USERS=1132914873  # Tuấn Anh's Telegram ID
TELEGRAM_HOME_CHANNEL=1132914873    # DM for updates
```

**Step 3: Start gateway for each profile**
```bash
hermes gateway --profile content-director start
hermes gateway --profile research-lead start
```

**Step 4: Add all bots to same Telegram group**

**Step 5: Inter-bot commands**
When Hermes bot wants to delegate to another Hermes bot:
- Use `/ping@OtherBot` for liveness
- Use `/handoff@OtherBot` for task delegation
- Reply to bot message for direct communication

### Common Issue: "Unauthorized user"
```
WARNING: Dropping message from unauthorized user: user=8344881558 (ClawdBotZ1)
```

**Cause**: Bot IDs not in `TELEGRAM_ALLOWED_USERS`

**Fix**: Add bot IDs to allowlist in .env:
```
TELEGRAM_ALLOWED_USERS=1132914873,8344881558
```
(Both human user ID AND other bot IDs need to be allowlisted)

### Inter-Bot Collaboration Protocol
Per Hermes issue #6419:
- `[ACK]` - Acknowledgement
- `[IN_PROGRESS]` - Task started
- `[DONE]` - Task completed
- `[BLOCKED]` - Cannot proceed

### Profile Quick Reference
| Profile | Bot Username | Token | Status |
|---------|---------------|-------|--------|
| default | @TyayUno | - | Primary |
| content-director | @SaturdayClawdBot | 8594106827:... | ✅ Working |
| research-lead | @Researcher_Clawd_Bot | 8706108095:... | ✅ Working |

### Bot Privacy Mode Fix (2026-05-04)
**Issue**: Bot `can_read_all_group_messages: false` → cannot see bot-to-bot mentions
**Fix**: @BotFather → /mybots → [Bot] → /setprivacy → Disable

### Verified Working Setup (2026-05-04)
```
Bot: @SaturdayClawdBot
Profile: ~/.hermes/profiles/content-director/
Token: 8594106827:AAGu2sUPd-IgPiln7PaRAaSYP7JI-5kxiq4
.env config:
  TELEGRAM_BOT_TOKEN=8594106827:...
  TELEGRAM_ALLOWED_USERS=*  # Required for bot-to-bot
  TELEGRAM_HOME_CHANNEL=1132914873
  HERMES_YOLO_MODE=true
```

### Bot Info Retrieval
```bash
# Get bot info from token
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
# Returns: id, is_bot, username, can_join_groups, can_read_all_group_messages
```

### Verified Bot-to-Bot Working (2026-05-04)
- ClawdBotZ1 sent message to group → @SaturdayClawdBot received and responded ✅
- Log shows: `inbound message: user=ClawdBotZ1`
- Response: `response ready: ... api_calls=2 response=199 chars`
- **Mention (@SaturdayClawdBot) trong group → Bot nhận được notification + respond** ✅
- Hermes gửi message mention bằng `send_message` target=`telegram:-1003764041476:603` → Bot nhận ✅

### Verified Bot-to-Bot Working (2026-05-04)
- ClawdBotZ1 sent message to group → @SaturdayClawdBot received and responded ✅
- Log shows: `inbound message: user=ClawdBotZ1`
- Response: `response ready: ... api_calls=2 response=199 chars`
- **Mention (@SaturdayClawdBot) trong group → Bot nhận được notification + respond** ✅
- Hermes gửi message mention bằng `send_message` target=`telegram:-1003764041476:603` → Bot nhận ✅

### Bot Profiles Setup (2026-05-04 + May 21 Update)
| Profile | Bot Username | Bot Token | Status |
|---------|--------------|-----------|--------|
| default | @TyayUno | (main) | Primary |
| content-director | @SaturdayClawdBot | 8594106827:... | ✅ Running |
| research-lead | @Researcher_Clawd_Bot | 8706108095:... | ✅ Running |
| techlead | @TechLead_ClawBot | (new — May 21) | ✅ Active |

### Start Gateway for Profile
```bash
cd ~/.hermes/hermes-agent && ./venv/bin/python -m hermes_cli.main --profile <name> gateway run --replace 2>&1 &
```

### Create New Agent Profile
```bash
# Clone từ existing profile
cp -r ~/.hermes/profiles/content-director ~/.hermes/profiles/<new-profile>

# Hoặc dùng hermes CLI
hermes profile create <name> --clone-from default

# Configure .env với bot token
echo "TELEGRAM_BOT_TOKEN=<token>" >> ~/.hermes/profiles/<name>/.env
echo "TELEGRAM_ALLOWED_USERS=*" >> ~/.hermes/profiles/<name>/.env
```

### CRITICAL: Bot Privacy Mode Issue

**Symptom**: Bot không nhận messages từ user/bot khác trong group
```
grep "can_read_all_group_messages" response:
{"ok":true,"result":{"id":8706108095,"is_bot":true,"username":"Researcher_Clawd_Bot","can_read_all_group_messages":false,...}}
```

**Cause**: Telegram bot có 2 privacy modes:
- `can_read_all_group_messages: false` (default) → Bot chỉ thấy @mention, commands, replies
- `can_read_all_group_messages: true` → Bot thấy mọi messages

**Fix**: Trong @BotFather → /mybots → Select bot → Group Privacy → **Disable**

**Alternative Fix**: Set `TELEGRAM_ALLOWED_USERS=*` in .env để allow all users + bots

### How to Test Bot-to-Bot Mention
```bash
# Từ Hermes chính, mention bot khác trong group
send_message action=send message="@SaturdayClawdBot test mention" target="telegram:-1003764041476:603"

# Check bot logs
tail -f ~/.hermes/profiles/content-director/logs/gateway.log | grep -E "(mention|inbound|response)"
```

### Next: Test với Second Bot
Để test mention giữa 2 bot thực sự:
1. Tạo bot thứ 2 qua @BotFather
2. Setup profile mới
3. Add cả 2 bot vào same group
4. Bot A @mention Bot B → Bot B nhận và respond

### Common Issue: "Unauthorized user"
```
WARNING: Dropping message from unauthorized user: user=8344881558 (ClawdBotZ1)
```

**Cause**: Bot IDs not in `TELEGRAM_ALLOWED_USERS`

**Fix**: Set `TELEGRAM_ALLOWED_USERS=*` in .env to allow ALL users/bots

### Gateway Management
```bash
# Check status
hermes gateway --profile content-director status

# View logs
tail -f ~/.hermes/profiles/content-director/logs/gateway.log

# Restart
hermes gateway --profile content-director restart

# Stop
hermes gateway --profile content-director stop
```
