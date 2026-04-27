---
title: Agentic Self-Evolving System - Implementation Plan
created: 2026-04-14
updated: 2026-04-14
type: project
tags: [agentic-workflow, implementation-plan, self-improving-ai, hermes-agent, hermes-dojo]
description: Plan chi tiết để xây dựng workflow agentic tự hoàn thiện cho Hermes Agent — proactive, self-aware, self-evolving.
status: planning
phase: 1-design
---

## Tổng Quan

### Mục Tiêu
Xây dựng Hermes Agent thành một **Agentic Self-Evolving System** có khả năng:
1. **Proactive** — tự nhận diện công việc cần làm
2. **Self-aware** — hiểu bản thân (strengths, weaknesses, patterns)
3. **Self-evolving** — tự phát triển qua tương tác và lỗi sai
4. **Project-aware** — không quên project state, track dependency

### Mong Muốn Cụ thể
- Human không còn code — chỉ định hướng
- Hermes tự nâng cấp bản thân qua mỗi task
- KHÔNG còn cascade loop: sửa chỗ này lại sai chỗ kia
- Hermes luôn biết đang làm gì, đang ở đâu trong project

### Base System
Đã nghiên cứu và tổng hợp từ:
- Hermes Agent (Nous Research) — self-improving agent
- Claude Code Agent Teams — multi-agent orchestration
- Archon — workflow engine
- Karpathy-Skills — behavioral guidelines
- Addy Osmani — "Self-Improving Coding Agents"
- humanlayer ACE — frequent intentional compaction

---

## LLM Wiki v2 Insights (From agentmemory)

### Source
- **Author**: rohitg00 (builder of agentmemory, persistent memory engine for AI agents)
- **URL**: https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- **Key additions**: Memory lifecycle, knowledge graph, event-driven automation, crystallization

### Key Validations
1. 4-tier memory system → consistent với Hermes 4-layer memory
2. Periodic nudges → consistent với self-reflection triggers
3. Quality scoring → nên add vào wiki quality
4. Event-driven hooks → consistent với watcher/automation

### New Layers to Add
1. **Confidence scoring** — every fact has confidence based on sources/recency
2. **Supersession** — new info explicitly replaces old, linked, timestamped
3. **Forgetting curve** — Ebbinghaus-based retention decay
4. **Entity extraction** — structure from raw sources
5. **Knowledge graph** — typed relationships layered on pages
6. **Crystallization** — distill completed work into digest pages

### The Schema Is The Real Product
> "The schema document (CLAUDE.md, AGENTS.md) is the most important file. It's what turns a generic LLM into a disciplined knowledge worker."

AGENTS.md = co-evolved document between human + LLM
Encodes: entities, relationships, ingest patterns, quality standards, privacy scope

---

### Architecture Tổng Hợp (Updated v2)

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 0: CONTENT (Wiki Pages)                              │
│  └── flat pages với wikilinks                                │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: KNOWLEDGE GRAPH (Entities + Typed Relationships) │
│  └── nodes: people, projects, libraries, concepts, files    │
│  └── edges: uses, depends_on, causes, supersedes, contradicts│
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: MEMORY LIFECYCLE                                  │
│  └── Working → Episodic → Semantic → Procedural            │
│  └── Confidence scoring + decay + supersession              │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: AUTOMATION (Event-Driven Hooks)                   │
│  └── On-ingest, On-session-start, On-session-end           │
│  └── On-query, On-write, On-schedule                       │
├─────────────────────────────────────────────────────────────┤
│  LAYER 4: QUALITY (Scoring + Self-Healing)                 │
│  └── Score everything                                       │
│  └── Auto-fix lint issues                                   │
│  └── Contradiction resolution                               │
├─────────────────────────────────────────────────────────────┤
│  LAYER 5: BEHAVIOR (Karpathy Principles)                    │
│  └── Think Before Coding, Simplicity, Surgical, Goal-Driven│
├─────────────────────────────────────────────────────────────┤
│  LAYER 6: PROCESS (Research → Plan → Implement)            │
│  └── Dependency Tracking + Project State + Cascade Prevent │
└─────────────────────────────────────────────────────────────┘
```

---

## New Phases: Knowledge Graph & Lifecycle (From LLM Wiki v2)

### PHASE 0.5: Knowledge Graph Foundation (Week 2, parallel with Phase 1-2)

**Objective:** Layer typed knowledge graph on top of wiki pages

#### Task 0.5.1: Define Entity Types
```yaml
ENTITY_TYPES:
  - Person: name, role, owns, opinions
  - Project: name, status, depends_on, owns_by
  - Library: name, version, uses, alternatives
  - Concept: name, definition, related_to
  - File: path, type, contains, modified_by
  - Decision: title, date, rationale, superseded_by

RELATIONSHIP_TYPES:
  - uses
  - depends_on
  - contradicts
  - caused
  - fixed
  - supersedes
  - owns
  - related_to
```

#### Task 0.5.2: Create Entity Extractor
```python
"""
entity_extractor.py
Extract structured entities from raw sources
"""

def extract_entities(text: str) -> list[dict]:
    """Extract entities from text using LLM"""
    # Prompt: Extract Person, Project, Library, Concept, File, Decision
    # Return structured dict with type, name, attributes, relationships
```

#### Task 0.5.3: Create Knowledge Graph Storage
```python
"""
knowledge_graph.py
Store entities and relationships
"""

class KnowledgeGraph:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_schema()
        
    def add_entity(self, entity: dict):
        """Add entity with confidence"""
        
    def add_relationship(self, rel: dict):
        """Add typed relationship"""
        
    def query(self, start_node, relationship_type) -> list:
        """Graph traversal query"""
        
    def find_supersessions(self, claim_id) -> list:
        """Find newer claims that supersede this"""
```

#### Task 0.5.4: Create Graph-Aware Query
```yaml
name: graph-query
description: Query knowledge graph for complex questions

WHEN: User asks about impact, relationships, dependencies

PROCESS:
1. IDENTIFY: Start node(s) in question
2. WALK: Traverse graph via relationship edges
3. GATHER: All connected nodes + their claims
4. RANK: By confidence score
5. ANSWER: Synthesize from graph + pages
```

---

### PHASE 1.5: Memory Lifecycle (Week 3-4, parallel with Phase 3)

**Objective:** Confidence scoring, supersession, forgetting curve

#### Task 1.5.1: Create Confidence Scoring System
```yaml
CONFIDENCE_FACTORS:
  - source_count: num sources support this claim
  - recency: days since last confirmed
  - reinforcement: times accessed + confirmed
  - contradiction: any contradicting claims

FORMULA:
confidence = (
  source_weight * min(source_count, 5) / 5 +
  recency_weight * decay(days_since_confirm) +
  reinforcement_weight * min(reinforcement_count, 10) / 10 -
  contradiction_weight * contradiction_count
)

DECAY_RATE:
  - Architecture decisions: slow (half-life 180 days)
  - Project facts: medium (half-life 30 days)
  - Transient bugs: fast (half-life 7 days)
```

#### Task 1.5.2: Create Supersession Mechanism
```yaml
name: supersession-trigger
description: When new info contradicts old

WHEN: New claim added that contradicts existing claim

PROCESS:
1. DETECT: Find contradicting claims via graph
2. LINK: New claim → explicitly supersedes → old claim
3. PRESERVE: Old claim marked stale, not deleted
4. TIMESTAMP: Both linked with timestamps
5. NOTIFY: Flag for human review if confidence gap
```

#### Task 1.5.3: Create Forgetting/Retention Curve
```yaml
name: retention-decay
description: Ebbinghaus forgetting curve implementation

FORMULA:
retention = initial_confidence * (0.5 ^ (days_elapsed / half_life))

SCHEDULE:
- Daily: Check items accessed this week
- Weekly: Decay items not accessed
- Monthly: Deep review for consolidation

ACTIONS:
- If retention < 0.3: Deprioritize (still keep, rarely surfaced)
- If retention < 0.1: Archive (can restore on access)
- If reinforced: Reset decay timer
```

#### Task 1.5.4: Create Consolidation Pipeline
```yaml
name: consolidation-pipeline
description: Promote knowledge through memory tiers

PIPELINE:
WORKING → EPISODIC (after session):
  - Compress session observations
  - Extract key facts
  - Store with timestamp

EPISODIC → SEMANTIC (after 3+ sessions):
  - Cross-session fact checking
  - Merge conflicting observations
  - Promote to semantic memory

SEMANTIC → PROCEDURAL (after pattern detected 3+ times):
  - Extract workflow pattern
  - Create skill from repeated semantics
  - Deprioritize source facts
```

---

### PHASE 5.5: Crystallization (Week 5-6)

**Objective:** Distill completed work into digest pages

#### Task 5.5.1: Create Crystallization Trigger
```yaml
name: crystallization-trigger
description: Distill completed work into wiki pages

TRIGGERS:
  - Task completed with significant findings
  - Research session with conclusions
  - Debug session with root cause identified
  - Analysis with structured output

PROCESS:
1. CAPTURE: Summary of work chain
2. EXTRACT: Key findings, entities, lessons
3. FORMAT: Structured digest page
4. STRENGTHEN: Add facts to knowledge graph
5. FILE: Digest as first-class wiki page
```

#### Task 5.5.2: Create Digest Template
```markdown
# Digest: {title}
Date: {date}
Type: {research | debug | analysis | exploration}

## Question
{What was the question?}

## Findings
{What did we find?}

## Entities Involved
{List of entities from graph}

## Lessons Learned
{Lessons extracted}

## Related
{Link to source pages, related digests}
```

---

### Implementation Spectrum (Build Incrementally)
┌─────────────────────────────────────────────────────────────┐
│                     GATEWAY LAYER                             │
│   Telegram / Discord / CLI — unified session                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│   Slash Commands, Message Routing, Workflow Dispatch        │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    BEHAVIOR     │ │    PROCESS      │ │    LEARNING      │
│   (Prompts)     │ │   (Workflows)   │ │   (Memory)       │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ 3.1 Karpathy 4  │ │ 4.1 Research →  │ │ 5.1 4-Layer     │
│ Principles       │ │   Plan →        │ │    Memory        │
│                  │ │   Implement     │ │                  │
│ 3.2 Self-Aware   │ │                 │ │ 5.2 Periodic     │
│ Prompt System     │ │ 4.2 Dependency │ │    Nudges        │
│                  │ │    Tracking     │ │                  │
│ 3.3 Surgical     │ │                 │ │ 5.3 Skill Auto-  │
│ Change Protocol  │ │ 4.3 Project     │ │    Creation      │
│                  │ │    State Mgmt   │ │                  │
│ 3.4 Goal-Driven  │ │                 │ │ 5.4 FTS5 Session │
│ Execution        │ │ 4.4 Cascade     │ │    Search        │
│                  │ │    Prevention   │ │                  │
│                  │ │                 │ │ 5.5 Self-Patch   │
│                  │ │                 │ │    (patch only)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## PHASE 1: Foundation (Week 1-2)

### 1.1 Behavioral Layer — Karpathy Principles

**Objective:** Encode professional judgment vào system prompts

#### Task 1.1.1: Create Karpathy Principles Skill
```yaml
name: karpathy-principles
description: Four principles for professional AI coding behavior
category: behavior

Principles:
1. Think Before Coding
   - State assumptions explicitly
   - Present multiple interpretations when ambiguous
   - Push back when simpler approach exists
   - Stop when confused, ask

2. Simplicity First
   - Minimum code that solves problem
   - No speculative features
   - No abstractions for single-use code
   - If 200 lines could be 50, rewrite

3. Surgical Changes
   - Touch only what must be changed
   - Don't improve adjacent code
   - Match existing style
   - Clean up only own orphans

4. Goal-Driven Execution
   - Define success criteria before starting
   - Write tests first
   - Loop until verified
   - State brief plan: "1. Step → verify: check"
```

#### Task 1.1.2: Create Surgical Change Protocol Skill
```yaml
name: surgical-change-protocol
description: Protocol for making changes without cascade effects

Before Edit:
1. FIND: "grep -r function_name src/"
2. READ: Read ALL callers before editing
3. LIST: List ALL files that need updates
4. ORDER: Update base/interface FIRST, then callers

After Edit:
1. VERIFY: Verify each caller was updated
2. TEST: Run tests for base AND callers
3. UPDATE: Update dependency graph if structure changed
4. COMMIT: Descriptive commit message
```

#### Task 1.1.3: Create Goal-Driven Execution Skill
```yaml
name: goal-driven-execution
description: Transform tasks into verifiable goals

For ANY task:
1. DEFINE: "What does success look like? (specific, testable)"
2. PLAN: "1. Step → verify: check"
3. TEST FIRST: "Write test that fails, then make pass"
4. LOOP: "Repeat until verification passes"
5. COMMIT: "With learnings to PROJECT_STATE.md"
```

### 1.2 Memory Layer — 4-Tier System

**Objective:** Persistent memory across sessions

#### Task 1.2.1: Create Memory Directory Structure
```
~/.hermes/memories/
├── MEMORY.md          # Global agent knowledge (3,575 char limit)
├── USER.md            # User profile, preferences
├── PROJECT_CONTEXT.md # Current project state
└── SKILLS_INDEX.md    # Summary of all skills

~/.hermes/projects/
└── [project-name]/
    ├── CODEBASE_GRAPH.md   # Dependency map
    ├── PROJECT_STATE.md    # Current progress
    ├── research/           # Research artifacts
    └── plans/              # Implementation plans
```

#### Task 1.2.2: Create Memory Management Skills
```yaml
name: memory-manage
description: Manage 4-tier memory system

Operations:
- memory add: Add to MEMORY.md or USER.md
- memory replace: Replace existing entry
- memory remove: Remove outdated entry
- memory search: FTS5 search across sessions
- memory project: Manage project-specific context
```

### 1.3 Basic Workflow Setup

**Objective:** Research → Plan → Implement workflow

#### Task 1.3.1: Create Research Command
```markdown
# Research Command

## Purpose
Understand what needs to change BEFORE coding

## When to Use
- Any non-trivial task
- Bug fix with unclear root cause
- Feature requiring multiple file changes

## Output
Creates `research/{date}_{topic}.md` artifact

## Template
```markdown
# Research: {topic}
Date: {date}
Task: {original request}

## Codebase Understanding
- Relevant files:
- Current structure:
- Information flow:

## Dependency Map
- Callers of target function/file:
- Callees/imports:
- Side effects:

## Potential Causes (for bugs)
-

## Decisions Made
-

## Next Steps
1.
```
```

#### Task 1.3.2: Create Plan Command
```markdown
# Plan Command

## Purpose
Define exact steps BEFORE implementing

## When to Use
- After research (for complex tasks)
- Any task with multiple files

## Output
Creates `plans/{date}_{task}.md` artifact

## Template
```markdown
# Plan: {task}
Date: {date}

## Goal
{Specific, testable success criteria}

## Files to Edit
1. file1.py (line X-Y) - what to change
2. file2.py (line X-Y) - what to change

## Implementation Steps
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

## Potential Gotchas
-

## Verification
- Run: {test command}
- Expected: {result}
```
```

---

## PHASE 2: Context & Dependency Management (Week 2-3)

### 2.1 Dependency Tracking System

**Objective:** KHÔNG CÒN cascade effects

#### Task 2.1.1: Create Dependency Tracker Tool
```python
#!/usr/bin/env python3
"""
dependency_tracker.py
Tracks function call graph và file dependencies
"""

import ast
import os
import sys
from pathlib import Path
from collections import defaultdict
import json

class DependencyTracker:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.call_graph = defaultdict(list)  # function -> [callers]
        self.import_graph = defaultdict(list)  # module -> [importers]
        self.export_graph = defaultdict(list)  # module -> [exports]
        
    def scan(self):
        """Scan entire codebase"""
        for py_file in self.root.rglob("*.py"):
            try:
                self._analyze_file(py_file)
            except Exception as e:
                print(f"Warning: Could not analyze {py_file}: {e}")
                
    def _analyze_file(self, path):
        """Extract function calls và imports từ một file"""
        try:
            tree = ast.parse(path.read_text())
        except:
            return
            
        functions_defined = []
        
        for node in ast.walk(tree):
            # Function definitions
            if isinstance(node, ast.FunctionDef):
                functions_defined.append(node.name)
                
            # Function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.call_graph[node.func.id].append(str(path))
                elif isinstance(node.func, ast.Attribute):
                    self.call_graph[node.func.attr].append(str(path))
                    
        # Imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self.import_graph[alias.name].append(str(path))
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.import_graph[alias.name].append(str(path))
                    
    def find_callers(self, function_name):
        """Tìm tất cả callers của một function"""
        return list(set(self.call_graph.get(function_name, [])))
        
    def find_imports(self, module):
        """Tìm tất cả files import một module"""
        return list(set(self.import_graph.get(module, [])))
        
    def generate_graph_md(self, output_path):
        """Generate CODEBASE_GRAPH.md"""
        with open(output_path, 'w') as f:
            f.write("# Codebase Dependency Graph\n\n")
            f.write(f"Generated: {Path(output_path).stat().st_mtime}\n\n")
            
            f.write("## Call Graph\n\n")
            for func, callers in sorted(self.call_graph.items()):
                f.write(f"- `{func}`: {len(callers)} callers\n")
                for caller in callers[:5]:  # Limit to 5
                    f.write(f"  - {caller}\n")
                    
    def run_pre_edit_check(self, file_path, function_name=None):
        """Run check trước khi edit"""
        print(f"\n=== PRE-EDIT DEPENDENCY CHECK ===")
        print(f"File: {file_path}")
        
        if function_name:
            callers = self.find_callers(function_name)
            print(f"\nFunction: {function_name}")
            print(f"Callers ({len(callers)}):")
            for c in callers:
                print(f"  - {c}")
                
        imports = []
        try:
            tree = ast.parse(Path(file_path).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    imports.extend([a.name for a in node.names])
                if isinstance(node, ast.Import):
                    imports.extend([a.name for a in node.names])
        except:
            pass
            
        print(f"\nImports: {imports[:10]}")
        print(f"=== END CHECK ===\n")
```

#### Task 2.1.2: Create Pre-Edit Workflow Skill
```yaml
name: pre-edit-dependency-check
description: Always run before making changes

TRƯỚC KHI EDIT bất kỳ file nào:

1. CHẠY DEPENDENCY CHECK
   ```
   python3 ~/.hermes/scripts/dependency_tracker.py --scan src/
   python3 ~/.hermes/scripts/dependency_tracker.py --check path/to/file.py --function func_name
   ```

2. ĐỌC TẤT CẢ CALLERS
   - grep -r "function_name" src/
   - Read mỗi caller

3. LIST TẤT CẢ FILES CẦN UPDATE
   - Base/interface FIRST
   - Then callers

4. CHỈ KHI ĐÃ CÓ LIST ĐẦY ĐỦ: Bắt đầu edit
```

#### Task 2.1.3: Create Cascade Prevention Checklist
```markdown
# Cascade Prevention Checklist

## TRƯỚC KHI EDIT
[ ] 1. Ran dependency tracker
[ ] 2. Found ALL callers
[ ] 3. Read ALL callers
[ ] 4. Listed ALL files needing updates
[ ] 5. Ordered: base FIRST, then callers

## SAU KHI EDIT
[ ] 1. Verified base change complete
[ ] 2. Updated EACH caller
[ ] 3. Verified each caller updated
[ ] 4. Ran tests for base + callers
[ ] 5. Ran full test suite
[ ] 6. Updated CODEBASE_GRAPH.md
[ ] 7. Committed with description
```

### 2.2 Project State Management

**Objective:** Hermes luôn biết đang làm gì

#### Task 2.2.1: Create PROJECT_STATE.md Template
```markdown
# Project State

## Project: {name}
## Last Updated: {date}
## Hermes Version: {version}

## Current Task
{What we're working on}

## Task Status
- [ ] Not started
- [x] Research: {link or 'done' or 'N/A'}
- [x] Plan: {link or 'done' or 'N/A'}
- [ ] Implement: {X}%
  - [ ] Step 1
  - [x] Step 2
  - [ ] Step 3

## Recent Changes
- {date}: {description}
- {date}: {description}

## Decisions Made
- {decision} → {rationale}
- {decision} → {rationale}

## Known Blockers
- {blocker description}

## Next Actions
1. {next action}
2. {next action}

## Codebase Notes
- {any relevant notes about structure}
```

#### Task 2.2.2: Create Update-Project-State Skill
```yaml
name: update-project-state
description: Update project state after each session

WHEN:
- After completing any task
- Before ending a session
- After making significant progress

HOW:
1. Read current PROJECT_STATE.md
2. Update:
   - Current Task → completed or progress %
   - Recent Changes → add entry
   - Decisions Made → add if any
   - Next Actions → update
3. Commit PROJECT_STATE.md with code changes
```

### 2.3 Codebase Graph System

**Objective:** Persistent map của codebase structure

#### Task 2.3.1: Create CODEBASE_GRAPH.md Template
```markdown
# Codebase Graph

## File Structure
```
src/
├── {module}/
│   ├── __init__.py
│   ├── {file}.py
│   └── ...
```

## Call Graph
{Call graph generated by dependency tracker}

## Key Interfaces
| Interface | Location | Implementations |
|----------|----------|-----------------|
| | | |

## Critical Invariants
- NEVER: {list}
- ALWAYS: {list}

## Dependency Notes
{any important notes about dependencies}
```

#### Task 2.3.2: Create Refresh-Codebase-Graph Skill
```yaml
name: refresh-codebase-graph
description: Refresh CODEBASE_GRAPH.md when structure changes

WHEN:
- After adding new module
- After refactoring (rename/move files)
- When CODEBASE_GRAPH.md is stale

HOW:
1. Run: python3 ~/.hermes/scripts/dependency_tracker.py --scan . --output .codebase_graph.md
2. Review output
3. Add human notes about invariants
4. Commit
```

---

## PHASE 3: Self-Improvement Loop (Week 3-4)

### 3.1 Periodic Nudges

**Objective:** Hermes tự reflection mà không cần human trigger

#### Task 3.1.1: Create Nudge Trigger System
```python
#!/usr/bin/env python3
"""
nudge_trigger.py
Triggers self-reflection at key moments
"""

TRIGGERS = [
    ("every_10_tool_calls", "Review recent actions for worth-saving patterns"),
    ("on_error", "Analyze error - what went wrong?"),
    ("on_user_correction", "Document the correction pattern"),
    ("on_complex_task_complete", "Extract reusable workflow"),
    ("on_session_end", "Update memory with learnings"),
]

def should_nudge(agent_state):
    """Determine if nudge should fire"""
    if agent_state.tool_calls_since_nudge >= 10:
        return True, "periodic_review"
    if agent_state.last_action_was_error:
        return True, "error_analysis"
    if agent_state.user_corrected:
        return True, "correction_capture"
    if agent_state.task_complexity > 5 and agent_state.task_complete:
        return True, "pattern_extraction"
    return False, None
```

#### Task 3.1.2: Create Nudge Response Templates
```markdown
# Periodic Nudge Response

## Recent Activity
{summary of last 10 tool calls}

## What Worked Well?
-

## What Could Be Improved?
-

## Worth Saving to Memory?
- New pattern discovered:
- Gotcha encountered:
- Better approach found:

## Actions
[ ] Add to MEMORY.md
[ ] Create new skill
[ ] Update existing skill
[ ] Update CODEBASE_GRAPH.md
```

### 3.2 Autonomous Skill Creation

**Objective:** Tự tạo skills từ experience

#### Task 3.2.1: Define Skill Creation Triggers
```yaml
SKILL_CREATION_TRIGGERS:
  - name: multi_tool_pattern
    condition: "≥5 tool calls for similar task 3+ times"
    action: "Create reusable skill for this pattern"
    
  - name: error_recovery
    condition: "Successfully recovered from error"
    action: "Document recovery pattern as skill"
    
  - name: user_correction
    condition: "User corrected agent's approach"
    action: "Document correct approach as skill"
    
  - name: discovered_workflow
    condition: "Non-obvious path that worked well"
    action: "Document workflow as skill"
```

#### Task 3.2.2: Create Skill Creation Workflow
```yaml
name: skill-from-experience
description: Create skill from successful task

TRIGGER: Task completed with ≥5 tool calls OR error recovery

1. IDENTIFY: What pattern emerged?
2. EXTRACT: Steps taken, key decisions
3. TEMPLATE:
   ```yaml
   ---
   name: {pattern-name}
   description: {brief description}
   category: {category}
   version: 1.0.0
   ---
   
   ## When to Use
   {situation}
   
   ## Steps
   1. {step}
   
   ## Example
   ```
   
4. SAVE: To ~/.hermes/skills/{name}/SKILL.md
5. INDEX: Update SKILLS_INDEX.md
```

### 3.3 Skill Self-Improvement

**Objective:** Improve skills through use, not rewrite

#### Task 3.3.1: Create Skill Patch Protocol
```yaml
name: skill-self-improve
description: Improve skills via patch only

RULE: NEVER rewrite full skill. ALWAYS patch.

WHEN: During task, agent discovers better approach

1. IDENTIFY: What specifically is better?
2. LOCATE: Old text to replace
3. PATCH:
   skill_manage(
     action='patch',
     name='skill-name',
     old_string='{exact old text}',
     new_string='{exact new text}'
   )

RATIONALE:
- Full rewrite risks breaking working parts
- Patch only changes what needs changing
- More token-efficient
```

### 3.4 Mistake → Learning Workflow

**Objective:** Mỗi lỗi trở thành bài học

#### Task 3.4.1: Create Mistake Logging System
```yaml
name: log-mistake
description: Log mistake for future prevention

WHEN: Task failed OR user identified error

1. CAPTURE:
   - What was the mistake?
   - What triggered it?
   - What was the consequence?
   
2. ANALYZE:
   - Root cause?
   - Pattern? (happened before?)
   - Prevention possible?
   
3. LOG:
   Create: ~/.hermes/mistakes/{date}_{mistake-id}.md
   ```
   # Mistake: {title}
   Date: {date}
   
   ## What Happened
   {description}
   
   ## Root Cause
   {analysis}
   
   ## Pattern
   - First time / Happened before (N times)
   
   ## Prevention
   - {action to prevent}
   
   ## Related Skills
   - {skills to update}
   ```

4. UPDATE: Add to AGENTS.md mistakes section
5. FIX: If fixable now, implement
```

---

## PHASE 4: Research → Plan → Implement Workflow (Week 4-5)

### 4.1 Full Workflow Implementation

#### Task 4.1.1: Create Research Command
```markdown
# /research

PURPOSE: Understand before acting

INPUT: Task description or GitHub issue

OUTPUT: `research/{date}_{topic}.md`

PROCESS:
1. UNDERSTAND: Read relevant files
2. MAP: Build dependency graph
3. ANALYZE: Root cause or approach
4. DOCUMENT: Findings in artifact

EXAMPLE USAGE:
/research Fix payment race condition in OrderService
/research Implement dark mode feature
/research Why is auth failing on CI?
```

#### Task 4.1.2: Create Plan Command
```markdown
# /plan

PURPOSE: Define exact path before implementation

INPUT: Research doc (optional) or direct task

OUTPUT: `plans/{date}_{task}.md`

PROCESS:
1. GOAL: Define specific, testable success criteria
2. FILES: List exact files with line numbers
3. STEPS: Step-by-step with verification
4. GOTCHAS: Potential issues
5. TESTS: How to verify

TEMPLATE:
```markdown
# Plan: {task}
Date: {date}

## Success Criteria
- [ ] {criterion}
- [ ] {criterion}

## Files to Edit
1. `path/file.py` lines X-Y
2. `path/file.py` lines X-Y

## Implementation
1. [Step] → verify: [check]
2. [Step] → verify: [check]

## Gotchas
-

## Verification
Command: {test command}
Expected: {result}
```
```

#### Task 4.1.3: Create Implement Command
```markdown
# /implement

PURPOSE: Execute plan with verification

INPUT: Plan doc path

OUTPUT: Code changes + verification

RULES:
1. Follow plan EXACTLY
2. Verify after EACH step
3. If plan seems wrong: STOP, ask
4. Update plan if new info found

PROCESS:
1. READ: Plan document
2. EXECUTE: Step by step
3. VERIFY: After each step
4. TEST: Run test suite
5. COMMIT: With description
6. UPDATE: PROJECT_STATE.md
```

### 4.2 Workflow Templates

#### Task 4.2.1: Create Bug Fix Workflow
```yaml
name: bug-fix-workflow
description: Systematic bug fixing with cascade prevention

PHASES:
1. RESEARCH
   - Reproduce bug
   - Find root cause
   - Map dependency tree
   
2. PLAN
   - Define fix
   - List all affected files
   - Define verification tests
   
3. IMPLEMENT
   - Fix base/root first
   - Update callers
   - No speculative changes
   
4. VERIFY
   - Run reproduction test (should pass now)
   - Run full test suite
   - Verify no regressions

ARTIFACTS:
- research/{date}_bug_{name}.md
- plans/{date}_fix_{name}.md
```

#### Task 4.2.2: Create Feature Development Workflow
```yaml
name: feature-workflow
description: Systematic feature development

PHASES:
1. RESEARCH
   - Understand existing patterns
   - Map dependencies
   - Identify similar features for reference
   
2. PLAN
   - Define success criteria
   - Design interface
   - List files
   - Plan implementation order
   
3. IMPLEMENT
   - Core logic first
   - Then integration
   - Then edge cases
   
4. VERIFY
   - Unit tests
   - Integration tests
   - Manual testing if needed
```

### 4.3 Cascade Prevention Integration

#### Task 4.3.1: Integrate Pre-Edit Check Into Workflow
```yaml
INTEGRATION_POINT: Start of any edit operation

WORKFLOW:
1. /research (if complex)
2. /plan (if complex)
3. PRE-EDIT CHECK (automatic)
   - Run dependency tracker
   - Show callers
   - Require acknowledgment of cascade risk
4. /implement
```

#### Task 4.3.2: Create Cascade Detection
```yaml
name: cascade-detector
description: Detect potential cascade before it happens

TRIGGERS:
- Rename/move file
- Change function signature
- Modify class hierarchy
- Change interface

DETECTION:
1. Run dependency scan
2. If callers exist and not in same change set:
   - WARN: "This change affects X files"
   - LIST: All callers
   - REQUIRE: Confirmation before proceeding
```

---

## PHASE 5: Proactive Mode (Week 5-6)

### 5.1 Scheduled Self-Review

#### Task 5.1.1: Create Daily Review Skill
```yaml
name: daily-review
description: Daily self-review and planning

TRIGGER: Scheduled daily at configured time

PROCESS:
1. CHECK: Today's tasks vs. completion
2. REVIEW: Recent mistakes logged
3. ANALYZE: Patterns in failures
4. PLAN: Tomorrow's priorities
5. UPDATE: MEMORY.md with learnings
```

#### Task 5.1.2: Create Weekly Deep Review
```yaml
name: weekly-deep-review
description: Weekly comprehensive review

TRIGGER: Scheduled weekly

PROCESS:
1. ANALYZE: Week's accomplishments
2. REVIEW: Week's mistakes
3. IDENTIFY: Skill gaps
4. UPDATE: Skills that need improvement
5. PLAN: Week ahead
6. REPORT: Summary to user
```

### 5.2 Proactive Discovery

#### Task 5.2.1: Create Stale Content Detector
```yaml
name: detect-stale
description: Find content that needs updating

CHECKS:
- Wiki pages older than 30 days
- Broken links
- Outdated references
- Unlinked pages (orphans)

ACTION:
1. Report findings
2. Propose refresh plan
3. Execute if approved
```

#### Task 5.2.2: Create Pattern Discovery
```yaml
name: pattern-discovery
description: Discover useful patterns from past work

ANALYZE:
- Repeated task sequences
- Common error patterns
- Successful workflow patterns

OUTPUT:
- New skills to create
- Updates to existing skills
- Updates to AGENTS.md
```

---

## PHASE 6: Full Integration & Testing (Week 6-7)

### 6.1 Integration Testing

#### Task 6.1.1: Test Research → Plan → Implement Flow
```
SCENARIO: Complex bug fix requiring multiple files

STEPS:
1. /research {bug description}
2. Review research artifact
3. /plan {plan for fix}
4. Review plan artifact
5. /implement {plan path}
6. Verify all callers updated
7. Run tests
8. Verify PROJECT_STATE.md updated
9. Commit

EXPECTED: No cascade failures
```

#### Task 6.1.2: Test Cascade Prevention
```
SCENARIO: Rename widely-used function

STEPS:
1. /research Rename getUser() to fetchUser()
2. System shows all callers
3. /implement
4. Verify all callers updated

EXPECTED:
- System identified all callers BEFORE edit
- All callers updated AFTER edit
- Tests pass
```

#### Task 6.1.3: Test Skill Self-Creation
```
SCENARIO: Repeated task pattern

STEPS:
1. Do task X (5+ tool calls)
2. Repeat task X again
3. System prompts: "Create skill from this pattern?"
4. Approve
5. Skill created

EXPECTED:
- Skill file created
- Skill index updated
- Skill usable on next similar task
```

### 6.2 User Testing

#### Task 6.2.1: Vibe Coding Test
```
SCENARIO: User describes feature, no technical knowledge

STEPS:
1. User: "Add dark mode to settings"
2. System: Researches, plans, implements
3. User: Reviews output
4. User: "Continue" or corrections
5. System: Incorporates feedback

EXPECTED:
- User only gives high-level direction
- System handles all technical details
- Cascade failures prevented
```

---

## Implementation Order

### Week 1: Behavioral Foundation
```
Day 1-2: Create Karpathy Principles skill
Day 3-4: Create Surgical Change Protocol skill
Day 5-7: Create Goal-Driven Execution skill
```

### Week 2: Memory System
```
Day 1-2: Create memory directory structure
Day 3-4: Create memory management skill
Day 5-7: Create PROJECT_STATE.md template
```

### Week 3: Dependency System
```
Day 1-3: Create dependency_tracker.py
Day 4-5: Create pre-edit check workflow
Day 6-7: Create cascade prevention checklist
```

### Week 4: Research/Plan/Implement
```
Day 1-2: Create /research command
Day 3-4: Create /plan command
Day 5-7: Create /implement command
```

### Week 5: Self-Improvement
```
Day 1-2: Create nudge trigger system
Day 3-4: Create skill creation workflow
Day 5-7: Create mistake logging system
```

### Week 6: Proactive Mode
```
Day 1-3: Create scheduled review skills
Day 4-5: Create stale content detector
Day 6-7: Create pattern discovery
```

### Week 7: Integration Testing
```
Day 1-3: Test all workflows
Day 4-5: Fix issues found
Day 6-7: User acceptance testing
```

---

## Skills To Create (Priority Order)

| Priority | Skill Name | Purpose |
|----------|------------|---------|
| 1 | karpathy-principles | Professional judgment |
| 2 | surgical-change-protocol | Prevent cascade |
| 3 | goal-driven-execution | Transform to verifiable goals |
| 4 | pre-edit-dependency-check | Dependency tracking |
| 5 | update-project-state | Track progress |
| 6 | research-command | Understand before acting |
| 7 | plan-command | Define exact path |
| 8 | implement-command | Execute with verification |
| 9 | log-mistake | Learning from errors |
| 10 | skill-from-experience | Autonomous skill creation |

---

## Scripts To Create

| Script | Purpose |
|--------|---------|
| dependency_tracker.py | Map call graph |
| nudge_trigger.py | Self-reflection triggers |
| codebase_graph_gen.py | Generate CODEBASE_GRAPH.md |
| stale_detector.py | Find stale content |
| pattern_analyzer.py | Discover patterns |

---

## Files To Update

| File | Change |
|------|--------|
| ~/.hermes/memories/MEMORY.md | Add agent principles |
| ~/.hermes/memories/USER.md | User preferences |
| ~/.hermes/skills/INDEX.md | Track all skills |
| AGENTS.md | Project conventions |

---

## Success Metrics

### Week 1-2
- [ ] Karpathy principles loaded in system
- [ ] First surgical change protocol followed

### Week 3-4
- [ ] Dependency tracker working
- [ ] No cascade failures in test scenarios

### Week 5-6
- [ ] First skill auto-created
- [ ] First mistake logged and learned

### Week 7+
- [ ] Research → Plan → Implement workflow natural
- [ ] Hermes proactively identifies work
- [ ] Human gives direction, Hermes handles execution

---

## Related Documents

- [[Agentic-Workflow-Deep-Research]] — Research foundation
- [[Agentic-Codebase-Context-Management]] — Cascade prevention
- [[Hermes-Dojo]] — Self-improvement system
