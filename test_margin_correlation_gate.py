#!/usr/bin/env python3
"""
MARGIN & CORRELATION GATE - COMPREHENSIVE TEST SUITE
PIN: 841921

Tests:
  1. Margin gate blocks orders when over cap
  2. Correlation gate blocks same-side increases
  3. Scale-out recommendations work
  4. Time stop logic correct
  5. SL validation works
"""

import sys
import logging
from foundation.margin_correlation_gate import (
    MarginCorrelationGate,
    Position,
    Order,
    HookResult,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def test_1_margin_gate_blocks_over_cap():
    """Test: Margin gate blocks orders when margin > 35%"""
    print("\n" + "=" * 80)
    print("TEST 1: Margin Gate Blocks Over Cap")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    positions = [
        Position(
            symbol="EUR_CHF",
            side="LONG",
            units=16300,
            entry_price=0.92404,
            current_price=0.92070,
            pnl=-7.03,
            pnl_pips=-3.4,
            margin_used=570,
            position_id="pos_117",
        ),
        Position(
            symbol="USD_CHF",
            side="LONG",
            units=19000,
            entry_price=0.79296,
            current_price=0.79225,
            pnl=-5.06,
            pnl_pips=-2.1,
            margin_used=570,
            position_id="pos_118",
        ),
    ]

    new_order = Order(
        symbol="EUR_USD", side="BUY", units=10000, price=1.0800, order_id="test_001"
    )

    # Current margin: 1140 / 1970 = 57.9% (over 35% cap)
    result = gate.margin_gate(total_margin_used=1140, new_order=new_order)

    print(f"\nResult: {result}")
    assert not result.allowed, "Gate should BLOCK order when margin > 35%"
    assert "margin" in result.reason.lower(), "Reason should mention margin"
    assert result.action == "AUTO_CANCEL", "Action should be AUTO_CANCEL"

    print("✅ TEST 1 PASSED: Margin gate correctly blocks orders over 35%")


def test_2_correlation_gate_blocks_same_side():
    """Test: Correlation gate blocks when currency bucket increases in same direction"""
    print("\n" + "=" * 80)
    print("TEST 2: Correlation Gate Blocks Same-Side Increase")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    positions = [
        Position(
            symbol="EUR_CHF",
            side="LONG",
            units=16300,
            entry_price=0.92404,
            current_price=0.92070,
            pnl=-7.03,
            pnl_pips=-3.4,
            margin_used=570,
            position_id="pos_117",
        ),
    ]

    # EUR/USD buy increases both EUR and (reduces USD, makes it short)
    new_order = Order(
        symbol="EUR_USD", side="BUY", units=10000, price=1.0800, order_id="test_002"
    )

    result = gate.correlation_gate_any_ccy(new_order, positions)

    print(f"\nResult: {result}")
    assert not result.allowed, "Gate should BLOCK order due to correlation"
    assert "correlation" in result.reason.lower(), "Reason should mention correlation"

    print("✅ TEST 2 PASSED: Correlation gate correctly blocks same-side increases")


def test_3_correlation_gate_allows_new_pair():
    """Test: Correlation gate allows entry into new currency pair"""
    print("\n" + "=" * 80)
    print("TEST 3: Correlation Gate Allows New Pair")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    positions = [
        Position(
            symbol="EUR_CHF",
            side="LONG",
            units=16300,
            entry_price=0.92404,
            current_price=0.92070,
            pnl=-7.03,
            pnl_pips=-3.4,
            margin_used=570,
            position_id="pos_117",
        ),
    ]

    # GBP/USD is a new currency pair (no correlation)
    new_order = Order(
        symbol="GBP_USD", side="BUY", units=10000, price=1.2700, order_id="test_003"
    )

    result = gate.correlation_gate_any_ccy(new_order, positions)

    print(f"\nResult: {result}")
    assert result.allowed, "Gate should ALLOW order for new currency pair"

    print("✅ TEST 3 PASSED: Correlation gate correctly allows new pairs")


def test_4_scale_out_recommendation():
    """Test: Scale-out recommendation when margin > cap"""
    print("\n" + "=" * 80)
    print("TEST 4: Scale-Out Recommendation")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    positions = [
        Position(
            symbol="EUR_CHF",
            side="LONG",
            units=16300,
            entry_price=0.92404,
            current_price=0.92070,
            pnl=-7.03,  # Weaker performer
            pnl_pips=-3.4,
            margin_used=570,
            position_id="pos_117",
        ),
        Position(
            symbol="USD_CHF",
            side="LONG",
            units=19000,
            entry_price=0.79296,
            current_price=0.79225,
            pnl=-5.06,  # Stronger performer
            pnl_pips=-2.1,
            margin_used=570,
            position_id="pos_118",
        ),
    ]

    current_margin_pct = 1140 / 1970  # 57.9%
    rec = gate.scale_out_recommendation(current_margin_pct, positions)

    print(f"\nRecommendation: {rec}")
    assert rec is not None, "Should have scale-out recommendation when over 35%"
    assert rec["current_pct"] > 0.35, "Current margin should be > 35%"
    assert rec["target_pct"] < 0.35, "Target margin should be < 35%"
    assert rec["recommended_position_id"] == "pos_117", "Should recommend scaling weaker position"

    print("✅ TEST 4 PASSED: Scale-out recommendation correct")


def test_5_time_stop_checks():
    """Test: Time stop logic (3h underperform & 6h hard close)"""
    print("\n" + "=" * 80)
    print("TEST 5: Time Stop Checks")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    pos = Position(
        symbol="EUR_CHF",
        side="LONG",
        units=16300,
        entry_price=0.92404,
        current_price=0.92070,
        pnl=-7.03,
        pnl_pips=-3.4,
        margin_used=570,
        position_id="pos_117",
    )

    # At 2 hours: should NOT close
    result = gate.time_stop_check(pos, minutes_held=120, current_r_multiple=0.3)
    print(f"\n2 hours, R=0.3: {result}")
    assert result is None, "Should NOT close before 3h"

    # At 3 hours, R < 0.5: should close
    result = gate.time_stop_check(pos, minutes_held=180, current_r_multiple=0.3)
    print(f"3 hours, R=0.3: {result}")
    assert result is not None, "Should close at 3h if R < 0.5"
    assert "3h" in result, "Close reason should mention 3h"

    # At 3 hours, R > 0.5: should keep open
    result = gate.time_stop_check(pos, minutes_held=180, current_r_multiple=0.8)
    print(f"3 hours, R=0.8: {result}")
    assert result is None, "Should keep open at 3h if R >= 0.5"

    # At 6 hours: should always close
    result = gate.time_stop_check(pos, minutes_held=360, current_r_multiple=10.0)
    print(f"6 hours, R=10.0: {result}")
    assert result is not None, "Should close at 6h regardless of R"
    assert "6h" in result, "Close reason should mention 6h"

    print("✅ TEST 5 PASSED: Time stop logic correct")


def test_6_sl_validation():
    """Test: Stop loss distance validation"""
    print("\n" + "=" * 80)
    print("TEST 6: SL Validation")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    # EUR/CHF pair (not JPY): pip size 0.0001
    entry = 0.92404
    sl_tight = 0.92300  # 104 pips (too tight)
    sl_good = 0.92200   # 204 pips (good)

    is_valid, reason = gate.validate_stop_loss_distance(entry, sl_tight, "EUR_CHF", atr_value=None)
    print(f"\nTight SL (104 pips): {is_valid} - {reason}")
    assert not is_valid, "Should reject SL < 18 pips"

    is_valid, reason = gate.validate_stop_loss_distance(entry, sl_good, "EUR_CHF", atr_value=None)
    print(f"Good SL (204 pips): {is_valid} - {reason}")
    assert is_valid, "Should accept SL >= 18 pips"

    # USD/JPY pair: pip size 0.01
    entry_jpy = 150.00
    sl_tight_jpy = 149.99  # 1 pip (too tight - should be rejected)
    sl_good_jpy = 149.82   # 18 pips (good - at minimum)

    is_valid, reason = gate.validate_stop_loss_distance(entry_jpy, sl_tight_jpy, "USD_JPY", atr_value=None)
    print(f"\nJPY Tight SL (1 pip): {is_valid} - {reason}")
    assert not is_valid, "Should reject JPY SL < 18 pips"

    is_valid, reason = gate.validate_stop_loss_distance(entry_jpy, sl_good_jpy, "USD_JPY", atr_value=None)
    print(f"JPY Good SL (18 pips): {is_valid} - {reason}")
    assert is_valid, "Should accept JPY SL >= 18 pips"

    print("✅ TEST 6 PASSED: SL validation correct")


def test_7_currency_bucket_exposure():
    """Test: Currency bucket exposure calculation"""
    print("\n" + "=" * 80)
    print("TEST 7: Currency Bucket Exposure")
    print("=" * 80)

    gate = MarginCorrelationGate(account_nav=1970.0)

    positions = [
        Position(
            symbol="EUR_CHF",
            side="LONG",
            units=16300,
            entry_price=0.92404,
            current_price=0.92070,
            pnl=-7.03,
            pnl_pips=-3.4,
            margin_used=570,
            position_id="pos_117",
        ),
        Position(
            symbol="USD_CHF",
            side="LONG",
            units=19000,
            entry_price=0.79296,
            current_price=0.79225,
            pnl=-5.06,
            pnl_pips=-2.1,
            margin_used=570,
            position_id="pos_118",
        ),
    ]

    exposure = gate.currency_bucket_exposure(positions)

    print(f"\nExposure: {exposure}")
    assert exposure["EUR"] == 16300, "EUR exposure should be +16,300 (from long EUR/CHF)"
    assert exposure["USD"] == 19000, "USD exposure should be +19,000 (from long USD/CHF)"
    assert exposure["CHF"] == -35300, "CHF exposure should be -35,300 (short from both pairs)"

    print("✅ TEST 7 PASSED: Currency bucket exposure correct")


def run_all_tests():
    """Run all tests"""
    print("\n" + "🛡️ " * 40)
    print("MARGIN & CORRELATION GATE - FULL TEST SUITE")
    print("🛡️ " * 40)

    tests = [
        test_1_margin_gate_blocks_over_cap,
        test_2_correlation_gate_blocks_same_side,
        test_3_correlation_gate_allows_new_pair,
        test_4_scale_out_recommendation,
        test_5_time_stop_checks,
        test_6_sl_validation,
        test_7_currency_bucket_exposure,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ TEST ERROR: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)

    if failed == 0:
        print("\n✅ ALL TESTS PASSED - Gates are working correctly!\n")
        return 0
    else:
        print(f"\n❌ {failed} tests failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
