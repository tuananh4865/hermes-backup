#!/bin/bash
# Transcript Saver v2.0 wrapper for Hermes shell hooks
# Receives env vars from Hermes: $RESPONSE, $MESSAGE, $SESSION_ID, $PLATFORM, $USER_ID
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
HERMES_PROFILE="${HERMES_PROFILE:-default}"
export HERMES_HOME
export HERMES_PROFILE

# Pass through args + env vars
exec python3 "$HERMES_HOME/hooks/transcript-saver-v2/handler.py" "$@"
