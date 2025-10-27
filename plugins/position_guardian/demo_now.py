#!/usr/bin/env python3
"""
Position Guardian Demo — Shows Profit Autopilot in action.
"""
from datetime import datetime, timezone, timedelta
from position_guardian import Position, Order, AccountState, pre_trade_hook, tick_enforce, tl_dr_actions

now = datetime.now(timezone.utc)

gbpusd = Position(
    id="GBPUSD_1",
    symbol="GBPUSD",
    side="long",
    units=11200,
    entry_price=1.34038,
    current_price=1.34340,
    stop_loss=None,
    opened_at=now - timedelta(hours=1, minutes=30),
    initial_sl=1.33839
)

usdcad = Position(
    id="USDCAD_1",
    symbol="USDCAD",
    side="short",
    units=10700,
    entry_price=1.40478,
    current_price=1.40559,
    stop_loss=None,
    opened_at=now - timedelta(hours=1, minutes=30),
    initial_sl=1.39837
)

acct = AccountState(nav=1952.22, margin_used=966.0, now_utc=now)
positions = [gbpusd, usdcad]

print("=" * 80)
print("POSITION GUARDIAN — PROFIT AUTOPILOT DEMO")
print("=" * 80)

print("\n📍 Current Positions:")
for p in positions:
    print(f"  {p.symbol:8} {p.side:5} {int(p.units):6} units | Entry: {p.entry_price:.5f} | Current: {p.current_price:.5f} | Pips: {p.pips_open:.1f}p | R: {p.r_multiple if p.r_multiple else 'N/A'}")

print(f"\n💰 Account: NAV={acct.nav:.2f}, Margin={acct.margin_utilization*100:.1f}%")

print("\n🤖 TL;DR Actions (Autonomous):")
actions = tl_dr_actions(positions, acct, now)
if actions:
    for i, a in enumerate(actions, 1):
        print(f"  {i}. {a.get('type', '?'):15} | Why: {a.get('why', '?'):30} | Symbol: {a.get('symbol', '-')}")
else:
    print("  (no actions needed at this moment)")

print("\n🚧 Pre-trade Gate Checks:")

test_orders = [
    ("EURUSD", "buy", 10000, "New long"),
    ("GBPUSD", "buy", 5000, "Add to existing (bad)"),
    ("USDJPY", "buy", 8000, "Hedge USD (good)"),
]

for symbol, side, units, desc in test_orders:
    order = Order(symbol=symbol, side=side, units=units)
    result = pre_trade_hook(order, positions, acct)
    status = "✅ ALLOWED" if result.allowed else "❌ BLOCKED"
    reason = result.reason if result.reason else "(no reason)"
    print(f"  {symbol:8} {side:4} {units:5} units — {status:12} | {reason}")
    print(f"           ({desc})")

print("\n✨ Profit Autopilot Features:")
print("  • Auto-breakeven: SL → BE+5 at ≥1R/25p")
print("  • Stage S1: SL to BE+5")
print("  • Stage S2: Trailing ≥40p (18p gap)")
print("  • Stage S3: Tight trailing ≥60p (12p gap)")
print("  • Peak giveback: Exit on 40% pullback from peak")
print("  • 6h hard cap | 3h <0.5R close")
print("  • Bootstrap SL: OCO safety")

print("\n" + "=" * 80)
