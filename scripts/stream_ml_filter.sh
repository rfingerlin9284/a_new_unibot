#!/usr/bin/env bash
# Stream ML trade-filter-related narration from logs/narration.jsonl
# Focus: TRADE_BLOCKED (guardian gates), HEDGE_ON/OFF (risk toggles), PACK_ROUTED (orchestrator)
# Falls back gracefully if jq is missing.

set -euo pipefail

cd "$(dirname "$0")/.."

LOG="logs/narration.jsonl"

echo "🔎 ML Filter Stream — focusing on TRADE_BLOCKED / HEDGE_ON / HEDGE_OFF / PACK_ROUTED"
echo "   Source: $LOG"

if [ ! -f "$LOG" ]; then
  echo "⏳ Waiting for $LOG to appear... (Ctrl+C to exit)"
  while [ ! -f "$LOG" ]; do sleep 1; done
fi

if command -v jq >/dev/null 2>&1; then
  tail -F "$LOG" \
    | jq -r 'select(.event=="TRADE_BLOCKED" or .event=="HEDGE_ON" or .event=="HEDGE_OFF" or .event=="PACK_ROUTED")
      | ("[" + (.ts // "-") + "] "
         + (.event // "-")
         + " sym=" + (.symbol // "-")
         + (if .pack then " pack=" + .pack else "" end)
         + (if .gate then " gate=" + .gate else "" end)
         + (if .details then " details=" + (try (.details|tostring) catch "{}") else "" end))'
else
  echo "⚠️  jq not found; showing raw lines filtered by grep"
  tail -F "$LOG" | grep -E "TRADE_BLOCKED|HEDGE_ON|HEDGE_OFF|PACK_ROUTED"
fi
