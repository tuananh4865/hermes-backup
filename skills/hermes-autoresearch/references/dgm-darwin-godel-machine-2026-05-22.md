# Self-Improving Agents — May 22, 2026 Update

## NEW: Darwin Gödel Machine (DGM)

**arXiv:** 2505.22954 | **Published:** Jan 2026, OpenReview | **Organization:** Sakana.ai

### What It Is
World's first self-improving coding agent that iteratively modifies its own code to improve performance on programming tasks.

### Core Mechanism
Combines two theoretical frameworks:
- **Darwinian evolution** — stepped stone discovery, random mutation + selection
- **Gödel machine** — self-referential improvement (system rewrites its own code when provably beneficial)

### Key Innovation
FROZEN pretrained FMs (Foundation Models) can self-improve by modifying their own code/workflows WITHOUT retraining. The model weights stay fixed; the agent learns to modify its scaffolding, prompts, and execution strategies.

### Why It Matters for Hermes
1. **Self-improvement without retraining** — directly applicable to Hermes self-improvement loop
2. **Open-ended exploration** — finds improvement paths humans would miss
3. **Codified as workflow** — not just research, it's an operational pattern

### How DGM Works (4-Stage Loop)
1. **Seed generation** — create variation candidates (code, prompts, configs)
2. **Evaluation** — score candidates against objective function
3. **Selection** — keep top performers, discard rest
4. **Iteration** — repeat with mutated variants of winners

### Relationship to Prior Techniques
| Technique | Self-Modifies | Retraining Required | Approach |
|-----------|--------------|---------------------|----------|
| ERL | Heuristics only | No | Experience → memory → retrieval |
| SICA | Scaffolding code | No | Edit own scaffolding (17→53% SWE-Bench) |
| **DGM** | **Any component** | **No** | **Evolutionary search + Gödel verification** |
| Hyperagents | Meta-procedure | Yes (RL) | Cross-domain strategy transfer |
| RetroAgent | Feedback policy | No | Dual intrinsic feedback |

### Hermes Applicability: HIGH
- Can be applied to Hermes workflow optimization (cron scheduling, skill selection, memory management)
- Non-destructive: doesn't require retraining
- Embodies "never stop" philosophy of autoresearch

### Sources
- https://sakana.ai/dgm/
- https://openreview.net/forum?id=pUpzQZTvGY
- https://github.com/jennyzzt/dgm