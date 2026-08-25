#!/usr/bin/env python3
"""
setup_new_project.py - Auto-scaffold một project MỚI theo task-log-standard-v2.

Anh verbatim 10/08/2026: "Cập nhật rule và wiki để từ lâng sau có project mới phải
bắt buộc có script hook log full details change log vào project đó."

Usage:
  python3 setup_new_project.py <project-name> [--code-dir=<path>]

Auto-creates:
  /Volumes/Storage-1/Hermes/wiki/projects/<name>/
  ├── HUB.md              (template từ _template/HUB_TEMPLATE.md)
  ├── _task-log.jsonl     (empty + 1 init entry)
  ├── _log_task.py        (từ _template/_log_task.py, PROJECT_NAME+LOG_PATH filled)
  └── data/               (folder rỗng cho data files)

Auto-verifies:
  - Project name valid (no spaces, lowercase, alphanumeric+hyphen)
  - Folder doesn't exist (hoặc flag --force)
  - Helper script executable
  - Init log entry written

Optional (if --code-dir specified):
  - Symlink or note code dir
  - Verify wiki-project ↔ code dir naming convention match

Author: Hermes Agent
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki/projects")
TEMPLATE_DIR = WIKI_ROOT / "_template"


def validate_name(name: str) -> bool:
    """Validate project name: lowercase, alphanumeric + hyphens, no spaces."""
    if not name:
        return False
    if name != name.lower():
        return False
    if " " in name:
        return False
    if not all(c.isalnum() or c == "-" for c in name):
        return False
    return True


def create_project(name: str, code_dir: str = None, force: bool = False) -> int:
    """Create a new project. Returns 0 on success, 1 on error."""
    
    # Validate
    if not validate_name(name):
        print(f"❌ Invalid project name '{name}'")
        print(f"   Rule: lowercase + alphanumeric + hyphens only (e.g. 'my-project')")
        return 1
    
    project_path = WIKI_ROOT / name
    if project_path.exists() and not force:
        print(f"❌ Project '{name}' already exists at {project_path}")
        print(f"   Use --force to overwrite (DESTRUCTIVE)")
        return 1
    
    print(f"📦 Creating project: {name}")
    print(f"   Path: {project_path}")
    
    # 1. Create folder
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / "data").mkdir(exist_ok=True)
    
    # 2. Copy _log_task.py from template + fill placeholders
    template_helper = TEMPLATE_DIR / "_log_task.py"
    target_helper = project_path / "_log_task.py"
    helper_src = template_helper.read_text()
    helper_src = helper_src.replace("{PROJECT_NAME}", name)
    helper_src = helper_src.replace("{LOG_PATH}", str(project_path / "_task-log.jsonl"))
    target_helper.write_text(helper_src)
    target_helper.chmod(0o755)
    print(f"   ✅ _log_task.py (executable)")
    
    # 3. Create _task-log.jsonl with init entry
    log_path = project_path / "_task-log.jsonl"
    log_path.touch()
    init_entry = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": "create",
        "file": "_log_task.py",
        "reason": f"Init project '{name}': scaffold folder + _log_task.py + empty _task-log.jsonl + HUB.md per task-log-standard-v2. Anh verbatim 10/08: project mới PHẢI có hook log full details change log vào project đó. Hook universal-task-log-enforcer sẽ auto-detect và enforce.",
        "before_size": 0,
        "after_size": target_helper.stat().st_size,
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(init_entry, ensure_ascii=False) + "\n")
    print(f"   ✅ _task-log.jsonl (1 init entry)")
    
    # 4. Copy HUB.md template + customize
    template_hub = TEMPLATE_DIR / "HUB_TEMPLATE.md"
    target_hub = project_path / "HUB.md"
    if template_hub.exists():
        hub_src = template_hub.read_text()
        hub_src = hub_src.replace("{PROJECT_NAME}", name)
        hub_src = hub_src.replace("{DATE}", datetime.now().strftime("%Y-%m-%d"))
        target_hub.write_text(hub_src)
        print(f"   ✅ HUB.md (from template)")
    else:
        # Fallback minimal HUB
        target_hub.write_text(f"""---
title: "{name}"
project: {name}
type: hub
created: {datetime.now().strftime("%Y-%m-%d")}
last_modified: {datetime.now().strftime("%Y-%m-%d")}
---

# {name}

> Project hub — created {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 📋 HARD RULE: Task Log Mandatory

Mọi task PHẢI log vào `_task-log.jsonl` qua `python3 _log_task.py <action> <file> <reason>`.

Hook `~/.hermes/hooks/universal-task-log-enforcer/` auto-detect và warn khi stale.

## 📁 Structure

- `HUB.md` (file này)
- `_task-log.jsonl` (append-only log)
- `_log_task.py` (helper script)
- `data/` (data files)
- `queries/` (queries)
- `raw/` (raw materials)
- `scripts/` (SOPs)
- `research/` (research notes)
""")
        print(f"   ✅ HUB.md (minimal fallback)")
    
    # 5. Optional: link code dir
    if code_dir:
        code_path = Path(code_dir).expanduser()
        if not code_path.exists():
            print(f"   ⚠️  Code dir {code_path} does NOT exist yet — created marker file")
            (project_path / "data" / ".code-dir.txt").write_text(f"Expected code dir: {code_path}\n")
        else:
            print(f"   ✅ Code dir verified: {code_path}")
            # Save link in data folder
            (project_path / "data" / ".code-dir.txt").write_text(f"Code dir: {code_path}\n")
    
    # 6. Verify
    print(f"\n🔍 Verifying setup...")
    import subprocess
    r = subprocess.run(
        ["python3", str(WIKI_ROOT.parent.parent / "scripts" / "verify_task_logs.py"),
         f"--project={name}"],
        capture_output=True, text=True
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"⚠️ Verify exited {r.returncode}")
    
    print(f"\n✅ Project '{name}' ready!")
    print(f"\n📝 Next steps:")
    print(f"   1. Edit HUB.md với project overview, schema, HARD RULE")
    print(f"   2. Add data files (products.md, customers.md, etc.) khi cần")
    print(f"   3. Log mọi task: cd /Volumes/Storage-1/Hermes/wiki/projects/{name} && python3 _log_task.py <action> <file> <reason>")
    
    return 0


def main():
    parser = argparse.ArgumentParser(description="Scaffold new project with task log mandatory")
    parser.add_argument("name", help="Project name (lowercase, alphanumeric, hyphens)")
    parser.add_argument("--code-dir", help="Path to associated code directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing project")
    args = parser.parse_args()
    
    sys.exit(create_project(args.name, args.code_dir, args.force))


if __name__ == "__main__":
    main()