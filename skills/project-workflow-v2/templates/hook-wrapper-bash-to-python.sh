#!/bin/bash
# Hook Wrapper Template (bash → python with env vars)
#
# Pattern for bridging Hermes shell hooks (configured in ~/.hermes/config.yaml
# as shell commands) to Python handlers without bash variable interpolation
# breaking Python source. Use this template for ANY new hook that needs to
# pass user/output data to a Python handler.
#
# Why env vars > heredoc-with-interpolation:
#   1. Quotes in user output won't break heredoc parsing
#   2. Multi-line strings with special chars stay clean
#   3. Newlines don't corrupt the inline Python source
#
# Usage in config.yaml:
#   hooks:
#     on_session_end:
#       - command: "/path/to/this/wrapper.sh --event on_session_end --output $RESPONSE"
#         timeout: 15
#
# Usage standalone (test):
#   bash wrapper.sh --event agent:end --output "test message" --project myproject --task T-01.1
#
# Verify:
#   bash ~/.hermes/scripts/check-fable5-compliance.sh  # overall compliance
#   tail -5 /Volumes/Storage-1/Hermes/wiki/log.md      # log entry written
#   ls -la /Volumes/Storage-1/Hermes/wiki/projects/{project_id}/logs/  # per-project log

set -e

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# === Parse args ===
EVENT=""
OUTPUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --event) EVENT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# === Export for Python (no interpolation INSIDE heredoc) ===
export HOOK_EVENT="$EVENT"
export HOOK_OUTPUT="$OUTPUT"
export HOOK_DIR

# === Run Python handler via quoted heredoc ===
# 'PYEOF' (quoted) prevents bash from interpreting $vars INSIDE the Python block.
# Vars still flow via os.environ.
exec python3 << 'PYEOF'
import sys, os
sys.path.insert(0, os.environ.get('HOOK_DIR', '.'))
from handler import handle

context = {
    'message': os.environ.get('HOOK_OUTPUT', '')[:500],
    'response': os.environ.get('HOOK_OUTPUT', '')[:1000],
    'project_id': os.environ.get('HOOK_PROJECT', ''),
    'phase_id': os.environ.get('HOOK_PHASE', ''),
    'task_id': os.environ.get('HOOK_TASK', ''),
}

handle(os.environ.get('HOOK_EVENT', 'agent:end'), context)
PYEOF