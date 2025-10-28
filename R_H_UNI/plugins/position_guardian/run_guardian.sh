#!/usr/bin/env bash
set -euo pipefail
BASE="/home/ing/RICK/R_H_UNI"
ENVF="$BASE/.env"

# Extract OANDA practice credentials
if [[ -f "$ENVF" ]]; then
  export OANDA_API_KEY=$(grep "^OANDA_PRACTICE_TOKEN=" "$ENVF" | cut -d'=' -f2- || echo "")
  export OANDA_ACCOUNT_ID=$(grep "^OANDA_PRACTICE_ACCOUNT_ID=" "$ENVF" | cut -d'=' -f2- || echo "")
  export OANDA_ENV="practice"
  export OANDA_API_URL=$(grep "^OANDA_PRACTICE_BASE_URL=" "$ENVF" | cut -d'=' -f2- || echo "https://api-fxpractice.oanda.com/v3")
fi

# Verify required env vars
if [[ -z "$OANDA_API_KEY" ]] || [[ -z "$OANDA_ACCOUNT_ID" ]]; then
  echo "ERROR: Missing OANDA_PRACTICE_TOKEN or OANDA_PRACTICE_ACCOUNT_ID in $ENVF"
  exit 1
fi

cd "$BASE/plugins/position_guardian"
exec python3 -u "$BASE/plugins/position_guardian/guardian_daemon.py" --live --loop 30
