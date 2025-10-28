#!/usr/bin/env python3
"""
EMA Scalper strategy stub.
Returns None by default.
"""
from typing import Optional, Dict
import pandas as pd

def ema_scalper_signal(df: pd.DataFrame) -> Optional[Dict]:
    """Placeholder: return None to indicate no actionable signal.
    Args:
        df: OHLC DataFrame
    Returns:
        Optional signal dict with keys like {'action': 'buy'|'sell', 'entry': ..., 'sl': ..., 'tp': ...}
    """
    return None
