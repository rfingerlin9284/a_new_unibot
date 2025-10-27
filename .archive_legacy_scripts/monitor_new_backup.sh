#!/bin/bash
# Monitor the new complete backup creation

echo "🔍 Monitoring RICK Complete Backup Creation"
echo "=========================================="
echo ""

while true; do
    clear
    echo "🔍 RICK COMPLETE BACKUP - LIVE MONITOR"
    echo "========================================"
    echo ""
    echo "📅 Time: $(date '+%H:%M:%S')"
    echo ""
    
    # Find the latest backup file
    BACKUP_FILE=$(ls -t /home/ing/RICK/RICK_COMPLETE_BACKUP_*.tar.gz 2>/dev/null | head -1)
    
    if [ -n "$BACKUP_FILE" ]; then
        echo "📦 Backup File: $(basename $BACKUP_FILE)"
        echo ""
        
        # Get current size
        CURRENT_SIZE=$(du -h "$BACKUP_FILE" 2>/dev/null | cut -f1)
        CURRENT_SIZE_MB=$(du -m "$BACKUP_FILE" 2>/dev/null | cut -f1)
        
        echo "💾 Current Size: $CURRENT_SIZE (${CURRENT_SIZE_MB}MB)"
        echo ""
        
        # Check if tar process is running
        if pgrep -f "tar.*RICK_COMPLETE_BACKUP" > /dev/null; then
            echo "✅ Status: COMPRESSING... (tar process active)"
            echo ""
            
            # Estimate completion (target ~650MB)
            if [ "$CURRENT_SIZE_MB" -gt 0 ]; then
                PERCENT=$((CURRENT_SIZE_MB * 100 / 650))
                if [ "$PERCENT" -gt 100 ]; then PERCENT=99; fi
                echo "📊 Estimated Progress: ~${PERCENT}%"
                echo "🎯 Target Size: ~600-700MB"
            fi
        else
            echo "🎉 Status: COMPLETE!"
            echo ""
            echo "✅ Backup finished successfully!"
            break
        fi
    else
        echo "⏳ Waiting for backup file to be created..."
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Press Ctrl+C to stop monitoring"
    
    sleep 5
done

echo ""
echo "🎯 FINAL RESULT:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh /home/ing/RICK/RICK_COMPLETE_BACKUP_*.tar.gz 2>/dev/null | tail -1
echo ""
echo "✅ Ready to copy to OneDrive!"
