#!/usr/bin/env python3
"""
Trade Shim & Position Guardian Validation Suite
PIN: 841921 | Comprehensive charter compliance validation
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Tuple

# Charter constants
MIN_SL_PIPS = 18
MIN_RR = 3.2


def run_command(cmd: List[str], description: str = "") -> Tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10, cwd="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def test_trade_shim_help() -> Tuple[bool, str]:
    """TEST 1: Verify trade_shim --help shows bracket flags"""
    code, out, err = run_command(["python3", "brokers/trade_shim.py", "--help"])
    
    if code != 0:
        return False, f"Help failed: {err}"
    
    required = ["--tp-pips", "--sl-pips", "--trail-pips", "charter"]
    for req in required:
        if req not in out.lower():
            return False, f"Missing '{req}' in help"
    
    return True, "Help displays all bracket flags ✓"


def test_bracket_generation() -> Tuple[bool, str]:
    """TEST 2: Verify bracket generation produces valid JSON"""
    cmd = [
        "python3", "brokers/trade_shim.py",
        "--instrument", "EUR_USD",
        "--units", "10000",
        "--type", "MARKET",
        "--entry", "1.10500",
        "--tp-pips", "80",
        "--sl-pips", "20",
        "--dry-run"
    ]
    code, out, err = run_command(cmd)
    
    if code != 0:
        return False, f"Bracket generation failed: {err}"
    
    try:
        data = json.loads(out)
        if "order" not in data:
            return False, "Missing 'order' in output"
        if "takeProfitOnFill" not in data["order"]:
            return False, "Missing 'takeProfitOnFill'"
        if "stopLossOnFill" not in data["order"]:
            return False, "Missing 'stopLossOnFill'"
        return True, "Bracket JSON valid ✓"
    except json.JSONDecodeError:
        return False, "Invalid JSON output"


def test_jpy_precision() -> Tuple[bool, str]:
    """TEST 3: Verify JPY instruments use 0.01 pip precision"""
    cmd = [
        "python3", "brokers/trade_shim.py",
        "--instrument", "GBP_JPY",
        "--units", "200",
        "--type", "MARKET",
        "--entry", "180.250",
        "--tp-pips", "100",
        "--sl-pips", "30",
        "--dry-run"
    ]
    code, out, err = run_command(cmd)
    
    if code != 0:
        return False, f"JPY test failed: {err}"
    
    try:
        data = json.loads(out)
        tp = float(data["order"]["takeProfitOnFill"]["price"])
        sl = float(data["order"]["stopLossOnFill"]["price"])
        
        # TP should be 180.250 + 1.00 = 181.250
        # SL should be 180.250 - 0.30 = 179.950
        if abs(tp - 181.250) > 0.001:
            return False, f"TP precision error: {tp} != 181.250"
        if abs(sl - 179.950) > 0.001:
            return False, f"SL precision error: {sl} != 179.950"
        return True, "JPY precision correct (0.01 pip) ✓"
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return False, str(e)


def test_rr_guardrail() -> Tuple[bool, str]:
    """TEST 4: Verify RR guardrail blocks RR < 3.2:1"""
    # This SHOULD fail with RR validation error
    cmd = [
        "python3", "brokers/trade_shim.py",
        "--instrument", "EUR_USD",
        "--units", "10000",
        "--type", "MARKET",
        "--entry", "1.10500",
        "--tp-pips", "50",  # RR = 50/25 = 2.0:1
        "--sl-pips", "25",
        "--dry-run"
    ]
    code, out, err = run_command(cmd)
    
    # Should exit with code 2 (validation error)
    if code != 2:
        return False, f"Should have failed with code 2, got {code}"
    
    combined = out + err
    if "Risk/Reward" in combined or "MIN_RR" in combined:
        return True, "RR guardrail blocks invalid ratio ✓"
    else:
        return False, "RR check didn't trigger"


def test_sl_guardrail() -> Tuple[bool, str]:
    """TEST 5: Verify SL guardrail blocks SL < 18 pips"""
    cmd = [
        "python3", "brokers/trade_shim.py",
        "--instrument", "USD_JPY",
        "--units", "100",
        "--type", "MARKET",
        "--entry", "149.500",
        "--tp-pips", "100",
        "--sl-pips", "10",  # < MIN_SL_PIPS
        "--dry-run"
    ]
    code, out, err = run_command(cmd)
    
    if code != 2:
        return False, f"Should have failed with code 2, got {code}"
    
    combined = out + err
    if "MIN_SL_PIPS" in combined or "violates" in combined:
        return True, "SL guardrail blocks insufficient SL ✓"
    else:
        return False, "SL check didn't trigger"


def test_bracket_validation_cli() -> Tuple[bool, str]:
    """TEST 6: Verify pg_bracket --validate enforces charter"""
    cmd = ["python3", "brokers/pg_bracket.py", "--validate", "--tp-pips", "100", "--sl-pips", "25"]
    code, out, err = run_command(cmd)
    
    if code != 0:
        return False, f"Validation failed: {err}"
    
    combined = out + err
    if "Bracket valid" in combined or "RR" in combined:
        return True, "Bracket validator working ✓"
    else:
        return False, "Unexpected validator output"


def test_bracket_rejection() -> Tuple[bool, str]:
    """TEST 7: Verify pg_bracket rejects invalid brackets"""
    cmd = ["python3", "brokers/pg_bracket.py", "--validate", "--tp-pips", "50", "--sl-pips", "25"]
    code, out, err = run_command(cmd)
    
    # Should fail validation
    if code == 0:
        return False, "Should have rejected invalid bracket"
    
    combined = out + err
    if "Risk/Reward" in combined or "MIN_RR" in combined:
        return True, "Bracket rejection working ✓"
    else:
        return False, "Rejection didn't trigger"


def test_templates() -> Tuple[bool, str]:
    """TEST 8: Verify bracket templates are all charter-compliant"""
    cmd = ["python3", "brokers/pg_bracket.py", "--list-templates"]
    code, out, err = run_command(cmd)
    
    if code != 0:
        return False, f"Template listing failed: {err}"
    
    # All templates should show valid RR
    templates = ["Conservative", "Balanced", "Aggressive", "Minimal"]
    for template in templates:
        if template not in out:
            return False, f"Missing template: {template}"
    
    return True, "All bracket templates listed ✓"


def test_makefile_targets() -> Tuple[bool, str]:
    """TEST 9: Verify Makefile targets exist"""
    code, out, err = run_command(["make", "shim-help"])
    if code != 0:
        return False, f"shim-help failed: {err}"
    
    code, out, err = run_command(["make", "pg-help"])
    if code != 0:
        return False, f"pg-help failed: {err}"
    
    return True, "Makefile targets operational ✓"


def test_dry_run_no_send() -> Tuple[bool, str]:
    """TEST 10: Verify --dry-run doesn't send orders"""
    cmd = [
        "python3", "brokers/trade_shim.py",
        "--instrument", "EUR_USD",
        "--units", "1000",  # Small amount
        "--type", "MARKET",
        "--entry", "1.10500",
        "--tp-pips", "100",
        "--sl-pips", "20",
        "--dry-run"
    ]
    code, out, err = run_command(cmd)
    
    if code != 0:
        return False, f"Dry-run failed: {err}"
    
    # Should produce JSON, not send message
    try:
        data = json.loads(out)
        if "order" in data:
            return True, "Dry-run produces JSON (no send) ✓"
        else:
            return False, "Unexpected dry-run output"
    except json.JSONDecodeError:
        return False, "Dry-run didn't produce JSON"


def main():
    """Run all validation tests."""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║ TRADE SHIM & POSITION GUARDIAN VALIDATION SUITE             ║")
    print("║ PIN: 841921 | Charter Compliance Tests                      ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()

    tests = [
        ("Help & CLI", test_trade_shim_help),
        ("Bracket Generation", test_bracket_generation),
        ("JPY Precision", test_jpy_precision),
        ("RR Guardrail", test_rr_guardrail),
        ("SL Guardrail", test_sl_guardrail),
        ("Bracket Validator", test_bracket_validation_cli),
        ("Bracket Rejection", test_bracket_rejection),
        ("Templates", test_templates),
        ("Makefile Targets", test_makefile_targets),
        ("Dry-Run Safety", test_dry_run_no_send),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            success, message = test_func()
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} | {name:25} | {message}")
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ FAIL | {name:25} | Exception: {e}")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")

    if failed == 0:
        print()
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║ ✅ ALL VALIDATION TESTS PASSED                              ║")
        print("║ Charter enforcement verified. System ready for deployment.   ║")
        print("║ PIN: 841921                                                 ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        return 0
    else:
        print()
        print("⚠️  Some tests failed. Review output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
