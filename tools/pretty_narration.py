#!/usr/bin/env python3
import argparse
import io
import json
import os
import re
import sys
import time
from collections import deque
import shutil
import textwrap
from datetime import datetime
from pathlib import Path

# Default file: narration.jsonl in workspace root
BASE = Path(__file__).resolve().parent.parent
DEFAULT_FILE = BASE / "narration.jsonl"


def read_tail_lines(path: Path, n: int):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            if n <= 0:
                return []
            dq = deque(maxlen=n)
            for line in f:
                dq.append(line.rstrip("\n"))
            return list(dq)
    except FileNotFoundError:
        return []


FORBIDDEN_RE = re.compile(r"(\{|\}|\[|\]|<[^>]*>|```|Traceback|Error:|Exception|0x[0-9a-fA-F]+)")
NAKED_DIGITS_RE = re.compile(r"(?<![A-Za-z%$#])\b\d{6,}\b")


def summarize_plain(text: str, event_type: str = "") -> str:
    raw = (text or "").strip()
    needs_summary = bool(FORBIDDEN_RE.search(raw) or NAKED_DIGITS_RE.search(raw))

    # Parse common signal format: "Signal: EUR_GBP BUY (78% confidence) - evaluating..."
    m = re.search(r"Signal:\s*([A-Z]{3}[_/][A-Z]{3})\s+(BUY|SELL)\s*\((\d{1,3})%\s*confidence\)", raw, re.I)
    if m:
        pair = m.group(1).replace('_', '/').upper()
        side = m.group(2).upper()
        conf = int(m.group(3))
        if conf >= 85:
            tone = "high confidence"
        elif conf >= 70:
            tone = "good confidence"
        else:
            tone = "early signal"
        return f"Considering a {side} on {pair} with {tone}; reviewing risk before acting."

    et = (event_type or '').upper()
    if et == 'TRADE_OPENED':
        return "Opened a position after checks passed; risk is controlled."
    if et == 'TRADE_CLOSED':
        return "Closed a position to protect capital and follow the plan."
    if 'HEDGE' in et:
        return "Placed a hedge to reduce exposure while conditions are uncertain."
    if et == 'SIGNAL':
        return "A potential trade setup appeared; evaluating it against the rules."

    if not needs_summary and 0 < len(raw) <= 160 and not re.search(r"[\{\}\[\]`]|<[^>]*>|Traceback|Error:|Exception", raw):
        raw = re.sub(r"\b([A-Z]{3})_([A-Z]{3})\b", r"\1/\2", raw)
        return raw

    return "A technical message was received; keeping the display simple and readable."


def _wrap_to_width(s: str, width: int) -> str:
    if width and width >= 20:
        # Keep it to a single line, truncated at word boundary with ellipsis if needed
        return textwrap.shorten(s, width=width, placeholder="…")
    return s


def parse_and_format(line: str, show_time: bool = True, max_width: int | None = None) -> str:
    try:
        obj = json.loads(line)
        ts = obj.get("timestamp") or datetime.utcnow().strftime("%H:%M:%S")
        text = obj.get("narration") or ""
        event_type = obj.get("event_type") or ""
        msg = summarize_plain(text, event_type)
        out = f"{ts} — {msg}" if show_time else msg
        return _wrap_to_width(out, max_width) if max_width else out
    except Exception:
        # Not JSON or malformed: summarize the raw content
        msg = summarize_plain(line, "")
        ts = datetime.utcnow().strftime("%H:%M:%S")
        out = f"{ts} — {msg}" if show_time else msg
        return _wrap_to_width(out, max_width) if max_width else out


def follow_file(path: Path, poll: float, show_time: bool):
    # If file doesn't exist yet, wait until it appears
    while not path.exists():
        time.sleep(poll)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        # Seek to end
        f.seek(0, io.SEEK_END)
        while True:
            where = f.tell()
            line = f.readline()
            if not line:
                time.sleep(poll)
                f.seek(where)
            else:
                sys.stdout.write(parse_and_format(line.rstrip("\n"), show_time) + "\n")
                sys.stdout.flush()


def main():
    p = argparse.ArgumentParser(description="Pretty print narration.jsonl as plain English")
    p.add_argument("--file", default=str(DEFAULT_FILE), help="Path to narration.jsonl")
    p.add_argument("--tail", type=int, default=10, help="Print last N lines first (0 to skip)")
    p.add_argument("--no-time", action="store_true", help="Do not show timestamps")
    p.add_argument("--once", action="store_true", help="Print tail and exit (do not follow)")
    p.add_argument("--max-width", type=int, default=0, help="Max line width; 0=auto detect terminal width; -1=no limit")
    p.add_argument("--poll", type=float, default=0.5, help="Polling interval when following")
    args = p.parse_args()

    path = Path(args.file)
    show_time = not args.no_time

    # Compute desired width
    if args.max_width == 0:
        try:
            term_width = shutil.get_terminal_size((90, 20)).columns
        except Exception:
            term_width = 90
        max_width = term_width
    elif args.max_width < 0:
        max_width = None
    else:
        max_width = args.max_width

    # Tail last N lines
    if args.tail > 0:
        for ln in read_tail_lines(path, args.tail):
            print(parse_and_format(ln, show_time, max_width))

    if args.once:
        return 0

    # Follow new lines
    # Follow new lines
    # When following, we keep the same width policy
    def _follow():
        while not path.exists():
            time.sleep(args.poll)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            f.seek(0, io.SEEK_END)
            while True:
                where = f.tell()
                line = f.readline()
                if not line:
                    time.sleep(args.poll)
                    f.seek(where)
                else:
                    sys.stdout.write(parse_and_format(line.rstrip("\n"), show_time, max_width) + "\n")
                    sys.stdout.flush()
    _follow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
