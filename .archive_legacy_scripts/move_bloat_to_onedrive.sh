#!/bin/bash
# RICK - Bloat Relocation to OneDrive
# Safely moves legacy backup directories to OneDrive cloud storage
# NO DELETION - files are relocated, not removed

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SOURCE_DIR="/home/ing/RICK/R_H_UNI"
DEST_BASE="/mnt/c/Users/RFing/OneDrive/RHUNI_BLOAT_10-2025"

# Directories to move
DIRS_TO_MOVE=(
    "ROLLBACK_SNAPSHOTS"
    "packaged_backups"
    "R_H_UNI_backups"
)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}   🚚 RICK BLOAT RELOCATION TO ONEDRIVE${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Verify source directories exist
echo -e "${YELLOW}📋 Verifying source directories...${NC}"
MISSING=0
for dir in "${DIRS_TO_MOVE[@]}"; do
    if [ -d "$SOURCE_DIR/$dir" ]; then
        SIZE=$(du -sh "$SOURCE_DIR/$dir" 2>/dev/null | cut -f1)
        echo -e "   ${GREEN}✅${NC} $dir ($SIZE)"
    else
        echo -e "   ${RED}❌${NC} $dir (NOT FOUND)"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo -e "\n${RED}ERROR: $MISSING directories not found. Aborting.${NC}"
    exit 1
fi

# Calculate total size
echo ""
echo -e "${YELLOW}📊 Calculating total size...${NC}"
TOTAL_SIZE=$(du -shc "${DIRS_TO_MOVE[@]/#/$SOURCE_DIR/}" 2>/dev/null | tail -1 | cut -f1)
echo -e "   Total to move: ${GREEN}$TOTAL_SIZE${NC}"

# Create destination directory
echo ""
echo -e "${YELLOW}📁 Creating destination directory...${NC}"
mkdir -p "$DEST_BASE"
echo -e "   ${GREEN}✅${NC} $DEST_BASE"

# Confirmation prompt
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}⚠️  READY TO RELOCATE FILES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "   Source: ${SOURCE_DIR}"
echo -e "   Destination: ${DEST_BASE}"
echo -e "   Size: ${TOTAL_SIZE}"
echo ""
echo -e "   ${GREEN}This is a MOVE operation (cut/paste), not delete.${NC}"
echo -e "   Files will be relocated to OneDrive cloud storage."
echo ""
echo -e "${YELLOW}⏱️  Estimated time: 15-30 minutes${NC}"
echo -e "   (plus additional time for OneDrive cloud sync)"
echo ""
read -p "   Type 'RELOCATE' to proceed: " CONFIRM

if [ "$CONFIRM" != "RELOCATE" ]; then
    echo -e "\n${RED}❌ Operation cancelled by user.${NC}"
    exit 1
fi

# Move directories with progress
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 STARTING RELOCATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

START_TIME=$(date +%s)

for dir in "${DIRS_TO_MOVE[@]}"; do
    echo -e "${YELLOW}📦 Moving $dir...${NC}"
    
    # Use rsync for progress and safety
    rsync -ah --progress --remove-source-files \
        "$SOURCE_DIR/$dir/" "$DEST_BASE/$dir/" 2>&1 | \
        grep -E '(to-check|%)' | tail -20
    
    # Remove empty source directory after rsync
    find "$SOURCE_DIR/$dir" -type d -empty -delete
    
    echo -e "   ${GREEN}✅ $dir relocated${NC}"
    echo ""
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

# Verification
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ RELOCATION COMPLETE${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "   ⏱️  Time taken: ${MINUTES}m ${SECONDS}s"
echo ""
echo -e "${YELLOW}📂 Verifying destination...${NC}"

for dir in "${DIRS_TO_MOVE[@]}"; do
    if [ -d "$DEST_BASE/$dir" ]; then
        DEST_SIZE=$(du -sh "$DEST_BASE/$dir" 2>/dev/null | cut -f1)
        echo -e "   ${GREEN}✅${NC} $dir ($DEST_SIZE) in OneDrive"
    else
        echo -e "   ${RED}❌${NC} $dir NOT FOUND in destination"
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 PROJECT SIZE AFTER RELOCATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
NEW_SIZE=$(du -sh "$SOURCE_DIR" 2>/dev/null | cut -f1)
echo -e "   New project size: ${GREEN}$NEW_SIZE${NC}"
echo ""
echo -e "${YELLOW}📌 NOTE: OneDrive cloud sync will continue in background.${NC}"
echo -e "   Check Windows system tray for sync status."
echo ""
echo -e "${GREEN}✅ All files safely relocated to OneDrive!${NC}"
echo ""
