---
title: Agentic Workflow Deep Research - Self-Evolving AI Systems
created: 2026-04-14
updated: 2026-04-14
type: deep-dive
tags: [agentic-workflow, self-improving-ai, hermes-agent, continuous-learning, autonomous-agents, claude-code, karpathy, archon, skills, memory]
description: Nghiên cứu sâu về mô hình workflow agentic tự hoàn thiện - từ Hermes Agent, Claude Code Agent Teams, Archon, đến mô hình con người không còn code nữa.
source: https://addyosmani.com/blog/self-improving-agents/, https://mranand.substack.com/p/inside-hermes-agent-how-a-self-improving, https://archon.diy/book/, https://claude.ai/blog/auto-mode
---

## Tổng Quan Nghiên Cứu

**Mong muốn:** Xây dựng một workflow agentic siêu thông minh có khả năng:
1. Proactive — tự động nhận diện công việc
2. Self-aware — nhận thức được bản thân (strengths, weaknesses, patterns)
3. Self-evolving — tự phát triển qua tương tác và lỗi sai

**Nguồn nghiên cứu:**
- Hermes Agent (Nous Research) — self-improving agent with built-in learning loop
- Claude Code Agent Teams + Auto Mode (Anthropic) — multi-agent orchestration
- Archon — workflow engine cho AI coding
- Karpathy-Skills — behavioral guidelines
- Addy Osmani — "Self-Improving Coding Agents"
- Ralph Wiggum / Compound Product loops

---

## Mô Hình Mới: Human không còn Code nữa

Đây là paradigm shift đang xảy ra ở các công ty như Anthropic:

```
TRƯỚC:
Human: viết code → review → merge

SAU:
Human: đưa ra định hướng → Claude Code tự nâng cấp bản thân → ship feature
```

**Thay đổi cốt lõi:**
- Human **không viết code** nữa — chỉ định hướng
- Claude Code **tự viết, tự test, tự review, tự fix**
- Claude Code **tự tạo skills mới** từ experience
- Claude Code **tự optimize chính workflow** của mình

**Mấu chốt:** Human như "product owner/architect" — define WHAT, AI handle HOW.

---

## Mô Hình 3 Layers Cho Self-Evolving Agent

Sau khi tổng hợp từ Hermes Agent, Archon, Claude Code, đây là architecture đầy đủ:

```
┌─────────────────────────────────────────────────────────────┐
│                     LAYER 1: BEHAVIOR                      │
│  Karpathy-Style Principles (encoded in prompts)            │
│  ├── Think Before Coding (state assumptions)               │
│  ├── Simplicity First (minimum code)                       │
│  ├── Surgical Changes (touch only what must)               │
│  └── Goal-Driven Execution (verify each step)               │
│                                                             │
│  → Quản lý "làm sao cho đúng" — professional judgment     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     LAYER 2: PROCESS                        │
│  Archon-Style Workflow Engine (YAML + Commands)             │
│  ├── Workflows define phases, gates, artifacts             │
│  ├── Deterministic nodes (bash) + AI nodes (prompt/command) │
│  ├── Human approval gates                                   │
│  ├── Evaluation gates (pass/fail criteria)                 │
│  └── Parallel execution (worktree isolation)               │
│                                                             │
│  → Quản lý "làm gì, làm khi nào" — process structure       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     LAYER 3: LEARNING                       │
│  Hermes-Style Closed Learning Loop                          │
│  ├── Memory: persistent across sessions                     │
│  ├── Skills: autonomous creation from experience            │
│  ├── Session Search: FTS5 + LLM summarization               │
│  ├── Periodic Nudges: self-reflection triggers             │
│  └── Skill Self-Improvement: patch not rewrite            │
│                                                             │
│  → Quản lý "tự cải thiện như thế nào" — meta-learning    │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 3 Chi Tiết: The Learning Loop

Đây là phần quan trọng nhất — cách agent thực sự tự hoàn thiện.

### 3.1 Four-Layer Memory System (Hermes Agent)

```
Layer 1: PROMPT MEMORY (Always-on)
├── MEMORY.md — agent's persistent knowledge
├── USER.md — user profile, preferences, context
└── Limit: 3,575 chars total (forced curation)

Layer 2: SESSION SEARCH (On-demand)
├── SQLite + FTS5 full-text search
├── LLM summarization before injection
├── Episodic memory: what happened when
└── Separate from skills (procedural memory)

Layer 3: SKILLS (Procedural Memory)
├── ~/.hermes/skills/ — reusable instruction sets
├── agentskills.io compatible format
├── Progressive disclosure (summary only → full on demand)
├── 200 skills ≈ same token cost as 40 (only load what's relevant)
└── Autonomous creation from experience

Layer 4: HONCHO (User Modeling)
├── User modeling dialectic
├── Tracks user preferences over time
└── Adjusts behavior based on user profile
```

### 3.2 Periodic Nudges — Self-Reflection Trigger

```
Every N tool calls OR every complex task:
→ Agent receives internal system prompt
→ "Look back at what happened. What is worth keeping?"
→ Agent decides: write to MEMORY.md? Create skill? Update USER.md?
→ Fires WITHOUT user input
```

**Điểm quan trọng:** Agent tự quyết định cái gì đáng lưu. Không phải dump tất cả, không phải empty. Curation is the job of the agent.

### 3.3 Autonomous Skill Creation

**Trigger conditions (5 signals):**
1. ≥5 tool calls used
2. Recovery from error
3. User correction
4. Non-obvious workflow that worked
5. Pattern detected across sessions

**Skill format (agentskills.io standard):**
```yaml
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]
    requires_toolsets: [terminal]
---
# Skill content: steps, tool calls, file references
```

### 3.4 Skill Self-Improvement

```
When agent finds better path mid-execution:
→ Uses skill_manage tool with patch action
→ Only changed text in tool call (token efficient)
→ Preference: PATCH over EDIT
  - Patch: corrects only what changed
  - Edit: full rewrite risks breaking working code
```

**6 skill actions:**
- `create` — new skill from scratch
- `patch` — targeted change (preferred)
- `edit` — full rewrite (only for major overhauls)
- `delete` — remove skill
- `write_file` — supporting files
- `remove_file` — cleanup

### 3.5 FTS5 Session Search

```
Session archive → SQLite + FTS5 index
Agent searches past context when relevant
Retrieved results → LLM summarization → inject only relevant portion
→ Keeps token usage flat regardless of session history length
```

**Design decision:** Session search = episodic memory (what happened). Skills = procedural memory (how to do). Keep SEPARATE.

---

## Mô Hình Continuous Coding Loop (Ralph Wiggum)

Từ Addy Osmani / Ryan Carson — iterative agent loop:

```
1. PICK NEXT TASK
   └── From task list (JSON), pick unfinished task
   
2. IMPLEMENT
   └── Agent writes/modifies code for that specific task
   
3. VALIDATE
   └── Run tests, type checks, quality gates
   
4. COMMIT
   └── If checks pass → git commit
   
5. UPDATE
   └── Mark task done, log learnings to AGENTS.md
   
6. RESET CONTEXT
   └── Clear agent memory, fresh prompt for next task
   
7. REPEAT
   └── Until all tasks done OR max iterations hit
```

**Tại sao stateless but iterative:**
- Tránh context overflow
- Mỗi task = fresh bounded prompt
- Ít hallucination, cleaner code
- Agent không drift qua nhiều tasks

### Compound Loop (Nâng cao)

```
Phase 1: ANALYSIS LOOP
  └── AI đọc reports → identify what to build
  
Phase 2: PLANNING LOOP  
  └── Generate PRD → tasks JSON
  
Phase 3: EXECUTION LOOP
  └── Implement tasks (Ralph Wiggum loop)
```

**Điểm mạnh:** Agent không chỉ code — nó quyết định WHAT to build dựa trên data.

---

## AGENTS.md Pattern

**File quan trọng nhất** cho persistent learning giữa các iterations:

```markdown
# AGENTS.md — Project Handbook

## Patterns & Conventions
- This project uses SSR
- UI components live in /components
- API routes in /routes

## Gotchas
- When adding new enum, update constants.ts or tests fail
- Always run `npm run type-check` before commit

## Style/Preferences
- Follow ESLint rules as configured
- Prefer functional components over classes
- Use pytest fixtures as in existing tests

## Recent Learnings
- 2026-04-14: Found that feature X causes memory leak in Python 3.12
- 2026-04-13: This API pattern was slow, switched to caching layer
```

**Sau mỗi task:** Append key learnings. Mỗi improvement làm future improvements dễ hơn.

---

## Claude Code Agent Teams

### Multi-Agent Architecture

```
Coordinator Agent (lighter model — dispatch only)
├── Research Agent (Haiku) — gather context
├── Planning Agent (Sonnet) — create plan  
├── Implementation Agent (Opus) — write code
├── Review Agent (Sonnet) — code review
└── QA Agent (Haiku) — validation
```

**Key principle:** Coordinator chỉ route tasks, không làm nặng. Specialized agents cho specialized work.

### Auto Mode

Claude Code's `claude --enable-auto-mode`:

```
- Background safety classifier replaces manual prompts
- Claude decides what's safe
- Blocks prompt injection and risky escalations
- Still has human oversight (can cycle back with Shift+Tab)
```

### Code Review Multi-Agent

Claude Code's internal review system (the one Anthropic uses internally):

```
PR submitted
→ 5 parallel agents review:
│   ├── Code quality agent
│   ├── Error handling agent
│   ├── Test coverage agent
│   ├── Comment quality agent
│   └── Docs impact agent
→ Synthesize findings
→ Auto-fix critical/high issues
→ Report
```

---

## Karpathy Auto Research — Meta-Learning

Karpathy's framework cho self-improvement beyond skill optimization:

```
1. DEFINE CRITERIA
   └── Binary true/false conditions
   └── Exact, not vague
   
2. ESTABLISH BASELINE
   └── Run tests with current version
   └── Score it
   
3. GENERATE HYPOTHESIS
   └── Propose specific change
   └── Based on patterns from real-world data
   
4. RUN ITERATION
   └── Test with separate sub-agent
   └── (Unbiased evaluation)
   
5. EVALUATE OUTCOME
   └── Script-based (deterministic)
   └── OR LLM Judge (subjective)
   
6. DECIDE
   └── Keep change if improved
   └── Discard if not
   
7. REPEAT
   └── Until goal reached OR max iterations
```

**Ứng dụng:** Optimize skills, optimize workflows, optimize BEHAVIOR prompts themselves.

---

## Architecture Tổng Hợp Cho Intelligent Wiki Agent

Dựa trên nghiên cứu, đây là architecture cho một **self-evolving wiki agent**:

```
┌──────────────────────────────────────────────────────────────┐
│                    MESSAGING GATEWAY                         │
│   Telegram, Discord, CLI — unified session                  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                             │
│   Session Management, Slash Commands, Message Routing        │
└──────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    BEHAVIOR     │ │    PROCESS      │ │    LEARNING      │
│   (Prompts)     │ │   (Workflows)   │ │   (Memory)       │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ Karpathy 4      │ │ Wiki Research   │ │ 4-Layer Memory  │
│ Principles      │ │ Wiki Write      │ │ Periodic Nudges  │
│ Self-Awareness  │ │ Wiki Self-Heal  │ │ Skill Creation   │
│ Goal-Driven     │ │ Wiki Quality    │ │ FTS5 Search      │
│                 │ │ Gate            │ │ Honcho User      │
│                 │ │                 │ │ Modeling         │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Wiki-Specific Workflows

**Research Workflow:**
```yaml
nodes:
  - id: define-topic
    prompt: "Define research scope and success criteria"
    
  - id: search
    bash: "python wiki_search.py $topic"
    
  - id: synthesize
    prompt: "Synthesize findings into outline"
    
  - id: validate
    bash: "python wiki_lint.py check"
    
  - id: write
    prompt: "Write wiki page following Karpathy principles"
    
  - id: quality-gate
    command: wiki-quality-score
    # If score < threshold → loop back to write
    
  - id: commit
    bash: "git add . && git commit"
```

**Self-Healing Workflow:**
```yaml
nodes:
  - id: scan
    bash: "python wiki_lint.py scan-broken-links"
    
  - id: diagnose
    prompt: "For each broken link, diagnose cause"
    
  - id: fix
    loop:
      prompt: "Fix next broken link. Verify fix."
      until: ALL_LINKS_FIXED
      
  - id: validate
    bash: "python wiki_lint.py verify"
```

**Mistake → Learning Workflow:**
```yaml
nodes:
  - id: detect-mistake
    prompt: "Analyze what went wrong in this task"
    
  - id: classify
    prompt: "Is this a skill gap? workflow gap? or behavior gap?"
    
  - id: create-fix
    prompt: "Propose specific fix — new skill, workflow update, or prompt change"
    
  - id: implement
    # Patch skill / update workflow / update prompt
    
  - id: verify
    bash: "Test the fix on next similar task"
```

---

## Implementation Roadmap

### Phase 1: Basic Setup (Ngay)
- [ ] Integrate Karpathy 4 principles vào Hermes system prompts
- [ ] Tạo AGENTS.md cho wiki project conventions
- [ ] Setup basic wiki workflows (research → write → validate → commit)

### Phase 2: Memory Layer (Tuần này)
- [ ] Setup 4-layer memory system (MEMORY.md, USER.md, session search, skills)
- [ ] Implement periodic nudges (every 10 tool calls)
- [ ] Setup skill creation triggers

### Phase 3: Self-Improvement (Tuần sau)
- [ ] Implement skill self-patching (patch not rewrite)
- [ ] Create mistake → learning workflow
- [ ] Setup FTS5 session search

### Phase 4: Proactive Mode (Một tuần nữa)
- [ ] Implement daily/weekly proactive research
- [ ] Auto-detect stale content
- [ ] Auto-suggest improvements based on usage patterns

---

## Key Insights Tổng Hợp

### Từ Hermes Agent
1. **Separate episodic vs procedural memory** — session search ≠ skills
2. **Curation over accumulation** — agent decides what's worth keeping
3. **Progressive disclosure** — 200 skills same token as 40
4. **Periodic nudges** — self-reflection without user input

### Từ Archon
1. **Deterministic > flexible** — encode process, AI fills intelligence
2. **Human gates** — approval points prevent runaway automation
3. **Evaluation gates** — pass/fail criteria define done
4. **Fresh context** — reset between tasks prevents drift

### Từ Karpathy-Skills
1. **Goal > imperative** — "define success criteria" beats "do this"
2. **Simplicity** — minimum code, nothing speculative
3. **Surgical** — touch only what must
4. **Verify first** — write test, then make pass

### Từ Claude Code Agent Teams
1. **Specialized agents** — lighter model for coordination
2. **Parallel review** — 5 agents simultaneously
3. **Auto mode** — background safety with human override

### Từ Addy Osmani Compound Loops
1. **Stateless but iterative** — reset context each task
2. **AGENTS.md** — persistent learnings between iterations
3. **Compound loops** — Analysis → Planning → Execution
4. **Small tasks** — atomic, clear pass/fail criteria

---

## So Sánh Các Hệ Thống

| Aspect | Hermes Agent | Claude Code | Archon | Karpathy-Skills |
|--------|-------------|-------------|--------|-----------------|
| **Focus** | Self-improving agent | AI coding assistant | Workflow engine | Behavioral guidelines |
| **Learning** | Built-in loop | Via skills/AGENTS.md | Via workflow updates | Via prompt edits |
| **Memory** | 4-layer explicit | AGENTS.md implicit | Artifact files | CLAUDE.md |
| **Process** | Implicit in agent | Via commands/skills | Explicit YAML | Implicit in principles |
| **Human control** | Via config | Via auto mode | Via approval gates | Via project CLAUDE.md |
| **Best for** | Long-running autonomous | Daily coding | Complex multi-phase | Coding quality |

---

## Related

- [[Hermes Agent Architecture]] — Chi tiết Hermes Agent
- [[Archon and Karpathy-Skills Deep Dive]] — Phân tích 2 repo trending
- [[Karpathy Auto Research]] — Self-improvement framework
- [[AI Agents]] — Multi-agent systems
- [[Claude Code Best Practices]] — Claude Code patterns
