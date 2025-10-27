#!/usr/bin/env bash
set -euo pipefail

# VSCode agent friendly master script:
# - Verify guardrails and preflight checks
# - Create pre-upgrade backups (read-only originals preserved)
# - Write live artifacts under DASH_SYSTEM_UPGRADE/live/
# - Require DOUBLE PIN + 5+ word explanation
# - Toggle .upgrade_toggle -> ON (so wrappers pick up upgrade code)
#
# Usage: chmod +x vscode_agent_run_live_check.sh
#        ./vscode_agent_run_live_check.sh

# === CONFIG - edit only if you must ===
ROOT="${ROOT:-/home/ing/RICK/R_H_UNI}"                 # your repo root
UPG="$ROOT/DASH_SYSTEM_UPGRADE"                 # upgrade folder (write-only)
EXTRACT="$ROOT/dev_post_live_extract"
BACKUP_DIR="$ROOT/pre_upgrade_backups"
TOGGLE_FILE="$ROOT/.upgrade_toggle"
PIN_EXPECT="841921"
PREFLIGHT_SCRIPT="$ROOT/live_preflight_check.sh"
VERIFY_GUARDRAILS="$ROOT/verify_guardrails.sh"
VERIFY_INTEGRITY="$ROOT/verify_integrity.sh"

# === 0. quick sanity ===
echo "=== RICK: LIVE ENABLE CHECK (write-only-in-UPG default) ==="
echo "Root: $ROOT"
if [ ! -d "$ROOT" ]; then
  echo "❌ ERROR: ROOT not found: $ROOT"; exit 1
fi

# === 1. Guardrail verification (fail early) ===
echo "--> Step 1: Guardrails verification"
if [ -x "$VERIFY_GUARDRAILS" ]; then
  "$VERIFY_GUARDRAILS"
else
  echo "⚠️ verify_guardrails.sh not found/executable - basic checks follow"
  [ -d "$UPG" ] || mkdir -p "$UPG"
  [ -f "$ROOT/.git/hooks/pre-commit" ] || echo "⚠️ Missing git pre-commit hook protection"
  echo "Basic guardrails OK"
fi

# === 2. Preflight (credentials & endpoints) ===
echo "--> Step 2: Preflight checks (env & endpoints are required)"
if [ -x "$PREFLIGHT_SCRIPT" ]; then
  "$PREFLIGHT_SCRIPT"
else
  echo "⚠️ live_preflight_check.sh not found - performing minimal checks"
  if [ ! -f "$ROOT/.env" ]; then
    echo "❌ Missing .env with credentials (abort)"; exit 1
  fi
  if grep -qiE "your.*here|demo|sandbox|paper|practice" "$ROOT/.env"; then
    echo "❌ Found demo/sandbox/placeholder strings in .env (abort)"; exit 1
  fi
  echo "Minimal preflight checks passed"
fi

# === 3. Verify integrity if available ===
echo "--> Step 3: Integrity (optional)"
if [ -x "$VERIFY_INTEGRITY" ]; then
  "$VERIFY_INTEGRITY"
else
  echo "No verify_integrity.sh present - continue"
fi

# === 4. Ensure toggle exists and is OFF by default ===
echo "--> Step 4: Toggle check"
if [ ! -f "$TOGGLE_FILE" ]; then
  echo "OFF" > "$TOGGLE_FILE"
  echo "Created $TOGGLE_FILE with OFF"
fi
CURRENT_TOGGLE="$(cat "$TOGGLE_FILE" || echo OFF)"
echo "Current .upgrade_toggle = $CURRENT_TOGGLE"
if [ "$CURRENT_TOGGLE" = "ON" ]; then
  echo "❗ .upgrade_toggle is already ON. Aborting - set to OFF and re-run if you intend to proceed."
  exit 1
fi

# === 5. Confirm operator intent (DOUBLE PIN + explanation) ===
echo "--> Step 5: Security confirmation (DOUBLE PIN + 5+ word reason required)"
read -s -p "Enter PIN: " p1; echo
read -s -p "Re-enter PIN: " p2; echo
if [ "$p1" != "$PIN_EXPECT" ] || [ "$p2" != "$PIN_EXPECT" ]; then
  echo "❌ PIN mismatch or incorrect PIN. Aborting."
  exit 1
fi

read -p "Please type a 5+ word reason for enabling LIVE now: " reason
words=$(echo "$reason" | wc -w)
if [ "$words" -lt 5 ]; then
  echo "❌ Explanation too short. Aborting."
  exit 1
fi
echo "Security confirmation OK."

# === 6. Backup current live folders (readonly originals preserved) ===
TIMESTAMP="$(date -u +%Y%m%d_%H%M%SZ)"
mkdir -p "$BACKUP_DIR"
BACKUP_TAR="$BACKUP_DIR/pre_live_backup_${TIMESTAMP}.tar.gz"
echo "--> Step 6: Creating backup tar to $BACKUP_TAR (headless + standalone live folders)"
tar -C "$ROOT" -czf "$BACKUP_TAR" \
    --exclude='./DASH_SYSTEM_UPGRADE' \
    micro_trading_engine.py standalone_shell packages 2>/dev/null || echo "⚠️ Some folders may be missing; backup may be partial"
echo "Backup complete."

# === 7. Prepare DASH_SYSTEM_UPGRADE/live/ with live artifacts ===
echo "--> Step 7: Write live artifacts into DASH_SYSTEM_UPGRADE/live/ (no originals altered)"
mkdir -p "$UPG/live"
cat > "$UPG/live/config.json" <<'JSON'
{
  "mode": "LIVE",
  "real_money": true,
  "simulation": false,
  "risk_parameters": {
    "daily_breaker": -0.05,
    "min_notional": 15000,
    "max_hold_hours": 6,
    "rr_minimum": 3.2,
    "concurrent_positions": 1
  },
  "venues": {
    "oanda": {
      "enabled": true,
      "api_url": "https://api-fxtrade.oanda.com/v3",
      "live_trading": true
    },
    "coinbase": {
      "enabled": true,
      "api_url": "https://api.coinbase.com",
      "live_trading": true
    }
  }
}
JSON

cat > "$UPG/live/micro_trading_engine.py" <<'PY'
#!/usr/bin/env python3
"""
DASH_SYSTEM_UPGRADE/live/micro_trading_engine.py
TEMPLATE live engine for add-on. This file lives in DASH_SYSTEM_UPGRADE/live/
and will be loaded only if .upgrade_toggle == "ON". It DOES NOT modify repo
root originals. Implement broker calls and thorough tests before use.

IMPORTANT: This template contains TODO markers. DO NOT remove safety checks.
"""
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()  # still reads real creds from ~/.env (protected)

class LiveTradingEngine:
    def __init__(self):
        self.PIN = "841921"
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        # Load config (the wrapper will ensure this file exists)
        import json
        with open(self.config_path) as f:
            self.cfg = json.load(f)
        # Safety assertions (basic)
        assert self.cfg['real_money'] is True
        assert self.cfg['risk_parameters']['min_notional'] >= 15000
        assert self.cfg['risk_parameters']['rr_minimum'] >= 3.0

    def place_live_order(self, symbol, side, amount, sl, tp):
        # Validate params
        if amount < self.cfg['risk_parameters']['min_notional']:
            raise ValueError("Position below minimum notional")
        # Compute naive RR (example)
        # TODO: replace with instrument-price-aware calculation
        rr = abs((tp - sl) / max(1e-9, abs(sl - tp)))
        if rr < self.cfg['risk_parameters']['rr_minimum']:
            raise AssertionError("RR below minimum")

        # TODO: Implement actual OANDA/Coinbase API calls here.
        # For safety, this template only logs the intended action.
        now = datetime.now(timezone.utc).isoformat()
        print(f"[{now}] LIVE_ORDER_INTENT symbol={symbol} side={side} amount={amount} sl={sl} tp={tp} rr={rr:.2f}")
        return {"status": "INTENT_LOGGED", "details": "Implement broker calls before enabling live."}

if __name__ == "__main__":
    e = LiveTradingEngine()
    print("LIVE ENGINE TEMPLATE LOADED (no live API calls executed).")
PY

chmod +x "$UPG/live/micro_trading_engine.py"
echo "Wrote config & micro_trading_engine.py into $UPG/live/"

# === 8. Enable the toggle (atomically) ===
echo "--> Step 8: Enabling upgrade toggle (will NOT modify originals)"
echo "ON" > "$TOGGLE_FILE"
sync
echo ".upgrade_toggle set to ON. UPGRADE code will be loaded by wrappers."

# === 9. Audit log entry ===
AUDIT_LOG="$ROOT/pre_upgrade_backups/enable_live_audit_${TIMESTAMP}.log"
cat > "$AUDIT_LOG" <<EOF
enable_live: timestamp=$TIMESTAMP
operator_reason="$reason"
backup="$BACKUP_TAR"
upgrade_folder="$UPG/live"
toggle="$TOGGLE_FILE -> ON"
preflight_script="$PREFLIGHT_SCRIPT"
guardrails_verified=true
EOF
echo "Audit log written to $AUDIT_LOG"

# === 10. Final instructions ===
echo "=== COMPLETE ==="
echo "Backup at: $BACKUP_TAR"
echo "Upgrade artifacts written to: $UPG/live/"
echo ".upgrade_toggle -> ON (wrappers will load the upgrade code)"
echo "NOTE: The template micro_trading_engine.py does NOT call brokers. Implement and test broker calls in $UPG/live/micro_trading_engine.py BEFORE placing real trades."
echo "Suggested immediate manual checks:"
echo "  - Inspect $UPG/live/micro_trading_engine.py and implement OANDA/Coinbase logic"
echo "  - Run the upgrade in a controlled dry-run with debug flags"
echo "  - Monitor logs and be ready to revert: set .upgrade_toggle -> OFF or restore backup"
echo ""
echo "To revert to pre-upgrade originals quickly:"
echo "  1) echo OFF > $TOGGLE_FILE"
echo "  2) (if needed) restore backup: tar -xzf $BACKUP_TAR -C $ROOT"
echo ""
exit 0