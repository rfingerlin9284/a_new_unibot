from __future__ import annotations
import argparse, time, traceback, json, os, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(__file__))
from brokers.oanda_adapter import OandaClient
from position_guardian.rules import tl_dr_actions

LOGDIR=os.path.join(os.path.expanduser("~"),"RICK","R_H_UNI","logs")
os.makedirs(LOGDIR, exist_ok=True)
LOGF=os.path.join(LOGDIR,"guardian.log")

def log(msg):
    ts=datetime.now(timezone.utc).isoformat()
    line=f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOGF,"a") as f: f.write(line+"\n")
    except Exception: pass

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--loop", type=int, default=30, help="seconds between passes")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--live", action="store_true", help="apply changes (else dry-run)")
    args=ap.parse_args()
    client=OandaClient()
    def pass_once():
        try:
            positions, acct, meta = client.snapshot_positions_and_account()
            acts=tl_dr_actions(positions, acct, acct.now_utc)
            if not acts:
                log("no-actions")
                return
            for a in acts:
                if a["type"]=="modify_sl":
                    if args.live:
                        client.set_stop_loss(a["position_id"], a["new_sl"])
                        log(json.dumps({"applied":"modify_sl", **a}))
                    else: log(json.dumps({"dry_run":"modify_sl", **a}))
                elif a["type"]=="close":
                    if args.live:
                        client.close_trade_all(a["position_id"])
                        log(json.dumps({"applied":"close", **a}))
                    else: log(json.dumps({"dry_run":"close", **a}))
                elif a["type"]=="advice":
                    log(json.dumps({"advice":a}))
        except Exception as e:
            log("error:"+repr(e))
            tb="".join(traceback.format_exc())
            log(tb)
    pass_once()
    if args.once: return
    while True:
        time.sleep(args.loop)
        pass_once()

if __name__=="__main__":
    main()
