#!/usr/bin/env python3
"""
RICK Unified Dashboard - Master Control Interface
PIN 841921 Approved | Charter Compliant | Read-Only Data Flow

Consolidates: app_futuristic_v2.py, companion.py, and TMUX integration
Purpose: Single entry point for all dashboard operations with progressive enhancement
"""

import streamlit as st
import json
import pathlib
import datetime as dt
import pytz
from typing import Dict, List, Optional

# ========== CONFIGURATION ==========
ROOT = pathlib.Path(__file__).resolve().parent
H_LOGS = ROOT / "pre_upgrade" / "headless" / "logs"
NARR_JL = H_LOGS / "narration.jsonl"
PNL_LOG = H_LOGS / "pnl.jsonl"
ENGINE_LOG = H_LOGS / "engine.log"
UPGRADE_TOGGLE = ROOT / ".upgrade_toggle"

# Charter validation
PIN_REQUIRED = "841921"
CHARTER_RULES = {
    "rr_min": 3.2,
    "daily_breaker": -0.05,
    "max_hold_hours": 6,
    "timeframes": ["M15", "M30", "H1"],
    "min_notional": 15000
}

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="RICK | Unified Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== STYLES ==========
CYBER_CSS = """
<style>
:root {
  --neon: #00ffd0;
  --purple: #a5b4fc;
  --cyan: #38bdf8;
  --bg: #0b1020;
  --soft: #11162a;
  --ink: #e6f7ff;
  --red: #ff006e;
  --green: #00ff41;
}

body, .stApp {
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: 'Arial', ui-monospace, monospace !important;
}

/* Header Styling */
.unified-header {
  background: linear-gradient(90deg, rgba(0,255,208,0.15), rgba(56,189,248,0.12));
  border: 1px solid rgba(0,255,208,0.3);
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  box-shadow: 0 0 20px rgba(0,255,208,0.1);
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  margin: 0 5px;
  border: 1px solid;
}

.status-active {
  background: rgba(0,255,65,0.2);
  border-color: var(--green);
  color: var(--green);
}

.status-ghost {
  background: rgba(0,255,208,0.2);
  border-color: var(--neon);
  color: var(--neon);
}

.status-offline {
  background: rgba(255,0,110,0.2);
  border-color: var(--red);
  color: var(--red);
}

/* Panel Styling */
.panel {
  background: rgba(17,22,42,0.8);
  border: 1px solid rgba(0,255,208,0.2);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 0 15px rgba(0,0,0,0.3);
}

.panel-title {
  color: var(--neon);
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  border-bottom: 1px solid rgba(0,255,208,0.2);
  padding-bottom: 5px;
}

/* Metric Cards */
.metric-card {
  background: linear-gradient(135deg, rgba(0,255,208,0.1), rgba(56,189,248,0.05));
  border: 1px solid rgba(0,255,208,0.25);
  border-radius: 6px;
  padding: 12px;
  text-align: center;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--neon);
}

.metric-label {
  font-size: 11px;
  color: var(--purple);
  text-transform: uppercase;
}

/* Charter Footer */
.charter-footer {
  background: rgba(255,0,110,0.1);
  border: 1px solid var(--red);
  border-radius: 4px;
  padding: 8px 12px;
  margin-top: 20px;
  text-align: center;
  font-size: 11px;
  color: var(--red);
  font-family: monospace;
}
</style>
"""

st.markdown(CYBER_CSS, unsafe_allow_html=True)

# ========== STATE MANAGEMENT ==========
def init_state():
    """Initialize session state with defaults"""
    defaults = {
        "hive_members": {
            "RICK": True,
            "GPT": True,
            "GROK": True,
            "DEEPSEEK": True,
            "GITHUB": True,
            "WOLFPACK": True
        },
        "chat_history": [],
        "timezone_utc": False,
        "pin_verified": False,
        "mode": "GHOST"  # GHOST, CANARY, LIVE
    }
    
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)

init_state()

# ========== UTILITY FUNCTIONS ==========
def read_jsonl(path: pathlib.Path, lines: int = 20) -> List[Dict]:
    """Read last N lines from JSONL file"""
    if not path.exists():
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f.readlines()[-lines:]]
        return data
    except Exception as e:
        st.error(f"Error reading {path.name}: {e}")
        return []

def get_system_status() -> Dict:
    """Check system status from toggle and logs"""
    status = {
        "mode": "GHOST",
        "toggle": "OFF",
        "engine_alive": False,
        "narration_active": False
    }
    
    # Check upgrade toggle
    if UPGRADE_TOGGLE.exists():
        toggle_val = UPGRADE_TOGGLE.read_text().strip().upper()
        status["toggle"] = toggle_val
        if toggle_val == "ON":
            status["mode"] = "LIVE"
    
    # Check engine log freshness
    if ENGINE_LOG.exists():
        mtime = dt.datetime.fromtimestamp(ENGINE_LOG.stat().st_mtime)
        age_seconds = (dt.datetime.now() - mtime).total_seconds()
        status["engine_alive"] = age_seconds < 60  # Fresh if < 1 min old
    
    # Check narration activity
    if NARR_JL.exists():
        mtime = dt.datetime.fromtimestamp(NARR_JL.stat().st_mtime)
        age_seconds = (dt.datetime.now() - mtime).total_seconds()
        status["narration_active"] = age_seconds < 60
    
    return status

def get_charter_compliance() -> Dict:
    """Read charter compliance status"""
    return {
        "rr_enforced": CHARTER_RULES["rr_min"],
        "breaker_threshold": CHARTER_RULES["daily_breaker"],
        "max_hold": CHARTER_RULES["max_hold_hours"],
        "pin_required": PIN_REQUIRED
    }

# ========== HEADER ==========
st.markdown('<div class="unified-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2,3,2])

with col1:
    st.markdown("## 🤖 RICK")
    st.markdown("**Unified Command Center**")

with col2:
    status = get_system_status()
    mode_class = "status-ghost" if status["mode"] == "GHOST" else ("status-active" if status["mode"] == "LIVE" else "status-offline")
    
    st.markdown(f"""
    <div style="text-align:center;">
        <span class="status-badge {mode_class}">MODE: {status["mode"]}</span>
        <span class="status-badge {'status-active' if status['engine_alive'] else 'status-offline'}">
            ENGINE: {'ONLINE' if status['engine_alive'] else 'OFFLINE'}
        </span>
        <span class="status-badge {'status-active' if status['narration_active'] else 'status-offline'}">
            NARRATION: {'ACTIVE' if status['narration_active'] else 'IDLE'}
        </span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Timezone display
    now_utc = dt.datetime.now(dt.timezone.utc)
    if st.session_state.timezone_utc:
        display_time = now_utc.strftime('%H:%M:%S UTC')
    else:
        est = pytz.timezone('America/New_York')
        now_est = now_utc.astimezone(est)
        display_time = now_est.strftime('%H:%M:%S EST')
    
    st.markdown(f"**Time**: `{display_time}`")
    st.markdown(f"**Toggle**: `{status['toggle']}`")

st.markdown('</div>', unsafe_allow_html=True)

# ========== MAIN LAYOUT ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Command Center",
    "💬 Rick Chat",
    "📈 Analytics",
    "⚙️ Settings"
])

# TAB 1: COMMAND CENTER
with tab1:
    col_left, col_right = st.columns([2,1])
    
    with col_left:
        # Live Narration Feed
        st.markdown('<div class="panel"><div class="panel-title">🪖 Rick\'s Workflow (Live)</div>', unsafe_allow_html=True)
        
        narration_data = read_jsonl(NARR_JL, lines=15)
        if narration_data:
            st.markdown('<div style="height:350px;overflow-y:auto;background:rgba(0,0,0,0.3);padding:10px;border-radius:6px;">', unsafe_allow_html=True)
            for entry in narration_data:
                ts = entry.get("ts", "")[:19].replace("T", " ")
                text = entry.get("text", "")
                level = entry.get("level", "INFO")
                component = entry.get("component", "General")
                
                color = "#00ffd0" if level == "INFO" else ("#ff006e" if level == "ERROR" else "#b86bff")
                icon = "🪖" if component == "General" else ("⚙️" if component == "Tech" else "📊")
                
                st.markdown(f'<p style="color:{color};font-size:12px;margin:4px 0;">{icon} <b>{component}</b> [{ts}] — {text}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("⏳ Waiting for Rick's workflow updates...")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # P&L Feed
        st.markdown('<div class="panel"><div class="panel-title">💰 P&L Stream</div>', unsafe_allow_html=True)
        
        pnl_data = read_jsonl(PNL_LOG, lines=10)
        if pnl_data:
            st.markdown('<div style="height:200px;overflow-y:auto;background:rgba(0,0,0,0.3);padding:10px;border-radius:6px;">', unsafe_allow_html=True)
            for entry in pnl_data:
                ts = entry.get("ts", "")[:19].replace("T", " ")
                net = entry.get("net_pnl", 0)
                pair = entry.get("pair", "N/A")
                
                color = "#00ff41" if net > 0 else "#ff006e"
                st.markdown(f'<p style="color:{color};font-size:11px;margin:2px 0;">[{ts}] {pair}: ${net:,.2f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("⏳ No P&L data yet...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # Hive Members Status
        st.markdown('<div class="panel"><div class="panel-title">🐝 Hive Status</div>', unsafe_allow_html=True)
        
        for member, active in st.session_state.hive_members.items():
            status_icon = "🟢" if active else "🔴"
            st.markdown(f"{status_icon} **{member}**: {'ACTIVE' if active else 'IDLE'}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Charter Compliance
        st.markdown('<div class="panel"><div class="panel-title">📜 Charter Compliance</div>', unsafe_allow_html=True)
        
        charter = get_charter_compliance()
        st.markdown(f"**RR Minimum**: ≥{charter['rr_enforced']}")
        st.markdown(f"**Daily Breaker**: {charter['breaker_threshold']*100}%")
        st.markdown(f"**Max Hold**: ≤{charter['max_hold']}h")
        st.markdown(f"**PIN**: `{charter['pin_required']}`")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Metrics
        st.markdown('<div class="panel"><div class="panel-title">📊 Quick Metrics</div>', unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Active Trades</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="metric-card"><div class="metric-value">$0.00</div><div class="metric-label">Today P&L</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: RICK CHAT
with tab2:
    st.markdown('<div class="panel"><div class="panel-title">💬 Conversation with Rick</div>', unsafe_allow_html=True)
    
    # Chat history display (VS Code style - most recent at bottom)
    if st.session_state.chat_history:
        st.markdown('<div style="height:400px;overflow-y:auto;background:rgba(0,0,0,0.3);padding:10px;border-radius:8px;margin-bottom:15px;">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history[-15:]:
            role = msg.get("role", "user")
            text = msg.get("text", "")
            ts = msg.get("ts", "")[:16]
            
            color = "#00ffd0" if role == "rick" else "#b86bff"
            icon = "🤖" if role == "rick" else "👤"
            st.markdown(f'<div style="color:{color};font-size:12px;margin:6px 0;padding:8px;background:rgba(0,0,0,0.2);border-radius:6px;"><b>{icon} {ts}</b><br/><span style="margin-top:4px;display:block;">{text}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💭 No conversation yet. Start chatting with Rick below!")
    
    # Input box at bottom (VS Code style)
    prompt = st.text_area("💬 Message Rick...", height=100, placeholder="e.g., Rick, what's the plan today? Summarize overnight FX news and list 3 vetted setups (RR≥3.2).")
    
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button("📤 Send to Hive"):
            if prompt.strip():
                # Add user message
                user_msg = {
                    "role": "user",
                    "text": prompt.strip(),
                    "ts": dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
                }
                st.session_state.chat_history.append(user_msg)
                
                # Add mock Rick response
                rick_msg = {
                    "role": "rick",
                    "text": "Message received. Analyzing... [Mock response - connect LLM API for real responses]",
                    "ts": dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
                }
                st.session_state.chat_history.append(rick_msg)
                
                st.success("✅ Message sent to Rick!")
                st.rerun()
    
    with col_b:
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_c:
        st.write("")  # Spacer
    
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: ANALYTICS
with tab3:
    st.markdown('<div class="panel"><div class="panel-title">📈 Performance Analytics</div>', unsafe_allow_html=True)
    st.info("📊 Analytics dashboard coming soon - will display equity curves, drawdown, Sharpe ratio, and strategy performance breakdown.")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: SETTINGS
with tab4:
    st.markdown('<div class="panel"><div class="panel-title">⚙️ System Settings</div>', unsafe_allow_html=True)
    
    # Hive Member Toggles
    st.markdown("### 🐝 Hive Members")
    for member in list(st.session_state.hive_members.keys()):
        st.session_state.hive_members[member] = st.checkbox(
            member,
            value=st.session_state.hive_members[member],
            key=f"toggle_{member}"
        )
    
    # Timezone Toggle
    st.markdown("### 🕐 Timezone")
    tz_choice = st.radio("Display Time", ["EST (NYC)", "UTC"], index=0 if not st.session_state.timezone_utc else 1)
    st.session_state.timezone_utc = (tz_choice == "UTC")
    
    # Mode Display (read-only)
    st.markdown("### 🎯 Trading Mode")
    st.info(f"Current Mode: **{st.session_state.mode}** (controlled by `.upgrade_toggle` file)")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown(f"""
<div class="charter-footer">
    ⚠️ CHARTER COMPLIANCE ACTIVE | RR≥{CHARTER_RULES['rr_min']} | Breaker {CHARTER_RULES['daily_breaker']*100}% | PIN {PIN_REQUIRED} | Mode: {st.session_state.mode}
</div>
""", unsafe_allow_html=True)

# Auto-refresh every 5 seconds
st.markdown('<script>setTimeout(function(){window.location.reload();}, 5000);</script>', unsafe_allow_html=True)
