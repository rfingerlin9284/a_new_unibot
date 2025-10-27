#!/usr/bin/env bash
set -euo pipefail
ROOT="${ROOT:-/home/ing/RICK/R_H_UNI}"

echo "=== RICK LIVE LAUNCH QUICKCHECK ==="

echo "[1] Confirm .upgrade_toggle is OFF (default):"
cat "$ROOT/.upgrade_toggle" 2>/dev/null || echo "OFF (not present)"

echo "[2] Run guardrails (if exist):"
[ -x "$ROOT/verify_guardrails.sh" ] && bash "$ROOT/verify_guardrails.sh" || echo "verify_guardrails.sh missing - skip"

echo "[3] Run preflight (env & endpoints):"
[ -x "$ROOT/live_preflight_check.sh" ] && bash "$ROOT/live_preflight_check.sh" || echo "live_preflight_check.sh missing - skip"

echo "[4] OPTIONAL: Run integrity check (if present):"
[ -x "$ROOT/verify_integrity.sh" ] && bash "$ROOT/verify_integrity.sh" || echo "verify_integrity.sh missing - skip"

echo "[5] When ready, run: ./vscode_agent_run_live_check.sh (interactive PIN + 5+ word reason required)"
echo "[6] After enabling, verify audit log in pre_upgrade_backups/"
echo ""
echo "Manual checks BEFORE first live trade:"
echo "- Confirm account balances & permission scopes in broker accounts"
echo "- Confirm OCO is supported and SLs are set on sample trade"
echo "- Choose operator to watch 1st trade; be ready to echo OFF > $ROOT/.upgrade_toggle"
echo ""
echo "To abort at any time: echo OFF > $ROOT/.upgrade_toggle"