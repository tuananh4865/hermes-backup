---
name: multi-agent-orchestrator
description: "Hermes là orchestrator cho multi-agent trên tmux. Điều phối, FOLLOW sát sao, ACTIVE VERIFY, và CORRECT trực tiếp khi cần. Không tin agent claims - luôn verify trước khi mark complete."
---

# Multi-Agent Orchestrator v8.1

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

## CRITICAL: Pre-Spawn Terminal Check

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

### CRITICAL: Symlinks don't resolve in spawned agents!

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

---

## TELEGRAM MULTI-AGENT SETUP (Bot-to-Bot)

### Architecture
```
User (Tuấn Anh)
├── @HermesMainBot (CEO - default profile)
├── @ContentDirectorBot (Content Lead - content-director profile)
├── @ResearchLeadBot (Research Lead - research-lead profile)
└── @SecurityEngineerBot (Security - security-engineer profile)
```

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

### Bot Profiles Setup (2026-05-04)
| Profile | Bot Username | Bot Token | Status |
|---------|--------------|-----------|--------|
| default | @TyayUno | (main) | Primary |
| content-director | @SaturdayClawdBot | 8594106827:... | ✅ Running |
| research-lead | @Researcher_Clawd_Bot | 8706108095:... | ✅ Running |

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
