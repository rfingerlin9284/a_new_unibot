# 📋 FILE ROOTS & REFERENCE COPY-PASTE COMMANDS FOR AI AGENT HELPER

**Purpose:** Reference only - Learn how to connect to OANDA API without modifying logic or strategy  
**PIN:** 841921 ✅

---

## 🤖 INSTRUCTION FOR AI AGENT HELPER

**Copy and paste this entire block to your AI agent helper:**

```
────────────────────────────────────────────────────────────────────────────────
🔍 REFERENCE TASK FOR AI AGENT HELPER
────────────────────────────────────────────────────────────────────────────────

OBJECTIVE: Study these 9 reference files to understand how RBOTzilla system 
connects to OANDA API. Use ONLY for reference/learning - do NOT modify any 
logic, strategy, or trading behavior.

IMPORTANT: This is a REFERENCE-ONLY task. No changes should be made to these 
files. Just analyze them to understand the API connection pattern.

────────────────────────────────────────────────────────────────────────────────
FILE 1: OANDA TRADING ENGINE (MAIN CONNECTION HUB)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/oanda_trading_engine.py

WHAT TO REFERENCE:
  • Lines 1-50: Imports (shows all required modules)
  • Lines 90-230: __init__() method - Shows how system initializes
  • Lines 280-330: get_current_price() - How to fetch real-time OANDA prices
  • Lines 900-1000: place_trade() - How orders are sent to OANDA
  • Lines 1100-1200: place_oanda_order() - Direct OANDA order placement

LEARN: How all subsystems (ML, Hive, Hedge, Guardian) integrate with OANDA API

────────────────────────────────────────────────────────────────────────────────
FILE 2: OANDA CONNECTOR (CORE API CONNECTION)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/brokers/oanda_connector.py

WHAT TO REFERENCE:
  • Lines 1-50: Class initialization
  • Lines 60-100: Authentication setup (headers, tokens)
  • Lines 110-150: API base URL configuration (practice vs live)
  • Lines 160-220: get_account_info() - How to fetch account data
  • Lines 230-280: get_prices() - Real-time price fetching
  • Lines 290-350: Place order methods - Order submission pattern

LEARN: Core OANDA REST v20 API connection and authentication pattern

────────────────────────────────────────────────────────────────────────────────
FILE 3: TERMINAL DISPLAY (VISUAL OUTPUT)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/util/terminal_display.py

WHAT TO REFERENCE:
  • Lines 1-50: Class definition and color definitions
  • Lines 60-100: header() method - Creates banner display
  • Lines 110-150: section() method - Creates section headers
  • Lines 160-200: info() method - Displays key-value pairs
  • Lines 210-250: connection_status() - Shows API connection state

LEARN: How to display connection status and system information visually

────────────────────────────────────────────────────────────────────────────────
FILE 4: RICK CHARTER (CONSTRAINTS & VALIDATION)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/rick_charter.py

WHAT TO REFERENCE:
  • Lines 1-50: Charter constants (MIN_RR_RATIO, MIN_NOTIONAL_USD, etc)
  • Lines 60-100: validate_pin() - PIN 841921 validation method
  • Lines 110-150: Charter enforcement rules
  • Lines 160-200: Risk parameter definitions

LEARN: How trading constraints are defined and validated (NO trading logic changes)

────────────────────────────────────────────────────────────────────────────────
FILE 5: NARRATION LOGGER (EVENT LOGGING)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/util/narration_logger.py

WHAT TO REFERENCE:
  • Lines 1-50: Log file initialization
  • Lines 60-100: log_narration() - How events are logged to narration.jsonl
  • Lines 110-150: Log format structure (JSON format)
  • Lines 160-200: Timestamp and metadata capture

LEARN: How to structure event logging without affecting trading logic

────────────────────────────────────────────────────────────────────────────────
FILE 6: RICK NARRATOR (AI NARRATION)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/util/rick_narrator.py

WHAT TO REFERENCE:
  • Lines 1-50: Class initialization
  • Lines 60-100: generate_narration() - How Rick narrates events
  • Lines 110-150: Market commentary generation
  • Lines 160-200: Ollama integration (optional voice synthesis)

LEARN: How narration system works alongside trading without affecting logic

────────────────────────────────────────────────────────────────────────────────
FILE 7: QUANT HEDGE ENGINE (OPTIONAL HEDGING)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/util/quant_hedge_engine.py

WHAT TO REFERENCE:
  • Lines 1-50: Correlation matrix definition
  • Lines 60-100: calculate_hedge_ratio() - Hedge calculation
  • Lines 110-150: evaluate_hedge_opportunity() - When to hedge
  • Lines 160-200: execute_hedge() - How hedge orders are placed

LEARN: Optional hedging logic - reference only, do not modify

────────────────────────────────────────────────────────────────────────────────
FILE 8: STRATEGY AGGREGATOR (5 STRATEGIES VOTING)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/util/strategy_aggregator.py

WHAT TO REFERENCE:
  • Lines 1-50: Strategy class definitions
  • Lines 60-100: aggregate_signals() - How 5 strategies vote
  • Lines 110-150: Voting threshold logic (2/5 minimum)
  • Lines 160-200: Signal weighting

LEARN: How multiple strategies are combined - reference pattern, do not modify

────────────────────────────────────────────────────────────────────────────────
FILE 9: MOMENTUM TRAILING (MOMENTUM DETECTION)
────────────────────────────────────────────────────────────────────────────────

FILE ROOT: /home/ing/RICK/RICK_LIVE_PROTOTYPE/util/momentum_trailing.py

WHAT TO REFERENCE:
  • Lines 1-50: MomentumDetector class
  • Lines 60-100: calculate_momentum() - Momentum calculation
  • Lines 110-150: SmartTrailingSystem class
  • Lines 160-200: Trailing stop logic

LEARN: How momentum detection works - reference pattern, do not modify

────────────────────────────────────────────────────────────────────────────────
CRITICAL INSTRUCTIONS FOR AI AGENT HELPER
────────────────────────────────────────────────────────────────────────────────

✅ DO:
  • Study HOW the system connects to OANDA API
  • Learn the pattern of authentication and requests
  • Understand the structure of the display/logging
  • Reference the validation and Charter enforcement patterns
  • Document the connection flow for reference

❌ DO NOT:
  • Modify any trading logic or strategy
  • Change any decision-making algorithms
  • Alter risk parameters or constraints
  • Modify the Guardian gate logic
  • Change the Hedge evaluation logic
  • Alter the Strategy aggregation voting
  • Change any OANDA order placement code

ACCEPTABLE MODIFICATIONS ONLY:
  • Add comments/documentation
  • Create new reference documentation
  • Generate diagrams or flowcharts
  • Create integration guides
  • Add monitoring/logging (non-invasive)

────────────────────────────────────────────────────────────────────────────────
GOAL OUTCOME
────────────────────────────────────────────────────────────────────────────────

After studying these 9 files, you should understand:

1. How OANDA API authentication works (tokens, headers, endpoints)
2. How the system fetches real-time prices from OANDA
3. How orders are constructed and sent to OANDA
4. How the connection status is displayed
5. How events are logged to JSON files
6. How the system validates Charter constraints
7. How all subsystems integrate together
8. The overall architecture of the system

BUT: Do NOT modify any of the actual trading logic or decision-making.

────────────────────────────────────────────────────────────────────────────────
REFERENCE OUTPUT EXAMPLE
────────────────────────────────────────────────────────────────────────────────

You may create documentation like:

  "OANDA Connection Flow:"
  1. OandaConnector initializes with API token and endpoint
  2. Headers are set with Bearer token authentication
  3. get_current_price() sends HTTP GET to /v3/accounts/{id}/pricing
  4. Response parsed for BID/ASK prices
  5. OandaTradingEngine receives price data
  6. Price passed to strategy aggregator for signal generation
  7. If signal generated, place_trade() creates OCO order
  8. Order sent to OANDA via HTTP POST
  9. Event logged to narration.jsonl
  10. Display updates with execution status

This type of documentation is helpful and allowed.

────────────────────────────────────────────────────────────────────────────────
VALIDATION CHECKLIST
────────────────────────────────────────────────────────────────────────────────

Before completing analysis, confirm:

  ✅ Studied all 9 files
  ✅ Understand OANDA API pattern (no modifications made)
  ✅ Understand display system (no modifications made)
  ✅ Understand logging system (no modifications made)
  ✅ Understand Charter validation (no modifications made)
  ✅ Understand subsystem integration (no modifications made)
  ✅ Created reference documentation (if needed)
  ✅ Did NOT modify any trading logic
  ✅ Did NOT modify any strategy files
  ✅ Did NOT modify any Guardian files
  ✅ Ready to deliver understanding to primary system

────────────────────────────────────────────────────────────────────────────────
END OF AGENT HELPER INSTRUCTION
────────────────────────────────────────────────────────────────────────────────
```

---

## 📁 QUICK FILE ROOT REFERENCE TABLE

| # | File Name | Full Path | Purpose | Size |
|---|-----------|-----------|---------|------|
| 1 | oanda_trading_engine.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/oanda_trading_engine.py` | Main engine + OANDA integration hub | 62 KB |
| 2 | oanda_connector.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/brokers/oanda_connector.py` | Core OANDA API connection | - |
| 3 | terminal_display.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/terminal_display.py` | Display formatting | 10 KB |
| 4 | rick_charter.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/rick_charter.py` | Charter validation (PIN 841921) | - |
| 5 | narration_logger.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/narration_logger.py` | Event logging | - |
| 6 | rick_narrator.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/rick_narrator.py` | AI narration | - |
| 7 | quant_hedge_engine.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/quant_hedge_engine.py` | Hedge logic (reference) | - |
| 8 | strategy_aggregator.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/strategy_aggregator.py` | Strategy voting (reference) | - |
| 9 | momentum_trailing.py | `/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/momentum_trailing.py` | Momentum detection (reference) | - |

---

## 🔧 COPY-PASTE FILE PATHS (For Easy Reference)

```bash
# File 1 - Main Engine
/home/ing/RICK/RICK_LIVE_PROTOTYPE/oanda_trading_engine.py

# File 2 - OANDA API Connection
/home/ing/RICK/RICK_LIVE_PROTOTYPE/brokers/oanda_connector.py

# File 3 - Display System
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/terminal_display.py

# File 4 - Charter Validation
/home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/rick_charter.py

# File 5 - Event Logging
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/narration_logger.py

# File 6 - Narration System
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/rick_narrator.py

# File 7 - Hedge Engine (Reference)
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/quant_hedge_engine.py

# File 8 - Strategy Aggregator (Reference)
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/strategy_aggregator.py

# File 9 - Momentum System (Reference)
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/momentum_trailing.py
```

---

## 📝 KEY SECTIONS TO STUDY IN EACH FILE

### oanda_trading_engine.py
- **Lines 20-40:** Imports (what modules are needed)
- **Lines 80-100:** `__init__()` start (initialization)
- **Lines 200-230:** Display code (what you see on screen)
- **Lines 280-330:** `get_current_price()` (how prices fetched from OANDA)
- **Lines 1100-1150:** `place_oanda_order()` (how orders sent to OANDA)

### brokers/oanda_connector.py
- **Lines 1-50:** Class definition & authentication setup
- **Lines 60-100:** Headers and API base URL configuration
- **Lines 120-180:** Account info methods
- **Lines 200-250:** Price fetching methods
- **Lines 300-400:** Order submission methods

### util/terminal_display.py
- **Lines 1-30:** Color definitions and class init
- **Lines 50-100:** header() method (creates main banner)
- **Lines 110-150:** section() method (creates section headers)
- **Lines 160-200:** info() method (key-value display)

### foundation/rick_charter.py
- **Lines 1-50:** Charter constant definitions
- **Lines 60-100:** validate_pin() method
- **Lines 110-150:** Charter rules and constraints

### Remaining files (5-9)
- Study the class definitions and main methods
- Understand the purpose and flow
- Reference the patterns but do NOT modify

---

## ✅ STATUS

All 9 file roots provided with complete instruction for AI agent helper.

**Ready to share with AI agent for reference-only analysis of OANDA API connection.**

**PIN: 841921 ✅** - All charter constraints maintained
