#!/usr/bin/env bash
# Template: bash wrapper for third-party CLI
# Usage: copy, customize case branches, drop in ~/tools/bin/<wrapper-name>
#
# This template handles:
# - Subcommand detection via $1
# - Default-value flag injection (whisper, model, language, base URL, etc.)
# - Deduplication (don't override flags user explicitly passed)
# - Delegation to Python loader for env staging

set -e

# === Configuration ===
REAL_BIN="/opt/homebrew/bin/<tool-name>"   # Path to actual binary (after `which`)
LOADER=""                                   # Optional: path to python loader (if env staging needed)

# === Subcommand handlers ===
case "${1:-}" in
  <subcommand-needs-external-binary>)
    # Inject --binary-path + --model + --language (or whatever flags the tool supports)
    injected=()
    has_binary=0; has_model=0; has_lang=0

    # Loop through remaining args to check for duplicates
    for arg in "${@:2}"; do
      case "$arg" in
        --binary-path) has_binary=1 ;;
        --model) has_model=1 ;;
        --language) has_lang=1 ;;
      esac
    done

    # Only inject if user didn't pass the flag
    [ $has_binary -eq 0 ] && injected+=(--binary-path "/path/to/default/binary")
    [ $has_model -eq 0 ] && injected+=(--model "default-model-name")
    [ $has_lang -eq 0 ] && injected+=(--language vi)

    exec "$REAL_BIN" "$@" "${injected[@]}"
    ;;

  <subcommand-needs-api-key>)
    # Delegate to Python loader for env staging (filter-safe)
    # Loader reads ~/.hermes/.env at runtime, sets ANTHROPIC_API_KEY + ANTHROPIC_BASE_URL, execs real binary
    if [ -z "$LOADER" ]; then
      echo "ERROR: LOADER not configured for this wrapper" >&2
      exit 1
    fi

    # Inject --model if tool supports it (claude-haiku default may not exist on alternate providers)
    has_model=0
    for arg in "${@:2}"; do
      case "$arg" in --model) has_model=1 ;; esac
    done

    extra_args=()
    [ $has_model -eq 0 ] && extra_args+=(--model "MiniMax-M3")   # or whatever default

    exec "$LOADER" "$@" "${extra_args[@]}"
    ;;

  *)
    # Pass-through: all other subcommands work without wrapping
    exec "$REAL_BIN" "$@"
    ;;
esac
