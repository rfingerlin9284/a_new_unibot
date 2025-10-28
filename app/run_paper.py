#!/usr/bin/env python3
"""
Paper Trading Runner - Non-HFT bar-close loop (Phase 10)
PIN: 841921 | Profile: Non-HFT (M15-H1)
Orchestrates hardened narration, pack routing, hedge hysteresis, and guardian gates
"""
import os, sys, time, math
from pathlib import Path
from types import SimpleNamespace

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.narration_logger import start_listener, log_event
from foundation.broker_config import CONFIG
from wolf_packs.orchestrator import on_bar_close
from hive.quant_hedge_rules import QuantHedgeRules

def main():
    """Main paper trading loop"""
    
    # Start hardened narration with non-HFT defaults
    start_listener(sample_one_in_n=0, max_bytes=25*1024*1024, backup_count=7, daily_rotation=True)
    
    # Verify paper API is configured
    if not CONFIG.ready():
        print("❌ Paper API env vars missing!")
        print(f"   Required: PAPER_API_BASE_URL, PAPER_API_KEY, PAPER_API_SECRET")
        print(f"   Config: {CONFIG.summary()}")
        return 1
    
    print(f"✅ Paper API configured")
    print(f"   Mode: {CONFIG.MODE}")
    print(f"   Timeframe: {CONFIG.TIMEFRAME_DEFAULT}")
    
    # Log boot event
    log_event(
        "BOOT",
        strategy="runner",
        details={
            "mode": CONFIG.MODE,
            "timeframe": CONFIG.TIMEFRAME_DEFAULT,
            "profile": "non-hft",
            "pin": 841921
        }
    )
    
    # Initialize hedge rules
    qh = QuantHedgeRules()
    print("✅ QuantHedgeRules initialized")
    
    # Get trading symbol and period
    SYMBOL = os.getenv("PAPER_SYMBOL", "EURUSD")
    timeframe = CONFIG.TIMEFRAME_DEFAULT
    period_sec = {
        "M15": 900,
        "M30": 1800,
        "H1": 3600,
    }.get(timeframe, 3600)
    
    print(f"✅ Trading symbol: {SYMBOL}")
    print(f"✅ Bar period: {timeframe} ({period_sec}s)")
    print(f"\n🚀 Paper trading loop started...")
    print(f"   Logs: logs/narration.jsonl")
    print(f"   Monitor: tail -f logs/narration.jsonl | jq -r '.event'")
    
    # Main loop: bar-close cadence
    next_tick = time.time()
    cycle = 0
    
    try:
        while True:
            now = time.time()
            
            if now >= next_tick:
                cycle += 1
                
                # Create fake bar and snapshot
                bar = SimpleNamespace(ts=now)
                snap = SimpleNamespace(symbol=SYMBOL)
                
                # Route to pack based on regime
                pack = on_bar_close(bar, snap)
                
                # Simulate market metrics for hedge evaluation
                # (Replace with real metrics in production)
                metrics = SimpleNamespace(
                    symbol=SYMBOL,
                    vol=0.02,
                    vol_z=0.8 * math.sin(now / 3600.0) + 1.0,
                    loss_streak=0,
                    regime="NEUTRAL" if cycle % 3 == 0 else "BULL"
                )
                
                # Check hedge conditions
                qh.maybe_update_hedge(metrics, now_ts=now)
                
                # Simulate guardian gates demo
                # (In production, these would run in real trade path)
                if cycle % 10 == 0:
                    # Demo: Once per 10 cycles, simulate a margin gate rejection
                    log_event(
                        "TRADE_BLOCKED",
                        gate="margin",
                        used_pct=35.5,
                        max_pct=35.0,
                        reason="Margin limit exceeded (demo)"
                    )
                
                # Schedule next bar close
                next_tick = now + period_sec
                
                # Keep terminal responsive
                if cycle % 6 == 0:  # Every 6 bar-closes
                    print(f"   Cycle {cycle}: {timeframe} bar closed")
            
            # Sleep briefly to avoid busy-waiting
            time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n✋ Interrupted after {cycle} cycles")
        log_event("SHUTDOWN", strategy="runner", details={"cycles": cycle})
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        log_event("ERROR", strategy="runner", details={"error": str(e)})
        return 1

if __name__ == "__main__":
    exit(main())
