#!/bin/bash
# Quick Browser Hive Commands
# PIN 841921 Approved

PROJECT_ROOT="/home/ing/RICK/R_H_UNI"
cd "$PROJECT_ROOT" || exit 1

case "${1:-help}" in
    test)
        echo "🧪 Testing browser automation..."
        python3 test_browser_snap.py
        ;;
    
    status)
        echo "📊 Browser Hive Status"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Chromium:      $(snap info chromium | grep installed | awk '{print $2}')"
        echo "ChromeDriver:  $(chromium.chromedriver --version 2>&1 | head -n1)"
        echo "Selenium:      $(python3 -c 'import selenium; print(selenium.__version__)' 2>/dev/null || echo 'NOT INSTALLED')"
        echo "Cache Dir:     $PROJECT_ROOT/.browser_cache"
        echo ""
        echo "Browser processes:"
        pgrep -fa chromium | grep -v grep || echo "  (none running)"
        ;;
    
    clean)
        echo "🧹 Cleaning browser cache..."
        rm -rf "$PROJECT_ROOT/.browser_cache"/*
        mkdir -p "$PROJECT_ROOT/.browser_cache"/{chatgpt,grok,deepseek,github}
        echo "✅ Cache cleaned"
        ;;
    
    kill)
        echo "🛑 Killing all browser processes..."
        pkill -f chromium
        echo "✅ Browsers terminated"
        ;;
    
    providers)
        echo "🧠 AI Providers (Browser-Based)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "ChatGPT:   https://chat.openai.com"
        echo "Grok:      https://x.com/i/grok"
        echo "DeepSeek:  https://chat.deepseek.com"
        echo "GitHub:    VS Code Extension API / github.com"
        echo ""
        echo "Cache status:"
        for provider in chatgpt grok deepseek github; do
            cache_dir="$PROJECT_ROOT/.browser_cache/$provider"
            if [ -d "$cache_dir" ]; then
                size=$(du -sh "$cache_dir" 2>/dev/null | awk '{print $1}')
                echo "  $provider: $size"
            else
                echo "  $provider: (no cache)"
            fi
        done
        ;;
    
    help|*)
        echo "🧠 Rick Browser Hive — Quick Commands"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Usage: ./quick_browser_hive.sh [command]"
        echo ""
        echo "Commands:"
        echo "  test       — Test browser automation (navigate to Google)"
        echo "  status     — Show Chromium/Selenium versions and running processes"
        echo "  clean      — Clear browser cache directories"
        echo "  kill       — Terminate all browser processes"
        echo "  providers  — List AI providers and cache status"
        echo "  help       — Show this message"
        echo ""
        echo "Examples:"
        echo "  ./quick_browser_hive.sh test      # Validate browser automation"
        echo "  ./quick_browser_hive.sh status    # Check versions"
        echo "  ./quick_browser_hive.sh clean     # Clear cache before testing"
        ;;
esac
