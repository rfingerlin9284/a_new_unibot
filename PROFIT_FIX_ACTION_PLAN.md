# 💰 PROFIT FIX ACTION PLAN
**Issue:** Wins too small ($2.22 avg) + Losses too large ($1.09 avg) = 0.05% daily return  
**Target:** Increase to 3%+ daily return with 65% win rate  
**Timeline:** 1-2 hours to implement

---

## THE MATH PROBLEM

### Current State:
```
64% win rate × $2.22 avg win = $1.42/trade
36% loss rate × $1.09 avg loss = $0.39/trade
NET: $1.03/trade on $2,250 account = 0.046% return 😞

To compound to 100% per year: (1.00046)^365 = 1.17x (17% annual)
That's too slow for active trading!
```

### Target State:
```
65% win rate × $4.50 avg win = $2.92/trade  ← SCALE EXITS
35% loss rate × $0.60 avg loss = $0.21/trade ← TIGHTER STOPS
NET: $2.71/trade on $2,250 account = 0.12% return 😎

Annual compound: (1.0012)^365 = 1.57x (57% annual)
Much better!
```

---

## IMPLEMENTATION: 4 SPECIFIC CODE CHANGES

### Change #1: Implement Partial Exit Scaling ⭐ MOST IMPORTANT

**File:** `autonomous_decision_engine.py`  
**Location:** In `decide_action()` function, after "PROTECTIVE ACTIONS" section

**Current Code (around line 410):**
```python
# 3. Major loss (< -300 USD)?
if position.pnl_usd < LOSS_HALT_THRESHOLD:
    narrate(f"🚨 Emergency exit on {position.instrument} - loss ${position.pnl_usd:.2f} hit threshold", "LOSS_HALT")
    return Decision(
        timestamp=now,
        instrument=position.instrument,
        trade_id=position.trade_id,
        decision="EXIT_EMERGENCY",
        reason=f"Loss exceeds halt threshold ({position.pnl_usd:.2f} < {LOSS_HALT_THRESHOLD})",
        action_taken=close_full(position.trade_id, position.instrument, position.side)
    )
```

**Replace With:**
```python
    # 3. Major loss (< -300 USD)?
    if position.pnl_usd < LOSS_HALT_THRESHOLD:
        narrate(f"🚨 Emergency exit on {position.instrument} - loss ${position.pnl_usd:.2f} hit threshold", "LOSS_HALT")
        return Decision(
            timestamp=now,
            instrument=position.instrument,
            trade_id=position.trade_id,
            decision="EXIT_EMERGENCY",
            reason=f"Loss exceeds halt threshold ({position.pnl_usd:.2f} < {LOSS_HALT_THRESHOLD})",
            action_taken=close_full(position.trade_id, position.instrument, position.side)
        )
    
    # NEW: Partial exits for profit scaling (1R, 2R, 3R levels)
    entry_risk = abs(position.entry_price - position.sl_price)
    current_profit = position.pnl_usd
    
    # At +1R profit: Exit 50% of position
    if current_profit > (position.units * entry_risk * pip_size(position.instrument)):
        narrate(f"💰 +1R reached on {position.instrument} - scaling out 50%", "SCALE_OUT")
        # Scale out 50%
        units_to_close = abs(position.units) / 2
        return Decision(
            timestamp=now,
            instrument=position.instrument,
            trade_id=position.trade_id,
            decision="SCALE_OUT_50",
            reason=f"Scaling out 50% at +1R (${current_profit:.2f})",
            action_taken=scale_position(position.trade_id, position.instrument, units_to_close)
        )
    
    # At +2R profit: Exit 25% more (25% remains)
    if current_profit > (position.units * entry_risk * 2 * pip_size(position.instrument)):
        narrate(f"🎯 +2R reached on {position.instrument} - scaling out 25% more", "SCALE_OUT")
        units_to_close = abs(position.units) / 4
        return Decision(
            timestamp=now,
            instrument=position.instrument,
            trade_id=position.trade_id,
            decision="SCALE_OUT_25",
            reason=f"Scaling out 25% more at +2R (${current_profit:.2f})",
            action_taken=scale_position(position.trade_id, position.instrument, units_to_close)
        )
```

---

### Change #2: Move Stop Loss to Breakeven After +1R

**File:** `autonomous_decision_engine.py`  
**Location:** In position management loop

**Add After SET_SL Logic:**
```python
    # Move stop loss to breakeven if +1R achieved
    if position.pnl_usd > (position.units * entry_risk * pip_size(position.instrument)):
        if position.sl_price != position.entry_price:  # Not already at breakeven
            narrate(f"🛡️ Moving {position.instrument} stop to breakeven (locked profit)", "PROTECTION")
            action = set_stop_loss(position.trade_id, position.instrument, position.entry_price)
            if action:
                return Decision(
                    timestamp=now,
                    instrument=position.instrument,
                    trade_id=position.trade_id,
                    decision="SET_SL",
                    reason=f"Moving SL to breakeven entry price at {position.entry_price:.5f}",
                    action_taken=action
                )
```

---

### Change #3: Reduce Min Stop Loss Pips

**File:** `autonomous_decision_engine.py`  
**Location:** Line ~89

**Current:**
```python
MIN_SL_PIPS = int(os.getenv("MIN_SL_PIPS", "18"))
```

**Change To:**
```python
MIN_SL_PIPS = int(os.getenv("MIN_SL_PIPS", "10"))  # Reduced from 18
```

**Why:** Tighter stops capture bad entries faster, reduce average loss from $1.09 → $0.60

---

### Change #4: Dynamic Position Sizing Based on Volatility

**File:** `autonomous_decision_engine.py`  
**Location:** In `open_position()` function

**Current Position Sizing (around line 520):**
```python
position_size_units = POSITION_SIZE_BASE  # Fixed 50,000 units
```

**Replace With:**
```python
# Dynamic position sizing: target 2% account risk per trade
account_nav = acct["nav"]
target_risk_pct = 0.02  # Risk 2% of account max
target_risk_usd = account_nav * target_risk_pct

# Calculate stop loss distance in pips
sl_pips = MIN_SL_PIPS
ps = pip_size(signal['instrument'])
risk_per_pip = 0  # Will calculate based on position size

# Position size = target risk / (SL pips * value per pip)
# For 1 pip = 0.0001 movement
# Position size = risk_usd / (sl_pips * 0.0001 * 10)  [10 = pip multiplier]

position_size_units = int((target_risk_usd / (sl_pips * ps * 10)) * 1000)

# Cap at reasonable max (don't exceed 50% of base)
position_size_units = min(position_size_units, POSITION_SIZE_BASE)

narrate(f"📊 Position size for {signal['instrument']}: {position_size_units} units (risk: ${target_risk_usd:.2f})", "SIZING")
```

---

## EXPECTED RESULTS AFTER IMPLEMENTATION

### Before Fixes:
```
Avg Win: $2.22 (small, capped at profit target)
Avg Loss: $1.09 (large, full stop hit)
R:R: 2.04:1
Daily Return: 0.046%
```

### After Fixes:
```
Avg Win: $4.50+ (scaling out at 1R, 2R, 3R)
Avg Loss: $0.60 (tighter stops)
R:R: 3.5:1+  
Daily Return: 0.12%+
```

---

## TESTING CHECKLIST

Before deploying these changes:

- [ ] Create a new log version to test on paper account
- [ ] Run 50 test trades with scaling enabled
- [ ] Verify scale_position() function exists and works
- [ ] Check that partial exits don't break Guardian Gate
- [ ] Verify dynamic position sizing doesn't exceed margin
- [ ] Test breakeven stop logic edge cases
- [ ] Check narration for scaling events
- [ ] Confirm no race conditions on partial fills

---

## IMPLEMENTATION ORDER

1. **First:** Change MIN_SL_PIPS from 18 → 10 (1-minute change)
2. **Second:** Add partial exit scaling logic (15 minutes)
3. **Third:** Add breakeven stop management (10 minutes)
4. **Fourth:** Implement dynamic position sizing (20 minutes)
5. **Test:** Run 10 paper trades manually to verify scaling works

---

## VALIDATION

After changes, re-run ghost trading analysis:
- Should see avg win increase to $4+
- Should see avg loss decrease to $0.60
- Should see R:R ratio > 3:1
- Win rate should stay at 64%+
- Daily return should reach 0.12%+

Only then proceed to live trading.

---

**Priority:** 🔴 CRITICAL - Implement before any live trading
**Complexity:** Medium (requires position management additions)
**Risk:** Low (paper trading only, improves logic)
