#!/usr/bin/env bash
# Open a tmux session with side-by-side panes:
# - Left: Pretty narration stream
# - Right: ML filter narration (TRADE_BLOCKED / HEDGE_ON/OFF / PACK_ROUTED)

set -euo pipefail

SESSION_NAME="rbotzilla-side-ml"
WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"

if ! command -v tmux >/dev/null 2>&1; then
  echo "❌ tmux is not installed. Please install tmux and retry."
  exit 1
fi

# If session exists, just attach
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  tmux attach -t "$SESSION_NAME"
  exit 0
fi

# Create session with one window
tmux new-session -d -s "$SESSION_NAME" -x 200 -y 50 -c "$WORK_DIR" -n "narration+ml"

# Left pane: pretty narration
tmux send-keys -t "$SESSION_NAME":0.0 "cd $WORK_DIR && echo '🎙️ Pretty Narration (left)' && python3 tools/pretty_narration.py --tail 20" Enter

# Split horizontally (right pane): ML filter stream
tmux split-window -h -t "$SESSION_NAME":0 -c "$WORK_DIR"
tmux send-keys -t "$SESSION_NAME":0.1 "cd $WORK_DIR && echo '🧠 ML Filtered Narration (right)' && bash scripts/stream_ml_filter.sh" Enter

# Focus left pane by default
tmux select-pane -t "$SESSION_NAME":0.0
tmux attach -t "$SESSION_NAME"
