#!/bin/bash
# setup_rick_ai.sh - Setup AI-Powered Rick with OpenAI Integration
# PIN 841921 Approved

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🤖 RICK AI - OpenAI Integration Setup      ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
echo ""

cd /home/ing/RICK/R_H_UNI

# ============================================================================
# STEP 1: Install Dependencies
# ============================================================================

echo -e "${CYAN}📦 Step 1: Installing Dependencies${NC}"
echo ""

VENV_PYTHON="pre_upgrade/standalone/.venv/bin/python3"
VENV_PIP="pre_upgrade/standalone/.venv/bin/pip"

if [[ -f "$VENV_PYTHON" ]]; then
    echo -e "${GREEN}✅ Virtual environment found${NC}"
    
    echo -e "${YELLOW}Installing OpenAI SDK...${NC}"
    $VENV_PIP install --upgrade openai python-dotenv
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ OpenAI SDK installed${NC}"
    else
        echo -e "${RED}❌ Failed to install OpenAI SDK${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Virtual environment not found. Using system Python.${NC}"
    
    echo -e "${YELLOW}Installing OpenAI SDK globally...${NC}"
    pip3 install --user --upgrade openai python-dotenv
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ OpenAI SDK installed${NC}"
    else
        echo -e "${RED}❌ Failed to install OpenAI SDK${NC}"
        exit 1
    fi
fi

echo ""

# ============================================================================
# STEP 2: Configure API Key
# ============================================================================

echo -e "${CYAN}🔑 Step 2: Configure OpenAI API Key${NC}"
echo ""

if [[ -f ".env" ]]; then
    if grep -q "OPENAI_API_KEY" .env; then
        echo -e "${YELLOW}⚠️  OPENAI_API_KEY already exists in .env${NC}"
        echo ""
        read -p "Overwrite existing key? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Keeping existing API key${NC}"
            SKIP_KEY=true
        fi
    fi
fi

if [[ "${SKIP_KEY:-false}" != "true" ]]; then
    echo -e "${YELLOW}Enter your OpenAI API key:${NC}"
    echo -e "${CYAN}(Get it from: https://platform.openai.com/api-keys)${NC}"
    echo ""
    
    read -p "API Key (sk-...): " -r API_KEY
    
    if [[ -z "$API_KEY" ]]; then
        echo -e "${RED}❌ No API key provided${NC}"
        exit 1
    fi
    
    # Append to .env (or create if doesn't exist)
    if grep -q "OPENAI_API_KEY" .env 2>/dev/null; then
        # Replace existing key
        sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$API_KEY/" .env
        echo -e "${GREEN}✅ Updated OPENAI_API_KEY in .env${NC}"
    else
        # Add new key
        echo "OPENAI_API_KEY=$API_KEY" >> .env
        echo -e "${GREEN}✅ Added OPENAI_API_KEY to .env${NC}"
    fi
    
    # Set secure permissions
    chmod 600 .env
    echo -e "${GREEN}✅ Set .env permissions (0600)${NC}"
fi

echo ""

# ============================================================================
# STEP 3: Test Connection
# ============================================================================

echo -e "${CYAN}🔍 Step 3: Testing OpenAI Connection${NC}"
echo ""

cat > test_openai.py << 'PYTHON_EOF'
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env")
    exit(1)

print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:]}")

try:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Rick is online!' in one sentence."}],
        max_tokens=20
    )
    print(f"✅ OpenAI Response: {response.choices[0].message.content}")
    print("✅ Connection successful!")
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    exit(1)
PYTHON_EOF

if [[ -f "$VENV_PYTHON" ]]; then
    $VENV_PYTHON test_openai.py
else
    python3 test_openai.py
fi

TEST_RESULT=$?
rm -f test_openai.py

echo ""

if [[ $TEST_RESULT -eq 0 ]]; then
    echo -e "${GREEN}✅ OpenAI connection verified!${NC}"
else
    echo -e "${RED}❌ OpenAI connection failed. Check your API key.${NC}"
    exit 1
fi

echo ""

# ============================================================================
# STEP 4: Create Launch Script
# ============================================================================

echo -e "${CYAN}🚀 Step 4: Creating Launch Script${NC}"
echo ""

cat > launch_rick_ai.sh << 'LAUNCH_EOF'
#!/bin/bash
# launch_rick_ai.sh - Launch AI-Powered Rick (OpenAI Integration)

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}🤖 Launching AI-Powered Rick (OpenAI Integration)${NC}"
echo ""

cd /home/ing/RICK/R_H_UNI

# Check if port 8504 is in use
if lsof -Pi :8504 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${CYAN}Killing existing process on port 8504...${NC}"
    pkill -f "streamlit run rick_ai_powered.py" || true
    sleep 2
fi

# Launch Rick AI
VENV_PYTHON="pre_upgrade/standalone/.venv/bin/python3"

if [[ -f "$VENV_PYTHON" ]]; then
    $VENV_PYTHON -m streamlit run rick_ai_powered.py \
        --server.port 8504 \
        --server.address localhost \
        --server.headless true \
        --browser.gatherUsageStats false \
        --theme.base dark \
        --theme.primaryColor "#00ffd0" \
        --theme.backgroundColor "#0b1020" \
        --theme.secondaryBackgroundColor "#11162a" \
        --theme.textColor "#e6f7ff" &
else
    python3 -m streamlit run rick_ai_powered.py \
        --server.port 8504 \
        --server.address localhost \
        --server.headless true \
        --browser.gatherUsageStats false &
fi

RICK_PID=$!

sleep 3

echo ""
echo -e "${GREEN}✅ AI-Powered Rick is ready!${NC}"
echo ""
echo -e "${CYAN}📌 Access:${NC}"
echo -e "   URL: http://localhost:8504"
echo -e "   PID: $RICK_PID"
echo ""
echo -e "${CYAN}💬 Now with Real GPT-4 Conversation!${NC}"
echo -e "   Ask anything naturally - no pre-scripted responses"
echo ""
LAUNCH_EOF

chmod +x launch_rick_ai.sh
echo -e "${GREEN}✅ Created launch_rick_ai.sh${NC}"

echo ""

# ============================================================================
# COMPLETION
# ============================================================================

echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          ✅ SETUP COMPLETE!                   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}🚀 To Launch AI-Powered Rick:${NC}"
echo -e "   ${YELLOW}./launch_rick_ai.sh${NC}"
echo ""

echo -e "${CYAN}📌 Access:${NC}"
echo -e "   ${YELLOW}http://localhost:8504${NC}"
echo ""

echo -e "${CYAN}🆕 What's Different:${NC}"
echo -e "   • Real OpenAI GPT-4 conversation"
echo -e "   • Natural language understanding"
echo -e "   • No pre-scripted responses"
echo -e "   • Still reads real RICK system data"
echo ""

echo -e "${CYAN}💬 Try Asking:${NC}"
echo -e "   • \"What do you think about the current market?\""
echo -e "   • \"Explain your risk management philosophy\""
echo -e "   • \"Should I be concerned about anything?\""
echo -e "   • Any natural conversation!"
echo ""

echo -e "${CYAN}📊 System Data Still Connected:${NC}"
echo -e "   • narration.jsonl (bot activities)"
echo -e "   • pnl.jsonl (profit/loss)"
echo -e "   • .upgrade_toggle (mode)"
echo ""
