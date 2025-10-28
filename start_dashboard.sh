#!/bin/bash
# 🎮 RBOTzilla TMUX Dashboard - Manual/Headless Control + Real-Time AI Decision Display
# Three-pane layout: Large left (narration/log), Top-right (AI decisions), Bottom-right (command input)
# PIN: 841921

WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
SESSION_NAME="rbotzilla-dashboard"
WINDOW_NAME="Dashboard"

# Kill existing session if exists
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true

# Wait a moment for session to fully terminate
sleep 0.5

# ═══════════════════════════════════════════════════════════════════════════════
# LAYOUT: 2x2 Grid configuration
# ┌─────────────────────────────────────────┬──────────────────────────┐
# │                                         │  AI Decisions (Top-R)    │
# │         Narration & Log                 │  Block B                 │
# │         (Large Left 70%)                │  Real-time filtering     │
# │         Block A (spans 2 rows)          ├──────────────────────────┤
# │                                         │  Command Input (Bot-R)   │
# │                                         │  Block C                 │
# │                                         │  Interactive terminal    │
# └─────────────────────────────────────────┴──────────────────────────┘
# ═══════════════════════════════════════════════════════════════════════════════

# Create new session with main window (Pane 0 = Block A - bottom original stack)
tmux new-session -d -s "$SESSION_NAME" -n "$WINDOW_NAME"
sleep 0.5

# Pane 0: Block A (Left side - spans full height, 70% width) - NARRATION & LOG
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.0" "cd '$WORK_DIR'" Enter
sleep 0.2

# Split horizontally to create right column (30% width)
# This creates pane 1 (Block B - top-right) from middle original stack
tmux split-window -t "$SESSION_NAME:$WINDOW_NAME.0" -h -p 30
sleep 0.3

# Split pane 1 vertically to create bottom-right pane
# This creates pane 2 (Block C - bottom-right) from top original stack
tmux split-window -t "$SESSION_NAME:$WINDOW_NAME.1" -v -p 50
sleep 0.3

# Now start the programs in each pane
# Pane 0 (Block A - left side): Narration & Log (bottom of original stack)
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.0" "clear" Enter
sleep 0.2
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.0" "python3 dashboard_live_monitor.py" Enter
sleep 0.2

# Pane 1 (Block B - top-right): Strategy Status (plain English, agents verbose)
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.1" "cd '$WORK_DIR'" Enter
sleep 0.2
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.1" "clear" Enter
sleep 0.2
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.1" "python3 tools/strategy_status.py --watch --verbose" Enter
sleep 0.2

# Pane 2 (Block C - bottom-right): Command Terminal (top of original stack)
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.2" "cd '$WORK_DIR'" Enter
sleep 0.2
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.2" "clear" Enter
sleep 0.2
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME.2" "bash interactive_command_terminal.sh" Enter

# Select left pane as active (Block A - pane 0)
tmux select-pane -t "$SESSION_NAME:$WINDOW_NAME.0"

echo "✅ Dashboard created with 2x2 grid layout"
echo "📍 Block A (Pane 0): Narration & Log (Left 70%, full height)"
echo "📍 Block B (Pane 1): Strategy Status (Top-Right 30%, agents: verbose)"
echo "📍 Block C (Pane 2): Command Input (Bottom-Right 30%)"
echo "📍 Attach with: tmux attach -t $SESSION_NAME"
echo ""

# Attach to session
tmux attach-session -t "$SESSION_NAME"
