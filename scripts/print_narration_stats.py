#!/usr/bin/env python3
"""
Print Narration Stats - Analyze narration.jsonl events (Phase 8)
PIN: 841921
"""
import json
from collections import Counter
from pathlib import Path

def print_stats():
    """Print narration statistics"""
    p = Path("logs/narration.jsonl")
    if not p.exists():
        print("ℹ️  No logs/narration.jsonl yet")
        return
    
    try:
        content = p.read_text()
        if not content.strip():
            print("ℹ️  logs/narration.jsonl is empty")
            return
    except:
        print("❌ Could not read logs/narration.jsonl")
        return
    
    c = Counter()
    on = off = pack_routed = blocked = 0
    
    for ln in content.splitlines():
        if not ln.strip():
            continue
        try:
            j = json.loads(ln)
        except:
            continue
        
        ev = j.get("event")
        if ev:
            c[ev] += 1
            if ev == "HEDGE_ON":
                on += 1
            elif ev == "HEDGE_OFF":
                off += 1
            elif ev == "PACK_ROUTED":
                pack_routed += 1
            elif ev == "TRADE_BLOCKED":
                blocked += 1
    
    print("\n📊 Narration Statistics:")
    print(f"   Total events: {sum(c.values())}")
    print(f"\n   Event counts:")
    for ev, count in sorted(c.items(), key=lambda x: -x[1]):
        print(f"     • {ev}: {count}")
    
    tot = on + off
    if tot > 0:
        rate = 100.0 * on / tot
        print(f"\n   Hedge toggles: {tot}")
        print(f"     • ON: {on} ({rate:.1f}%)")
        print(f"     • OFF: {off}")
    
    print(f"\n   Pack routings: {pack_routed}")
    print(f"   Trade blocks: {blocked}")

if __name__ == "__main__":
    print_stats()
