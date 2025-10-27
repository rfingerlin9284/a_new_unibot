#!/bin/bash

################################################################################
#
#  🎭 RICK TRADING TMUX HELPER SCRIPT
#
#  Easy commands for managing your Rick trading tmux session
#  Usage: ./tmux_helper.sh [command]
#
################################################################################

RICK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
SESSION_NAME="rick"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Show menu
show_menu() {
    echo
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║          🎭 RICK TRADING TMUX HELPER MENU                     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo
    echo "  ${BLUE}Session Management:${NC}"
    echo "    1) Start session           - Create and attach to rick tmux session"
    echo "    2) Attach session          - Attach to existing rick session"
    echo "    3) Kill session            - Stop all rick tmux windows/panes"
    echo "    4) Status                  - Show current session status"
    echo
    echo "  ${BLUE}Pane Commands:${NC}"
    echo "    5) Show panes              - List all panes in rick session"
    echo "    6) Split vertical          - Add new vertical pane"
    echo "    7) Split horizontal        - Add new horizontal pane"
    echo
    echo "  ${BLUE}Quick Actions:${NC}"
    echo "    8) View engine pane        - Maximize trading engine pane"
    echo "    9) View narration pane     - Maximize narration pane"
    echo "    10) View status pane       - Maximize system status pane"
    echo "    11) Show shortcuts         - Display tmux keyboard shortcuts"
    echo
    echo "  ${BLUE}Other:${NC}"
    echo "    12) Clear screen           - Clear this menu"
    echo "    0) Exit menu               - Close this helper"
    echo
    echo "  Enter command number (1-12, 0 to exit): "
}

# Start session
start_session() {
    echo
    echo -e "${YELLOW}🚀 Starting RICK tmux session...${NC}"
    echo
    
    # Kill existing session if it exists
    tmux kill-session -t $SESSION_NAME 2>/dev/null
    
    # Create new session
    tmux new-session -d -s $SESSION_NAME -x 200 -y 50
    
    # Pane 0.0 - Trading Engine
    echo -e "${GREEN}✅ Pane 0.0: Starting Trading Engine${NC}"
    tmux send-keys -t $SESSION_NAME:0.0 "cd $RICK_DIR && python3 oanda_trading_engine.py --env practice" Enter
    sleep 2
    
    # Pane 0.1 - Narration Monitor
    echo -e "${GREEN}✅ Pane 0.1: Starting Narration Monitor${NC}"
    tmux split-window -t $SESSION_NAME -h
    tmux send-keys -t $SESSION_NAME:0.1 "cd $RICK_DIR && watch -n 1 'tail -20 narration.jsonl 2>/dev/null | grep -E \"Rick|ML_ANALYZER|SMART|HIVE\" | tail -10 || echo \"Waiting for narration...\"'" Enter
    sleep 1
    
    # Pane 0.2 - System Status
    echo -e "${GREEN}✅ Pane 0.2: Starting System Status${NC}"
    tmux split-window -t $SESSION_NAME -v
    tmux send-keys -t $SESSION_NAME:0.2 "cd $RICK_DIR && watch -n 2 './status.sh 2>/dev/null | head -20'" Enter
    
    echo
    echo -e "${GREEN}✅ SESSION READY!${NC}"
    echo
    echo -e "${YELLOW}Attaching to session in 2 seconds...${NC}"
    sleep 2
    
    tmux attach-session -t $SESSION_NAME
}

# Attach to existing session
attach_session() {
    echo
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo -e "${GREEN}✅ Attaching to $SESSION_NAME session${NC}"
        echo
        sleep 1
        tmux attach-session -t $SESSION_NAME
    else
        echo -e "${RED}❌ Session '$SESSION_NAME' does not exist${NC}"
        echo -e "${YELLOW}Use option 1 to start a new session${NC}"
        echo
    fi
}

# Kill session
kill_session() {
    echo
    echo -e "${YELLOW}Are you sure you want to kill the $SESSION_NAME session? (y/n)${NC}"
    read -r response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        tmux kill-session -t $SESSION_NAME 2>/dev/null
        echo -e "${GREEN}✅ Session killed${NC}"
        echo
    else
        echo -e "${BLUE}Cancelled${NC}"
        echo
    fi
}

# Session status
show_status() {
    echo
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                   SESSION STATUS                              ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo
    
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo -e "${GREEN}✅ Session '$SESSION_NAME' exists${NC}"
        echo
        echo "Panes:"
        tmux list-panes -t $SESSION_NAME -a
        echo
        echo "Windows:"
        tmux list-windows -t $SESSION_NAME
        echo
        echo "All Sessions:"
        tmux list-sessions
    else
        echo -e "${RED}❌ Session '$SESSION_NAME' not running${NC}"
        echo -e "${YELLOW}Start with option 1${NC}"
    fi
    echo
}

# Show panes
show_panes() {
    echo
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    ACTIVE PANES                               ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
        tmux list-panes -t $SESSION_NAME -a
        echo
    else
        echo -e "${RED}❌ No active session${NC}"
        echo
    fi
}

# View engine pane
view_engine() {
    echo
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo -e "${YELLOW}Maximizing trading engine pane (Pane 0.0)${NC}"
        echo -e "${BLUE}Press Ctrl+B then z to return to split view${NC}"
        echo
        sleep 1
        tmux select-pane -t $SESSION_NAME:0.0
        tmux resize-pane -t $SESSION_NAME:0.0 -Z
        tmux attach-session -t $SESSION_NAME
    else
        echo -e "${RED}❌ No active session${NC}"
        echo
    fi
}

# View narration pane
view_narration() {
    echo
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo -e "${YELLOW}Maximizing narration pane (Pane 0.1)${NC}"
        echo -e "${BLUE}Press Ctrl+B then z to return to split view${NC}"
        echo
        sleep 1
        tmux select-pane -t $SESSION_NAME:0.1
        tmux resize-pane -t $SESSION_NAME:0.1 -Z
        tmux attach-session -t $SESSION_NAME
    else
        echo -e "${RED}❌ No active session${NC}"
        echo
    fi
}

# View status pane
view_status() {
    echo
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo -e "${YELLOW}Maximizing status pane (Pane 0.2)${NC}"
        echo -e "${BLUE}Press Ctrl+B then z to return to split view${NC}"
        echo
        sleep 1
        tmux select-pane -t $SESSION_NAME:0.2
        tmux resize-pane -t $SESSION_NAME:0.2 -Z
        tmux attach-session -t $SESSION_NAME
    else
        echo -e "${RED}❌ No active session${NC}"
        echo
    fi
}

# Show shortcuts
show_shortcuts() {
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║              TMUX KEYBOARD SHORTCUTS                          ║
║           (All start with Ctrl+B prefix)                      ║
╚════════════════════════════════════════════════════════════════╝

NAVIGATION:
  ↑ ↓ ← →        Navigate between panes
  o              Cycle to next pane
  q              Show pane numbers
  ;              Go to last pane

PANE MANAGEMENT:
  z              Toggle maximize/minimize
  x              Kill pane
  {              Move pane left
  }              Move pane right
  Space          Cycle layouts
  Ctrl+↑↓←→      Resize pane

WINDOW MANAGEMENT:
  c              New window
  n              Next window
  p              Previous window
  0-9            Jump to window
  w              Window selector
  &              Kill window

SESSION MANAGEMENT:
  d              Detach session (leave running)
  $              Rename session
  (              Previous session
  )              Next session
  L              Last session

TEXT MODES:
  [              Enter scroll mode
  ]              Paste
  Ctrl+S         Search forward
  Ctrl+R         Search backward
  q              Exit scroll mode

═══════════════════════════════════════════════════════════════

EXAMPLE WORKFLOW:

1. Start session:
   tmux attach-session -t rick

2. View trading:
   Pane 0.0 shows automatically

3. Check narration:
   Ctrl+B then →

4. Back to engine:
   Ctrl+B then ←

5. Full screen narration:
   Ctrl+B then z

6. Return to split:
   Ctrl+B then z (again)

7. Leave running:
   Ctrl+B then d

8. Come back later:
   tmux attach-session -t rick

EOF
}

# Main loop
while true; do
    show_menu
    read -r choice
    
    case $choice in
        1) start_session ;;
        2) attach_session ;;
        3) kill_session ;;
        4) show_status ;;
        5) show_panes ;;
        6) 
            if tmux has-session -t $SESSION_NAME 2>/dev/null; then
                tmux split-window -t $SESSION_NAME -v
                echo -e "${GREEN}✅ Vertical split created${NC}"
            else
                echo -e "${RED}❌ No active session${NC}"
            fi
            echo
            ;;
        7) 
            if tmux has-session -t $SESSION_NAME 2>/dev/null; then
                tmux split-window -t $SESSION_NAME -h
                echo -e "${GREEN}✅ Horizontal split created${NC}"
            else
                echo -e "${RED}❌ No active session${NC}"
            fi
            echo
            ;;
        8) view_engine ;;
        9) view_narration ;;
        10) view_status ;;
        11) show_shortcuts ;;
        12) clear ;;
        0) 
            echo
            echo -e "${YELLOW}Goodbye! 👋${NC}"
            echo
            exit 0
            ;;
        *) 
            echo
            echo -e "${RED}Invalid option${NC}"
            echo
            ;;
    esac
done
