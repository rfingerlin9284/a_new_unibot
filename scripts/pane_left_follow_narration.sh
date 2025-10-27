#!/bin/bash
set -euo pipefail
WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
SESSION_NAME="rbotzilla-dashboard"
WINDOW_NAME="Dashboard"
TARGET_PANE="$SESSION_NAME:$WINDOW_NAME.0"
CMD="cd '$WORK_DIR' && python3 tools/pretty_narration.py --tail 20"
# Try respawn, fall back to send-keys if respawn not supported
if tmux respawn-pane -k -t "$TARGET_PANE" "$CMD" 2>/dev/null; then
  exit 0
else
  tmux send-keys -t "$TARGET_PANE" C-c "$CMD" Enter
fi
