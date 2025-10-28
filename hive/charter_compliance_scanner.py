#!/usr/bin/env python3
"""
CHARTER COMPLIANCE SCANNER - Real-time Position Validation
Continuously monitors active positions against RICK immutable charter rules

PIN: 841921 | Generated: 2025-10-20

Charter Rules (Immutable):
  - MIN_SL = 18 pips (never less)
  - MIN_RR = 3.2:1 (never less)
  - MAX_MARGIN = 35% (hard cap)
  - MAX_POSITIONS = 3 (concurrent)
  - MAX_HOLD_TIME = 6 hours
  - MIN_NOTIONAL = $15,000
  - DAILY_LOSS_LIMIT = -5%

Alert Levels:
  - CRITICAL: Immediately halt trading
  - WARNING: Log and notify
  - INFO: Track and report
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, '/home/ing/RICK/RICK_LIVE_CLEAN')
sys.path.insert(0, '/home/ing/RICK/RICK_LIVE_PROTOTYPE')

# Load environment
env_file = '/home/ing/RICK/RICK_LIVE_CLEAN/master.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from util.narration_logger import log_narration
from util.terminal_display import TerminalDisplay, Colors


# ============================================================================
# ALERT LEVELS & VIOLATION MODELS
# ============================================================================

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class CharterViolation:
    """Single charter violation"""
    rule_name: str
    symbol: str
    current_value: float
    required_value: float
    threshold: str
    alert_level: AlertLevel
    action: str
    timestamp: datetime
    
    def __str__(self):
        return f"{self.symbol}: {self.rule_name} ({self.current_value} vs {self.required_value})"


# ============================================================================
# CHARTER RULES (IMMUTABLE)
# ============================================================================

class CharterRules:
    """Immutable RICK Charter rules - cannot be modified without PIN verification"""
    
    # Stop Loss Rules
    MIN_SL_PIPS = 18                    # Minimum 18 pips
    
    # Risk/Reward Rules
    MIN_RR_RATIO = 3.2                 # Minimum 3.2:1
    
    # Margin Rules
    MAX_MARGIN_UTILIZATION = 0.35      # 35% hard cap
    
    # Position Rules
    MAX_CONCURRENT_POSITIONS = 3       # Never more than 3
    MAX_HOLD_TIME_HOURS = 6            # Auto-close after 6 hours
    MAX_HOLD_TIME_SECONDS = MAX_HOLD_TIME_HOURS * 3600
    
    # Notional Rules
    MIN_NOTIONAL_USD = 15000            # Minimum $15k notional
    
    # Daily Rules
    DAILY_LOSS_LIMIT_PCT = -0.05       # -5% daily limit
    
    @classmethod
    def get_all_rules(cls) -> Dict[str, float]:
        """Get all charter rules as dict"""
        return {
            'MIN_SL_PIPS': cls.MIN_SL_PIPS,
            'MIN_RR_RATIO': cls.MIN_RR_RATIO,
            'MAX_MARGIN_UTILIZATION': cls.MAX_MARGIN_UTILIZATION,
            'MAX_CONCURRENT_POSITIONS': cls.MAX_CONCURRENT_POSITIONS,
            'MAX_HOLD_TIME_HOURS': cls.MAX_HOLD_TIME_HOURS,
            'MIN_NOTIONAL_USD': cls.MIN_NOTIONAL_USD,
            'DAILY_LOSS_LIMIT_PCT': cls.DAILY_LOSS_LIMIT_PCT,
        }


# ============================================================================
# CHARTER COMPLIANCE SCANNER
# ============================================================================

class CharterComplianceScanner:
    """
    Scans active trading positions against RICK charter rules.
    Generates violations and recommended actions.
    """
    
    def __init__(self):
        """Initialize scanner"""
        self.display = TerminalDisplay()
        self.violations: List[CharterViolation] = []
        self.last_scan_time: Optional[datetime] = None
        self.scan_history: List[Tuple[datetime, List[CharterViolation]]] = []
    
    # ========================================================================
    # MAIN SCAN FUNCTION
    # ========================================================================
    
    def scan_positions(
        self,
        positions: List[Dict],
        account_margin_ratio: float = 0.0,
        daily_pnl_pct: float = 0.0
    ) -> List[CharterViolation]:
        """
        Scan all positions against charter rules
        
        Args:
            positions: List of position dicts with keys:
                      [symbol, direction, entry_price, current_price, size, 
                       stop_loss, take_profit, open_time_seconds]
            account_margin_ratio: Current margin utilization (0.0-1.0)
            daily_pnl_pct: Daily P&L percentage
        
        Returns:
            List of CharterViolation objects
        """
        violations = []
        self.last_scan_time = datetime.now(timezone.utc)
        
        # ====================================================================
        # ACCOUNT-LEVEL SCANS
        # ====================================================================
        
        # Check position count
        if len(positions) > CharterRules.MAX_CONCURRENT_POSITIONS:
            violations.append(CharterViolation(
                rule_name="MAX_CONCURRENT_POSITIONS",
                symbol="SYSTEM",
                current_value=len(positions),
                required_value=CharterRules.MAX_CONCURRENT_POSITIONS,
                threshold=f"≤ {CharterRules.MAX_CONCURRENT_POSITIONS}",
                alert_level=AlertLevel.CRITICAL,
                action="CLOSE_EXCESS_POSITIONS",
                timestamp=self.last_scan_time
            ))
        
        # Check margin
        if account_margin_ratio > CharterRules.MAX_MARGIN_UTILIZATION:
            violations.append(CharterViolation(
                rule_name="MARGIN_UTILIZATION",
                symbol="SYSTEM",
                current_value=round(account_margin_ratio * 100, 2),
                required_value=CharterRules.MAX_MARGIN_UTILIZATION * 100,
                threshold=f"≤ {CharterRules.MAX_MARGIN_UTILIZATION * 100}%",
                alert_level=AlertLevel.CRITICAL,
                action="REDUCE_POSITIONS_IMMEDIATELY",
                timestamp=self.last_scan_time
            ))
        
        # Check daily loss limit
        if daily_pnl_pct <= CharterRules.DAILY_LOSS_LIMIT_PCT:
            violations.append(CharterViolation(
                rule_name="DAILY_LOSS_LIMIT",
                symbol="SYSTEM",
                current_value=round(daily_pnl_pct * 100, 2),
                required_value=CharterRules.DAILY_LOSS_LIMIT_PCT * 100,
                threshold=f"≥ {CharterRules.DAILY_LOSS_LIMIT_PCT * 100}%",
                alert_level=AlertLevel.CRITICAL,
                action="HALT_ALL_TRADING",
                timestamp=self.last_scan_time
            ))
        
        # ====================================================================
        # POSITION-LEVEL SCANS
        # ====================================================================
        
        for pos in positions:
            symbol = pos.get('symbol', 'UNKNOWN')
            direction = pos.get('direction', 'BUY')
            entry_price = pos.get('entry_price', 0)
            current_price = pos.get('current_price', 0)
            stop_loss = pos.get('stop_loss', 0)
            take_profit = pos.get('take_profit', 0)
            open_time_seconds = pos.get('open_time_seconds', 0)
            
            # Calculate pip size
            pip_size = 0.0001 if 'JPY' not in symbol else 0.01
            
            # ================================================================
            # RULE 1: STOP LOSS MINIMUM
            # ================================================================
            sl_pips = abs(stop_loss - entry_price) / pip_size
            
            if sl_pips < CharterRules.MIN_SL_PIPS:
                violations.append(CharterViolation(
                    rule_name="MIN_STOP_LOSS",
                    symbol=symbol,
                    current_value=round(sl_pips, 1),
                    required_value=CharterRules.MIN_SL_PIPS,
                    threshold=f"≥ {CharterRules.MIN_SL_PIPS} pips",
                    alert_level=AlertLevel.CRITICAL,
                    action="WIDEN_STOP_LOSS_OR_CLOSE",
                    timestamp=self.last_scan_time
                ))
            
            # ================================================================
            # RULE 2: RISK/REWARD RATIO
            # ================================================================
            tp_pips = abs(take_profit - entry_price) / pip_size
            rr_ratio = tp_pips / sl_pips if sl_pips > 0 else 0
            
            if rr_ratio < CharterRules.MIN_RR_RATIO:
                violations.append(CharterViolation(
                    rule_name="MIN_RISK_REWARD",
                    symbol=symbol,
                    current_value=round(rr_ratio, 2),
                    required_value=CharterRules.MIN_RR_RATIO,
                    threshold=f"≥ {CharterRules.MIN_RR_RATIO}:1",
                    alert_level=AlertLevel.CRITICAL,
                    action="ADJUST_TP_OR_CLOSE",
                    timestamp=self.last_scan_time
                ))
            
            # ================================================================
            # RULE 3: MAXIMUM HOLD TIME
            # ================================================================
            if open_time_seconds > CharterRules.MAX_HOLD_TIME_SECONDS:
                hold_hours = open_time_seconds / 3600
                
                violations.append(CharterViolation(
                    rule_name="MAX_HOLD_TIME",
                    symbol=symbol,
                    current_value=round(hold_hours, 1),
                    required_value=CharterRules.MAX_HOLD_TIME_HOURS,
                    threshold=f"≤ {CharterRules.MAX_HOLD_TIME_HOURS} hours",
                    alert_level=AlertLevel.WARNING,
                    action="CLOSE_POSITION_TTL_EXCEEDED",
                    timestamp=self.last_scan_time
                ))
        
        # Store in history (keep last 100)
        self.scan_history.append((self.last_scan_time, violations))
        if len(self.scan_history) > 100:
            self.scan_history.pop(0)
        
        self.violations = violations
        return violations
    
    # ========================================================================
    # VIOLATION ANALYSIS
    # ========================================================================
    
    def get_critical_violations(self) -> List[CharterViolation]:
        """Get only critical violations"""
        return [v for v in self.violations if v.alert_level == AlertLevel.CRITICAL]
    
    def get_warning_violations(self) -> List[CharterViolation]:
        """Get only warning violations"""
        return [v for v in self.violations if v.alert_level == AlertLevel.WARNING]
    
    def get_violations_by_symbol(self, symbol: str) -> List[CharterViolation]:
        """Get violations for a specific symbol"""
        return [v for v in self.violations if v.symbol == symbol]
    
    def should_halt_trading(self) -> bool:
        """Check if any critical violations require immediate halt"""
        for v in self.get_critical_violations():
            if v.action in ["HALT_ALL_TRADING", "REDUCE_POSITIONS_IMMEDIATELY"]:
                return True
        return False
    
    # ========================================================================
    # LOGGING & DISPLAY
    # ========================================================================
    
    def log_violations(self):
        """Log all violations to narration"""
        if not self.violations:
            return
        
        for violation in self.violations:
            log_narration(
                event_type="CHARTER_VIOLATION",
                details={
                    "rule": violation.rule_name,
                    "symbol": violation.symbol,
                    "current": violation.current_value,
                    "required": violation.required_value,
                    "threshold": violation.threshold,
                    "level": violation.alert_level.value,
                    "action": violation.action
                },
                symbol=violation.symbol,
                venue="charter_compliance"
            )
    
    def display_violations(self):
        """Display violations to terminal"""
        if not self.violations:
            self.display.success("✅ All positions charter compliant")
            return
        
        critical = self.get_critical_violations()
        warnings = self.get_warning_violations()
        
        self.display.section("CHARTER COMPLIANCE SCAN")
        
        if critical:
            self.display.alert(f"🚨 {len(critical)} CRITICAL VIOLATION(S)", "CRITICAL")
            for v in critical:
                self.display.error(
                    f"  {v.symbol}: {v.rule_name}",
                    Colors.BRIGHT_RED
                )
                self.display.info("    Current", f"{v.current_value} {v.symbol}")
                self.display.info("    Required", f"{v.threshold}")
                self.display.info("    Action", v.action, Colors.BRIGHT_RED)
        
        if warnings:
            self.display.warning(f"⚠️  {len(warnings)} WARNING(S)")
            for v in warnings:
                self.display.warning(f"  {v.symbol}: {v.rule_name}")
                self.display.info("    Current", f"{v.current_value} {v.symbol}")
                self.display.info("    Required", f"{v.threshold}")
                self.display.info("    Action", v.action)
        
        print()
    
    def get_summary(self) -> Dict:
        """Get summary of violations"""
        critical = self.get_critical_violations()
        warnings = self.get_warning_violations()
        
        return {
            'timestamp': self.last_scan_time.isoformat() if self.last_scan_time else None,
            'total_violations': len(self.violations),
            'critical': len(critical),
            'warnings': len(warnings),
            'should_halt': self.should_halt_trading(),
            'violations': [
                {
                    'rule': v.rule_name,
                    'symbol': v.symbol,
                    'current': v.current_value,
                    'required': v.required_value,
                    'level': v.alert_level.value,
                    'action': v.action
                }
                for v in self.violations
            ]
        }


if __name__ == "__main__":
    # Example usage
    scanner = CharterComplianceScanner()
    
    # Example positions
    test_positions = [
        {
            'symbol': 'EUR_USD',
            'direction': 'BUY',
            'entry_price': 1.0800,
            'current_price': 1.0850,
            'stop_loss': 1.0750,
            'take_profit': 1.1100,
            'open_time_seconds': 3600,
        }
    ]
    
    violations = scanner.scan_positions(test_positions, account_margin_ratio=0.25)
    scanner.display_violations()
    print(scanner.get_summary())
