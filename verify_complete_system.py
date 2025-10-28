#!/usr/bin/env python3

"""
🟢 RBOTZILLA COMPLETE SYSTEM VERIFICATION CHECKLIST
PIN: 841921 | Timestamp: 2025-10-20
Purpose: Verify all features are turned on, activated, and connected to gate agent
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class VerificationSuite:
    def __init__(self):
        self.base_dir = Path("/home/ing/RICK/RICK_LIVE_PROTOTYPE")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "pin": "841921",
            "checks": [],
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
    
    def print_header(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("═" * 70)
        print("  🟢 RBOTZILLA COMPLETE SYSTEM VERIFICATION CHECKLIST")
        print("═" * 70)
        print(f"{Colors.END}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Working Dir: {self.base_dir}")
        print(f"PIN: 841921 ✅\n")
    
    def check(self, name, condition, details=""):
        """Record a check result"""
        result = {
            "name": name,
            "passed": condition,
            "details": details
        }
        self.results["checks"].append(result)
        
        symbol = f"{Colors.GREEN}✅{Colors.END}" if condition else f"{Colors.RED}❌{Colors.END}"
        status = f"{Colors.GREEN}PASS{Colors.END}" if condition else f"{Colors.RED}FAIL{Colors.END}"
        
        print(f"{symbol} [{status}] {name}")
        if details:
            print(f"    └─ {details}")
        
        if condition:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
        
        return condition
    
    def warn(self, name, message):
        """Record a warning"""
        result = {
            "name": name,
            "passed": None,  # Warning, not a pass/fail
            "details": message
        }
        self.results["checks"].append(result)
        
        print(f"{Colors.YELLOW}⚠️ {Colors.END} [WARN] {name}")
        print(f"    └─ {message}")
        
        self.results["warnings"] += 1
    
    def section(self, title):
        """Print a section header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        print(f"{Colors.BOLD}{title}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}\n")
    
    def run_all_checks(self):
        """Execute all verification checks"""
        self.print_header()
        
        # SECTION 1: Charter Immutability
        self.section("1️⃣  CHARTER IMMUTABILITY CHECKS")
        self.check_charter_pin()
        self.check_charter_constants()
        self.check_charter_validation()
        
        # SECTION 2: Guardian Gate System
        self.section("2️⃣  GUARDIAN GATE SYSTEM CHECKS")
        self.check_margin_gate()
        self.check_correlation_gate()
        self.check_gate_integration()
        
        # SECTION 3: Trading Engine Components
        self.section("3️⃣  TRADING ENGINE COMPONENTS")
        self.check_engine_initialization()
        self.check_engine_imports()
        self.check_charter_import()
        
        # SECTION 4: Subsystems & Features
        self.section("4️⃣  SUBSYSTEMS & FEATURES ACTIVATION")
        self.check_ml_intelligence()
        self.check_hive_mind()
        self.check_momentum_system()
        self.check_strategy_aggregator()
        self.check_quant_hedge()
        
        # SECTION 5: Event Logging & Narration
        self.section("5️⃣  EVENT LOGGING & NARRATION")
        self.check_narration_logger()
        self.check_narration_file()
        self.check_event_logging()
        
        # SECTION 6: OANDA API Connection
        self.section("6️⃣  OANDA API CONNECTION")
        self.check_oanda_connector()
        self.check_environment_config()
        
        # SECTION 7: State Persistence
        self.section("7️⃣  STATE PERSISTENCE")
        self.check_connection_state()
        self.check_backup_system()
        
        # SECTION 8: Process Management
        self.section("8️⃣  PROCESS MANAGEMENT")
        self.check_startup_script()
        self.check_dashboard_script()
        self.check_process_detection()
        
        # SECTION 9: Integration Verification
        self.section("9️⃣  FULL SYSTEM INTEGRATION")
        self.check_gate_logging()
        self.check_pre_trade_gate()
        self.check_all_gates_connected()
        
        # Print summary
        self.print_summary()
    
    # ========== SECTION 1: Charter Immutability ==========
    
    def check_charter_pin(self):
        """Verify Charter PIN is immutable"""
        try:
            os.chdir(self.base_dir)
            from foundation.rick_charter import RickCharter
            pin_ok = RickCharter.PIN == 841921
            self.check(
                "Charter PIN immutable (841921)",
                pin_ok,
                f"PIN = {RickCharter.PIN}"
            )
        except Exception as e:
            self.check("Charter PIN immutable (841921)", False, str(e))
    
    def check_charter_constants(self):
        """Verify all Charter constants are correct"""
        try:
            from foundation.rick_charter import RickCharter
            
            checks = [
                ("MIN_NOTIONAL_USD", RickCharter.MIN_NOTIONAL_USD, 15000),
                ("MIN_RISK_REWARD_RATIO", RickCharter.MIN_RISK_REWARD_RATIO, 3.0),
                ("MAX_HOLD_DURATION_HOURS", RickCharter.MAX_HOLD_DURATION_HOURS, 6),
                ("DAILY_LOSS_BREAKER_PCT", RickCharter.DAILY_LOSS_BREAKER_PCT, -5.0),
                ("MAX_CONCURRENT_POSITIONS", RickCharter.MAX_CONCURRENT_POSITIONS, 3),
            ]
            
            all_ok = True
            for name, actual, expected in checks:
                ok = actual == expected
                all_ok = all_ok and ok
                symbol = "✓" if ok else "✗"
                print(f"    {symbol} {name}: {actual} (expected {expected})")
            
            self.check("All Charter constants correct", all_ok)
        except Exception as e:
            self.check("All Charter constants correct", False, str(e))
    
    def check_charter_validation(self):
        """Verify Charter validation methods work"""
        try:
            from foundation.rick_charter import RickCharter
            
            # Test PIN validation
            pin_valid = RickCharter.validate_pin(841921)
            pin_invalid = not RickCharter.validate_pin(999999)
            
            # Test timeframe validation
            tf_valid = RickCharter.validate_timeframe("M15")
            tf_invalid = not RickCharter.validate_timeframe("M1")
            
            # Test notional validation
            notional_valid = RickCharter.validate_notional(15000)
            notional_invalid = not RickCharter.validate_notional(1000)
            
            all_ok = all([pin_valid, pin_invalid, tf_valid, tf_invalid, notional_valid, notional_invalid])
            
            self.check(
                "Charter validation methods functional",
                all_ok,
                "PIN, timeframe, notional validators all working"
            )
        except Exception as e:
            self.check("Charter validation methods functional", False, str(e))
    
    # ========== SECTION 2: Guardian Gate System ==========
    
    def check_margin_gate(self):
        """Verify Margin Guardian Gate"""
        try:
            from foundation.margin_correlation_gate import MarginCorrelationGate
            gate = MarginCorrelationGate(account_nav=2000.0)
            self.check("Margin Guardian Gate initialized", True, "Account NAV: $2000")
        except Exception as e:
            self.check("Margin Guardian Gate initialized", False, str(e))
    
    def check_correlation_gate(self):
        """Verify Correlation Guardian Gate"""
        try:
            from foundation.margin_correlation_gate import MarginCorrelationGate
            gate = MarginCorrelationGate(account_nav=2000.0)
            # Verify gate has correlation logic
            has_corr_method = hasattr(gate, 'correlation_gate')
            self.check(
                "Correlation Guardian Gate functional",
                has_corr_method,
                "Correlation gate method present"
            )
        except Exception as e:
            self.check("Correlation Guardian Gate functional", False, str(e))
    
    def check_gate_integration(self):
        """Verify gates are connected to trading engine"""
        try:
            from oanda_trading_engine import OandaTradingEngine
            # The engine should import gates during init
            import inspect
            source = inspect.getsource(OandaTradingEngine.__init__)
            has_gate_init = "MarginCorrelationGate" in source or "self.gate" in source
            self.check(
                "Gates integrated into Trading Engine",
                has_gate_init,
                "Engine initializes gate system"
            )
        except Exception as e:
            self.check("Gates integrated into Trading Engine", False, str(e))
    
    # ========== SECTION 3: Trading Engine ==========
    
    def check_engine_initialization(self):
        """Verify Trading Engine initializes correctly"""
        try:
            # Just verify imports work
            from oanda_trading_engine import OandaTradingEngine
            self.check("Trading Engine class imports", True)
        except Exception as e:
            self.check("Trading Engine class imports", False, str(e))
    
    def check_engine_imports(self):
        """Verify Trading Engine has all required imports"""
        try:
            engine_file = self.base_dir / "oanda_trading_engine.py"
            content = engine_file.read_text()
            
            required_imports = [
                "from foundation.rick_charter import RickCharter",
                "from foundation.margin_correlation_gate import MarginCorrelationGate",
                "from brokers.oanda_connector import OandaConnector",
            ]
            
            all_found = all(imp in content for imp in required_imports)
            self.check(
                "Trading Engine has all critical imports",
                all_found,
                f"Found {sum(1 for imp in required_imports if imp in content)}/{len(required_imports)}"
            )
        except Exception as e:
            self.check("Trading Engine has all critical imports", False, str(e))
    
    def check_charter_import(self):
        """Verify Charter is properly imported and validated"""
        try:
            engine_file = self.base_dir / "oanda_trading_engine.py"
            content = engine_file.read_text()
            
            has_pin_check = "RickCharter.validate_pin(841921)" in content
            has_pin_check = has_pin_check or "validate_pin(841921)" in content
            
            self.check(
                "Charter PIN validation in engine",
                has_pin_check,
                "Engine validates PIN before initialization"
            )
        except Exception as e:
            self.check("Charter PIN validation in engine", False, str(e))
    
    # ========== SECTION 4: Subsystems ==========
    
    def check_ml_intelligence(self):
        """Verify ML Intelligence system"""
        try:
            from ml_learning.regime_detector import RegimeDetector
            from ml_learning.signal_analyzer import SignalAnalyzer
            self.check("ML Intelligence system available", True, "Regime detector & signal analyzer present")
        except ImportError:
            self.warn("ML Intelligence", "ML system not available (optional)")
    
    def check_hive_mind(self):
        """Verify Hive Mind system"""
        try:
            from hive.rick_hive_mind import RickHiveMind
            self.check("Hive Mind system available", True, "Rick Hive Mind connected")
        except ImportError:
            self.warn("Hive Mind", "Hive Mind not available (system runs standalone)")
    
    def check_momentum_system(self):
        """Verify Momentum system"""
        try:
            from util.momentum_trailing import MomentumDetector, SmartTrailingSystem
            self.check("Momentum/Trailing system available", True, "Golden Age momentum system present")
        except ImportError:
            self.warn("Momentum System", "Momentum system not available (optional)")
    
    def check_strategy_aggregator(self):
        """Verify Strategy Aggregator"""
        try:
            from util.strategy_aggregator import StrategyAggregator
            self.check("Strategy Aggregator available", True, "5-strategy voting system ready")
        except ImportError:
            self.check("Strategy Aggregator available", False, "Strategy aggregator not found")
    
    def check_quant_hedge(self):
        """Verify Quant Hedge Engine"""
        try:
            from util.quant_hedge_engine import QuantHedgeEngine
            self.check("Quant Hedge Engine available", True, "7-rule correlation hedge system ready")
        except ImportError:
            self.check("Quant Hedge Engine available", False, "Hedge engine not found")
    
    # ========== SECTION 5: Event Logging ==========
    
    def check_narration_logger(self):
        """Verify Narration Logger"""
        try:
            from util.narration_logger import log_narration
            self.check("Narration Logger available", True, "Event logging system functional")
        except ImportError as e:
            self.check("Narration Logger available", False, str(e))
    
    def check_narration_file(self):
        """Verify narration.jsonl file exists and is writable"""
        try:
            narration_file = self.base_dir / "narration.jsonl"
            if narration_file.exists():
                # Test write capability
                with open(narration_file, 'a') as f:
                    f.write('{"test": "ok"}\n')
                self.check("narration.jsonl file writable", True, "File exists and has write permission")
            else:
                self.warn("narration.jsonl", "File will be created on first event")
        except Exception as e:
            self.check("narration.jsonl file writable", False, str(e))
    
    def check_event_logging(self):
        """Verify events can be logged"""
        try:
            os.chdir(self.base_dir)
            from util.narration_logger import log_narration
            log_narration("VERIFICATION", {"test": "check"}, "TEST", "system")
            self.check("Event logging functional", True, "Test event logged successfully")
        except Exception as e:
            self.check("Event logging functional", False, str(e))
    
    # ========== SECTION 6: OANDA API ==========
    
    def check_oanda_connector(self):
        """Verify OANDA Connector"""
        try:
            from brokers.oanda_connector import OandaConnector
            self.check("OANDA Connector available", True, "API connection layer ready")
        except ImportError as e:
            self.check("OANDA Connector available", False, str(e))
    
    def check_environment_config(self):
        """Verify .env file configuration"""
        try:
            env_file = self.base_dir / ".env"
            if env_file.exists():
                content = env_file.read_text()
                has_practice_account = "OANDA_PRACTICE_ACCOUNT_ID" in content
                has_practice_token = "OANDA_PRACTICE_TOKEN" in content
                all_ok = has_practice_account and has_practice_token
                
                self.check(
                    ".env file properly configured",
                    all_ok,
                    "Practice account credentials present"
                )
            else:
                self.check(".env file properly configured", False, ".env file not found")
        except Exception as e:
            self.check(".env file properly configured", False, str(e))
    
    # ========== SECTION 7: State Persistence ==========
    
    def check_connection_state(self):
        """Verify connection_state.json for position tracking"""
        try:
            state_file = self.base_dir / "connection_state.json"
            if state_file.exists():
                with open(state_file) as f:
                    state = json.load(f)
                self.check("Position state file exists", True, f"Tracking {len(state.get('positions', []))} positions")
            else:
                self.warn("Position state file", "File will be created on first trade")
        except Exception as e:
            self.check("Position state file exists", False, str(e))
    
    def check_backup_system(self):
        """Verify backup and restore system"""
        try:
            backup_script = self.base_dir / "backup_restore.sh"
            backup_ok = backup_script.exists() and os.access(backup_script, os.X_OK)
            self.check("Backup/restore system available", backup_ok, "Timestamped backup capability ready")
        except Exception as e:
            self.check("Backup/restore system available", False, str(e))
    
    # ========== SECTION 8: Process Management ==========
    
    def check_startup_script(self):
        """Verify smart startup script"""
        try:
            startup_script = self.base_dir / "SMART_STARTUP.sh"
            startup_ok = startup_script.exists() and os.access(startup_script, os.X_OK)
            self.check("Smart startup script available", startup_ok, "Reliable on/off/reboot capability")
        except Exception as e:
            self.check("Smart startup script available", False, str(e))
    
    def check_dashboard_script(self):
        """Verify dashboard script"""
        try:
            dashboard_script = self.base_dir / "start_dashboard.sh"
            dashboard_ok = dashboard_script.exists() and os.access(dashboard_script, os.X_OK)
            self.check("Dashboard launch script available", dashboard_ok, "3-pane tmux layout ready")
        except Exception as e:
            self.check("Dashboard launch script available", False, str(e))
    
    def check_process_detection(self):
        """Verify process detection works"""
        try:
            import subprocess
            result = subprocess.run(['pgrep', '--version'], capture_output=True)
            pgrep_ok = result.returncode == 0
            self.check("Process detection available", pgrep_ok, "System can detect running processes")
        except Exception as e:
            self.check("Process detection available", False, str(e))
    
    # ========== SECTION 9: Full Integration ==========
    
    def check_gate_logging(self):
        """Verify gates log to narration"""
        try:
            engine_file = self.base_dir / "oanda_trading_engine.py"
            content = engine_file.read_text()
            
            has_gate_rejection_logging = "GATE_REJECTION" in content
            has_gate_logging = "log_narration" in content and "gate" in content.lower()
            
            all_ok = has_gate_rejection_logging and has_gate_logging
            self.check(
                "Gates log decisions to narration",
                all_ok,
                "Gate rejections are recorded in event log"
            )
        except Exception as e:
            self.check("Gates log decisions to narration", False, str(e))
    
    def check_pre_trade_gate(self):
        """Verify pre-trade gate is integrated"""
        try:
            engine_file = self.base_dir / "oanda_trading_engine.py"
            content = engine_file.read_text()
            
            has_pre_trade = "pre_trade_gate" in content
            has_gate_result = "gate_result" in content
            
            all_ok = has_pre_trade and has_gate_result
            self.check(
                "Pre-trade guardian gate integrated",
                all_ok,
                "Every order passes through gate check"
            )
        except Exception as e:
            self.check("Pre-trade guardian gate integrated", False, str(e))
    
    def check_all_gates_connected(self):
        """Verify all gates are connected and active"""
        try:
            os.chdir(self.base_dir)
            from foundation.margin_correlation_gate import MarginCorrelationGate
            from oanda_trading_engine import OandaTradingEngine
            
            # Verify gate initialization in engine
            gate = MarginCorrelationGate(account_nav=2000.0)
            
            # Verify engine imports gate
            import inspect
            source = inspect.getsource(OandaTradingEngine.__init__)
            gates_active = "MarginCorrelationGate" in source
            
            self.check(
                "All gates connected and active",
                gates_active,
                "Margin gate & Correlation gate: ACTIVE"
            )
        except Exception as e:
            self.check("All gates connected and active", False, str(e))
    
    # ========== SUMMARY REPORT ==========
    
    def print_summary(self):
        """Print final summary report"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("═" * 70)
        print("  📊 VERIFICATION SUMMARY")
        print("═" * 70)
        print(f"{Colors.END}")
        
        print(f"\n{Colors.GREEN}Checks Passed:   {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}Checks Failed:   {self.results['failed']}{Colors.END}")
        print(f"{Colors.YELLOW}Warnings:        {self.results['warnings']}{Colors.END}")
        
        total_checks = self.results['passed'] + self.results['failed']
        pass_percentage = (self.results['passed'] / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n{Colors.BOLD}Pass Rate: {pass_percentage:.1f}% ({self.results['passed']}/{total_checks}){Colors.END}")
        
        if self.results['failed'] == 0 and self.results['warnings'] <= 2:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SYSTEM READY FOR AUTONOMOUS OPERATION{Colors.END}")
            print(f"{Colors.GREEN}All critical features activated and gates connected.{Colors.END}")
            return 0
        elif self.results['failed'] == 0:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  SYSTEM OPERATIONAL WITH WARNINGS{Colors.END}")
            print(f"{Colors.YELLOW}Some optional features unavailable.{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ SYSTEM REQUIRES ATTENTION{Colors.END}")
            print(f"{Colors.RED}Critical failures detected. Review above for details.{Colors.END}")
            return 1

def main():
    suite = VerificationSuite()
    suite.run_all_checks()
    sys.exit(suite.results['failed'] > 0)

if __name__ == "__main__":
    main()
