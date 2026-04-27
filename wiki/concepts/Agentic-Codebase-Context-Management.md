---
title: Agentic Codebase Context Management - Ending the Cascade Loop
created: 2026-04-14
updated: 2026-04-14
type: deep-dive
tags: [agentic-coding, codebase-context, cascading-effects, dependency-tracking, frequent-compaction, project-state, vibe-coding, context-engineering]
description: Nghiên cứu chi tiết về cách quản lý codebase context để agent không quên project state và không gây ra cascading side effects khi sửa code.
source: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents, https://www.abstractalgorithms.dev/how-ai-coding-agents-work, https://www.augmentcode.com/learn/cod-model-5-phase-guide-to-codebase-dependency-mapping
---

## Vấn Đề Cốt Lõi: Tại Sao Agent Sửa Chỗ Này Lại Sai Chỗ Khác

### Đây Không Phải Bug — Đây Là Architecture

```
Bạn: "Đừng gọi LegacyBillingClient, chỉ dùng PaymentProcessor"
Agent: "OK, acknowledged!"

...45 phút sau, context overflow...

Agent: "Tôi sẽ import LegacyBillingClient..."
```

**Agent không quên. Agent đã thực sự KHÔNG BAO GIỜ THẤY instruction đó.**

Khi context window overflow, tokens bị evict. Instructions cũ bay ra. Agent không có "trí nhớ mờ" — nó **literal không thấy** những gì đã nói trước đó.

> "The agent hasn't gone dumb; it has literally never seen your earlier instructions. Those tokens were evicted when the window overflowed. This is not a bug in the product. It is the fundamental architecture of every AI coding agent working exactly as designed."
> — Abstract Algorithms

---

## Tại Sao Vibe Coding Thất Bại Với Large Codebase

### Stanford Study (2025-2026)

```
1. A lot of "extra code" shipped by AI tools ends up just reworking the slop shipped last week
2. AI tools work well for greenfield projects, but often counter-productive for brownfield codebases
3. Coding agents are great for new projects, but in large established codebases, they can make developers LESS productive
```

### Triệu Chứng Cụ Thể

| Triệu chứng | Nguyên nhân gốc |
|-------------|------------------|
| Sửa chỗ A, sai chỗ B | Context overflow → instructions bị evict |
| Agent không nhớ đang làm gì | Session không có persistent state |
| Cùng function gọi, cùng lỗi lặp lại | Dependency graph không được track |
| Refactor xong, test cũ fail | Side effects không được map |
| Code mới đè lên code đang hoạt động | Agent không thấy callers của function |

---

## Root Cause: The Stateless Function Problem

LLM là **stateless function**:

```
tokens đi vào → tokens đi ra
```

**Agent = LLM + Tool Registry + Orchestration Loop + Context Manager**

Mỗi turn của agent là một stateless function call:

```
Context Window IN → LLM → Next Action OUT
```

**Đây là lever DUY NHẤT để affect output quality.**

```
Nói cách khác: Context window = BẤT KỲ thứ gì quyết định output.
             = Worth obsessing over.
```

### Context Window Physics

```
Typical context window: ~170k tokens (≈ 130k cho Claude)
Rủi ro: evicted instructions = literally never seen
→ Phải manage context như finite resource
→ 40-60% utilization target
```

---

## Giải Pháp: Frequent Intentional Compaction

Đây là framework từ **humanlayer** (Y Combinator, 2025) — đã được prove với 300k LOC Rust codebase.

### Core Philosophy

```
Thiết kế ENTIRE WORKFLOW xung quanh context management.

Research → Plan → Implement
    ↓         ↓         ↓
Tạo artifacts (markdown files) để persist state
Mỗi phase = fresh context window
Human review ở HIGHEST LEVERAGE points
```

### Tại Sao Research/Plan/Implement?

```
Research output = understanding của codebase
Plan output = exact steps + files cần edit
Implement = step through plan

Bad research → thousands of bad lines
Bad plan → hundreds of bad lines
Bad implementation → bad lines (scoped)
```

**Human review leverage: Research > Plan > Implement**

### Research Phase

```
Input: Feature/bug description
Output: Research doc (.md artifact)

Nội dung research doc:
- Codebase structure liên quan
- Information flow
- Potential causes (cho bug)
- Files cần đọc
- Patterns đang dùng
```

### Plan Phase

```
Input: Research doc (nếu có)
Output: Plan doc (.md artifact)

Nội dung plan:
- Exact steps để fix/implement
- Files cần edit (với line numbers)
- Testing/verification mỗi step
- Potential gotchas
- Acceptance criteria
```

### Implement Phase

```
Input: Plan doc
Output: Code changes + verification

Process:
- Step through plan, phase by phase
- Verify sau mỗi phase
- Compact status back vào plan file
- Fresh context cho phase tiếp theo
```

---

## Dependency Tracking: Không Để Side Effects Bay Đi

### Vấn Đề: Agent Không Biết Function Được Gọi Ở Đâu

```
Agent: "Tôi sẽ rename getPayment() → fetchPayment()"
→ Rename thành công
→ NHƯNG không update callers
→ Test fail
→ Agent không hiểu tại sao
```

### Giải Pháp: Dependency Map

Các tools hiện có:

| Tool | Cách hoạt động |
|------|---------------|
| **code-review-graph** | Tree-sitter AST → persistent structural map → Claude đọc chỉ relevant files |
| **claude-code-graph** | Dependency analysis, call graph mapping |
| **Understand-Anything** | Multi-agent pipeline → knowledge graph của mọi file |
| **BAML's internal tools** | Dependency tracking cho large codebase |

### Dependency Map Nên Chứa

```yaml
# CODEBASE_GRAPH.md

## File Structure
src/
├── payment/
│   ├── payment_processor.py    # Abstract base
│   ├── stripe_processor.py      # implements PaymentProcessor
│   └── legacy_billing.py        # DEPRECATED - don't use
│
## Call Graph
PaymentProcessor (interface)
├── StripeProcessor.get_payment()  ← callers: OrderService, CheckoutFlow
├── PayPalProcessor.get_payment()  ← callers: OrderService
└── LegacyBillingClient.get_payment()  ← DEPRECATED

## Export/Import Chains
OrderService → PaymentProcessor (interface, NOT implementation)
CheckoutFlow → PaymentProcessor (interface, NOT implementation)

## Key Invariants
- NEVER call LegacyBillingClient directly
- Always use PaymentProcessor interface
- All new processors must implement Retryable
```

### Agent Cần Được Instructed Về Side Effects

```
TRƯỚC KHI LÀM GÌ:
→ "Bạn sẽ edit file X. Trước khi edit, tìm TẤT CẢ callers và dependees của X."
→ "Sau khi edit, update TẤT CẢ files gọi X."
```

---

## Project State Management: Không Quên Đang Làm Gì

### Vấn Đề: Session Loss

```
Bạn: "Continue where we left off"
Agent: "Tôi không nhớ chúng ta đang làm gì"
```

### Giải Pháp: Progress Artifact

```markdown
# PROJECT_STATE.md

## Current Task
Fix payment processing race condition in OrderService

## Status
- [x] Research: Done (see research/2026-04-14_payment_race.md)
- [x] Plan: Done (see plans/payment_race_fix.md)
- [ ] Implement: In progress
  - [x] Step 1: Add locking mechanism to OrderService
  - [ ] Step 2: Update CheckoutFlow to use new lock
  - [ ] Step 3: Add integration test
  - [ ] Step 4: Run full test suite

## Context for next session
- Last edit: Added `_lock` attribute to OrderService.__init__
- Working in: src/services/order_service.py
- blocker: Need to find all places CheckoutFlow calls OrderService

## Decisions Made
- Using threading.Lock instead of asyncio.Lock (legacy compatibility)
- NOT changing PaymentProcessor interface (too risky)
```

### Tạo Progress Artifact Sau Mỗi Session

```
Sau mỗi working session, commit cả:
1. Code changes
2. PROJECT_STATE.md updated
3. Any new research/plan docs
```

---

## Implementation: Specific Workflow Cho Vibe Coders

### Workflow: Research Before Touch

```
1. Tạo research doc TRƯỚC KHI code
2. Tìm dependency graph
3. Plan exact changes
4. Implement the plan
5. Verify all callers updated
```

### Step-by-Step:

```
TASK: "Refactor getPayment() method"

1. RESEARCH
   → "Research getPayment() - find all callers, understand the interface contract"
   → Output: research.md với call graph

2. PLAN
   → "Create implementation plan with exact files, line numbers, and verification steps"
   → Output: plan.md với step-by-step

3. IMPLEMENT
   → Step 1: Rename method in PaymentProcessor (base)
   → Verify: grep for all usages, check callers
   → Step 2: Update each caller
   → Verify: run tests
   → ...

4. FINAL VERIFY
   → Run full test suite
   → Check no broken links in call graph
   → Update PROJECT_STATE.md
```

### Workflow: Dependency Check Trước Mỗi Edit

```
TRƯỚC KHI EDIT:
1. `grep -r "function_name" src/` — tìm tất cả callers
2. `grep -r "from module import" src/` — tìm imports
3. List tất cả files cần update
4. Đọc mỗi caller TRƯỚC KHI edit

SAU KHI EDIT:
1. Update base/interface
2. Update TẤT CẢ callers (một cách systematic)
3. Run tests
4. Commit
```

---

## Tooling: Codebase Understanding

### code-review-graph

```bash
# Cài đặt
npm install -g code-review-graph

# Chạy analysis
code-review-graph analyze

# Output: persistent structural map của codebase
# Claude đọc map → biết phải edit những file nào
```

### Build Your Own Dependency Tracker

```python
#!/usr/bin/env python3
"""dependency_tracker.py — Track function call graph"""

import ast
import os
from pathlib import Path
from collections import defaultdict

class DependencyTracker:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.call_graph = defaultdict(list)  # function -> [callers]
        self.import_graph = defaultdict(list)  # module -> [importers]
        
    def scan(self):
        """Scan entire codebase"""
        for py_file in self.root.rglob("*.py"):
            self._analyze_file(py_file)
            
    def _analyze_file(self, path):
        """Extract function calls và imports từ một file"""
        tree = ast.parse(path.read_text())
        # ... AST analysis ...
        
    def find_callers(self, function_name):
        """Tìm tất cả callers của một function"""
        return self.call_graph.get(function_name, [])
        
    def find_imports(self, module):
        """Tìm tất cả files import một module"""
        return self.import_graph.get(module, [])
        
    def generate_report(self):
        """Generate markdown dependency report"""
        # ... generate CODEBASE_GRAPH.md ...
```

---

## Context Compaction Techniques

### Nguyên Tắc: 40-60% Utilization

```
< 40%: Có thể feed thêm context (đang under-utilized)
40-60%: Sweet spot (recommended)
60-80%: Bắt đầu cần compact
> 80%: Nguy hiểm — có thể overflow
> 90%: Almost certainly will lose instructions
```

### Khi Nào Cần Compact

```
1. Context utilization > 60%
2. Bạn thấy agent bắt đầu "lather, rinse, repeat"
3. Agent bắt đầu quên constraints đã đặt
4. Sau mỗi 10-15 tool calls
```

### Compaction Prompt

```
"Compact everything we've done so far into a progress.md file.
 Include:
 - The end goal
 - The approach we're taking
 - Steps we've completed
 - Current failure/blocker
 - Decisions made so far
 
 Then I'll start a fresh session with this as context."
```

### Subagent Cho Compaction

```yaml
# Không dùng main context để search/summarize
# Tạo subagent cho việc đó

- id: research
  command: research_codebase
  context: fresh  # Fresh context window
  
- id: synthesize
  prompt: "Synthesize research findings into structured artifact"
```

---

## Memory Architecture for Projects

### 4 Tiers (Inspired by Hermes Agent)

```
Tier 1: PROMPT MEMORY (Always-on)
├── MEMORY.md — global agent knowledge
├── USER.md — your preferences
└── PROJECT_CONTEXT.md — current project state

Tier 2: PROJECT ARTIFACTS (Per-project)
├── CODEBASE_GRAPH.md — dependency map
├── PROJECT_STATE.md — current progress
├── research/ — research docs
└── plans/ — implementation plans

Tier 3: SESSION SEARCH (On-demand)
├── FTS5 search across all sessions
├── Retrieve relevant past context
└── LLM summarize before inject

Tier 4: SKILLS (Reusable)
├── skill: dependency-check — always run before edit
├── skill: plan-before-implement — enforce research/plan
└── skill: verify-callers — verify all callers updated
```

### PROJECT_CONTEXT.md Template

```markdown
# Project Context

## Project: [Tên Project]
## Last Updated: [Date]

## Architecture
[High-level architecture]

## Key Files
| File | Purpose | Dependencies |
|------|---------|--------------|
| src/a.py | Core logic | b.py, c.py |

## Current Task
[What we're working on]

## Status
- [x] Research: [link to research doc]
- [x] Plan: [link to plan]
- [ ] Implement: [X]%
  - [ ] Step 1
  - [x] Step 2
  - [ ] Step 3

## Active Decisions
- [Decision made] → [Rationale]
- [Decision made] → [Rationale]

## Known Issues
- [Issue 1] — workaround: [workaround]
- [Issue 2] — workaround: [workaround]

## Next Steps
1. [Next action]
2. [Next action]
```

---

## Cascading Effects Prevention Checklist

### Trước Khi Edit

```
[ ] 1. Tìm tất cả callers của function/file
[ ] 2. Tìm tất cả imports của module
[ ] 3. Đọc mỗi caller trước khi edit
[ ] 4. List tất cả files cần update
[ ] 5. Update base/interface TRƯỚC
[ ] 6. Update callers theo systematic order
```

### Sau Khi Edit

```
[ ] 1. Verify base/interface change is complete
[ ] 2. Verify mỗi caller đã updated
[ ] 3. Run tests cho base + callers
[ ] 4. Run full test suite
[ ] 5. Update CODEBASE_GRAPH.md nếu có thay đổi
[ ] 6. Update PROJECT_STATE.md
[ ] 7. Commit với descriptive message
```

### Research Before Modify

```
[ ] 1. Tạo research doc
[ ] 2. Map dependency graph
[ ] 3. Identify all affected files
[ ] 4. Create plan with verification steps
[ ] 5. Get human review of plan (nếu complex)
[ ] 6. Implement the plan
[ ] 7. Verify all steps
```

---

## Common Failure Modes

### Failure Mode 1: Rename Without Update Callers

```
Problem: Rename function, don't update callers
Fix: Always grep for usages before AND after rename
```

### Failure Mode 2: Change Interface Without Update Implementations

```
Problem: Change base class, don't update derived classes
Fix: Map inheritance tree before change
```

### Failure Mode 3: Refactor Without Map Side Effects

```
Problem: Refactor A, break B that A affects
Fix: Draw dependency graph before refactoring
```

### Failure Mode 4: Session Loss

```
Problem: Start new session, agent forgets everything
Fix: Always update PROJECT_STATE.md at end of session
```

---

## Workflow Summary: Research → Plan → Implement

```
┌─────────────────────────────────────────────────────────────┐
│  RESEARCH: Understand what needs to change                  │
│  - Read relevant code                                       │
│  - Map dependencies (callers, callees, imports)            │
│  - Identify side effects                                   │
│  - Output: research.md artifact                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PLAN: Define exact steps                                    │
│  - List files to edit with line numbers                     │
│  - Define verification for each step                       │
│  - Identify potential gotchas                               │
│  - Output: plan.md artifact                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  IMPLEMENT: Execute with verification                       │
│  - Step through plan systematically                         │
│  - Verify after each step                                   │
│  - Update callers before/after                              │
│  - Keep context fresh (compact if > 60%)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  VERIFY: Ensure no regressions                              │
│  - Run affected tests                                       │
│  - Run full test suite                                      │
│  - Update PROJECT_STATE.md                                  │
│  - Commit                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Related

- [[Agentic-Workflow-Deep-Research]] — Self-evolving AI systems
- [[Archon-and-Karpathy-Skills-Deep-Dive]] — Workflow engine và coding guidelines
- [[Karpathy-Auto-Research]] — Self-improvement framework
- [[Hermes-Agent-Architecture]] — Hermes Agent internals
