# Karpathy AutoResearch — Research Notes

## Source
- GitHub: https://github.com/karpathy/autoresearch
- Stars: 78K+
- Author: Andrej Karpathy

## Core Concept

AI agents running research on single-GPU LLM training automatically. Give an agent a small but real setup and let it experiment autonomously overnight.

## Key Design Principles

### 1. Single File to Modify
The agent ONLY touches `train.py`. Everything is fair game: architecture, optimizer, hyperparameters, batch size, model size. This keeps scope manageable.

### 2. Fixed Time Budget
Training always runs for exactly **5 minutes**, regardless of platform. This means:
- ~12 experiments/hour
- ~100 experiments while you sleep
- Results directly comparable regardless of changes
- Finds most optimal model for your time budget

### 3. Git is Memory
Every experiment is a commit. Failures can be rolled back cleanly. No need for external memory systems.

### 4. Program.md is the Skill
```markdown
# You're not touching Python files. 
# You're programming the program.md
```

The `program.md` is a super lightweight "skill" that programs the agent. Human edits this file to guide the agent.

## The Experiment Loop

```
LOOP FOREVER:
1. Look at git state: current branch/commit
2. Tune train.py with experimental idea
3. git commit
4. Run: uv run train.py > run.log 2>&1
5. Read results: grep "^val_bpb:" run.log
6. If val_bpb improved (lower) → keep
7. If val_bpb same/worse → git reset
8. Record in RESULTS.tsv
9. Repeat
```

## Key Insight

> "Once the experiment loop has begun, do NOT pause to ask the human if you should continue. The human might be asleep, or gone from a computer and expects you to continue working indefinitely until you are manually stopped. You are autonomous."

## What Made It Work

1. **Narrow scope**: One file, one metric
2. **Single metric**: val_bpb (bits per byte) — lower is better
3. **Fast iteration**: 5 min × many experiments = compounding improvement
4. **Git memory**: Rollback when needed
5. **Never stop**: Agent runs until human interrupts

## Application to Hermes

We adapted this pattern for Hermes Agent with:

1. **3 research focuses** instead of 1
2. **Multi-dimensional metrics** instead of single
3. **Progress reports every 30 min** for visibility
4. **program.md guides agent** (not hardcoded instructions)
5. **Git is memory** (branch per session, commits per experiment)

## Why Narrow Scope Matters

From the article:
> "When the objective function is ambiguous or multi-dimensional, the pattern breaks down. If success isn't a single number but a combination of factors — performance, latency, memory, code readability, user experience — the agent has no clean way to make keep/discard decisions."

We addressed this with SUCCESS CRITERIA (stop when ANY met) rather than continuous optimization.
