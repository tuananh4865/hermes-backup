---
name: multi-agent-orchestrator
description: "Hermes là orchestrator cho multi-agent trên tmux. Điều phối, FOLLOW sát sao, ACTIVE VERIFY, và CORRECT trực tiếp khi cần. Không tin agent claims - luôn verify trước khi mark complete."
---

# Multi-Agent Orchestrator v3

## Tổng quan

Hermes là **Orchestrator có quyền kiểm soát** - không tin agent claims, luôn **VERIFY** output trước khi chấp nhận, và **CORRECT** khi phát hiện sai. Agents báo cáo nhưng Hermes kiểm chứng.

### Khác biệt chính

| Trước | Sau |
|-------|-----|
| Chờ agent done | Monitor và detect issues |
| Tin agent "done" | Verify output trước |
| Không correct được | Correct cụ thể với evidence |
| Không escalation | Escalate sau 2 lần thất bại |

## Luồng hoàn chỉnh v4

```
User → Hermes (Orchestrator)
  │
  ├─► [1] Phân tích task → chia sub-tasks với ACCEPTANCE CRITERIA
  │
  ├─► [2] Spawn agents với role + criteria vào split panes
  │
  ├─► [3] FOLLOW - theo dõi sát sao
  │     ├─ Monitor định kỳ qua tmux capture-pane
  │     ├─ Detect issues qua DETECTION MATRIX
  │     └─ Chờ report từ agents
  │
  ├─► [4] ACTIVE VERIFY - kiểm chứng output
  │     ├─ Agent claim "done" → VERIFY against criteria
  │     ├─ Check files changed
  │     ├─ Run tests if applicable
  │     └─ Không tin cho đến khi evidence rõ ràng
  │
  ├─► [5] CORRECTION PROTOCOL - sửa khi sai
  │     ├─ Detect sai → identify root cause
  │     ├─ Send corrective instruction cụ thể
  │     ├─ Re-verify sau correction
  │     └─ Track failure count
  │
  ├─► [6] ESCALATION - sau 2 failures
  │     ├─ Agent thất bại 2 lần → escalate
  │     ├─ Spawn stronger agent
  │     └─ Hoặc tự làm
  │
  └─► [7] Report cho user
```

## DETECTION MATRIX

### Symptoms → Actions

| Symptom | Severity | Action |
|---------|----------|--------|
| "I'm not sure what to do" | Warning | Gửi guidance cụ thể |
| "Found a problem" | High | INTERVENE ngay |
| "This is taking longer than expected" | Medium | Check progress, có thể guide |
| Error messages trong output | High | INTERVENE - analyze error |
| Agent đi sai hướng (output không match criteria) | High | CORRECTION PROTOCOL |
| "Task complete" nhưng chưa verify | Low | Chưa trust - VERIFY |
| Agent stuck > 2 phút | High | INTERVENE |
| Same issue lặp lại | Critical | ESCALATE |
| Agent không respond | Critical | Kill + respawn |

### Red Flags (không tin agent)

- Agent claim "done" nhưng chưa check files
- "I think this is correct" thay vì "verified by X"
- Có lỗi trong output nhưng agent proceed
- Agent ignore part của task
- Output không match acceptance criteria

## ACTIVE VERIFICATION

### Khi nào verify

1. **Agent claim "done"** → KHÔNG tin → verify trước
2. **Agent report "complete"** → Check evidence
3. **Agent gửi file changes** → Inspect files
4. **Agent nói "pass"** → Run tests yourself

### Verification checklist

```
□ Files tồn tại đúng path?
□ Code match acceptance criteria?
□ Tests run và pass?
□ No obvious errors?
□ Output format đúng?
□ Logic đúng?
□ Edge cases handled?
```

### Verification methods

```bash
# Check file exists
ls -la /path/to/file

# Run tests
cd /path && npm test

# Inspect output
tmux capture-pane -p -t <pane-id>

# Check git diff
cd /path && git diff --stat

# Run linter
cd /path && npm run lint
```

### Trust level

| Agent says | Trust level | Action |
|------------|--------------|--------|
| "Error: X" | 100% | Analyze error |
| "I found issue" | 100% | Investigate |
| "Done - created file X" | 50% | Verify file exists |
| "Tests pass" | 70% | Run tests yourself |
| "Complete - see diff" | 40% | Inspect diff |
| "I'm done" | 0% | Verify everything |

## CORRECTION PROTOCOL

### Khi nào correct

- Output không match acceptance criteria
- Agent đi sai hướng
- Logic sai
- Missing requirements
- Same mistake lặp lại

### Correction flow (5 bước)

```
[1/5] Identify WHAT is wrong      → Be specific
[2/5] Identify WHY it went wrong   → Root cause
[3/5] Write corrective instruction → Cụ thể, có example
[4/5] Send to agent via send-to-pane
[5/5] Re-verify sau correction
```

### Correction message template

```
[CORRECTION REQUIRED]
Task: <original task>
Issue: <what is wrong - BE SPECIFIC>
Root cause: <why it went wrong>
Correction: <exactly what to do>
Evidence: <proof this is the right direction>

Example:
[CORRECTION REQUIRED]
Task: Implement JWT refresh token
Issue: Token không được persist sau khi refresh
Root cause: Code refresh nhưng không save vào storage
Correction: Sau khi refresh thành công, gọi SecureStorage.set('refreshToken', newToken)

Do NOT repeat this mistake. Verify before reporting done.
```

### Correction Examples

**Wrong direction:**
```
[CORRECTION] You're implementing password reset but the task asks for 
email verification flow. These are different:
- Password reset: user forgot password → send reset link
- Email verification: new user → verify email exists

Please re-read the task and implement EMAIL VERIFICATION, not password reset.
```

**Missing requirement:**
```
[CORRECTION] Your implementation doesn't handle the case when user 
is already verified (calling verify twice). The task requires:
"Idempotent: calling verify on already-verified user returns success"

Add check at start of verify() function:
if (user.emailVerified) return { success: true, alreadyVerified: true }
```

**Wrong technology:**
```
[CORRECTION] The task specifies using SQLite with better-sqlite3, 
not MongoDB. You used Mongoose models. Please:
1. Remove MongoDB/mongoose code
2. Setup SQLite with better-sqlite3
3. Create tables: users, sessions
4. Rewrite the auth logic
```

**Logic error:**
```
[CORRECTION] In auth.js line 45, you check token expiration AFTER 
decoding. This is wrong - if token is expired, jwt.verify() throws 
BEFORE you can check the payload.

Fix:
try {
  const payload = jwt.verify(token, secret);
  // payload is only reached if token is valid and not expired
} catch (err) {
  // Handle expired/invalid token here
}
```

## TASK ASSIGNMENT TEMPLATE

### Template với Acceptance Criteria

```
[AGENT TASK]
Role: <role>
Task: <specific task description>

Working directory: <path>

Acceptance Criteria (MUST satisfy ALL):
1. <criterion>
2. <criterion>
3. <criterion>

Context:
<additional context>

Reporting: Report when ALL criteria are met. Include evidence for each criterion.
```

### Example

```
[AGENT TASK]
Role: coder
Task: Implement JWT refresh token flow

Working directory: /project/auth

Acceptance Criteria (MUST satisfy ALL):
1. When access token expires, automatically refresh using refresh token
2. Refresh token rotated on each use (new refresh token issued)
3. Refresh token stored in httpOnly cookie
4. Concurrent refresh requests handled (only one succeeds)
5. After 30 days of no activity, user must re-login

Context: Using jsonwebtoken library. Already have login() and verifyToken().

Reporting: Report with:
- Evidence of each criterion met
- Files changed
- How to test each criterion
```

### Acceptance Criteria Checklist

| Type | Criteria |
|------|----------|
| Functional | Does X happen when Y? |
| Error | Does it handle error X gracefully? |
| Edge case | What happens when X is null/empty/max? |
| Security | Is X protected from Y attack? |
| Performance | Does X complete in < Y ms? |
| Idempotent | Can X be called multiple times safely? |
| Atomic | Is X transaction-safe? |

## ESCALATION RULES

### When to escalate

| Attempt | Situation | Action |
|---------|-----------|--------|
| 1st failure | Agent sai hướng | CORRECTION PROTOCOL |
| 2nd failure | Agent lặp lại sai | ESCALATE |
| 3rd failure | Agent liên tục fail | Kill + stronger agent |

### Escalation protocol

```
[ESCALATION]
Task: <task>
Attempts: <count>
Failed: <what>
Root cause: <why agent keeps failing>

Options:
1. Spawn specialist agent with more specific instructions
2. Take over task myself (Hermes)
3. Break task into smaller pieces
```

### Escalation actions

```bash
# Kill failed agent
kill-pane.sh <pane-id>

# Spawn specialist with tighter constraints
spawn-pane.sh "claude-code" "/path" "specialist" \
  "TASK: <specific sub-task>
  CRITICAL: Do NOT deviate from this specification
  VERIFY: Run tests after each change"

# Or take over myself
# Switch to pane or do directly
```

## Agent Types & Startup

| Type | Command | Startup | Best for |
|------|---------|---------|----------|
| claude-code | `claude` | 5s | Complex coding, architecture |
| gemini | `gemini` | 4s | Fast prototyping, research |
| hermes | `hermes-agent` | 3s | Wiki, research, coordination |
| codex | `codex` | 3s | Code completions, fast edits |
| opencode | `opencode` | 3s | Lightweight coding tasks |

## Roles

| Role | Mô tả | Best paired with |
|------|--------|-----------------|
| pm | Project Manager - điều phối, quản lý tiến độ | All roles |
| designer | UI/UX Designer - wireframe, mockup | pm, coder |
| researcher | Researcher - tìm hiểu, so sánh | architect, pm |
| architect | System Architect - DB, API, architecture | coder, reviewer |
| coder | Coder - implement, write code | reviewer, tester |
| reviewer | Reviewer - code review, quality check | coder, pm |
| tester | Tester - viết tests | coder, architect |
| docs-writer | Documentation - viết docs | coder, pm |
| coordinator | Sub-orchestrator - điều phối sub-agents | pm |

## Spawn Flow (6 bước)

```
[1/6] tmux split-window -h         → Tạo pane
[2/6] send-keys "<agent-cmd>"    → Khởi động agent
[3/6] sleep N                      → Đợi load (3-5s)
[4/6] send-keys "You are **role** agent" → Gán role
[5/6] send-keys "[AGENT TASK]..." → Task với ACCEPTANCE CRITERIA
[6/6] "IMPORTANT: Verify..."      → Verify + Report instruction
```

## Scripts

| Script | Chức năng |
|--------|-----------|
| `spawn-pane.sh` | Spawn agent với role + criteria + verification |
| `list-panes.sh` | List all panes |
| `follow-pane.sh` | Capture output từ pane để monitor |
| `send-to-pane.sh` | Gửi message đến pane |
| `switch-pane.sh` | Switch để intervene trực tiếp |
| `kill-pane.sh` | Kill pane |

## FOLLOW - Theo dõi sát sao

### Khi nào follow

- Sau khi spawn agents → ngay lập tức monitor
- Agent đang chạy → check định kỳ (mỗi 30s-1p)
- Agent report → verify trước
- Signs of issues → detect sớm

### Signs cần intervene

- "I'm not sure what to do next"
- Error messages
- Output không match criteria
- Agent stuck
- Agent ignoring part của task
- Same mistake lặp lại

### Cách follow

```bash
# Đọc output của một pane
tmux capture-pane -p -t <pane-id>

# Check status tất cả panes
tmux list-panes

# Gửi message hỏi progress
tmux send-keys -t <pane-id> "[ORCHESTRATOR] Status update?" Enter
```

## REPORT - Agents báo cáo

### Yêu cầu agent report

```
Important: Report back to the orchestrator (Hermes) when:
1. Task is complete - send summary with EVIDENCE
2. Found a problem - describe issue
3. Need a decision - ask clearly
4. Stuck for more than 2 minutes - ask for help

CRITICAL: "Done" is not enough. Include:
- Files changed
- How you verified each acceptance criterion
- Any issues encountered

To report: Say "[REPORT] ..." and wait for verification.
```

### Report format

```
[REPORT] 
Task: <task-name> 
Status: done/issue/need-help 
Evidence: <files, tests, verification results>
```

## Intent → Action

### User muốn bắt đầu multi-agent task

```
"build cái app này", "làm feature lớn"
"spawn agents", "multi-agent", "điều phối"
```
→ Orchestrator: phân tích → spawn → **FOLLOW sát sao** → **VERIFY** → **CORRECT if needed**

### User muốn check progress

```
"agents đang làm gì", "check progress"
"theo dõi", "monitor"
```
→ Follow từng pane qua capture-pane

### User muốn intervene

```
"sửa agent đó", "can thiệp"
"agent kia đang sai"
```
→ Switch sang pane → correct trực tiếp

### User muốn kill

```
"dừng agent", "kill pane"
```
→ kill-pane.sh

## Workflow Examples

### Example: Build Auth System

```
1. Spawn agents:

   Pane 1 (architect):
   spawn với task "Design auth architecture"
   Acceptance: JWT, refresh rotation, httpOnly cookies

   Pane 2 (researcher):
   spawn với task "Research JWT best practices"
   
2. FOLLOW:
   - Monitor architect's design output
   - If going wrong → CORRECTION PROTOCOL
   - If researcher finds issues → inform architect

3. VERIFY:
   - Architect claims design done → verify against criteria
   - Check: JWT? refresh rotation? httpOnly?

4. If wrong direction → CORRECTION
   - Send specific correction
   - Re-verify

5. If 2 failures → ESCALATE
   - Spawn specialist or take over
```

## Tmux Quick Reference

```bash
# Panes
tmux split-window -h              # Split ngang
tmux split-window -v              # Split dọc
tmux list-panes                   # List panes
tmux select-pane -t <id>          # Switch pane
tmux kill-pane -t <id>           # Kill pane
tmux send-keys -t <id> "text"    # Send text
tmux capture-pane -p -t <id>      # Read pane output

# Layout
tmux select-layout even-horizontal
tmux select-layout even-vertical

# Navigation
Ctrl+b q         # Show pane numbers
Ctrl+b Alt+Left  # Previous pane
Ctrl+b Alt+Right # Next pane
Ctrl+b o         # Next pane
```

## INTER-AGENT COMMUNICATION

Agents không tự talk với nhau - Hermes là trung gian. Nhưng có thể coordinate qua Hermes.

### Message types

| Type | Format | Use case |
|------|--------|----------|
| Request | `[TO: architect] Can you share the API spec?` | Agent cần info từ agent khác |
| Response | `[FROM: architect] Here is the API spec...` | Agent reply |
| Broadcast | `[TO: all] New requirement added` | Announce change |
| Delegation | `[TO: coder] Architect finished design, start coding` | Orchestrator assign |

### How to coordinate

```bash
# Agent gửi message qua orchestrator
tmux send-keys -t <pane-id> "[TO: architect] Need the DB schema" Enter

# Hoặc orchestrator relay
# 1. Read from agent A
# 2. Parse what agent B needs
# 3. Send to agent B
tmux send-keys -t <pane-b> "[FROM: orchestrator] From researcher: found issue with..." Enter
```

### Coordination patterns

**Sequential dependency:**
```
architect (design) → [output] → coder (implement)
```
Spawn architect first, wait for report, verify, then spawn coder.

**Parallel independent:**
```
researcher (research A) ─┬─ [results] → architect
designer (wireframes) ────┘
```
Spawn all at once - they don't need each other's output.

**Fan-out/fan-in:**
```
architect → splits into
  ├─ coder-1 (auth module)
  ├─ coder-2 (api module)
  └─ coder-3 (db module)
  
All complete → architect (integrate)
```

## PARALLEL vs SEQUENTIAL

### Khi nào spawn PARALLEL (cùng lúc)

| Situation | Example |
|-----------|---------|
| Independent tasks | Research A + Research B cùng lúc |
| No dependency | Design UI + Setup CI pipeline |
| Waiting for slow task | Trong khi architect design dài, spawn researcher |
| Different domains | Frontend + Backend độc lập |

### Khi nào spawn SEQUENTIAL (từng cái)

| Situation | Example |
|-----------|---------|
| Dependent tasks | Design → Implement → Test |
| Resource contention | 2 agents cùng edit 1 file |
| Need output | Architect output là input cho coder |
| Complex coordination | Quá nhiều agents = overhead quản lý |

### Decision matrix

```
                    │
     Dependencies? │
          ├─ YES ──┼─── YES → SEQUENTIAL (wait for output)
          │        │
          │        └── NO  → PARALLEL (spawn together)
          │
          └─ NO ────────── → PARALLEL (spawn all)
```

### Spawn order guidelines

```
1. Architect/Researcher trước (foundation)
2. Designer/PM second (if needed)
3. Coder last (needs design/spec)
4. Tester/Reviewer cuối (after code exists)
```

### Max agents guideline

| Complexity | Max parallel | Notes |
|------------|--------------|-------|
| Simple task | 2-3 | Keep it simple |
| Medium task | 3-4 | Monitor becomes hard |
| Large task | 5-6 | Need coordinator role |
| Very large | 6+ | Break into sub-projects |

**Rule of thumb:** Nếu cần > 5 agents cùng lúc → nên break thành smaller phases.

## DEAD LETTER QUEUE

Tasks that fail repeatedly go to DLQ - không block workflow.

### DLQ conditions

| Condition | Action |
|-----------|--------|
| 2 consecutive failures | Move to DLQ |
| Agent not respond > 10 min | Mark as DLQ |
| Circular failures (correct → fail → correct → fail) | DLQ |
| Agent hit resource limit | DLQ |

### DLQ structure

```
[DLQ]
Task: <task-name>
Attempts: <count>
Last error: <error>
Root cause: <why it keeps failing>
Created: <timestamp>
Status: pending-review | skipped | retry-later
```

### DLQ handling

```bash
# Check DLQ
cat ~/dlq.log

# DLQ options:
# 1. Retry with more specific instructions
# 2. Break into smaller subtasks
# 3. Spawn specialist agent
# 4. Mark as skipped
# 5. Tự làm (Hermes take over)
```

### DLQ workflow

```
[Task assigned] → [Agent attempts]
                          │
                    success? ──yes──→ ✅ Done
                          │
                         no
                          │
                    attempt < 2? ──yes──→ [CORRECTION] → retry
                          │
                         no
                          │
                    [MOVE TO DLQ]
                          │
              ┌───────────┼───────────┐
              ↓           ↓           ↓
         Retry-later  Skipped   Hermes take over
```

### Retry strategy

| DLQ reason | Retry approach |
|------------|----------------|
| Too complex | Break into subtasks |
| Wrong technology | Change tech stack |
| Missing context | Add more context |
| Agent capability | Spawn different agent type |
| Resource limit | Reduce scope |

## PARALLEL EXECUTION EXAMPLES

### Example 1: E-commerce Platform

```
Phase 1 (PARALLEL - 3 agents):
├─ architect: Design system architecture
├─ researcher: Research payment providers
└─ designer: Wireframes for product pages

[Wait for architect + researcher → verify]
[Designer can work independently]

Phase 2 (SEQUENTIAL after Phase 1):
├─ coder-auth: After architect done → implement auth
├─ coder-api: After architect done → implement API
└─ designer: Continue → product page designs

Phase 3 (PARALLEL - 3 agents after Phase 2):
├─ coder-checkout: After auth + researcher
├─ tester: After coders done
└─ docs-writer: Document APIs

Total: 6 agents, 3 phases
```

### Example 2: Simple Feature (PARALLEL)

```
Task: Add dark mode to existing app

PARALLEL (2 agents):
├─ designer: Create dark mode color palette
└─ coder: Implement theme switching

No sequential needed - designer output is just specs, coder implements independently.
```

### Example 3: Complex Feature (SEQUENTIAL)

```
Task: Build new ML pipeline

SEQUENTIAL:
1. researcher → Research best ML approaches
   ↓ verify output
2. architect → Design pipeline architecture
   ↓ verify output
3. coder → Implement pipeline
   ↓ verify output
4. tester → Write tests and validate
```

## Quy tắc quan trọng

1. **VERIFY trước khi tin** - agent claim "done" không có nghĩa là done
2. **CORRECT cụ thể** - chỉ ra WHAT + WHY + HOW
3. **Escalate sau 2 failures** - không để agent fail mãi
4. **FOLLOW sát sao** - không spawn rồi quên
5. **Acceptance Criteria** - mọi task phải có criteria rõ ràng
6. **Hermes là Orchestrator** - kiểm soát cuối cùng
7. **Parallel when independent** - không cần output của nhau
8. **Sequential when dependent** - cần output để tiếp tục
9. **DLQ for failed tasks** - không block workflow
