#!/usr/bin/env python3
"""
Quick diagnostic: Verify Position Guardian is installed and ready to integrate.
Run this BEFORE wiring into your manager.

Usage:
    python3 pg_diagnostic.py

Expected output:
    ✅ All checks passed — ready to integrate
"""

import sys
import os
import json
from pathlib import Path

# Add plugins directory to path so imports work
sys.path.insert(0, '/home/ing/RICK/R_H_UNI/plugins')

def check_imports():
    """Verify all Position Guardian modules import correctly."""
    print("\n📦 Checking imports...")
    try:
        from position_guardian import (
            Position, Order, AccountState, HookResult,
            pre_trade_hook, tick_enforce, tl_dr_actions
        )
        print("  ✅ Core rules module imports OK")
    except Exception as e:
        print(f"  ❌ Core rules import failed: {e}")
        return False
    
    try:
        from position_guardian.manager_integration import PositionGuardianManager
        print("  ✅ Manager integration imports OK")
    except Exception as e:
        print(f"  ❌ Manager import failed: {e}")
        return False
    
    try:
        from position_guardian.profit_tracker import ProfitTracker
        print("  ✅ Profit tracker imports OK")
    except Exception as e:
        print(f"  ❌ Profit tracker import failed: {e}")
        return False
    
    return True

def check_directories():
    """Verify required directories exist."""
    print("\n📁 Checking directories...")
    
    required_dirs = [
        Path("/home/ing/RICK/R_H_UNI/plugins/position_guardian"),
        Path("/home/ing/RICK/R_H_UNI/logs"),
    ]
    
    all_ok = True
    for d in required_dirs:
        if d.exists():
            print(f"  ✅ {d}")
        else:
            print(f"  ❌ {d} MISSING")
            all_ok = False
    
    return all_ok

def check_files():
    """Verify required Python files exist."""
    print("\n📄 Checking files...")
    
    required_files = [
        "/home/ing/RICK/R_H_UNI/plugins/position_guardian/__init__.py",
        "/home/ing/RICK/R_H_UNI/plugins/position_guardian/rules.py",
        "/home/ing/RICK/R_H_UNI/plugins/position_guardian/manager_integration.py",
        "/home/ing/RICK/R_H_UNI/plugins/position_guardian/profit_tracker.py",
        "/home/ing/RICK/R_H_UNI/plugins/position_guardian/demo_now.py",
    ]
    
    all_ok = True
    for f in required_files:
        p = Path(f)
        size = p.stat().st_size if p.exists() else 0
        if p.exists() and size > 100:
            print(f"  ✅ {p.name} ({size} bytes)")
        else:
            print(f"  ❌ {p.name} MISSING or empty")
            all_ok = False
    
    return all_ok

def check_logs():
    """Check if logs directory is writable."""
    print("\n📝 Checking logs...")
    
    logs_dir = Path("/home/ing/RICK/R_H_UNI/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = logs_dir / "diagnostic_test.txt"
    try:
        test_file.write_text("test")
        test_file.unlink()
        print("  ✅ Logs directory is writable")
        return True
    except Exception as e:
        print(f"  ❌ Cannot write to logs: {e}")
        return False

def check_manager_initialization():
    """Try to initialize PositionGuardianManager."""
    print("\n🔧 Checking manager initialization...")
    
    try:
        from position_guardian.manager_integration import PositionGuardianManager
        pg = PositionGuardianManager()
        print("  ✅ PositionGuardianManager initialized successfully")
        
        # Try setting account state
        pg.set_account(nav=100000, margin_used=15000)
        print("  ✅ set_account() works")
        
        # Try gating a trade
        allowed, reason = pg.pg_trade("EURUSD", "buy", 10000)
        print(f"  ✅ pg_trade() works (EURUSD/BUY: {allowed}, reason: {reason})")
        
        # Try enforcing
        actions = pg.tick_enforce_positions()
        print(f"  ✅ tick_enforce_positions() works (returned {len(actions)} actions)")
        
        return True
    except Exception as e:
        print(f"  ❌ Manager initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_demo():
    """Verify demo_now.py runs."""
    print("\n🎮 Checking demo...")
    
    try:
        from position_guardian.demo_now import run_demo
        print("  ✅ demo_now imports OK")
        
        # Try running it (will print output)
        print("\n  Running demo_now.run_demo()...")
        run_demo()
        print("  ✅ demo_now ran successfully")
        return True
    except Exception as e:
        print(f"  ⚠️  demo_now failed (not critical): {e}")
        return False

def print_summary(results):
    """Print final summary."""
    print("\n" + "="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    if passed == total:
        print("✅ ALL CHECKS PASSED — Ready to integrate!")
        print("="*60)
        print("\nNext steps:")
        print("1. Read: /home/ing/RICK/R_H_UNI/LIVE_READINESS_CHECKLIST.md")
        print("2. Wire Position Guardian into your manager (see INTEGRATION_GUIDE.md)")
        print("3. Test in paper mode")
        print("4. Monitor 24h live")
        print("5. Deploy to production")
        return 0
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("="*60)
        print("\nFix the issues above, then run this diagnostic again.")
        return 1

if __name__ == "__main__":
    print("="*60)
    print("Position Guardian Diagnostic")
    print("="*60)
    
    results = {
        "imports": check_imports(),
        "directories": check_directories(),
        "files": check_files(),
        "logs": check_logs(),
        "manager_init": check_manager_initialization(),
        "demo": check_demo(),
    }
    
    sys.exit(print_summary(results))
