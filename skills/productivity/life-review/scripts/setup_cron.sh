#!/usr/bin/env bash
# setup_cron.sh — Life Review cron installer (DRY-RUN BY DEFAULT).
#
# This script prints the planned `hermes cron create` invocations for the
# 4 life-review cadences:
#   daily brief        07:30 ICT
#   weekly review      Sunday 18:00 ICT
#   monthly summary    28th  09:00 ICT
#   quarterly review   Jan/Apr/Jul/Oct 09:00 ICT
#
# SAFEGUARD: by default the script DOES NOT execute any `hermes cron create`
# command. The user (Tuấn Anh) must review the dry-run output, then call
# `--apply` to actually create the cron jobs. This mirrors the EP P6 rule
# "don't fix any of it, just send me the list" — we report; we don't
# mutate the scheduler without explicit approval.
#
# Usage:
#   ./setup_cron.sh --dry-run          # show planned commands (default)
#   ./setup_cron.sh --apply            # actually create the cron jobs
#   ./setup_cron.sh --apply --promote  # after a trial period, set delivery=telegram
#   ./setup_cron.sh --list             # list existing life-review* cron jobs
#   ./setup_cron.sh --remove           # remove all life-review* cron jobs
#
# Timezone: Asia/Ho_Chi_Minh (ICT, UTC+7) — Tuấn Anh's local.

set -euo pipefail

MODE="dry-run"
PROMOTE=0
LIST=0
REMOVE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)   MODE="dry-run"; shift ;;
    --apply)     MODE="apply"; shift ;;
    --promote)   PROMOTE=1; shift ;;
    --list)      MODE="list"; LIST=1; shift ;;
    --remove)    MODE="remove"; REMOVE=1; shift ;;
    --help|-h)
      sed -n '2,28p' "$0"; exit 0 ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 2 ;;
  esac
done

# --- delivery resolution -------------------------------------------------
# Default: local (cron writes to wiki/_meta/life-review/ for review).
# After trial: --promote switches daily + weekly to Telegram 1132914873.
TELEGRAM_ID="1132914873"
DAILY_DELIVER="local"
WEEKLY_DELIVER="local"
MONTHLY_DELIVER="local"
QUARTERLY_DELIVER="local"

if [[ "$PROMOTE" == "1" ]]; then
  DAILY_DELIVER="telegram:${TELEGRAM_ID}"
  WEEKLY_DELIVER="telegram:${TELEGRAM_ID}"
  # monthly + quarterly STAY local — higher-stakes summaries need explicit user send.
fi

# --- emit plan -----------------------------------------------------------
emit_plan() {
  cat <<PLAN
============================================================
life-review cron plan (mode: $MODE)
timezone: Asia/Ho_Chi_Minh
============================================================

# 1. daily brief — 07:30 every day
hermes cron create \\
  --name "life-review-daily-brief" \\
  --schedule "0 7 * * *" \\
  --timezone "Asia/Ho_Chi_Minh" \\
  --prompt "/skill life-review cadence=daily" \\
  --deliver "${DAILY_DELIVER}" \\
  --notify_on_complete true

# 2. weekly review — Sunday 18:00
hermes cron create \\
  --name "life-review-weekly-review" \\
  --schedule "0 18 * * 0" \\
  --timezone "Asia/Ho_Chi_Minh" \\
  --prompt "/skill life-review cadence=weekly" \\
  --deliver "${WEEKLY_DELIVER}" \\
  --notify_on_complete true

# 3. monthly summary — 28th of each month 09:00
hermes cron create \\
  --name "life-review-monthly-summary" \\
  --schedule "0 9 28 * *" \\
  --timezone "Asia/Ho_Chi_Minh" \\
  --prompt "/skill life-review cadence=monthly deliver=local require_approval=true" \\
  --deliver "${MONTHLY_DELIVER}" \\
  --notify_on_complete true

# 4. quarterly review — Jan/Apr/Jul/Oct 09:00
hermes cron create \\
  --name "life-review-quarterly-review" \\
  --schedule "0 9 1 */3 *" \\
  --timezone "Asia/Ho_Chi_Minh" \\
  --prompt "/skill life-review cadence=quarterly deliver=local require_approval=true" \\
  --deliver "${QUARTERLY_DELIVER}" \\
  --notify_on_complete true
PLAN
}

case "$MODE" in
  dry-run)
    emit_plan
    echo ""
    echo "============================================================"
    echo "DRY RUN: no cron jobs created. Re-run with --apply to install."
    echo "============================================================"
    ;;

  apply)
    if [[ -z "${HERMES_CONFIRM_CREATE:-}" ]]; then
      echo "Safety gate: --apply requires HERMES_CONFIRM_CREATE=1 in env." >&2
      echo "Set HERMES_CONFIRM_CREATE=1 only after reviewing the dry-run output." >&2
      exit 3
    fi
    if ! command -v hermes >/dev/null 2>&1; then
      echo "ERROR: hermes CLI not on PATH. Activate the Hermes venv first." >&2
      exit 4
    fi
    emit_plan
    echo ""
    echo "HERMES_CONFIRM_CREATE=1 set — proceeding to call 'hermes cron create'."
    set -x
    hermes cron create "0 7 * * *" "/skill life-review cadence=daily" \
      --name "life-review-daily-brief" \
      --deliver "$DAILY_DELIVER"

    hermes cron create "0 18 * * 0" "/skill life-review cadence=weekly" \
      --name "life-review-weekly-review" \
      --deliver "$WEEKLY_DELIVER"

    hermes cron create "0 9 28 * *" "/skill life-review cadence=monthly deliver=local require_approval=true" \
      --name "life-review-monthly-summary" \
      --deliver "$MONTHLY_DELIVER"

    hermes cron create "0 9 1 */3 *" "/skill life-review cadence=quarterly deliver=local require_approval=true" \
      --name "life-review-quarterly-review" \
      --deliver "$QUARTERLY_DELIVER"
    { set +x; } 2>/dev/null || true
    echo ""
    echo "Cron jobs installed. Verify with: $0 --list"
    ;;

  list)
    if ! command -v hermes >/dev/null 2>&1; then
      echo "ERROR: hermes CLI not on PATH." >&2
      exit 4
    fi
    hermes cron list | grep -E "life-review" || echo "(no life-review cron jobs found)"
    ;;

  remove)
    if [[ -z "${HERMES_CONFIRM_CREATE:-}" ]]; then
      echo "Safety gate: --remove requires HERMES_CONFIRM_CREATE=1 in env." >&2
      exit 3
    fi
    if ! command -v hermes >/dev/null 2>&1; then
      echo "ERROR: hermes CLI not on PATH." >&2
      exit 4
    fi
    for name in life-review-daily-brief life-review-weekly-review life-review-monthly-summary life-review-quarterly-review; do
      ids=$(hermes cron list 2>/dev/null | awk -v n="$name" '$0 ~ n {print $1}') || true
      for id in $ids; do
        echo "Removing $id ($name)"
        hermes cron delete "$id" || true
      done
    done
    ;;
esac
