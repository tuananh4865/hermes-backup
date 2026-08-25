# Self-Debugging Techniques — June 8, 2026

Research session: 3 new self-debugging techniques documented. Total self-improvement techniques: 33+.

## Debug2Fix (2602.18571) — HIGH Applicability

**What it does:** Uses real debugger tools (pdb/lldb) as agents, not just trial-error edit cycles. Spawns a debugger subagent that reads runtime state, sets breakpoints, steps through code to find root cause. Then separate fix agent patches based on debugger diagnosis.

**Why HIGH for Hermes:** Terminal access already exists. Could wire in `pdb`, `lldb`, `python -m pdb` as tools. Hermes could self-debug own gateway code with real runtime traces.

**Key insight:** Debugger > LLM guess. Instead of "here's my patch, try it and see if it works", the agent WATCHES the program run and sees exactly where it fails.

**Source:** https://arxiv.org/abs/2602.18571

## PyCapsule (2502.02928v2) — MEDIUM Applicability

**What it does:** Dual-agent system — one agent executes code and generates runtime execution traces, second agent uses those traces to diagnose failures. Separate of execution from diagnosis.

**Key insight:** Runtime traces as communication medium between fix and diagnosis agents.

**Source:** https://arxiv.org/abs/2502.02928v2

## Self-Improving Coding Agent (2504.15228) — HIGH Applicability

**What it does:** Agent autonomously edits its own source code and improves its behavior based on failure patterns. Not just patching target code — the agent modifies its own scaffolding/prompts/code.

**Why HIGH for Hermes:** Aligns with MOSS source-level self-rewriting. Hermes gateway could self-patch based on repeated failures. Terminal + file access already exist.

**Key insight:** Self-modification of agent's own code, not just external tools. Most powerful form of self-improvement.

**Source:** https://arxiv.org/abs/2504.15228

## Quick Reference: All Self-Debugging Techniques

| Technique | arXiv | Method | Hermes Fit |
|-----------|-------|--------|------------|
| Debug2Fix | 2602.18571 | Debugger integration (PDB/lldb) | **HIGH** |
| PyCapsule | 2502.02928v2 | Dual-agent runtime tracing | MEDIUM |
| Self-Improving Coding Agent | 2504.15228 | Self-modification of agent code | **HIGH** |
| SelfHeal | 2604.17699 | Dual-agent Fix+Critic | HIGH |
| ErrorProbe | 2604.17658 | 3-stage diagnosis team | HIGH |
| ReflexiCoder | — | Self-generated verification | HIGH |
| Polaris | — | Self-consistency verification | MEDIUM |
| DebugRepair | — | Test-case driven repair | MEDIUM |
| DeepVerifier | — | Multi-head verification | MEDIUM |
| ERL | — | Experience replay | MEDIUM |