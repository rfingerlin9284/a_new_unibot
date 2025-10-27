#!/bin/bash
set -euo pipefail
WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
SESSION_NAME="rbotzilla-dashboard"
WINDOW_NAME="Dashboard"
TARGET_PANE="$SESSION_NAME:$WINDOW_NAME.1"
CMD="cd '$WORK_DIR' && python3 tools/strategy_status.py --watch --verbose"
if tmux respawn-pane -k -t "$TARGET_PANE" "$CMD" 2>/dev/null; then
  exit 0
else
  tmux send-keys -t "$TARGET_PANE" C-c "$CMD" Enter
fi
