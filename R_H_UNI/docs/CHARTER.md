# RBOTzilla Charter (Live Trading — Practice/LIVE)

## Source-of-truth (Self-contained)
This pack is authoritative under `RICK_LIVE_PROTOTYPE/R_H_UNI` and is designed to operate independently without referencing other project folders.

## Risk & Trade Management (immutable)
- Min notional per Charter: $15k (practice), sized dynamically per pair.
- Max concurrent positions: 3.
- Base risk per trade: target 0.5–1.0% of NAV (strategy-specific overrides allowed only if guardian permits).
- Hard time caps: close at 6h; at 3h close if unrealized < +0.5R.
- Margin governor: if margin_used/NAV > 35%, block new exposure unless it reduces/hedges net USD.
- Correlation gate: block orders that increase net USD exposure on same side.

## Exit Logic (guardian/autopilot)
- Auto-BE: ≥1R or ≥25 pips → SL to BE +5 pips.
- Trailing: start near +40 pips; tighten at +60 pips; prefer broker-native trailing; fallback to ratcheted SL.
- Partial scale: 50% at ~1.5R/35p; 25% at ~2.5R/55p; leave runner with tight trail.
- Peak giveback: exit if giveback ≥40% from peak pips.
- Session awareness: tighten or flatten off-hours; close before weekend (Fri ~20:55 UTC).

## Observability
- Narration logging: 100% of state changes to `logs/guardian.log` (+ `guardian_state.json`).
- Status surface: `make status` prints exposure, margin, and actions.

## Compliance
- Orders MUST be routed via the pre-trade gate (pg_trade). Direct broker calls are prohibited.
