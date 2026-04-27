---
title: Archon & Karpathy-Skills Deep Dive
created: 2026-04-14
updated: 2026-04-14
type: deep-dive
tags: [archon, workflow-engine, claude-code, karpathy, coding-guidelines, self-improvement, yaml-workflows]
description: Phân tích chi tiết Archon (workflow engine) và Karpathy-inspired coding guidelines — hai repo trending tháng 4/2026.
source: https://github.com/coleam00/Archon, https://github.com/forrestchang/andrej-karpathy-skills
---

## Tổng Quan

Hai repo này giải quyết hai vấn đề khác nhau nhưng bổ trợ nhau:

| | Archon | Karpathy-Skills |
|---|---|---|
| **Stars** | 17.6k | 24.9k |
| **Chủ đề** | Workflow engine cho AI coding | Coding guidelines cho Claude Code |
| **Format** | YAML workflows + commands (.md) | Single CLAUDE.md file |
| **Mấu chốt** | Deterministic process + AI fill-in | Encode professional judgment |

---

## #9: Karpathy-Skills — Encoding Professional Judgment

### Nguồn Gốc

Andrej Karpathy observe 4 lỗi cơ bản LLMs mắc khi code:

1. **Wrong assumptions** — Silent misinterpretation, không hỏi
2. **Overcomplication** — 1000 dòng khi 100 đủ, bloat abstractions
3. **Side-effect edits** — Thay đổi code không liên quan vì không hiểu
4. **No verification** — Không define success criteria

### 4 Nguyên Tắc Cốt Lõi

#### 1. Think Before Coding

```
Don't assume. Don't hide confusion. Surface tradeoffs.
```

Force explicit reasoning TRƯỚC khi code:
- State assumptions explicitly — hỏi khi không chắc
- Present multiple interpretations — không chọn silent khi ambiguous
- Push back when warranted — nói ra khi có approach đơn giản hơn
- Stop when confused — đặt tên cái gì không rõ, hỏi

**Ví dụ:**
```
Thay vì: "Okay, I'll assume you meant..."
→ "Bạn muốn X hay Y? Tôi không chắc về requirement này."
```

#### 2. Simplicity First

```
Minimum code that solves the problem. Nothing speculative.
```

Chống lại tendency over-engineer:
- No features beyond what was asked
- No abstractions for single-use code
- No "flexibility" that wasn't requested
- No error handling for impossible scenarios
- If 200 lines could be 50, rewrite it

**Test:** "Would a senior engineer say this is overcomplicated?" If yes, simplify.

#### 3. Surgical Changes

```
Touch only what you must. Clean up only your own mess.
```

Khi edit existing code:
- Don't "improve" adjacent code, comments, formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do it differently
- If you notice unrelated dead code, mention it — don't delete it

**Khi changes tạo orphans:**
- Remove imports/variables/functions mà YOUR changes làm unused
- Don't remove pre-existing dead code unless asked

**Test:** Every changed line should trace directly to the user's request.

#### 4. Goal-Driven Execution

```
Define success criteria. Loop until verified.
```

Transform imperative → declarative goals:

| Instead of... | Transform to... |
|--------------|-----------------|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

**Multi-step plan format:**
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria → LLM loops independently. Weak criteria ("make it work") → constant clarification.

### Cách Install

**Option A: Claude Code Plugin (recommended)**
```
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

**Option B: CLAUDE.md (per-project)**
```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

### Key Insight

> "LLMs are exceptionally good at looping until they meet specific goals. Don't tell it what to do, give it success criteria and watch it go."
> — Andrej Karpathy

### Dấu Hiệu Guidelines Đang Hoạt Động

- Fewer unnecessary changes in diffs
- Fewer rewrites due to overcomplication
- Clarifying questions come BEFORE implementation
- Clean, minimal PRs — no drive-by refactoring

### Tradeoff

Bias toward **caution over speed**. Với trivial tasks (typo fixes, one-liners), dùng judgment — không phải change nào cũng cần full rigor. Goal là reduce costly mistakes trên non-trivial work.

---

## #8: Archon — Workflow Engine Cho AI Coding

### Core Concept

```
Docker → containers
GitHub Actions → CI/CD
Archon → AI coding workflows
```

**Vấn đề:** Khi ask AI agent "fix this bug", kết quả phụ thuộc vào model's mood. Có thể skip planning, forget tests, write PR description ignore template. Every run is different.

**Giải pháp:** Encode development process as workflow. Workflow defines phases, validation gates, artifacts. AI fills in intelligence at each step, nhưng **structure deterministic và owned by developer**.

### 5 Key Properties

| Property | Ý nghĩa |
|----------|---------|
| **Repeatable** | Same workflow, same sequence every time |
| **Isolated** | Every run gets its own git worktree. Run 5 fixes in parallel. |
| **Fire and forget** | Kick off, go do other work, come back to finished PR |
| **Composable** | Mix deterministic nodes (bash scripts) với AI nodes (planning) |
| **Portable** | `.archon/workflows/` — works from CLI, Web UI, Slack, Telegram |

### YAML Workflow Structure

```yaml
nodes:
  - id: plan
    prompt: "Explore and create plan"
    # AI node — fills intelligence

  - id: implement
    depends_on: [plan]
    loop:
      prompt: "Read plan. Implement next task. Run validation."
      until: ALL_TASKS_COMPLETE
      fresh_context: true  # Fresh session each iteration
    # AI loop node — iterates until done

  - id: run-tests
    depends_on: [implement]
    bash: "bun run validate"
    # Deterministic — no AI

  - id: review
    depends_on: [run-tests]
    prompt: "Review changes..."
    # AI node

  - id: approve
    depends_on: [review]
    loop:
      prompt: "Present for review..."
      until: APPROVED
      interactive: true  # Pauses, waits for human
    # Human gate

  - id: create-pr
    depends_on: [approve]
    prompt: "Push and create PR"
```

### Node Types

| Type | Description |
|------|-------------|
| `prompt` | AI node với custom prompt |
| `command` | Reuses a named command (.md file) |
| `bash` | Deterministic shell command |
| `loop` | AI loop — iterates until condition met |
| `interactive` | Human-in-the-loop gate |

### Conditional Execution

```yaml
- id: investigate
  command: archon-investigate-issue
  when: "$classify.output.issue_type == 'bug'"

- id: plan
  command: archon-create-plan
  when: "$classify.output.issue_type != 'bug'"
```

### Trigger Rules

```yaml
trigger_rule: one_success  # Chỉ cần 1 trong các deps thành công
trigger_rule: all_success  # Tất cả deps phải thành công
```

### Built-in Workflows (17 workflows)

| Workflow | Use case |
|----------|----------|
| `archon-assist` | General Q&A, debugging |
| `archon-fix-github-issue` | Fix/implement GitHub issue → PR |
| `archon-idea-to-pr` | Feature idea → plan → PR |
| `archon-smart-pr-review` | Classify PR → run targeted review agents |
| `archon-comprehensive-pr-review` | 5 parallel reviewers |
| `archon-plan-to-pr` | Execute existing plan |
| `archon-architect` | Architectural sweep |
| `archon-refactor-safely` | Safe refactoring with type-check |
| `archon-ralph-dag` | PRD → iterate through stories |
| `archon-resolve-conflicts` | Merge conflict resolution |

### archon-fix-github-issue Workflow (10 phases)

Đây là workflow phức tạp nhất — 10 phases:

```
Phase 1: FETCH & CLASSIFY
  └── extract-issue-number → fetch-issue → classify (bug/feature/enhancement/etc)

Phase 2: RESEARCH (parallel)
  └── web-research

Phase 3: INVESTIGATE (bugs) / PLAN (features)
  └── investigate hoặc plan

Phase 4: IMPLEMENT
  └── implement (fresh context, claude-opus-4-6)

Phase 5: VALIDATE
  └── validate

Phase 6: CREATE DRAFT PR
  └── create-pr (reads PR template, creates draft)

Phase 7: REVIEW (conditional agents)
  └── review-scope → review-classify
      ├── code-review (always)
      ├── error-handling (conditional)
      ├── test-coverage (conditional)
      ├── comment-quality (conditional)
      ├── docs-impact (conditional)

Phase 8: SYNTHESIZE + SELF-FIX
  └── synthesize → self-fix-all

Phase 9: SIMPLIFY
  └── simplify-changes

Phase 10: REPORT
  └── issue-completion-report
```

### Architecture

```
┌──────────────────────────────────────────────────────┐
│  Platform Adapters (Web UI, CLI, Telegram, Slack,     │
│              Discord, GitHub)                         │
└─────────────────────────┬────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│              Orchestrator                            │
│        (Message Routing & Context Management)         │
└──────┬─────────────────┬──────────────────┬──────────┘
       │                 │                  │
       ▼                 ▼                  ▼
┌────────────┐   ┌────────────┐   ┌─────────────────────┐
│  Command   │   │  Workflow  │   │  AI Assistant Clients │
│  Handler   │   │  Executor  │   │   (Claude / Codex)   │
│  (Slash)   │   │   (YAML)   │   │                      │
└────────────┘   └────────────┘   └─────────────────────┘
       │                 │                  │
       └─────────────────┴──────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────┐
│         SQLite / PostgreSQL (7 Tables)              │
│  Codebases, Conversations, Sessions, Workflow Runs,   │
│  Isolation Environments, Messages, Workflow Events    │
└──────────────────────────────────────────────────────┘
```

### Giá Trị Cốt Lõi

**AI only runs where it adds value.** Deterministic steps (bash scripts, git ops, tests) không cần AI. AI chỉ dùng cho planning, code generation, review — những thứ cần judgment.

---

## So Sánh Hai Cách Tiếp Cận

| Aspect | Karpathy-Skills | Archon |
|-------|----------------|--------|
| **What** | Behavioral guidelines (prompt) | Process workflow (YAML) |
| **When** | Every interaction | When running a workflow |
| **Granularity** | Global (cho mọi task) | Per-workflow (define per task type) |
| **Human in loop** | Implicit (judgment call) | Explicit (`interactive: true`) |
| **Validation** | Implicit (human checks) | Explicit (validation nodes) |
| **Best for** | Coding style, judgment calls | Complex multi-step processes |

### Hai cách tiếp cận KHÔNG conflict — bổ trợ nhau

Karpathy-Skills có thể nhúng vào Archon workflows như một phần của prompt. Ví dụ:

```yaml
- id: implement
  prompt: |
    Follow the Karpathy principles:
    1. Think Before Coding — state assumptions
    2. Simplicity First — minimum code
    3. Surgical Changes — touch only what must
    4. Goal-Driven — verify each step

    Read the plan. Implement the next task.
```

---

## Áp Dụng Cho Intelligent Wiki

### Từ Karpathy-Skills

1. **Think Before Coding** → Research Before Writing
   - State assumptions about topic
   - Present multiple interpretations
   - Push back when scope is unclear
   - Stop when topic is ambiguous

2. **Simplicity First** → Minimum Viable Page
   - Start with core concept
   - Add detail only when needed
   - Don't over-link hoặc over-structure

3. **Surgical Changes** → Surgical Edits
   - Touch only the page being updated
   - Don't cascade changes across unrelated pages
   - Clean up own orphans (broken links introduced by your edits)

4. **Goal-Driven Execution** → Wiki Research Loop
   ```
   1. Define topic → verify: outline exists
   2. Research sources → verify: X sources collected
   3. Write section → verify: section has content
   4. Link references → verify: no broken links
   ```

### Từ Archon

1. **Workflow engine cho wiki operations**

```yaml
nodes:
  - id: research
    prompt: "Research topic X. Create outline with sources."

  - id: write-concept
    depends_on: [research]
    prompt: "Write concept page from outline. Follow simplicity."

  - id: validate
    depends_on: [write-concept]
    bash: "python wiki_lint.py check"

  - id: review
    depends_on: [validate]
    prompt: "Review page quality. Check for clarity, completeness."

  - id: approve
    depends_on: [review]
    loop:
      prompt: "Present for approval..."
      until: APPROVED
      interactive: true

  - id: commit
    depends_on: [approve]
    bash: "git add . && git commit"
```

2. **Self-healing workflow**

```yaml
nodes:
  - id: scan
    bash: "python wiki_lint.py scan-broken-links"

  - id: diagnose
    command: wiki-diagnose-link
    depends_on: [scan]
    loop:
      prompt: "Fix next broken link. Verify fix."
      until: ALL_LINKS_FIXED

  - id: validate
    depends_on: [diagnose]
    bash: "python wiki_lint.py check"
```

3. **Quality gate workflow** (như archon-smart-pr-review)

```yaml
nodes:
  - id: score
    command: wiki-score-page

  - id: classify
    prompt: "Classify page quality..."
    # trivial/simple/medium/complex

  - id: expand-depth
    depends_on: [classify]
    when: "$classify.output.needs_depth == 'true'"
    command: wiki-expand-stub

  - id: fix-links
    depends_on: [classify]
    when: "$classify.output.has_broken_links == 'true'"
    command: wiki-fix-links

  - id: verify
    depends_on: [expand-depth, fix-links]
    bash: "python wiki_quality_gate.py"
```

---

## Kết Luận

**Karpathy-Skills** = encoding **professional judgment** vào một file. Mạnh vì đơn giản, merge được vào bất kỳ project nào, giải quyết root cause behavior.

**Archon** = encoding **process** vào YAML. Mạnh vì deterministic, repeatable, có cả human gates, AI loops, và conditional execution.

**Kết hợp:** Dùng Karpathy principles trong prompts, Archon workflow cho execution. Một wiki thông minh cần cả hai — judgment (khi nào research đủ, khi nào page quality đủ) và process (research → write → validate → review → approve).

---

## Related

- [[10 GitHub Trending Repos Lessons]] — Overview của 10 repo trending
- [[Karpathy Auto Research]] — Self-improving AI framework
- [[AI Agents]] — Multi-agent systems và autonomous AI
- [[Claude Code Best Practices]] — Claude Code patterns
