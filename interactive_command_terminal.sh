#!/bin/bash
# 🎮 Interactive Command Terminal - Bottom-right pane
# Type messages/commands to control system or send to log
# PIN: 841921

WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
LOG_FILE="$WORK_DIR/dashboard.log"
COMMAND_LOG="$WORK_DIR/command_log.jsonl"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}${BOLD}🎮 RBOTzilla Command Terminal${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Available Commands:${NC}"
echo "  start          - Start trading engine"
echo "  stop           - Stop trading engine"
echo "  status         - Show engine status"
echo "  positions      - Show open positions"
echo "  log [message]  - Log custom message"
echo "  agents on      - Show agents list in top-right pane"
echo "  agents off     - Hide agents list in top-right pane"
echo "  narration follow- Replace left pane with live, plain-English stream"
echo "  narration panel - Restore left pane to full dashboard view"
echo "  help           - Show all commands"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Main loop
while true; do
    echo -e "${CYAN}> ${NC}" | tr -d '\n'
    read -r user_input
    
    # Parse command
    cmd=$(echo "$user_input" | awk '{print $1}')
    args=$(echo "$user_input" | cut -d' ' -f2-)
    
    case "$cmd" in
        start)
            echo -e "${GREEN}✅ Starting trading engine...${NC}"
            echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"command\": \"start\", \"status\": \"executed\"}" >> "$COMMAND_LOG"
            cd "$WORK_DIR" && python3 oanda_trading_engine.py &
            sleep 2
            echo -e "${GREEN}✅ Trading engine started${NC}"
            ;;
        stop)
            echo -e "${YELLOW}⏹️  Stopping trading engine...${NC}"
            echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"command\": \"stop\", \"status\": \"executed\"}" >> "$COMMAND_LOG"
            pkill -f "oanda_trading_engine.py" 2>/dev/null || true
            sleep 1
            echo -e "${GREEN}✅ Trading engine stopped${NC}"
            ;;
        status)
            echo -e "${CYAN}📊 Engine Status:${NC}"
            ps aux | grep -E "oanda_trading_engine|python3" | grep -v grep && echo -e "${GREEN}✅ Running${NC}" || echo -e "${RED}❌ Not running${NC}"
            ;;
        positions)
            echo -e "${CYAN}📈 Open Positions:${NC}"
            if [ -f "$WORK_DIR/connection_state.json" ]; then
                jq -r '.open_trades[] | "\(.instrument): \(.units) units @ \(.entry_price)"' "$WORK_DIR/connection_state.json" 2>/dev/null || echo -e "${YELLOW}No positions data available${NC}"
            else
                echo -e "${YELLOW}No position data available yet${NC}"
            fi
            ;;
        log)
            if [ -z "$args" ]; then
                echo -e "${RED}❌ Usage: log [message]${NC}"
            else
                echo -e "${GREEN}📝 Logging: $args${NC}"
                echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"type\": \"manual_log\", \"message\": \"$args\"}" >> "$COMMAND_LOG"
                echo -e "${GREEN}✅ Message logged${NC}"
            fi
            ;;
    agents)
            sub=$(echo "$args" | awk '{print $1}')
            SESSION_NAME="rbotzilla-dashboard"
            WINDOW_NAME="Dashboard"
            TARGET_PANE="$SESSION_NAME:$WINDOW_NAME.1"
            case "$sub" in
                on)
                    echo -e "${GREEN}🔎 Enabling agents list in top-right pane...${NC}"
                    "$WORK_DIR/scripts/pane_topright_agents_show.sh" 2>/dev/null || tmux send-keys -t "$TARGET_PANE" C-c "cd '$WORK_DIR' && python3 tools/strategy_status.py --watch --verbose" Enter
                    echo -e "${GREEN}✅ Agents list enabled${NC}"
                    ;;
                off)
                    echo -e "${GREEN}🙈 Hiding agents list in top-right pane...${NC}"
                    "$WORK_DIR/scripts/pane_topright_agents_hide.sh" 2>/dev/null || tmux send-keys -t "$TARGET_PANE" C-c "cd '$WORK_DIR' && python3 tools/strategy_status.py --watch" Enter
                    echo -e "${GREEN}✅ Agents list hidden${NC}"
                    ;;
                *)
                    echo -e "${YELLOW}Usage:${NC} agents on|off"
                    ;;
            esac
            ;;
    narration)
            sub=$(echo "$args" | awk '{print $1}')
            SESSION_NAME="rbotzilla-dashboard"
            WINDOW_NAME="Dashboard"
            TARGET_PANE="$SESSION_NAME:$WINDOW_NAME.0"
            case "$sub" in
                follow)
                    echo -e "${GREEN}📜 Switching left pane to live narration follow (plain English)...${NC}"
                    "$WORK_DIR/scripts/pane_left_follow_narration.sh"
                    echo -e "${GREEN}✅ Left pane now following narration live${NC}"
                    ;;
                panel)
                    echo -e "${GREEN}🖥️  Restoring left pane to dashboard monitor...${NC}"
                    "$WORK_DIR/scripts/pane_left_full_monitor.sh"
                    echo -e "${GREEN}✅ Left pane restored to dashboard view${NC}"
                    ;;
                *)
                    echo -e "${YELLOW}Usage:${NC} narration follow|panel"
                    ;;
            esac
            ;;
        help)
            echo -e "${CYAN}${BOLD}Available Commands:${NC}"
            echo "  start              Start trading engine"
            echo "  stop               Stop trading engine"
            echo "  status             Show engine status"
            echo "  positions          Show open positions"
            echo "  log [msg]          Log custom message"
            echo "  agents on          Show agents list in top-right pane"
            echo "  agents off         Hide agents list in top-right pane"
            echo "  narration follow   Replace left pane with live narration follower"
            echo "  narration panel    Restore left pane to dashboard monitor"
            echo "  help               Show this help"
            echo "  clear              Clear terminal"
            echo "  exit/quit          Exit terminal"
            ;;
        clear)
            clear
            ;;
        exit|quit)
            echo -e "${YELLOW}Exiting command terminal...${NC}"
            exit 0
            ;;
        "")
            continue
            ;;
        *)
            echo -e "${RED}❌ Unknown command: '$cmd'${NC}"
            echo -e "${YELLOW}Type 'help' for available commands${NC}"
            ;;
    esac
    
    echo ""
done
