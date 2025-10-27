Position Guardian
-----------------
What it does:
- Auto-breakeven: if pips >=25 (or >=1R when initial SL known) -> SL = BE+5 pips.
- Time-stop: close at 6h hard cap; or at 3h if <0.5R.
- Correlation gate: reject orders that increase net USD exposure on the same side.
- Margin governor: if margin_used/NAV > 35%, only allow reduce/hedge orders.

How to test:
    cd /home/ing/RICK/R_H_UNI/plugins/position_guardian
    python3 demo_now.py

How to integrate (manager pipeline):
- Before sending any order: call pre_trade_hook(order, positions, account).
- Each tick (or per minute): call tick_enforce(positions, account, now) and apply returned actions:
    - {"type":"modify_sl", "position_id":..., "new_sl":...}
    - {"type":"close", "position_id":...}
    - {"type":"advice", ...}

Notes:
- Symbol format accepted: GBPUSD or GBP/USD.
- USD exposure logic: pairs with USD only. Crosses are treated as uncorrelated for the gate.
