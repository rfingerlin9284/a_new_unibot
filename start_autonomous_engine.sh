#!/bin/bash
# Start autonomous engine with properly loaded environment variables
# Avoids python-dotenv parsing issues with multi-line secrets

cd /home/ing/RICK/RICK_LIVE_PROTOTYPE

# Load environment variables manually (skips multi-line keys that break dotenv)
export RICK_PIN=841921

# OANDA Practice credentials
export OANDA_ENV=practice
export OANDA_ACCOUNT_ID=101-001-31210531-002
export OANDA_API_TOKEN=1a45b898c57f609f329a0af8f2800e7e-6fcc25eef7c3f94ad79acff6d5f6bfaf

# Start the autonomous engine
echo "🤖 Starting Autonomous Decision Engine..."
echo "📍 OANDA Account: $OANDA_ACCOUNT_ID"
echo "📍 Environment: $OANDA_ENV"
echo ""

python3 autonomous_decision_engine.py
