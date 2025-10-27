#!/bin/bash
# launch_rick_gpt.sh - Launch ChatGPT-Style Rick Interface
# PIN 841921 Approved | Charter Compliant

set -euo pipefail

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}🤖 Launching Rick Trading Assistant (ChatGPT-Style)${NC}"
echo -e "${CYAN}=================================================${NC}"
echo ""

# Navigate to project root
cd /home/ing/RICK/R_H_UNI

# Check if rick_chat_gpt.py exists
if [[ ! -f "rick_chat_gpt.py" ]]; then
    echo -e "${YELLOW}⚠️  rick_chat_gpt.py not found${NC}"
    exit 1
fi

# Check if port 8503 is already in use
if lsof -Pi :8503 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8503 already in use. Killing existing process...${NC}"
    pkill -f "streamlit run rick_chat_gpt.py" || true
    sleep 2
fi

# Verify venv exists
VENV_PYTHON="pre_upgrade/standalone/.venv/bin/python3"
if [[ ! -f "$VENV_PYTHON" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found at $VENV_PYTHON${NC}"
    echo -e "${YELLOW}Falling back to system Python3${NC}"
    VENV_PYTHON="python3"
fi

# Log launch action
echo "[$(date -u +%Y-%m-%dT%H:%M:%S)] ACTION=LAUNCH_RICK_GPT DETAILS=chatgpt_style REASON='Starting Rick with ChatGPT interface and real backend connection'" >> alerts_log.jsonl

echo -e "${GREEN}✅ Starting Rick Trading Assistant...${NC}"
echo ""

# Launch Rick with ChatGPT theme
if [[ "$VENV_PYTHON" == "python3" ]]; then
    streamlit run rick_chat_gpt.py \
        --server.port 8503 \
        --server.address localhost \
        --server.headless true \
        --browser.gatherUsageStats false \
        --theme.base dark \
        --theme.primaryColor "#00ffd0" \
        --theme.backgroundColor "#0b1020" \
        --theme.secondaryBackgroundColor "#11162a" \
        --theme.textColor "#e6f7ff" &
else
    $VENV_PYTHON -m streamlit run rick_chat_gpt.py \
        --server.port 8503 \
        --server.address localhost \
        --server.headless true \
        --browser.gatherUsageStats false \
        --theme.base dark \
        --theme.primaryColor "#00ffd0" \
        --theme.backgroundColor "#0b1020" \
        --theme.secondaryBackgroundColor "#11162a" \
        --theme.textColor "#e6f7ff" &
fi

# Get PID
RICK_PID=$!

sleep 3

echo ""
echo -e "${GREEN}✅ Rick Trading Assistant is ready!${NC}"
echo ""
echo -e "${CYAN}📌 Access:${NC}"
echo -e "   URL: ${YELLOW}http://localhost:8503${NC}"
echo -e "   PID: ${YELLOW}$RICK_PID${NC}"
echo ""
echo -e "${CYAN}💬 Try asking Rick:${NC}"
echo -e "   • \"Show me the current status\""
echo -e "   • \"Any active positions?\""
echo -e "   • \"What's the market looking like?\""
echo -e "   • \"Explain FVG in simple terms\""
echo ""
echo -e "${CYAN}⚙️  System Commands (PIN 841921):${NC}"
echo -e "   • RICK> START GHOST"
echo -e "   • RICK> TOGGLE MODE"
echo -e "   • RICK> HALT"
echo ""
echo -e "${CYAN}🛑 To Stop:${NC}"
echo -e "   ${YELLOW}pkill -f 'streamlit run rick_chat_gpt.py'${NC}"
echo ""
