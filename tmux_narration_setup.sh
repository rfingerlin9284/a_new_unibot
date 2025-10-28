#!/bin/bash
# 📺 RBOTzilla Narration & Live Activity Tmux Setup
# Ctrl+Shift+N opens tmux with narration and live activity panes

set -e

SESSION_NAME="rbotzilla-narration"
WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"

# Kill existing session if it exists (optional, remove if you want to reuse)
# tmux kill-session -t $SESSION_NAME 2>/dev/null || true

# Check if session already exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ Tmux session '$SESSION_NAME' already running"
    tmux attach-session -t $SESSION_NAME
    exit 0
fi

# Create new session with 2 windows
tmux new-session -d -s $SESSION_NAME -x 200 -y 50

# Window 0: Rick Narration Stream
tmux rename-window -t $SESSION_NAME:0 "📜 Rick Narration"
tmux send-keys -t $SESSION_NAME:0 "cd $WORK_DIR && echo '🎙️ Rick Narration Stream - Live Commentary' && python3 tools/pretty_narration.py --tail 20" Enter

# Window 1: Live Market Activity
tmux new-window -t $SESSION_NAME:1 -n "📊 Market Activity"
tmux send-keys -t $SESSION_NAME:1 "cd $WORK_DIR && echo '📊 Live Market Activity - Order & Position Monitoring' && while true; do python3 -c \"import json; open('connection_state.json').read()\" 2>/dev/null && sleep 5 || { echo '⏳ Waiting for market data...'; sleep 2; }; done" Enter

# Window 2: Engine Status Monitor
tmux new-window -t $SESSION_NAME:2 -n "⚙️ Engine Status"
tmux send-keys -t $SESSION_NAME:2 "cd $WORK_DIR && echo '⚙️ Engine Diagnostics & System Status' && python3 canary_oanda_connector.py" Enter

# Window 3: Trading Log (Real-time)
tmux new-window -t $SESSION_NAME:3 -n "🤖 Trading Log"
tmux send-keys -t $SESSION_NAME:3 "cd $WORK_DIR && tail -f *.log 2>/dev/null || echo 'Waiting for trading logs...' && sleep 30" Enter

# Select first window and attach
tmux select-window -t $SESSION_NAME:0
tmux attach-session -t $SESSION_NAME
