---
title: "Self-Evolution Integration — Wiki + Hermes Agent"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [self-evolution, hermes, wiki, dspy, gepa, optimization]
phase: planning
---

# Self-Evolution Integration — Wiki + Hermes Agent

## Nguồn gốc
**Source**: [NousResearch/hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution)

Clone tại: `~/wiki/hermes-agent-self-evolution/`

## Tổng quan

Áp dụng evolutionary self-improvement (DSPy + GEPA) để tự động tối ưu:
1. **Wiki pages** — như "skills" cho knowledge agent
2. **Hermes agent skills** — cải thiện skills hiện có
3. **Memory patterns** — tối ưu cách agent ghi nhớ và truy xuất knowledge
4. **Agent behavior** — cải thiện response quality

**Chi phí**: ~$2-10 per optimization run, không cần GPU

---

## 1. Architecture Adaptation

### Wiki như Skill Ecosystem

Wiki pages tương đương với "skills" trong Hermes framework:

| Wiki Component | Hermes Concept | Áp dụng GEPA |
|----------------|----------------|---------------|
| Concept pages | Skill files | Evolve content quality |
| Index pages | Skill hub | Evolve linking structure |
| _meta/start-here | Skill entry point | Evolve onboarding flow |
| Wiki structure | Skill ecosystem | Evolve cross-linking patterns |
| SCHEMA.md | Skill spec template | Evolve schema itself |

### 3-Tier Optimization Model

```
Tier 1: Wiki Pages (Content)
├── concept pages → evolve explanations, examples, clarity
├── task pages → evolve procedures, steps, commands
└── reference pages → evolve API docs, tool references

Tier 2: Wiki Structure (Architecture)
├── index pages → evolve navigation structure
├── cross-links → evolve link topology
└── _meta files → evolve schema, templates

Tier 3: Hermes Agent (Agentic)
├── agent skills → evolve SKILL.md files
├── memory system → evolve memory patterns
└── system prompts → evolve agent behavior
```

---

## 2. DSPy + GEPA Integration

### Cài đặt

```bash
cd ~/wiki/hermes-agent-self-evolution
pip install -e ".[dev]"

# Verify installation
python -c "import dspy; print(dspy.__version__)"
```

### Cấu hình

```python
# ~/wiki/hermes-agent-self-evolution/wikievo/config.py
from evolution.core.config import EvolutionConfig

WIKI_EVOLUTION_CONFIG = EvolutionConfig(
    iterations=10,
    optimizer_model="openai/gpt-4.1",      # Mutations & reflections
    eval_model="openai/gpt-4.1-mini",       # Fast scoring
    judge_model="openai/gpt-4.1-mini",
    max_skill_size=15_000,                 # Max wiki page size
    max_prompt_growth=0.5,                 # Max 50% growth
    train_ratio=0.6,
    val_ratio=0.2,
    eval_dataset_size=20,                   # Examples per page
)
```

---

## 3. Wiki Page Evolution Pipeline

### 3.1. Page Selection Strategy

Ưu tiên cao:
- Pages có `quality < 6.0` (poor/fair content)
- Pages có `tags: [stubs]` (cần expand)
- Pages có nhiều views nhưng low quality

Ưu tiên thấp:
- Pages đã ở quality > 8.0 (excellent)
- Generated/automated pages

### 3.2. Evaluation Dataset Generation

```python
from evolution.core.dataset_builder import SyntheticDatasetBuilder
from dataclasses import dataclass

@dataclass
class WikiEvalExample:
    task_input: str      # "Explain X concept"
    expected_behavior: str  # "Should include definition, examples, related concepts"
    page_context: str   # Current page content
    difficulty: str      # easy/medium/hard
    category: str        # explanation/tutorial/reference

# Generation prompt for wiki pages
WIKI_TEST_CASE_PROMPT = """
Given a wiki page about {concept}, generate test cases that evaluate:
1. Does the page explain the concept clearly?
2. Are there good examples?
3. Are related concepts linked?
4. Is the difficulty appropriate?
5. Is the structure scannable?

For each test case provide:
- task_input: what a reader might ask/search
- expected_behavior: rubric for good content
- difficulty: easy/medium/hard
- category: explanation/example/structure/reference
"""
```

### 3.3. Fitness Metrics

```python
@dataclass
class WikiFitnessScore:
    correctness: float      # Content accuracy (0-1)
    clarity: float           # Readability score (0-1)
    completeness: float      # All aspects covered (0-1)
    structure: float        # Good headings, lists (0-1)
    links: float            # Proper wiki-links (0-1)
    examples: float          # Has good examples (0-1)

    def composite(self) -> float:
        return (
            0.30 * self.correctness +
            0.20 * self.clarity +
            0.15 * self.completeness +
            0.15 * self.structure +
            0.10 * self.links +
            0.10 * self.examples
        )
```

### 3.4. Constraint Gates

```python
WIKI_CONSTRAINTS = {
    "size_limit": 15_000,        # chars
    "growth_limit": 0.5,         # max 50% growth
    "min_examples": 1,            # At least 1 example
    "min_links": 3,               # At least 3 wiki-links
    "valid_frontmatter": True,     # Must have YAML frontmatter
    "no_broken_links": True,       # All links resolve
    "quality_threshold": 6.0,      # Min quality score
}
```

---

## 4. Hermes Agent Skills Evolution

### 4.1. Existing Skills Analysis

```bash
# List all Hermes skills
ls ~/.hermes/skills/

# Analyze skill quality
python -m evolution.skills.evolve_skill \
    --skill wiki-self-heal \
    --iterations 10 \
    --eval-source synthetic \
    --dry-run
```

### 4.2. Target Skills for Evolution

**Priority 1 (High Impact)**:
- `wiki-self-heal` — self-healing wiki patterns
- `wiki-self-evolution` — autonomous improvement
- `memory-hygiene` — memory management
- `autonomous-wiki-agent` — main agent loop

**Priority 2 (Medium Impact)**:
- `deep-research` — research workflow
- `spec-driven-development` — spec writing
- `skill-factory` — meta-skill for creating skills

**Priority 3 (Nice to Have)**:
- All apple-* skills
- All ios-* skills
- All mlops-* skills

### 4.3. Evolution Workflow

```bash
# Full evolution for a skill
python -m evolution.skills.evolve_skill \
    --skill wiki-self-heal \
    --iterations 10 \
    --eval-source synthetic \
    --hermes-repo ~/.hermes/hermes-agent \
    --run-tests
```

Output saved to:
```
output/wiki-self-heal/20260412_143022/
├── evolved_skill.md
├── baseline_skill.md
└── metrics.json
```

---

## 5. Memory System Evolution

### 5.1. Memory Patterns as Evolvable Units

Giống như skills, memory patterns có thể evolved:

```
memory patterns/
├── user_profile.md      → User preferences, communication style
├── memory_notes.md      → Persistent notes about facts
├── session_context/     → Per-session context
└── skill_knowledge/    → How to use skills effectively
```

### 5.2. Memory Evolution Target

```python
class MemoryPatternEvolution:
    """
    Evolve memory patterns for better knowledge retention.

    What to optimize:
    - What to remember (relevance)
    - How to format memory (clarity)
    - When to update (freshness)
    - How to retrieve (recall)
    """

    targets = [
        "user_preferences",
        "project_context",
        "skill_metadata",
        "convention_patterns",
    ]
```

### 5.3. Session Data Mining

```python
# Extract patterns from session history
from evolution.core.external_importers import build_dataset_from_external

dataset = build_dataset_from_external(
    skill_name="memory-usage",
    sources=["hermes", "claude-code"],
    output_path=Path("datasets/memory"),
)
```

---

## 6. Continuous Improvement Loop

### 6.1. Automated Cron Pipeline

```yaml
# Cron: Daily Self-Evolution Check
name: Daily Self-Evolution
schedule: "0 4 * * *"  # 4 AM daily
skills:
  - hermes-dojo
  - deep-research

pipeline:
  1. Scan for degraded performance
     - Check recent task success rates
     - Identify skills with low scores

  2. Select candidates for evolution
     - Top 3 skills needing improvement
     - Top 3 wiki pages needing expansion

  3. Run targeted evolution
     - GEPA optimization (10 iterations each)
     - Synthetic eval dataset generation

  4. Quality gate
     - All constraints must pass
     - Improvement > 5% required

  5. Human review
     - Commit to preview branch
     - Notify via Telegram

  6. Deploy (if approved)
     - Merge to main
     - Monitor for regressions
```

### 6.2. Hermes Dojo Integration

```python
# ~/wiki/concepts/hermes-dojo.md
HERMES_DOJO_CRITERIA = {
    "min_improvement": 0.05,      # 5% minimum improvement
    "max_cost_per_run": 10.0,     # $10 max per evolution
    "max_iterations": 20,         # Per skill
    "parallel_evolutions": 3,      # Max concurrent
    "escalation_threshold": 3,    # Fail 3x → human review
}
```

---

## 7. Implementation Phases

### Phase 1: Setup (1-2 days)
- [ ] Install hermes-agent-self-evolution
- [ ] Configure DSPy API keys
- [ ] Set up output directory structure
- [ ] Create wiki-specific evaluation templates

### Phase 2: Pilot (3-5 days)
- [ ] Evolve 3 wiki pages (proof of concept)
- [ ] Evolve 1 Hermes skill (wiki-self-heal)
- [ ] Validate constraint system
- [ ] Tune fitness metrics

### Phase 3: Automation (1 week)
- [ ] Set up cron job for daily evolution
- [ ] Build Telegram notification system
- [ ] Create review workflow
- [ ] Document best practices

### Phase 4: Scaling (2 weeks)
- [ ] Batch evolution for all low-quality pages
- [ ] Evolve all Hermes skills
- [ ] Set up A/B testing framework
- [ ] Build evolution history dashboard

---

## 8. Expected Outcomes

| Metric | Baseline | After 1 Month |
|--------|----------|---------------|
| Wiki quality (avg) | ~5.5 | 7.0+ |
| Hermes skill scores | ~6.0 | 8.0+ |
| Task success rate | ~80% | 90%+ |
| Manual updates needed | 100% | 30% |
| Agent autonomy | Low | High |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| GEPA produces worse output | High | Strict constraint gates, human review |
| API costs balloon | Medium | Cost limits, caching, dry-run first |
| Skill drift from purpose | High | Semantic preservation checks |
| Broken wiki links | Medium | Link validation in constraints |
| Overfitting to eval set | Medium | Holdout set required |

---

## 10. Quick Start Commands

```bash
# 1. Install evolution environment
cd ~/wiki/hermes-agent-self-evolution
~/hermes-evolution-venv/bin/pip install -e ".[dev]"

# 2. Set API key (from .env)
MINIMAX_API_KEY=$(sed -n 's/^MINIMAX_API_KEY=//p' ~/.hermes/.env | tr -d '\n\r')
export MINIMAX_API_KEY

# 3. Dry run on a skill
HERMES_AGENT_REPO=~/.hermes ~/hermes-evolution-venv/bin/python -m evolution.skills.evolve_skill \
    --skill wiki-orphan-resolution \
    --iterations 5 \
    --eval-source synthetic \
    --optimizer-model minimax/MiniMax-M2.7 \
    --eval-model minimax/MiniMax-M2.7 \
    --dry-run

# 4. Full evolution (MiniMax API)
HERMES_AGENT_REPO=~/.hermes ~/hermes-evolution-venv/bin/python -m evolution.skills.evolve_skill \
    --skill wiki-orphan-resolution \
    --iterations 5 \
    --eval-source synthetic \
    --optimizer-model minimax/MiniMax-M2.7 \
    --eval-model minimax/MiniMax-M2.7

# 5. Check results
cat output/wiki-orphan-resolution/*/metrics.json | jq '.improvement'
```

## 11. Bugs Fixed in hermes-agent-self-evolution

These bugs were discovered and patched locally in `~/wiki/hermes-agent-self-evolution`:

### Bug 1: Validate raw skill not body (CRITICAL)
**File**: `evolution/skills/evolve_skill.py`
**Issue**: Line 122 validated `skill["body"]` (markdown without frontmatter) instead of `skill["raw"]` (full skill with frontmatter). All evolved skills failed `skill_structure` constraint even when frontmatter was valid.
**Fix**: Changed `validate_all(skill["body"]...)` → `validate_all(skill["raw"]...)`

### Bug 2: Python single-quote syntax from MiniMax
**File**: `evolution/core/dataset_builder.py`
**Issue**: MiniMax-M2.7 model returns Python dict syntax with single quotes (`{'key': 'value'}`) instead of JSON double quotes. `json.loads()` failed to parse.
**Fix**: Added `ast.literal_eval` fallback chain: json.loads → ast.literal_eval → regex extract + replace

### Bug 3: Missing API key in dspy.LM
**File**: `evolution/core/dataset_builder.py`
**Issue**: `dspy.LM(config.judge_model)` called without api_key, causing auth failures for MiniMax.
**Fix**: Pass `api_key=os.getenv("MINIMAX_API_KEY")` to dspy.LM

## 12. Verified Working

- [x] MiniMax-M2.7 as optimizer + eval model
- [x] Synthetic dataset generation (3 examples per skill)
- [x] GEPA optimization runs and converges
- [x] Constraint validation passes for valid skills
- [x] Evolution results saved to `output/{skill_name}/{timestamp}/`
- [x] hermes_dojo.py cron job configured for 4AM daily
- [x] Wiki page evolution (as separate skill-like artifacts) — implemented in hermes_dojo.py
- [x] Hermes agent skill auto-deployment — deploy_skill() in hermes_dojo.py
- [x] Telegram notification on evolution complete — send_telegram() via Bot API

---

_Last updated: 2026-04-12_

