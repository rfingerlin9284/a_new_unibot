#!/usr/bin/env python3
import json, time, sys
from pathlib import Path

# Stream and pretty-print ML/trade-related narration events
# Filters: SIGNAL, TRADE_OPENED, GATE_APPROVED, GATE_REJECTION, PACK_ROUTED,
#          HEDGE_ON, HEDGE_OFF, TRADE_BLOCKED, PROFIT_TAKE, LOSS_HALT, PROTECTION, ERROR, SYSTEM

FILTER_EVENTS = {
    "SIGNAL",
    "TRADE_OPENED",
    "GATE_APPROVED",
    "GATE_REJECTION",
    "PACK_ROUTED",
    "HEDGE_ON",
    "HEDGE_OFF",
    "TRADE_BLOCKED",
    "PROFIT_TAKE",
    "LOSS_HALT",
    "PROTECTION",
    "ERROR",
    "SYSTEM",
}

LOG_PATH = Path("logs/narration.jsonl")

def follow(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with open(path, "r", encoding="utf-8") as f:
        f.seek(0, 2)  # Seek to end
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

def fmt_event(obj: dict) -> str:
    ts = obj.get("ts") or obj.get("timestamp") or ""
    ev = obj.get("event") or obj.get("event_type") or ""
    pack = obj.get("pack") or obj.get("strategy") or ""
    sym = obj.get("symbol") or obj.get("pair") or obj.get("instrument") or ""
    regime = obj.get("regime") or ""
    details = obj.get("details")

    core = f"[{ts}] {ev:14} {sym:10}"
    extra = []
    if pack:
        extra.append(f"pack={pack}")
    if regime:
        extra.append(f"regime={regime}")
    if isinstance(details, dict):
        # show a compact dict subset
        keys = list(details.keys())[:4]
        kv = ", ".join(f"{k}={details[k]}" for k in keys)
        extra.append(kv)
    elif details:
        extra.append(str(details)[:80])
    tail = (" | " + " | ".join(extra)) if extra else ""
    return core + tail


def main():
    print("\n=== ML / Trade Filtered Narration ===")
    print("Showing only key events: " + ", ".join(sorted(FILTER_EVENTS)))
    print("Press Ctrl+C to exit.\n")
    for line in follow(LOG_PATH):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        ev = obj.get("event") or obj.get("event_type")
        if ev in FILTER_EVENTS:
            print(fmt_event(obj))
            sys.stdout.flush()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
