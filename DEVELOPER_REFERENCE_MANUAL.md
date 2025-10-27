# RICK Trading System - Developer Reference Manual

**Created:** October 10, 2025  
**Version:** 1.0  
**Audience:** Developers, Engineers, Technical Colleagues  
**Purpose:** Complete node-by-node system architecture reference with integration details

---

## 📋 DOCUMENT STRUCTURE

This manual documents each **node** (component) of the RICK trading system:
- **Purpose & Responsibilities** - What the node does
- **Integration Points** - How it connects to other nodes
- **File Inventory** - Complete list of files with color-coded categories
- **Dependencies** - What this node requires
- **Output** - What this node produces

---

## 🎨 COLOR CODING LEGEND

### File Type Categories:

| Color | Category | Description | Example Files |
|-------|----------|-------------|---------------|
| 🔴 **RED** | **Strategy Logic** | Trading strategies, signal generation, entry/exit rules | `wolfpack_orchestrator.py`, `ict_strategy.py` |
| 🟡 **YELLOW** | **Safety & Risk** | Stop-loss logic, risk management, circuit breakers | `smart_trailing.py`, `session_breaker.py` |
| 🟢 **GREEN** | **Execution** | Order placement, broker communication, trade execution | `oanda_connector.py`, `coinbase_connector.py` |
| 🔵 **BLUE** | **Data & Analysis** | Market data, indicators, analysis tools | `regime_detector.py`, `pattern_learner.py` |
| 🟣 **PURPLE** | **Infrastructure** | Core systems, configuration, utilities | `rick_charter.py`, `stochastic_config.py` |
| 🟠 **ORANGE** | **ML & Intelligence** | Machine learning, AI models, optimization | `ml_models.py`, `optimizer.py` |
| ⚫ **GRAY** | **Monitoring & Logs** | Logging, dashboards, monitoring tools | `narrate.py`, `pnl_tail.py` |

---

## 📊 SYSTEM ARCHITECTURE FLOWCHART

```
┌─────────────────────────────────────────────────────────────────┐
│                    RICK TRADING SYSTEM                          │
│                  (Live Ghost → Canary → Live)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
  ┌─────▼──────┐                            ┌──────▼─────┐
  │ FOUNDATION │                            │   BROKERS  │
  │  (Charter  │←──────────────────────────│  (API      │
  │   Rules)   │    PIN Validation          │   Connectors)│
  └─────┬──────┘                            └──────┬─────┘
        │                                          │
        │         ┌────────────────────────────────┘
        │         │
  ┌─────▼─────────▼──────┐
  │   WOLF PACKS          │
  │  (ICT/SMC Strategies) │
  └─────┬─────────────────┘
        │
        ├──────────┬──────────┬──────────┐
        │          │          │          │
  ┌─────▼───┐ ┌───▼────┐ ┌───▼────┐ ┌──▼──────┐
  │  RISK   │ │   ML   │ │  HIVE  │ │ SWARM   │
  │ CONTROL │ │ MODELS │ │  MIND  │ │ DELEGATE│
  └─────┬───┘ └───┬────┘ └───┬────┘ └──┬──────┘
        │         │          │          │
        └─────────┴──────────┴──────────┘
                    │
              ┌─────▼─────┐
              │   GHOST   │
              │  ENGINE   │
              └───────────┘
```

---

# 🏗️ NODE DOCUMENTATION

---

## NODE 1: FOUNDATION

### 📌 Block Title: `FOUNDATION - Charter & Core Rules`

### 🎯 Overall Purpose
**FOUNDATION** is the immutable ruleset that governs all trading activity. It acts as the constitutional authority for the RICK system, enforcing non-negotiable constraints on every trade decision. No trade can execute without passing Foundation validation.

### 📋 Jobs & Responsibilities
1. **PIN Authentication** - Validates PIN 841921 for all destructive operations
2. **Timeframe Enforcement** - Only allows M15, M30, H1 timeframes (blocks M1, M5)
3. **Risk-Reward Validation** - Enforces minimum 3.2:1 RR ratio on every trade
4. **Position Size Control** - Ensures minimum $15,000 notional per position
5. **Hold Duration Limits** - Maximum 6 hours per trade
6. **Daily Loss Circuit Breaker** - Halts trading at -5% daily P&L
7. **Immutability Verification** - SHA256 checksums prevent tampering

### 🔗 Integration Points
- **Brokers** ← Validates all order parameters before submission
- **Wolf Packs** ← Validates strategy signals before execution
- **Risk Control** ← Provides breach notifications
- **Ghost Engine** ← Validates simulation parameters
- **ML Models** ← Validates ML-generated signals

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `rick_charter.py` | `foundation/` | 🟣 PURPLE | Infrastructure | Core charter rules, PIN validation, RR enforcement |
| `RICK_CHARTER_IMMUTABLE.md` | `.system/` | 🟣 PURPLE | Infrastructure | Human-readable charter documentation |
| `PREPENDED_INSTRUCTIONS_IMMUTABLE.md` | `.system/` | 🟣 PURPLE | Infrastructure | AI agent instructions for charter compliance |
| `IMMUTABLE_SHA256SUMS.txt` | `.system/` | 🟣 PURPLE | Infrastructure | Integrity checksums for immutable files |

**Directory:** `/home/ing/RICK/R_H_UNI/foundation/` (48 KB total)

### 🔄 Dependencies
- **None** - Foundation is self-contained and has no external dependencies
- Depends only on Python stdlib (`hashlib`, `os`, `datetime`)

### 📤 Output
- Boolean validation results (PASS/FAIL)
- Exception raising on validation failures
- Audit log entries for all validations

### 🚨 Critical Notes
- **NEVER MODIFY** - Foundation files are immutable
- PIN 841921 is hardcoded and cannot be changed
- Any SHA256 mismatch triggers immediate halt

---

## NODE 2: BROKERS

### 📌 Block Title: `BROKERS - Exchange Connectivity`

### 🎯 Overall Purpose
**BROKERS** provides unified API connectivity to multiple exchanges (OANDA for FX, Coinbase for crypto). It abstracts venue-specific implementation details and presents a consistent interface for order execution, market data retrieval, and account management across all supported platforms.

### 📋 Jobs & Responsibilities
1. **API Authentication** - Manages credentials and tokens for OANDA/Coinbase
2. **Order Placement** - Executes market/limit orders on live exchanges
3. **Market Data Streaming** - Fetches real-time pricing (bid/ask spreads)
4. **Position Management** - Queries open positions and P&L
5. **Account Information** - Retrieves balances, margin, account status
6. **Error Handling** - Retries, rate limiting, API failure recovery
7. **Venue Abstraction** - Uniform interface regardless of exchange

### 🔗 Integration Points
- **Foundation** → Receives validated orders only
- **Wolf Packs** → Receives strategy signals, returns execution confirmations
- **Risk Control** → Reports position status, notifies on execution failures
- **Ghost Engine** → Provides live market data for simulation
- **Connectors (Futures)** → Shares authentication patterns for Binance/Bybit/OKX

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `oanda_connector.py` | `brokers/` | 🟢 GREEN | Execution | OANDA API v3 wrapper, FX order execution |
| `coinbase_connector.py` | `brokers/` | 🟢 GREEN | Execution | Coinbase Advanced Trade API, crypto execution |
| `broker_interface.py` | `brokers/` | 🟣 PURPLE | Infrastructure | Abstract base class for broker implementations |
| `retry.py` | `brokers/` | 🟡 YELLOW | Safety & Risk | Exponential backoff retry logic for API calls |

**Directory:** `/home/ing/RICK/R_H_UNI/brokers/` (68 KB total)

### 🔄 Dependencies
- `oandapyV20` (OANDA API client)
- `coinbase-advanced-py` (Coinbase SDK)
- `requests` (HTTP client)
- `python-dotenv` (Environment variables)
- **Foundation** (PIN validation for live trading)

### 📤 Output
- Order execution confirmations (order IDs, fill prices)
- Market data streams (JSONL format)
- Position snapshots (JSON)
- Error/retry logs

### 🚨 Critical Notes
- **Live API URLs only** - No practice/sandbox URLs allowed
- OANDA: `https://api-fxtrade.oanda.com/v3` (not fxpractice)
- Coinbase: No `passphrase` field (uses ECDSA ES256)
- Credentials stored in `.env` with 600 permissions

---

## NODE 3: WOLF PACKS

### 📌 Block Title: `WOLF PACKS - ICT/SMC Trading Strategies`

### 🎯 Overall Purpose
**WOLF PACKS** implements institutional trading methodologies (Inner Circle Trader concepts and Smart Money Concepts) organized into coordinated "packs." Each pack specializes in specific market conditions (Momentum, Scan, Trail, etc.) and delegates entry/exit decisions using stochastic thresholds to avoid deterministic patterns.

### 📋 Jobs & Responsibilities
1. **Signal Generation** - Identifies trade opportunities using ICT/SMC principles
2. **Stochastic Configuration** - Loads thresholds with 2% relative jitter (anti-pattern)
3. **Multi-Timeframe Analysis** - Analyzes M15, M30, H1 simultaneously
4. **Fair Value Gap Detection** - Identifies institutional order blocks
5. **Liquidity Sweep Recognition** - Detects stop hunts and reversals
6. **Orchestration** - Coordinates multiple packs based on regime
7. **Signal Filtering** - Ensures 3.2:1 RR minimum before forwarding

### 🔗 Integration Points
- **Foundation** → Validates all generated signals
- **Brokers** → Sends validated signals for execution
- **Risk Control** → Checks position limits before signaling
- **Regime Detector** → Receives market state (trending/ranging/volatile)
- **ML Models** → May receive ML confidence scores for signal augmentation
- **Hive Mind** → Delegates analysis to specialized members

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `wolfpack_orchestrator.py` | `wolf_packs/` | 🔴 RED | Strategy Logic | Coordinates all strategy packs based on regime |
| `ict_strategy.py` | `wolf_packs/` | 🔴 RED | Strategy Logic | Inner Circle Trader methodology implementation |
| `smc_strategy.py` | `wolf_packs/` | 🔴 RED | Strategy Logic | Smart Money Concepts (order blocks, FVG) |
| `momentum_pack.py` | `wolf_packs/` | 🔴 RED | Strategy Logic | Trending market specialist pack |
| `scan_pack.py` | `wolf_packs/` | 🔴 RED | Strategy Logic | Ranging market specialist pack |
| `trail_pack.py` | `wolf_packs/` | 🔴 RED | Strategy Logic | Trailing stop management pack |
| `stochastic_config.py` | `wolf_packs/` | 🟣 PURPLE | Infrastructure | Jittered threshold loader (2% randomness) |

**Directory:** `/home/ing/RICK/R_H_UNI/wolf_packs/` (36 KB total)

### 🔄 Dependencies
- **Foundation** (Charter validation)
- **Logic** (Regime detector, decision logic)
- **Configs** (`thresholds.json`, `wolfpack_config.json`)
- `numpy`, `pandas` (Technical analysis)
- **Stochastic** (Randomness utilities)

### 📤 Output
- Trade signals (JSON): `{"pair": "EUR_USD", "action": "BUY", "entry": 1.1605, "sl": 1.1575, "tp": 1.1701, "rr": 3.2}`
- Signal logs (JSONL)
- Pack activation events

### 🚨 Critical Notes
- **Stochastic by default** - Set `UNIBOT_SEED=1337` for deterministic (testing only)
- **M1/M5 rejected** - Only M15, M30, H1 allowed
- **3.2:1 RR minimum** - Lower RR signals are discarded immediately

---

## NODE 4: ML MODELS

### 📌 Block Title: `ML MODELS - Machine Learning Intelligence`

### 🎯 Overall Purpose
**ML MODELS** provides three specialized machine learning models (A for Forex, B for Crypto, C for Futures) that learn from historical patterns and enhance strategy signals with confidence scoring. Models are Charter-compliant, PIN-gated (841921), and operate in shadow mode initially to validate performance before live integration.

### 📋 Jobs & Responsibilities
1. **Pattern Learning** - Identifies recurring win/loss patterns from historical trades
2. **Regime Detection** - Classifies market conditions (trending/ranging/volatile)
3. **Confidence Scoring** - Assigns 0-100% confidence to strategy signals
4. **Signal Augmentation** - Enhances manual signals with ML insights (shadow mode)
5. **Continuous Learning** - Updates model weights based on realized P&L
6. **Sharpe Optimization** - Tunes strategy parameters for maximum risk-adjusted return
7. **Charter Compliance** - All ML signals validate against 3.2:1 RR, timeframes, etc.

### 🔗 Integration Points
- **Foundation** → Validates ML-generated signals (PIN 841921 required)
- **Wolf Packs** → Receives manual signals, augments with confidence scores
- **Ghost Engine** → Provides shadow mode testing environment
- **Pattern Learner** → Stores win/loss patterns for model training
- **Optimizer** → Receives Sharpe-driven parameter suggestions
- **Risk Control** → Reports ML signal performance for validation

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `ml_models.py` | `ml_learning/` | 🟠 ORANGE | ML & Intelligence | MLModel class (A/B/C), regime detection, confidence scoring |
| `pattern_learner.py` | `ml_learning/` | 🟠 ORANGE | ML & Intelligence | Pattern memory system, win/loss tracking |
| `optimizer.py` | `ml_learning/` | 🟠 ORANGE | ML & Intelligence | Sharpe-driven strategy optimization |
| `test_ml_intelligence.py` | `tests/` | 🔵 BLUE | Data & Analysis | ML model validation tests (Phase 13) |

**Directory:** `/home/ing/RICK/R_H_UNI/ml_learning/` (92 KB total)

### 🔄 Dependencies
- **Foundation** (PIN validation, RR enforcement)
- **Logic** (Regime detector for market state)
- `numpy`, `pandas` (Numerical processing)
- `scikit-learn` (Model training - optional)
- **Wolf Packs** (Strategy signal interface)

### 📤 Output
- ML-augmented signals (JSON): `{"signal": {...}, "ml_confidence": 0.87, "model": "A"}`
- Pattern memory (pickle files)
- Optimization suggestions (JSON)
- Performance reports (Sharpe, win rate)

### 🚨 Critical Notes
- **PIN 841921 required** - All ML operations gated
- **Shadow mode first** - Must validate 45-90 min before canary
- **Not integrated yet** - Status: YELLOW (testing, not live)
- **Model A/B/C specialization** - A=Forex, B=Crypto, C=Futures

---

## NODE 5: RISK CONTROL

### 📌 Block Title: `RISK CONTROL - Risk Management & Circuit Breakers`

### 🎯 Overall Purpose
**RISK CONTROL** is the guardian layer that enforces position limits, manages stop-losses, monitors P&L, and activates circuit breakers. It operates as a fail-safe above all other systems, capable of overriding any trade decision and halting the system if thresholds are breached.

### 📋 Jobs & Responsibilities
1. **Session Breaker** - Halts trading at -5% daily P&L loss
2. **OCO Validator** - Ensures every trade has stop-loss + take-profit
3. **Position Sizing** - Enforces minimum $15,000 notional per trade
4. **Concurrent Position Limits** - Max 1 position (canary), 3 (live)
5. **Exposure Tracking** - Monitors total risk across all pairs
6. **Smart Trailing** - Dynamic trailing stop-loss management
7. **Emergency Stop** - Force-closes all positions on critical breach

### 🔗 Integration Points
- **Foundation** → Receives Charter breach notifications
- **Wolf Packs** → Intercepts signals before execution
- **Brokers** → Can force-close positions directly
- **Ghost Engine** → Validates simulation risk parameters
- **ML Models** → Reports ML signal risk profile

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `session_breaker.py` | `risk/` | 🟡 YELLOW | Safety & Risk | Daily -5% P&L circuit breaker |
| `session_breaker_integration.py` | `risk/` | 🟡 YELLOW | Safety & Risk | Integration layer for session breaker |
| `oco_validator.py` | `risk/` | 🟡 YELLOW | Safety & Risk | Ensures stop-loss + take-profit on every trade |
| `risk_control_center.py` | `risk/` | 🟡 YELLOW | Safety & Risk | Central risk coordination, PIN 841921 gate |
| `smart_trailing.py` | `risk/` | 🟡 YELLOW | Safety & Risk | Trailing stop-loss manager (NOT stop-loss logic) |
| `position_sizer.py` | `risk/` | 🟣 PURPLE | Infrastructure | $15k minimum notional enforcement |

**Directory:** `/home/ing/RICK/R_H_UNI/risk/` (180 KB total)

### 🔄 Dependencies
- **Foundation** (Charter validation)
- **Brokers** (Position query, force-close API)
- **Logic** (Decision thresholds)
- `python-dotenv` (Environment config)

### 📤 Output
- Risk alerts (JSON): `{"event": "SESSION_BREAKER", "pnl": -5.2%, "action": "HALT"}`
- Position close confirmations
- Trailing stop adjustments
- Session breaker logs (JSONL)

### 🚨 Critical Notes
- **-5% daily halt** - Non-negotiable, immediate stop
- **OCO required** - Every trade must have SL+TP
- **PIN 841921** - Required for emergency stop override
- **$15k minimum** - Smaller positions rejected immediately

---

## NODE 6: GHOST ENGINE

### 📌 Block Title: `GHOST ENGINE - Live Simulation with Real Data`

### 🎯 Overall Purpose
**GHOST ENGINE** runs a live simulation environment using real API data from OANDA/Coinbase without executing actual trades. It validates the entire trading pipeline (signals → risk checks → execution simulation) and produces performance metrics to qualify systems for canary/live promotion.

### 📋 Jobs & Responsibilities
1. **Live Data Polling** - Fetches real market data every 750ms
2. **Signal Simulation** - Generates signals using live strategies
3. **Execution Simulation** - Simulates fills at real bid/ask prices
4. **P&L Tracking** - Calculates unrealized/realized P&L with slippage
5. **Performance Metrics** - Sharpe, win rate, max drawdown, VaR95
6. **Shadow Sanity Check** - 45-90 minute validation run
7. **Canary Qualification** - Must pass metrics before canary promotion

### 🔗 Integration Points
- **Foundation** → Validates all simulation parameters
- **Brokers** → Uses live API data (no actual orders)
- **Wolf Packs** → Receives live strategy signals
- **Risk Control** → Simulates risk checks
- **ML Models** → Can run ML shadow mode validation

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `live_ghost_engine.py` | `RICK_LIVE_DEPLOYMENT/` | 🟢 GREEN | Execution | Main ghost engine (750ms polling, live simulation) |
| `ghost_trading_engine.py` | `/` (root) | 🟢 GREEN | Execution | Legacy ghost engine implementation |
| `launch_live_ghost.sh` | `scripts/` | 🟣 PURPLE | Infrastructure | Ghost engine launcher with environment loading |
| `realistic_ghost_trading.log` | `/` (root) | ⚫ GRAY | Monitoring & Logs | Ghost engine execution log |
| `ghost_trading_final_report.json` | `/` (root) | ⚫ GRAY | Monitoring & Logs | Shadow sanity check results |

**Directory:** Various (primary: `RICK_LIVE_DEPLOYMENT/`) (10.8 KB code + logs)

### 🔄 Dependencies
- **Foundation** (Charter validation)
- **Brokers** (Live API data)
- **Wolf Packs** (Strategy signals)
- **Risk Control** (Risk validation)
- `.env` (API credentials with 600 perms)

### 📤 Output
- Ghost trading log (JSONL)
- Final report (JSON): `{"win_rate": 0.58, "sharpe": 0.92, "max_dd": 0.23, "expectancy": 1.7}`
- Signal history
- Simulated fills

### 🚨 Critical Notes
- **Shadow sanity: 45-90 min** - Must generate ≥1 signal, ≥1 P&L entry
- **Canary qualification** - Win rate ≥55%, Sharpe ≥0.8, DD <30%
- **Currently GRAY** - Shown as inactive in deployment blueprint (running separately)
- **PID 1543574** - Currently running as background process

---

## NODE 7: HIVE MIND

### 📌 Block Title: `HIVE MIND - Multi-Member Delegation`

### 🎯 Overall Purpose
**HIVE MIND** implements a delegation system where analysis is distributed across specialized "members" (Momentum, Scan, Trail, etc.). Each member provides independent assessments, and the system aggregates votes to reach consensus decisions. This reduces single-point-of-failure risk and leverages multiple perspectives.

### 📋 Jobs & Responsibilities
1. **Member Coordination** - Manages specialized analyst members
2. **Task Delegation** - Assigns analysis tasks to appropriate members
3. **Vote Aggregation** - Combines member assessments into consensus
4. **Quorum Enforcement** - Requires minimum member agreement
5. **Member Health Monitoring** - Tracks member availability/performance
6. **Conflict Resolution** - Handles disagreements between members
7. **Load Balancing** - Distributes analysis workload evenly

### 🔗 Integration Points
- **Wolf Packs** → Receives delegation requests from orchestrator
- **Risk Control** → Aggregate risk assessments from multiple members
- **ML Models** → May integrate ML member for intelligent voting
- **Swarm** → Works alongside swarm for coordinated delegation

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `rick_hive_mind.py` | `hive/` | 🔵 BLUE | Data & Analysis | Main hive coordination logic |
| `hive_mock_worker.py` | `pre_upgrade/headless/bin/` | 🔵 BLUE | Data & Analysis | Mock member implementation for testing |
| `hive_member_interface.py` | `hive/` | 🟣 PURPLE | Infrastructure | Abstract base class for hive members |

**Directory:** `/home/ing/RICK/R_H_UNI/hive/` (60 KB total)

### 🔄 Dependencies
- **Wolf Packs** (Strategy interface)
- **Logic** (Decision thresholds)
- `asyncio` (Async member coordination)
- **Swarm** (Coordinated delegation)

### 📤 Output
- Aggregated assessments (JSON): `{"consensus": "BUY", "votes": {"momentum": "BUY", "scan": "HOLD", "trail": "BUY"}, "confidence": 0.75}`
- Member health reports
- Quorum logs

### 🚨 Critical Notes
- **Quorum required** - Minimum member agreement threshold
- **Member specialization** - Each member has domain expertise
- **Async coordination** - Uses asyncio for parallel member queries
- **Mock mode available** - Can run with hive_mock_worker for testing

---

## NODE 8: CONNECTORS (FUTURES)

### 📌 Block Title: `CONNECTORS - Multi-Venue Futures Trading`

### 🎯 Overall Purpose
**CONNECTORS (FUTURES)** extends the system to perpetual futures markets across multiple venues (Binance, Bybit, OKX). It handles venue selection, dynamic leverage calculation (1-25x based on volatility), and emergency deleveraging during severe drawdowns. This node operates independently of spot brokers.

### 📋 Jobs & Responsibilities
1. **Venue Manager** - Selects optimal futures exchange (Binance/Bybit/OKX)
2. **Leverage Calculator** - Dynamically adjusts leverage 1-25x based on volatility
3. **Emergency Deleveraging** - Reduces leverage at severe/critical thresholds
4. **Futures Order Execution** - Perpetual contract order placement
5. **Funding Rate Monitoring** - Tracks funding rates across venues
6. **Liquidation Protection** - Monitors margin and prevents liquidation
7. **Cross-Venue Arbitrage** - (Future) Identifies funding arbitrage opportunities

### 🔗 Integration Points
- **Foundation** → Validates futures orders (same Charter rules)
- **Brokers** → Shares authentication patterns but operates independently
- **Wolf Packs** → Receives futures-specific signals
- **Risk Control** → Monitors futures exposure separately
- **ML Models** → Model C specializes in futures

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `venue_manager.py` | `connectors/futures/` | 🟢 GREEN | Execution | Binance/Bybit/OKX venue selection |
| `leverage_calculator.py` | `connectors/futures/` | 🟡 YELLOW | Safety & Risk | Dynamic 1-25x leverage based on volatility |
| `futures_engine.py` | `connectors/futures/` | 🟢 GREEN | Execution | Perpetual futures order execution |
| `__init__.py` | `connectors/futures/` | 🟣 PURPLE | Infrastructure | Package initialization |

**Directory:** `/home/ing/RICK/R_H_UNI/connectors/futures/` (80 KB total)

### 🔄 Dependencies
- **Foundation** (Charter validation)
- `ccxt` (Unified exchange API library)
- **Risk Control** (Leverage limits)
- **Configs** (`futures_venues.json`)

### 📤 Output
- Futures order confirmations
- Leverage adjustments
- Funding rate alerts
- Liquidation warnings

### 🚨 Critical Notes
- **Dynamic leverage** - 1-25x based on volatility (higher vol = lower leverage)
- **Emergency deleverage** - Automatic reduction at severe/critical levels
- **Independent risk pool** - Futures exposure tracked separately from spot
- **Model C specialization** - ML Model C trained for futures patterns

---

## NODE 9: MONITORING & DASHBOARDS

### 📌 Block Title: `MONITORING - Real-Time System Observation`

### 🎯 Overall Purpose
**MONITORING** provides real-time visibility into system health, trade performance, and operational status through dashboards, logs, and narration feeds. It enables human operators to observe system behavior without interrupting autonomous operation.

### 📋 Jobs & Responsibilities
1. **Rick Narration** - Human-readable system event stream
2. **P&L Tracking** - Real-time profit/loss with fees and slippage
3. **Keepalive Monitoring** - Heartbeat signals from all subsystems
4. **Dashboard Rendering** - Streamlit UI with metrics/charts
5. **Log Aggregation** - Centralized JSONL log collection
6. **Alert Generation** - Notifications for critical events
7. **Performance Metrics** - Sharpe, win rate, drawdown visualization

### 🔗 Integration Points
- **Ghost Engine** → Displays simulation results
- **Risk Control** → Shows circuit breaker status
- **Wolf Packs** → Displays active pack status
- **Brokers** → Shows connection health
- **ML Models** → Displays ML confidence scores

### 📂 File Inventory

| File | Path | Color | Category | Description |
|------|------|-------|----------|-------------|
| `rick_coach.py` | `pre_upgrade/headless/bin/` | ⚫ GRAY | Monitoring & Logs | Main Streamlit dashboard launcher |
| `narrate.py` | `pre_upgrade/headless/bin/` | ⚫ GRAY | Monitoring & Logs | Rick narration feed generator |
| `pnl_tail.py` | `pre_upgrade/headless/bin/` | ⚫ GRAY | Monitoring & Logs | Real-time P&L tracker |
| `narration.jsonl` | `pre_upgrade/headless/logs/` | ⚫ GRAY | Monitoring & Logs | Human-readable event log (29 MB) |
| `keepalive.log` | `logs/` | ⚫ GRAY | Monitoring & Logs | Heartbeat log (3.2 MB) |
| `pnl.jsonl` | `pre_upgrade/headless/logs/` | ⚫ GRAY | Monitoring & Logs | P&L tracking with fees/slippage |

**Directory:** Various (primary: `pre_upgrade/headless/`) (579 MB total including logs)

### 🔄 Dependencies
- `streamlit` (Dashboard framework)
- `plotly`, `altair` (Charting)
- `pandas` (Data processing)
- **All nodes** (Reads logs from everywhere)

### 📤 Output
- Streamlit UI (port 8501)
- JSONL logs (structured events)
- Alerts (JSON/email/Slack)
- Performance reports (PDF)

### 🚨 Critical Notes
- **Read-only** - Monitoring never modifies system state
- **Upgrade toggle enforced** - UI only runs when `.upgrade_toggle = OFF`
- **Narration feed** - 29 MB of human-readable events
- **Charter footer** - Must display "Charter Compliance Active | RR≥3.2 | Breaker -5% | PIN 841921"

---

# 📊 INTEGRATION FLOW EXAMPLES

## Example 1: Manual Trade Flow (ICT Signal)

```
1. Market Data (Brokers)
   └─> EUR_USD: 1.1605/1.1606
         ↓
2. Wolf Pack (ICT Strategy)
   └─> Signal: BUY EUR_USD @ 1.1605, SL 1.1575, TP 1.1701, RR 3.2
         ↓
3. Foundation Validation
   ├─> Timeframe: M15 ✅
   ├─> RR: 3.2 ✅
   ├─> Notional: $16,000 ✅
   └─> Hold: 4.5 hrs ✅
         ↓
4. Risk Control (OCO Validator)
   ├─> Stop-loss present ✅
   ├─> Take-profit present ✅
   └─> Position limit: 1/3 ✅
         ↓
5. Broker (OANDA)
   └─> Order placed, ID: 12345
         ↓
6. Monitoring (Narration)
   └─> "🟢 EUR_USD BUY executed @ 1.1605, RR 3.2:1"
```

## Example 2: ML-Augmented Trade Flow (Shadow Mode)

```
1. Wolf Pack Signal (ICT)
   └─> BUY EUR_USD @ 1.1605, RR 3.2
         ↓
2. ML Model A (Forex)
   ├─> Confidence: 87%
   ├─> Regime: Trending
   └─> Pattern: High-prob reversal ✅
         ↓
3. Hive Mind (Consensus)
   ├─> Momentum: BUY
   ├─> Scan: HOLD
   ├─> Trail: BUY
   └─> Consensus: BUY (2/3 votes)
         ↓
4. Foundation Validation
   └─> All checks pass ✅
         ↓
5. Ghost Engine (Shadow)
   └─> Simulation: Win (profit $520)
         ↓
6. Monitoring
   └─> "🟡 ML shadow: 87% confidence, simulated win $520"
```

## Example 3: Circuit Breaker Activation

```
1. Risk Control (P&L Monitor)
   └─> Daily P&L: -5.1% ❌
         ↓
2. Session Breaker
   ├─> Threshold breach detected
   ├─> HALT signal issued
   └─> All packs disabled
         ↓
3. Brokers
   ├─> Close all open positions
   └─> Disable new order submission
         ↓
4. Monitoring (Alert)
   └─> 🔴 CIRCUIT BREAKER: -5.1% daily loss
         ↓
5. Foundation (Audit)
   └─> Log breach event with timestamp
```

---

# 🎯 DEPLOYMENT SCENARIOS

## Scenario A: Ghost Mode (Current)
**Active Nodes:** Foundation, Brokers (data only), Wolf Packs, Ghost Engine  
**Inactive Nodes:** Risk Control (simulation), ML Models (shadow)  
**Purpose:** Validate strategy performance with live data, zero risk  
**Duration:** 45-90 minutes minimum

## Scenario B: Canary Mode (Next)
**Active Nodes:** Foundation, Brokers (execution), Wolf Packs, Risk Control  
**Inactive Nodes:** ML Models (shadow testing)  
**Risk:** 0.1% per trade, 1 concurrent position max  
**Purpose:** Real-money validation with minimal capital exposure  
**Duration:** 7 days minimum

## Scenario C: Live Mode (Production)
**Active Nodes:** All nodes except ML (ML in shadow)  
**Risk:** Full Charter limits (3.2:1 RR, $15k notional, 3 positions max)  
**Purpose:** Full production trading  
**ML Integration:** After canary passes, promote ML from shadow to active

---

# 📋 FILE CATEGORIES SUMMARY

## 🔴 RED (Strategy Logic) - 7 files
- `wolfpack_orchestrator.py`, `ict_strategy.py`, `smc_strategy.py`
- `momentum_pack.py`, `scan_pack.py`, `trail_pack.py`

## 🟡 YELLOW (Safety & Risk) - 6 files
- `session_breaker.py`, `oco_validator.py`, `risk_control_center.py`
- `smart_trailing.py`, `leverage_calculator.py`, `retry.py`

## 🟢 GREEN (Execution) - 5 files
- `oanda_connector.py`, `coinbase_connector.py`
- `venue_manager.py`, `futures_engine.py`, `live_ghost_engine.py`

## 🔵 BLUE (Data & Analysis) - 4 files
- `regime_detector.py`, `rick_hive_mind.py`, `hive_mock_worker.py`
- `test_ml_intelligence.py`

## 🟣 PURPLE (Infrastructure) - 8 files
- `rick_charter.py`, `stochastic_config.py`, `broker_interface.py`
- `hive_member_interface.py`, `position_sizer.py`, `launch_live_ghost.sh`
- `RICK_CHARTER_IMMUTABLE.md`, `PREPENDED_INSTRUCTIONS_IMMUTABLE.md`

## 🟠 ORANGE (ML & Intelligence) - 3 files
- `ml_models.py`, `pattern_learner.py`, `optimizer.py`

## ⚫ GRAY (Monitoring & Logs) - 6 files
- `rick_coach.py`, `narrate.py`, `pnl_tail.py`
- `narration.jsonl`, `keepalive.log`, `pnl.jsonl`

**Total Core Files:** 39 files across 7 categories

---

# 🔗 QUICK REFERENCE

## Critical PIN: `841921`
All destructive operations require this PIN.

## Critical Thresholds:
- **Min RR:** 3.2:1
- **Min Notional:** $15,000
- **Max Hold:** 6 hours
- **Daily Halt:** -5% P&L
- **Timeframes:** M15, M30, H1 only

## API Endpoints:
- **OANDA Live:** `https://api-fxtrade.oanda.com/v3`
- **Coinbase:** `https://api.coinbase.com`

## Key Directories:
- **Core Code:** `foundation/`, `brokers/`, `wolf_packs/`, `risk/`
- **ML:** `ml_learning/`
- **Logs:** `logs/`, `pre_upgrade/headless/logs/`
- **Configs:** `configs/`

---

*Developer Reference Manual v1.0*  
*Created: October 10, 2025*  
*Total Nodes Documented: 9*  
*Total Files Cataloged: 39*  
*Color Categories: 7*
