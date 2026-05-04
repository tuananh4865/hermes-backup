# Karpathy AutoResearch — Research Notes

## Source
- Repo: https://github.com/karpathy/autoresearch
- Stars: 78K+
- Author: Andrej Karpathy

## Core Insight
"You're not touching Python files. You're programming the `program.md`."
— karpathy/autoresearch README

## Key Design Principles

### 1. Single File to Modify
- Agent only touches `train.py` (for Karpathy's case) or `program.md` (for Hermes)
- This keeps scope manageable and diffs reviewable

### 2. Fixed Time Budget
- Karpathy: 5 minutes per experiment
- Hermes: 3 minutes per experiment
- Makes experiments directly comparable regardless of what agent changes

### 3. Git is Memory
- Every experiment = git commit
- Failed experiments = git reset
- Never lose good state
- Branch per experiment session

### 4. Single Metric
- Karpathy: val_bpb (validation bits per byte) — lower is better
- Hermes: WHS (wiki health score) — lower is better

### 5. NEVER STOP
- Loop runs until human interrupts
- Agent should not ask "should I continue?"
- If stuck, try harder

## Karpathy's program.md Structure

```markdown
# Mission
[What the agent is trying to achieve]

## Current state
[Baseline measurements]

## Constraints
[What NOT to do]

## Experiment Ideas
[List of specific things to try]

## Loop Instructions
[Step-by-step experiment loop]
```

## Why This Works

1. **Narrow scope**: Prevents agent from getting lost in ambiguity
2. **Clear metric**: No debate about what "better" means
3. **Fast iteration**: Many experiments per session = more data
4. **Git memory**: Rollback prevents catastrophic mistakes
5. **Autonomy**: Human doesn't need to be in the loop

## Comparison

| Aspect | Karpathy | Hermes |
|--------|----------|--------|
| Domain | LLM training | Wiki health |
| File to modify | train.py | program.md |
| Metric | val_bpb | WHS |
| Time budget | 5 min | 3 min |
| Memory | Git | Git |
| Loop | Forever | Forever |
