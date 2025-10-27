# 📘 RICK AUTONOMOUS TRADING SYSTEM - MASTER MANUAL
**Version:** 2.0 Production  
**Date:** October 20, 2025  
**PIN:** 841921 ✅  
**System:** RICK_LIVE_PROTOTYPE

---

## 📋 TABLE OF CONTENTS

1. [Executive Overview](#1-executive-overview)
2. [System Architecture](#2-system-architecture)
3. [Quick Start Guide](#3-quick-start-guide)
4. [Installation & Setup](#4-installation--setup)
5. [Operations & Control](#5-operations--control)
6. [Protection & Security](#6-protection--security)
7. [Troubleshooting](#7-troubleshooting)
8. [API Reference](#8-api-reference)
9. [Port & Service Allocation](#9-port--service-allocation)
10. [Appendices](#10-appendices)

---

# 1. EXECUTIVE OVERVIEW

## 1.1 System Purpose

**RICK** is a fully autonomous forex trading system designed for paper and live trading via the OANDA REST v20 API. The system combines:

- **5 Trading Strategies** with multi-signal voting
- **Guardian Gate System** (10 autopilot rules)
- **Quantitative Hedge Engine** (7-rule correlation-based)
- **ML Intelligence** (regime detection, signal analysis)
- **Hive Mind** consensus engine
- **Rick LLM Narration** (optional Ollama integration)
- **Charter-Based Constraints** (PIN-locked immutability)

## 1.2 Key Features

✅ **Fully Autonomous:** No human intervention required  
✅ **Multi-Layer Protection:** Charter + PIN + Gates + Audit Trail  
✅ **Real-Time Monitoring:** 3-pane tmux dashboard  
✅ **State Persistence:** Automatic recovery after reboot  
✅ **100% Gated Trading:** Every decision passes 4-gate validation  
✅ **Event Logging:** Append-only audit trail (narration.jsonl)  
✅ **Multi-Agent Safe:** Port-isolated, no conflicts  

## 1.3 System Status

**Current Configuration:**
- OANDA Account: Practice (101-001-31210531-002)
- Account Balance: $1,898.48 USD
- Charter PIN: 841921 ✅ VALIDATED
- Trading Mode: Paper Trading (Practice API)
- Status: ✅ OPERATIONAL

**Core Components:**
- Trading Engine: ✅ READY
- Guardian Gates: ✅ ACTIVE (10 rules)
- Hedge Engine: ✅ ACTIVE (7 rules)
- Strategy Aggregator: ✅ ACTIVE (5 strategies)
- Dashboard: ✅ READY (3-pane tmux)
- Verification Suite: ✅ 27/27 checks passing

## 1.4 Charter Constraints (IMMUTABLE)

These values are **hardcoded** and **cannot be overridden**:

```
PIN:                841921 (required for init)
MIN_NOTIONAL_USD:   $15,000 (minimum trade size)
MIN_RR_RATIO:       3.2:1 (minimum risk:reward)
MAX_HOLD_DURATION:  6 hours (maximum position hold)
MAX_CONCURRENT:     3 positions (maximum open at once)
MAX_MARGIN:         35% (maximum margin utilization)
DAILY_LOSS_BREAKER: -5% (circuit breaker threshold)
CHART_VERSION:      2.0_IMMUTABLE
```

**Protection Level:** 🔒 PIN-LOCKED + HARDCODED + GATE-ENFORCED

---

# 2. SYSTEM ARCHITECTURE

## 2.1 Visual Overview

See: `SYSTEM_ARCHITECTURE.png` (300 dpi, 7-layer visualization)

**Architecture Layers:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 7: ORCHESTRATION (Startup, Verification, Control)        │
├─────────────────────────────────────────────────────────────────┤
│ Layer 6: STATE PERSISTENCE (Position, Events, Backups)         │
├─────────────────────────────────────────────────────────────────┤
│ Layer 5: CORE TRADING ENGINE (Order Execution, Logging)        │
├─────────────────────────────────────────────────────────────────┤
│ Layer 4: GUARDIAN GATES (Charter, Margin, Correlation, RR)     │
├─────────────────────────────────────────────────────────────────┤
│ Layer 3: DECISION AGGREGATION (Hive Mind, Trade Logic)         │
├─────────────────────────────────────────────────────────────────┤
│ Layer 2: ANALYSIS ENGINES (ML, Strategy, Momentum, Hedge)      │
├─────────────────────────────────────────────────────────────────┤
│ Layer 1: INPUT SOURCES (OANDA API, Market Data, Correlation)   │
└─────────────────────────────────────────────────────────────────┘
```

## 2.2 Data Flow

```
OANDA API (real-time pricing)
  ↓
ML Regime Detection (trending/ranging filter)
  ↓
5 Trading Strategies (parallel signal generation)
  ↓
Strategy Aggregator (2/5 vote threshold)
  ↓
Hive Mind Consensus (≥70% confidence boost)
  ↓
Trade Decision Logic
  ↓
4-Gate Validation (Charter + Margin + Correlation + RR)
  ↓
Order Execution (OANDA API)
  ↓
Hedge Analysis (7-rule correlation-based)
  ↓
Position Guardian (10 autopilot rules)
  ↓
Event Logging (narration.jsonl append-only)
  ↓
Dashboard Display (3-pane tmux real-time)
```

## 2.3 Component Map

### Core Trading (`/home/ing/RICK/RICK_LIVE_PROTOTYPE/`)

```
oanda_trading_engine.py         Main trading engine (62 KB)
├── Initialization (PIN 841921)
├── OANDA API connection
├── Strategy aggregator integration
├── ML regime detection
├── Hive Mind consensus
├── 4-gate pre-trade validation
├── Order execution
├── Hedge decision engine
├── Position guardian integration
└── Event logging

canary_trading_engine.py        Canary (test) engine
oanda_paper_trading.py          Paper trading wrapper
ghost_trading_engine.py         Ghost (shadow) engine
autonomous_decision_engine.py   Monitor/decision logger
```

### Foundation (`foundation/`)

```
rick_charter.py                 Immutable Charter constants
├── PIN validation (841921)
├── Hardcoded constraints
├── Charter enforcement methods
└── Version control

margin_correlation_gate.py      Pre-trade gate system
├── Margin gate (≤35%)
├── Correlation gate (USD exposure)
├── Notional gate (≥$15k)
├── RR gate (≥3.2:1)
└── Integration with engine
```

### Brokers (`brokers/`)

```
oanda_connector.py              OANDA REST v20 API
├── Authentication (Bearer token)
├── Price fetching
├── Order placement (market/limit/stop)
├── Position management
├── Account info retrieval
└── Error handling
```

### Utilities (`util/`)

```
strategy_aggregator.py          5-strategy voting system
quant_hedge_engine.py           7-rule correlation hedge
momentum_trailing.py            Momentum detection + trails
narration_logger.py             Event logging (narration.jsonl)
rick_narrator.py                LLM narration (optional Ollama)
terminal_display.py             Status display formatting
```

### Position Guardian (`plugins/position_guardian/`)

```
rules.py                        10 autopilot rules
├── Auto breakeven (BE+5 @ ≥1R)
├── Time stops (3h/6h)
├── ATR trailing (Stage 2/3)
├── Giveback exit (40% from peak)
├── Scale outs (50%@1.5R, 25%@2.5R)
├── Session gate (Friday 20:55 UTC)
└── Margin/correlation gates

guardian_daemon.py              30s tick enforcement
manager_integration.py          pg_trade() entry point
```

### Dashboard (`/home/ing/RICK/RICK_LIVE_PROTOTYPE/`)

```
start_dashboard.sh              3-pane tmux launcher
dashboard_live_monitor.py       Left pane: narration stream
ai_decision_monitor.py          Top-right: AI decisions (1.5s refresh)
interactive_command_terminal.sh Bottom-right: manual control
```

### Orchestration (`/home/ing/RICK/RICK_LIVE_PROTOTYPE/`)

```
SMART_STARTUP.sh                7-phase intelligent boot
verify_complete_system.py       9-section validation (27 checks)
```

## 2.4 File Structure

```
/home/ing/RICK/RICK_LIVE_PROTOTYPE/
├── oanda_trading_engine.py      ✅ Main engine
├── canary_trading_engine.py     ✅ Canary engine
├── oanda_paper_trading.py       ✅ Paper wrapper
├── ghost_trading_engine.py      ✅ Ghost engine
├── autonomous_decision_engine.py ✅ Decision logger
├── SMART_STARTUP.sh             ✅ Smart boot (18 KB)
├── verify_complete_system.py    ✅ Verification (12 KB)
├── start_dashboard.sh           ✅ Tmux launcher
├── dashboard_live_monitor.py    ✅ Left pane
├── ai_decision_monitor.py       ✅ Top-right pane
├── interactive_command_terminal.sh ✅ Bottom-right pane
├── .env                         🔒 Credentials (NEVER COMMIT)
├── narration.jsonl              📝 Event log (append-only)
├── connection_state.json        💾 Position state
├── SYSTEM_ARCHITECTURE.png      📊 Visual diagram (300 dpi)
├── foundation/
│   ├── rick_charter.py          🔒 Immutable Charter
│   └── margin_correlation_gate.py 🛡️ Pre-trade gates
├── brokers/
│   └── oanda_connector.py       🔌 OANDA API
├── util/
│   ├── strategy_aggregator.py   🎯 5-strategy voting
│   ├── quant_hedge_engine.py    ⚖️ 7-rule hedge
│   ├── momentum_trailing.py     📈 Momentum system
│   ├── narration_logger.py      📝 Event logging
│   ├── rick_narrator.py         🤖 LLM narration
│   └── terminal_display.py      🖥️ Display formatting
├── plugins/position_guardian/
│   ├── rules.py                 🛡️ 10 autopilot rules
│   ├── guardian_daemon.py       ⚙️ 30s tick enforcement
│   └── manager_integration.py   🔗 pg_trade() entry
└── .archive_legacy_docs/        📦 Historical docs (300+ files)
```

---

# 3. QUICK START GUIDE

## 3.1 30-Second Startup

### Method 1: VS Code Task (RECOMMENDED - EASIEST)

```
1. Open VS Code in /home/ing/RICK/RICK_LIVE_PROTOTYPE
2. Press: Ctrl+Shift+B
3. Select: "🟢 START EVERYTHING (Rick + Hive Mind + Dashboard)"
4. Wait 10-15 seconds for system boot
5. Dashboard opens automatically in tmux
6. ✅ System ready for autonomous trading
```

### Method 2: Command Line (FAST)

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash SMART_STARTUP.sh
```

**What SMART_STARTUP.sh does:**
- Phase 1: Pre-flight checks (Charter validation, PIN 841921)
- Phase 2: Process detection (reuses running Ollama/Engine)
- Phase 3: Start Ollama (if not already running)
- Phase 4: Start Trading Engine (if not already running)
- Phase 5: Launch Dashboard (3-pane tmux)
- Phase 6: Run verification suite (27 checks)
- Phase 7: Display readiness confirmation

### Method 3: Manual Step-by-Step (FOR DEBUGGING)

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE

# Step 1: Verify immutable state
python3 verify_complete_system.py

# Step 2: Start Ollama (optional for narration)
ollama serve &
sleep 3

# Step 3: Start Trading Engine
python3 oanda_trading_engine.py &
sleep 5

# Step 4: Launch Dashboard
bash start_dashboard.sh

# Step 5: Verify system ready
python3 verify_complete_system.py
```

## 3.2 Verification (1 Minute)

**Automatic Verification (RECOMMENDED):**

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
python3 verify_complete_system.py
```

**Expected Output:**

```
════════════════════════════════════════════════════════════
  RICK SYSTEM - COMPLETE VERIFICATION
════════════════════════════════════════════════════════════

[1/9] Charter Immutability...................... ✅ PASS (3/3)
[2/9] Guardian Gate System...................... ✅ PASS (3/3)
[3/9] Trading Engine Components................. ✅ PASS (3/3)
[4/9] Subsystems & Features..................... ✅ PASS (5/5)
[5/9] Event Logging & Narration................. ✅ PASS (3/3)
[6/9] OANDA API Connection...................... ✅ PASS (2/2)
[7/9] State Persistence......................... ✅ PASS (3/3)
[8/9] Process Management........................ ✅ PASS (3/3)
[9/9] Full System Integration................... ✅ PASS (2/2)

════════════════════════════════════════════════════════════
  RESULT: 27/27 CHECKS PASSED (100.0%)
  ✅ SYSTEM READY FOR AUTONOMOUS OPERATION
════════════════════════════════════════════════════════════
```

**Manual Verification (IF NEEDED):**

```bash
# Check Charter constants
python3 -c "from foundation.rick_charter import RickCharter; print(f'PIN: {RickCharter.PIN}, Min Notional: ${RickCharter.MIN_NOTIONAL_USD:,}')"

# Check Guardian Gates
python3 -c "from foundation.margin_correlation_gate import MarginCorrelationGate; g = MarginCorrelationGate(2000); print('Gates: READY')"

# Check OANDA connection
python3 -c "from brokers.oanda_connector import OandaConnector; c = OandaConnector('practice'); print(c.get_account_info())"

# Check narration logging
tail -5 narration.jsonl

# Check position state
cat connection_state.json
```

## 3.3 Dashboard Access

**Attach to Dashboard:**

```bash
tmux attach -t rbotzilla
```

**Dashboard Layout:**

```
┌──────────────────────────────────────────────────────────────────┐
│ LEFT PANE (70%): NARRATION STREAM                                │
│                                                                   │
│ [18:45:23] TRADE_EXECUTION: EUR_USD LONG 15000 units @ 1.0850   │
│ [18:45:24] HEDGE_ANALYSIS: Considering USD_JPY hedge...         │
│ [18:45:25] POSITION_GUARDIAN: Auto breakeven @ BE+5             │
│ [18:45:30] MARKET_REGIME: Trending detected (0.73 confidence)   │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│ TOP-RIGHT (30%): AI DECISIONS (1.5s refresh)                     │
│                                                                   │
│ Current Positions: 2                                             │
│ EUR_USD LONG: +$125.50 (0.8R)                                    │
│ USD_JPY SHORT: -$45.20 (HEDGE)                                   │
│                                                                   │
│ Last Decision: HOLD (Guardian active)                            │
│ Next Check: 25 seconds                                           │
├──────────────────────────────────────────────────────────────────┤
│ BOTTOM-RIGHT (30%): MANUAL CONTROL                               │
│                                                                   │
│ > status                                                          │
│ ✅ System: OPERATIONAL                                            │
│ ✅ Gates: ALL ACTIVE                                              │
│ ✅ Balance: $1,898.48                                             │
│                                                                   │
│ > help                                                            │
│ Commands: start, stop, status, positions, log, help, exit        │
│                                                                   │
│ >                                                                 │
└──────────────────────────────────────────────────────────────────┘
```

**Detach from Dashboard (Keep Running):**

Press: `Ctrl+B` then `D`

## 3.4 Control Commands

**Inside Dashboard Terminal (Bottom-Right Pane):**

```bash
> start          # Start autonomous trading
> stop           # Stop gracefully (closes positions)
> status         # Show current system state
> positions      # List open positions
> log            # Show recent events (last 20)
> help           # Show all commands
> exit           # Exit terminal (dashboard keeps running)
```

## 3.5 Graceful Shutdown

### Method 1: Dashboard Terminal

```bash
> stop
# System closes positions → saves state → exits gracefully
```

### Method 2: Command Line

```bash
# Stop trading engine
pkill -f "oanda_trading_engine.py"

# Stop Ollama (optional)
pkill -f "ollama serve"

# Close dashboard
tmux kill-session -t rbotzilla
```

### Method 3: Emergency Stop (VS Code Task)

```
1. Press: Ctrl+Shift+P
2. Select: "Tasks: Run Task"
3. Select: "🛑 Stop All Trading"
4. Confirm: All trading processes killed
```

## 3.6 Restart (Guaranteed Safe State Recovery)

```bash
# 1. Stop gracefully
pkill -f "oanda_trading_engine.py"
sleep 5

# 2. Verify state saved
cat connection_state.json
tail -5 narration.jsonl

# 3. Start fresh
bash SMART_STARTUP.sh

# 4. Verify ready
python3 verify_complete_system.py
```

**State Recovery Guarantees:**
- ✅ Previous positions restored from `connection_state.json`
- ✅ Event history preserved in `narration.jsonl` (append-only)
- ✅ Charter constants never change (immutable)
- ✅ Guardian gates automatically re-initialized
- ✅ All subsystems reconnect to OANDA API

---

# 4. INSTALLATION & SETUP

## 4.1 Prerequisites

**System Requirements:**
- OS: Linux (Ubuntu 20.04+, Debian 10+, or similar)
- Python: 3.10 or higher
- Disk Space: 1 GB minimum
- Network: Stable internet connection (OANDA API)
- Optional: Ollama (for Rick LLM narration)

**Python Dependencies:**

```bash
pip3 install python-dotenv requests jq
```

**System Tools:**

```bash
sudo apt-get install tmux curl jq
```

## 4.2 OANDA Account Setup

### Practice Account (Paper Trading - FREE)

1. Visit: https://www.oanda.com/us-en/trading/demo-account/
2. Create free demo account
3. Login to: https://www.oanda.com/demo-account/login
4. Navigate to: Manage API Access
5. Generate Practice API Token
6. Note your Account ID (format: 101-001-XXXXXXXX-XXX)

### Live Account (Real Trading - FUNDED)

1. Visit: https://www.oanda.com/us-en/trading/
2. Create funded live account
3. Complete KYC verification
4. Login to: https://www.oanda.com/account/login
5. Navigate to: Manage API Access
6. Generate Live API Token
7. Note your Account ID (format: 001-001-XXXXXXXX-XXX)

## 4.3 Environment Configuration

**Create `.env` file:**

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
nano .env
```

**Required Variables:**

```bash
# OANDA Practice (Paper Trading)
OANDA_PRACTICE_TOKEN=YOUR_PRACTICE_TOKEN_HERE
OANDA_PRACTICE_ACCOUNT_ID=YOUR_PRACTICE_ACCOUNT_ID_HERE

# OANDA Live (Real Trading) - OPTIONAL
OANDA_LIVE_TOKEN=YOUR_LIVE_TOKEN_HERE
OANDA_LIVE_ACCOUNT_ID=YOUR_LIVE_ACCOUNT_ID_HERE

# Optional: Dashboard Port (default 8080)
DASHBOARD_PORT=8080
```

**Security Best Practices:**

```bash
# Set restrictive permissions
chmod 600 .env

# NEVER commit .env to git
echo ".env" >> .gitignore

# Verify .env not tracked
git status
```

## 4.4 Initial Verification

**Test OANDA Connection:**

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
python3 canary_oanda_connector.py
```

**Expected Output:**

```
✅ OANDA Practice API: Connected
Account ID: 101-001-31210531-002
Balance: $1,898.48 USD
Margin Available: $1,898.48
Margin Used: $0.00
Open Positions: 0
```

**Test Charter Validation:**

```bash
python3 -c "from foundation.rick_charter import RickCharter; print('PIN:', RickCharter.validate_pin(841921))"
```

**Expected Output:**

```
PIN: True
```

## 4.5 Optional: Ollama Setup (Rick Narration)

**Install Ollama:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Pull Model:**

```bash
ollama pull llama2:7b
```

**Start Service:**

```bash
ollama serve &
```

**Verify:**

```bash
curl -s http://127.0.0.1:11434/api/tags
```

---

# 5. OPERATIONS & CONTROL

## 5.1 Daily Workflow

### Morning Startup (Pre-Market)

```bash
# 1. Navigate to project
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE

# 2. Start system
bash SMART_STARTUP.sh

# 3. Verify ready
python3 verify_complete_system.py

# 4. Attach to dashboard
tmux attach -t rbotzilla

# 5. Check account balance
> status

# 6. Start autonomous trading
> start
```

### Intraday Monitoring

**Dashboard Terminal Commands:**

```bash
> status         # System health check
> positions      # Open position status
> log            # Recent trade history
```

**Check Specific Position:**

```bash
grep "EUR_USD" narration.jsonl | tail -10 | jq -r '.narration'
```

**Check Guardian Activity:**

```bash
tail -20 logs/guardian.log
```

**Check Hedge Activity:**

```bash
grep "HEDGE" narration.jsonl | tail -10 | jq .
```

### End of Day Shutdown

```bash
# 1. Attach to dashboard
tmux attach -t rbotzilla

# 2. Stop trading (closes positions)
> stop

# 3. Verify positions closed
> positions

# 4. Verify state saved
exit
cat connection_state.json

# 5. Optional: Kill all processes
pkill -f "oanda_trading_engine.py"
pkill -f "ollama serve"
tmux kill-session -t rbotzilla
```

## 5.2 VS Code Task Integration

**Available Tasks (Press `Ctrl+Shift+B`):**

| Task | Description | Action |
|------|-------------|--------|
| 🟢 START EVERYTHING | Full system startup | Ollama + Engine + Dashboard |
| 📊 View OANDA Account Balance | Quick balance check | Runs canary_oanda_connector.py |
| 🧪 Test OANDA Connection | API connectivity test | Validates credentials |
| 🛑 Stop All Trading | Emergency stop | Kills all trading processes |
| 🔧 Start Ollama | LLM narration only | Starts Ollama server |
| 📜 View Narration Log | Live event stream | Tails narration.jsonl |
| 📈 View Live Positions | Dashboard monitor | Launches position monitor |
| 🤖 View AI Decisions | Decision monitor | Launches AI decision pane |
| 🎮 Interactive Control | Manual terminal | Launches command interface |

**Task Configuration File:**

`.vscode/tasks.json` (automatically configured)

## 5.3 Position Management

### Manual Position Entry (Emergency)

**Not Recommended** - System is fully autonomous. Manual intervention only for emergency testing.

```python
# Inside dashboard terminal
> exit

# Run Python interactive
python3
from oanda_trading_engine import OandaTradingEngine
engine = OandaTradingEngine(841921, 'practice')
engine.place_order('EUR_USD', 'buy', 15000, 1.0850, 1.0800, 1.1200)
exit()
```

### Force Position Close

```python
python3
from brokers.oanda_connector import OandaConnector
conn = OandaConnector('practice')
conn.close_position('EUR_USD', 'long')
exit()
```

### Check Position State

```bash
cat connection_state.json | jq .
```

## 5.4 Event Log Analysis

**View Recent Events:**

```bash
tail -50 narration.jsonl | jq -r '.narration'
```

**Filter by Event Type:**

```bash
grep "TRADE_EXECUTION" narration.jsonl | jq .
grep "HEDGE_ANALYSIS" narration.jsonl | jq .
grep "GUARDIAN_ACTION" narration.jsonl | jq .
grep "STRATEGY_SIGNAL" narration.jsonl | jq .
```

**Filter by Symbol:**

```bash
grep "EUR_USD" narration.jsonl | jq -r '.narration'
```

**Filter by Time Range:**

```bash
grep "2025-10-20T18:" narration.jsonl | jq -r '.narration'
```

**Count Events by Type:**

```bash
jq -r '.event_type' narration.jsonl | sort | uniq -c
```

---

# 6. PROTECTION & SECURITY

## 6.1 Multi-Layer Protection Architecture

### Layer 1: Immutable Constants

**What It Is:**  
Charter values are hardcoded at class level in `foundation/rick_charter.py` and cannot be overridden.

**How It Works:**

```python
class RickCharter:
    PIN = 841921                    # Hardcoded
    MIN_NOTIONAL_USD = 15000        # Hardcoded
    MIN_RISK_REWARD_RATIO = 3.0     # Hardcoded
    MAX_HOLD_DURATION_HOURS = 6     # Hardcoded
    DAILY_LOSS_BREAKER_PCT = -5.0   # Hardcoded
    MAX_CONCURRENT_POSITIONS = 3    # Hardcoded
    MAX_MARGIN_UTILIZATION = 35.0   # Hardcoded
```

**Protection:**
- No method to override these values
- No environment variable override
- No config file override
- No runtime modification

### Layer 2: PIN-Based Access Control

**What It Is:**  
Every trading engine initialization requires PIN 841921 validation.

**How It Works:**

```python
# In oanda_trading_engine.py line 85-86
if not RickCharter.validate_pin(841921):
    raise PermissionError("Invalid Charter PIN - cannot initialize")
```

**Protection:**
- Engine won't start without PIN
- AI agents can't bypass PIN
- Prevents accidental modification
- Audit trail of all init attempts

### Layer 3: Pre-Trade Guardian Gates

**What It Is:**  
4 gates validate every order before execution.

**Gates:**

1. **Charter Gate** - Validates notional ≥$15k, RR ≥3.2:1
2. **Margin Gate** - Blocks if margin >35%
3. **Correlation Gate** - Blocks same-side USD exposure
4. **Notional Gate** - Ensures Charter compliance

**How It Works:**

```python
# In oanda_trading_engine.py lines 715-732
gate_result = self.gate.pre_trade_validation(
    symbol=symbol,
    direction=direction,
    size_units=size_units,
    entry=entry_price,
    stop_loss=stop_loss,
    take_profit=take_profit
)

if not gate_result['approved']:
    self.log_event('GATE_REJECTION', gate_result)
    return None  # Order blocked
```

**Protection:**
- Every order checked
- No bypass mechanism
- Full audit trail
- Automatic rejection

### Layer 4: Append-Only Event Logging

**What It Is:**  
All decisions logged to `narration.jsonl` (cannot modify past events).

**How It Works:**

```python
# In util/narration_logger.py
def log_event(event_type, details):
    with open('narration.jsonl', 'a') as f:  # 'a' = append only
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }, f)
        f.write('\n')
```

**Protection:**
- Append-only (cannot edit)
- Timestamped (chronological)
- Complete audit trail
- Immutable record

## 6.2 AI Agent Protection Strategy

**How to Prevent AI Agents from Accidentally Changing System:**

### File Permission Locks

```bash
# Make Charter read-only
chmod 444 foundation/rick_charter.py

# Make gate system read-only
chmod 444 foundation/margin_correlation_gate.py

# Verify permissions
ls -la foundation/
```

### Git Tracking

```bash
# Track Charter changes
git add foundation/rick_charter.py
git commit -m "Lock Charter constants"

# Revert any accidental changes
git checkout foundation/rick_charter.py
```

### Documentation Strategy

Create `SIMPLE_AI_AGENT_INSTRUCTION.md` with clear DO/DON'T lists (already exists).

**Key Points:**
- ✅ AI can READ all files for understanding
- ✅ AI can CREATE documentation
- ✅ AI can ADD comments (non-invasive)
- ❌ AI CANNOT modify trading logic
- ❌ AI CANNOT modify Charter constants
- ❌ AI CANNOT modify Guardian gates
- ❌ AI CANNOT modify Hedge decisions

## 6.3 State Recovery Mechanisms

### Automatic State Persistence

**Position State:**

```json
// connection_state.json (auto-saved every 30s)
{
  "positions": [
    {
      "symbol": "EUR_USD",
      "direction": "long",
      "size": 15000,
      "entry": 1.0850,
      "stop_loss": 1.0800,
      "take_profit": 1.1200,
      "unrealized_pl": 125.50
    }
  ],
  "timestamp": "2025-10-20T18:45:00Z"
}
```

**Event History:**

```jsonl
// narration.jsonl (append-only, never deleted)
{"timestamp":"2025-10-20T18:45:00Z","event_type":"TRADE_EXECUTION","symbol":"EUR_USD",...}
{"timestamp":"2025-10-20T18:45:05Z","event_type":"HEDGE_ANALYSIS","symbol":"USD_JPY",...}
{"timestamp":"2025-10-20T18:45:10Z","event_type":"GUARDIAN_ACTION","action":"auto_breakeven",...}
```

### Manual Backup/Restore

**Create Backup:**

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
mkdir -p backups
cp connection_state.json backups/connection_state_$(date +%Y%m%d_%H%M%S).json
cp narration.jsonl backups/narration_$(date +%Y%m%d_%H%M%S).jsonl
```

**Restore from Backup:**

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
cp backups/connection_state_20251020_184500.json connection_state.json
cp backups/narration_20251020_184500.jsonl narration.jsonl
```

## 6.4 Security Best Practices

**Credential Management:**

```bash
# .env file must be restricted
chmod 600 .env

# NEVER commit credentials
echo ".env" >> .gitignore
echo "*.token" >> .gitignore

# Rotate tokens quarterly
# OANDA: Manage API Access → Revoke old → Generate new
```

**Process Isolation:**

```bash
# Run as non-root user
whoami  # Should NOT be root

# Check process ownership
ps aux | grep oanda_trading_engine
```

**Network Security:**

```bash
# Only allow OANDA API endpoints
sudo ufw allow out 443/tcp comment 'HTTPS OANDA API'
sudo ufw deny in 11434/tcp comment 'Block external Ollama'
```

---

# 7. TROUBLESHOOTING

## 7.1 Common Issues

### Issue: "Ollama already running"

**Symptom:**

```
Error: listen tcp 127.0.0.1:11434: bind: address already in use
```

**Solution:**

SMART_STARTUP.sh handles this automatically. If running manually:

```bash
# Check if Ollama running
pgrep -f "ollama serve"

# Option 1: Reuse existing Ollama (preferred)
# Do nothing - system will detect and reuse

# Option 2: Force restart
pkill -f "ollama serve"
sleep 2
ollama serve &
```

### Issue: Unknown System State

**Symptom:**

Don't know if system is ready or what's working.

**Solution:**

```bash
python3 verify_complete_system.py
```

**Diagnosis:**
- ✅ All checks passed → System ready
- ❌ Some checks failed → See specific section that failed

### Issue: "Permission denied" on .env

**Symptom:**

```
PermissionError: [Errno 13] Permission denied: '.env'
```

**Solution:**

```bash
chmod 600 .env
chown $USER:$USER .env
```

### Issue: OANDA API Connection Failed

**Symptom:**

```
ConnectionError: Unable to connect to OANDA API
```

**Solution:**

```bash
# 1. Check internet connection
ping -c 3 api-fxpractice.oanda.com

# 2. Verify .env credentials
cat .env | grep OANDA_PRACTICE_TOKEN

# 3. Test connection
python3 canary_oanda_connector.py

# 4. Check token validity (login to OANDA dashboard)
```

### Issue: Dashboard Not Showing Positions

**Symptom:**

Dashboard panes empty or not updating.

**Solution:**

```bash
# 1. Check if engine running
ps aux | grep oanda_trading_engine

# 2. Check narration log exists
ls -lh narration.jsonl

# 3. Check connection state exists
ls -lh connection_state.json

# 4. Restart dashboard
tmux kill-session -t rbotzilla
bash start_dashboard.sh
```

### Issue: Trades Not Executing

**Symptom:**

Strategies generating signals but no orders placed.

**Diagnosis:**

```bash
# Check recent gate rejections
grep "GATE_REJECTION" narration.jsonl | tail -10 | jq .
```

**Common Causes:**
- Margin >35% → Reduce position size
- Notional <$15k → Increase position size
- Same-side USD exposure → Wait for position close
- RR <3.2:1 → Adjust stop/take profit

### Issue: Charter PIN Validation Failed

**Symptom:**

```
PermissionError: Invalid Charter PIN - cannot initialize trading engine
```

**Solution:**

This should NEVER happen. PIN is hardcoded as 841921.

**Recovery:**

```bash
# 1. Verify Charter file not corrupted
python3 -c "from foundation.rick_charter import RickCharter; print(RickCharter.PIN)"

# Expected: 841921

# 2. If wrong PIN, restore from git
git checkout foundation/rick_charter.py

# 3. Verify restoration
python3 -c "from foundation.rick_charter import RickCharter; print(RickCharter.validate_pin(841921))"

# Expected: True
```

## 7.2 Log Analysis

**Engine Logs:**

```bash
tail -50 /tmp/engine.log
```

**Ollama Logs:**

```bash
tail -50 /tmp/ollama.log
```

**Guardian Logs:**

```bash
tail -50 logs/guardian.log
```

**Event Logs:**

```bash
tail -50 narration.jsonl | jq -r '.narration'
```

**Error Pattern Search:**

```bash
grep -i "error" narration.jsonl | tail -20 | jq .
grep -i "failed" narration.jsonl | tail -20 | jq .
grep -i "rejected" narration.jsonl | tail -20 | jq .
```

## 7.3 System Reset

**Soft Reset (Keep Positions):**

```bash
# Stop engine
pkill -f "oanda_trading_engine.py"

# Restart
bash SMART_STARTUP.sh
```

**Hard Reset (Close All Positions):**

```bash
# 1. Stop engine
pkill -f "oanda_trading_engine.py"

# 2. Close all positions via OANDA API
python3 << EOF
from brokers.oanda_connector import OandaConnector
conn = OandaConnector('practice')
positions = conn.get_open_positions()
for pos in positions:
    conn.close_position(pos['instrument'], pos['side'])
EOF

# 3. Clear state
rm connection_state.json
echo '{"positions": []}' > connection_state.json

# 4. Restart
bash SMART_STARTUP.sh
```

**Nuclear Reset (Factory Defaults):**

```bash
# ⚠️ WARNING: Loses all event history

# 1. Stop all processes
pkill -f "oanda_trading_engine.py"
pkill -f "ollama serve"
tmux kill-session -t rbotzilla

# 2. Backup current state
mkdir -p backups
cp narration.jsonl backups/narration_backup_$(date +%Y%m%d_%H%M%S).jsonl
cp connection_state.json backups/connection_state_backup_$(date +%Y%m%d_%H%M%S).json

# 3. Clear state
rm narration.jsonl connection_state.json

# 4. Initialize fresh
touch narration.jsonl
echo '{"positions": []}' > connection_state.json

# 5. Start system
bash SMART_STARTUP.sh
```

---

# 8. API REFERENCE

## 8.1 OANDA REST v20 API

**Base URLs:**
- Practice: `https://api-fxpractice.oanda.com/v3`
- Live: `https://api-fxtrade.oanda.com/v3`

**Authentication:**

```
Authorization: Bearer <token>
Content-Type: application/json
```

**Rate Limits:**
- Practice: 120 requests/second
- Live: 100 requests/second

### 8.1.1 Account Information

**Endpoint:** `GET /accounts/{accountID}`

**Example:**

```python
from brokers.oanda_connector import OandaConnector
conn = OandaConnector('practice')
info = conn.get_account_info()
print(info)
```

**Response:**

```json
{
  "account": {
    "id": "101-001-31210531-002",
    "balance": "1898.48",
    "marginAvailable": "1898.48",
    "marginUsed": "0.00",
    "openPositionCount": 0
  }
}
```

### 8.1.2 Get Pricing

**Endpoint:** `GET /accounts/{accountID}/pricing`

**Example:**

```python
conn = OandaConnector('practice')
prices = conn.get_prices(['EUR_USD', 'GBP_USD'])
print(prices)
```

**Response:**

```json
{
  "prices": [
    {
      "instrument": "EUR_USD",
      "bids": [{"price": "1.08500"}],
      "asks": [{"price": "1.08520"}],
      "time": "2025-10-20T18:45:00Z"
    }
  ]
}
```

### 8.1.3 Place Market Order

**Endpoint:** `POST /accounts/{accountID}/orders`

**Example:**

```python
conn = OandaConnector('practice')
order = conn.place_market_order(
    instrument='EUR_USD',
    units=15000,  # Positive = long, negative = short
    stop_loss=1.0800,
    take_profit=1.1200
)
print(order)
```

**Request Body:**

```json
{
  "order": {
    "type": "MARKET",
    "instrument": "EUR_USD",
    "units": "15000",
    "stopLossOnFill": {"price": "1.0800"},
    "takeProfitOnFill": {"price": "1.1200"}
  }
}
```

### 8.1.4 Close Position

**Endpoint:** `PUT /accounts/{accountID}/positions/{instrument}/close`

**Example:**

```python
conn = OandaConnector('practice')
result = conn.close_position('EUR_USD', 'long')
print(result)
```

## 8.2 Charter API

**Class:** `RickCharter`  
**Location:** `foundation/rick_charter.py`

### 8.2.1 Constants

```python
from foundation.rick_charter import RickCharter

PIN = RickCharter.PIN                           # 841921
MIN_NOTIONAL = RickCharter.MIN_NOTIONAL_USD     # 15000
MIN_RR = RickCharter.MIN_RISK_REWARD_RATIO      # 3.0
MAX_HOLD = RickCharter.MAX_HOLD_DURATION_HOURS  # 6
MAX_CONCURRENT = RickCharter.MAX_CONCURRENT_POSITIONS  # 3
MAX_MARGIN = RickCharter.MAX_MARGIN_UTILIZATION  # 35.0
DAILY_LOSS = RickCharter.DAILY_LOSS_BREAKER_PCT  # -5.0
```

### 8.2.2 Validation Methods

**Validate PIN:**

```python
is_valid = RickCharter.validate_pin(841921)  # True
```

**Validate Trade:**

```python
is_valid = RickCharter.validate_trade(
    notional_usd=20000,      # Must be ≥$15k
    risk_reward_ratio=3.5,   # Must be ≥3.0
    hold_duration_hours=4    # Must be ≤6
)
# Returns: True
```

## 8.3 Guardian Gate API

**Class:** `MarginCorrelationGate`  
**Location:** `foundation/margin_correlation_gate.py`

### 8.3.1 Initialization

```python
from foundation.margin_correlation_gate import MarginCorrelationGate

gate = MarginCorrelationGate(account_nav=2000.0)
```

### 8.3.2 Pre-Trade Validation

```python
result = gate.pre_trade_validation(
    symbol='EUR_USD',
    direction='long',
    size_units=15000,
    entry=1.0850,
    stop_loss=1.0800,
    take_profit=1.1200
)

print(result)
# {
#   'approved': True,
#   'margin_utilization': 0.28,
#   'correlation_risk': 'low',
#   'notional_usd': 16275
# }
```

## 8.4 Strategy Aggregator API

**Class:** `StrategyAggregator`  
**Location:** `util/strategy_aggregator.py`

### 8.4.1 Get Consensus Signal

```python
from util.strategy_aggregator import StrategyAggregator

aggregator = StrategyAggregator()
signal = aggregator.get_consensus_signal('EUR_USD')

print(signal)
# {
#   'symbol': 'EUR_USD',
#   'direction': 'long',
#   'confidence': 0.80,
#   'vote_count': 4,
#   'total_strategies': 5
# }
```

## 8.5 Hedge Engine API

**Class:** `QuantHedgeEngine`  
**Location:** `util/quant_hedge_engine.py`

### 8.5.1 Get Hedge Recommendation

```python
from util.quant_hedge_engine import QuantHedgeEngine

hedge_engine = QuantHedgeEngine()
recommendation = hedge_engine.analyze_hedge_need(
    symbol='EUR_USD',
    direction='long',
    size=15000,
    margin_pct=0.30
)

print(recommendation)
# {
#   'hedge_recommended': True,
#   'hedge_symbol': 'USD_JPY',
#   'hedge_direction': 'short',
#   'hedge_size': 15000,
#   'reason': 'High margin (30%) + strong inverse correlation (-0.72)'
# }
```

---

# 9. PORT & SERVICE ALLOCATION

## 9.1 Port Summary

| Service | Port | Protocol | Host | Status |
|---------|------|----------|------|--------|
| Tmux Dashboard | PTY (7680-7690 range) | Terminal | localhost | ACTIVE |
| Ollama LLM | 11434 | HTTP | 127.0.0.1 | OPTIONAL |
| OANDA API | 443 | HTTPS | External | REQUIRED |
| Trading Engine | Internal IPC | Python | localhost | ACTIVE |
| Event Logging | File I/O | Local FS | localhost | ACTIVE |

## 9.2 Network Diagram

```
┌────────────────────────────────────────────────────────┐
│           RICK SYSTEM - NETWORK ARCHITECTURE           │
└────────────────────────────────────────────────────────┘

LOCAL MACHINE (127.0.0.1):
├─ Tmux Session (PTY) ← Dashboard (3-pane)
├─ Port 11434 (HTTP) ← Ollama LLM [OPTIONAL]
└─ File I/O ← narration.jsonl, connection_state.json

EXTERNAL (Internet):
└─ Port 443 (HTTPS) → OANDA API
   ├─ api-fxpractice.oanda.com (practice)
   └─ api-fxtrade.oanda.com (live)
```

## 9.3 Multi-Agent Coordination

**RICK Reserves:**
- Port 11434 (Ollama - optional)
- Port 443 (HTTPS - shared standard)

**Available for Other Agents:**
- Port 8000-8999
- Port 3000-3999
- Port 5000-5999
- All other standard ports

**Coordination Strategy:**

```bash
# Start RICK first
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash SMART_STARTUP.sh

# Start other agent with different port
cd /your/agent/path
your_startup_command --port 8080
```

**Information Exchange:**

Other agents can READ (but not WRITE):
- `narration.jsonl` - Event history
- `connection_state.json` - Position state
- `logs/guardian.log` - Guardian actions

Other agents CANNOT modify:
- `foundation/rick_charter.py` - Immutable Charter
- `.env` - Credentials
- Port 11434 - Ollama (if running)

---

# 10. APPENDICES

## 10.1 File Reference

**Core System Files:**

| File | Size | Purpose |
|------|------|---------|
| `oanda_trading_engine.py` | 62 KB | Main trading engine |
| `foundation/rick_charter.py` | 8 KB | Immutable Charter |
| `foundation/margin_correlation_gate.py` | 12 KB | Pre-trade gates |
| `brokers/oanda_connector.py` | 15 KB | OANDA API client |
| `util/strategy_aggregator.py` | 18 KB | 5-strategy voting |
| `util/quant_hedge_engine.py` | 14 KB | 7-rule hedge logic |
| `plugins/position_guardian/rules.py` | 22 KB | 10 autopilot rules |
| `SMART_STARTUP.sh` | 18 KB | Intelligent boot |
| `verify_complete_system.py` | 12 KB | Verification suite |

**Documentation Files:**

| File | Size | Purpose |
|------|------|---------|
| `RICK_SYSTEM_MASTER_MANUAL.md` | This file | Complete system manual |
| `FUNCTIONAL_STATE_MAINTENANCE.md` | 15 KB | Protection strategy |
| `STARTUP_VERIFICATION_GUIDE.md` | 14 KB | Operations guide |
| `PORT_AUDIT.md` | 12 KB | Port allocation |
| `SYSTEM_COMPREHENSIVE_ANALYSIS.md` | 10 KB | Capability analysis |
| `QUICK_START_REFERENCE.md` | 4 KB | Quick reference |

## 10.2 Strategy Reference

**5 Trading Strategies:**

1. **Trap Reversal**
   - Entry: Failed breakout reversal
   - Stop: Beyond false break level
   - Target: Previous structure level
   - RR: 3.5:1 typical

2. **Fibonacci Confluence**
   - Entry: 0.618-0.786 retracement + support/resistance
   - Stop: Below 1.0 Fib level
   - Target: 1.618 extension
   - RR: 4.0:1 typical

3. **Price Action Holy Grail**
   - Entry: Pin bar + trend alignment
   - Stop: Beyond pin bar wick
   - Target: Next structure level
   - RR: 3.2:1 typical

4. **Liquidity Sweep**
   - Entry: Stop hunt + reversal
   - Stop: Beyond liquidity sweep
   - Target: Opposite side liquidity
   - RR: 3.8:1 typical

5. **EMA Scalper**
   - Entry: Price rejection at 20/50 EMA
   - Stop: 15 pips beyond EMA
   - Target: Next EMA level
   - RR: 3.0:1 typical

## 10.3 Guardian Rules Reference

**10 Autopilot Rules:**

1. **Correlation Gate** - Blocks same-side USD exposure
2. **Margin Gate** - Blocks if margin >35%
3. **Auto Breakeven** - Moves SL to BE+5 @ ≥1R or 25 pips
4. **Time Stops** - Closes losing trades (3h @ <0.5R, 6h all)
5. **ATR Trailing** - Dynamic trail in Stage 2/3
6. **Giveback Exit** - Exits @ 40% retracement from peak
7. **Scale Outs** - 50% @ 1.5R, 25% @ 2.5R
8. **Session Gate** - Closes all @ Friday 20:55 UTC
9. **Guardian Daemon** - 30s tick enforcement
10. **Manager Integration** - pg_trade() entry point

## 10.4 Hedge Rules Reference

**7-Rule Hedge Decision Matrix:**

| Rule # | Condition | Action | Reason |
|--------|-----------|--------|--------|
| 1 | No hedge pair | SKIP | Correlation too weak |
| 2 | Weak correlation (>-0.50) | SKIP | Ineffective hedge |
| 3 | High margin (>25%) | HEDGE | Risk reduction |
| 4 | Large notional (>$20k) | HEDGE | Protective hedge |
| 5 | Cumulative USD exposure (≥2 same side) | HEDGE | Correlation risk |
| 6 | Strong inverse correlation (<-0.70) | HEDGE | Opportunistic |
| 7 | Moderate margin + strong corr (15-25% + <-0.65) | HEDGE | Proactive |

## 10.5 Correlation Matrix

**Inverse Pairs (Hedge Candidates):**

| Pair 1 | Pair 2 | Correlation | Strength |
|--------|--------|-------------|----------|
| AUD_USD | USD_JPY | -0.80 | Very Strong |
| EUR_USD | USD_JPY | -0.72 | Strong |
| GBP_USD | USD_JPY | -0.68 | Strong |
| NZD_USD | USD_JPY | -0.65 | Moderate |

**Positive Pairs (Avoid Same-Side):**

| Pair 1 | Pair 2 | Correlation | Strength |
|--------|--------|-------------|----------|
| EUR_USD | GBP_USD | +0.85 | Very Strong |
| AUD_USD | NZD_USD | +0.82 | Very Strong |
| AUD_USD | USD_CAD | +0.75 | Strong |
| EUR_USD | AUD_USD | +0.70 | Strong |

## 10.6 Environment Variables Reference

**Required:**

```bash
OANDA_PRACTICE_TOKEN=<your_token>
OANDA_PRACTICE_ACCOUNT_ID=<your_account_id>
```

**Optional:**

```bash
OANDA_LIVE_TOKEN=<your_live_token>
OANDA_LIVE_ACCOUNT_ID=<your_live_account_id>
DASHBOARD_PORT=8080
OLLAMA_HOST=http://127.0.0.1:11434
```

## 10.7 Command Reference

**System Control:**

```bash
bash SMART_STARTUP.sh              # Full system startup
python3 verify_complete_system.py  # Verification suite
tmux attach -t rbotzilla           # Attach to dashboard
pkill -f "oanda_trading_engine.py" # Stop engine
pkill -f "ollama serve"            # Stop Ollama
tmux kill-session -t rbotzilla     # Kill dashboard
```

**Dashboard Commands:**

```
> start       # Start autonomous trading
> stop        # Stop gracefully
> status      # System health check
> positions   # List open positions
> log         # Recent events
> help        # Show all commands
> exit        # Exit terminal
```

**Log Analysis:**

```bash
tail -50 narration.jsonl | jq -r '.narration'    # Recent events
grep "EUR_USD" narration.jsonl | jq .            # Filter by symbol
grep "TRADE_EXECUTION" narration.jsonl | jq .    # Filter by type
jq -r '.event_type' narration.jsonl | sort | uniq -c  # Event counts
```

## 10.8 Verification Checklist

**Pre-Flight (Before Start):**

- [ ] Charter PIN: 841921 ✅
- [ ] .env file: Exists with valid credentials
- [ ] .env permissions: 600 (read/write owner only)
- [ ] OANDA connection: Test with `canary_oanda_connector.py`
- [ ] Python version: 3.10+ (`python3 --version`)
- [ ] Dependencies: Installed (`pip3 list`)
- [ ] Disk space: >1 GB available (`df -h`)

**Post-Startup (After Start):**

- [ ] Verification suite: 27/27 checks pass
- [ ] Ollama: Running (optional) (`pgrep -f "ollama serve"`)
- [ ] Trading engine: Running (`pgrep -f "oanda_trading_engine"`)
- [ ] Dashboard: Accessible (`tmux list-sessions`)
- [ ] Narration log: Writing events (`tail narration.jsonl`)
- [ ] Connection state: Valid JSON (`cat connection_state.json`)
- [ ] Guardian gates: Active (check verification output)
- [ ] OANDA API: Connected (check account balance in dashboard)

## 10.9 Support Resources

**Official Documentation:**
- OANDA API: https://developer.oanda.com/rest-live-v20/introduction/
- Ollama: https://ollama.com/docs/

**System Files:**
- Main Manual: `RICK_SYSTEM_MASTER_MANUAL.md` (this file)
- Protection Guide: `FUNCTIONAL_STATE_MAINTENANCE.md`
- Operations Guide: `STARTUP_VERIFICATION_GUIDE.md`
- Port Audit: `PORT_AUDIT.md`
- Quick Reference: `QUICK_START_REFERENCE.md`

**Contact:**
- Project Location: `/home/ing/RICK/RICK_LIVE_PROTOTYPE`
- Git Repository: (if applicable)
- System Version: 2.0 Production
- Last Updated: October 20, 2025

---

## 📝 REVISION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2025-10-20 | Consolidated master manual created |
| 1.5 | 2025-10-20 | SMART_STARTUP.sh added |
| 1.4 | 2025-10-20 | Verification suite added |
| 1.3 | 2025-10-20 | Dashboard 3-pane layout |
| 1.2 | 2025-10-20 | Architecture redesign (always-running) |
| 1.1 | 2025-10-20 | Micro trading disabled |
| 1.0 | 2025-10-19 | Initial system deployment |

---

**END OF MANUAL**

*This manual contains all information required to deploy, operate, maintain, and troubleshoot the RICK Autonomous Trading System. For updates and additional documentation, refer to the project directory.*

**PIN:** 841921 ✅  
**Status:** ✅ PRODUCTION READY  
**Version:** 2.0 Master Manual
