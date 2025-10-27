#!/usr/bin/env python3
"""
live_production_manifest.py - RICK Production Deployment Analyzer
PIN 841921 Approved | Charter Compliant

Analyzes R_H_UNI project to identify:
1. Essential files for live trading bot
2. Legacy/bloat files to exclude
3. Create clean deployment structure
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

PROJECT_ROOT = Path("/home/ing/RICK/R_H_UNI")

# ============================================================================
# ESSENTIAL COMPONENTS FOR LIVE TRADING
# ============================================================================

ESSENTIAL_CORE = {
    "foundation/": "Immutable trading rules and charter enforcement (PIN 841921, RR≥3.2, -5% breaker)",
    "wolf_packs/": "Trading strategy modules with stochastic config loading",
    "risk/": "Risk management (session_breaker, oco_validator, risk_control_center)",
    "brokers/": "OANDA and Coinbase API connectors",
    "execution/": "Trade execution and smart OCO logic",
    "connectors/": "Multi-venue connectors (futures, spot)",
    "swarm/": "Position shepherding swarm bots",
    "logic/": "Core trading logic and decision making",
    "configs/": "Configuration files (thresholds.json, instruments, etc)",
    ".upgrade_toggle": "Safety switch (OFF=UI only, ON=live trading)",
    ".env": "API credentials (OANDA, Coinbase) - MUST have 0600 permissions"
}

ESSENTIAL_ENGINES = {
    "live_ghost_engine.py": "Live ghost trading with real API polling (750ms)",
    "micro_trading_engine.py": "Micro/canary trading engine",
    "ghost_trading_engine.py": "Ghost mode simulation",
    "canary_to_live.py": "Canary→Live graduation logic"
}

ESSENTIAL_UTILITIES = {
    "util/": "Logging, stochastic helpers, utilities",
    "stochastic.py": "Stochastic randomness helpers (random_hex, random_bytes)",
    "log_graduation.py": "Track mode graduations"
}

# ============================================================================
# DASHBOARD/UI COMPONENTS (Optional but recommended)
# ============================================================================

ESSENTIAL_UI = {
    "dashboard_enhanced.py": "Main dashboard entry point (Streamlit)",
    "rick_chat_gpt.py": "Conversational Rick interface",
    "rick_ollama_server.py": "Local LLM server for natural language",
    "dashboard/": {
        "bridge_readonly.py": "Read-only backend data bridge",
        "narrate_plain.py": "Plain-English narration translator",
        "live_activity_feed.py": "Real-time activity feed widget",
        "ws_server.py": "WebSocket server (port 5056)",
        "rest_server.py": "REST API server (port 5000)"
    },
    "pre_upgrade/headless/": {
        "bin/": "Helper scripts (narrate.py, rick_coach.py, pnl_tail.py)",
        "logs/": "JSONL logs (narration.jsonl, keepalive.log, pnl.jsonl)"
    }
}

# ============================================================================
# AI/HIVE MIND (Optional - for browser/local LLM integration)
# ============================================================================

ESSENTIAL_AI = {
    "hive/": {
        "rick_hive_mind.py": "Multi-agent simulation (GPT, GROK, DEEPSEEK)",
        "browser_ai_connector.py": "Browser automation for web AI services",
        "rick_hive_browser.py": "Browser hive mind orchestration"
    },
    "rick_ollama_server.py": "Local conversational LLM"
}

# ============================================================================
# SCRIPTS & AUTOMATION
# ============================================================================

ESSENTIAL_SCRIPTS = {
    "scripts/": {
        "ui_headless/": "TMUX session launchers",
        "system_startup.py": "System initialization"
    },
    "activate_live_trading.sh": "Live trading activation (PIN-gated)",
    "live_preflight_check.sh": "Pre-flight safety checks",
    "verify_live_safety.sh": "Post-activation verification",
    "start_ghost_trading.sh": "Ghost mode launcher"
}

# ============================================================================
# LEGACY/BLOAT TO EXCLUDE
# ============================================================================

EXCLUDE_BLOAT = {
    "ROLLBACK_SNAPSHOTS/": "47GB - Old snapshots",
    "packaged_backups/": "25GB - Packaged backups",
    "R_H_UNI_backups/": "1.7GB - Old backups",
    "archive/": "177MB - Archived code",
    "extracted_legacy/": "173MB - Legacy extracted code",
    "backups/": "21MB - Backup directories",
    "venv/": "499MB - Virtual environment (recreate on target)",
    "mobile_console/": "7MB - Mobile console (not needed for headless)",
    "standalone_shell/": "13MB - Standalone shell (legacy)",
    "pre_upgrade/audit/": "Audit documents (not runtime)",
    "pre_upgrade/pre_upgrade/": "Duplicate pre_upgrade folder",
    "pre_upgrade_backups/": "Backup pre_upgrade files",
    "artifacts/": "112KB - Test artifacts (not production)",
    "snapshots/": "Old snapshots",
    "thefolder/": "Unknown legacy folder",
    "r_h_uni/": "128KB - Duplicate lowercase folder",
    ".git/": "7.7MB - Git repository (use clean clone)",
    ".pytest_cache/": "Test cache",
    "__pycache__/": "Python cache (regenerates)",
    "*.pyc": "Compiled Python (regenerates)",
    "node_modules/": "NPM dependencies (recreate if needed)",
    ".vscode/": "VS Code settings (copy if needed)",
    ".state/": "Temporary state",
    "DASH_SYSTEM_UPGRADE/": "Old dashboard system",
    "R_H_UNI-mirror.git/": "Mirror git repo"
}

EXCLUDE_FILES = {
    "test_*.py": "Test files (not production)",
    "validate_*.py": "Validation scripts (not production)",
    "*_test.py": "Test files",
    "*.md": "Documentation (optional - keep key docs)",
    "*.txt": "Text docs (optional)",
    "phase*.txt": "Phase descriptions",
    "dash_debug": "Debug files",
    "*.log": "Old log files (will regenerate)"
}

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_directory_sizes():
    """Analyze directory sizes to identify bloat."""
    print("📊 Analyzing directory sizes...")
    print("=" * 80)
    
    bloat_total = 0
    essential_total = 0
    
    for path, description in EXCLUDE_BLOAT.items():
        full_path = PROJECT_ROOT / path.rstrip("/")
        if full_path.exists():
            size = get_dir_size(full_path)
            bloat_total += size
            print(f"❌ {path:40s} {format_size(size):>10s} - {description}")
    
    print()
    print(f"Total bloat: {format_size(bloat_total)}")
    print()
    
    return bloat_total, essential_total

def get_dir_size(path: Path) -> int:
    """Get directory size in bytes."""
    total = 0
    try:
        for item in path.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
    except:
        pass
    return total

def format_size(bytes: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.1f}TB"

def generate_manifest():
    """Generate deployment manifest."""
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "project_root": str(PROJECT_ROOT),
        "essential_core": ESSENTIAL_CORE,
        "essential_engines": ESSENTIAL_ENGINES,
        "essential_ui": ESSENTIAL_UI,
        "essential_ai": ESSENTIAL_AI,
        "essential_scripts": ESSENTIAL_SCRIPTS,
        "exclude_bloat": EXCLUDE_BLOAT,
        "exclude_files": EXCLUDE_FILES
    }
    
    manifest_file = PROJECT_ROOT / "LIVE_PRODUCTION_MANIFEST.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Manifest saved: {manifest_file}")
    return manifest

def print_essential_structure():
    """Print essential directory structure."""
    print("\n🎯 ESSENTIAL LIVE PRODUCTION STRUCTURE")
    print("=" * 80)
    
    print("\n📁 CORE TRADING MODULES (Required):")
    for path, desc in ESSENTIAL_CORE.items():
        print(f"   ├── {path:40s} # {desc}")
    
    print("\n🚀 TRADING ENGINES (Required):")
    for file, desc in ESSENTIAL_ENGINES.items():
        print(f"   ├── {file:40s} # {desc}")
    
    print("\n🛠️ UTILITIES (Required):")
    for path, desc in ESSENTIAL_UTILITIES.items():
        print(f"   ├── {path:40s} # {desc}")
    
    print("\n🖥️ DASHBOARD/UI (Optional but recommended):")
    print(f"   ├── dashboard_enhanced.py                    # Main UI")
    print(f"   ├── rick_chat_gpt.py                         # Chat interface")
    print(f"   ├── dashboard/                               # UI components")
    print(f"   └── pre_upgrade/headless/                    # Logs & helpers")
    
    print("\n🧠 AI/HIVE MIND (Optional):")
    print(f"   ├── hive/                                    # Multi-agent AI")
    print(f"   └── rick_ollama_server.py                    # Local LLM")
    
    print("\n📜 SCRIPTS (Required):")
    print(f"   ├── activate_live_trading.sh                 # PIN-gated activation")
    print(f"   ├── live_preflight_check.sh                  # Safety checks")
    print(f"   └── scripts/ui_headless/                     # TMUX launchers")

def estimate_sizes():
    """Estimate sizes of essential vs bloat."""
    print("\n💾 STORAGE ANALYSIS")
    print("=" * 80)
    
    bloat_size, _ = analyze_directory_sizes()
    
    print("\n✅ ESSENTIAL COMPONENTS (estimated):")
    essential_paths = [
        "foundation/", "wolf_packs/", "risk/", "brokers/", 
        "execution/", "connectors/", "swarm/", "logic/", 
        "configs/", "util/", "dashboard/", "hive/"
    ]
    
    essential_total = 0
    for path in essential_paths:
        full_path = PROJECT_ROOT / path
        if full_path.exists():
            size = get_dir_size(full_path)
            essential_total += size
            print(f"   ✓ {path:40s} {format_size(size):>10s}")
    
    # Add root-level essentials
    root_essentials = [
        "live_ghost_engine.py", "micro_trading_engine.py",
        "ghost_trading_engine.py", "canary_to_live.py",
        "dashboard_enhanced.py", "rick_chat_gpt.py",
        "rick_ollama_server.py", "stochastic.py"
    ]
    
    for file in root_essentials:
        full_path = PROJECT_ROOT / file
        if full_path.exists():
            size = full_path.stat().st_size
            essential_total += size
    
    print(f"\n   Total Essential: {format_size(essential_total)}")
    print(f"   Total Bloat:     {format_size(bloat_size)}")
    print(f"   Reduction:       {(bloat_size / (bloat_size + essential_total) * 100):.1f}% smaller")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  🎯 RICK LIVE PRODUCTION MANIFEST GENERATOR                 ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    
    # Analysis
    print_essential_structure()
    estimate_sizes()
    
    # Generate manifest
    print()
    manifest = generate_manifest()
    
    print()
    print("=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print()
    print("NEXT STEPS:")
    print("1. Review LIVE_PRODUCTION_MANIFEST.json")
    print("2. Run: ./create_live_deployment.sh (will create clean package)")
    print("3. Test in isolated environment")
    print("4. Deploy to production server")
