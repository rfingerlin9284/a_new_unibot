"""
Execution Throttle - Non-HFT order rate limiting (Phase 4)
PIN: 841921 | Profile: Non-HFT (M15-H1)
Enforces: MIN_SECONDS_BETWEEN_ORDERS, MAX_ORDERS_PER_SYMBOL_PER_DAY, MAX_REPLACEMENTS_PER_ORDER
"""
import time
from collections import defaultdict
from datetime import datetime, timezone

_last_order_ts = defaultdict(float)
_daily_count = defaultdict(int)
_daily_reset_date = None
_replacement_count = defaultdict(int)

def _reset_daily_if_needed():
    """Reset daily counters at midnight UTC"""
    global _daily_count, _daily_reset_date
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if _daily_reset_date != today:
        _daily_count.clear()
        _replacement_count.clear()
        _daily_reset_date = today

def can_place(symbol: str, now: float = None, charter=None) -> bool:
    """
    Check if an order can be placed on this symbol right now.
    
    Returns:
        bool: True if order can be placed, False if throttled
    """
    if now is None:
        now = time.time()
    if charter is None:
        MIN_SECONDS = 180
        MAX_ORDERS = 8
    else:
        MIN_SECONDS = getattr(charter, "MIN_SECONDS_BETWEEN_ORDERS", 180)
        MAX_ORDERS = getattr(charter, "MAX_ORDERS_PER_SYMBOL_PER_DAY", 8)
    
    _reset_daily_if_needed()
    
    # Check time throttle
    if now - _last_order_ts[symbol] < MIN_SECONDS:
        return False
    
    # Check daily quota
    if _daily_count[symbol] >= MAX_ORDERS:
        return False
    
    return True

def record_order(symbol: str, now: float = None):
    """Record that an order was placed on this symbol"""
    if now is None:
        now = time.time()
    _reset_daily_if_needed()
    _last_order_ts[symbol] = now
    _daily_count[symbol] += 1

def can_replace_order(order_id: str, charter=None) -> bool:
    """
    Check if an order can be replaced (modified).
    
    Returns:
        bool: True if replacement allowed, False if limit reached
    """
    if charter is None:
        MAX_REPLACEMENTS = 2
    else:
        MAX_REPLACEMENTS = getattr(charter, "MAX_REPLACEMENTS_PER_ORDER", 2)
    
    return _replacement_count[order_id] < MAX_REPLACEMENTS

def record_replacement(order_id: str):
    """Record that an order was replaced/modified"""
    _replacement_count[order_id] += 1

def get_stats(symbol: str = None) -> dict:
    """Get throttle statistics"""
    _reset_daily_if_needed()
    if symbol:
        return {
            "symbol": symbol,
            "daily_orders": _daily_count.get(symbol, 0),
            "last_order_ts": _last_order_ts.get(symbol, 0),
            "seconds_since_last": time.time() - _last_order_ts.get(symbol, 0)
        }
    else:
        return {
            "daily_counts": dict(_daily_count),
            "last_order_times": dict(_last_order_ts),
            "daily_reset_date": _daily_reset_date
        }
