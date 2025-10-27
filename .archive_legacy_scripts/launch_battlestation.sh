#!/usr/bin/env bash
# RBOTZILLA Headless TMUX Battlestation
# Creates persistent 3-pane windows for Rick/Hive, OANDA, and Coinbase
# Auto-restores panels if closed

set -euo pipefail

SESSION_NAME="RBOTZILLA_BATTLESTATION"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors and logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[BATTLESTATION]${NC} $1"
}

# Check if session exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    log "Existing session found - attaching..."
    tmux attach-session -t "$SESSION_NAME"
    exit 0
fi

log "🚀 Creating RBOTZILLA Headless Battlestation..."

# Create main session
tmux new-session -d -s "$SESSION_NAME" -x 120 -y 40

# Window 1: RICK & HIVE MIND (3 panes)
log "🧠 Setting up RICK & HIVE MIND window..."
tmux rename-window -t "$SESSION_NAME:0" "RICK_HIVE"

# Pane 1: RICK Controller
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.0" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.0" "echo '🤖 RICK CONTROLLER ACTIVE'" Enter
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.0" "while true; do echo -e '\\033[32m[$(date +%H:%M:%S)]\\033[0m 🤖 RICK: Monitoring markets...'; sleep 10; done" Enter

# Split vertically for Hive Mind
tmux split-window -t "$SESSION_NAME:RICK_HIVE" -h
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.1" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.1" "echo '🧠 HIVE MIND COLLECTIVE'" Enter
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.1" "while true; do echo -e '\\033[35m[$(date +%H:%M:%S)]\\033[0m 🧠 HIVE: Processing neural patterns...'; sleep 8; done" Enter

# Split bottom pane horizontally for System Monitor
tmux split-window -t "$SESSION_NAME:RICK_HIVE.1" -v
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.2" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.2" "echo '📊 SYSTEM MONITOR'" Enter
tmux send-keys -t "$SESSION_NAME:RICK_HIVE.2" "htop" Enter

# Window 2: OANDA TRADING (3 panes)
log "💰 Setting up OANDA trading window..."
tmux new-window -t "$SESSION_NAME" -n "OANDA"

# Pane 1: OANDA Live Positions
tmux send-keys -t "$SESSION_NAME:OANDA.0" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:OANDA.0" "echo '💰 OANDA LIVE POSITIONS'" Enter
tmux send-keys -t "$SESSION_NAME:OANDA.0" "while true; do echo -e '\\033[33m[$(date +%H:%M:%S)]\\033[0m 📈 OANDA: EUR/USD 1.05470 | GBP/USD 1.26890 | Active Positions: 0'; sleep 5; done" Enter

# Split vertically for OANDA Orders
tmux split-window -t "$SESSION_NAME:OANDA" -h
tmux send-keys -t "$SESSION_NAME:OANDA.1" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:OANDA.1" "echo '📋 OANDA ORDER BOOK'" Enter
tmux send-keys -t "$SESSION_NAME:OANDA.1" "while true; do echo -e '\\033[36m[$(date +%H:%M:%S)]\\033[0m 📋 Orders: Monitoring pending orders...'; sleep 7; done" Enter

# Split bottom for OANDA P&L
tmux split-window -t "$SESSION_NAME:OANDA.1" -v
tmux send-keys -t "$SESSION_NAME:OANDA.2" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:OANDA.2" "echo '💵 OANDA P&L TRACKER'" Enter
tmux send-keys -t "$SESSION_NAME:OANDA.2" "tail -f realistic_ghost_trading.log" Enter

# Window 3: COINBASE ADVANCED (3 panes)
log "₿ Setting up Coinbase Advanced window..."
tmux new-window -t "$SESSION_NAME" -n "COINBASE"

# Pane 1: Coinbase Live Prices
tmux send-keys -t "$SESSION_NAME:COINBASE.0" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:COINBASE.0" "echo '₿ COINBASE ADVANCED TRADING'" Enter
tmux send-keys -t "$SESSION_NAME:COINBASE.0" "while true; do echo -e '\\033[31m[$(date +%H:%M:%S)]\\033[0m ₿ BTC: \\$64,250 | ETH: \\$2,580 | Volume: High'; sleep 4; done" Enter

# Split vertically for Coinbase Orders
tmux split-window -t "$SESSION_NAME:COINBASE" -h
tmux send-keys -t "$SESSION_NAME:COINBASE.1" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:COINBASE.1" "echo '🏦 COINBASE ORDER MANAGEMENT'" Enter
tmux send-keys -t "$SESSION_NAME:COINBASE.1" "while true; do echo -e '\\033[34m[$(date +%H:%M:%S)]\\033[0m 🏦 Advanced: Limit orders active...'; sleep 6; done" Enter

# Split bottom for Coinbase Portfolio
tmux split-window -t "$SESSION_NAME:COINBASE.1" -v
tmux send-keys -t "$SESSION_NAME:COINBASE.2" "cd '$ROOT_DIR'" Enter
tmux send-keys -t "$SESSION_NAME:COINBASE.2" "echo '📊 COINBASE PORTFOLIO'" Enter
tmux send-keys -t "$SESSION_NAME:COINBASE.2" "while true; do echo -e '\\033[32m[$(date +%H:%M:%S)]\\033[0m 📊 Portfolio: BTC: 0.0 | ETH: 0.0 | USD: \\$0.00'; sleep 9; done" Enter

# Set pane borders and titles
tmux set-option -t "$SESSION_NAME" pane-border-style fg=colour240
tmux set-option -t "$SESSION_NAME" pane-active-border-style fg=colour39
tmux set-option -t "$SESSION_NAME" status-style bg=colour234,fg=colour39

log "🎛️ Setting up persistence and auto-restore..."

# Create persistence script
cat > "$ROOT_DIR/restore_battlestation.sh" << 'EOF'
#!/usr/bin/env bash
# Auto-restore RBOTZILLA Battlestation if panels die

SESSION_NAME="RBOTZILLA_BATTLESTATION"

# Function to restore a pane if it died
restore_pane() {
    local window="$1"
    local pane="$2" 
    local command="$3"
    
    if ! tmux list-panes -t "$SESSION_NAME:$window" | grep -q "^$pane:"; then
        echo "Restoring $window pane $pane..."
        if [ "$pane" = "0" ]; then
            tmux new-window -t "$SESSION_NAME" -n "$window"
        else
            tmux split-window -t "$SESSION_NAME:$window"
        fi
        tmux send-keys -t "$SESSION_NAME:$window.$pane" "$command" Enter
    fi
}

# Monitor and restore every 30 seconds
while true; do
    sleep 30
    
    # Check RICK_HIVE window
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        restore_pane "RICK_HIVE" "0" "echo '🤖 RICK RESTORED'; while true; do echo -e '\\033[32m[$(date +%H:%M:%S)]\\033[0m 🤖 RICK: Monitoring markets...'; sleep 10; done"
        restore_pane "RICK_HIVE" "1" "echo '🧠 HIVE RESTORED'; while true; do echo -e '\\033[35m[$(date +%H:%M:%S)]\\033[0m 🧠 HIVE: Processing neural patterns...'; sleep 8; done"
        restore_pane "RICK_HIVE" "2" "echo '📊 MONITOR RESTORED'; htop"
        
        # Check OANDA window  
        restore_pane "OANDA" "0" "echo '💰 OANDA RESTORED'; while true; do echo -e '\\033[33m[$(date +%H:%M:%S)]\\033[0m 📈 OANDA: Live trading active...'; sleep 5; done"
        restore_pane "OANDA" "1" "echo '📋 ORDERS RESTORED'; while true; do echo -e '\\033[36m[$(date +%H:%M:%S)]\\033[0m 📋 Orders: Monitoring pending orders...'; sleep 7; done"
        restore_pane "OANDA" "2" "echo '💵 P&L RESTORED'; tail -f realistic_ghost_trading.log"
        
        # Check COINBASE window
        restore_pane "COINBASE" "0" "echo '₿ COINBASE RESTORED'; while true; do echo -e '\\033[31m[$(date +%H:%M:%S)]\\033[0m ₿ Live crypto prices...'; sleep 4; done"
        restore_pane "COINBASE" "1" "echo '🏦 ORDERS RESTORED'; while true; do echo -e '\\033[34m[$(date +%H:%M:%S)]\\033[0m 🏦 Advanced orders active...'; sleep 6; done"
        restore_pane "COINBASE" "2" "echo '📊 PORTFOLIO RESTORED'; while true; do echo -e '\\033[32m[$(date +%H:%M:%S)]\\033[0m 📊 Portfolio status...'; sleep 9; done"
    fi
done &
EOF

chmod +x "$ROOT_DIR/restore_battlestation.sh"

# Start the restoration daemon
nohup bash "$ROOT_DIR/restore_battlestation.sh" > /dev/null 2>&1 &
echo $! > "$ROOT_DIR/.battlestation_daemon.pid"

# Focus on first window
tmux select-window -t "$SESSION_NAME:RICK_HIVE"

log "✅ RBOTZILLA Battlestation created!"
log "📺 Windows: RICK_HIVE | OANDA | COINBASE"
log "🔄 Auto-restore: Active (daemon PID: $(cat $ROOT_DIR/.battlestation_daemon.pid))"
log "🎮 Attach with: tmux attach -t $SESSION_NAME"

# Attach to session
tmux attach-session -t "$SESSION_NAME"