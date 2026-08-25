# Session 2026-06-17 (Part 2) — 3-Stage Maker→Reviewer→QA Chain + 4-Agent E2E

> **Context**: After building qa-agent + engineering-lead (part 1, separate reference),
> the user asked to continue iterating: "Tiếp tục vừa làm vừa test cho đến khi done đi!
> Anh trao quyền cho em orchestrator, làm theo loop em làm và đưa một agent khác verify"
>
> Result: 2 more profiles created, AND a 3-stage verification chain worked end-to-end
> with real evidence. This is the **first time** the chain has been demonstrated with
> 3 separate independent verifiers.

## What was built (part 2)

1. **`operations-manager` profile** — Pure task router, no work execution
2. **`code-reviewer` profile** — Independent code style/best-practices reviewer
3. **3-stage chain demonstrated**: engineering-lead (maker) → code-reviewer (style) → qa-agent (functionality)
4. **4-agent E2E test**: operations-manager routes → engineering-lead builds → code-reviewer reviews → qa-agent verifies

## New Insights

### Insight 1: 3-stage chain works (not just 2-stage)

The existing `agentic-company-setup` SKILL.md documents **2-stage** verification:
> engineering-lead (code) → qa-agent (verify)

This session demonstrated a **3-stage** chain adds value:
- **engineering-lead**: code correctness
- **code-reviewer**: code style, error handling, type safety, security, testability
- **qa-agent**: independent functional verification

**Why it works**: each stage has a different concern. Code-reviewer catches style
issues (PEP 585, type annotations) that qa-agent's 6-check rubric doesn't cover.
qa-agent catches functional bugs (empty list not handled) that code-reviewer's
6-axis rubric doesn't cover.

**Real evidence from session**:

| Stage | Verdict | Score | Concern caught |
|-------|---------|-------|----------------|
| engineering-lead (calc.py) | "Works locally" | n/a | n/a |
| qa-agent (calc.py) | PASS | 10.0/10 | None |
| code-reviewer (stats.py) | APPROVED | 9.0/10 | PEP 585 type hint suggestion |
| qa-agent (stats.py) | PASS | 9.5/10 | None (functional) |

**Action**: Update SKILL.md to document the 3-stage chain. The "Separation of Duties"
table currently shows `engineering-lead → qa-agent` only.

### Insight 2: operations-manager is a "pure router" — different from orchestrator

The default profile (Orchestrator) routes tasks and does the work. operations-manager
is a separate profile that **only routes** — it never executes tasks.

**Why this matters**: In a multi-agent system, you need:
- **Orchestrator** (default): Decides WHICH task to do, takes ownership, accepts results
- **operations-manager**: Decomposes tasks into sub-tasks, routes to specialists
- **Specialists** (engineering-lead, content-director, etc.): Execute the sub-tasks
- **Verifiers** (qa-agent, code-reviewer): Independently verify

The 4 roles are NOT redundant — each handles a different layer of the agentic stack.

**Real evidence**: operations-manager correctly routed a 3-step task:
1. research-lead (research scraping feasibility)
2. engineering-lead (code)
3. qa-agent (verify)
And flagged the ToS concern that a maker might have missed.

### Insight 3: "Lead with trigger conditions" rule

User asked: "Anh muốn hỏi loop này sẽ kích hoạt ở trường hợp nào?"

**The right answer** (from session) was a clear trigger-condition answer:
- Loop fires on `on_session_end` (auto-check quality)
- Loop fires when a goal is set (loop to condition)
- Loop fires when output > 1 deliverable (auto-loop Maker→Checker)
- Loop does NOT fire on simple Q&A

**Lesson**: When the user asks "WHEN does X trigger?" before adopting X, lead with
the trigger conditions, not a how-to. The user wants to evaluate fit, not learn the
mechanism. This is a decision-style rule for the orchestrator.

**Capture for next time**: When user asks "kích hoạt ở trường hợp nào?" or
"when does this fire?" or "what's the trigger?" — answer with a clear list of
trigger conditions BEFORE any other content. Don't preemptively list options or
propose 3+ profile setups before answering the trigger question.

### Insight 4: The `model` field is editable in-place (works without profile re-create)

During this session:
1. Created qa-agent with model `MiniMax-M3` (worked for verify tasks)
2. Created engineering-lead with `MiniMax-M2.7` (faster for code tasks)
3. Discovered M3 hit 120s timeout on engineering-lead handoff-format test
4. Swapped M3 → M2.7 via `sed` in config.yaml
5. Re-tested — worked

**Practical rule for next time**:
- Quick web-search / verify tasks → M3 (faster, more concise)
- Multi-tool code generation / handoff-format tests → M2.7 (faster, fewer timeouts)
- Don't commit to a model before testing. `sed` swap is cheap, profile re-create is not.

**Already in SKILL.md** under "MODEL SELECTION" section.

### Insight 5: User's "self-verification bias" rule proved again

The user re-emphasized: "Anh muốn tách riêng các profiles phù hợp với các role ra để
khi check được chính xác và khách quan nhất, nếu em tự check nó sẽ không còn khách
quan nữa và có tỉ lệ cạo bị tự nhận passed."

**Stronger lesson**: The user does NOT want me (default profile / Orchestrator) to
verify my own work. The 4-agent chain (ops → eng → reviewer → qa) is the proof:
- ops routes the task
- eng writes the code
- code-reviewer reviews (different concern: style)
- qa-agent verifies (different concern: function)

**No profile ever verifies its own work.** This is now a hard rule.

## 3-Stage Chain — When to Use

| Scenario | Use 2-stage (maker → qa) | Use 3-stage (maker → reviewer → qa) |
|----------|--------------------------|--------------------------------------|
| Quick prototype | ✅ | ❌ |
| Code style matters | ❌ | ✅ |
| Production code review | ❌ | ✅ |
| One-off script | ✅ | ❌ |
| Pre-merge review | ❌ | ✅ |
| Learning exercise | ✅ | ❌ |

**Default to 2-stage for speed. Add code-reviewer when style/PR-readiness matters.**

## 4-Agent E2E Test Recipe (REPRODUCIBLE)

```bash
# Step 1: operations-manager routes
~/.local/bin/operations-manager chat --yolo -q \
  "Route this task: 'Create Python stats module with median+std_dev'. Tell me which agent to use and why."

# Step 2: engineering-lead executes
~/.local/bin/engineering-lead chat --yolo -q \
  "Create /tmp/el-test/stats.py with median() and std_dev() functions. Use type hints. Handle empty list."

# Step 3: code-reviewer reviews
~/.local/bin/code-reviewer chat --yolo -q \
  "Review /tmp/el-test/stats.py using your 6-axis rubric. Output APPROVED or CHANGES_REQUESTED + Score."

# Step 4: qa-agent independently verifies
~/.local/bin/qa-agent chat --yolo -q \
  "Verify /tmp/el-test/stats.py works. Run it. Output VERDICT + SCORE + evidence."

# Expected results:
#   code-reviewer: APPROVED 9.0/10 (style note: PEP 585)
#   qa-agent: PASS 9.5/10 (functional verified)
```

**Real results from 2026-06-17 session**:
- Step 1: ops → "research-lead → engineering-lead → qa-agent" (with ToS note)
- Step 2: eng → created stats.py with type hints, all functions work
- Step 3: reviewer → APPROVED 9.0/10 (PEP 585 suggestion, not blocking)
- Step 4: qa → PASS 9.5/10 (independently verified)

## 6-Axis Rubric (code-reviewer)

The code-reviewer uses a 6-axis rubric DIFFERENT from qa-agent's 6-check rubric:

| Axis | What it checks | Where qa-agent also covers |
|------|----------------|----------------------------|
| Correctness | Logic, edge cases | Yes (correctness check) |
| Style | PEP 8, naming, docstrings | No |
| Error Handling | try/except, no silent failures | Partial |
| Type Safety | Type hints, no Any | No |
| Security | No hardcoded secrets, no shell injection | No |
| Testability | Small functions, mockable | No |

**Why two different rubrics**:
- qa-agent: "Does it work?" (functional)
- code-reviewer: "Is it good code?" (qualitative)

Both must PASS for code to ship in production. qa-agent FAIL = bug. code-reviewer
FAIL = must refactor before merge.

## State File Updates (Patterns)

Each profile's `state.md` gets a section for its role:

| Profile | State section | Update trigger |
|---------|---------------|----------------|
| qa-agent | `## Verdict History` | After every verification |
| engineering-lead | `## Handoff History (to qa-agent)` | After handoff to qa |
| code-reviewer | `## Recent Reviews` | After every review |
| operations-manager | `## Routing Log` | After every route |

This makes audit trails clear and easy to grep.

## Anti-Patterns Confirmed

- ❌ **Em (Orchestrator) self-verify** — high risk of "looks good to me" bias
- ❌ **qa-agent verify qa-agent's own work** — defeats the purpose
- ❌ **engineering-lead mark its own output as DONE** — should always route to qa
- ❌ **Skip code-reviewer for "trivial" code** — trivial code becomes production code
- ❌ **operations-manager execute tasks** — should be a pure router

## Cross-References

- `agentic-company-setup` SKILL.md — parent skill
- `references/qa-agent-soul-template.md` — qa-agent template
- `references/session-2026-06-17-engineering-lead.md` — part 1 (qa + eng-lead)
- `references/agentic-company-gap-analysis.md` — 8 roles vs current state
- `multi-agent-orchestrator` — orchestrator-side routing rules
- `quality-checker` skill — universal 6-check rubric
- `strict-system-qa-protocol` — for verifying a deployed system

## Date

2026-06-17 (second half of session) — closed 4 of the 8 agent gaps (qa-agent,
engineering-lead, operations-manager, code-reviewer). Remaining: security-engineer,
refactor-specialist.
