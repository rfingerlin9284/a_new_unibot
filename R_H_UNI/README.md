# R_H_UNI Self-Contained Pack — Complete Index

## Overview
This pack includes all Position Guardian logic, gated upgrade workflows, autopilot rules, Charter, prompts, and tools needed to operate the RICK_LIVE_PROTOTYPE system autonomously.

## Directory Structure

```
R_H_UNI/
├── config/
│   └── reactive_actions.yaml         # BE+5, trailing, time-caps, giveback, gates
├── docs/
│   ├── CHARTER.md                     # Risk & trade rules (immutable)
│   ├── GATED_UPGRADES_MODIFICATIONS_CONFIRMED.md  # PIN-gated upgrade flow
│   └── GUARDIAN_GATED_LOGIC.md        # Position Guardian rules & prompts
├── logs/
│   ├── guardian.log                   # Daemon narration
│   ├── guardian_state.json            # Persistent peak/scale state
│   ├── guardian_metrics.json          # Performance counters
│   └── files_index.json               # Audit trail (read-only)
├── plugins/
│   └── position_guardian/
│       ├── __init__.py                # Exports Position, Order, AccountState, hooks
│       ├── rules.py                   # Core logic (gates, autopilot, time-stops)
│       ├── manager_integration.py     # PositionGuardianManager (pg_trade entry)
│       ├── guardian_daemon.py         # Tick enforce daemon (--loop 30 --live)
│       ├── profit_tracker.py          # PnL and R-multiple tracking
│       ├── demo_now.py                # Standalone demo
│       └── brokers/
│           └── oanda_adapter.py       # OANDA practice/live snapshot & execution
├── prompts/
│   ├── prelude.md                     # Self-contained file rule + guardian assumptions
│   └── prompt_modes.yaml              # Commander, guardian, scribe, fixer, scout modes
├── scripts/
│   └── audit_sync.sh                  # CLEAN-first sync (optional) + files index
├── tools/
│   └── status.py                      # NAV, margin, net USD, position flags (BE+5, trail, time)
├── Makefile                           # deps, audit, status, guardian, trade placeholders
└── requirements.txt                   # requests, python-dotenv
```

## Core Components

### 1. Position Guardian (`plugins/position_guardian/`)

#### `rules.py`
- **Pre-Trade Gates:**
  - `correlation_gate()` — blocks orders that increase net USD exposure same side
  - `margin_gate()` — blocks if margin > 35%
  - `pre_trade_hook()` — enforces both gates before order execution

- **Autopilot Rules:**
  - `auto_breakeven_action()` — SL → BE+5 at ≥1R or ≥25 pips
  - `time_stop_action()` — close at 6h; close at 3h if <0.5R
  - `trail_action()` — 18p trail at 40+ pips; 12p trail at 60+ pips
  - `giveback_exit()` — close if 40% drop from peak pips
  - `scale_out_action()` — 50% at 1.5R/35p; 25% at 2.5R/55p
  - `bootstrap_sl()` — ensure SL exists (20 pips default)
  - `tl_dr_actions()` — returns list of all applicable actions for current positions

#### `manager_integration.py`
- **PositionGuardianManager** class
  - `pg_trade(symbol, side, units)` — main gate for all orders
  - `tick_enforce_positions()` — applies autopilot on every tick/minute
  - `report()` — metrics (blocked orders, BE applied, exits, profit)

#### `guardian_daemon.py`
- Runs continuous loop (default 30s)
- Snapshots positions & account via OANDA adapter
- Calls `tl_dr_actions()` and applies modifications
- Logs to `logs/guardian.log`
- Flags: `--loop N`, `--once`, `--live` (else dry-run)

#### `brokers/oanda_adapter.py`
- **OandaClient** class
  - Reads OANDA practice/live creds from env
  - `snapshot_positions_and_account()` — returns (positions, account, metadata)
  - `set_stop_loss(trade_id, price)` — modify SL
  - `close_trade_all(trade_id)` — close full position
  - `close_trade_partial(trade_id, units)` — reduce position

### 2. Documentation (`docs/`)

#### `CHARTER.md`
- Risk parameters: min $15k notional, 3 max concurrent, 6h hold cap, margin ≤35%
- Exit logic: BE+5, trailing, time-stops, giveback, partial scales
- Compliance: all orders via `pg_trade` gate

#### `GATED_UPGRADES_MODIFICATIONS_CONFIRMED.md`
- PIN 841921 gated workflow
- `.upgrade_toggle` file controls live mode
- Requires double PIN + 5-word explanation
- Pre-upgrade backups + audit logs
- Write-only upgrade folder (`DASH_SYSTEM_UPGRADE/live/`)

#### `GUARDIAN_GATED_LOGIC.md`
- Detailed logic for each gate and autopilot rule
- Gated prompt examples (e.g., "EURUSD buy blocked: increases long USD")
- Integration flow: `pg_trade` CLI and daemon mode
- Summary table of all triggers/actions

### 3. Configuration (`config/`)

#### `reactive_actions.yaml`
- `autobreakeven`: r_multiple: 1.0, pip_threshold: 25, be_offset_pips: 5
- `time_stops`: minor_hours: 3, minor_min_r: 0.5, major_hours: 6
- `trailing`: start_pips: 40, tighten_pips: 60, atr_mult_stage2/3, min_distance: 8
- `scale_outs`: [1.5R/35p → 50%, 2.5R/55p → 25%]
- `giveback_exit`: percent: 0.40
- `gates`: margin_cap: 0.35, usd_correlation: true
- `sessions`: off_hours_tighten: true, friday_exit_utc: "20:55"

### 4. Tools (`tools/`)

#### `status.py`
- Reads OANDA practice creds from env or `env_new.env` in project root
- Fetches NAV, margin_used, open positions
- Computes margin utilization, net USD exposure
- Flags each position: BE+5 eligible, trail start/tighten, 3h/6h close
- Warns if margin > 35% or single-sided USD exposure

### 5. Prompts (`prompts/`)

#### `prelude.md`
- Self-contained file rule (no external deps unless configured)
- Orders must route via `pg_trade`
- Guardian enforces BE+5, time-stops, trailing, scale-outs, giveback
- Session awareness: avoid weekend exposure, tighten off-hours
- Prioritize capital preservation: margin ≤35% before adding risk

#### `prompt_modes.yaml`
- **commander**: orchestrate strategies, reduce leverage when in doubt, self-contained
- **guardian**: enforce all gates and autopilot rules
- **scribe**: log every action with full context (pair, age, R, ATR, peak)
- **fixer**: auto-install missing deps, self-heal configs
- **scout**: propose entries only if margin ≤35% and USD exposure balanced

### 6. Scripts (`scripts/`)

#### `audit_sync.sh`
- Syncs from `/home/ing/RICK/RICK_LIVE_CLEAN` if present (optional)
- Builds `docs/files_index.json` with path/size/mtime/sha256 for all files
- Locks index read-only
- Gracefully skips if CLEAN source missing (self-contained mode)

### 7. Makefile

**Targets:**
- `make deps` — installs python-dotenv, requests via pip
- `make audit` — runs audit_sync.sh
- `make status` — runs tools/status.py (NAV, margin, flags)
- `make guardian.start/stop/logs` — placeholders for systemd service (to be wired)
- `make trade.buy/sell SYMBOL=... UNITS=... [DRY=1]` — placeholders for `pg_trade` CLI

## Integration Flow

### Pre-Trade (Order Entry)
1. User/strategy calls: `make trade.buy SYMBOL=GBPUSD UNITS=10000`
2. Makefile invokes: `pg_trade --venue oanda --symbol GBPUSD --side buy --units 10000`
3. `pg_trade` loads PositionGuardianManager
4. Calls `pre_trade_hook(order, positions, account)`
5. Checks:
   - Correlation gate: does this increase net USD same side?
   - Margin gate: is margin_used/NAV > 35%?
6. If blocked → log reason → exit
7. If allowed → execute via `OandaClient.place_order()`

### Tick Enforce (Autopilot)
1. Daemon runs: `python3 guardian_daemon.py --loop 30 --live`
2. Every 30s:
   - `OandaClient.snapshot_positions_and_account()`
   - `tl_dr_actions(positions, account, now_utc)`
   - Returns list of actions (modify_sl, close, close_partial, advice)
3. For each action:
   - `modify_sl` → `OandaClient.set_stop_loss()`
   - `close` → `OandaClient.close_trade_all()`
   - `close_partial` → `OandaClient.close_trade_partial()`
4. Log action + reason to `logs/guardian.log`
5. Update metrics in `logs/guardian_metrics.json`

### Status Check
1. Run: `make status`
2. Fetches account summary & open positions from OANDA
3. Prints:
   - UTC timestamp
   - NAV, margin used, utilization %
   - Net USD exposure (+ = long, - = short)
   - Warnings: margin > 35%, single-sided USD
   - Per position: symbol, side, units, pips, age, flags
4. Flags: BE+5 eligible, trail start, trail tighten, 3h <0.5R close, 6h cap close

## Gated Upgrade Workflow

### Activation (PIN 841921)
1. Run: `bash vscode_agent_run_live_check.sh`
2. Enter PIN: 841921 (twice)
3. Provide 5-word explanation
4. Script creates pre-upgrade backup: `pre_upgrade_backups/pre_live_backup_[TS].tar.gz`
5. Generates upgrade artifacts in `DASH_SYSTEM_UPGRADE/live/`
6. Writes: `echo ON > .upgrade_toggle`
7. Wrappers detect toggle and load upgrade code

### Revert
```bash
echo OFF > .upgrade_toggle
```

### Audit
- Backup location logged in `pre_upgrade_backups/enable_live_audit_[TS].log`
- Originals remain unmodified
- Upgrade artifacts isolated in write-only folder

## Quick Start

### Setup
```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE/R_H_UNI
make deps
make audit
```

### Check Status
```bash
make status
```

### Start Guardian Daemon (Dry-Run)
```bash
python3 plugins/position_guardian/guardian_daemon.py --loop 30
```

### Start Guardian Daemon (Live)
```bash
python3 plugins/position_guardian/guardian_daemon.py --loop 30 --live
```

### Test Pre-Trade Gate (Dry-Run)
```bash
make trade.buy SYMBOL=GBPUSD UNITS=10000 DRY=1
```

### View Guardian Logs
```bash
tail -f logs/guardian.log
```

### View Metrics
```bash
cat logs/guardian_metrics.json
```

## Files Included

- **Core Logic:** 350+ lines of gated rules (correlation, margin, BE+5, trailing, time-stops, giveback, scale-outs)
- **Broker Adapters:** OANDA practice/live snapshot & execution (set SL, close, pricing)
- **Manager:** PositionGuardianManager with metrics tracking (blocked orders, BE applied, exits)
- **Daemon:** Continuous tick enforce with dry-run/live modes
- **Documentation:** Charter, gated upgrades flow (PIN 841921), full guardian logic reference
- **Tools:** Status snapshot with margin/USD exposure warnings and position flags
- **Prompts:** Self-contained prelude + 5 agent modes (commander, guardian, scribe, fixer, scout)
- **Config:** Reactive actions YAML with all thresholds
- **Makefile:** Automation for deps, audit, status, and placeholders for guardian/trade

## Self-Contained Operation

- All files under `/home/ing/RICK/RICK_LIVE_PROTOTYPE/R_H_UNI`
- No external project dependencies
- Graceful fallback if CLEAN source missing
- Reads env from project root (`env_new.env`)
- Logs to local `logs/` directory
- Can operate independently without external folders

## PIN-Gated Deployment

- Live trading requires PIN 841921
- Double entry + 5-word explanation
- Pre-upgrade backups mandatory
- Audit trail for all activations
- Instant revert via toggle file

All Position Guardian logic, gated prompts, Charter compliance, and autopilot rules are now included and self-contained in this pack.
