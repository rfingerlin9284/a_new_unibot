#!/bin/bash
# create_live_deployment.sh - Create Clean RICK Production Deployment Package
# PIN 841921 Approved | Charter Compliant

set -e

PROJECT_ROOT="/home/ing/RICK/R_H_UNI"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_DIR="${PROJECT_ROOT}/../RICK_LIVE_${TIMESTAMP}"
MANIFEST="${PROJECT_ROOT}/LIVE_PRODUCTION_MANIFEST.json"

cd "$PROJECT_ROOT" || exit 1

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  📦 RICK LIVE PRODUCTION DEPLOYMENT PACKAGER               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# VERIFY MANIFEST EXISTS
# ============================================================================

if [ ! -f "$MANIFEST" ]; then
    echo "❌ Manifest not found. Running generator..."
    python3 live_production_manifest.py
fi

echo "📋 Using manifest: $MANIFEST"
echo "📁 Creating deployment: $DEPLOY_DIR"
echo ""

# ============================================================================
# CREATE DEPLOYMENT DIRECTORY
# ============================================================================

echo "🏗️  Creating deployment structure..."

mkdir -p "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"/{foundation,wolf_packs,risk,brokers,execution,connectors,swarm,logic,configs,util,hive,dashboard,scripts,pre_upgrade/headless}

echo "✅ Directory structure created"
echo ""

# ============================================================================
# COPY ESSENTIAL CORE MODULES
# ============================================================================

echo "📦 Copying essential core modules..."

# Core directories
for dir in foundation wolf_packs risk brokers execution connectors swarm logic configs util hive; do
    if [ -d "$dir" ]; then
        echo "   Copying $dir/"
        cp -r "$dir" "$DEPLOY_DIR/" 2>/dev/null || true
    fi
done

# Dashboard components
echo "   Copying dashboard/"
cp -r dashboard "$DEPLOY_DIR/" 2>/dev/null || true

# Pre-upgrade essentials (logs and bin)
echo "   Copying pre_upgrade/headless/ (logs & bin)"
mkdir -p "$DEPLOY_DIR/pre_upgrade/headless"
cp -r pre_upgrade/headless/bin "$DEPLOY_DIR/pre_upgrade/headless/" 2>/dev/null || true
cp -r pre_upgrade/headless/logs "$DEPLOY_DIR/pre_upgrade/headless/" 2>/dev/null || true

# Scripts
echo "   Copying scripts/"
cp -r scripts "$DEPLOY_DIR/" 2>/dev/null || true

echo "✅ Core modules copied"
echo ""

# ============================================================================
# COPY ESSENTIAL ROOT FILES
# ============================================================================

echo "📄 Copying essential root files..."

# Trading engines
for file in \
    live_ghost_engine.py \
    micro_trading_engine.py \
    ghost_trading_engine.py \
    canary_to_live.py \
    log_graduation.py \
    stochastic.py
do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
        cp "$file" "$DEPLOY_DIR/"
    fi
done

# Dashboard/UI
for file in \
    dashboard_enhanced.py \
    dashboard_unified.py \
    rick_chat_gpt.py \
    rick_ai_powered.py \
    rick_ollama_server.py \
    hive_mind_processor.py \
    rick_live_narrator.py
do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
        cp "$file" "$DEPLOY_DIR/"
    fi
done

# Scripts
for file in \
    activate_live_trading.sh \
    live_preflight_check.sh \
    verify_live_safety.sh \
    start_ghost_trading.sh \
    launch_live_ghost.sh \
    setup_rick_local_llm.sh \
    quick_browser_hive.sh
do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
        cp "$file" "$DEPLOY_DIR/"
        chmod +x "$DEPLOY_DIR/$file"
    fi
done

# Configuration and safety files
echo "   ✓ .upgrade_toggle"
cp .upgrade_toggle "$DEPLOY_DIR/" 2>/dev/null || echo "OFF" > "$DEPLOY_DIR/.upgrade_toggle"

echo "   ✓ requirements.txt"
cp requirements.txt "$DEPLOY_DIR/" 2>/dev/null || true

echo "   ✓ README.md"
cp README.md "$DEPLOY_DIR/" 2>/dev/null || true

# Create .env template (DO NOT copy actual .env with credentials)
if [ -f ".env" ]; then
    echo "   ⚠️  Creating .env.template (review and populate on deployment)"
    cat > "$DEPLOY_DIR/.env.template" << 'EOF'
# OANDA Live Trading API
OANDA_ACCOUNT_ID=your_account_id_here
OANDA_TOKEN=your_api_token_here

# Coinbase Advanced Trade API
COINBASE_API_KEY_ID=your_key_id_here
COINBASE_API_KEY_SECRET=your_secret_here
COINBASE_API_ALGO=ES256

# OpenAI (optional - for rick_ai_powered.py)
# OPENAI_API_KEY=sk-...

# IMPORTANT: Set permissions after populating
# chmod 0600 .env
EOF
else
    echo "   ⚠️  No .env found - create .env.template"
fi

echo "✅ Root files copied"
echo ""

# ============================================================================
# CLEAN UP UNNECESSARY FILES IN DEPLOYMENT
# ============================================================================

echo "🧹 Cleaning deployment package..."

cd "$DEPLOY_DIR" || exit 1

# Remove test files
find . -type f -name "test_*.py" -delete 2>/dev/null || true
find . -type f -name "*_test.py" -delete 2>/dev/null || true
find . -type f -name "validate_*.py" -delete 2>/dev/null || true

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Remove node_modules if present
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

# Remove .git if copied
rm -rf .git .gitignore 2>/dev/null || true

# Remove backup/audit files
rm -rf pre_upgrade/audit 2>/dev/null || true

echo "✅ Cleanup complete"
echo ""

cd "$PROJECT_ROOT"

# ============================================================================
# CREATE DEPLOYMENT README
# ============================================================================

echo "📝 Creating deployment README..."

cat > "$DEPLOY_DIR/DEPLOYMENT_README.md" << 'EOF'
# RICK Live Production Deployment

## 🎯 Package Contents

This is a **minimal, production-ready** RICK trading system deployment containing ONLY essential files for live trading operations.

**Size**: ~3-5 MB (vs 98GB+ source project with bloat)

## ⚠️ PRE-DEPLOYMENT CHECKLIST

### 1. Environment Setup
```bash
# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Credentials
```bash
# Copy template and edit
cp .env.template .env
nano .env

# Add your credentials:
# - OANDA_ACCOUNT_ID and OANDA_TOKEN
# - COINBASE_API_KEY_ID and COINBASE_API_KEY_SECRET

# CRITICAL: Set secure permissions
chmod 0600 .env
```

### 3. Verify Safety Switch
```bash
# MUST be OFF for initial testing
cat .upgrade_toggle
# Should show: OFF
```

### 4. Test Ghost Mode (Simulation)
```bash
# Start ghost trading (uses real API data, NO actual trades)
./start_ghost_trading.sh

# Monitor logs
tail -f pre_upgrade/headless/logs/narration.jsonl
```

### 5. Run Pre-Flight Checks
```bash
# Verify all safety systems
./live_preflight_check.sh

# Expected: All checks PASS
```

## 🚀 ACTIVATION SEQUENCE (PIN 841921 Required)

### Ghost Mode (Safe Testing)
```bash
./start_ghost_trading.sh
# Duration: 45-90 minutes
# Validates: Signals, P&L tracking, risk management
```

### Canary Mode (Minimal Risk)
```bash
# After successful ghost run
./micro_trading_engine.py
# Risk: 0.1% per trade, 1 concurrent position
```

### Live Mode (Full Production)
```bash
# PIN 841921 required
./activate_live_trading.sh
# Enter PIN: 841921

# Verify safety
./verify_live_safety.sh
```

## 🛑 EMERGENCY STOP

```bash
# IMMEDIATE HALT
echo "OFF" > .upgrade_toggle

# Kill all processes
pkill -f "ghost_trading\|micro_trading\|live_ghost"
```

## 📊 MONITORING

### Dashboard (UI)
```bash
# Launch Streamlit dashboard
streamlit run dashboard_enhanced.py --server.port 8501
# Access: http://localhost:8501
```

### TMUX Terminals (Headless)
```bash
# Launch 4-pane battlestation
scripts/ui_headless/launch_rick_comms.sh
scripts/ui_headless/launch_oanda_ops.sh
scripts/ui_headless/launch_coinbase_ops.sh

# Attach to session
tmux attach -t RBZ_RICK_COMMS
```

### Logs
```bash
# Real-time narration
tail -f pre_upgrade/headless/logs/narration.jsonl | jq -r .text

# P&L tracking
tail -f pre_upgrade/headless/logs/pnl.jsonl | jq

# System mode
cat .upgrade_toggle
```

## 📁 STRUCTURE

```
RICK_LIVE_YYYYMMDD_HHMMSS/
├── foundation/                 # Charter enforcement (PIN 841921, RR≥3.2, -5% breaker)
├── wolf_packs/                 # Trading strategies
├── risk/                       # Risk management
├── brokers/                    # OANDA & Coinbase connectors
├── execution/                  # Trade execution & OCO
├── logic/                      # Trading logic
├── configs/                    # Configuration files
├── dashboard/                  # UI components
├── hive/                       # AI hive mind (optional)
├── scripts/                    # Automation scripts
├── pre_upgrade/headless/       # Logs & narration
├── live_ghost_engine.py        # Main trading engine
├── dashboard_enhanced.py       # Main UI entry
├── activate_live_trading.sh    # PIN-gated activation
└── .upgrade_toggle             # Safety switch (OFF=safe, ON=live)
```

## 🔐 SECURITY

- `.env` file MUST have `chmod 0600` permissions
- `.upgrade_toggle` gate prevents accidental live trading
- PIN 841921 required for live activation
- Charter rules enforced: RR≥3.2:1, -5% daily breaker, ≤6hr holds

## 📖 CHARTER RULES (Non-Negotiable)

- **PIN**: 841921 required for live operations
- **Risk/Reward**: Minimum 3.2:1 (auto-reject ≤2.9:1)
- **Session Breaker**: -5% daily loss halts trading
- **Hold Time**: Maximum 6 hours per position
- **Position Size**: Minimum $15,000 notional
- **Timeframes**: Only M15, M30, H1 allowed

## 🆘 SUPPORT

- Check logs: `pre_upgrade/headless/logs/`
- Run diagnostics: `./live_preflight_check.sh`
- Emergency stop: `echo "OFF" > .upgrade_toggle`
- GitHub Issues: [repo link]

## 📝 VERSION INFO

- Deployment Date: [TIMESTAMP]
- Source Commit: [GIT_COMMIT]
- Essential Files Only: ~3-5 MB
- Bloat Removed: 98GB

---

**⚠️ CRITICAL**: Always test in Ghost mode first. Never activate live trading without successful ghost validation and PIN 841921 approval.
EOF

echo "✅ Deployment README created"
echo ""

# ============================================================================
# CREATE TARBALL
# ============================================================================

echo "📦 Creating deployment tarball..."

cd "$(dirname "$DEPLOY_DIR")"
TARBALL="RICK_LIVE_${TIMESTAMP}.tar.gz"

tar -czf "$TARBALL" "$(basename "$DEPLOY_DIR")"

TARBALL_SIZE=$(du -h "$TARBALL" | awk '{print $1}')

echo "✅ Tarball created: $TARBALL ($TARBALL_SIZE)"
echo ""

# ============================================================================
# GENERATE DEPLOYMENT CHECKLIST
# ============================================================================

cat > "${DEPLOY_DIR}/DEPLOYMENT_CHECKLIST.txt" << EOF
═══════════════════════════════════════════════════════════════
  RICK LIVE DEPLOYMENT CHECKLIST
═══════════════════════════════════════════════════════════════

Created: $(date)
Package: RICK_LIVE_${TIMESTAMP}

PRE-DEPLOYMENT:
  [ ] Copy deployment package to target server
  [ ] Extract: tar -xzf RICK_LIVE_${TIMESTAMP}.tar.gz
  [ ] Create venv: python3 -m venv venv
  [ ] Activate venv: source venv/bin/activate
  [ ] Install deps: pip install -r requirements.txt
  
CONFIGURATION:
  [ ] Copy .env.template to .env
  [ ] Edit .env with OANDA credentials
  [ ] Edit .env with Coinbase credentials
  [ ] Set permissions: chmod 0600 .env
  [ ] Verify .upgrade_toggle = OFF
  
TESTING:
  [ ] Run ghost mode: ./start_ghost_trading.sh
  [ ] Monitor for 45-90 minutes
  [ ] Verify signals generated
  [ ] Verify P&L tracking works
  [ ] Check logs: tail -f pre_upgrade/headless/logs/narration.jsonl
  
PRE-FLIGHT:
  [ ] Run: ./live_preflight_check.sh
  [ ] All checks must PASS
  [ ] Verify API endpoints (live, not practice)
  [ ] Confirm account balances correct
  
ACTIVATION (PIN 841921):
  [ ] Have PIN 841921 ready
  [ ] Run: ./activate_live_trading.sh
  [ ] Enter PIN when prompted
  [ ] Verify: cat .upgrade_toggle (should be ON)
  [ ] Run: ./verify_live_safety.sh
  
MONITORING:
  [ ] Launch dashboard: streamlit run dashboard_enhanced.py
  [ ] Monitor first trade closely
  [ ] Verify OCO orders placed correctly
  [ ] Check risk limits enforced
  
EMERGENCY PROCEDURES:
  [ ] Know how to stop: echo "OFF" > .upgrade_toggle
  [ ] Have phone alerts configured
  [ ] Monitor account balance
  
═══════════════════════════════════════════════════════════════
IMPORTANT NOTES:
- NEVER skip ghost mode validation
- ALWAYS verify .env permissions (0600)
- KEEP .upgrade_toggle=OFF until ready
- PIN 841921 required for live activation
- Charter rules enforced automatically
═══════════════════════════════════════════════════════════════
EOF

echo "✅ Deployment checklist created"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ DEPLOYMENT PACKAGE COMPLETE                              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 PACKAGE SUMMARY:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Location:       $DEPLOY_DIR"
echo "Tarball:        $(dirname "$DEPLOY_DIR")/$TARBALL"
echo "Size:           $TARBALL_SIZE"
echo "Created:        $(date)"
echo ""

echo "📁 INCLUDED COMPONENTS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Foundation (charter enforcement)"
echo "✅ Wolf packs (trading strategies)"
echo "✅ Risk management"
echo "✅ Broker connectors (OANDA, Coinbase)"
echo "✅ Execution engine"
echo "✅ Dashboard UI"
echo "✅ Hive mind (AI orchestration)"
echo "✅ Scripts & automation"
echo "✅ Configuration templates"
echo ""

echo "❌ EXCLUDED (98GB bloat removed):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• Rollback snapshots (47GB)"
echo "• Packaged backups (25GB)"
echo "• Git repositories (25GB)"
echo "• Archive/legacy code (177MB)"
echo "• Test files and artifacts"
echo "• Development environments"
echo ""

echo "📋 NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Review:    $DEPLOY_DIR/DEPLOYMENT_README.md"
echo "2. Checklist: $DEPLOY_DIR/DEPLOYMENT_CHECKLIST.txt"
echo "3. Transfer:  scp $TARBALL user@server:/path/"
echo "4. Extract:   tar -xzf $TARBALL"
echo "5. Configure: cp .env.template .env && nano .env"
echo "6. Test:      ./start_ghost_trading.sh"
echo "7. Activate:  ./activate_live_trading.sh (PIN 841921)"
echo ""

echo "⚠️  IMPORTANT:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• DO NOT copy .env with credentials (use .env.template)"
echo "• ALWAYS test in Ghost mode first"
echo "• VERIFY .upgrade_toggle=OFF before deployment"
echo "• RUN live_preflight_check.sh before activation"
echo "• PIN 841921 required for live trading"
echo ""

echo "✅ Deployment package ready for production use"
