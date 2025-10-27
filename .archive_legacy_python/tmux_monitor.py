#!/usr/bin/env python3
"""
RBOTzilla UNI - TMUX Monitoring System
Real-time monitoring interface for micro trading canary
PIN: 841921 | Phase 19
"""

import asyncio
import json
import time
import os
import sys
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import threading
import queue
from pathlib import Path

class TMUXMonitor:
    """
    TMUX-based monitoring system for micro trading canary
    Provides real-time updates across 4 monitoring panes
    """
    
    def __init__(self, session_name: str = "rbot_micro_canary"):
        self.session_name = session_name
        self.monitoring_active = False
        self.stats_queue = queue.Queue()
        self.trade_queue = queue.Queue()
        self.system_queue = queue.Queue()
        
        # Monitoring state
        self.current_stats = {}
        self.fx_trades = []
        self.crypto_trades = []
        self.system_metrics = {}
        
        # Configuration
        self.update_interval = 2.0  # 2 second updates
        self.max_trade_history = 20  # Show last 20 trades per pane
        
    def check_tmux_session(self) -> bool:
        """Check if TMUX session exists"""
        try:
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}"],
                capture_output=True, text=True, check=False
            )
            return self.session_name in result.stdout
        except Exception:
            return False
    
    def send_tmux_command(self, pane: str, command: str) -> bool:
        """Send command to specific TMUX pane"""
        try:
            subprocess.run([
                "tmux", "send-keys", "-t", f"{self.session_name}:0.{pane}",
                command, "C-m"
            ], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def clear_pane(self, pane: str) -> bool:
        """Clear specific TMUX pane"""
        try:
            subprocess.run([
                "tmux", "send-keys", "-t", f"{self.session_name}:0.{pane}",
                "clear", "C-m"
            ], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def update_overall_stats_pane(self, stats: Dict[str, Any]) -> None:
        """Update pane 0: Overall Canary Stats"""
        pane = "0"
        self.clear_pane(pane)
        
        # Format overall statistics display
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        stats_display = f"""🐤 MICRO CANARY - OVERALL STATS [{timestamp}]
{'='*50}
Target: {stats.get('total_target', 100)} trades ({stats.get('fx_target', 50)} FX + {stats.get('crypto_target', 50)} Crypto)
Executed: {stats.get('trades_executed', 0)}/{stats.get('total_target', 100)}
FX: {stats.get('fx_trades', 0)}/{stats.get('fx_target', 50)} | Crypto: {stats.get('crypto_trades', 0)}/{stats.get('crypto_target', 50)}

PERFORMANCE METRICS:
Win Rate: {stats.get('win_rate_pct', 0.0):.1f}% (Target: ≥{stats.get('target_win_rate', 65.0)}%)
Total P&L: ${stats.get('total_pnl', 0.0):.2f}
Average P&L: ${stats.get('avg_pnl', 0.0):.2f}
Sharpe Estimate: {stats.get('sharpe_estimate', 0.0):.2f} (Target: ≥{stats.get('target_sharpe', 1.2)})

RISK MONITORING:
Consecutive Losses: {stats.get('consecutive_losses', 0)}/{stats.get('max_consecutive_losses', 3)}
Latency Failures: {stats.get('latency_failures', 0)}/{stats.get('max_latency_failures', 3)}
Elapsed Time: {stats.get('elapsed_time', 0):.0f}s

STATUS: {"🟢 ACTIVE" if stats.get('active', False) else "🔴 STOPPED"}
"""
        
        # Send multiline display to TMUX
        for line in stats_display.strip().split('\n'):
            self.send_tmux_command(pane, f'echo "{line}"')
    
    def update_fx_trade_pane(self, trades: List[Dict[str, Any]]) -> None:
        """Update pane 1: FX Trade Log"""
        pane = "1"
        self.clear_pane(pane)
        
        # Header
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.send_tmux_command(pane, f'echo "📈 FX TRADE LOG (OANDA) [{timestamp}]"')
        self.send_tmux_command(pane, f'echo "{"="*45}"')
        
        # Show recent FX trades
        fx_trades = [t for t in trades if t.get('asset_class') == 'fx'][-self.max_trade_history:]
        
        if fx_trades:
            for trade in fx_trades:
                time_str = datetime.fromisoformat(trade['timestamp'].replace('Z', '+00:00')).strftime("%H:%M:%S")
                result_icon = "✅" if trade['result'] == 'win' else "❌"
                pnl_str = f"${trade['pnl']:+.2f}"
                
                trade_line = f"[{time_str}] {trade['symbol']} {trade['strategy']} {result_icon} {pnl_str}"
                self.send_tmux_command(pane, f'echo "{trade_line}"')
        else:
            self.send_tmux_command(pane, 'echo "No FX trades executed yet..."')
        
        # Summary
        fx_count = len([t for t in trades if t.get('asset_class') == 'fx'])
        fx_wins = len([t for t in trades if t.get('asset_class') == 'fx' and t.get('result') == 'win'])
        fx_pnl = sum(t.get('pnl', 0) for t in trades if t.get('asset_class') == 'fx')
        
        self.send_tmux_command(pane, f'echo ""')
        self.send_tmux_command(pane, f'echo "FX SUMMARY: {fx_count} trades, {fx_wins} wins, ${fx_pnl:.2f} P&L"')
    
    def update_crypto_trade_pane(self, trades: List[Dict[str, Any]]) -> None:
        """Update pane 2: Crypto Trade Log"""
        pane = "2"
        self.clear_pane(pane)
        
        # Header
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.send_tmux_command(pane, f'echo "₿ CRYPTO TRADE LOG (Coinbase) [{timestamp}]"')
        self.send_tmux_command(pane, f'echo "{"="*45}"')
        
        # Show recent crypto trades
        crypto_trades = [t for t in trades if t.get('asset_class') == 'crypto'][-self.max_trade_history:]
        
        if crypto_trades:
            for trade in crypto_trades:
                time_str = datetime.fromisoformat(trade['timestamp'].replace('Z', '+00:00')).strftime("%H:%M:%S")
                result_icon = "✅" if trade['result'] == 'win' else "❌"
                pnl_str = f"${trade['pnl']:+.2f}"
                
                trade_line = f"[{time_str}] {trade['symbol']} {trade['strategy']} {result_icon} {pnl_str}"
                self.send_tmux_command(pane, f'echo "{trade_line}"')
        else:
            self.send_tmux_command(pane, 'echo "No crypto trades executed yet..."')
        
        # Summary
        crypto_count = len([t for t in trades if t.get('asset_class') == 'crypto'])
        crypto_wins = len([t for t in trades if t.get('asset_class') == 'crypto' and t.get('result') == 'win'])
        crypto_pnl = sum(t.get('pnl', 0) for t in trades if t.get('asset_class') == 'crypto')
        
        self.send_tmux_command(pane, f'echo ""')
        self.send_tmux_command(pane, f'echo "CRYPTO SUMMARY: {crypto_count} trades, {crypto_wins} wins, ${crypto_pnl:.2f} P&L"')
    
    def update_runtime_engine_pane(self, system_stats: Dict[str, Any]) -> None:
        """Update pane 3: Runtime Engine"""
        pane = "3"
        self.clear_pane(pane)
        
        # System monitoring
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Get system metrics
        try:
            # CPU load
            with open('/proc/loadavg', 'r') as f:
                load_avg = float(f.read().split()[0])
            cpu_cores = os.cpu_count() or 1
            cpu_load_pct = (load_avg / cpu_cores) * 100
        except:
            cpu_load_pct = 0.0
        
        try:
            # Memory usage
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            mem_total = int([line for line in meminfo.split('\n') if 'MemTotal' in line][0].split()[1])
            mem_available = int([line for line in meminfo.split('\n') if 'MemAvailable' in line][0].split()[1])
            mem_used_pct = ((mem_total - mem_available) / mem_total) * 100
        except:
            mem_used_pct = 0.0
        
        # Network status (simplified)
        network_status = "🟢 CONNECTED"
        try:
            result = subprocess.run(["ping", "-c", "1", "-W", "1", "8.8.8.8"], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode != 0:
                network_status = "🔴 DISCONNECTED"
        except:
            network_status = "🟡 UNKNOWN"
        
        runtime_display = f"""⚙️ RUNTIME ENGINE [{timestamp}]
{'='*40}
SYSTEM RESOURCES:
CPU Load: {cpu_load_pct:.1f}% ({cpu_cores} cores)
Memory: {mem_used_pct:.1f}% used
Network: {network_status}

TRADING ENGINE STATUS:
Engine State: {"🟢 ACTIVE" if system_stats.get('active', False) else "🔴 STOPPED"}
Trades Queue: {system_stats.get('queue_size', 0)} pending
Last Update: {timestamp}
Uptime: {system_stats.get('uptime', 0):.0f}s

SAFETY MONITORS:
Latency Failures: {system_stats.get('latency_failures', 0)}/3
Consecutive Losses: {system_stats.get('consecutive_losses', 0)}/3
CPU Threshold: {cpu_load_pct:.1f}%/80%

PERFORMANCE:
Avg Trade Duration: {system_stats.get('avg_trade_duration', 0):.1f}s
Execution Latency: {system_stats.get('avg_latency', 0):.3f}s
Success Rate: {system_stats.get('execution_success_rate', 0):.1f}%
"""
        
        # Send multiline display to TMUX
        for line in runtime_display.strip().split('\n'):
            self.send_tmux_command(pane, f'echo "{line}"')
    
    async def monitor_loop(self) -> None:
        """Main monitoring loop"""
        print(f"Starting TMUX monitoring for session: {self.session_name}")
        
        if not self.check_tmux_session():
            print(f"Error: TMUX session '{self.session_name}' not found")
            return
        
        self.monitoring_active = True
        trade_history = []
        
        while self.monitoring_active:
            try:
                # Check for updates from queues (non-blocking)
                stats_update = None
                try:
                    stats_update = self.stats_queue.get_nowait()
                except queue.Empty:
                    pass
                
                trade_update = None
                try:
                    trade_update = self.trade_queue.get_nowait()
                except queue.Empty:
                    pass
                
                system_update = None
                try:
                    system_update = self.system_queue.get_nowait()
                except queue.Empty:
                    pass
                
                # Update internal state
                if stats_update:
                    self.current_stats.update(stats_update)
                
                if trade_update:
                    trade_history.append(trade_update)
                    # Keep only recent trades to avoid memory issues
                    if len(trade_history) > 100:
                        trade_history = trade_history[-100:]
                
                if system_update:
                    self.system_metrics.update(system_update)
                
                # Update TMUX panes
                if self.current_stats:
                    self.update_overall_stats_pane(self.current_stats)
                
                self.update_fx_trade_pane(trade_history)
                self.update_crypto_trade_pane(trade_history)
                
                # Combine system stats
                combined_system_stats = {
                    **self.system_metrics,
                    **self.current_stats,
                    'uptime': time.time() - self.system_metrics.get('start_time', time.time())
                }
                self.update_runtime_engine_pane(combined_system_stats)
                
                # Wait for next update
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                print(f"Monitor error: {e}")
                await asyncio.sleep(1.0)
    
    def update_stats(self, stats: Dict[str, Any]) -> None:
        """Update overall statistics"""
        self.stats_queue.put(stats)
    
    def add_trade(self, trade: Dict[str, Any]) -> None:
        """Add new trade to display"""
        self.trade_queue.put(trade)
    
    def update_system_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update system metrics"""
        self.system_queue.put(metrics)
    
    def start_monitoring(self) -> None:
        """Start monitoring in background thread"""
        self.system_metrics['start_time'] = time.time()
        
        def run_monitor():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.monitor_loop())
        
        monitor_thread = threading.Thread(target=run_monitor, daemon=True)
        monitor_thread.start()
        print(f"TMUX monitoring started for session: {self.session_name}")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring"""
        self.monitoring_active = False
        print("TMUX monitoring stopped")

def load_canary_progress(log_dir: str = "logs/micro_canary") -> Dict[str, Any]:
    """Load canary progress from log files"""
    try:
        # Look for most recent canary results
        log_path = Path(log_dir)
        if log_path.exists():
            json_files = list(log_path.glob("canary_results_*.json"))
            if json_files:
                latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
                with open(latest_file, 'r') as f:
                    return json.load(f)
    except Exception as e:
        print(f"Could not load canary progress: {e}")
    
    return {}

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TMUX Monitor for Micro Trading Canary")
    parser.add_argument("--session", "-s", default="rbot_micro_canary", 
                       help="TMUX session name")
    parser.add_argument("--interval", "-i", type=float, default=2.0,
                       help="Update interval in seconds")
    parser.add_argument("--simulate", action="store_true",
                       help="Run with simulated data for testing")
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = TMUXMonitor(args.session)
    monitor.update_interval = args.interval
    
    if args.simulate:
        # Simulate monitoring data for testing
        print("Running in simulation mode...")
        
        monitor.start_monitoring()
        
        # Simulate trading activity
        for i in range(100):
            # Update stats
            stats = {
                'trades_executed': i,
                'fx_trades': i // 2,
                'crypto_trades': i - (i // 2),
                'total_target': 100,
                'fx_target': 50,
                'crypto_target': 50,
                'wins': int(i * 0.65),
                'losses': int(i * 0.35),
                'win_rate_pct': 65.0,
                'total_pnl': i * 1.5,
                'avg_pnl': 1.5,
                'target_win_rate': 65.0,
                'target_sharpe': 1.2,
                'sharpe_estimate': 1.3,
                'consecutive_losses': 1,
                'max_consecutive_losses': 3,
                'latency_failures': 0,
                'max_latency_failures': 3,
                'elapsed_time': i * 2,
                'active': i < 90
            }
            monitor.update_stats(stats)
            
            # Add trade
            if i > 0:
                trade = {
                    'trade_id': f"sim_{i}",
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'asset_class': 'fx' if i % 2 == 0 else 'crypto',
                    'symbol': 'EUR_USD' if i % 2 == 0 else 'BTC-USD',
                    'strategy': 'trend_following',
                    'result': 'win' if (i % 3 != 0) else 'loss',
                    'pnl': 1.5 if (i % 3 != 0) else -0.8
                }
                monitor.add_trade(trade)
            
            # Update system metrics
            system_metrics = {
                'active': i < 90,
                'queue_size': max(0, 10 - i // 10),
                'avg_trade_duration': 15.5,
                'avg_latency': 0.125,
                'execution_success_rate': 98.5,
                'consecutive_losses': min(2, i % 5),
                'latency_failures': 0
            }
            monitor.update_system_metrics(system_metrics)
            
            await asyncio.sleep(0.5)
        
        print("Simulation complete. Monitoring will continue...")
        await asyncio.sleep(30)  # Keep running for 30 more seconds
        
    else:
        # Real monitoring mode
        print(f"Monitoring TMUX session: {args.session}")
        
        if not monitor.check_tmux_session():
            print(f"Error: TMUX session '{args.session}' not found")
            print("Start the micro canary deployment first:")
            print("bash deploy_micro_canary.sh")
            sys.exit(1)
        
        # Load any existing progress
        existing_progress = load_canary_progress()
        if existing_progress:
            print("Loaded existing canary progress")
            monitor.update_stats(existing_progress)
        
        monitor.start_monitoring()
        
        # Keep monitoring running
        print("Monitoring active. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down monitor...")
    
    monitor.stop_monitoring()

if __name__ == "__main__":
    asyncio.run(main())