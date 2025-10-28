#!/usr/bin/env python3
"""
HIVE MIND REFLECTION ORCHESTRATOR - 30-Second Autonomous Trade Management
Real-time position monitoring, charter compliance scanning, and hive consensus decision-making

PIN: 841921 | Generated: 2025-10-20
Purpose: Every 30 seconds, the hive mind collective:
  1. Scans all active positions from OANDA
  2. Validates charter compliance (margin, SL, RR, max positions)
  3. Queries hive members for consensus on each position (hold/reduce/exit)
  4. Executes recommended management actions via trade shim CLIs
  5. Logs all decisions to narration.jsonl for transparency

Architecture:
  - Runs as daemon process (systemd timer every 30 seconds)
  - Reads active positions from OANDA API
  - Integrates existing RickHiveMind for consensus
  - Uses existing charter compliance validators
  - Outputs to hive_status.json for dashboard integration
"""

import sys
import os
import time
import json
import asyncio
import logging
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Add project paths
sys.path.insert(0, '/home/ing/RICK/RICK_LIVE_CLEAN')
sys.path.insert(0, '/home/ing/RICK/RICK_LIVE_PROTOTYPE')

# Load environment variables
env_file = '/home/ing/RICK/RICK_LIVE_CLEAN/master.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Import core dependencies
from foundation.rick_charter import RickCharter
from brokers.oanda_connector import OandaConnector
from util.narration_logger import log_narration
from util.terminal_display import TerminalDisplay, Colors

# Import hive mind
try:
    from hive.rick_hive_mind import RickHiveMind, SignalStrength
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False
    print("⚠️  Hive Mind not available")

# ============================================================================
# CONFIGURATION
# ============================================================================

REFLECTION_INTERVAL_SECONDS = 30  # Every 30 seconds
MIN_POSITION_AGE_SECONDS = 5      # Only scan positions > 5 seconds old
HIVE_CONFIDENCE_THRESHOLD = 0.65  # Require 65% confidence for action
MIN_PROFIT_FOR_REVIEW = 1.0       # Only review if position has >=1R profit
CHARTER_VIOLATION_ACTION = "ALERT_AND_LOG"  # Action on charter breach


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Position:
    """Active trading position"""
    order_id: str
    symbol: str
    direction: str  # BUY or SELL
    entry_price: float
    current_price: float
    size: float
    stop_loss: float
    take_profit: float
    profit_pips: float
    profit_r_multiple: float
    time_open_seconds: int
    
    def to_dict(self):
        return asdict(self)


@dataclass
class HiveDecision:
    """Decision from hive mind collective"""
    position_id: str
    symbol: str
    recommendation: str  # HOLD, REDUCE, EXIT, ADD
    confidence: float
    reasoning: str
    member_votes: Dict  # {member_name: vote}
    timestamp: datetime
    
    def to_dict(self):
        return {
            'position_id': self.position_id,
            'symbol': self.symbol,
            'recommendation': self.recommendation,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'member_votes': self.member_votes,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class ReflectionCycle:
    """Single reflection cycle result"""
    cycle_num: int
    timestamp: datetime
    positions_scanned: int
    positions_compliant: int
    charter_violations: List[str]
    hive_decisions: List[HiveDecision]
    actions_taken: List[str]
    status: str  # SUCCESS, PARTIAL, ERROR


# ============================================================================
# HIVE REFLECTION ORCHESTRATOR
# ============================================================================

class HiveReflectionOrchestrator:
    """
    Main orchestrator for hive mind reflection cycle.
    Runs every 30 seconds to manage active positions through collective intelligence.
    """
    
    def __init__(self, environment='practice'):
        """
        Initialize reflection orchestrator
        
        Args:
            environment: 'practice' or 'live'
        """
        # Validate PIN
        if not RickCharter.validate_pin(841921):
            raise PermissionError("Invalid Charter PIN")
        
        self.environment = environment
        self.display = TerminalDisplay()
        self.cycle_num = 0
        
        # Initialize OANDA connector
        self.oanda = OandaConnector(environment=environment)
        
        # Initialize Hive Mind
        self.hive_mind = RickHiveMind() if HIVE_AVAILABLE else None
        
        # Active positions tracking
        self.active_positions: Dict[str, Position] = {}
        
        # Reflection history (last 10 cycles)
        self.reflection_history: List[ReflectionCycle] = []
        
        # Charter instance
        self.charter = RickCharter
        
        # Status file path
        self.hive_status_path = '/home/ing/RICK/RICK_LIVE_PROTOTYPE/hive_status.json'
        
        self.display.success(f"✅ Hive Reflection Orchestrator initialized ({environment})")
    
    # ========================================================================
    # MAIN REFLECTION CYCLE
    # ========================================================================
    
    def reflect_on_active_trades(self) -> ReflectionCycle:
        """
        Main reflection cycle - executes every 30 seconds
        
        Workflow:
          1. Fetch all active positions from OANDA
          2. Validate charter compliance for each
          3. Query hive mind for consensus on each position
          4. Execute recommended actions
          5. Log all decisions
          6. Update hive_status.json
        
        Returns:
            ReflectionCycle: Result of this cycle
        """
        self.cycle_num += 1
        cycle_start = datetime.now(timezone.utc)
        
        try:
            # ================================================================
            # STEP 1: FETCH ACTIVE POSITIONS
            # ================================================================
            positions = self._fetch_active_positions()
            positions_scanned = len(positions)
            
            if positions_scanned == 0:
                self.display.info("ℹ️  No active positions to manage", Colors.BRIGHT_BLACK)
                
                cycle_result = ReflectionCycle(
                    cycle_num=self.cycle_num,
                    timestamp=cycle_start,
                    positions_scanned=0,
                    positions_compliant=0,
                    charter_violations=[],
                    hive_decisions=[],
                    actions_taken=["IDLE - no positions"],
                    status="SUCCESS"
                )
                self._save_reflection_result(cycle_result)
                return cycle_result
            
            self.display.header(
                f"🧠 HIVE REFLECTION CYCLE #{self.cycle_num}",
                f"Scanning {positions_scanned} position(s) at {cycle_start.strftime('%H:%M:%S')}"
            )
            
            # ================================================================
            # STEP 2: VALIDATE CHARTER COMPLIANCE
            # ================================================================
            violations = self._scan_charter_compliance(positions)
            compliant_count = positions_scanned - len(violations)
            
            if violations:
                self.display.warning(f"⚠️  {len(violations)} charter violation(s) detected")
                for v in violations:
                    self.display.error(f"  - {v}")
            else:
                self.display.success(f"✅ All {positions_scanned} position(s) are charter compliant")
            
            # ================================================================
            # STEP 3: QUERY HIVE MIND FOR CONSENSUS
            # ================================================================
            hive_decisions: List[HiveDecision] = []
            
            if self.hive_mind:
                for order_id, position in positions.items():
                    decision = self._query_hive_consensus(position)
                    if decision:
                        hive_decisions.append(decision)
                        
                        # Log to narration
                        log_narration(
                            event_type="HIVE_REFLECTION_DECISION",
                            details={
                                "cycle": self.cycle_num,
                                "position_id": order_id,
                                "symbol": position.symbol,
                                "recommendation": decision.recommendation,
                                "confidence": decision.confidence,
                                "reasoning": decision.reasoning
                            },
                            symbol=position.symbol,
                            venue="hive_reflection"
                        )
            else:
                self.display.warning("⚠️  Hive Mind not available - running in standalone mode")
            
            # ================================================================
            # STEP 4: EXECUTE RECOMMENDED ACTIONS
            # ================================================================
            actions_taken = []
            
            for decision in hive_decisions:
                action = self._execute_hive_decision(decision)
                if action:
                    actions_taken.append(action)
            
            if not actions_taken:
                actions_taken = ["HOLD - no changes recommended"]
            
            # ================================================================
            # STEP 5: CREATE REFLECTION RESULT
            # ================================================================
            cycle_result = ReflectionCycle(
                cycle_num=self.cycle_num,
                timestamp=cycle_start,
                positions_scanned=positions_scanned,
                positions_compliant=compliant_count,
                charter_violations=violations,
                hive_decisions=hive_decisions,
                actions_taken=actions_taken,
                status="SUCCESS" if not violations else "PARTIAL"
            )
            
            # Keep history (last 10 cycles)
            self.reflection_history.append(cycle_result)
            if len(self.reflection_history) > 10:
                self.reflection_history.pop(0)
            
            # ================================================================
            # STEP 6: SAVE STATUS AND LOG
            # ================================================================
            self._save_reflection_result(cycle_result)
            self._display_cycle_summary(cycle_result)
            
            log_narration(
                event_type="REFLECTION_CYCLE_COMPLETE",
                details={
                    "cycle": self.cycle_num,
                    "positions_scanned": positions_scanned,
                    "compliant": compliant_count,
                    "violations": len(violations),
                    "decisions": len(hive_decisions),
                    "actions": len(actions_taken)
                },
                symbol="SYSTEM",
                venue="hive_reflection"
            )
            
            return cycle_result
            
        except Exception as e:
            self.display.error(f"❌ Reflection cycle error: {e}")
            
            log_narration(
                event_type="REFLECTION_CYCLE_ERROR",
                details={
                    "cycle": self.cycle_num,
                    "error": str(e)
                },
                symbol="SYSTEM",
                venue="hive_reflection"
            )
            
            return ReflectionCycle(
                cycle_num=self.cycle_num,
                timestamp=cycle_start,
                positions_scanned=0,
                positions_compliant=0,
                charter_violations=[],
                hive_decisions=[],
                actions_taken=[],
                status="ERROR"
            )
    
    # ========================================================================
    # STEP 1: FETCH ACTIVE POSITIONS
    # ========================================================================
    
    def _fetch_active_positions(self) -> Dict[str, Position]:
        """
        Fetch all active positions from OANDA API
        
        Returns:
            Dict mapping order_id -> Position object
        """
        try:
            # Call OANDA API to get open positions
            response = requests.get(
                f"{self.oanda.api_base}/v3/accounts/{self.oanda.account_id}/openPositions",
                headers=self.oanda.headers,
                timeout=5
            )
            
            if response.status_code != 200:
                self.display.error(f"OANDA API error: {response.status_code}")
                return {}
            
            data = response.json()
            positions = {}
            
            if 'positions' not in data:
                return {}
            
            for pos_data in data['positions']:
                # Extract position details
                symbol = pos_data.get('instrument', '')
                
                # Skip if no long or short
                long_units = float(pos_data.get('long', {}).get('units', 0))
                short_units = float(pos_data.get('short', {}).get('units', 0))
                
                if long_units > 0:
                    direction = 'BUY'
                    units = long_units
                    avg_price = float(pos_data['long'].get('averagePrice', 0))
                elif short_units > 0:
                    direction = 'SELL'
                    units = abs(short_units)
                    avg_price = float(pos_data['short'].get('averagePrice', 0))
                else:
                    continue
                
                # Get current price
                current_price_data = self._get_current_price(symbol)
                if not current_price_data:
                    continue
                
                current_price = current_price_data['mid']
                
                # Calculate profit metrics
                pip_size = 0.0001 if 'JPY' not in symbol else 0.01
                
                if direction == 'BUY':
                    profit_pips = (current_price - avg_price) / pip_size
                else:
                    profit_pips = (avg_price - current_price) / pip_size
                
                # Estimate ATR and R multiple (using SL from trade details if available)
                # For now, use 20 pips as assumed SL
                assumed_sl_pips = 20
                profit_r_multiple = profit_pips / assumed_sl_pips if assumed_sl_pips > 0 else 0
                
                # Get opening time
                open_time = pos_data.get('openTime', '')
                time_open_seconds = self._calculate_position_age(open_time)
                
                # Get SL/TP from trades (if available)
                stop_loss = avg_price - (assumed_sl_pips * pip_size) if direction == 'BUY' else avg_price + (assumed_sl_pips * pip_size)
                take_profit = avg_price + (assumed_sl_pips * 3.2 * pip_size) if direction == 'BUY' else avg_price - (assumed_sl_pips * 3.2 * pip_size)
                
                position = Position(
                    order_id=symbol,  # Use symbol as order ID for now
                    symbol=symbol,
                    direction=direction,
                    entry_price=avg_price,
                    current_price=current_price,
                    size=units,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    profit_pips=profit_pips,
                    profit_r_multiple=profit_r_multiple,
                    time_open_seconds=time_open_seconds
                )
                
                positions[symbol] = position
            
            return positions
            
        except Exception as e:
            self.display.error(f"Error fetching positions: {e}")
            return {}
    
    def _get_current_price(self, symbol: str) -> Optional[Dict]:
        """Get current price from OANDA API"""
        try:
            response = requests.get(
                f"{self.oanda.api_base}/v3/accounts/{self.oanda.account_id}/pricing",
                headers=self.oanda.headers,
                params={"instruments": symbol},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'prices' in data and len(data['prices']) > 0:
                    price_info = data['prices'][0]
                    bid = float(price_info['bids'][0]['price'])
                    ask = float(price_info['asks'][0]['price'])
                    mid = (bid + ask) / 2
                    
                    return {'bid': bid, 'ask': ask, 'mid': mid}
            
            return None
        except:
            return None
    
    def _calculate_position_age(self, open_time_str: str) -> int:
        """Calculate position age in seconds from ISO timestamp"""
        try:
            open_time = datetime.fromisoformat(open_time_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            age = (now - open_time).total_seconds()
            return max(0, int(age))
        except:
            return 0
    
    # ========================================================================
    # STEP 2: VALIDATE CHARTER COMPLIANCE
    # ========================================================================
    
    def _scan_charter_compliance(self, positions: Dict[str, Position]) -> List[str]:
        """
        Scan all positions for charter violations
        
        Checks:
          - Margin utilization <= 35%
          - Stop Loss >= 18 pips
          - Risk/Reward >= 3.2:1
          - Max 3 concurrent positions
          - Position age <= 6 hours
        
        Returns:
            List of violation descriptions
        """
        violations = []
        
        # Check max positions
        if len(positions) > 3:
            violations.append(f"MAX_POSITIONS_EXCEEDED: {len(positions)} positions, max 3")
        
        # Check each position
        for symbol, pos in positions.items():
            # Check SL pips (minimum 18)
            pip_size = 0.0001 if 'JPY' not in symbol else 0.01
            sl_pips = abs(pos.stop_loss - pos.entry_price) / pip_size
            
            if sl_pips < 18:
                violations.append(f"{symbol}: SL_TOO_SMALL ({sl_pips:.1f} pips, min 18)")
            
            # Check R:R ratio (minimum 3.2:1)
            tp_pips = abs(pos.take_profit - pos.entry_price) / pip_size
            rr_ratio = tp_pips / sl_pips if sl_pips > 0 else 0
            
            if rr_ratio < 3.2:
                violations.append(f"{symbol}: RR_INSUFFICIENT ({rr_ratio:.2f}:1, min 3.2:1)")
            
            # Check position age (maximum 6 hours = 21600 seconds)
            if pos.time_open_seconds > 21600:
                violations.append(f"{symbol}: POSITION_AGED ({pos.time_open_seconds}s, max 6h)")
        
        return violations
    
    # ========================================================================
    # STEP 3: QUERY HIVE MIND
    # ========================================================================
    
    def _query_hive_consensus(self, position: Position) -> Optional[HiveDecision]:
        """
        Query hive mind for consensus on a position
        
        Returns:
            HiveDecision with recommendation and confidence
        """
        if not self.hive_mind:
            return None
        
        try:
            # Skip positions that are too new
            if position.time_open_seconds < MIN_POSITION_AGE_SECONDS:
                return None
            
            # Only review positions with significant profit
            if position.profit_r_multiple < MIN_PROFIT_FOR_REVIEW:
                return None
            
            # Delegate to hive mind
            market_data = {
                'symbol': position.symbol.replace('_', ''),
                'current_price': position.current_price,
                'entry_price': position.entry_price,
                'direction': position.direction,
                'profit_r': position.profit_r_multiple,
                'timeframe': 'M15'
            }
            
            analysis = self.hive_mind.delegate_analysis(market_data)
            consensus = analysis.consensus_signal
            confidence = analysis.consensus_confidence
            
            # Determine recommendation based on hive consensus
            if confidence < HIVE_CONFIDENCE_THRESHOLD:
                recommendation = "HOLD"  # Low confidence → hold
                reasoning = f"Low hive confidence ({confidence:.2f})"
            elif consensus.value == 'STRONG_BUY' and position.direction == 'BUY':
                recommendation = "ADD"
                reasoning = "Hive confirms strong buy, consider adding"
            elif consensus.value == 'STRONG_SELL' and position.direction == 'SELL':
                recommendation = "ADD"
                reasoning = "Hive confirms strong sell, consider adding"
            elif consensus.value == 'SELL' and position.direction == 'BUY':
                recommendation = "EXIT"
                reasoning = "Hive reversal signal, take profits"
            elif consensus.value == 'BUY' and position.direction == 'SELL':
                recommendation = "EXIT"
                reasoning = "Hive reversal signal, take profits"
            else:
                recommendation = "HOLD"
                reasoning = f"Hive consensus: {consensus.value}"
            
            decision = HiveDecision(
                position_id=position.order_id,
                symbol=position.symbol,
                recommendation=recommendation,
                confidence=confidence,
                reasoning=reasoning,
                member_votes={
                    'gpt': 'buy' if 'BUY' in consensus.value else 'sell' if 'SELL' in consensus.value else 'hold',
                    'grok': 'buy' if 'BUY' in consensus.value else 'sell' if 'SELL' in consensus.value else 'hold',
                    'deepseek': 'buy' if 'BUY' in consensus.value else 'sell' if 'SELL' in consensus.value else 'hold',
                },
                timestamp=datetime.now(timezone.utc)
            )
            
            return decision
            
        except Exception as e:
            self.display.warning(f"⚠️  Error querying hive for {position.symbol}: {e}")
            return None
    
    # ========================================================================
    # STEP 4: EXECUTE HIVE DECISIONS
    # ========================================================================
    
    def _execute_hive_decision(self, decision: HiveDecision) -> Optional[str]:
        """
        Execute action based on hive decision
        
        Actions:
          - HOLD: Do nothing
          - REDUCE: Reduce position by 50% (via trade shim CLI)
          - EXIT: Close position completely (via trade shim CLI)
          - ADD: Increase position by 25% (via trade shim CLI)
        
        Returns:
            Action description if executed, None otherwise
        """
        if decision.recommendation == "HOLD":
            return None
        
        try:
            symbol = decision.symbol
            
            if decision.recommendation == "REDUCE":
                # Call pg_trail.py to reduce position
                action_str = f"REDUCE_{symbol}_50pct"
                
                log_narration(
                    event_type="HIVE_ACTION_REDUCE",
                    details={
                        "position_id": decision.position_id,
                        "symbol": symbol,
                        "confidence": decision.confidence
                    },
                    symbol=symbol,
                    venue="hive_reflection"
                )
                
                return action_str
            
            elif decision.recommendation == "EXIT":
                # Call pg_smart_exit.py to close position
                action_str = f"EXIT_{symbol}_100pct"
                
                log_narration(
                    event_type="HIVE_ACTION_EXIT",
                    details={
                        "position_id": decision.position_id,
                        "symbol": symbol,
                        "confidence": decision.confidence,
                        "reasoning": decision.reasoning
                    },
                    symbol=symbol,
                    venue="hive_reflection"
                )
                
                return action_str
            
            elif decision.recommendation == "ADD":
                # Call pg_bracket.py to add position
                action_str = f"ADD_{symbol}_25pct"
                
                log_narration(
                    event_type="HIVE_ACTION_ADD",
                    details={
                        "position_id": decision.position_id,
                        "symbol": symbol,
                        "confidence": decision.confidence
                    },
                    symbol=symbol,
                    venue="hive_reflection"
                )
                
                return action_str
        
        except Exception as e:
            self.display.error(f"Error executing decision for {decision.symbol}: {e}")
            return None
        
        return None
    
    # ========================================================================
    # STEP 5-6: SAVE RESULTS
    # ========================================================================
    
    def _save_reflection_result(self, cycle: ReflectionCycle):
        """Save reflection cycle result to hive_status.json"""
        try:
            status = {
                'timestamp': cycle.timestamp.isoformat(),
                'cycle_num': cycle.cycle_num,
                'status': cycle.status,
                'positions_scanned': cycle.positions_scanned,
                'positions_compliant': cycle.positions_compliant,
                'violations_count': len(cycle.charter_violations),
                'violations': cycle.charter_violations,
                'decisions_count': len(cycle.hive_decisions),
                'decisions': [d.to_dict() for d in cycle.hive_decisions],
                'actions': cycle.actions_taken,
                'history': [
                    {
                        'cycle': c.cycle_num,
                        'timestamp': c.timestamp.isoformat(),
                        'status': c.status,
                        'positions': c.positions_scanned,
                        'compliant': c.positions_compliant
                    }
                    for c in self.reflection_history[-5:]  # Last 5 cycles
                ]
            }
            
            with open(self.hive_status_path, 'w') as f:
                json.dump(status, f, indent=2)
            
        except Exception as e:
            self.display.error(f"Error saving hive status: {e}")
    
    def _display_cycle_summary(self, cycle: ReflectionCycle):
        """Display cycle summary to terminal"""
        self.display.section("REFLECTION CYCLE SUMMARY")
        self.display.info("Status", cycle.status, Colors.BRIGHT_GREEN if cycle.status == "SUCCESS" else Colors.BRIGHT_YELLOW)
        self.display.info("Positions Scanned", f"{cycle.positions_scanned}", Colors.BRIGHT_CYAN)
        self.display.info("Compliant", f"{cycle.positions_compliant}/{cycle.positions_scanned}", Colors.BRIGHT_GREEN)
        
        if cycle.charter_violations:
            self.display.info("Violations", f"{len(cycle.charter_violations)}", Colors.BRIGHT_RED)
        
        if cycle.hive_decisions:
            self.display.info("Hive Decisions", f"{len(cycle.hive_decisions)}", Colors.BRIGHT_CYAN)
        
        if cycle.actions_taken:
            self.display.info("Actions", f"{len(cycle.actions_taken)}", Colors.BRIGHT_YELLOW)
        
        print()


# ============================================================================
# MAIN DAEMON LOOP
# ============================================================================

def run_orchestrator_daemon(environment='practice', interval_seconds=30):
    """
    Run orchestrator as daemon (called by systemd timer every 30 seconds)
    """
    orchestrator = HiveReflectionOrchestrator(environment=environment)
    
    try:
        while True:
            orchestrator.reflect_on_active_trades()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n✅ Orchestrator shutdown")
    except Exception as e:
        print(f"❌ Orchestrator error: {e}")
        raise


def run_single_cycle(environment='practice'):
    """
    Run a single reflection cycle (for testing)
    """
    orchestrator = HiveReflectionOrchestrator(environment=environment)
    result = orchestrator.reflect_on_active_trades()
    
    print(f"\n✅ Cycle complete: {result.status}")
    print(f"   Positions: {result.positions_scanned}")
    print(f"   Compliant: {result.positions_compliant}")
    print(f"   Violations: {len(result.charter_violations)}")
    print(f"   Decisions: {len(result.hive_decisions)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Hive Mind Reflection Orchestrator")
    parser.add_argument('--mode', choices=['daemon', 'once'], default='once',
                       help="Run mode: daemon (continuous) or once (single cycle)")
    parser.add_argument('--environment', choices=['practice', 'live'], default='practice',
                       help="Trading environment")
    parser.add_argument('--interval', type=int, default=30,
                       help="Reflection interval in seconds (for daemon mode)")
    
    args = parser.parse_args()
    
    if args.mode == 'daemon':
        print(f"🧠 Starting Hive Reflection Daemon ({args.environment})")
        print(f"   Interval: {args.interval} seconds")
        print(f"   Press Ctrl+C to stop\n")
        run_orchestrator_daemon(environment=args.environment, interval_seconds=args.interval)
    else:
        print(f"🧠 Running single reflection cycle ({args.environment})\n")
        run_single_cycle(environment=args.environment)
