# Position Guardian — Gated Logic & Prompts

## Overview
Position Guardian enforces pre-trade gates (correlation, margin) and autopilot rules (BE+5, trailing, time-stops, giveback exits, partial scale-outs) on all positions.

## Pre-Trade Gates (Correlation & Margin)

### Correlation Gate
**Purpose:** Block orders that increase net USD exposure on the same side.

**Logic:**
```python
def correlation_gate(order: Order, positions: List[Position]) -> HookResult:
    """
    Reject if order increases net USD exposure on the same side.
    Allow if it hedges/balances.
    """
    net_before = net_usd_exposure(positions)
    net_after = net_before + usd_exposure_for(order)
    
    # If net_before and net_after have same sign and magnitude increases
    if net_before != 0 and net_after != 0:
        if (net_before > 0 and net_after > net_before) or \
           (net_before < 0 and net_after < net_before):
            return HookResult(
                allowed=False,
                reason=f"Correlation gate: order increases net USD {'+' if net_before>0 else '-'} from {abs(net_before):.0f} to {abs(net_after):.0f}"
            )
    return HookResult(allowed=True, reason="Correlation OK")
```

**Gated Prompt:**
- "Should I add EURUSD long?" → Check if we already have net long USD → if yes, BLOCK → suggest hedge.

### Margin Gate
**Purpose:** Block new exposure if margin utilization > 35%.

**Logic:**
```python
def margin_gate(order: Order, account: AccountState) -> HookResult:
    """
    Block if margin_used/NAV > 35% unless order is reduce_only.
    """
    mu = account.margin_utilization
    if mu > MARGIN_CAP and not order.reduce_only:
        return HookResult(
            allowed=False,
            reason=f"Margin gate: {mu*100:.1f}% > {MARGIN_CAP*100:.0f}% cap — reduce exposure before adding"
        )
    return HookResult(allowed=True, reason="Margin OK")
```

**Gated Prompt:**
- "Trade new position?" → If margin > 35% → BLOCK → "Reduce margin first."

## Autopilot Rules (Tick Enforce)

### 1. Auto-Breakeven (BE+5)
**Trigger:** Position reaches ≥1R or ≥25 pips profit  
**Action:** Move SL to entry + 5 pips

**Logic:**
```python
def auto_breakeven_action(p: Position) -> Optional[Dict]:
    meets_r = (p.r_multiple is not None and p.r_multiple >= 1.0)
    meets_pips = (p.pips_open >= 25.0)
    if not (meets_r or meets_pips):
        return None
    new_sl = p.entry_price + (5.0 * p.pip_size * p.direction)
    if p.stop_loss is None or (p.direction * (new_sl - p.stop_loss)) > 0:
        return {"type": "modify_sl", "new_sl": new_sl, "why": "auto_breakeven"}
    return None
```

**Gated Prompt:**
- "GBPUSD +28 pips" → AUTO → "Moving SL to BE+5."

### 2. Time-Based Exits
**Minor Cap (3h):** Close if position age ≥3h AND pips < 0.5R  
**Major Cap (6h):** Close ALL positions ≥6h

**Logic:**
```python
def time_stop_action(p: Position, now_utc: datetime) -> Optional[Dict]:
    age = now_utc - p.opened_at
    if age >= timedelta(hours=6):
        return {"type": "close", "why": "time_stop_6h"}
    if age >= timedelta(hours=3):
        if p.r_multiple is None or p.r_multiple < 0.5:
            return {"type": "close", "why": "time_stop_3h<0.5R"}
    return None
```

**Gated Prompt:**
- "EURUSD age 6.2h" → AUTO → "Closing (6h cap)."
- "USDJPY age 3.5h, +0.3R" → AUTO → "Closing (3h <0.5R)."

### 3. ATR Trailing
**Stage 2 (40+ pips):** Trail distance = 18 pips  
**Stage 3 (60+ pips):** Trail distance = 12 pips

**Logic:**
```python
def trail_action(p: Position, state: Dict) -> Optional[Dict]:
    pips = p.pips_open
    if pips < 40:
        return None
    
    peak = _get(state, p.id, "peak_pips", pips)
    if pips > peak:
        _set(state, p.id, "peak_pips", pips)
        peak = pips
    
    distance = 12.0 if pips >= 60 else 18.0
    trail_price = p.current_price - (distance * p.pip_size * p.direction)
    
    if p.stop_loss is None or (p.direction * (trail_price - p.stop_loss)) > 0:
        return {"type": "modify_sl", "new_sl": trail_price, "why": f"trail_stage{3 if pips>=60 else 2}"}
    return None
```

**Gated Prompt:**
- "GBPUSD +45 pips" → AUTO → "Trail 18 pips."
- "GBPUSD +65 pips" → AUTO → "Trail 12 pips."

### 4. Peak Giveback Exit
**Trigger:** Current pips < 60% of peak pips (40% giveback)  
**Action:** Close position

**Logic:**
```python
def giveback_exit(p: Position, state: Dict) -> Optional[Dict]:
    pips = p.pips_open
    peak = _get(state, p.id, "peak_pips", pips)
    if pips > peak:
        _set(state, p.id, "peak_pips", pips)
        return None
    
    giveback_pct = 1.0 - (pips / peak) if peak > 0 else 0.0
    if giveback_pct >= 0.40:
        return {"type": "close", "why": f"giveback_{giveback_pct*100:.0f}%_from_peak"}
    return None
```

**Gated Prompt:**
- "EURUSD peaked at +50 pips, now +28 pips" → (44% giveback) → AUTO → "Close (giveback)."

### 5. Partial Scale-Outs
**50% at 1.5R or 35 pips**  
**25% at 2.5R or 55 pips**

**Logic:**
```python
def scale_out_action(p: Position, state: Dict) -> Optional[Dict]:
    pips = p.pips_open
    r = p.r_multiple or 0.0
    
    scaled_50 = _get(state, p.id, "scaled_50", False)
    scaled_25 = _get(state, p.id, "scaled_25", False)
    
    if not scaled_50 and (r >= 1.5 or pips >= 35):
        _set(state, p.id, "scaled_50", True)
        return {"type": "close_partial", "percent": 0.50, "why": "scale_50%_at_1.5R"}
    
    if scaled_50 and not scaled_25 and (r >= 2.5 or pips >= 55):
        _set(state, p.id, "scaled_25", True)
        return {"type": "close_partial", "percent": 0.25, "why": "scale_25%_at_2.5R"}
    
    return None
```

**Gated Prompt:**
- "GBPUSD +38 pips (1.6R)" → AUTO → "Close 50%."
- "GBPUSD +58 pips (2.6R)" → AUTO → "Close 25% more."

### 6. Session Awareness
**Off-hours:** Tighten or flatten  
**Friday close:** Exit before 20:55 UTC

**Logic:**
```python
def session_gate(now_utc: datetime) -> Optional[str]:
    # Friday close warning
    if now_utc.weekday() == 4 and now_utc.hour >= 20 and now_utc.minute >= 55:
        return "flatten_friday_close"
    return None
```

**Gated Prompt:**
- "Friday 20:56 UTC" → AUTO → "Flatten all (weekend)."

## Integration: pg_trade CLI

**Command:**
```bash
pg_trade --venue oanda --symbol GBPUSD --side buy --units 10000 [--dry-run]
```

**Flow:**
1. Construct `Order` object
2. Call `pre_trade_hook(order, positions, account)`
3. If `result.allowed == False` → BLOCK → print reason
4. If `result.allowed == True` → execute order via broker adapter

**Gated Prompts Applied:**
- Correlation check → "EURUSD buy blocked: increases net long USD"
- Margin check → "Order blocked: margin 37% > 35%"

## Daemon Mode

**Command:**
```bash
python3 guardian_daemon.py --loop 30 --live
```

**Flow:**
1. Every 30s: snapshot positions & account
2. Call `tl_dr_actions(positions, account, now_utc)`
3. Apply actions:
   - `modify_sl` → set new stop
   - `close` → close trade
   - `close_partial` → reduce units
4. Log to `logs/guardian.log`

**Gated Prompts Applied (Auto):**
- "BE+5 applied to GBPUSD"
- "Trail tightened to 12 pips on EURUSD"
- "Closed USDJPY (6h cap)"
- "Closed AUDUSD (giveback 42%)"
- "Scaled out 50% of GBPUSD (1.6R)"

## Summary Table

| Rule | Trigger | Action | Gated Prompt Example |
|------|---------|--------|----------------------|
| **Correlation Gate** | New order increases net USD same side | BLOCK | "EURUSD buy blocked: increases long USD" |
| **Margin Gate** | Margin > 35% | BLOCK | "Order blocked: reduce margin first" |
| **Auto-BE** | ≥1R or ≥25 pips | SL → BE+5 | "GBPUSD BE+5 applied" |
| **Time 3h** | Age ≥3h, <0.5R | CLOSE | "USDJPY closed (3h <0.5R)" |
| **Time 6h** | Age ≥6h | CLOSE | "EURUSD closed (6h cap)" |
| **Trail S2** | ≥40 pips | SL trail 18p | "GBPUSD trail 18 pips" |
| **Trail S3** | ≥60 pips | SL trail 12p | "GBPUSD trail 12 pips" |
| **Giveback** | 40% drop from peak | CLOSE | "AUDUSD closed (giveback 44%)" |
| **Scale 50%** | 1.5R or 35p | Close 50% | "GBPUSD scale 50% at 1.6R" |
| **Scale 25%** | 2.5R or 55p | Close 25% | "GBPUSD scale 25% at 2.7R" |
| **Session** | Friday 20:55+ UTC | FLATTEN | "Flatten all (weekend)" |

All logic enforces Charter compliance (6h max, margin ≤35%, risk management) and is PIN-gated via the upgrade toggle for live deployment.
