#!/usr/bin/env python3
"""
Hardened Narration System - Thread-safe JSONL logging with rotation
PIN: 841921 | Profile: Non-HFT | Generated: 2025-10-27
"""
from __future__ import annotations
import atexit, io, json, os, queue, signal, sys, threading, time
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

DEFAULT_LOG_DIR = Path("logs")
DEFAULT_BASENAME = "narration"
DEFAULT_PATH = DEFAULT_LOG_DIR / f"{DEFAULT_BASENAME}.jsonl"
MAX_BYTES = 20 * 1024 * 1024
BACKUP_COUNT = 10
DAILY_ROTATION = True
SAMPLE_ONE_IN_N = 0
CLOCK_DRIFT_WARN_S = 2.5
QUEUE_MAX = 5000
FLUSH_INTERVAL = 0.50

_writer_started=False
_writer_thread=None
_q=queue.Queue(maxsize=QUEUE_MAX)
_stop=threading.Event()
_file_lock=threading.Lock()
_current_path=None
_current_file=None
_current_bytes=0
_current_day=None
_start_mono_ns=time.monotonic_ns()
_last_wall_ns=time.time_ns()
_counters: Dict[Tuple[str,str,str],int]={}

def _ensure_dir(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def _utc_iso(dt=None):
    return (dt or datetime.now(timezone.utc)).isoformat()

def _redact(obj: Dict[str,Any]) -> Dict[str,Any]:
    return obj

def _js(x):
    if is_dataclass(x):
        return asdict(x)
    if isinstance(x, datetime):
        return x.isoformat()
    try:
        json.dumps(x)
        return x
    except:
        return repr(x)

def _event_key(p):
    return (str(p.get("event","")), str(p.get("strategy",p.get("pack",""))), str(p.get("symbol",p.get("pair",""))))

def _should_sample(k):
    global SAMPLE_ONE_IN_N, _counters
    if SAMPLE_ONE_IN_N and SAMPLE_ONE_IN_N>0:
        c=_counters.get(k,0)+1
        _counters[k]=c
        return (c % SAMPLE_ONE_IN_N) != 1
    return False

def _open_new_file(base: Path):
    global _current_file,_current_bytes,_current_day,_current_path
    if _current_file:
        _current_file.flush()
        _current_file.close()
    _ensure_dir(base)
    _current_path=base
    _current_file=open(base,"a",encoding="utf-8",buffering=1)
    try:
        _current_bytes=_current_file.tell()
    except:
        _current_bytes=base.stat().st_size if base.exists() else 0
    _current_day=datetime.now(timezone.utc).strftime("%Y%m%d")

def _do_rotate(base: Path):
    global _current_file,_current_bytes,_current_day
    if _current_file:
        _current_file.flush()
        _current_file.close()
    for idx in range(BACKUP_COUNT,0,-1):
        older=base.with_suffix(base.suffix+f".{idx}")
        if idx==BACKUP_COUNT and older.exists():
            older.unlink(missing_ok=True)
        else:
            newer=base.with_suffix(base.suffix+f".{idx-1}") if idx>1 else base
            if newer.exists():
                newer.rename(older)
    _open_new_file(base)
    _current_bytes=0
    _current_day=datetime.now(timezone.utc).strftime("%Y%m%d")

def _rotate_if_needed(base: Path):
    if _current_file is None:
        _open_new_file(base)
        return
    today=datetime.now(timezone.utc).strftime("%Y%m%d")
    if DAILY_ROTATION and _current_day!=today and _current_bytes>0:
        _do_rotate(base)
        return
    if _current_bytes>=MAX_BYTES:
        _do_rotate(base)

def _safe_write_line(line:str):
    global _current_bytes
    if _current_file is None:
        _open_new_file(DEFAULT_PATH)
    _current_file.write(line)
    _current_bytes+=len(line)

def _writer_loop(path: Path):
    last_flush=time.monotonic()
    while not _stop.is_set():
        try:
            item=_q.get(timeout=FLUSH_INTERVAL)
        except queue.Empty:
            item=None
        if item is not None:
            payload,line=item
            with _file_lock:
                _rotate_if_needed(path)
                _safe_write_line(line)
        now=time.monotonic()
        if (now-last_flush)>=FLUSH_INTERVAL and _current_file:
            try:
                _current_file.flush()
            except:
                pass
            last_flush=now
    while True:
        try:
            payload,line=_q.get_nowait()
        except queue.Empty:
            break
        with _file_lock:
            _rotate_if_needed(path)
            _safe_write_line(line)
    if _current_file:
        try:
            _current_file.flush()
            _current_file.close()
        except:
            pass

def _install_signals():
    def _h(sig,frame):
        stop_listener()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig,_h)
        except:
            pass

def start_listener(log_path:Path=DEFAULT_PATH,*,sample_one_in_n:int=SAMPLE_ONE_IN_N,
                   max_bytes:int=MAX_BYTES,backup_count:int=BACKUP_COUNT,daily_rotation:bool=DAILY_ROTATION)->None:
    global _writer_started,_writer_thread,SAMPLE_ONE_IN_N,MAX_BYTES,BACKUP_COUNT,DAILY_ROTATION
    if _writer_started:
        return
    SAMPLE_ONE_IN_N=sample_one_in_n
    MAX_BYTES=max_bytes
    BACKUP_COUNT=backup_count
    DAILY_ROTATION=daily_rotation
    _install_signals()
    _open_new_file(log_path)
    _writer_thread=threading.Thread(target=_writer_loop,args=(log_path,),name="narration-writer",daemon=True)
    _writer_thread.start()
    _writer_started=True
    atexit.register(stop_listener)

def stop_listener():
    global _writer_started
    if not _writer_started:
        return
    _stop.set()
    if _writer_thread and _writer_thread.is_alive():
        _writer_thread.join(timeout=2.5)

def log_event(event:str,*,strategy=None,pack=None,symbol=None,pair=None,details=None,level:str="INFO",**extra):
    if not _writer_started:
        start_listener()
    wall_ns=time.time_ns()
    mono_ns=time.monotonic_ns()
    wall_iso=_utc_iso()
    global _last_wall_ns, _start_mono_ns
    wall_delta=(wall_ns-_last_wall_ns)/1e9
    mono_delta=(mono_ns-_start_mono_ns)/1e9
    drift=abs(wall_delta-(mono_delta % 1e9))
    _last_wall_ns=wall_ns
    payload={"ts":wall_iso,"ts_mono_ns":mono_ns,"event":event,"level":level,
             "strategy":strategy,"pack":pack,"symbol":symbol or pair,"details":_js(details),
             **{k:_js(v) for k,v in extra.items()}}
    payload=_redact(payload)
    if _should_sample(_event_key(payload)):
        return
    if drift>CLOCK_DRIFT_WARN_S:
        payload.setdefault("warnings",[]).append({"kind":"clock_drift","delta_s":round(drift,3)})
    try:
        line=json.dumps(payload,ensure_ascii=False,separators=(",",":"))+"\n"
    except:
        payload["details"]=repr(details)
        line=json.dumps(payload,ensure_ascii=False,separators=(",",":"))+"\n"
    try:
        _q.put_nowait((payload,line))
    except queue.Full:
        try:
            _q.get_nowait()
        except:
            pass
        try:
            _q.put_nowait((payload,line))
        except:
            pass
