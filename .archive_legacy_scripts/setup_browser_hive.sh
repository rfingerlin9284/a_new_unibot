#!/bin/bash
# setup_browser_hive.sh - Setup Browser-Based Hive Mind
# PIN 841921 Approved | Charter Compliant
#
# Installs dependencies and configures browser automation for
# Rick's hive mind to connect to ChatGPT, Grok, DeepSeek, GitHub Copilot

set -euo pipefail

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🧠 RICK BROWSER HIVE MIND SETUP            ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Navigate to project root
cd /home/ing/RICK/R_H_UNI

echo -e "${CYAN}📦 Installing Dependencies...${NC}"
echo ""

# Check if venv exists
if [[ ! -d "pre_upgrade/standalone/.venv" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo -e "${YELLOW}Creating venv...${NC}"
    python3 -m venv pre_upgrade/standalone/.venv
fi

# Activate venv
source pre_upgrade/standalone/.venv/bin/activate

# Install Selenium and WebDriver Manager
echo -e "${CYAN}Installing Selenium...${NC}"
pip install -q selenium webdriver-manager

# Install Chrome/Chromium if not present
echo ""
echo -e "${CYAN}🌐 Checking for Chrome/Chromium...${NC}"

if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version)
    echo -e "${GREEN}✅ Chrome installed: $CHROME_VERSION${NC}"
elif command -v chromium-browser &> /dev/null; then
    CHROMIUM_VERSION=$(chromium-browser --version)
    echo -e "${GREEN}✅ Chromium installed: $CHROMIUM_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Chrome/Chromium not found${NC}"
    echo -e "${YELLOW}Installing Chromium...${NC}"
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y chromium-browser chromium-chromedriver
    elif command -v yum &> /dev/null; then
        sudo yum install -y chromium chromedriver
    else
        echo -e "${RED}❌ Could not install Chromium automatically${NC}"
        echo -e "${YELLOW}Please install Chrome or Chromium manually${NC}"
        echo -e "${YELLOW}Download from: https://www.google.com/chrome/${NC}"
        exit 1
    fi
fi

# Create browser cache directory
echo ""
echo -e "${CYAN}📁 Creating browser cache directory...${NC}"
mkdir -p .browser_cache
chmod 700 .browser_cache
echo -e "${GREEN}✅ Cache directory created${NC}"

# Test browser automation
echo ""
echo -e "${CYAN}🧪 Testing browser automation...${NC}"

python3 << 'PYTHON_TEST'
import sys
sys.path.insert(0, '/home/ing/RICK/R_H_UNI')

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    print("✅ Selenium imported successfully")
    
    # Test driver creation
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    print("✅ Chrome driver created successfully")
    
    # Test navigation
    driver.get("https://www.google.com")
    print(f"✅ Navigation test passed (title: {driver.title[:30]}...)")
    
    driver.quit()
    print("✅ Browser automation working!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
PYTHON_TEST

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Browser automation test passed${NC}"
else
    echo -e "${RED}❌ Browser automation test failed${NC}"
    exit 1
fi

# Test hive mind imports
echo ""
echo -e "${CYAN}🧪 Testing hive mind modules...${NC}"

python3 << 'PYTHON_HIVE_TEST'
import sys
sys.path.insert(0, '/home/ing/RICK/R_H_UNI')

try:
    from hive.browser_ai_connector import BrowserAIConnector, AIProvider
    print("✅ browser_ai_connector imported")
    
    from hive.rick_hive_browser import RickHiveBrowserMind, get_hive_browser_mind
    print("✅ rick_hive_browser imported")
    
    print("✅ All hive mind modules working!")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
PYTHON_HIVE_TEST

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Hive mind modules working${NC}"
else
    echo -e "${RED}❌ Hive mind module test failed${NC}"
    exit 1
fi

# Create test script
echo ""
echo -e "${CYAN}📝 Creating test script...${NC}"

cat > test_hive_browser.py << 'TEST_SCRIPT'
#!/usr/bin/env python3
"""Quick test of browser hive mind."""
import sys
sys.path.insert(0, '/home/ing/RICK/R_H_UNI')

from hive.rick_hive_browser import get_hive_browser_mind
from hive.browser_ai_connector import AIProvider

print("🧠 Rick Browser Hive Mind - Quick Test")
print("=" * 50)

# Create hive with PIN
hive = get_hive_browser_mind(pin=841921, headless=True)

try:
    # Test status
    print("\n📊 Checking provider status...")
    status = hive.get_provider_status()
    print(f"Browser enabled: {status['browser_enabled']}")
    print(f"PIN verified: {status['pin_verified']}")
    
    # Test single provider
    print("\n💬 Testing ChatGPT...")
    response = hive.query_single_provider(
        AIProvider.CHATGPT,
        "What is 2+2? Answer with just the number."
    )
    print(f"Response: {response.response}")
    print(f"Confidence: {response.confidence}")
    print(f"Latency: {response.latency_ms}ms")
    
    if response.error:
        print(f"Error: {response.error}")
    
    print("\n✅ Test complete!")

finally:
    hive.cleanup()
TEST_SCRIPT

chmod +x test_hive_browser.py
echo -e "${GREEN}✅ Test script created: test_hive_browser.py${NC}"

# Summary
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ BROWSER HIVE MIND SETUP COMPLETE         ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}📚 What was installed:${NC}"
echo -e "  • Selenium (browser automation)"
echo -e "  • WebDriver Manager (automatic driver updates)"
echo -e "  • Chrome/Chromium (if not already present)"
echo ""

echo -e "${CYAN}🧠 Available AI Providers:${NC}"
echo -e "  • ChatGPT (chat.openai.com)"
echo -e "  • Grok (x.com/i/grok)"
echo -e "  • DeepSeek (chat.deepseek.com)"
echo -e "  • Perplexity (perplexity.ai)"
echo -e "  • GitHub Copilot (via VS Code extension - TBD)"
echo ""

echo -e "${CYAN}🚀 Quick Test:${NC}"
echo -e "  ${YELLOW}python3 test_hive_browser.py${NC}"
echo ""

echo -e "${CYAN}💡 Usage in Rick:${NC}"
echo -e "${YELLOW}from hive.rick_hive_browser import get_hive_browser_mind"
echo -e ""
echo -e "hive = get_hive_browser_mind(pin=841921, headless=True)"
echo -e "consensus = hive.consult_hive('Analyze EUR/USD at 1.0850')"
echo -e "print(consensus.consensus_text)${NC}"
echo ""

echo -e "${CYAN}🔒 Security Notes:${NC}"
echo -e "  • No API keys stored (uses browser automation)"
echo -e "  • Browser sessions cached in .browser_cache/"
echo -e "  • PIN 841921 required for all operations"
echo -e "  • Browsers run in headless mode by default"
echo ""

echo -e "${CYAN}📝 Next Steps:${NC}"
echo -e "  1. Run test: ${YELLOW}python3 test_hive_browser.py${NC}"
echo -e "  2. Test in Rick: Edit rick_chat_gpt.py to use hive"
echo -e "  3. View logs: Browser cache in .browser_cache/"
echo ""

echo -e "${GREEN}✅ Setup complete!${NC}"
