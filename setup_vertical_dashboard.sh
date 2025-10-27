#!/usr/bin/env bash
# 3 Vertical Panes Dashboard with Color-Coded, Clean Messages
# Older text scrolls up; clean separators between sections

set -euo pipefail

ROOT="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
CONF_DIR="$ROOT/tmux_config"
TOOLS_DIR="$ROOT/tools"
SESSION="rbotzilla-dashboard"
WINDOW="Dashboard"

mkdir -p "$CONF_DIR" "$TOOLS_DIR"

# ============================================================================
# 1) TMUX Configuration - History, Mouse, Borders
# ============================================================================
cat > "$CONF_DIR/tmux.vertical.conf" <<'EOF'
# Massive history for scrollback
set -g history-limit 100000

# Mouse scrolling enabled
set -g mouse on
setw -g mode-keys vi

# Pane numbering and titles
set -g pane-base-index 1
setw -g automatic-rename off
set -g allow-rename off

# Border colors: bright active, subtle inactive
set -g pane-border-style fg=colour238
set -g pane-active-border-style fg=colour39,bold

# Show pane title on border
setw -g pane-border-status top
setw -g pane-border-format ' #[bg=colour238,fg=white,bold] #{pane_title} #[default] '

# Status bar at top
set -g status on
set -g status-position top
set -g status-justify centre
set -g status-style bg=colour234,fg=colour244
set -g status-left '#[bold,fg=colour39]🤖 RBOTzilla Live #[default]'
set -g status-right '#[fg=colour244]#{session_name} | %Y-%m-%d %H:%M:%S '

# Copy mode styling
set -g message-style bg=colour22,fg=white

# Smooth wheel scrolling
bind -T copy-mode-vi WheelUpPane send -X scroll-up
bind -T copy-mode-vi WheelDownPane send -X scroll-down
EOF

chmod 444 "$CONF_DIR/tmux.vertical.conf"

# ============================================================================
# 2) Pretty Logger - Color-Coded Message Blocks
# ============================================================================
cat > "$TOOLS_DIR/prettylog.sh" <<'EOFLOG'
#!/usr/bin/env bash
# Usage: pecho CHANNEL "Header text" "- Bullet 1" "- Bullet 2"
# Creates clean, color-coded blocks with separators

_pecho_color() {
  case "${1^^}" in
    TRADE)     echo 39  ;; # Bright blue
    SIGNAL)    echo 214 ;; # Orange
    GATE)      echo 203 ;; # Pink/red
    PROTECTION) echo 135 ;; # Purple
    PROFIT)    echo 82  ;; # Green
    LOSS)      echo 196 ;; # Red
    SYSTEM)    echo 244 ;; # Gray
    INFO)      echo 45  ;; # Cyan
    WARN)      echo 226 ;; # Yellow
    ERROR)     echo 196 ;; # Red
    *)         echo 81  ;; # Bright cyan default
  esac
}

pecho() {
  local channel="${1:-INFO}"; shift || true
  local color=$(_pecho_color "$channel")
  local reset="\033[0m"
  local fg="\033[38;5;${color}m"
  local bold="\033[1m"
  
  # Top border
  printf "${fg}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${reset}\n"
  printf "${fg}┃${reset} ${bold}${fg}%-15s${reset} ${fg}│${reset} %s\n" "${channel^^}" "$(date '+%H:%M:%S')"
  printf "${fg}┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩${reset}\n"
  
  # Message lines with clean spacing
  for line in "$@"; do
    if [[ "$line" =~ ^[[:space:]]*[-•] ]]; then
      # Bullet point
      printf "  ${fg}•${reset} %s\n" "${line#*[-• ]}"
    else
      # Regular text with indent
      printf "    %s\n" "$line"
    fi
  done
  
  # Bottom border + blank separator
  printf "${fg}└────────────────────────────────────────────────────────────────┘${reset}\n"
  printf "\n"  # Blank line between blocks
}

export -f pecho
EOFLOG

chmod 755 "$TOOLS_DIR/prettylog.sh"

# ============================================================================
# 3) Create/Reset Session with 3 Vertical Panes
# ============================================================================

# Start tmux server and load config
tmux start-server 2>/dev/null || true
tmux source-file "$CONF_DIR/tmux.vertical.conf" 2>/dev/null || true

# Kill existing session to start fresh
tmux kill-session -t "$SESSION" 2>/dev/null || true
sleep 0.5

# Create new session with first pane
tmux new-session -d -s "$SESSION" -n "$WINDOW"

# Split into 3 vertical panes (equal width)
tmux split-window -h -t "$SESSION:$WINDOW"
tmux split-window -h -t "$SESSION:$WINDOW"

# Make them equal width
tmux select-layout -t "$SESSION:$WINDOW" even-horizontal

# Set pane titles
PANES=($(tmux list-panes -t "$SESSION:$WINDOW" -F '#{pane_id}'))
tmux select-pane -t "${PANES[0]}" -T "📜 Live Narration & Events"
tmux select-pane -t "${PANES[1]}" -T "📊 Active Positions & Decisions"
tmux select-pane -t "${PANES[2]}" -T "⚙️  System Status & Config"

# ============================================================================
# 4) Initialize Each Pane with Pretty Logger
# ============================================================================

INIT_CMD="cd $ROOT && source $TOOLS_DIR/prettylog.sh && clear"

# Pane 0 (Left): Live Narration Monitor
tmux send-keys -t "${PANES[0]}" "$INIT_CMD" Enter
sleep 0.3
tmux send-keys -t "${PANES[0]}" "python3 dashboard_live_monitor.py" Enter

# Pane 1 (Middle): AI Decision Monitor
tmux send-keys -t "${PANES[1]}" "$INIT_CMD" Enter
sleep 0.3
tmux send-keys -t "${PANES[1]}" "python3 ai_decision_monitor.py" Enter

# Pane 2 (Right): Interactive Command Terminal
tmux send-keys -t "${PANES[2]}" "$INIT_CMD" Enter
sleep 0.3
tmux send-keys -t "${PANES[2]}" "bash interactive_command_terminal.sh" Enter

# Select first pane as active
tmux select-pane -t "${PANES[0]}"

echo ""
echo "✅ Vertical 3-pane dashboard created!"
echo "📍 Pane 0 (Left): Live Narration"
echo "📍 Pane 1 (Middle): AI Decisions"
echo "📍 Pane 2 (Right): System Status"
echo ""
echo "🎨 Features:"
echo "  • Color-coded message blocks"
echo "  • Clean separators between sections"
echo "  • Scrollback: 100,000 lines (mouse wheel enabled)"
echo "  • Older text scrolls up automatically"
echo ""
echo "📌 Attach with: tmux attach -t $SESSION"
echo ""
echo "💡 Use in scripts:"
echo "   source $TOOLS_DIR/prettylog.sh"
echo "   pecho TRADE 'EUR_USD opened' '- Size: 15k' '- SL: 18 pips'"
echo ""

# Auto-attach if not already in tmux
if [ -z "${TMUX:-}" ]; then
  exec tmux attach -t "$SESSION"
else
  tmux switch-client -t "$SESSION"
fi
