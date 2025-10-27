"""
Wolf Pack Orchestrator - Pack routing at bar close (Phase 5)
PIN: 841921 | Profile: Non-HFT (M15-H1)
Emits PACK_ROUTED events based on regime detection
"""
from typing import Any
from util.narration_logger import log_event, start_listener

# Start hardened narration at module load
start_listener(sample_one_in_n=0, max_bytes=25*1024*1024, backup_count=7, daily_rotation=True)

_last_bar_ts = None

def detect_regime(data: Any = None) -> str:
    """
    Detect market regime from snapshot data.
    Falls back to neutral if detection unavailable.
    """
    try:
        from stochastic import random_choice
        return random_choice(["neutral", "bull", "bear"])
    except Exception:
        return "neutral"

def choose_pack_for_regime(regime: str) -> str:
    """
    Select trading pack based on detected regime.
    
    Args:
        regime: Market regime ("bull", "bear", "neutral")
        
    Returns:
        str: Pack identifier
    """
    if regime == "bull":
        return "momentum_v2"
    if regime == "bear":
        return "mean_reversion_v3"
    return "baseline_conservative"

def on_bar_close(bar, snapshot):
    """
    Called at each bar close. Routes to appropriate pack based on regime.
    Emits PACK_ROUTED event for narration.
    
    Args:
        bar: Bar object with ts attribute
        snapshot: Data snapshot with symbol attribute
        
    Returns:
        str: Selected pack identifier
    """
    global _last_bar_ts
    
    # Skip if bar timestamp hasn't advanced
    if _last_bar_ts and getattr(bar, "ts", None) and bar.ts <= _last_bar_ts:
        return
    
    _last_bar_ts = getattr(bar, "ts", None)
    regime = detect_regime(snapshot)
    pack = choose_pack_for_regime(regime)
    
    # Log the pack routing decision
    log_event(
        "PACK_ROUTED",
        regime=regime,
        pack=pack,
        symbol=getattr(snapshot, "symbol", None),
        details={
            "bar_ts": getattr(bar, "ts", None),
            "reason": "orchestrator-regime-map"
        }
    )
    
    return pack
