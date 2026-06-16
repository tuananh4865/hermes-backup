#!/bin/bash
# Hook wrapper for Loop Engineering
# Receives env vars from Hermes: $RESPONSE, $MESSAGE, $SESSION_ID, $PLATFORM, $USER_ID
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
HERMES_PROFILE="${HERMES_PROFILE:-default}"
export HERMES_HOME
export HERMES_PROFILE

exec python3 "$HERMES_HOME/loop-engineering/hook.py" "$@"
