#!/usr/bin/env python3
"""
Quant Hedge Rules System - Multi-Condition Analysis Engine
Analyzes market conditions and provides hedging/positioning recommendations
PIN: 841921 | Phase: Active Analysis | Profile: Non-HFT (M15-H1)
Emits HEDGE_ON / HEDGE_OFF events
"""

import numpy as np
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timezone
import json

# Import hardened narration
try:
    from util.narration_logger import log_event, start_listener
except ImportError:
    # Fallback if narration not available
    def log_event(*args, **kwargs):
        pass
    def start_listener(*args, **kwargs):
        pass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HedgeAction(Enum):
    """Recommended hedge actions based on market conditions"""
    FULL_LONG = "full_long"           # Aggressive long positions
    MODERATE_LONG = "moderate_long"    # Conservative long positions
    REDUCE_EXPOSURE = "reduce_exposure" # Cut position size by 50%
    CLOSE_ALL = "close_all"            # Exit all positions immediately
    HEDGE_SHORT = "hedge_short"        # Add offsetting short hedge
    PAUSE_TRADING = "pause_trading"    # Stop new entries temporarily
    WAIT_FOR_CLARITY = "wait_for_clarity"  # Hold and monitor

class VolatilityLevel(Enum):
    """Volatility classification"""
    LOW = "low"           # 0-1.5% annualized
    MODERATE = "moderate" # 1.5-3.0% annualized
    HIGH = "high"         # 3.0-5.0% annualized
    EXTREME = "extreme"   # 5%+ annualized

class CorrelationLevel(Enum):
    """Correlation risk classification"""
    LOW = "low"           # Different assets moving independently
    MODERATE = "moderate" # Some correlation detected
    HIGH = "high"         # Strong correlation (risky for diversification)
    EXTREME = "extreme"   # Perfect/near-perfect correlation

@dataclass
class HedgeCondition:
    """Individual condition evaluation for hedge decision"""
    condition_name: str
    current_value: float
    threshold: float
    is_warning: bool
    details: Optional[Dict] = None

class QuantHedgeRules:
    """
    Quant Hedge Rules Engine with hysteresis
    Emits HEDGE_ON/HEDGE_OFF events based on risk conditions
    """
    
    def __init__(self, *args, pin=None, **kwargs):
        """
        Initialize QuantHedgeRules.
        
        Args:
            pin: Charter PIN for authorization (optional for soft enforcement)
        """
        self._hedge_active = False
        self._last_toggle_ts = 0.0
        self.MIN_SECONDS_BETWEEN_TOGGLES = 900  # 15 minutes minimum between toggles
        self.ON_THRESHOLD = 1.0  # Risk score to activate hedge
        self.OFF_THRESHOLD = 0.7  # Risk score to deactivate hedge
        self.logger = logger
        
        # Start narration at first instantiation
        try:
            start_listener(sample_one_in_n=0, max_bytes=25*1024*1024, backup_count=7, daily_rotation=True)
        except:
            pass
    
    def risk_score(self, m) -> float:
        """
        Calculate composite risk score from market metrics.
        
        Score formula:
            0.5 * vol_z (volatility zscore)
            + 0.3 * max(0, loss_streak - 1) (consecutive losses)
            + 0.4 if BEAR regime (market condition)
        
        Returns:
            float: Risk score (0.0 to ~2.0)
        """
        try:
            vol_component = 0.5 * getattr(m, "vol_z", 0.0)
            loss_component = 0.3 * max(0, getattr(m, "loss_streak", 0) - 1)
            regime = str(getattr(m, "regime", ""))
            regime_component = 0.4 if regime.startswith("BEAR") else 0.0
            
            return vol_component + loss_component + regime_component
        except Exception as e:
            self.logger.error(f"Error calculating risk score: {e}")
            return 0.0
    
    def maybe_update_hedge(self, m, now_ts) -> None:
        """
        Check if hedge status should change and emit event if needed.
        Uses hysteresis (ON_THRESHOLD > OFF_THRESHOLD) to prevent oscillation.
        
        Args:
            m: Market metrics object with vol_z, loss_streak, regime attributes
            now_ts: Current timestamp (unix epoch seconds)
        """
        score = self.risk_score(m)
        elapsed = now_ts - self._last_toggle_ts
        
        # Check activation: risk score high + enough time has passed
        if (not self._hedge_active) and score >= self.ON_THRESHOLD and elapsed >= self.MIN_SECONDS_BETWEEN_TOGGLES:
            self._hedge_active = True
            self._last_toggle_ts = now_ts
            
            log_event(
                "HEDGE_ON",
                strategy="quant_hedge",
                symbol=getattr(m, "symbol", None),
                details={
                    "score": round(score, 3),
                    "vol": getattr(m, "vol", None),
                    "loss_streak": getattr(m, "loss_streak", None),
                    "regime": getattr(m, "regime", None)
                }
            )
            self.logger.info(f"Hedge activated: score={score:.3f}")
        
        # Check deactivation: risk score low + enough time has passed
        elif self._hedge_active and score <= self.OFF_THRESHOLD and elapsed >= self.MIN_SECONDS_BETWEEN_TOGGLES:
            self._hedge_active = False
            self._last_toggle_ts = now_ts
            
            log_event(
                "HEDGE_OFF",
                strategy="quant_hedge",
                symbol=getattr(m, "symbol", None),
                details={
                    "score": round(score, 3),
                    "vol": getattr(m, "vol", None),
                    "loss_streak": getattr(m, "loss_streak", None),
                    "regime": getattr(m, "regime", None)
                }
            )
            self.logger.info(f"Hedge deactivated: score={score:.3f}")
    
    def get_hedge_action(self, conditions: List[HedgeCondition]) -> HedgeAction:
        """
        Determine recommended action based on hedge conditions.
        
        Args:
            conditions: List of HedgeCondition objects
            
        Returns:
            HedgeAction: Recommended trading action
        """
        warning_count = sum(1 for c in conditions if c.is_warning)
        total_count = len(conditions)
        
        if warning_count == 0:
            return HedgeAction.FULL_LONG
        elif warning_count < total_count / 3:
            return HedgeAction.MODERATE_LONG
        elif warning_count < total_count / 2:
            return HedgeAction.REDUCE_EXPOSURE
        else:
            return HedgeAction.CLOSE_ALL
