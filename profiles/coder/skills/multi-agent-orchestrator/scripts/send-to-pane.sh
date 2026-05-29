#!/bin/bash
# Send text to a specific pane
# Usage: send-to-pane.sh <pane-index> "<text>"

PANE="$1"
TEXT="$2"

if [ -z "$PANE" ] || [ -z "$TEXT" ]; then
    echo "Usage: send-to-pane.sh <pane-index> <text>"
    exit 1
fi

tmux send-keys -t "$PANE" "$TEXT" Enter
echo "Sent to pane $PANE: $TEXT"
