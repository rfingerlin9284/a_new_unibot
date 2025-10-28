#!/usr/bin/env python3
"""
RBOTzilla System Architecture Diagram Generator
Creates PNG visualization of complete system architecture with modular components
PIN: 841921 | Date: 2025-10-20
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Color scheme
COLOR_CORE = '#FF6B6B'        # Red for core trading
COLOR_GATE = '#4ECDC4'        # Teal for gates
COLOR_SUBSYSTEM = '#45B7D1'   # Blue for subsystems
COLOR_INFRASTRUCTURE = '#95E1D3'  # Mint for infrastructure
COLOR_DATA = '#FFD93D'        # Yellow for data
COLOR_API = '#A8E6CF'         # Light green for API
COLOR_UI = '#FF8B94'          # Pink for UI

def draw_box(ax, x, y, width, height, label, color, fontsize=9, fontweight='normal'):
    """Draw a rounded rectangle box with text"""
    box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.05",
                         edgecolor='black', facecolor=color, linewidth=2, alpha=0.8)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, label, ha='center', va='center',
           fontsize=fontsize, fontweight=fontweight, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='black', style='->', lw=2):
    """Draw an arrow between two points"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                          mutation_scale=20, linewidth=lw, edgecolor=color, facecolor=color)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 1, mid_y + 1, label, fontsize=7, style='italic', color=color)

# Title
ax.text(50, 97, '🤖 RBOTzilla Trading System Architecture', 
        ha='center', fontsize=18, fontweight='bold')
ax.text(50, 95, 'PIN: 841921 | Charter-Compliant | Fully Autonomous', 
        ha='center', fontsize=10, style='italic')

# ============================================================================
# LAYER 1: INPUT SOURCES (Top)
# ============================================================================
ax.text(2, 92, 'INPUT SOURCES', fontsize=10, fontweight='bold', color='black')

draw_box(ax, 3, 87, 12, 4, 'OANDA API\nReal-time Forex\nPrices & Positions', COLOR_API)
draw_box(ax, 17, 87, 12, 4, 'Market Data\nLive Streams\nTechnical Data', COLOR_API)
draw_box(ax, 31, 87, 12, 4, 'Correlation\nMatrix\nCurrency Pairs', COLOR_DATA)
draw_box(ax, 45, 87, 12, 4, 'Account State\nBalance\nMargin Usage', COLOR_DATA)

# ============================================================================
# LAYER 2: ANALYSIS ENGINES (Upper-Middle)
# ============================================================================
ax.text(2, 80, 'ANALYSIS ENGINES', fontsize=10, fontweight='bold', color='black')

draw_box(ax, 3, 74, 11, 5, 'ML Intelligence\n• Regime Detection\n• Signal Analysis\n• Confidence Scoring', COLOR_SUBSYSTEM)
draw_arrow(ax, 9, 87, 8.5, 79, style='->', color='black')

draw_box(ax, 16, 74, 11, 5, 'Strategy Aggregator\n• 5 Prototype Strategies\n• Voting System (2/5)\n• Signal Consensus', COLOR_SUBSYSTEM)
draw_arrow(ax, 23, 87, 21.5, 79, style='->', color='black')

draw_box(ax, 29, 74, 11, 5, 'Momentum System\n• Golden Age Detector\n• Trailing Stops\n• Breakeven Manager', COLOR_SUBSYSTEM)
draw_arrow(ax, 37, 87, 34.5, 79, style='->', color='black')

draw_box(ax, 42, 74, 11, 5, 'Quant Hedge Engine\n• Correlation Analysis\n• 7-Rule Hedge Logic\n• Inverse Pair Matching', COLOR_SUBSYSTEM)
draw_arrow(ax, 51, 87, 47.5, 79, style='->', color='black')

# ============================================================================
# LAYER 3: DECISION AGGREGATION (Middle)
# ============================================================================
ax.text(2, 68, 'DECISION AGGREGATION', fontsize=10, fontweight='bold', color='black')

draw_box(ax, 8, 60, 14, 7, 'Hive Mind\nConsensus Engine\n• Multi-Signal Vote\n• Confidence Weighting\n• Signal Amplification', COLOR_SUBSYSTEM)
draw_arrow(ax, 8.5, 74, 10, 67, style='->', color='black')
draw_arrow(ax, 21.5, 74, 15.5, 67, style='->', color='black')
draw_arrow(ax, 34.5, 74, 12.5, 67, style='->', color='black')
draw_arrow(ax, 47.5, 74, 14.5, 67, style='->', color='black')

draw_box(ax, 28, 60, 14, 7, 'Trade Decision Logic\n• Signal Threshold: 70%\n• Timeframe Validation\n• Entry Price Calculation', COLOR_SUBSYSTEM)
draw_arrow(ax, 15, 63, 28, 63, style='->', color='black')

# ============================================================================
# LAYER 4: GUARDIAN GATES (Critical Center)
# ============================================================================
ax.text(2, 55, 'GUARDIAN GATE SYSTEM', fontsize=10, fontweight='bold', color='darkred')
ax.text(2, 53, '🛡️ Pre-Trade Validation (IMMUTABLE)', fontsize=9, fontweight='bold', color='darkred')

draw_box(ax, 52, 58, 13, 8, 'Charter Validation\n• PIN: 841921 ✅\n• Min Notional: $15k\n• Min R:R: 3.2:1\n• Max Daily Loss: -5%', COLOR_GATE, fontweight='bold')
ax.text(58.5, 51.5, 'Charter Constants\n(Immutable)', fontsize=7, ha='center', style='italic')

draw_box(ax, 42, 58, 9, 8, 'Margin Gate\nMargin ≤ 35%\nBlock if violated', COLOR_GATE, fontweight='bold')
draw_arrow(ax, 35, 63, 42, 63, style='->', color='red', lw=2.5)

draw_box(ax, 32, 58, 9, 8, 'Correlation Gate\nNo Same-Side\nCorrelated Increase', COLOR_GATE, fontweight='bold')
draw_arrow(ax, 35, 60, 32, 63, style='->', color='red', lw=2.5)

draw_box(ax, 22, 58, 9, 8, 'Notional Gate\n≥ $15,000\nBlock if under', COLOR_GATE, fontweight='bold')
draw_arrow(ax, 35, 60, 31, 63, style='->', color='red', lw=2.5)

# ============================================================================
# LAYER 5: CORE TRADING ENGINE (Lower-Middle)
# ============================================================================
ax.text(2, 50, 'CORE TRADING ENGINE', fontsize=10, fontweight='bold', color='black')

draw_box(ax, 10, 42, 16, 6, 'Order Execution\n• OCO Orders (Immutable)\n• Position Sizing\n• Stop Loss & Take Profit\n• Risk-Reward Enforcement', COLOR_CORE, fontweight='bold')
draw_arrow(ax, 58.5, 58, 35, 48, label='validated order', color='red', lw=2)
draw_arrow(ax, 42, 58, 25, 48, label='margin check', color='red', lw=2)

draw_box(ax, 35, 42, 16, 6, 'Trade Logging\n• Narration System\n• Event Capture\n• Decision Trail\n• Audit Log', COLOR_DATA, fontweight='bold')
draw_arrow(ax, 26, 45, 35, 45, style='->', color='black', lw=2)

# ============================================================================
# LAYER 6: STATE PERSISTENCE & MONITORING (Lower)
# ============================================================================
ax.text(2, 38, 'STATE PERSISTENCE & MONITORING', fontsize=10, fontweight='bold', color='black')

draw_box(ax, 5, 30, 12, 6, 'Position State\nconnection_state.json\n• Open Positions\n• Entry Prices\n• P&L Tracking', COLOR_DATA)
draw_arrow(ax, 18, 42, 11, 36, style='->', color='black')

draw_box(ax, 20, 30, 12, 6, 'Event Logging\nnarration.jsonl\n• Append-only\n• Timestamped\n• Immutable', COLOR_DATA)
draw_arrow(ax, 35, 42, 26, 36, style='->', color='black')

draw_box(ax, 35, 30, 12, 6, 'Backup System\nTimestamped Snapshots\n• State Recovery\n• Rollback Capability\n• Emergency Restore', COLOR_INFRASTRUCTURE)

draw_box(ax, 50, 30, 12, 6, 'Terminal Display\nReal-time Dashboard\n• 3-Pane Layout\n• Live Narration\n• AI Decisions\n• Manual Control', COLOR_UI)

# ============================================================================
# LAYER 7: ORCHESTRATION & CONTROL (Bottom)
# ============================================================================
ax.text(2, 24, 'ORCHESTRATION & CONTROL', fontsize=10, fontweight='bold', color='black')

draw_box(ax, 5, 16, 11, 6, 'Smart Startup\nSMART_STARTUP.sh\n• Process Detection\n• Graceful Reuse\n• 7-Phase Boot\n• Verification', COLOR_INFRASTRUCTURE, fontweight='bold')

draw_box(ax, 19, 16, 11, 6, 'Verification Suite\nverify_complete_system.py\n• 9-Section Checklist\n• Gate Validation\n• Feature Confirmation', COLOR_INFRASTRUCTURE, fontweight='bold')

draw_box(ax, 33, 16, 11, 6, 'System Control\nTask.json Integration\n• Start/Stop/Restart\n• Ollama Management\n• Dashboard Launch', COLOR_INFRASTRUCTURE, fontweight='bold')

draw_box(ax, 47, 16, 11, 6, 'Rick Narrator\nOllama Integration\n• LLM Commentary\n• Background Service\n• Optional Narration', COLOR_SUBSYSTEM)

# Draw arrows from engines to gates
draw_arrow(ax, 50, 56, 50, 50, color='red', lw=2.5)

# Draw flow from gates to logging
draw_arrow(ax, 45, 48, 26, 36, label='all decisions\nlogged', color='blue', lw=2)

# ============================================================================
# LEGEND & ANNOTATIONS
# ============================================================================
ax.text(2, 12, 'SECURITY LAYERS', fontsize=9, fontweight='bold')
ax.text(2, 10, '🔐 Layer 1: Immutable Constants (hardcoded, cannot override)', fontsize=7)
ax.text(2, 8.5, '🔐 Layer 2: PIN Validation (841921, enforced at startup)', fontsize=7)
ax.text(2, 7, '🔐 Layer 3: Pre-Trade Gates (margin, correlation, notional, RR)', fontsize=7)
ax.text(2, 5.5, '🔐 Layer 4: Append-Only Logging (immutable event trail)', fontsize=7)

# Add legend
legend_elements = [
    mpatches.Patch(facecolor=COLOR_CORE, edgecolor='black', label='Core Trading'),
    mpatches.Patch(facecolor=COLOR_GATE, edgecolor='black', label='Guardian Gates'),
    mpatches.Patch(facecolor=COLOR_SUBSYSTEM, edgecolor='black', label='AI Subsystems'),
    mpatches.Patch(facecolor=COLOR_DATA, edgecolor='black', label='Data/Logging'),
    mpatches.Patch(facecolor=COLOR_INFRASTRUCTURE, edgecolor='black', label='Infrastructure'),
    mpatches.Patch(facecolor=COLOR_API, edgecolor='black', label='External API'),
    mpatches.Patch(facecolor=COLOR_UI, edgecolor='black', label='User Interface'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.9)

# Add status indicators
ax.text(70, 10, 'SYSTEM STATUS', fontsize=9, fontweight='bold')
ax.text(70, 8, '✅ Charter: IMMUTABLE', fontsize=7, color='darkgreen')
ax.text(70, 6.5, '✅ Gates: ACTIVE', fontsize=7, color='darkgreen')
ax.text(70, 5, '✅ Logging: ENABLED', fontsize=7, color='darkgreen')
ax.text(70, 3.5, '✅ State Recovery: AUTO', fontsize=7, color='darkgreen')
ax.text(70, 2, '✅ Verification: COMPLETE', fontsize=7, color='darkgreen')

plt.tight_layout()
plt.savefig('/home/ing/RICK/RICK_LIVE_PROTOTYPE/SYSTEM_ARCHITECTURE.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ System architecture PNG created: SYSTEM_ARCHITECTURE.png")
