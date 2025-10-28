#!/usr/bin/env python3
"""
Plain-English viewer for Strategy Aggregator availability.

Usage:
    python3 tools/strategy_status.py            # one-shot
    python3 tools/strategy_status.py --watch    # auto-refresh every 2s
    python3 tools/strategy_status.py --watch --verbose  # includes grouped agents if available
"""
import sys
import time
import shutil
from typing import List
from pathlib import Path
import json
from datetime import datetime, timezone

# Ensure repo root is on sys.path so `util` can be imported when run from anywhere
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from util.strategy_aggregator import StrategyAggregator
except Exception as e:
    print("⚠️  Could not import StrategyAggregator:", e)
    sys.exit(1)


def pretty_list_status() -> List[str]:
    agg = StrategyAggregator()
    lines = []
    lines.append("Strategy Aggregator status")
    lines.append("-" * 30)
    lines.append(f"Available strategies: {agg.strategies_available}/5")
    order = [
        ("trap_reversal", "Trap Reversal"),
        ("fib_confluence", "Fibonacci Confluence"),
        ("price_action_holy_grail", "Price Action (Holy Grail)"),
        ("liquidity_sweep", "Liquidity Sweep"),
        ("ema_scalper", "EMA Scalper"),
    ]
    for key, label in order:
        ok = agg.strategies.get(key, {}).get('available', False)
        check = "✓" if ok else "✗"
        note = "ready" if ok else "not installed"
        lines.append(f"  {check} {label}: {note}")
    return lines


def clear_screen():
    try:
        # ANSI clear
        print("\033[2J\033[H", end="")
    except Exception:
        pass


def print_header():
    cols = shutil.get_terminal_size((80, 20)).columns
    inner = max(10, cols - 2)
    title = "  🧩 Strategy Aggregator — Plain-English Status"
    print("\033[95m\033[1m", end="")  # bright magenta bold
    print("╔" + "═" * inner + "╗")
    print("║" + title[:inner].ljust(inner) + "║")
    print("╚" + "═" * inner + "╝")
    print("\033[0m")  # reset


def oneshot(verbose: bool = False):
    # Show Hive consensus first (if available), then agents (if verbose), then strategies
    _print_consensus_line()
    if verbose:
        _print_agents_section()
    for line in pretty_list_status():
        print(line)


def watch_loop(interval: float = 2.0, verbose: bool = False):
    try:
        while True:
            clear_screen()
            print_header()
            _print_consensus_line()
            if verbose:
                _print_agents_section()
            for line in pretty_list_status():
                # Colorize checkmarks lightly
                if line.strip().startswith("✓"):
                    print("\033[92m" + line + "\033[0m")  # green
                elif line.strip().startswith("✗"):
                    print("\033[91m" + line + "\033[0m")  # red
                else:
                    print(line)
            print("\nPress Ctrl+C to exit. Refreshing every %.1fs..." % interval)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[status] watch stopped")


# --- Hive consensus helpers ---
CONS_FILE = ROOT / "config" / "hive_consensus.json"
AGENTS_FILE = ROOT / "config" / "agents.json"


def _read_consensus() -> tuple:
    try:
        if not CONS_FILE.exists():
            return float('nan'), None
        data = json.loads(CONS_FILE.read_text())
        return float(data.get("consensus")), data.get("timestamp")
    except Exception:
        return float('nan'), None


def _load_agents_manifest():
    """
    Load agents manifest. Returns a tuple (groups, flat_list).
    - groups: dict[str, list[str]] if present, else {}
    - flat_list: list[str] of agents (fallback and for totals)
    """
    groups = {}
    flat = []
    try:
        if AGENTS_FILE.exists():
            data = json.loads(AGENTS_FILE.read_text())
            # Preserve dict insertion order (Python 3.7+)
            g = data.get("groups")
            if isinstance(g, dict) and g:
                groups = {str(k): [str(vv) for vv in v] for k, v in g.items() if isinstance(v, list)}
            a = data.get("agents")
            if isinstance(a, list) and a:
                flat = [str(x) for x in a]
    except Exception:
        pass
    if not flat:
        flat = [
            "Smart Logic",
            "Momentum Analyzer",
            "Strategy Aggregator",
            "Dynamic Leverage",
            "Position Sizing",
            "Risk Manager",
            "Guardian Gate",
            "OCO Manager",
            "Trailing Swarm Shepherd",
            "Pricing Cache",
            "Hive Mind",
            "Narration Writer",
        ]
    return groups, flat


def _print_consensus_line():
    val, ts = _read_consensus()
    if not (val == val):  # NaN check
        print("Hive consensus: unavailable (waiting for updater)")
        print()
        return
    pct = f"{val*100:.2f}%"
    # Format timestamp and staleness
    ts_note = "timestamp unavailable"
    freshness = ""
    if ts:
        try:
            ts_norm = ts.replace("Z", "+00:00")
            dt = datetime.fromisoformat(ts_norm)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            age = (now - dt).total_seconds()
            if age < 0:
                age = 0  # guard for clock skew
            if age < 60:
                freshness = "\033[92mFRESH\033[0m"
            elif age < 300:
                freshness = "\033[93mSTALE %dm ago\033[0m" % int(age // 60)
            else:
                freshness = "\033[91mSTALE %dm ago\033[0m" % int(age // 60)
            ts_note = f"updated {ts} ({freshness})"
        except Exception:
            ts_note = f"updated {ts}"
    base = f"🐝 Hive Consensus: {pct} ({ts_note}) — forwarding to RBOTzilla"
    print("\033[96m" + base + "\033[0m\n")


def _print_agents_section():
    """Render agents, grouped if groups exist; otherwise flat list on one line."""
    groups, flat = _load_agents_manifest()
    if groups:
        total = sum(len(v) for v in groups.values())
        print(f"Agents grouped ({total}):")
        for group_name, items in groups.items():
            print(f"  • {group_name} ({len(items)}):")
            # Render as comma-separated within group
            if items:
                print("    - " + ", ".join(items))
        print()
    else:
        print(f"Agents ({len(flat)}): " + ", ".join(flat))
        print()


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    if "--watch" in sys.argv:
        watch_loop(verbose=verbose)
    else:
        oneshot(verbose=verbose)
