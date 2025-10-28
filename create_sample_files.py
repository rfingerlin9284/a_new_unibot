#!/usr/bin/env python3
"""
Test script for the Critical Files Snapshot Tool

This script creates some sample files to demonstrate the snapshot functionality.
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from common_utils import ensure_directory_exists, write_file_safely

def create_sample_trading_files():
    """Create sample trading bot files for testing the snapshot tool."""
    
    # Create directories
    directories = [
        "src/strategies",
        "src/algorithms", 
        "src/risk_management",
        "src/data",
        "src/monitoring",
        "config",
        "tests/integration",
        "tests/live_trading",
        "docs"
    ]
    
    for directory in directories:
        ensure_directory_exists(directory)
    
    # Create sample files
    sample_files = {
        "src/strategies/momentum_strategy.py": '''
"""Momentum Trading Strategy"""
class MomentumStrategy:
    def __init__(self):
        self.name = "Momentum Strategy"
    
    def execute_trade(self, signal):
        # Critical trading logic here
        pass
''',
        "src/algorithms/trading_algorithm.py": '''
"""Core Trading Algorithm"""
class TradingAlgorithm:
    def __init__(self):
        self.active = True
    
    def process_market_data(self, data):
        # Core algorithm logic
        return {"action": "buy", "quantity": 100}
''',
        "src/risk_management/stop_loss.py": '''
"""Stop Loss Risk Management"""
class StopLossManager:
    def __init__(self, max_loss_pct=0.02):
        self.max_loss_pct = max_loss_pct
    
    def check_stop_loss(self, position, current_price):
        # Risk management logic
        pass
''',
        "config/live_trading.json": json.dumps({
            "api_endpoint": "https://api.exchange.com",
            "trading_pairs": ["BTC/USD", "ETH/USD"],
            "max_position_size": 10000,
            "risk_limits": {"max_daily_loss": 500}
        }, indent=2),
        "config/trading_parameters.json": json.dumps({
            "strategy_params": {
                "momentum_threshold": 0.05,
                "volume_threshold": 1000000
            },
            "risk_params": {
                "stop_loss": 0.02,
                "take_profit": 0.05
            }
        }, indent=2),
        "src/data/market_data_handler.py": '''
"""Market Data Handler"""
class MarketDataHandler:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        # Connect to data feed
        self.connected = True
''',
        "src/monitoring/trading_monitor.py": '''
"""Trading Monitor"""
import logging

class TradingMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_trade(self, trade_data):
        self.logger.info(f"Trade executed: {trade_data}")
''',
        "tests/integration/test_live_trading.py": '''
"""Integration tests for live trading"""
import unittest

class TestLiveTrading(unittest.TestCase):
    def test_trading_strategy(self):
        # Gold standard test
        self.assertTrue(True)
    
    def test_risk_management(self):
        # Critical risk test
        self.assertTrue(True)
''',
        "main_trading.py": '''
"""Main Trading Bot Entry Point"""
from src.strategies.momentum_strategy import MomentumStrategy
from src.risk_management.stop_loss import StopLossManager

def main():
    strategy = MomentumStrategy()
    risk_manager = StopLossManager()
    
    print("Trading bot starting...")
    # Main trading loop would go here

if __name__ == "__main__":
    main()
''',
        "requirements.txt": '''
pandas>=1.3.0
numpy>=1.21.0
requests>=2.25.1
python-dotenv>=0.19.0
ccxt>=1.70.0
''',
        "docs/trading_guide.md": '''
# Trading Bot User Guide

## Overview
This is a critical trading bot for live operations.

## Configuration
1. Set up API keys in config/
2. Configure risk parameters
3. Test with paper trading first

## Critical Operations
- Always monitor risk limits
- Never exceed position sizes
- Maintain proper logging
''',
        ".env": '''
# API Keys (DO NOT COMMIT TO REPO)
EXCHANGE_API_KEY=your_api_key_here
EXCHANGE_SECRET=your_secret_here
TELEGRAM_BOT_TOKEN=your_telegram_token
'''
    }
    
    # Write all sample files
    for file_path, content in sample_files.items():
        write_file_safely(file_path, content)
    
    print("✅ Sample trading bot files created successfully!")
    print(f"📁 Created {len(sample_files)} files across {len(directories)} directories")
    
    # List created files by category
    print("\n📋 Files created:")
    for file_path in sorted(sample_files.keys()):
        print(f"  - {file_path}")

def main():
    """Main function to create sample files and test snapshot."""
    print("🚀 Creating sample trading bot files for testing...")
    create_sample_trading_files()
    
    print("\n🔍 You can now run the snapshot tool:")
    print("   python snapshot_critical_files.py")

if __name__ == "__main__":
    main()