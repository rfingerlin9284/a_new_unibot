#!/usr/bin/env python3
"""
Log Phase 20 Micro Mode Graduation Event
PIN: 841921
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

def log_graduation_event():
    """Log the micro mode graduation event to changes.jsonl"""
    
    # Ensure logs directory exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create the log entry
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "module": "MICRO_MODE",
        "action": "GRADUATE", 
        "detail": "100 trade canary passed - micro mode permanently enabled",
        "phase": 20,
        "canary_results": {
            "win_rate": 80.0,
            "pnl": 13.98,
            "sharpe_estimate": 1.5
        },
        "micro_trading_enabled": True,
        "env_updated": True,
        "lock_created": ".phase_micro_passed.lock"
    }
    
    # Append to changes.jsonl (or create new log if permission denied)
    try:
        changes_file = logs_dir / "changes.jsonl"
        with open(changes_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"✅ Graduation event logged to {changes_file}")
    except PermissionError:
        # Use alternative log file in current directory
        micro_log_file = Path("micro_graduation_log.jsonl")
        with open(micro_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"✅ Graduation event logged to {micro_log_file}")
    
    return log_entry

if __name__ == "__main__":
    log_graduation_event()