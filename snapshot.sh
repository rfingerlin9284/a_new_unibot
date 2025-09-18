#!/bin/bash
# Critical Files Snapshot Wrapper Script
# Quick and easy way to create snapshots of critical trading files

set -e

echo "🔍 Critical Files Snapshot Tool"
echo "================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

# Check if configuration file exists
if [ ! -f "critical_files_config.json" ]; then
    echo "❌ Error: critical_files_config.json not found"
    echo "   Make sure you're in the correct directory"
    exit 1
fi

# Parse command line arguments
case "${1:-snapshot}" in
    "snapshot"|"snap")
        echo "📸 Creating critical files snapshot..."
        python3 snapshot_critical_files.py
        ;;
    "demo"|"test")
        echo "🧪 Creating demo files and running snapshot..."
        python3 create_sample_files.py
        echo ""
        python3 snapshot_critical_files.py
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  snapshot, snap    Create snapshot of critical files (default)"
        echo "  demo, test        Create demo files and run snapshot"
        echo "  help, -h, --help  Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                # Create snapshot"
        echo "  $0 snapshot       # Create snapshot"
        echo "  $0 demo           # Demo with sample files"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "   Use '$0 help' for usage information"
        exit 1
        ;;
esac

echo ""
echo "✅ Operation completed successfully!"