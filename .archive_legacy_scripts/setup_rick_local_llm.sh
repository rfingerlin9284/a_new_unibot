#!/bin/bash
# setup_rick_local_llm.sh - Install and Configure Rick's Local LLM Brain
# PIN 841921 Approved | Charter Compliant

set -e

PROJECT_ROOT="/home/ing/RICK/R_H_UNI"
cd "$PROJECT_ROOT" || exit 1

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🧠 RICK LOCAL LLM SETUP - Ollama Installation             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: Install Ollama
# ============================================================================

echo "📦 Step 1: Installing Ollama..."
echo ""

if command -v ollama &> /dev/null; then
    echo "✅ Ollama already installed: $(ollama --version)"
else
    echo "⬇️  Downloading and installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama installed successfully"
    else
        echo "❌ Ollama installation failed"
        exit 1
    fi
fi

echo ""

# ============================================================================
# STEP 2: Start Ollama Service
# ============================================================================

echo "🚀 Step 2: Starting Ollama service..."
echo ""

# Check if ollama is already running
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama service already running"
else
    echo "   Starting Ollama in background..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    
    if pgrep -x "ollama" > /dev/null; then
        echo "✅ Ollama service started"
    else
        echo "⚠️  Ollama service didn't start automatically"
        echo "   You may need to run: ollama serve"
    fi
fi

echo ""

# ============================================================================
# STEP 3: Download LLM Models
# ============================================================================

echo "📥 Step 3: Downloading LLM models..."
echo ""

# Recommended models in order of size/speed
MODELS=(
    "llama3.2:1b"      # 1GB  - Fastest (good for quick responses)
    "llama3.2:latest"  # 3GB  - Balanced (recommended)
    # "mistral:latest"   # 7GB  - More powerful (optional)
)

echo "Available models:"
echo "  1. llama3.2:1b     (~1GB) - Fastest, good for chat"
echo "  2. llama3.2:latest (~3GB) - Balanced (RECOMMENDED)"
echo "  3. mistral:latest  (~7GB) - Most powerful, slower"
echo ""

read -p "Which model to download? (1/2/3 or 'all') [2]: " choice
choice=${choice:-2}

case $choice in
    1)
        DOWNLOAD_MODELS=("llama3.2:1b")
        ;;
    2)
        DOWNLOAD_MODELS=("llama3.2:latest")
        ;;
    3)
        DOWNLOAD_MODELS=("mistral:latest")
        ;;
    all)
        DOWNLOAD_MODELS=("llama3.2:1b" "llama3.2:latest" "mistral:latest")
        ;;
    *)
        DOWNLOAD_MODELS=("llama3.2:latest")
        ;;
esac

for model in "${DOWNLOAD_MODELS[@]}"; do
    echo ""
    echo "⬇️  Downloading $model..."
    ollama pull "$model"
    
    if [ $? -eq 0 ]; then
        echo "✅ $model downloaded"
    else
        echo "❌ Failed to download $model"
    fi
done

echo ""

# ============================================================================
# STEP 4: Test Rick's LLM
# ============================================================================

echo "🧪 Step 4: Testing Rick's local brain..."
echo ""

python3 rick_ollama_server.py

echo ""

# ============================================================================
# STEP 5: Create Systemd Service (Optional)
# ============================================================================

echo "🔧 Step 5: Setup Ollama as system service..."
echo ""

read -p "Enable Ollama to start on boot? (y/n) [y]: " enable_service
enable_service=${enable_service:-y}

if [ "$enable_service" = "y" ] || [ "$enable_service" = "Y" ]; then
    if [ ! -f /etc/systemd/system/ollama.service ]; then
        echo "   Creating systemd service..."
        
        cat << 'EOF' | sudo tee /etc/systemd/system/ollama.service > /dev/null
[Unit]
Description=Ollama Local LLM Server
After=network-online.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
        
        # Fix $USER in service file
        sudo sed -i "s/\$USER/$USER/g" /etc/systemd/system/ollama.service
        
        sudo systemctl daemon-reload
        sudo systemctl enable ollama
        sudo systemctl start ollama
        
        echo "✅ Ollama service enabled and started"
    else
        echo "✅ Ollama service already exists"
    fi
else
    echo "⏭️  Skipped service setup"
    echo "   To start Ollama manually: ollama serve"
fi

echo ""

# ============================================================================
# COMPLETION
# ============================================================================

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ RICK LOCAL LLM SETUP COMPLETE                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 Installation Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ollama:        $(ollama --version 2>/dev/null || echo 'Not in PATH')"
echo "Service:       $(systemctl is-active ollama 2>/dev/null || echo 'Not running as service')"
echo "API:           http://localhost:11434"
echo ""
echo "Installed Models:"
ollama list 2>/dev/null || echo "  (run 'ollama list' to see models)"
echo ""

echo "🚀 Quick Start Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "# Test Rick's brain"
echo "python3 rick_ollama_server.py"
echo ""
echo "# Chat with Rick (CLI)"
echo "ollama run llama3.2"
echo ""
echo "# Check status"
echo "systemctl status ollama"
echo ""
echo "# View logs"
echo "journalctl -u ollama -f"
echo ""

echo "📚 Integration with Dashboard:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Rick Chat will automatically detect local LLM"
echo "2. No API keys needed - runs 100% offline"
echo "3. Faster responses than external APIs"
echo "4. Complete privacy - data never leaves your machine"
echo ""

echo "⚠️  Important Notes:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "- Ollama uses ~2-8GB RAM depending on model"
echo "- First response may be slower (model loading)"
echo "- Models stored in: ~/.ollama/models"
echo "- To remove models: ollama rm <model-name>"
echo ""

echo "✅ Setup complete! Rick's local brain is ready."
