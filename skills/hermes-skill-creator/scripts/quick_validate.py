#!/usr/bin/env python3
"""
Hermes Skill Quick Validator v1.0
Ported từ anthropics/skills skill-creator/scripts/quick_validate.py
Adapted cho Hermes workflow (Vietnamese comments + stricter rules cho Hermes paths).

Usage:
    python quick_validate.py <skill_directory>

Exit codes:
    0 = valid
    1 = invalid (with reason)
"""
import sys
import re
from pathlib import Path

# Hermes extensions: allow version, author, license, platforms, metadata (extended)
ALLOWED_PROPERTIES = {
    'name', 'description', 'license', 'allowed-tools', 'metadata',
    'compatibility', 'version', 'author', 'platforms',  # Hermes additions
}


def validate_skill(skill_path):
    """Basic validation of a skill per Anthropic spec + Hermes extensions."""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "❌ SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "❌ No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "❌ Invalid frontmatter format (need `---` at start AND end)"

    frontmatter_text = match.group(1)

    # Parse YAML (lazy import to avoid hard dep)
    try:
        import yaml
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "❌ Frontmatter must be a YAML dictionary"
    except ImportError:
        return False, "❌ PyYAML not installed. Install via: pip install pyyaml"
    except yaml.YAMLError as e:
        return False, f"❌ Invalid YAML in frontmatter: {e}"

    # Check for unexpected keys
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        return False, (f"❌ Unexpected key(s): {', '.join(sorted(unexpected))}. "
                       f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}")

    # Required: name + description
    if 'name' not in frontmatter:
        return False, "❌ Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "❌ Missing 'description' in frontmatter"

    # Validate name (kebab-case)
    name = str(frontmatter.get('name', '')).strip()
    if not name:
        return False, "❌ Name is empty"
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"❌ Name '{name}' must be kebab-case (lowercase + digits + hyphens)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"❌ Name '{name}' cannot start/end with hyphen or have consecutive hyphens"
    if len(name) > 64:
        return False, f"❌ Name too long ({len(name)} chars, max 64)"

    # Validate description
    desc = str(frontmatter.get('description', '')).strip()
    if not desc:
        return False, "❌ Description is empty"
    if '<' in desc or '>' in desc:
        return False, "❌ Description cannot contain angle brackets (< or >)"
    if len(desc) > 1024:
        return False, f"❌ Description too long ({len(desc)} chars, max 1024)"

    # Hermes-specific: warn if description looks weak (no trigger contexts)
    weak_triggers = ['use this skill', 'for tasks', 'helps with']
    pushy_triggers = ['BẮT BUỘC', 'ALWAYS', 'MUST', 'cụ thể contexts', 'specific trigger',
                      'ngay cả khi', 'even if', 'khi user nói']
    has_pushy = any(t.lower() in desc.lower() for t in pushy_triggers)
    if not has_pushy:
        # Warning, not error — but flag for awareness
        print(f"⚠️  Description may be too generic (no 'pushy' trigger contexts found)")
        print(f"   Recommended: add specific trigger phrases like 'khi user nói X', 'BẮT BUỘC dùng khi...'")

    # Validate compatibility if present
    compat = frontmatter.get('compatibility', '')
    if compat and (not isinstance(compat, str) or len(compat) > 500):
        return False, "❌ Compatibility must be string ≤ 500 chars"

    return True, f"✅ Skill '{name}' is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)