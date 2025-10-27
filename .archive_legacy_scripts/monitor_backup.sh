#!/bin/bash
# Monitor the full backup progress
# Run this to check status: ./monitor_backup.sh

BACKUP_FILE="/home/ing/RICK/R_H_UNI/RICK_FULL_98GB_BACKUP_20251008.tar.gz"

echo "🔍 RICK Full Backup Monitor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if backup file exists
if [[ ! -f "$BACKUP_FILE" ]]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Check if tar process is running
if ps aux | grep "[t]ar.*RICK_FULL" > /dev/null; then
    echo "✅ Status: RUNNING"
    echo ""
    
    # Get process info
    PS_INFO=$(ps aux | grep "[t]ar.*RICK_FULL" | awk '{print "   PID: "$2"\n   CPU Time: "$10"\n   Start: "$9}')
    echo "$PS_INFO"
    echo ""
    
    # Get current file size
    CURRENT_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "📦 Current Size: $CURRENT_SIZE"
    echo "🎯 Target Size:  ~15-25 GB"
    echo ""
    
    # Calculate rough percentage (assuming 20GB target)
    SIZE_MB=$(du -m "$BACKUP_FILE" | cut -f1)
    TARGET_MB=20480  # 20GB
    PERCENT=$((SIZE_MB * 100 / TARGET_MB))
    if [[ $PERCENT -gt 100 ]]; then
        PERCENT=100
    fi
    
    echo "⏳ Progress: ~${PERCENT}%"
    echo ""
    echo "💡 Estimated time remaining: 10-20 minutes"
    echo ""
    echo "Run this script again to check progress:"
    echo "   ./monitor_backup.sh"
    
else
    echo "✅ Status: COMPLETE"
    echo ""
    
    FINAL_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "📦 Final Size: $FINAL_SIZE"
    echo ""
    echo "✅ Backup ready to copy to OneDrive!"
    echo ""
    echo "Next steps:"
    echo "1. Copy to OneDrive:"
    echo "   cp $BACKUP_FILE /mnt/c/Users/RFing/OneDrive/"
    echo ""
    echo "2. Copy clean version too:"
    echo "   cp /home/ing/RICK/R_H_UNI/RICK_LIVE_20251008_110119.tar.gz /mnt/c/Users/RFing/OneDrive/"
    echo "   cp -r /home/ing/RICK/R_H_UNI/RICK_LIVE_20251008_110119 /mnt/c/Users/RFing/OneDrive/"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
