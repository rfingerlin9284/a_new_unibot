#!/usr/bin/env python3
"""
Liquidity Sweep strategy stub.
Returns an empty list by default.
"""
from typing import List, Dict
import pandas as pd

def detect_liquidity_sweep(df: pd.DataFrame) -> List[Dict]:
    """Placeholder: return empty list to indicate no signals.
    Args:
        df: OHLC DataFrame
    Returns:
        List of signal dicts (possibly empty)
    """
    return []
