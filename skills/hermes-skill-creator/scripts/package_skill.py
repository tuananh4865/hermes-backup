#!/usr/bin/env python3
"""
Hermes Skill Packager v1.0
Ported từ anthropics/skills skill-creator/scripts/package_skill.py
Adapted: Hermes-specific excludes (add _task-log.jsonl, eval-viewer/ assets).

Usage:
    python package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python package_skill.py /Volumes/Storage-1/Hermes/skills/my-skill
    python package_skill.py /Volumes/Storage-1/Hermes/skills/my-skill ./dist
"""
import fnmatch
import sys
import zipfile
from pathlib import Path

# Import sibling validator (sys.path adjusted for direct execution)
sys.path.insert(0, str(Path(__file__).parent))
from quick_validate import validate_skill

# Standard excludes
EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git"}
EXCLUDE_GLOBS = {"*.pyc", "*.tmp"}
EXCLUDE_FILES = {".DS_Store", "_task-log.jsonl"}  # Hermes: don't package task logs
# Root-only excludes
ROOT_EXCLUDE_DIRS = {"evals", "workspace", "iteration-*"}  # eval working dirs


def should_exclude(rel_path: Path) -> bool:
    """Check if path should be excluded."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS or part.startswith('.') for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    if any(fnmatch.fnmatch(parts[0], pat) for pat in ROOT_EXCLUDE_DIRS):
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package_skill(skill_path, output_dir=None):
    """Package skill folder into .skill file (zip format)."""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None
    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None
    if not (skill_path / "SKILL.md").exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Validate first
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Fix validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()
    skill_filename = output_path / f"{skill_name}.skill"

    # Create zip
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                if should_exclude(arcname):
                    continue
                zipf.write(file_path, arcname)
        print(f"✅ Packaged: {skill_filename}")
        return skill_filename
    except Exception as e:
        print(f"❌ Error creating .skill file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill-folder> [output-dir]")
        print("\nExample:")
        print("  python package_skill.py /Volumes/Storage-1/Hermes/skills/my-skill")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging: {skill_path}")
    if output_dir:
        print(f"   Output: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()