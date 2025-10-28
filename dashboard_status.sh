#!/bin/bash
# dashboard_status.sh - Quick Status Check for All Dashboard Components
# Shows what's running and how to access it

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🤖 RICK DASHBOARD STATUS CHECK           ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check mode
MODE="UNKNOWN"
if [[ -f /home/ing/RICK/R_H_UNI/.upgrade_toggle ]]; then
    MODE=$(cat /home/ing/RICK/R_H_UNI/.upgrade_toggle 2>/dev/null || echo "UNKNOWN")
fi

echo -e "${CYAN}📊 SYSTEM MODE:${NC}"
case "$MODE" in
    "OFF"|"GHOST")
        echo -e "   ${YELLOW}🌫️  GHOST MODE${NC} (Paper Trading)"
        ;;
    "CANARY")
        echo -e "   ${YELLOW}🐤 CANARY MODE${NC} (Limited Live)"
        ;;
    "ON"|"LIVE")
        echo -e "   ${RED}🔴 LIVE MODE${NC} (Real Money)"
        ;;
    *)
        echo -e "   ${RED}❓ UNKNOWN${NC}"
        ;;
esac
echo ""

# Check services
echo -e "${CYAN}🚀 SERVICES:${NC}"

# Enhanced Dashboard
if pgrep -f "dashboard_enhanced.py" > /dev/null; then
    PID=$(pgrep -f "dashboard_enhanced.py")
    echo -e "   ${GREEN}✅ Enhanced Dashboard${NC}"
    echo -e "      URL: ${YELLOW}http://localhost:8501${NC}"
    echo -e "      PID: ${YELLOW}$PID${NC}"
else
    echo -e "   ${RED}❌ Enhanced Dashboard (OFFLINE)${NC}"
    echo -e "      Start: ${YELLOW}streamlit run dashboard_enhanced.py --server.port 8501${NC}"
fi

# Rick Chat GPT
if pgrep -f "rick_chat_gpt.py" > /dev/null; then
    PID=$(pgrep -f "rick_chat_gpt.py")
    echo -e "   ${GREEN}✅ Rick Chat GPT${NC}"
    echo -e "      URL: ${YELLOW}http://localhost:8503${NC}"
    echo -e "      PID: ${YELLOW}$PID${NC}"
else
    echo -e "   ${RED}❌ Rick Chat GPT (OFFLINE)${NC}"
    echo -e "      Start: ${YELLOW}./launch_rick_gpt.sh${NC}"
fi

# Live Activity Feed (test)
if pgrep -f "live_activity_feed.py" > /dev/null; then
    PID=$(pgrep -f "live_activity_feed.py")
    echo -e "   ${GREEN}✅ Live Activity Feed (Test)${NC}"
    echo -e "      URL: ${YELLOW}http://localhost:8502${NC}"
    echo -e "      PID: ${YELLOW}$PID${NC}"
else
    echo -e "   ${YELLOW}⚪ Live Activity Feed${NC} (Optional test widget)"
fi

# Ghost Trading Engine
if pgrep -f "ghost_trading_engine\|live_ghost_engine" > /dev/null; then
    PID=$(pgrep -f "ghost_trading_engine\|live_ghost_engine")
    echo -e "   ${GREEN}✅ Ghost Trading Engine${NC}"
    echo -e "      PID: ${YELLOW}$PID${NC}"
else
    echo -e "   ${YELLOW}⚪ Ghost Trading Engine${NC} (Not running)"
    echo -e "      Start: ${YELLOW}./start_ghost_trading.sh${NC}"
fi

# TMUX Session
if tmux has-session -t RICK_UNIFIED_DASH 2>/dev/null; then
    echo -e "   ${GREEN}✅ TMUX Monitoring Session${NC}"
    echo -e "      Attach: ${YELLOW}tmux attach -t RICK_UNIFIED_DASH${NC}"
else
    echo -e "   ${YELLOW}⚪ TMUX Monitoring${NC} (Not running)"
    echo -e "      Start: ${YELLOW}./scripts/launch_unified_dashboard.sh${NC}"
fi

echo ""
echo -e "${CYAN}📋 QUICK ACCESS:${NC}"
echo -e "   • Main Dashboard:  ${YELLOW}http://localhost:8501${NC}"
echo -e "   • Rick Chat:       ${YELLOW}http://localhost:8503${NC}"
echo -e "   • Activity Feed:   ${YELLOW}http://localhost:8502${NC}"
echo ""

echo -e "${CYAN}💬 TRY ASKING RICK:${NC}"
echo -e "   • \"Show me the current status\""
echo -e "   • \"Any active positions?\""
echo -e "   • \"Explain FVG in simple terms\""
echo -e "   • \"What's the market looking like?\""
echo ""

echo -e "${CYAN}⚙️  SYSTEM COMMANDS (PIN 841921):${NC}"
echo -e "   • ${YELLOW}RICK> START GHOST${NC}    - Launch trading engine"
echo -e "   • ${YELLOW}RICK> TOGGLE MODE${NC}    - Switch GHOST ↔ LIVE"
echo -e "   • ${YELLOW}RICK> HALT${NC}           - Emergency stop"
echo ""

echo -e "${CYAN}📚 DOCUMENTATION:${NC}"
echo -e "   • Dashboard:      ${YELLOW}DASHBOARD_INTEGRATION_COMPLETE.md${NC}"
echo -e "   • Rick Chat:      ${YELLOW}RICK_CHAT_GPT_COMPLETE.md${NC}"
echo -e "   • Action Plan:    ${YELLOW}DASHBOARD_UNIFIED_ACTION_PLAN.md${NC}"
echo ""

echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
