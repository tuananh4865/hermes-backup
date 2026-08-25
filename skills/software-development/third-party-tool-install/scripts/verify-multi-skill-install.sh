#!/usr/bin/env bash
# verify-multi-skill-install.sh
# Audits the state of a multi-skill install (3-hop symlink chain):
#   ~/.hermes/skills/<name>  →  ~/.claude/skills/<name>  →  /Volumes/Storage-1/Hermes/skills/<namespace>-vX.Y.Z/<name>
#
# Usage:
#   verify-multi-skill-install.sh <namespace>-vX.Y.Z <skill-name> [<skill-name> ...]
#   verify-multi-skill-install.sh heygen-hyperframes-v0.7.83 hyperframes hyperframes-cli media-use
#
# Exit code:
#   0 — all OK
#   1 — one or more FAIL
#   2 — pre-flight failed (storage unmounted, namespace dir missing, etc.)
#
# Verified for heygen-hyperframes-v0.7.83 (2026-07-30).

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <namespace>-vX.Y.Z <skill-name> [<skill-name> ...]" >&2
  echo "Example: $0 heygen-hyperframes-v0.7.83 hyperframes media-use" >&2
  exit 64
fi

NAMESPACE_DIR="$1"
shift
SKILL_NAMES=("$@")

STORAGE_DIR="/Volumes/Storage-1/Hermes/skills/${NAMESPACE_DIR}"
HERMES_DIR="$HOME/.hermes/skills"
CLAUDE_DIR="$HOME/.claude/skills"

fail_count=0
preflight_failed=0

echo "=================================================================="
echo "Multi-Skill Install Audit"
echo "Namespace dir: ${STORAGE_DIR}"
echo "Skills checked: ${#SKILL_NAMES[@]}"
echo "=================================================================="
echo

# --- Pre-flight: storage mount + dir exists ---
echo "[1/4] Pre-flight checks"
if ! mount | grep -q '/Volumes/Storage-1 '; then
  echo "  FAIL  /Volumes/Storage-1 NOT mounted"
  preflight_failed=1
else
  echo "  OK    /Volumes/Storage-1 mounted"
fi

if [ ! -d "$STORAGE_DIR" ]; then
  echo "  FAIL  Storage dir missing: $STORAGE_DIR"
  preflight_failed=1
else
  echo "  OK    Storage dir exists: $STORAGE_DIR"
fi

if [ "$preflight_failed" -ne 0 ]; then
  echo
  echo "PRE-FLIGHT FAILED — aborting (HARD STOP rule)"
  exit 2
fi
echo

# --- Per-skill audit ---
echo "[2/4] Per-skill symlink chain audit"
for skill in "${SKILL_NAMES[@]}"; do
  hermes_path="$HERMES_DIR/$skill"
  claude_path="$CLAUDE_DIR/$skill"
  storage_path="$STORAGE_DIR/$skill"

  # Check hermes hop
  if [ ! -L "$hermes_path" ]; then
    if [ -d "$hermes_path" ]; then
      echo "  FAIL  $skill: ~/.hermes/skills/$skill is REAL DIR (should be symlink)"
    else
      echo "  FAIL  $skill: ~/.hermes/skills/$skill MISSING"
    fi
    fail_count=$((fail_count + 1))
    continue
  fi

  # Check claude hop
  if [ ! -L "$claude_path" ]; then
    if [ -d "$claude_path" ]; then
      echo "  FAIL  $skill: ~/.claude/skills/$skill is REAL DIR (should be symlink)"
    else
      echo "  FAIL  $skill: ~/.claude/skills/$skill MISSING"
    fi
    fail_count=$((fail_count + 1))
    continue
  fi

  # Resolve final target
  final=$(readlink -f "$hermes_path")
  case "$final" in
    "$STORAGE_DIR"/*)
      echo "  OK    $skill → $final"
      ;;
    *)
      echo "  FAIL  $skill → $final (does NOT resolve under $STORAGE_DIR)"
      fail_count=$((fail_count + 1))
      ;;
  esac
done
echo

# --- Content integrity check ---
echo "[3/4] Content integrity (storage vs source)"
# Find a corresponding source repo if available
# Convention: /Volumes/Storage-1/Hermes/research/<namespace-without-version>/
namespace_base="${NAMESPACE_DIR%-v*}"
source_repo="/Volumes/Storage-1/Hermes/research/${namespace_base}"
if [ -d "$source_repo/skills" ]; then
  for skill in "${SKILL_NAMES[@]}"; do
    src_skill_md="$source_repo/skills/$skill/SKILL.md"
    storage_skill_md="$STORAGE_DIR/$skill/SKILL.md"
    if [ ! -f "$src_skill_md" ]; then
      echo "  SKIP  $skill: source SKILL.md missing"
      continue
    fi
    if diff -q "$src_skill_md" "$storage_skill_md" >/dev/null 2>&1; then
      echo "  OK    $skill: SKILL.md matches source"
    else
      echo "  WARN  $skill: SKILL.md differs from source"
    fi
  done
else
  echo "  SKIP  source repo not found at $source_repo (no comparison possible)"
fi
echo

# --- User-override protection check ---
echo "[4/4] User-override protection (creative/* must remain real dirs)"
override_count=0
while IFS= read -r f; do
  override_count=$((override_count + 1))
  printf "  OK    protected: %s\n" "$f"
done < <(find "$HERMES_DIR" -maxdepth 4 -name 'SKILL.md' -type f 2>/dev/null | \
        while IFS= read -r f; do
          d=$(dirname "$f")
          if [ ! -L "$d" ]; then
            # Only flag if it WOULD collide with a canonical name
            base=$(basename "$d")
            for canon in "${SKILL_NAMES[@]}"; do
              if [ "$base" = "$canon" ]; then
                echo "$d"
                break
              fi
            done
          fi
        done)

if [ "$override_count" -eq 0 ]; then
  echo "  OK    no name-colliding overrides found"
fi
echo

# --- Summary ---
echo "=================================================================="
echo "Summary"
echo "  Skills checked:   ${#SKILL_NAMES[@]}"
echo "  Failures:         $fail_count"
echo "  Exit code:        $([ $fail_count -eq 0 ] && echo 0 || echo 1)"
echo "=================================================================="

[ "$fail_count" -eq 0 ]