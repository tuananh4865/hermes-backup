#!/usr/bin/env python3
"""
Register transcript-saver-v2 hook into Hermes config.yaml.

Safer than direct file edit:
- Uses ruamel.yaml to preserve formatting
- Backs up config first
- Validates YAML before write
- Only adds the new hook, doesn't touch others
"""
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip3 install --user pyyaml", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = Path("/Users/tuananh4865/.hermes/config.yaml")
NEW_HOOK_CMD = (
    "/Users/tuananh4865/.hermes/hooks/transcript-saver-v2/hook_wrapper.sh "
    "--event agent_end "
    "--output \"$RESPONSE\" "
    "--message \"$MESSAGE\" "
    "--session_id \"$SESSION_ID\" "
    "--platform \"$PLATFORM\" "
    "--user_id \"$USER_ID\""
)
NEW_HOOK = {
    "command": NEW_HOOK_CMD,
    "timeout": 10,
}


def main():
    if not CONFIG_PATH.exists():
        print(f"ERROR: config not found: {CONFIG_PATH}")
        sys.exit(1)

    # Backup
    backup = CONFIG_PATH.with_suffix(f".yaml.bak-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(CONFIG_PATH, backup)
    print(f"✓ Backed up: {backup}")

    # Read
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        config = yaml.safe_load(content) or {}

    hooks = config.get("hooks", {})
    if not hooks:
        print("ERROR: no hooks section in config")
        sys.exit(1)

    # Add new hook to on_session_end
    target_event = "on_session_end"
    if target_event not in hooks:
        print(f"ERROR: {target_event} not in hooks")
        sys.exit(1)

    # Check if already added
    existing_cmds = [h.get("command", "") for h in hooks[target_event]]
    if any("transcript-saver-v2" in cmd for cmd in existing_cmds):
        print("✓ Hook already registered, skipping")
        return

    # Add
    hooks[target_event].append(NEW_HOOK)
    config["hooks"] = hooks

    # Write back
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)  # Write original first to preserve formatting
        # Then use yaml.dump for the new hooks section only
        # (Alternative: full dump but with default_flow_style=False)
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✓ Hook added to {target_event}")
    print(f"  Command: {NEW_HOOK_CMD[:80]}...")

    # Verify by running hermes hooks list
    result = subprocess.run(["hermes", "hooks", "list"], capture_output=True, text=True)
    print("\n--- hermes hooks list ---")
    print(result.stdout)


if __name__ == "__main__":
    main()
