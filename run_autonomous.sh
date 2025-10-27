#!/bin/bash
# Wrapper to ensure autonomous engine runs with proper environment
# Prevents silent failures from missing credentials

cd /home/ing/RICK/RICK_LIVE_PROTOTYPE

# Export variables directly (bypass dotenv parsing issues)
export RICK_PIN=841921
export OANDA_ENV=practice
export OANDA_ACCOUNT_ID=101-001-31210531-002
export OANDA_API_TOKEN=1a45b898c57f609f329a0af8f2800e7e-6fcc25eef7c3f94ad79acff6d5f6bfaf
export OANDA_PRACTICE_ACCOUNT_ID=101-001-31210531-002
export OANDA_PRACTICE_TOKEN=1a45b898c57f609f329a0af8f2800e7e-6fcc25eef7c3f94ad79acff6d5f6bfaf
export MICRO_TRADING_MODE=true
export TRADING_ENVIRONMENT=practice
export DEFAULT_CAPITAL_USD=2000
export LOG_LEVEL=INFO
export TZ=UTC

# Start autonomous engine
echo "🤖 Starting Autonomous Decision Engine (v2)"
echo "======================================================================"
echo "Account: $OANDA_ACCOUNT_ID"
echo "Environment: $OANDA_ENV"
echo "Cycle: 30s | Monitoring for positions"
echo "======================================================================"
echo ""

exec python3 autonomous_decision_engine.py "$@"
