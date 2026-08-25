#!/usr/bin/env python3
"""
Hermes Description Improver v1.0 (stub + Hermes-specific)
Tham khảo full Anthropic implementation ở skill-creator/scripts/improve_description.py (247 LOC).

Hermes workflow:
1. Load eval_set.json (20 eval queries: 10 should + 10 should-not)
2. Split 60/40 train/test
3. Run baseline eval (current description trigger rate)
4. Call claude CLI để propose improved description
5. Re-eval new description
6. Pick best by TEST score (avoid overfit)
7. Output best_description + report

Usage:
    python improve_description.py \
        --eval-set eval_set.json \
        --skill-path /path/to/skill/ \
        --model claude-sonnet-4-5 \
        --max-iterations 5

NOTE: This is a STUB. Full implementation requires:
- run_eval.py (spawn eval prompts + measure trigger rate)
- parser for grading.json + benchmark.json
- Anthropic API integration (or claude CLI subprocess)

For now, this script:
- Validates inputs
- Generates a prompt template cho claude CLI
- Manages iteration loop structure

Adapt cho Hermes: support Vietnamese eval queries + Hermes skill paths.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Pushy description triggers (Anthropic principle)
PUSHY_TRIGGERS_VI = ["BẮT BUỘC", "ALWAYS", "MUST", "ngay cả khi user không nói rõ",
                     "khi user nói", "khi user đề cập", "trigger ngay cả với"]
PUSHY_TRIGGERS_EN = ["ALWAYS", "MUST", "even if", "whenever user", "trigger immediately"]


def parse_skill_md(skill_path: Path):
    """Extract name + description + body từ SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None
    content = skill_md.read_text()
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not fm_match:
        return None
    import yaml
    fm = yaml.safe_load(fm_match.group(1))
    body = fm_match.group(2)
    return {
        "name": fm.get("name", skill_path.name),
        "description": fm.get("description", ""),
        "body": body
    }


def is_pushy(desc: str) -> bool:
    """Check if description has pushy trigger contexts."""
    all_triggers = PUSHY_TRIGGERS_VI + PUSHY_TRIGGERS_EN
    desc_lower = desc.lower()
    return any(t.lower() in desc_lower for t in all_triggers)


def build_improvement_prompt(name, current_desc, failed_triggers, false_triggers):
    """Build prompt cho claude CLI to propose improved description."""
    return f"""You are optimizing a skill description for Hermes Agent skill called "{name}".

The description appears in Claude's available_skills list. When user sends a query, Claude decides whether to invoke the skill based on this description.

Goal: Description should TRIGGER for relevant queries, NOT trigger for irrelevant ones.

Current description:
"{current_desc}"

Issues to fix:
{chr(10).join(f'- FAILED TO TRIGGER: "{q}"' for q in failed_triggers) if failed_triggers else ''}
{chr(10).join(f'- FALSE TRIGGER: "{q}"' for q in false_triggers) if false_triggers else ''}

Apply these principles:
1. Be PUSHY — include specific trigger contexts ("BẮT BUỘC dùng khi user nói X", "ALWAYS trigger when...")
2. Include both what skill does AND when to use
3. Stay under 1024 chars
4. Don't use angle brackets
5. Keep kebab-case name unchanged

Output ONLY the improved description (no quotes, no preamble)."""


def main():
    parser = argparse.ArgumentParser(description="Improve Hermes skill description via eval-driven loop")
    parser.add_argument("--eval-set", required=True, help="Path to eval_set.json (20 queries)")
    parser.add_argument("--skill-path", required=True, help="Path to skill folder")
    parser.add_argument("--model", default="claude-sonnet-4-5", help="Claude model for proposing improvements")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max iterations")
    parser.add_argument("--output", help="Output JSON file (default: <skill-path>/optimization_report.json)")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    skill_info = parse_skill_md(skill_path)
    if not skill_info:
        print(f"❌ Cannot parse SKILL.md in {skill_path}")
        sys.exit(1)

    # Quick check: is current description pushy?
    pushy_now = is_pushy(skill_info["description"])
    print(f"📊 Current description: {len(skill_info['description'])} chars, pushy={pushy_now}")

    # Stub: generate prompt template (user can run claude CLI manually)
    prompt = build_improvement_prompt(
        skill_info["name"],
        skill_info["description"],
        failed_triggers=[],
        false_triggers=[]
    )
    print(f"\n📝 Generated improvement prompt template ({len(prompt)} chars)")
    print(f"   Run: claude -p '<paste-prompt-here>' --model {args.model}")
    print(f"\n⚠️ STUB: Full eval-driven iteration loop requires run_eval.py (TODO)")
    print(f"   This script validates inputs + generates prompt template.")
    print(f"   See anthropics/skills skill-creator/scripts/run_eval.py for full impl.")

    sys.exit(0)


if __name__ == "__main__":
    main()