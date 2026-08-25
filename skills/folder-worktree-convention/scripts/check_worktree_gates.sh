#!/bin/bash
# check_worktree_gates.sh — Verify worktree gates trước khi act
# Usage: ./check_worktree_gates.sh /path/to/folder [--strict]
#
# Exit codes:
#   0 — All gates pass (or --strict and asked user)
#   1 — Gate fail, STOP and ask user
#
# Examples:
#   ./check_worktree_gates.sh /Volumes/Storage-1/Pocket3/Hermes-Edit
#   ./check_worktree_gates.sh /Volumes/Storage-1/Workspace/MyProject --strict

set -e

FOLDER="$1"
STRICT="${2:-}"

if [ -z "$FOLDER" ]; then
  echo "Usage: $0 /path/to/folder [--strict]"
  echo ""
  echo "Verify folder worktree gates (tmp/ exists, no nested folders, etc.)"
  echo ""
  echo "Exit codes:"
  echo "  0 = All gates pass"
  echo "  1 = Gate fail, STOP and ask user"
  exit 2
fi

if [ ! -d "$FOLDER" ]; then
  echo "❌ Gate 0: Folder does not exist: $FOLDER"
  exit 1
fi

echo "=== Worktree Gate Check: $FOLDER ==="
echo ""

# Gate 1: tmp/ exists?
if [ -d "$FOLDER/tmp" ]; then
  echo "✅ Gate 1: $FOLDER/tmp/ exists"
else
  echo "❌ Gate 1: $FOLDER/tmp/ does NOT exist"
  if [ "$STRICT" = "--strict" ]; then
    echo "  → STOP. Ask user: 'mkdir -p $FOLDER/tmp/' ?"
    exit 1
  else
    echo "  → Auto-fix: mkdir -p $FOLDER/tmp/"
    mkdir -p "$FOLDER/tmp"
    echo "  → Created."
  fi
fi

# Gate 2: No nested folders in root (except tmp/, hidden, parent)
echo ""
echo "Gate 2: Check for nested folders in root (except tmp/)"
NESTED=$(ls -la "$FOLDER/" | awk '/^d/ && $NF != "." && $NF != ".." && $NF != "tmp" && $NF !~ /^\./ {print $NF}')
if [ -z "$NESTED" ]; then
  echo "✅ Gate 2: No nested folders in root (except tmp/)"
else
  echo "⚠️  Gate 2: Found nested folders:"
  echo "$NESTED" | sed 's/^/    /'
  echo ""
  echo "  → These may be legacy/candidates for tmp/legacy-{name}/"
  if [ "$STRICT" = "--strict" ]; then
    echo "  → STOP. Ask user about each."
    exit 1
  else
    echo "  → Continue but report to user"
  fi
fi

# Gate 3: No suspicious files in root (audio/wav/json/jpg/raw)
echo ""
echo "Gate 3: Check for non-final files in root"
SUSPICIOUS=$(ls -la "$FOLDER/" 2>/dev/null | grep -vE "\.mp4$|\.DS_Store|^d|\.\.$|^\.$|tmp$|^total" | awk '$NF ~ /\.(wav|json|txt|srt|jpg|jpeg|png|mov|log)$/ {print $NF}')
if [ -z "$SUSPICIOUS" ]; then
  echo "✅ Gate 3: No suspicious non-final files in root"
else
  echo "⚠️  Gate 3: Suspicious files (not .mp4) in root:"
  echo "$SUSPICIOUS" | sed 's/^/    /'
  echo ""
  echo "  → These should likely move to $FOLDER/tmp/"
  if [ "$STRICT" = "--strict" ]; then
    echo "  → STOP. Ask user about each."
    exit 1
  else
    echo "  → Continue but report to user"
  fi
fi

# Gate 4: tmp/ is not too bloated (sanity check)
echo ""
echo "Gate 4: Check tmp/ size (sanity)"
TMP_SIZE=$(du -sh "$FOLDER/tmp/" 2>/dev/null | cut -f1)
TMP_COUNT=$(find "$FOLDER/tmp/" -maxdepth 1 -mindepth 1 2>/dev/null | wc -l)
echo "  → $FOLDER/tmp/ size: $TMP_SIZE ($TMP_COUNT items)"
echo "  → (No threshold check — large tmp/ is OK if legacy files)"

# Gate 5: System /tmp cleanup check (only files WE created)
echo ""
echo "Gate 5: Check system /tmp for our task files"
# Heuristic: files matching patterns from edit-clip / research / etc.
TASK_TMP=$(ls /tmp/ 2>/dev/null | grep -E "^(audio|source|transcript|keep_plan|filter|whisper).*\.(wav|mp4|json|txt|srt)$" | head -10)
if [ -z "$TASK_TMP" ]; then
  echo "✅ Gate 5: No obvious task files in /tmp"
else
  echo "⚠️  Gate 5: Found task files in /tmp (should cleanup):"
  echo "$TASK_TMP" | sed 's/^/    /'
  if [ "$STRICT" = "--strict" ]; then
    echo "  → STOP. Run cleanup: rm -f /tmp/{files}?"
    exit 1
  else
    echo "  → Continue but cleanup before ending task"
  fi
fi

echo ""
echo "=== Summary ==="
if [ "$STRICT" = "--strict" ]; then
  echo "Mode: STRICT (any ⚠️ → exit 1)"
else
  echo "Mode: LENIENT (auto-create tmp/, report issues but continue)"
fi
echo ""
echo "Next: Apply gates to your task. If any ⚠️ above, ask user before acting."