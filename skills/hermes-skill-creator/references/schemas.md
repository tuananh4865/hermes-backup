# JSON Schemas — Hermes Skill Eval System

> Ported từ anthropics/skills skill-creator/references/schemas.md
> Adapted cho Hermes workflow.

## evals.json

Schema cho test cases:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt here",
      "expected_output": "Description of expected result",
      "files": []
    },
    {
      "id": 2,
      "prompt": "Another test prompt",
      "expected_output": "What success looks like",
      "files": ["input.json"]
    }
  ]
}
```

Fields:
- `id` (int): unique eval ID
- `prompt` (string): realistic user prompt (Vietnamese OK)
- `expected_output` (string): mô tả kết quả mong đợi
- `files` (array): input files nếu cần

## eval_metadata.json (per eval directory)

```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": [
    {
      "text": "Description of what to check",
      "passed": true,
      "evidence": "Why it passed"
    }
  ]
}
```

**Required fields:** `text`, `passed`, `evidence` (not `name`/`met`/`details`).

## grading.json (per run directory)

Same as eval_metadata.json — one grading.json per run with all assertions.

## benchmark.json (per iteration)

Output của `aggregate_benchmark.py`:

```json
{
  "skill_name": "my-skill",
  "configs": {
    "with_skill": {
      "run_count": 3,
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90}
    },
    "without_skill": {
      "run_count": 3,
      "pass_rate": {"mean": 0.60, "stddev": 0.10, "min": 0.50, "max": 0.70}
    }
  },
  "deltas": {
    "with_skill_vs_without_skill": 0.25
  }
}
```

## trigger_eval.json (for description optimization)

20 queries: 10 should-trigger + 10 should-not-trigger:

```json
[
  {"query": "edit clip TikTok về Yonex Astrox 99", "should_trigger": true},
  {"query": "viết script bán hàng cho body mist", "should_trigger": true},
  {"query": "Format this data into CSV", "should_trigger": false},
  {"query": "What is the capital of France?", "should_trigger": false}
]
```

**Quality rules:**
- ✅ Realistic context (file paths, column names, user backstory)
- ✅ Near-miss queries (share keywords but shouldn't trigger)
- ❌ Generic ("Format this data" too easy to test)

## feedback.json (from user review)

After `generate_review.py` + user click "Submit":

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback = user thought it was fine.

## Related

- [[../SKILL.md]] — workflow
- [[../scripts/quick_validate.py]] — validates SKILL.md frontmatter
- [[../scripts/aggregate_benchmark.py]] — produces benchmark.json
- [[../scripts/improve_description.py]] — stub for description optimization loop