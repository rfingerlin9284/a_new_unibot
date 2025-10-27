# RICK Quick Start Guide

## 🎯 For Non-Coders: What You Need to Know

### Safety First
- **Trading is OFF by default** — The system starts in safe mode
- **PIN 841921** is required for any risky operations
- **Emergency stop**: Run task "RICK: Emergency STOP" or type `echo OFF > .upgrade_toggle`

---

## 📋 Common Tasks (VS Code)

### Check System Status
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "RICK: Quick Status"
4. ✅ Shows toggle state, document integrity, and recent activity

### Launch Dashboard UI
1. Run Task → "RICK: Start (Rick Coach)"
2. Opens dashboard on http://localhost:8501
3. View narration feed, P&L, and charter compliance

### Verify System Documents
1. Run Task → "RICK: Verify System Documents"
2. ✅ Shows OK if documents are unchanged
3. ❌ Shows FAIL if tampering detected

### View Ghost Trading Status
1. Run Task → "RBOTZILLA: View Ghost Trading Status"
2. Shows running processes and last 20 log lines
3. Safe mode — no real trades executed

---

## 🚀 Trading Mode Progression

### 1. Ghost Mode (SAFE)
- Uses real market data
- No actual trades placed
- Tests logic without risk
- **Command**: `./start_ghost_trading.sh` (requires PIN 841921)

### 2. Canary Mode (MINIMAL RISK)
- Tiny position sizes (≤0.1% risk)
- Only 1 position at a time
- Auto-halts on errors
- **Promotion**: Automatic after successful ghost run

### 3. Live Mode (FULL PRODUCTION)
- Real trading with real money
- All safety gates enforced
- Requires preflight check
- **Command**: `./activate_live_trading.sh` (requires PIN 841921)

---

## ⚠️ Safety Rules (Non-Negotiable)

### Always Enforced
- ✅ Risk-Reward ≥ 3.2 (no exceptions)
- ✅ Position size ≥ $15,000
- ✅ Max hold time ≤ 6 hours
- ✅ Daily halt at -5% loss
- ✅ Stop-loss on every trade

### Timeframes Allowed
- ✅ M15 (15 minutes)
- ✅ M30 (30 minutes)
- ✅ H1 (1 hour)
- ❌ M1, M5 (rejected — too fast)

---

## 📁 Important Files & Locations

### System Documents (IMMUTABLE)
```
.system/RICK_CHARTER_IMMUTABLE.md           — Trading rules
.system/PREPENDED_INSTRUCTIONS_IMMUTABLE.md — Agent protocol
.system/IMMUTABLE_SHA256SUMS.txt            — Integrity verification
```

### Logs (Monitor Activity)
```
pre_upgrade/headless/logs/narration.jsonl   — Human-readable events
pre_upgrade/headless/logs/pnl.jsonl         — P&L tracking
realistic_ghost_trading.log                 — Ghost trading activity
```

### Configuration
```
.upgrade_toggle                              — OFF = safe, ON = live trading
.env                                         — API credentials (0600 perms)
configs/thresholds.json                      — Trading thresholds
```

---

## 🔧 Troubleshooting

### "Cannot verify system documents"
1. Run: `cd .system && sha256sum -c IMMUTABLE_SHA256SUMS.txt`
2. If FAILED: Documents were modified (restore from git)

### "Ghost trading not starting"
1. Check: `tail -50 realistic_ghost_trading.log`
2. Verify: `.env` file has correct API credentials
3. Permissions: `chmod 0600 .env`

### "Dashboard won't load"
1. Check: Port 8501 is not already in use
2. Try: `pkill -f streamlit` then restart
3. Browser: Open http://localhost:8501

### "Emergency stop needed"
1. Run Task: "RICK: Emergency STOP (toggle OFF)"
2. Or terminal: `echo OFF > .upgrade_toggle`
3. Verify: Check `.upgrade_toggle` file shows "OFF"

---

## 📞 Key Commands (Terminal)

```bash
# Check system status
./scripts/ui_headless/status_all.sh

# Verify safety guardrails
./scripts/verify_guardrails.sh

# Pre-flight checks (before live)
./live_preflight_check.sh

# Emergency stop
echo OFF > .upgrade_toggle

# Run tests
pytest tests/wolf_packs -v
```

---

## 🎓 Learning Path

### Day 1: Understand the System
1. Read: `LIVE_TRADING_SAFETY_PROTOCOL.md`
2. Read: `.system/RICK_CHARTER_IMMUTABLE.md`
3. Run Task: "RICK: Quick Status"

### Day 2: Practice with Ghost Mode
1. Run: `./start_ghost_trading.sh`
2. Watch logs: `tail -f realistic_ghost_trading.log`
3. Review report: `cat ghost_trading_final_report.json`

### Day 3: Monitor Dashboard
1. Start dashboard: Run Task "RICK: Start (Rick Coach)"
2. Watch narration feed in browser
3. Understand charter compliance indicators

### Day 4+: Advanced Operations
1. Review test results: `pytest tests/wolf_packs -v`
2. Understand promotion gates (GS requirements)
3. Practice emergency procedures

---

## ✅ Daily Checklist (Before Trading)

- [ ] Run "RICK: Quick Status" — verify toggle is correct
- [ ] Run "RICK: Verify System Documents" — ensure integrity
- [ ] Check logs for errors: `tail -f realistic_ghost_trading.log`
- [ ] Confirm account balance is acceptable for risk
- [ ] Know how to execute emergency stop

---

## 🆘 Emergency Contacts

**System Failure**: Check `.system/` documents, restore from git if needed

**Trading Halt**: Emergency stop sets `.upgrade_toggle` to OFF automatically at -5% daily loss

**Data Integrity**: SHA256 checksums in `.system/IMMUTABLE_SHA256SUMS.txt` must match

---

## 📖 More Documentation

- **Full System Guide**: `.github/copilot-instructions.md`
- **Trading Charter**: `.system/RICK_CHARTER_IMMUTABLE.md`
- **Safety Protocol**: `LIVE_TRADING_SAFETY_PROTOCOL.md`
- **Ghost Trading**: `GHOST_TRADING_MODE_GUIDE.md`

---

**Last Updated**: October 3, 2025
**Version**: 1.0 (Immutable System)
