#!/bin/bash
# RICK System Cleanup - Remove Legacy, Duplicate, and Redundant Files
# Date: October 20, 2025
# PIN: 841921

set -e

WORKSPACE="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
ARCHIVE_DIR="$WORKSPACE/.archive_$(date +%Y%m%d_%H%M%S)"

echo "================================================================"
echo "🧹 RICK SYSTEM CLEANUP - Removing Legacy & Duplicate Files"
echo "================================================================"
echo ""

# Create archive directory for safety
mkdir -p "$ARCHIVE_DIR"
echo "✅ Archive directory created: $ARCHIVE_DIR"
echo ""

# ============================================================================
# PHASE 1: Remove Duplicate position_guardian Nested Directories
# ============================================================================
echo "📁 PHASE 1: Cleaning Duplicate Position Guardian Directories"
echo "----------------------------------------------------------------"

# plugins/position_guardian/position_guardian (NESTED DUPLICATE)
if [ -d "$WORKSPACE/plugins/position_guardian/position_guardian" ]; then
    echo "  🗑️  Removing nested duplicate: plugins/position_guardian/position_guardian/"
    mv "$WORKSPACE/plugins/position_guardian/position_guardian" "$ARCHIVE_DIR/"
    echo "     ✅ Archived to $ARCHIVE_DIR"
fi

# R_H_UNI/plugins/position_guardian/position_guardian (NESTED DUPLICATE)
if [ -d "$WORKSPACE/R_H_UNI/plugins/position_guardian/position_guardian" ]; then
    echo "  🗑️  Removing nested duplicate: R_H_UNI/plugins/position_guardian/position_guardian/"
    mv "$WORKSPACE/R_H_UNI/plugins/position_guardian/position_guardian" "$ARCHIVE_DIR/"
    echo "     ✅ Archived to $ARCHIVE_DIR"
fi

echo ""

# ============================================================================
# PHASE 2: Remove Backup Files
# ============================================================================
echo "📁 PHASE 2: Removing Backup Files"
echo "----------------------------------------------------------------"

# dashboard_unified_backup.py
if [ -f "$WORKSPACE/dashboard_unified_backup.py" ]; then
    echo "  🗑️  Removing: dashboard_unified_backup.py"
    mv "$WORKSPACE/dashboard_unified_backup.py" "$ARCHIVE_DIR/"
    echo "     ✅ Archived"
fi

echo ""

# ============================================================================
# PHASE 3: Consolidate Redundant Documentation (145 .md files!)
# ============================================================================
echo "📁 PHASE 3: Archiving Legacy Documentation (Keep Recent Only)"
echo "----------------------------------------------------------------"

# Create docs archive subfolder
mkdir -p "$ARCHIVE_DIR/legacy_docs"

# Keep essential docs, archive the rest
KEEP_DOCS=(
    "README.md"
    "🚀_AI_BUILDABLE_BLUEPRINT_README.md"
    "SYSTEM_COMPREHENSIVE_ANALYSIS.md"
    "SYSTEM_SIDE_BY_SIDE_COMPARISON.md"
    "SYSTEM_EXECUTIVE_SUMMARY.md"
    "GO_LIVE_PAPER_TRADING_NOW.md"
    "GATED_UPGRADES_MODIFICATIONS_CONFIRMED.md"
    "SESSION_SUMMARY_OCT20.md"
    "QUICK_START.md"
    "DEVELOPER_REFERENCE_MANUAL.md"
)

echo "  📦 Archiving legacy documentation (keeping $(echo ${KEEP_DOCS[@]} | wc -w) essential docs)..."

cd "$WORKSPACE"
for doc in *.md; do
    if [[ ! " ${KEEP_DOCS[@]} " =~ " ${doc} " ]]; then
        mv "$doc" "$ARCHIVE_DIR/legacy_docs/" 2>/dev/null || true
    fi
done

ARCHIVED_COUNT=$(ls -1 "$ARCHIVE_DIR/legacy_docs/" 2>/dev/null | wc -l)
echo "     ✅ Archived $ARCHIVED_COUNT legacy documentation files"
echo ""

# ============================================================================
# PHASE 4: Remove Duplicate .env Files
# ============================================================================
echo "📁 PHASE 4: Cleaning Duplicate Environment Files"
echo "----------------------------------------------------------------"

# Keep env_new.env (working), archive duplicates
if [ -f "$WORKSPACE/.env_temp.txt" ]; then
    echo "  🗑️  Removing: .env_temp.txt"
    mv "$WORKSPACE/.env_temp.txt" "$ARCHIVE_DIR/"
fi

echo "     ✅ env_new.env retained as primary"
echo ""

# ============================================================================
# PHASE 5: Remove Redundant Scripts
# ============================================================================
echo "📁 PHASE 5: Archiving Redundant/Legacy Scripts"
echo "----------------------------------------------------------------"

mkdir -p "$ARCHIVE_DIR/legacy_scripts"

LEGACY_SCRIPTS=(
    "create_dual_packages.sh"
    "deploy_micro_canary_demo.sh"
    "activate_live_trading.sh"
    "launch_battlestation.sh"
    "launch_live_ghost.sh"
    "launch_production.sh"
    "install_reflection_orchestrator.sh"
    "move_bloat_to_onedrive.sh"
    "monitor_backup.sh"
    "monitor_new_backup.sh"
    "phase_42_dashboard_integration.sh"
    "phase_45_socket_live_feeds.sh"
    "phases_46_52_final_battlestation.sh"
    "production_autologin_status.sh"
    "provision_instruments.sh"
    "quick_browser_hive.sh"
    "quick_dashboard_commands.sh"
    "rbuilder_all_phases.sh"
    "setup_browser_hive.sh"
    "setup_production_services.sh"
    "setup_rick_ai.sh"
    "setup_rick_local_llm.sh"
    "setup_rick_walkthrough.sh"
    "start_dashboard_with_rick.sh"
    "start_ghost_trading.sh"
    "test_pin_shutdown.sh"
    "tmux_ghost_monitor.sh"
    "tmux_helper.sh"
    "validate_and_paper_trade.sh"
    "verify_hive_reflection.py"
    "verify_live_safety.sh"
)

for script in "${LEGACY_SCRIPTS[@]}"; do
    if [ -f "$WORKSPACE/$script" ]; then
        mv "$WORKSPACE/$script" "$ARCHIVE_DIR/legacy_scripts/" 2>/dev/null || true
    fi
done

ARCHIVED_SCRIPTS=$(ls -1 "$ARCHIVE_DIR/legacy_scripts/" 2>/dev/null | wc -l)
echo "     ✅ Archived $ARCHIVED_SCRIPTS legacy scripts"
echo ""

# ============================================================================
# PHASE 6: Archive Old Session Documentation
# ============================================================================
echo "📁 PHASE 6: Archiving Old Session Reports"
echo "----------------------------------------------------------------"

mkdir -p "$ARCHIVE_DIR/old_sessions"

cd "$WORKSPACE"
mv SESSION_COMPLETE_OCT4_2025.md "$ARCHIVE_DIR/old_sessions/" 2>/dev/null || true
mv SESSION_COMPLETION_REPORT.md "$ARCHIVE_DIR/old_sessions/" 2>/dev/null || true
mv WALKTHROUGH_COMPLETION_REPORT.md "$ARCHIVE_DIR/old_sessions/" 2>/dev/null || true

echo "     ✅ Old session reports archived"
echo ""

# ============================================================================
# PHASE 7: Clean Up Redundant Python Files
# ============================================================================
echo "📁 PHASE 7: Archiving Redundant Python Modules"
echo "----------------------------------------------------------------"

mkdir -p "$ARCHIVE_DIR/legacy_python"

LEGACY_PYTHON=(
    "canary_to_live.py"
    "position_guardian.py"
    "rick_ai_powered.py"
    "rick_chat_gpt.py"
    "rick_cli.py"
    "rick_enhancement_roadmap.py"
    "rick_live_narrator.py"
    "rick_llm_queries.py"
    "rick_ollama_server.py"
    "sentinel_mode.py"
    "serve_status.py"
    "stochastic.py"
    "test_browser_snap.py"
    "test_dashboard_simple.py"
    "test_guardrails.py"
    "test_ml_intelligence.py"
    "test_wolf_pack.py"
    "tmux_monitor.py"
    "log_graduation.py"
    "live_monitor.py"
    "live_production_manifest.py"
    "hive_mind_processor.py"
)

for pyfile in "${LEGACY_PYTHON[@]}"; do
    if [ -f "$WORKSPACE/$pyfile" ]; then
        mv "$WORKSPACE/$pyfile" "$ARCHIVE_DIR/legacy_python/" 2>/dev/null || true
    fi
done

ARCHIVED_PY=$(ls -1 "$ARCHIVE_DIR/legacy_python/" 2>/dev/null | wc -l)
echo "     ✅ Archived $ARCHIVED_PY legacy Python files"
echo ""

# ============================================================================
# PHASE 8: Clean Logs Directory (Keep Recent Only)
# ============================================================================
echo "📁 PHASE 8: Cleaning Old Logs"
echo "----------------------------------------------------------------"

if [ -d "$WORKSPACE/logs" ]; then
    # Archive logs older than 7 days
    find "$WORKSPACE/logs" -name "*.log" -mtime +7 -exec mv {} "$ARCHIVE_DIR/" \; 2>/dev/null || true
    find "$WORKSPACE/logs" -name "*.jsonl" -mtime +7 -exec mv {} "$ARCHIVE_DIR/" \; 2>/dev/null || true
    
    echo "     ✅ Logs older than 7 days archived"
fi

echo ""

# ============================================================================
# PHASE 9: Remove Empty Directories
# ============================================================================
echo "📁 PHASE 9: Removing Empty Directories"
echo "----------------------------------------------------------------"

find "$WORKSPACE" -type d -empty -delete 2>/dev/null || true
echo "     ✅ Empty directories removed"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================
echo "================================================================"
echo "✅ CLEANUP COMPLETE"
echo "================================================================"
echo ""
echo "📊 Summary:"
echo "  - Duplicate position_guardian dirs removed"
echo "  - Backup files archived"
echo "  - $(echo ${KEEP_DOCS[@]} | wc -w) essential docs retained, $(ls -1 $ARCHIVE_DIR/legacy_docs/ 2>/dev/null | wc -l) archived"
echo "  - $ARCHIVED_SCRIPTS legacy scripts archived"
echo "  - $ARCHIVED_PY legacy Python files archived"
echo "  - Old logs archived (>7 days)"
echo ""
echo "📦 All archived files stored in: $ARCHIVE_DIR"
echo ""
echo "🎯 Essential Files Retained:"
for doc in "${KEEP_DOCS[@]}"; do
    echo "  ✅ $doc"
done
echo ""
echo "🚀 System cleaned and ready!"
echo ""
