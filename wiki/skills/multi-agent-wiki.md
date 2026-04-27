---
name: multi-agent-wiki
description: "Multi-Agent Wiki Coordination Skill"
created: 2026-04-09
updated: 2026-04-09
type: skill
tags: [skill, wiki, multi-agent, automation]
---

# Multi-Agent Wiki Coordination Skill

## When to Use

When you need to handle complex, multi-faceted wiki tasks that would benefit from parallel execution:
- Large gap analysis across multiple domains
- Content generation for many topics simultaneously
- Large-scale refactoring (bulk link fixes, template updates)
- Research + creation cycles

## How Multi-Agent Coordination Works

```
USER REQUEST (complex task)
         ↓
[ORCHESTRATOR AGENT] ← You (the main agent)
         ↓
    DECOMPOSE into sub-tasks
         ↓
    ┌─────┼─────┐
    ↓     ↓     ↓
 [SUB1] [SUB2] [SUB3]  ← spawned via mcp_delegate_task
    ↓     ↓     ↓
    └─────┼─────┘
         ↓
    AGGREGATE results
         ↓
    RESOLVE conflicts
         ↓
    COMMIT + REPORT
```

## Task Decomposition Patterns

**Research Task:**
```
sub-tasks:
  - web_search (priority 1)
  - wiki_review (priority 1)  
  - synthesize (priority 2, deps: [web_search, wiki_review])
```

**Build Task:**
```
sub-tasks:
  - research_req (priority 1)
  - write_code (priority 1, deps: [research_req])
  - write_tests (priority 2, deps: [write_code])
  - write_docs (priority 2, deps: [write_code])
```

**Improve/Wiki Task:**
```
sub-tasks:
  - analyze_gaps (priority 1)
  - generate_content (priority 1, deps: [analyze_gaps])
  - fix_links (priority 2)
  - refresh_stale (priority 2)
```

## Spawning Sub-Agents

Use `mcp_delegate_task` to spawn parallel agents:

```
/mcp_delegate_task
  goal: "Analyze wiki gaps in [domain]..."
  context: |
    Wiki path: ~/wiki
    Look for: missing topics, outdated content, broken links
    Output: JSON to .agent_results/[task_id]-[subtask_id].json
  toolsets: ["terminal", "file", "web"]
```

## Sub-Agent Context Template

Each sub-agent receives:
- Wiki path and structure
- Specific sub-task description
- Where to write results
- Checkpoint mechanism

## Conflict Resolution

When sub-agents produce conflicting outputs:

1. **Detect**: Compare outputs for contradictions
2. **Prioritize**: User edits > Recent > More detailed
3. **Merge**: Keep both perspectives, flag for review
4. **Report**: Notify user of conflicts

## Checkpoint System

Before spawning agents, save state:
```
python3 ~/wiki/scripts/project_state.py checkpoint \
  --action-text "Starting multi-agent coordination" \
  --next-action "aggregate results" \
  --phase "multi-agent-[task-name]"
```

After completion:
```
python3 ~/wiki/scripts/project_state.py checkpoint \
  --action-text "Multi-agent task complete" \
  --next-action "commit and push" \
  --phase "multi-agent-[task-name]-done"
```

## Critical Rules

1. **Always checkpoint before** spawning agents
2. **Always aggregate** before ending session
3. **Always commit** aggregated results
4. **Never let agents run unbounded** — set max_iterations
5. **Fail-safe**: If sub-agent fails, re-assign to main agent

## Example Workflow

```
1. User asks: "Update all LLM-related pages with latest model info"

2. Main agent decomposes:
   - research_llms → sub-agent (web search)
   - update_concepts → sub-agent (write new content)
   - fix_cross_links → sub-agent (link updates)
   - verify_quality → main agent (final check)

3. Spawn 3 agents in parallel via mcp_delegate_task

4. Aggregate results

5. Main agent does final verification

6. Commit + push
```

## Anti-Patterns (Don't Do)

- ❌ Spawn agents without checkpointing first
- ❌ Let agents run without max_iterations limit
- ❌ Skip aggregation step
- ❌ Let conflicts propagate without resolution
- ❌ Forget to commit results

## Related

- [[automation]] — General automation patterns
- [[wiki-self-evolution]] — Self-evolution coordination
- [[project-management]] — Task management
