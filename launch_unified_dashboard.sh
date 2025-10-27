#!/bin/bash
# RICK Unified Dashboard Launcher
# PIN 841921 Approved | Quick start for consolidated dashboard

echo "🤖 RICK Unified Dashboard Launcher"
echo "===================================="
echo ""

# Check if streamlit is available
STREAMLIT_PATH="$HOME/RICK/R_H_UNI/pre_upgrade/standalone/.venv/bin/streamlit"
DASHBOARD_PATH="$HOME/RICK/R_H_UNI/dashboard_unified.py"

if [ ! -f "$STREAMLIT_PATH" ]; then
    echo "⚠️  Streamlit not found at expected location"
    echo "   Trying alternate virtual environment..."
    STREAMLIT_PATH="$HOME/RICK/R_H_UNI/venv/bin/streamlit"
fi

if [ ! -f "$STREAMLIT_PATH" ]; then
    echo "❌ Streamlit not found. Please install it first:"
    echo "   source pre_upgrade/standalone/.venv/bin/activate"
    echo "   pip install streamlit"
    exit 1
fi

if [ ! -f "$DASHBOARD_PATH" ]; then
    echo "❌ Dashboard file not found at: $DASHBOARD_PATH"
    exit 1
fi

echo "✅ Streamlit found: $STREAMLIT_PATH"
echo "✅ Dashboard found: $DASHBOARD_PATH"
echo ""
echo "🚀 Launching unified dashboard on port 8501..."
echo "🌐 Open browser to: http://localhost:8501"
echo ""
echo "Features:"
echo "  📊 Live narration feed from Rick's workflow"
echo "  💰 Real-time P&L stream"
echo "  💬 Chat interface with Rick and Hive"
echo "  🐝 Hive member status monitoring"
echo "  📜 Charter compliance display"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Launch the unified dashboard
"$STREAMLIT_PATH" run "$DASHBOARD_PATH" --server.port 8501
