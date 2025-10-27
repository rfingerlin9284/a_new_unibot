#!/bin/bash
# RICK Dashboard Startup Script

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv_dashboard"
LOG_DIR="$SCRIPT_DIR/logs"
OLLAMA_MODEL="llama3.1:8b"
STREAMLIT_PORT=8501

mkdir -p "$LOG_DIR"

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }
warning() { echo -e "${YELLOW}[!]${NC} $1"; }

check_ollama() {
    if pgrep -x "ollama" > /dev/null; then
        success "Ollama is running"
        return 0
    fi
    return 1
}

check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
}

show_usage() {
    cat << USAGE
${CYAN}RICK Dashboard Startup${NC}
Usage: $0 [--web|--cli|--both]
USAGE
}

main() {
    echo -e "${CYAN}╔════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  🤖 RICK DASHBOARD STARTUP       ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════╝${NC}\n"
    
    check_venv
    
    info "Checking dependencies..."
    pip install -q streamlit plotly pandas requests 2>/dev/null || warning "Some packages may not install"
    success "Dependencies ready"
    
    info "Checking Ollama..."
    if ! check_ollama; then
        warning "Ollama not running. Start with: ollama serve"
    fi
    
    local mode="${1:---web}"
    
    case "$mode" in
        --web)
            info "Starting Streamlit dashboard..."
            streamlit run "$SCRIPT_DIR/dashboard_unified.py" --logger.level=error
            ;;
        --cli)
            info "Starting headless dashboard..."
            python "$SCRIPT_DIR/dashboard_headless.py"
            ;;
        --both)
            info "Starting both dashboards..."
            python "$SCRIPT_DIR/dashboard_headless.py" > "$LOG_DIR/headless.log" 2>&1 &
            success "Headless dashboard running (background)"
            sleep 2
            streamlit run "$SCRIPT_DIR/dashboard_unified.py" --logger.level=error
            ;;
        *)
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
