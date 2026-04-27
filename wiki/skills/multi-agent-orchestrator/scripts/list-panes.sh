#!/bin/bash
# List all panes in current tmux session with details
# Shows pane index, current command, working directory

echo "=== Tmux Panes ==="
echo ""

# Get session name
SESSION=$(tmux display-message -p '#{session_name}')
CURRENT_PANE=$(tmux display-message -p '#{pane_index}')

echo "Session: $SESSION"
echo "Current pane: $CURRENT_pane"
echo ""

tmux list-panes -a -F "#{session_name}|#{window_index}|#{pane_index}|#{pane_current_command}|#{pane_current_path}" 2>/dev/null | while IFS='|' read -r sess win pane cmd path; do
    MARK=""
    if [ "$pane" = "$CURRENT_PANE" ]; then
        MARK=" (current)"
    fi
    echo "Pane $pane$MARK"
    echo "  Window: $win | Command: $cmd"
    echo "  Path: $path"
    echo "---"
done

echo ""
echo "Total panes: $(tmux list-panes -a 2>/dev/null | wc -l | tr -d ' ')"
