#!/usr/bin/env python3
"""
Validate Narration JSONL - Check file integrity (Phase 8)
PIN: 841921
"""
import json
import sys
from pathlib import Path

def validate_narration(filepath=None):
    """
    Validate narration.jsonl file.
    
    Args:
        filepath: Path to narration file (default: logs/narration.jsonl)
        
    Returns:
        bool: True if valid, False if errors found
    """
    if filepath is None:
        filepath = "logs/narration.jsonl"
    
    path = Path(filepath)
    if not path.exists():
        print(f"[validate] missing: {path}")
        return True  # Not an error if file doesn't exist yet
    
    bad = 0
    total = 0
    
    try:
        content = path.read_text()
    except Exception as e:
        print(f"[validate] could not read file: {e}")
        return False
    
    for i, ln in enumerate(content.splitlines(), 1):
        s = ln.strip()
        if not s:
            continue
        
        total += 1
        try:
            obj = json.loads(s)
        except Exception as e:
            print(f"[validate] line {i}: invalid json: {e}")
            bad += 1
            continue
        
        # Check required fields
        for k in ("event", "ts"):
            if k not in obj:
                print(f"[validate] line {i}: missing key '{k}'")
                bad += 1
                break
    
    if bad == 0:
        print(f"[validate] ✅ OK ({total} lines)")
        return True
    else:
        print(f"[validate] ❌ FAIL ({bad} bad lines / {total} total)")
        return False

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    success = validate_narration(filepath)
    sys.exit(0 if success else 1)
