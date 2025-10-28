# 🛡️ GATED LOGIC - COMPLETE REFERENCE
**PIN: 841921 | Generated: October 21, 2025**

## 📍 EXECUTIVE SUMMARY

**Status:** ✅ **GATED LOGIC FOUND AND DOCUMENTED**

The gated logic exists in **TWO LOCATIONS** with different implementations:

1. **`foundation/margin_correlation_gate.py`** - Used by OANDA trading engine ✅ ACTIVE
2. **`R_H_UNI/plugins/position_guardian/rules.py`** - Comprehensive guardian system ✅ COMPLETE

---

## 🗺️ LOCATION MAP

```
📂 RICK_LIVE_PROTOTYPE/
│
├── 🛡️ foundation/margin_correlation_gate.py
│   ├── MarginCorrelationGate class (488 lines)
│   ├── Used by: oanda_trading_engine.py (lines 715-732)
│   ├── Status: ✅ ACTIVE in production
│   └── Functions:
│       ├── correlation_gate_any_ccy()       → Block same-side currency exposure
│       ├── margin_gate()                    → Block if margin > 35%
│       ├── pre_trade_gate()                 → Master validation (all gates)
│       ├── validate_stop_loss_distance()    → ATR-based SL validation
│       ├── time_stop_check()                → 3h/6h time caps
│       └── scale_out_recommendation()       → Auto-scale on margin breach
│
├── 🛡️ R_H_UNI/plugins/position_guardian/rules.py
│   ├── Position Guardian system (350 lines)
│   ├── Used by: Multi-broker orchestration, future integration
│   ├── Status: ✅ COMPLETE (not yet integrated with autonomous engine)
│   └── Functions:
│       ├── correlation_gate()               → USD exposure limits
│       ├── margin_governor()                → 35% margin cap
│       ├── pre_trade_hook()                 → Combined gate validation
│       ├── auto_breakeven_action()          → BE+5 at 1R or 25 pips
│       ├── time_stop_action()               → 3h/6h forced exits
│       ├── enforce_bootstrap_sl()           → Auto-set missing SL (20 pips)
│       ├── trailing_actions()               → Stage-based trailing (18p/12p)
│       └── tick_enforce()                   → Per-tick autopilot execution
│
└── 📄 R_H_UNI/docs/GUARDIAN_GATED_LOGIC.md
    └── Complete documentation of all 10 guardian rules

```

---

## 🔍 DETAILED GATE LOGIC BREAKDOWN

### 1️⃣ MARGIN & CORRELATION GATE (`foundation/margin_correlation_gate.py`)

**File:** `/home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/margin_correlation_gate.py`  
**Lines:** 488 total  
**Active In:** `oanda_trading_engine.py` (lines 34, 162, 715-732)

#### Key Parameters (Immutable)
```python
MARGIN_CAP_PCT = 0.35                  # 35% hard cap
MIN_ATR_BUFFER_PIPS = 18               # Minimum SL distance
TIME_STOP_3H_MINUTES = 180             # 3-hour check
TIME_STOP_6H_MINUTES = 360             # 6-hour forced exit
MIN_R_RATIO_AT_3H = 0.5                # Close if R < 0.5 at 3h
SCALE_OUT_TARGET_MARGIN_PCT = 0.25     # Target 25% after scale-out
```

#### Gate Functions

##### A. `correlation_gate_any_ccy(new_order, current_positions)` 
**Lines:** 148-190  
**Logic:**
```python
# Calculate currency bucket exposures
before_exposure = {'EUR': +16000, 'USD': +19000, 'CHF': -35000}
after_exposure = {'EUR': +26000, 'USD': +9000, 'CHF': -35000}

# Block if any currency increases in same direction
for ccy in after_exposure:
    if abs(after_exp) > abs(before_exp) and same_sign:
        return BLOCK  # "correlation_gate:CHF_bucket"
```

**Example Block:**
```
Current:  Long EUR/CHF 16k, Long USD/CHF 19k → CHF -35k
New:      Long EUR/USD 10k → EUR +10k, USD -10k
Result:   EUR increased from +16k to +26k (same long side)
Action:   ❌ BLOCKED → "correlation_gate:EUR_bucket"
```

##### B. `margin_gate(total_margin_used, new_order=None)`
**Lines:** 195-227  
**Logic:**
```python
current_pct = total_margin_used / account_nav

# Block if already over cap
if current_pct > 0.35:
    return BLOCK  # "margin_cap_exceeded: 58.0% > 35%"

# Block if new order would exceed
if new_order:
    projected_pct = (total_margin_used + order_margin) / account_nav
    if projected_pct > 0.35:
        return BLOCK  # "margin_cap_would_exceed: 38.0%"
```

##### C. `pre_trade_gate(new_order, positions, pending, total_margin)`
**Lines:** 232-257  
**Master gate that runs ALL checks:**
```python
def pre_trade_gate(...):
    # Check 1: Margin
    margin_result = self.margin_gate(total_margin_used, new_order)
    if not margin_result.allowed:
        return margin_result  # BLOCKED
    
    # Check 2: Correlation
    correlation_result = self.correlation_gate_any_ccy(new_order, positions)
    if not correlation_result.allowed:
        return correlation_result  # BLOCKED
    
    # All gates passed
    return HookResult(allowed=True, action="EXECUTE")
```

##### D. `validate_stop_loss_distance(entry, stop, symbol, atr)`
**Lines:** 262-296  
**ATR-based SL validation:**
```python
pip_size = 0.01 if "JPY" in symbol else 0.0001
distance_pips = abs(entry - stop) / pip_size

# Use ATR if available, else conservative 18-pip floor
min_distance = atr_pips if atr_value else 18

if distance_pips < min_distance:
    return False, "SL too tight: 12.5 pips < 18.0 pips"
```

##### E. `time_stop_check(position, minutes_held, r_multiple)`
**Lines:** 298-318  
**Charter time caps:**
```python
# 6-hour hard cap
if minutes_held >= 360:
    return "time_stop_6h_hard_cap"

# 3-hour underperformance
if minutes_held >= 180:
    if r_multiple < 0.5:
        return "time_stop_3h_underperforming (R=0.3 < 0.5)"
```

##### F. `scale_out_recommendation(margin_pct, positions)`
**Lines:** 323-350  
**Auto-scale when margin > 35%:**
```python
if margin_pct <= 0.35:
    return None  # No action needed

# Target 25% utilization
target = 0.25
scale_out_pct = 1.0 - (target / margin_pct)
scale_out_pct = min(scale_out_pct, 0.50)  # Max 50% reduction

# Returns weakest position to scale (lowest R multiple)
```

---

### 2️⃣ POSITION GUARDIAN (`R_H_UNI/plugins/position_guardian/rules.py`)

**File:** `/home/ing/RICK/RICK_LIVE_PROTOTYPE/R_H_UNI/plugins/position_guardian/rules.py`  
**Lines:** 350 total  
**Status:** ✅ COMPLETE (ready for integration)

#### Key Parameters (Tunable)
```python
PIP_BE_THRESHOLD = 25.0        # Breakeven trigger
BE_OFFSET_PIPS = 5.0           # BE+5
R_FOR_BE = 1.0                 # Also trigger at 1R
MINOR_TIME_HRS = 3.0           # First time check
MAJOR_TIME_HRS = 6.0           # Hard cap
HALF_R = 0.5                   # Min R at 3h
MARGIN_CAP = 0.35              # 35% hard cap

# Profit Autopilot
S2_START_PIPS = 40.0           # Stage 2 (2R or 40p)
S3_START_PIPS = 60.0           # Stage 3 (3R or 60p)
TRAIL_D2_PIPS = 18.0           # Stage 2 trailing distance
TRAIL_D3_PIPS = 12.0           # Stage 3 trailing distance
BOOTSTRAP_SL_PIPS = 20.0       # Auto-set missing SL
GIVEBACK_PCT = 0.40            # 40% giveback exit
```

#### Guardian Functions

##### A. `correlation_gate(order, positions)`
**Lines:** 289-296  
**USD exposure gate:**
```python
current = net_usd_exposure(positions)  # e.g., +35000 (long USD)
delta = usd_exposure_for(order)        # e.g., +10000 (buy EURUSD)
after = current + delta                # e.g., +45000

# Block if increases same-side exposure
increases_same_side = abs(after) > abs(current) and (after * current >= 0)
if increases_same_side:
    return BLOCK  # "correlation_gate: increases_net_USD_exposure"
```

##### B. `margin_governor(order, positions, acct)`
**Lines:** 299-309  
**Margin cap with hedge exception:**
```python
if acct.margin_utilization <= 0.35:
    return ALLOW

# If over cap, allow only if order reduces exposure
current = net_usd_exposure(positions)
delta = usd_exposure_for(order)
after = current + delta

if abs(after) <= abs(current):
    return ALLOW  # "margin_cap: allow_reduce_or_hedge_only"
else:
    return BLOCK  # "margin_cap: block_new_exposure"
```

##### C. `pre_trade_hook(order, positions, acct)`
**Lines:** 312-320  
**Combined gate validation:**
```python
def pre_trade_hook(...):
    # Gate 1: Correlation
    ck = correlation_gate(order, positions)
    if not ck.allowed:
        return ck
    
    # Gate 2: Margin
    mg = margin_governor(order, positions, acct)
    if not mg.allowed:
        return mg
    
    return HookResult(True)
```

##### D. `auto_breakeven_action(position)`
**Lines:** 177-188  
**BE+5 automation:**
```python
meets_r = (position.r_multiple >= 1.0)
meets_pips = (position.pips_open >= 25.0)

if meets_r or meets_pips:
    new_sl = entry_price + (5 * pip_size * direction)
    if new_sl better than current_sl:
        return {"type": "modify_sl", "new_sl": new_sl, "why": "auto_breakeven"}
```

##### E. `time_stop_action(position, now_utc)`
**Lines:** 191-206  
**Time-based exits:**
```python
age = now_utc - position.opened_at

# 6-hour hard cap
if age >= timedelta(hours=6):
    return {"type": "close", "why": "time_stop_6h"}

# 3-hour underperformance
if age >= timedelta(hours=3):
    if position.r_multiple < 0.5:
        return {"type": "close", "why": "time_stop_3h_lt_0.5R"}
```

##### F. `enforce_bootstrap_sl(position)`
**Lines:** 209-217  
**Auto-set missing SL:**
```python
if position.stop_loss is None:
    new_sl = entry_price - (20 * pip_size * direction)
    return {"type": "modify_sl", "new_sl": new_sl, "why": "bootstrap_hard_SL_OCO"}
```

##### G. `trailing_actions(position, state)`
**Lines:** 220-275  
**Stage-based trailing stop:**
```python
# Stage machine
stage = 0  # Initial
stage = 1  # At 1R or 25 pips → BE+5
stage = 2  # At 2R or 40 pips → Trail 18 pips
stage = 3  # At 3R or 60 pips → Trail 12 pips

# Giveback exit
if peak >= 40 pips:
    floor = peak * 0.6  # 40% giveback tolerance
    if current <= floor:
        return {"type": "close", "why": "peak_giveback_40pct"}

# Trailing stop ratchet
if stage >= 2:
    gap = 12 if stage >= 3 else 18
    target_sl = current_price - (gap * pip_size)
    if target_sl > current_sl:
        return {"type": "modify_sl", "new_sl": target_sl, "why": f"trail_stage_{stage}"}
```

##### H. `tick_enforce(positions, acct, now_utc)`
**Lines:** 323-343  
**Per-tick autopilot execution:**
```python
def tick_enforce(...):
    actions = []
    state = load_state()
    
    for position in positions:
        # Bootstrap SL
        a0 = enforce_bootstrap_sl(position)
        if a0: actions.append(a0)
        
        # Standard BE/time
        a1 = auto_breakeven_action(position)
        if a1: actions.append(a1)
        
        a2 = time_stop_action(position, now_utc)
        if a2: actions.append(a2)
        
        # Profit autopilot
        acts = trailing_actions(position, state)
        actions.extend(acts)
    
    save_state(state)
    return actions
```

---

## 📊 COMPARISON: TWO GATE SYSTEMS

| Feature | `margin_correlation_gate.py` | `position_guardian/rules.py` |
|---------|------------------------------|------------------------------|
| **Status** | ✅ Active in OANDA engine | ✅ Complete, not integrated |
| **Complexity** | 488 lines | 350 lines |
| **Margin Gate** | ✅ 35% hard cap | ✅ 35% with hedge exception |
| **Correlation Gate** | ✅ All currency buckets | ✅ USD exposure only |
| **Breakeven Logic** | ❌ Not included | ✅ BE+5 at 1R/25p |
| **Time Stops** | ✅ 3h/6h checks | ✅ 3h/6h forced exits |
| **Trailing Stop** | ❌ Not included | ✅ Stage-based (18p/12p) |
| **SL Validation** | ✅ ATR-based | ✅ Bootstrap (20p minimum) |
| **Giveback Exit** | ❌ Not included | ✅ 40% peak drawdown |
| **Scale-Out** | ✅ On margin breach | ❌ Not included |
| **State Management** | Stateless | ✅ Persistent (JSON) |
| **Integration** | `oanda_trading_engine.py` | Not yet connected |

---

## 🔗 INTEGRATION POINTS

### Current Active Integration (OANDA Engine)

**File:** `oanda_trading_engine.py`

**Import (Line 34):**
```python
from foundation.margin_correlation_gate import MarginCorrelationGate, Position, Order, HookResult
```

**Initialization (Lines 150-165):**
```python
# MARGIN & CORRELATION GUARDIAN GATES (NEW)
account_nav = account_info["nav"]
self.gate = MarginCorrelationGate(account_nav=account_nav)
self.current_positions = []  # Track for gate monitoring
self.pending_orders = []
self.display.success("🛡️  Margin & Correlation Guardian Gates ACTIVE")
```

**Pre-Trade Validation (Lines 715-732):**
```python
# 🛡️ PRE-TRADE GUARDIAN GATE CHECK
gate_order = Order(
    symbol=instrument,
    side="BUY" if action == "buy" else "SELL",
    units=position_size,
    price=entry_price,
    order_id="pending_" + instrument,
)

gate_result = self.gate.pre_trade_gate(
    new_order=gate_order,
    current_positions=self.current_positions,
    pending_orders=self.pending_orders,
    total_margin_used=account_info["margin_used"],
)

if not gate_result.allowed:
    self.display.error(f"❌ GUARDIAN GATE BLOCKED: {gate_result.reason}")
    # Order rejected, logged to narration.jsonl
    return
```

**Position Tracking (Lines 877-891):**
```python
# 🛡️ TRACK POSITION FOR GUARDIAN GATE ONGOING MONITORING
gate_position = Position(
    symbol=instrument,
    side="LONG" if action == "buy" else "SHORT",
    units=position_size,
    entry_price=entry_price,
    current_price=entry_price,
    pnl=0.0,
    pnl_pips=0.0,
    margin_used=notional * 0.02,
    position_id=trade_id,
)
self.current_positions.append(gate_position)
```

---

## 🚀 AUTONOMOUS ENGINE INTEGRATION GAPS

### What's Missing in `autonomous_decision_engine.py`

**Current State:**
- ❌ No `MarginCorrelationGate` import
- ❌ No pre-trade gate validation
- ❌ No swarm bot assignment per trade
- ❌ No per-trade guardian monitoring
- ❌ Uses fixed decision rules (not gated)

**What Should Be Added:**

#### 1. Import Gate System
```python
from foundation.margin_correlation_gate import MarginCorrelationGate, Position, Order, HookResult
```

#### 2. Initialize Gate in Main Loop
```python
# Get account info
acct = get_account_info()
gate = MarginCorrelationGate(account_nav=acct["nav"])
```

#### 3. Validate Before Opening Position
```python
# Before calling open_position()
gate_order = Order(
    symbol=signal["instrument"],
    side="BUY" if signal["direction"] == "BUY" else "SELL",
    units=calculated_units,
    price=entry_price,
    order_id=f"signal_{signal['instrument']}",
)

gate_result = gate.pre_trade_gate(
    new_order=gate_order,
    current_positions=existing_positions,
    pending_orders=[],
    total_margin_used=acct["margin_used"],
)

if not gate_result.allowed:
    print(f"  ❌ Gate blocked: {gate_result.reason}")
    log_decision(Decision(
        timestamp=now,
        instrument=signal["instrument"],
        trade_id="N/A",
        decision="GATE_REJECTION",
        reason=gate_result.reason,
        action_taken=False,
    ))
    continue  # Skip this signal
```

#### 4. Use Position Guardian for Management
```python
from plugins.position_guardian.rules import tick_enforce, AccountState

# In main loop, for each position
guardian_positions = [convert_to_guardian_position(p) for p in positions]
guardian_acct = AccountState(
    nav=acct["nav"],
    margin_used=acct["margin_used"],
    now_utc=datetime.now(timezone.utc),
)

# Get autopilot actions
actions = tick_enforce(guardian_positions, guardian_acct)

for action in actions:
    if action["type"] == "modify_sl":
        # Update stop loss
        set_stop_loss(action["position_id"], action["new_sl"])
    elif action["type"] == "close":
        # Close position
        close_full(action["position_id"])
```

---

## 📚 DOCUMENTATION LOCATIONS

### Comprehensive Gate Documentation

1. **`R_H_UNI/docs/GUARDIAN_GATED_LOGIC.md`**
   - Complete logic for all 10 guardian rules
   - Gated prompt examples
   - Code snippets for each gate
   - 248 lines of detailed documentation

2. **`R_H_UNI/docs/CHARTER.md`**
   - Immutable Charter rules
   - PIN 841921 enforcement
   - Correlation gate requirements
   - Pre-trade gate routing

3. **`R_H_UNI/README.md`**
   - Position Guardian pack overview
   - File structure
   - Integration guide
   - Test instructions

4. **`SYSTEM_COMPREHENSIVE_ANALYSIS.md`**
   - Part 4: Gate Logic Confirmation
   - 100% coverage audit
   - Active vs. inactive strategies

5. **`FUNCTIONAL_STATE_MAINTENANCE.md`**
   - Layer 3: Pre-Trade Guardian Gates
   - Gate validation testing
   - Immutable file protection

---

## ✅ VERIFICATION CHECKLIST

### Active Gate System Status

- [x] **Margin Gate** - Active in OANDA engine
- [x] **Correlation Gate** - Active in OANDA engine  
- [x] **Pre-Trade Validation** - Integrated at lines 715-732
- [x] **Position Tracking** - Tracked for ongoing monitoring
- [x] **Gate Rejections** - Logged to narration.jsonl
- [ ] **Autonomous Engine** - NOT YET INTEGRATED
- [ ] **Per-Trade Swarm Bots** - NOT IMPLEMENTED
- [ ] **Guardian Autopilot** - NOT CONNECTED
- [ ] **Breakeven Logic** - NOT IN AUTONOMOUS ENGINE
- [ ] **Trailing Stops** - NOT IN AUTONOMOUS ENGINE

---

## 🎯 NEXT STEPS FOR AUTONOMOUS ENGINE

### Priority 1: Add Pre-Trade Gates
1. Import `MarginCorrelationGate` 
2. Initialize gate with account NAV
3. Validate every signal before opening position
4. Log gate rejections to audit trail

### Priority 2: Integrate Position Guardian
1. Import `tick_enforce` from `position_guardian.rules`
2. Convert positions to Guardian format
3. Execute autopilot actions (BE+5, trailing, time-stops)
4. Replace fixed decision logic with dynamic guardian rules

### Priority 3: Per-Trade Swarm Assignment
1. Add `swarm_bot_id` field to Position dataclass
2. Create `assign_swarm_guardian(trade_id, instrument)`
3. Query swarm bot for position-specific recommendations
4. Use bot confidence in decision engine

### Priority 4: Enhanced Decision Engine
1. Replace 7-tier fixed rules with guardian autopilot
2. Use stage-based profit management (S1/S2/S3)
3. Implement giveback exits (40% peak drawdown)
4. Add trailing stops (18p/12p based on stage)

---

## 📞 SUPPORT & REFERENCES

**Charter PIN:** 841921  
**Gate Test Command:** `python3 foundation/margin_correlation_gate.py --diagnose`  
**Guardian Demo:** `python3 R_H_UNI/plugins/position_guardian/demo_now.py`

**Key Files:**
- `/home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/margin_correlation_gate.py`
- `/home/ing/RICK/RICK_LIVE_PROTOTYPE/R_H_UNI/plugins/position_guardian/rules.py`
- `/home/ing/RICK/RICK_LIVE_PROTOTYPE/oanda_trading_engine.py`
- `/home/ing/RICK/RICK_LIVE_PROTOTYPE/autonomous_decision_engine.py`

---

## 🏁 SUMMARY

✅ **Gated logic FOUND in 2 locations**  
✅ **Active in OANDA trading engine**  
✅ **Complete Position Guardian system ready**  
⚠️ **NOT YET integrated with autonomous engine**  
⚠️ **No per-trade swarm bot assignment**  

**Status:** Gate infrastructure exists and is production-ready. Autonomous engine needs integration to use these sophisticated guardian systems instead of current fixed rules.

**PIN:** 841921 | **Charter:** IMMUTABLE | **Gates:** ACTIVE (OANDA) | READY (Guardian)
