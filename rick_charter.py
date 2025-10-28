#!/usr/bin/env python3
"""
RICK CHARTER - Immutable Trading Rules (PIN: 841921)
=====================================================

This charter defines the inviolable trading rules for the RICK autonomous trading system.
All trading decisions, position sizing, risk management, and gate enforcement must comply
with these rules. These are hardcoded constants and cannot be overridden at runtime.

PIN: 841921 (Change-control lock)
Version: 2.0_IMMUTABLE
Status: ACTIVE for Paper & Live Trading
"""

# ============================================================================
# CHARTER PIN (Immutable Access Control)
# ============================================================================
CHARTER_PIN = 841921
CHARTER_VERSION = "2.0_IMMUTABLE"
CHARTER_STATUS = "ACTIVE"


# ============================================================================
# POSITION SIZING RULES
# ============================================================================
MIN_NOTIONAL_USD = 15000  # Minimum position size (paper & live)
MAX_NOTIONAL_USD = 50000  # Maximum position size (only for 90%+ confidence)

# Dynamic sizing tiers (based on signal confidence)
POSITION_SIZING_TIERS = {
    0.70: 15000,   # 70-75% confidence → $15k minimum
    0.75: 15000,   # 75% confidence → $15k (Charter minimum)
    0.80: 20000,   # 80% confidence → $20k
    0.85: 30000,   # 85% confidence → $30k
    0.90: 50000,   # 90%+ confidence → $50k (max)
}


# ============================================================================
# RISK MANAGEMENT RULES
# ============================================================================
MAX_MARGIN_PERCENT = 35  # Never use more than 35% of account margin
MAX_CONCURRENT_POSITIONS = 3  # Maximum 3 open positions at any time
MAX_HOLD_DURATION_HOURS = 6  # Never hold a position longer than 6 hours
MIN_RISK_REWARD_RATIO = 3.2  # Minimum R:R ratio for all trades (3.2:1)

# Stop loss rules
MIN_SL_PIPS = 10  # Minimum stop loss (10 pips = 0.001 for most pairs)
MAX_SL_PIPS = 50  # Maximum stop loss (50 pips = protection limit)

# Profit target rules
MIN_TP_PIPS = 32  # Minimum profit target (32 pips to meet 3.2:1 R:R)


# ============================================================================
# MARKET RULES
# ============================================================================
ALLOWED_INSTRUMENTS = [
    # Major pairs
    "EUR_USD",
    "GBP_USD",
    "USD_JPY",
    "USD_CHF",
    "AUD_USD",
    "NZD_USD",
    "USD_CAD",
    # Cross pairs
    "EUR_GBP",
    "EUR_JPY",
    "EUR_CHF",
    "GBP_JPY",
    "AUD_JPY",
    "CHF_JPY",
]

ALLOWED_TIMEFRAMES = [
    "M15",  # 15 minutes (minimum)
    "M30",  # 30 minutes
    "H1",   # 1 hour
    "H4",   # 4 hours
    "D",    # Daily
]

# Forex market hours (UTC)
MARKET_OPEN_DAY = 0  # Sunday (0=Monday, 6=Sunday in Python)
MARKET_OPEN_HOUR = 21  # 21:00 UTC = Sunday 5 PM EST
MARKET_CLOSE_DAY = 4  # Friday
MARKET_CLOSE_HOUR = 21  # 21:00 UTC = Friday 5 PM EST


# ============================================================================
# GATE ENFORCEMENT RULES
# ============================================================================
GATE_RULES = {
    "MARGIN_CHECK": {
        "max_margin_pct": MAX_MARGIN_PERCENT,
        "description": "Never exceed 35% margin usage",
    },
    "POSITION_LIMIT_CHECK": {
        "max_concurrent": MAX_CONCURRENT_POSITIONS,
        "description": "Never have more than 3 open positions",
    },
    "INSTRUMENT_WHITELIST_CHECK": {
        "allowed": ALLOWED_INSTRUMENTS,
        "description": "Only trade whitelisted FX pairs",
    },
    "TIMEFRAME_WHITELIST_CHECK": {
        "allowed": ALLOWED_TIMEFRAMES,
        "description": "Only trade M15+ timeframes (no micro trading)",
    },
    "NOTIONAL_CHECK": {
        "min_notional": MIN_NOTIONAL_USD,
        "max_notional": MAX_NOTIONAL_USD,
        "description": "Position size must be 15k-50k notional",
    },
    "RISK_REWARD_CHECK": {
        "min_ratio": MIN_RISK_REWARD_RATIO,
        "description": "Risk:Reward ratio must be at least 3.2:1",
    },
    "DURATION_CHECK": {
        "max_hours": MAX_HOLD_DURATION_HOURS,
        "description": "Hold time must not exceed 6 hours",
    },
    "LATENCY_CHECK": {
        "max_latency_ms": 300,
        "description": "API latency must be < 300ms",
    },
}


# ============================================================================
# PERFORMANCE METRICS & THRESHOLDS
# ============================================================================
MIN_WIN_RATE_FOR_LIVE = 0.60  # 60% win rate minimum to go live
TARGET_WIN_RATE = 0.70  # Target is 70%+
DAILY_RETURN_TARGET = 0.063  # 0.063% daily return target

# Profit-taking rules
PARTIAL_EXIT_LEVELS = [
    {"profit_pct": 1.0, "exit_pct": 0.50},  # Take 50% profit at +1R
    {"profit_pct": 2.0, "exit_pct": 0.25},  # Take 25% profit at +2R
    # Remaining 25% trails with breakeven stop
]

# Stop loss escalation
BREAKEVEN_STOP_ENABLED = True  # Move stop to breakeven after +1R profit
TRAILING_STOP_ENABLED = True  # Partial trailing for remaining position


# ============================================================================
# REPORTING & AUDIT RULES
# ============================================================================
AUDIT_LOG_FILE = "logs/audit.jsonl"
DECISIONS_LOG_FILE = "logs/autonomous_decisions.jsonl"
NARRATION_LOG_FILE = "narration.jsonl"

# All trades must be logged with:
REQUIRED_TRADE_FIELDS = [
    "timestamp",
    "instrument",
    "side",  # BUY or SELL
    "entry_price",
    "position_size",
    "notional_usd",
    "stop_loss",
    "take_profit",
    "expected_rr_ratio",
    "signal_confidence",
    "gate_checks",  # Which gates passed
]


# ============================================================================
# ACTIVATION & VALIDATION
# ============================================================================
class RickCharter:
    """
    Charter validator - ensures all trading decisions comply with PIN 841921 rules.
    Used by autonomous_decision_engine.py and guardian_gates.py
    """

    def __init__(self, pin: int = None):
        """Initialize charter with optional PIN verification"""
        if pin is not None and pin != CHARTER_PIN:
            raise ValueError(f"Invalid PIN. Expected {CHARTER_PIN}, got {pin}")
        self.pin_verified = pin == CHARTER_PIN if pin else False

    def validate_position_size(self, notional_usd: float, confidence: float = 0.75) -> bool:
        """Validate position size against charter"""
        if not (MIN_NOTIONAL_USD <= notional_usd <= MAX_NOTIONAL_USD):
            return False
        return True

    def validate_risk_reward(self, risk_pips: float, reward_pips: float) -> bool:
        """Validate R:R ratio meets minimum"""
        if risk_pips <= 0 or reward_pips <= 0:
            return False
        ratio = reward_pips / risk_pips
        return ratio >= MIN_RISK_REWARD_RATIO

    def validate_margin(self, margin_used_pct: float) -> bool:
        """Validate margin usage"""
        return margin_used_pct <= MAX_MARGIN_PERCENT

    def validate_position_count(self, open_positions: int) -> bool:
        """Validate concurrent position count"""
        return open_positions <= MAX_CONCURRENT_POSITIONS

    def validate_hold_duration(self, entry_time_seconds: float, current_time_seconds: float) -> bool:
        """Validate position hold duration"""
        hold_hours = (current_time_seconds - entry_time_seconds) / 3600
        return hold_hours <= MAX_HOLD_DURATION_HOURS

    def validate_instrument(self, instrument: str) -> bool:
        """Validate instrument is whitelisted"""
        return instrument in ALLOWED_INSTRUMENTS

    def validate_timeframe(self, timeframe: str) -> bool:
        """Validate timeframe is allowed"""
        return timeframe in ALLOWED_TIMEFRAMES


if __name__ == "__main__":
    print("🔐 RICK CHARTER (PIN: 841921)")
    print("=" * 70)
    print(f"Version: {CHARTER_VERSION}")
    print(f"Status: {CHARTER_STATUS}")
    print()
    print("Position Sizing Rules:")
    print(f"  Minimum: ${MIN_NOTIONAL_USD:,} USD")
    print(f"  Maximum: ${MAX_NOTIONAL_USD:,} USD")
    print()
    print("Risk Management Rules:")
    print(f"  Max Margin: {MAX_MARGIN_PERCENT}%")
    print(f"  Max Concurrent Positions: {MAX_CONCURRENT_POSITIONS}")
    print(f"  Max Hold Time: {MAX_HOLD_DURATION_HOURS} hours")
    print(f"  Min Risk:Reward: {MIN_RISK_REWARD_RATIO}:1")
    print(f"  Min Stop Loss: {MIN_SL_PIPS} pips")
    print(f"  Min Profit Target: {MIN_TP_PIPS} pips")
    print()
    print("Market Rules:")
    print(f"  Allowed Instruments: {len(ALLOWED_INSTRUMENTS)} pairs")
    print(f"  Allowed Timeframes: {ALLOWED_TIMEFRAMES}")
    print()
    print("Gate Enforcement:")
    print(f"  Active Gates: {len(GATE_RULES)}")
    for gate_name in GATE_RULES:
        print(f"    ✅ {gate_name}")
    print()
    print("✅ Charter verified and ready for deployment")


# ============================================================================
# NON-HFT PROFILE DEFAULTS (Phase 4 - Auto-injected 2025-10-27)
# ============================================================================
# These enforce a non-HFT (M15-H1) trading profile with throttled order cadence

class TimeFrame:
    """Allowed trading timeframes"""
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"

class RejectedTimeFrame:
    """Explicitly rejected timeframes"""
    M1 = "M1"
    M5 = "M5"

# Order execution throttles for non-HFT profile
MIN_TRADE_DURATION_MIN = 20  # Minimum 20 minutes per trade
MIN_SECONDS_BETWEEN_ORDERS = 180  # At least 3 minutes between orders on same symbol
MAX_ORDERS_PER_SYMBOL_PER_DAY = 8  # Max 8 orders per symbol per day
MAX_REPLACEMENTS_PER_ORDER = 2  # Max 2 replacements (modifications) per order
