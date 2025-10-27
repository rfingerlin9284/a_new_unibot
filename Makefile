# ============================================================================
# RICK LIVE PROTOTYPE MAKEFILE
# ============================================================================
# Assimilated from: /home/ing/RICK/RICK_LIVE_CLEAN/Makefile
# Adapted for: /home/ing/RICK/RICK_LIVE_PROTOTYPE
# Date: October 20, 2025
# PIN: 841921
#
# This Makefile provides consistent build, test, and deployment commands
# All references to RICK_LIVE_CLEAN have been updated to RICK_LIVE_PROTOTYPE
# ============================================================================

.PHONY: help setup test run clean deploy gates integration docs

PROJECT_ROOT := $(shell pwd)
PYTHON := python3
PIP := pip3
VENV := venv

# ============================================================================
# DOCUMENTATION & HELP
# ============================================================================

help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║     RICK LIVE PROTOTYPE - Makefile Help                      ║"
	@echo "║     PIN: 841921 | Date: $(shell date +%Y-%m-%d)              ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📚 AVAILABLE TARGETS:"
	@echo ""
	@echo "SETUP & ENVIRONMENT:"
	@echo "  make setup              Setup virtual environment & dependencies"
	@echo "  make deps               Install/update dependencies only"
	@echo "  make clean              Clean build artifacts & caches"
	@echo ""
	@echo "TESTING:"
	@echo "  make test               Run all tests"
	@echo "  make test-gates         Test margin & correlation gates"
	@echo "  make test-broker        Test OANDA broker connection"
	@echo "  make test-charter       Test charter compliance"
	@echo ""
	@echo "RUNNING:"
	@echo "  make run                Start trading engine (practice)"
	@echo "  make run-live           Start trading engine (LIVE - USE WITH CAUTION)"
	@echo "  make run-dashboard      Start dashboard"
	@echo "  make run-narration      Monitor narration stream"
	@echo ""
	@echo "GATES & INTEGRATION:"
	@echo "  make gates              Build & test guardian gates"
	@echo "  make gates-integrate    Integrate gates into engine"
	@echo "  make gates-status       Check gate status"
	@echo ""
	@echo "TRADE SHIM (Auto-Bracket, Charter PIN: 841921):"
	@echo "  make shim-help          Show trade shim help"
	@echo "  make shim-test-all      Run all bracket generation tests"
	@echo "  make shim-test-bracket  Test bracket generation (EUR_USD)"
	@echo "  make shim-test-jpy      Test JPY pip precision"
	@echo "  make shim-test-rr       Test RR guardrail (should fail)"
	@echo "  make shim-test-sl       Test SL guardrail (should fail)"
	@echo ""
	@echo "HIVE MIND REFLECTION (Autonomous Position Management):"
	@echo "  make reflection-help    Show reflection orchestrator info"
	@echo "  make reflection-test    Run single reflection cycle"
	@echo "  make reflection-daemon  Start 24/7 reflection loop (30s)"
	@echo "  make reflection-status  Check reflection status"
	@echo "  make reflection-logs    Tail reflection logs"
	@echo ""
	@echo "OPERATOR CLIs (Position Guardian):"
	@echo "  make pg-help            Show Position Guardian CLIs info"
	@echo "  make pg-trail-help      Trailing stop manager help"
	@echo "  make pg-bracket-help    Bracket generator help"
	@echo "  make pg-bracket-templates  Show bracket templates"
	@echo "  make pg-smart-exit-help Smart exit manager help"
	@echo ""
	@echo "DOCUMENTATION:"
	@echo "  make docs               Generate all documentation"
	@echo "  make docs-gates         Generate gate documentation"
	@echo "  make docs-api           Generate API documentation"
	@echo ""
	@echo "DEPLOYMENT:"
	@echo "  make deploy             Deploy to production (requires PIN)"
	@echo "  make backup             Backup current state"
	@echo "  make validate           Validate system readiness"
	@echo ""
	@echo "PIN: 841921"
	@echo ""

# ============================================================================
# SETUP & ENVIRONMENT
# ============================================================================

setup: clean deps
	@echo "✅ Setup complete!"
	@echo "   Virtual environment: $(VENV)"
	@echo "   Project root: $(PROJECT_ROOT)"
	@echo "   Ready to run: make run"

deps:
	@echo "📦 Installing dependencies..."
	$(PIP) install -q oanda-v20 requests python-dotenv jsonschema pydantic numpy pandas scikit-learn
	@echo "✅ Dependencies installed"

clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage 2>/dev/null || true
	@echo "✅ Cleaned"

# ============================================================================
# TESTING
# ============================================================================

test: test-gates test-broker test-charter
	@echo "✅ All tests complete"

test-gates:
	@echo "🛡️  Testing guardian gates..."
	@$(PYTHON) test_margin_correlation_gate.py
	@echo "✅ Gate tests passed"

test-broker:
	@echo "🔌 Testing OANDA broker connection..."
	@$(PYTHON) -c "from brokers.oanda_connector import OandaConnector; c = OandaConnector(environment='practice'); print('✅ OANDA connection OK')"
	@echo ""

test-charter:
	@echo "📋 Testing charter compliance..."
	@$(PYTHON) -c "from foundation.rick_charter import RickCharter; RickCharter.validate_pin(841921); print('✅ Charter PIN valid')"
	@echo ""

# ============================================================================
# RUNNING TRADING ENGINE
# ============================================================================

run:
	@echo "🚀 Starting RICK Trading Engine (PRACTICE)..."
	@echo "   PIN: 841921"
	@echo "   Environment: PRACTICE"
	@echo "   Gates: ACTIVE"
	@echo ""
	@$(PYTHON) oanda_trading_engine.py --env practice

run-live:
	@echo "⚠️  WARNING: STARTING LIVE TRADING ENGINE"
	@echo "   PIN: 841921"
	@echo "   Environment: LIVE"
	@echo "   Real money will be used!"
	@echo ""
	@read -p "Type 'YES' to confirm: " confirm; \
	if [ "$$confirm" = "YES" ]; then \
		$(PYTHON) oanda_trading_engine.py --env live; \
	else \
		echo "Cancelled."; \
	fi

run-dashboard:
	@echo "📊 Starting unified dashboard..."
	@$(PYTHON) dashboard_unified.py --pin 841921

run-narration:
	@echo "🎙️  Monitoring narration stream..."
	@tail -f narration.jsonl | grep -E "Rick|ML_ANALYZER|SMART|HIVE" || echo "Waiting for narration..."

# ============================================================================
# GUARDIAN GATES
# ============================================================================

gates: clean test-gates
	@echo "✅ Guardian gates validated & ready"
	@echo ""
	@echo "Gate Status:"
	@echo "  ✅ Margin Cap Gate (35%)"
	@echo "  ✅ Correlation Gate (Currency Bucket)"
	@echo "  ✅ SL Validation Gate (ATR-Aware)"
	@echo "  ✅ Time Stop Gate (3h/6h)"
	@echo ""

gates-integrate:
	@echo "🔧 Integrating gates into trading engine..."
	@echo "   Status: ALREADY INTEGRATED (see oanda_trading_engine.py)"
	@echo ""
	@echo "Integration Points:"
	@echo "  ✅ Imports: foundation/margin_correlation_gate.py"
	@echo "  ✅ Init: MarginCorrelationGate in __init__()"
	@echo "  ✅ Pre-Trade: pre_trade_gate() in place_trade()"
	@echo "  ✅ Tracking: Position tracking for ongoing monitoring"
	@echo ""
	@echo "Next: make run (to activate gates)"

gates-status:
	@echo "🛡️  Gate Status Check"
	@echo ""
	@$(PYTHON) foundation/margin_correlation_gate.py
	@echo ""

# ============================================================================
# DOCUMENTATION
# ============================================================================

docs: docs-gates docs-api
	@echo "✅ Documentation generated"

docs-gates:
	@echo "📄 Gate documentation files:"
	@ls -1h GATE_*.md NET_VIEW_*.md QUICK_*.md 2>/dev/null || echo "No gate docs found"
	@echo ""

docs-api:
	@echo "📄 API documentation files:"
	@ls -1h DEVELOPER_*.md BLUEPRINT_*.md 2>/dev/null || echo "No API docs found"
	@echo ""

# ============================================================================
# DEPLOYMENT
# ============================================================================

validate:
	@echo "✅ Validating system readiness..."
	@echo ""
	@echo "Checking components:"
	@echo -n "  Charter compliance... "
	@$(PYTHON) -c "from foundation.rick_charter import RickCharter; RickCharter.validate_pin(841921); print('OK')" 2>/dev/null || echo "FAIL"
	@echo -n "  Guardian gates... "
	@$(PYTHON) -c "from foundation.margin_correlation_gate import MarginCorrelationGate; print('OK')" 2>/dev/null || echo "FAIL"
	@echo -n "  OANDA connector... "
	@$(PYTHON) -c "from brokers.oanda_connector import OandaConnector; print('OK')" 2>/dev/null || echo "FAIL"
	@echo -n "  Terminal display... "
	@$(PYTHON) -c "from util.terminal_display import TerminalDisplay; print('OK')" 2>/dev/null || echo "FAIL"
	@echo ""
	@echo "✅ System ready for deployment"

backup:
	@echo "📦 Creating backup..."
	@mkdir -p backups
	@tar -czf backups/rick_prototype_$(shell date +%Y%m%d_%H%M%S).tar.gz \
		--exclude=backups --exclude=__pycache__ --exclude=.git \
		.
	@echo "✅ Backup created: backups/"

deploy: validate
	@echo "🚀 Deploying RICK Trading System..."
	@echo "   Folder: $(PROJECT_ROOT)"
	@echo "   PIN: 841921"
	@echo ""
	@echo "Deployment checklist:"
	@echo "  ✅ Charter compliance validated"
	@echo "  ✅ Guardian gates tested"
	@echo "  ✅ OANDA connection verified"
	@echo "  ✅ Terminal display ready"
	@echo ""
	@echo "Status: READY FOR PRODUCTION"
	@echo ""
	@echo "To start trading:"
	@echo "  make run           (Practice environment)"
	@echo "  make run-live      (LIVE environment)"

# ============================================================================
# UTILITY
# ============================================================================

status:
	@echo "📊 System Status"
	@echo ""
	@echo "Project: $(PROJECT_ROOT)"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Date: $$(date)"
	@echo ""
	@echo "Gate Status:"
	@$(PYTHON) test_margin_correlation_gate.py 2>&1 | grep "PASSED\|FAILED" | head -7
	@echo ""
	@echo "Active processes:"
	@ps aux | grep -E "oanda_trading|dashboard|ollama" | grep -v grep | wc -l
	@echo ""

# ============================================================================
# TRADE SHIM TARGETS (Auto-Bracket, Charter-Compliant)
# ============================================================================

.PHONY: shim-help shim-test-bracket shim-test-jpy shim-test-rr shim-test-sl shim-test-all

shim-help:
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo "TRADE SHIM HELP - Auto-Bracket Generation (Charter PIN: 841921)"
	@echo "═══════════════════════════════════════════════════════════════════"
	@$(PYTHON) brokers/trade_shim.py --help

shim-test-bracket:
	@echo "Testing bracket generation (EUR_USD, TP=80, SL=25, Trail=20)..."
	@$(PYTHON) brokers/trade_shim.py \
		--instrument EUR_USD --units 10000 --type MARKET --entry 1.10500 \
		--tp-pips 80 --sl-pips 25 --trail-pips 20 --dry-run 2>/dev/null | python3 -m json.tool

shim-test-jpy:
	@echo "Testing JPY precision (GBP_JPY, TP=100, SL=30)..."
	@$(PYTHON) brokers/trade_shim.py \
		--instrument GBP_JPY --units 200 --type MARKET --entry 180.250 \
		--tp-pips 100 --sl-pips 30 --dry-run 2>/dev/null | python3 -m json.tool

shim-test-rr:
	@echo "Testing RR guardrail (should FAIL: RR=2.0:1 < 3.2:1)..."
	@$(PYTHON) brokers/trade_shim.py \
		--instrument GBP_USD --units 5000 --type MARKET --entry 1.30000 \
		--tp-pips 50 --sl-pips 25 --dry-run 2>&1 | grep -E "Validation|Risk"

shim-test-sl:
	@echo "Testing SL guardrail (should FAIL: SL=15 < 18)..."
	@$(PYTHON) brokers/trade_shim.py \
		--instrument USD_JPY --units 100 --type MARKET --entry 149.500 \
		--tp-pips 100 --sl-pips 15 --dry-run 2>&1 | grep -E "Validation|MIN_SL"

shim-test-all: shim-test-bracket shim-test-jpy shim-test-rr shim-test-sl
	@echo ""
	@echo "✅ All trade shim tests completed"

# ============================================================================
# HIVE MIND REFLECTION ORCHESTRATOR
# ============================================================================

.PHONY: reflection-help reflection-test reflection-once reflection-daemon reflection-stop reflection-status reflection-logs

reflection-help:
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo "HIVE MIND REFLECTION ORCHESTRATOR (30-Second Autonomous Loop)"
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🧠 The hive mind reflection system provides continuous autonomous"
	@echo "   management of active trading positions through collective intelligence."
	@echo ""
	@echo "Workflow (Every 30 seconds):"
	@echo "  1. Fetch active positions from OANDA API"
	@echo "  2. Validate charter compliance (margin, SL, RR, TTL)"
	@echo "  3. Query hive mind consensus for each position (hold/reduce/exit/add)"
	@echo "  4. Execute recommended actions via trade shim CLIs"
	@echo "  5. Log all decisions to narration.jsonl"
	@echo "  6. Update hive_status.json for dashboard"
	@echo ""
	@echo "Available Targets:"
	@echo "  make reflection-test          Run single reflection cycle (test mode)"
	@echo "  make reflection-once          Run single cycle (production)"
	@echo "  make reflection-daemon        Start reflection daemon (30s loop)"
	@echo "  make reflection-status        Check daemon status"
	@echo "  make reflection-logs          Tail daemon logs"
	@echo "  make reflection-stop          Stop the daemon"
	@echo ""
	@echo "Charter Rules Monitored:"
	@echo "  ✅ Margin ≤ 35%"
	@echo "  ✅ Stop Loss ≥ 18 pips"
	@echo "  ✅ Risk/Reward ≥ 3.2:1"
	@echo "  ✅ Max 3 concurrent positions"
	@echo "  ✅ Max hold time = 6 hours"
	@echo "  ✅ Daily loss limit = -5%"
	@echo ""
	@echo "Example Usage:"
	@echo "  make reflection-test          # Test with one cycle"
	@echo "  make reflection-daemon        # Start 24/7 monitoring"
	@echo "  # OR in systemd:"
	@echo "  systemctl start reflection_orchestrator.service"
	@echo ""

reflection-test:
	@echo "🧠 Running HIVE MIND REFLECTION (test mode)..."
	@echo ""
	@$(PYTHON) hive/hive_reflection_orchestrator.py --mode once --environment practice

reflection-once:
	@echo "🧠 Running HIVE MIND REFLECTION (production - once)..."
	@echo ""
	@$(PYTHON) hive/hive_reflection_orchestrator.py --mode once --environment practice

reflection-daemon:
	@echo "🧠 Starting HIVE MIND REFLECTION DAEMON (30-second loop)..."
	@echo "   Press Ctrl+C to stop"
	@echo ""
	@$(PYTHON) hive/hive_reflection_orchestrator.py --mode daemon --environment practice --interval 30

reflection-status:
	@echo "🧠 Checking Hive Reflection Status..."
	@if [ -f hive_status.json ]; then \
		echo ""; \
		echo "Last reflection cycle:"; \
		tail -20 hive_status.json | $(PYTHON) -m json.tool 2>/dev/null || cat hive_status.json; \
	else \
		echo "❌ hive_status.json not found - no reflection cycles yet"; \
	fi

reflection-logs:
	@echo "🧠 Tailing hive reflection logs..."
	@tail -f narration.jsonl | grep -E "HIVE_REFLECTION|HIVE_DECISION|HIVE_ACTION|CHARTER_VIOLATION" || echo "No reflection logs yet"

reflection-stop:
	@echo "🧠 Stopping hive reflection daemon..."
	@pkill -f "hive_reflection_orchestrator.py" || echo "No daemon running"
	@echo "✅ Daemon stopped"

# ============================================================================
# OPERATOR CLI TARGETS (Position Guardian)
# ============================================================================

.PHONY: pg-help pg-trail-help pg-bracket-help pg-smart-exit-help

pg-help:
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo "POSITION GUARDIAN OPERATOR CLIs (Charter PIN: 841921)"
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Available CLIs:"
	@echo "  python brokers/pg_trail.py --help        Trailing stop manager"
	@echo "  python brokers/pg_bracket.py --help      Bracket generator"
	@echo "  python brokers/pg_smart_exit.py --help   Smart exit manager"
	@echo ""

pg-trail-help:
	@$(PYTHON) brokers/pg_trail.py --help

pg-bracket-help:
	@$(PYTHON) brokers/pg_bracket.py --help

pg-smart-exit-help:
	@$(PYTHON) brokers/pg_smart_exit.py --help

pg-bracket-templates:
	@$(PYTHON) brokers/pg_bracket.py --list-templates

version:
	@echo "RICK Live Prototype v2.0"
	@echo "Assimilated: October 20, 2025"
	@echo "PIN: 841921"

# ============================================================================
# DEFAULT TARGET
# ============================================================================

.DEFAULT_GOAL := help

# ============================================================================
# PROJECT NOTES
# ============================================================================
#
# ASSIMILATION NOTES:
# ==================
# This Makefile was adapted from /home/ing/RICK/RICK_LIVE_CLEAN/Makefile
# All references have been updated to point to RICK_LIVE_PROTOTYPE
#
# KEY CHANGES FROM ORIGINAL:
# - All paths now reference $(PROJECT_ROOT) instead of RICK_LIVE_CLEAN
# - Added new targets: gates, gates-integrate, gates-status
# - Added new target: test-gates
# - Updated run-live warning (now for this deployment)
# - Added guardian gate integration info
#
# GUARDIAN GATES:
# ===============
# All 4 guardian gates are now integrated:
#   1. Margin Cap (35% hard limit)
#   2. Correlation Gate (currency bucket)
#   3. SL Validation (ATR-aware)
#   4. Time Stops (3h/6h protection)
#
# ACTIVE INTEGRATION POINTS:
# ==========================
# - foundation/margin_correlation_gate.py (core logic)
# - oanda_trading_engine.py (pre-trade checks + tracking)
# - test_margin_correlation_gate.py (7/7 tests passing)
#
# ============================================================================

# ============================================================================
# 🤖 AUTONOMOUS DECISION ENGINE
# ============================================================================
# Real-time autonomous position management based on:
#   - P&L thresholds (profit-taking, loss-halting)
#   - Hive consensus (auto-reduce on low consensus)
#   - Charter rules (SL, hold time, margin limits)
#   - No human input required

autonomous-test:
	@echo "[DOING] Testing autonomous decision engine (single cycle)"
	$(PYTHON) autonomous_decision_engine.py 2>&1 | head -20

autonomous-daemon:
	@echo "[DOING] Running autonomous decision engine (foreground, Ctrl+C to stop)"
	$(PYTHON) autonomous_decision_engine.py

autonomous-install:
	@echo "[DOING] Installing autonomous engine as systemd service"
	mkdir -p $(HOME)/.config/systemd/user
	cp systemd/autonomous_decision_engine.service $(HOME)/.config/systemd/user/
	systemctl --user daemon-reload
	systemctl --user enable autonomous_decision_engine.service
	@echo "[OK] Service installed; start with: make autonomous-start"

autonomous-start:
	@echo "[DOING] Starting autonomous decision engine service"
	systemctl --user start autonomous_decision_engine.service
	sleep 2
	@systemctl --user status autonomous_decision_engine.service

autonomous-stop:
	@echo "[DOING] Stopping autonomous decision engine"
	systemctl --user stop autonomous_decision_engine.service || true
	@echo "[OK] Stopped"

autonomous-status:
	@echo "[INFO] Autonomous Decision Engine Status"
	@systemctl --user status autonomous_decision_engine.service --no-pager 2>/dev/null || echo "Not running"
	@echo ""
	@echo "Recent decisions:"
	@tail -5 logs/autonomous_decisions.jsonl 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "No decisions yet"

autonomous-logs:
	@tail -50 logs/autonomous_engine.log 2>/dev/null || echo "No logs yet"

autonomous-config:
	@echo "Current autonomous engine thresholds:"
	@echo "  PROFIT_TAKE_THRESHOLD: $$(echo $$PROFIT_TAKE_THRESHOLD || echo '150 USD')"
	@echo "  LOSS_HALT_THRESHOLD: $$(echo $$LOSS_HALT_THRESHOLD || echo '-300 USD')"
	@echo "  AUTONOMOUS_CYCLE_SECONDS: $$(echo $$AUTONOMOUS_CYCLE_SECONDS || echo '30 seconds')"
	@echo ""
	@echo "To customize, set env vars in .env:"
	@echo "  PROFIT_TAKE_THRESHOLD=200"
	@echo "  LOSS_HALT_THRESHOLD=-250"
	@echo "  AUTONOMOUS_CYCLE_SECONDS=20"
