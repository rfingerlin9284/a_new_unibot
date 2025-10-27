---
description: Repository Information Overview
alwaysApply: true
---

# RICK Trading System Information

## Summary
RICK_LIVE_PROTOTYPE is an algorithmic trading system focused on forex trading through the OANDA API. It implements a charter-compliant trading engine with risk management, position tracking, and autonomous decision-making capabilities. The system includes multiple components such as trading engines, dashboard interfaces, and position management tools.

## Structure
- **brokers/**: Connector modules for different trading platforms (OANDA, Coinbase, IB)
- **configs/**: Configuration files for trading pairs, thresholds, and venues
- **foundation/**: Core components including charter compliance and risk management
- **hive/**: Autonomous position management and decision orchestration
- **logs/**: Trading logs, alerts, and system state tracking
- **plugins/**: Modular extensions including position guardian
- **strategies/**: Trading strategies (bearish_wolf, bullish_wolf, sideways_wolf)
- **util/**: Utility modules for logging, display, and system monitoring
- **systemd/**: Service definitions for autonomous components

## Language & Runtime
**Language**: Python
**Version**: 3.12.3
**Build System**: Makefile
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- requests
- python-dotenv
- numpy
- pandas
- scikit-learn
- oanda-v20
- jsonschema
- pydantic
- streamlit (for dashboard)

**Development Dependencies**:
- pytest

## Build & Installation
```bash
# Setup environment and dependencies
make setup

# Install dependencies only
make deps

# Clean build artifacts
make clean
```

## Main Entry Points
- **oanda_trading_engine.py**: Primary trading engine for OANDA
- **autonomous_decision_engine.py**: Autonomous decision-making system
- **dashboard_unified.py**: Monitoring dashboard interface
- **canary_oanda_connector.py**: Connector for OANDA API

## Testing
**Framework**: pytest
**Test Files**: 
- test_margin_correlation_gate.py
- test_live_brokers.py
**Run Command**:
```bash
make test
```

## Execution
**Practice Mode**:
```bash
make run
```

**Live Trading**:
```bash
make run-live
```

**Dashboard**:
```bash
make run-dashboard
```

## Risk Management
The system implements strict risk management with:
- Minimum risk-reward ratio of 3.2:1
- Maximum daily loss limit of 5%
- Margin cap at 35%
- Minimum stop-loss of 18 pips
- Position sizing to meet $15,000 minimum notional value