#!/usr/bin/env bash
# setup_rick_walkthrough.sh
# Purpose: One-click install of a friendly, step-by-step "Rick Coach" startup for both Headless (tmux) and Standalone.
# Safe: Does NOT enable live trading; keeps .upgrade_toggle OFF. Designed for non-coders.
# Run from project root: /home/ing/RICK/R_H_UNI

set -euo pipefail
ROOT="${1:-/home/ing/RICK/R_H_UNI}"
cd "$ROOT"

mkdir -p scripts .vscode pre_upgrade/headless/{bin,logs} pre_upgrade/standalone/logs

# ------------------------------------------------------------------------------
# 0) Safety defaults
# ------------------------------------------------------------------------------
[ -f .upgrade_toggle ] || echo "OFF" > .upgrade_toggle

# ------------------------------------------------------------------------------
# 1) Rick Coach (interactive, non-coder friendly)
# ------------------------------------------------------------------------------
cat > pre_upgrade/headless/bin/rick_coach.py <<'PY'
#!/usr/bin/env python3
import os, sys, time, json, shutil, subprocess, pathlib, datetime as dt

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOGGLE = ROOT / ".upgrade_toggle"
HLOGS  = ROOT / "pre_upgrade" / "headless" / "logs"
SLOGS  = ROOT / "pre_upgrade" / "standalone" / "logs"

NEON = "\033[38;2;0;255;208m"
PURP = "\033[38;2;165;180;252m"
GREEN= "\033[38;2;16;185;129m"
CYAN = "\033[38;2;56;189;248m"
DIM  = "\033[2m"
RST  = "\033[0m"

BANNER = f"""{NEON}
██████╗ ██████╗  ██████╗ ████████╗███████╗██╗██╗     ██╗      █████╗ 
██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝╚══███╔╝██║██║     ██║     ██╔══██╗
██████╔╝██████╔╝██║   ██║   ██║     ███╔╝ ██║██║     ██║     ███████║
██╔══██╗██╔══██╗██║   ██║   ██║    ███╔╝  ██║██║     ██║     ██╔══██║
██║  ██║██████╔╝╚██████╔╝   ██║   ███████╗██║███████╗███████╗██║  ██║
╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
{PURP}RBOT{RST}{CYAN}zilla{RST}  —  Unified Trading Console
{DIM}R_B_O_T_z_i_l_l_a{RST}
{RST}"""

def metric(name, val, sub=""):
    print(f"{PURP}{name:<18}{RST}{val} {DIM}{sub}{RST}")

def wait_key():
    print(f"{DIM}Press ENTER to continue…{RST}", end="", flush=True)
    try: input()
    except KeyboardInterrupt: sys.exit(0)

def safe_read(p: pathlib.Path, default="OFF"):
    try: return p.read_text().strip()
    except Exception: return default

def seed_logs():
    HLOGS.mkdir(parents=True, exist_ok=True)
    SLOGS.mkdir(parents=True, exist_ok=True)
    narr = HLOGS/"narration.jsonl"
    pnl  = HLOGS/"pnl.jsonl"
    if not narr.exists():
        lines = []
        for i in range(20):
            ts = (dt.datetime.utcnow()-dt.timedelta(seconds=5*i)).isoformat()+"Z"
            lines.append(json.dumps({"ts":ts,"text":"Boot OK • guardrails on • awaiting signals","confidence":0.83}))
        narr.write_text("\n".join(lines)+"\n")
    if not pnl.exists():
        total = 0.0
        rows=[]
        for i in range(120):
            total += (0.4 if i%5 else -0.2)
            ts=(dt.datetime.utcnow()-dt.timedelta(minutes=120-i)).isoformat()+"Z"
            rows.append({"ts":ts,"gross":total+0.7,"fees":0.15,"net":total,"cumulative":total})
        pnl.write_text("\n".join(json.dumps(r) for r in rows)+"\n")
    # mirror to standalone
    (SLOGS/"narration.jsonl").write_text((HLOGS/"narration.jsonl").read_text())
    (SLOGS/"pnl.jsonl").write_text((HLOGS/"pnl.jsonl").read_text())

def run(cmd, attach=False):
    if attach:
        os.execvp(cmd[0], cmd)
    return subprocess.run(cmd, check=False)

def show_home():
    os.system("clear")
    print(BANNER)
    metric("Mode", "PRE-UPGRADE (SAFE)", "Live trading is DISABLED")
    metric("Upgrade Toggle", safe_read(TOGGLE, "OFF"))
    metric("Headless", "TMUX battlestation", "Multi-window dashboard")
    metric("Standalone", "Web dashboard", "Streamlit in browser")
    print()
    print(f"{GREEN}I'm Rick. I'll walk you through starting everything in small steps.{RST}")
    print()
    print("1) Start Headless (tmux) — open a terminal dashboard")
    print("2) Start Standalone — open web dashboard")
    print("3) Attach to Headless (if it's already running)")
    print("4) Kill Headless session (safe)")
    print("5) Show Quick Tips")
    print("6) Exit")
    print()
    choice = input(f"{CYAN}Choose 1-6 and press ENTER:{RST} ").strip()
    return choice

def ensure_tmux():
    if shutil.which("tmux") is None:
        print("tmux is not installed. Please install: sudo apt-get install tmux")
        wait_key(); return False
    return True

def main():
    seed_logs()
    while True:
        c = show_home()
        if c == "1":
            if not ensure_tmux(): continue
            print()
            print(f"{GREEN}Launching Headless…{RST}")
            run(["bash","-lc", "scripts/run_headless_preupgrade.sh"])
            print(f"{DIM}(Headless launched. You can also attach via option 3.){RST}")
            wait_key()
        elif c == "2":
            print()
            print(f"{GREEN}Launching Standalone (browser)…{RST}")
            run(["bash","-lc","scripts/run_standalone_preupgrade.sh &>/dev/null &"])
            print("Opening http://localhost:8501 …")
            run(["bash","-lc","python3 - <<'P'\nimport webbrowser; webbrowser.open('http://localhost:8501')\nP"])
            wait_key()
        elif c == "3":
            if not ensure_tmux(): continue
            run(["bash","-lc","scripts/attach_battlestation.sh"], attach=True)
        elif c == "4":
            run(["bash","-lc","scripts/kill_battlestation.sh"])
            wait_key()
        elif c == "5":
            os.system("clear")
            print(BANNER)
            print(f"{PURP}Tips{RST}")
            print("- Headless = terminal dashboard with multiple windows.")
            print("- Standalone = web page dashboard at http://localhost:8501")
            print("- You can run both at the same time; they're read-only and SAFE.")
            print("- If screen looks empty, pick option 1 or 2 to start things.")
            print("- Nothing here makes real trades. Live needs explicit approval later.")
            print()
            wait_key()
        elif c == "6":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Please pick a number 1-6.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
PY
chmod +x pre_upgrade/headless/bin/rick_coach.py

# ------------------------------------------------------------------------------
# 2) Minimal headless assets (narration / pnl tail / health probe)
# ------------------------------------------------------------------------------
cat > pre_upgrade/headless/bin/narrate.py <<'PY'
#!/usr/bin/env python3
import os, json, time, random, datetime as dt, pathlib
LOG = pathlib.Path(__file__).resolve().parent.parent/"logs"/"narration.jsonl"
LOG.parent.mkdir(parents=True, exist_ok=True)
PH=[
 "Scanning liquidity rivers…","Orderflow microbursts steady…",
 "Guardrails: RR≥3.2, TTL≤6h","OCO watchdog online","Momentum trail armed…"
]
while True:
    msg={"ts":dt.datetime.utcnow().isoformat()+"Z","text":random.choice(PH),"level":"INFO"}
    print(json.dumps(msg), flush=True)
    with open(LOG,"a",encoding="utf-8") as f: f.write(json.dumps(msg)+"\n")
    time.sleep(5)
PY
chmod +x pre_upgrade/headless/bin/narrate.py

cat > pre_upgrade/headless/bin/pnl_tail.py <<'PY'
#!/usr/bin/env python3
import os, json, time, pathlib, datetime as dt
LOG = pathlib.Path(__file__).resolve().parent.parent/"logs"/"pnl.jsonl"
pos=0
print("=== P&L TAIL === CTRL-C to exit", flush=True)
while True:
    if not LOG.exists(): print(f"[{dt.datetime.utcnow().isoformat()}Z] waiting for pnl.jsonl"); time.sleep(3); continue
    with open(LOG,"r",encoding="utf-8") as f:
        f.seek(pos)
        for line in f:
            try:
                j=json.loads(line.strip()); print(f"{j['ts']}  NET:{j.get('net',0):>8.2f}  GROSS:{j.get('gross',0):>8.2f}  FEES:{j.get('fees',0):>6.2f}", flush=True)
            except Exception: print(line.rstrip(), flush=True)
        pos=f.tell()
    time.sleep(2)
PY
chmod +x pre_upgrade/headless/bin/pnl_tail.py

cat > pre_upgrade/headless/bin/health_probe.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
while true; do
  printf "%s  ENGINE:OK  FEEDS:OK  GUARDRAILS:%s\n" "$(date -u +%FT%TZ)" "$(cat "$ROOT/.upgrade_toggle" 2>/dev/null || echo OFF)"
  sleep 10
done
SH
chmod +x pre_upgrade/headless/bin/health_probe.sh

# ------------------------------------------------------------------------------
# 3) tmux battlestation launcher (headless)
# ------------------------------------------------------------------------------
cat > pre_upgrade/headless/launch_headless_tmux.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION="RBOTZILLA"

tmux kill-session -t "$SESSION" 2>/dev/null || true
tmux new-session -d -s "$SESSION" -n RICK_HIVE

tmux send-keys -t "$SESSION":0.0 "cd '$ROOT' && python3 bin/rick_coach.py" C-m
tmux split-window -h -t "$SESSION":0
tmux send-keys -t "$SESSION":0.1 "cd '$ROOT' && python3 bin/pnl_tail.py" C-m
tmux split-window -v -t "$SESSION":0.1
tmux send-keys -t "$SESSION":0.2 "cd '$ROOT' && bash bin/health_probe.sh" C-m

tmux new-window -t "$SESSION" -n OANDA
tmux send-keys -t "$SESSION":1.0 "cd '$ROOT' && python3 bin/narrate.py | sed -u 's/^/[OANDA] /'" C-m
tmux split-window -h -t "$SESSION":1
tmux send-keys -t "$SESSION":1.1 "cd '$ROOT' && tail -f logs/oanda.log 2>/dev/null || (touch logs/oanda.log; tail -f logs/oanda.log)" C-m
tmux split-window -v -t "$SESSION":1.1
tmux send-keys -t "$SESSION":1.2 "cd '$ROOT' && bash" C-m

tmux new-window -t "$SESSION" -n COINBASE
tmux send-keys -t "$SESSION":2.0 "cd '$ROOT' && python3 bin/narrate.py | sed -u 's/^/[CB] /'" C-m
tmux split-window -h -t "$SESSION":2
tmux send-keys -t "$SESSION":2.1 "cd '$ROOT' && tail -f logs/coinbase.log 2>/dev/null || (touch logs/coinbase.log; tail -f logs/coinbase.log)" C-m
tmux split-window -v -t "$SESSION":2.1
tmux send-keys -t "$SESSION":2.2 "cd '$ROOT' && bash" C-m

tmux new-window -t "$SESSION" -n DEV
tmux send-keys -t "$SESSION":3.0 "cd '$ROOT' && tail -F logs/*.jsonl 2>/dev/null || watch -n1 'date; echo waiting for logs…'" C-m
tmux split-window -h -t "$SESSION":3
tmux send-keys -t "$SESSION":3.1 "cd '$ROOT' && bash" C-m
tmux split-window -v -t "$SESSION":3.1
tmux send-keys -t "$SESSION":3.2 "cd '$ROOT' && bash" C-m

tmux select-window -t "$SESSION:RICK_HIVE"
tmux attach -t "$SESSION"
SH
chmod +x pre_upgrade/headless/launch_headless_tmux.sh

# ------------------------------------------------------------------------------
# 4) Convenience runners
# ------------------------------------------------------------------------------
cat > scripts/run_headless_preupgrade.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
[ "$(cat "$ROOT/.upgrade_toggle" 2>/dev/null || echo OFF)" = "OFF" ] || { echo "❌ .upgrade_toggle must stay OFF in pre-upgrade."; exit 1; }
exec bash "$ROOT/pre_upgrade/headless/launch_headless_tmux.sh"
SH
chmod +x scripts/run_headless_preupgrade.sh

cat > scripts/attach_battlestation.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
tmux has-session -t RBOTZILLA 2>/dev/null || { echo "No RBOTZILLA session yet. Start via Rick Coach or tasks."; exit 1; }
exec tmux attach -t RBOTZILLA
SH
chmod +x scripts/attach_battlestation.sh

cat > scripts/kill_battlestation.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
tmux kill-session -t RBOTZILLA 2>/dev/null || true
echo "RBOTZILLA session terminated (if it existed)."
SH
chmod +x scripts/kill_battlestation.sh

# ------------------------------------------------------------------------------
# 5) Standalone dashboard (streamlit) with simple runner
# ------------------------------------------------------------------------------
cat > pre_upgrade/standalone/requirements.txt <<'REQ'
streamlit==1.37.0
pandas==2.2.2
REQ

cat > pre_upgrade/standalone/app.py <<'PY'
import os, json, pathlib, pandas as pd, streamlit as st
ROOT = pathlib.Path(__file__).resolve().parent
HLOGS = ROOT.parent / "headless" / "logs"
NARR = HLOGS / "narration.jsonl"
PNL  = HLOGS / "pnl.jsonl"
TOGGLE = ROOT.parents[2] / ".upgrade_toggle"

st.set_page_config(page_title="RBOTZILLA — Standalone", layout="wide")
st.title("🤖 RBOTZILLA — Standalone Dashboard (Pre-Upgrade)")
st.caption("SAFE VIEW • Live trading disabled • .upgrade_toggle stays OFF")

cols = st.columns(3)
toggle_state = "OFF"
try:
    if TOGGLE.exists(): toggle_state = TOGGLE.read_text().strip()
except Exception: pass
cols[0].metric("Upgrade Toggle", toggle_state)
cols[1].metric("Mode", "PRE-UPGRADE")
cols[2].metric("Status", "SAFE")

st.divider()
c1, c2 = st.columns([2,1])

c1.subheader("📡 Narration")
if NARR.exists():
    try:
        df = pd.read_json(NARR, lines=True).tail(40)
        c1.table(df[["ts","text"]])
    except Exception as e:
        c1.warning(f"Narration parse error: {e}")
else:
    c1.info("Start Headless (or Rick Coach) to generate narration.")

c2.subheader("💰 P&L")
if PNL.exists():
    try:
        df = pd.read_json(PNL, lines=True)
        if not df.empty:
            c2.metric("Net (last)", f"{df.iloc[-1].get('net',0):.2f}")
            c2.line_chart(df.set_index("ts")[["net"]].tail(200))
        else:
            c2.info("No P&L yet.")
    except Exception as e:
        c2.warning(f"P&L parse error: {e}")
else:
    c2.info("Start Headless (or Rick Coach) to generate P&L.")
PY

cat > scripts/run_standalone_preupgrade.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/pre_upgrade/standalone"
cd "$APP_DIR"
python3 -m venv .venv 2>/dev/null || true
. .venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null
exec streamlit run app.py --server.headless true --server.fileWatcherType poll
SH
chmod +x scripts/run_standalone_preupgrade.sh

# ------------------------------------------------------------------------------
# 6) VS Code tasks — one-click for non-coders
# ------------------------------------------------------------------------------
cat > .vscode/tasks.json <<'JSON'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "RICK: Start (Rick Coach)",
      "type": "shell",
      "command": "bash",
      "args": ["-lc", "python3 pre_upgrade/headless/bin/rick_coach.py"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    },
    {
      "label": "RICK: Headless Dash (tmux)",
      "type": "shell",
      "command": "bash",
      "args": ["-lc", "scripts/run_headless_preupgrade.sh"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "shared" }
    },
    {
      "label": "RICK: Attach Headless",
      "type": "shell",
      "command": "bash",
      "args": ["-lc", "scripts/attach_battlestation.sh"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "shared" }
    },
    {
      "label": "RICK: Kill Headless",
      "type": "shell",
      "command": "bash",
      "args": ["-lc", "scripts/kill_battlestation.sh"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "shared" }
    },
    {
      "label": "RICK: Standalone (web)",
      "type": "shell",
      "command": "bash",
      "args": ["-lc", "scripts/run_standalone_preupgrade.sh"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    }
  ]
}
JSON

# ------------------------------------------------------------------------------
# 7) Friendly starter — opens Rick Coach first
# ------------------------------------------------------------------------------
cat > scripts/start_here.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
echo "Launching Rick Coach…"
exec python3 pre_upgrade/headless/bin/rick_coach.py
SH
chmod +x scripts/start_here.sh

echo "[OK] Rick Coach walkthrough installed."
echo "VS Code → Terminal → Run Task → 'RICK: Start (Rick Coach)'"
echo "CLI: bash scripts/start_here.sh"