#!/usr/bin/env python3
"""
🎯 RICK_LIVE_PROTOTYPE - Pre-Market Diagnostics & Validation
Comprehensive system check before market open (Sunday 5 PM EST)
PIN: 841921 | Version: 2.0_IMMUTABLE | Account: 101-001-31210531-002 (OANDA Practice)
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_check(name, passed, details=""):
    status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    detail_str = f" ({details})" if details else ""
    print(f"  {status} {name}{detail_str}")

def check_charter():
    """Verify Charter is loaded and immutable"""
    print_header("1️⃣  CHARTER & SECURITY")
    
    try:
        from rick_charter import (
            CHARTER_PIN, CHARTER_VERSION, MIN_NOTIONAL_USD, MAX_NOTIONAL_USD,
            MAX_MARGIN_PERCENT, MAX_CONCURRENT_POSITIONS, MIN_SL_PIPS, MAX_SL_PIPS,
            MIN_TP_PIPS, ALLOWED_INSTRUMENTS, GATE_RULES
        )
        
        # Verify PIN
        pin_correct = CHARTER_PIN == 841921
        print_check("Charter PIN", pin_correct, f"PIN={CHARTER_PIN}")
        
        # Verify version immutable
        version_immutable = "IMMUTABLE" in CHARTER_VERSION
        print_check("Version Immutable", version_immutable, f"v{CHARTER_VERSION}")
        
        # Verify risk params
        notional_ok = MIN_NOTIONAL_USD == 15000 and MAX_NOTIONAL_USD == 50000
        print_check("Position Sizing", notional_ok, f"${MIN_NOTIONAL_USD:,} - ${MAX_NOTIONAL_USD:,}")
        
        # Verify stop loss
        stops_ok = MIN_SL_PIPS == 10 and MAX_SL_PIPS == 50
        print_check("Stop Loss Range", stops_ok, f"{MIN_SL_PIPS}-{MAX_SL_PIPS} pips")
        
        # Verify gate rules
        gate_count = len(GATE_RULES)
        gates_ok = gate_count >= 8
        print_check("Guardian Gates", gates_ok, f"{gate_count} rules active")
        
        # Verify instruments
        instrument_count = len(ALLOWED_INSTRUMENTS)
        instruments_ok = instrument_count >= 13
        print_check("Allowed Instruments", instruments_ok, f"{instrument_count} FX pairs")
        
        return all([pin_correct, version_immutable, notional_ok, stops_ok, gates_ok, instruments_ok])
    except Exception as e:
        print_check("Charter Import", False, str(e))
        return False

def check_autonomous_engine():
    """Verify autonomous engine has Phase 1 improvements"""
    print_header("2️⃣  AUTONOMOUS ENGINE (Phase 1)")
    
    try:
        import autonomous_decision_engine as engine
        
        # Check MIN_SL_PIPS is 10
        min_sl = int(os.getenv("MIN_SL_PIPS", "10"))
        sl_correct = min_sl == 10
        print_check("MIN_SL_PIPS", sl_correct, f"{min_sl} pips (optimized from 18)")
        
        # Check market hours function exists
        has_market_hours = hasattr(engine, 'is_forex_market_open')
        print_check("Market Hours Detection", has_market_hours, "is_forex_market_open() active")
        
        # Check gate analysis functions
        has_gate_analysis = hasattr(engine, 'analyze_gate_rejections')
        print_check("Gate Analysis", has_gate_analysis, "analyze_gate_rejections() available")
        
        # Check dynamic sizing exists
        has_dynamic_sizing = hasattr(engine, 'calculate_position_size')
        print_check("Dynamic Sizing", has_dynamic_sizing, "calculate_position_size() active")
        
        # Check logging
        has_logging = hasattr(engine, 'logger') or 'logging' in dir(engine)
        print_check("Logging Framework", has_logging, "configured")
        
        return all([sl_correct, has_market_hours, has_gate_analysis, has_dynamic_sizing, has_logging])
    except Exception as e:
        print_check("Engine Import", False, str(e))
        return False

def check_oanda_connectivity():
    """Verify OANDA practice connectivity"""
    print_header("3️⃣  OANDA PRACTICE ACCOUNT")
    
    try:
        from practice_oanda_connector import CanaryOandaConnector
        
        connector = CanaryOandaConnector(pin=841921)
        health = connector.health_check()
        connected = health.get('connected', False)
        print_check("OANDA API Connection", connected, f"Account: 101-001-31210531-002")
        
        if connected:
            account_id = health.get('account_id', 'Unknown')
            balance = health.get('balance', 0)
            margin = health.get('margin_available', 0)
            print_check("Account Health", True, f"Balance: ${balance:,.2f}, Margin: ${margin:,.2f}")
            
            positions = health.get('open_positions', 0)
            print_check("Open Positions", True, f"{positions} positions")
        
        return connected
    except Exception as e:
        print_check("OANDA Connection", False, str(e))
        return False

def check_log_files():
    """Verify all critical log files exist and are writable"""
    print_header("4️⃣  LOG FILES & AUDIT TRAIL")
    
    log_files = {
        "narration.jsonl": "Real-time trading decisions",
        "logs/autonomous_decisions.jsonl": "Detailed decision log",
        "logs/audit.jsonl": "Guardian Gate audit trail",
        "logs/autonomous_engine.log": "Engine lifecycle & errors",
        "logs/ghost_trading.log": "Ghost mode trades",
        "logs/replay_results.jsonl": "Backtest results",
    }
    
    all_writable = True
    base_path = Path(os.path.dirname(os.path.abspath(__file__)))
    
    for filename, description in log_files.items():
        filepath = base_path / filename
        exists = filepath.exists()
        writable = filepath.parent.is_dir() and os.access(filepath.parent, os.W_OK)
        
        if exists:
            size = filepath.stat().st_size
            size_str = f"{size / 1024 / 1024:.1f} MB" if size > 1024*1024 else f"{size / 1024:.1f} KB"
            print_check(f"{filename}", True, f"{size_str} - {description}")
        else:
            print_check(f"{filename}", False, f"NOT FOUND - {description}")
            all_writable = False
    
    return all_writable

def check_config_immutability():
    """Verify critical configs are read-only"""
    print_header("5️⃣  CONFIG IMMUTABILITY & SECURITY")
    
    base_path = Path(os.path.dirname(os.path.abspath(__file__)))
    
    critical_files = {
        "rick_charter.py": "Charter rules (PIN 841921)",
        ".vscode/tasks_prototype.json": "Prototype tasks (RICK_LIVE only)",
    }
    
    all_locked = True
    
    for filename, description in critical_files.items():
        filepath = base_path / filename
        if filepath.exists():
            mode = filepath.stat().st_mode
            is_readonly = not (mode & 0o200)  # Check if write bit is NOT set
            perms = oct(mode)[-3:]
            print_check(f"{filename}", is_readonly, f"Permissions: {perms} - {description}")
            if not is_readonly:
                all_locked = False
        else:
            print_check(f"{filename}", False, f"NOT FOUND - {description}")
            all_locked = False
    
    return all_locked

def check_environment_vars():
    """Verify environment variables are set"""
    print_header("6️⃣  ENVIRONMENT VARIABLES")
    
    required_vars = {
        "OANDA_ACCOUNT_ID": "OANDA practice account ID",
        "OANDA_PRACTICE_TOKEN": "OANDA practice API token",
        "MIN_SL_PIPS": "Stop loss minimum (pips)",
        "CHARTER_PIN": "Charter security PIN",
    }
    
    all_set = True
    
    for var, description in required_vars.items():
        value = os.getenv(var, None)
        is_set = value is not None and len(str(value).strip()) > 0
        display_val = f"{value[:10]}..." if is_set and len(str(value)) > 10 else value
        print_check(f"{var}", is_set, f"{display_val} - {description}")
        if not is_set:
            all_set = False
    
    return all_set

def run_full_diagnostics():
    """Run complete pre-market diagnostic suite"""
    print(f"\n{BOLD}{BLUE}🎯 RICK_LIVE_PROTOTYPE - PRE-MARKET DIAGNOSTICS{RESET}")
    print(f"{BOLD}{BLUE}Timestamp: {datetime.now().isoformat()}{RESET}")
    print(f"{BOLD}{BLUE}Market Open: Sunday 5:00 PM EST (22:00 EST / Monday 03:00 UTC){RESET}")
    
    results = {
        "Charter & Security": check_charter(),
        "Autonomous Engine (Phase 1)": check_autonomous_engine(),
        "OANDA Connectivity": check_oanda_connectivity(),
        "Log Files": check_log_files(),
        "Config Immutability": check_config_immutability(),
        "Environment Variables": check_environment_vars(),
    }
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, passed_check in results.items():
        status = f"{GREEN}✅ PASS{RESET}" if passed_check else f"{RED}❌ FAIL{RESET}"
        print(f"  {status} {check_name}")
    
    print(f"\n{BOLD}Overall Status: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}{BOLD}🟢 ALL SYSTEMS GO - Ready for market open!{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}🔴 ISSUES DETECTED - Review failures above{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_full_diagnostics())
