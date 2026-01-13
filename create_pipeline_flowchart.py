#!/usr/bin/env python3
"""
Generate data pipeline flowchart for Smart Agri BigData Platform
Updated for modern Dash/Plotly UI
Based on original sequence diagram
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import os

# Set up figure with dark background
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
fig.patch.set_facecolor('#1a1a1a')
ax.set_facecolor('#1a1a1a')
ax.set_xlim(0, 14)
ax.set_ylim(0, 12)
ax.axis('off')

# Define colors
color_box = '#2d5016'          # Dark green
color_box_light = '#4a7c2c'    # Light green
color_accent = '#7cb342'       # Bright green
color_phase = '#558b2f'        # Medium green
color_arrow = '#7cb342'        # Arrow color
color_text = '#ffffff'         # White text
color_phase_bg = '#3d5a1f'     # Dark green for phase backgrounds

# Title
ax.text(7, 11.5, 'Smart Agriculture Big Data Pipeline', 
        fontsize=22, fontweight='bold', ha='center', color=color_accent)
ax.text(7, 11.05, 'Phases 1-4: Data Generation → Processing → Analytics → Visualization', 
        fontsize=11, ha='center', color='#aaa', style='italic')

# Component boxes at top
components = [
    (0.5, 10.2, 1.3, 0.6, "Generator Script"),
    (2.1, 10.2, 1.3, 0.6, "Hadoop HDFS"),
    (3.7, 10.2, 1.3, 0.6, "MongoDB"),
    (5.3, 10.2, 1.3, 0.6, "Spark Job"),
    (6.9, 10.2, 1.3, 0.6, "Streamlit App"),
    (8.5, 10.2, 1.3, 0.6, "End User"),
    (10.1, 10.2, 1.3, 0.6, "HostFS")
]

for x, y, w, h, label in components:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                          edgecolor=color_accent, facecolor=color_box, linewidth=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, fontsize=9, fontweight='bold', 
           ha='center', va='center', color=color_text)

# PHASE 1: Data Generation & Ingestion
phase1_y = 9.5
phase1_box = Rectangle((0.2, phase1_y - 0.35), 13.6, 0.4, 
                       facecolor=color_phase_bg, edgecolor=color_phase, linewidth=2)
ax.add_patch(phase1_box)
ax.text(0.4, phase1_y, 'Phase 1: Data Generation & Ingestion', 
       fontsize=11, fontweight='bold', color=color_accent, va='center')

# Phase 1 interactions
interactions_p1 = [
    (0.5, 10.2, 0.5, 9.8, "IoT Sensors\nSimulation", "#E8F5E9"),
    (1.15, 9.8, 2.1, 9.8, ""),
    (2.1, 9.8, 3.7, 9.8, "Insert\nMetadata"),
    (3.7, 9.8, 0.3, 9.3, "Prepare\nDisease CSV"),
]

ax.text(0.8, 9.5, "Generate\n96 JSON Files", fontsize=8, ha='center', color='#ccc', style='italic')
ax.text(2.6, 9.5, "Write Sensor JSONs\n(Local/Shared)", fontsize=8, ha='center', color='#ccc', style='italic')
ax.text(3.7, 9.3, "Clean Disease\nMetadata (CSV)", fontsize=8, ha='center', color='#ccc', style='italic')

# Arrows for phase 1
arrow_p1_1 = FancyArrowPatch((1.15, 9.8), (2.1, 9.8), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow_p1_1)

arrow_p1_2 = FancyArrowPatch((2.8, 9.8), (3.7, 9.8), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow_p1_2)

arrow_p1_3 = FancyArrowPatch((3.7, 9.8), (2.1, 9.5), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color=color_arrow, linestyle='dashed')
ax.add_patch(arrow_p1_3)
ax.text(2.8, 9.2, "Command:\nhdfs dfs -put", fontsize=7, ha='center', color='#999', style='italic')

# Store data path
ax.text(1.15, 8.95, "Store Raw Data (/data/agri/sensors)", fontsize=8, ha='left', color='#aaa')

# PHASE 2: Batch Processing
phase2_y = 8.2
phase2_box = Rectangle((0.2, phase2_y - 0.35), 13.6, 0.4, 
                       facecolor=color_phase_bg, edgecolor=color_phase, linewidth=2)
ax.add_patch(phase2_box)
ax.text(0.4, phase2_y, 'Phase 2: Batch Processing', 
       fontsize=11, fontweight='bold', color=color_accent, va='center')

# Phase 2 interactions
ax.text(2.1, 7.9, "Read Sensor JSONs", fontsize=8, ha='center', color='#ccc')
ax.text(2.1, 7.7, "Read Disease CSV", fontsize=8, ha='center', color='#ccc')
ax.text(4.0, 7.8, "Filter, Aggregate\n(Daily Avg), Join", fontsize=8, ha='center', color='#ccc', style='italic')
ax.text(4.8, 7.4, "Write Output Parquet\n(aggdaily, diseasestats)", fontsize=8, ha='center', color='#ccc')

# Arrows for phase 2
arrow_p2_1 = FancyArrowPatch((2.1, 9.8), (2.1, 7.95), arrowstyle='<-', 
                           mutation_scale=20, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow_p2_1)

arrow_p2_2 = FancyArrowPatch((3.7, 9.8), (3.7, 7.75), arrowstyle='<-', 
                           mutation_scale=20, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow_p2_2)

arrow_p2_3 = FancyArrowPatch((2.8, 7.8), (5.3, 7.8), arrowstyle='->', 
                           mutation_scale=20, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow_p2_3)

arrow_p2_4 = FancyArrowPatch((5.3, 7.8), (2.1, 7.2), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow_p2_4)

# PHASE 3: Analytics Loading
phase3_y = 6.2
phase3_box = Rectangle((0.2, phase3_y - 0.35), 13.6, 0.4, 
                       facecolor=color_phase_bg, edgecolor=color_phase, linewidth=2)
ax.add_patch(phase3_box)
ax.text(0.4, phase3_y, 'Phase 3: Analytics Loading', 
       fontsize=11, fontweight='bold', color=color_accent, va='center')

# Phase 3 interactions
ax.text(3.7, 5.9, "Load Processed Results\n(analyticsdaily)", fontsize=8, ha='center', color='#ccc')
ax.text(3.7, 5.4, "Query Analytics Data", fontsize=8, ha='center', color='#ccc', style='italic')

# Arrow for phase 3
arrow_p3_1 = FancyArrowPatch((3.7, 7.2), (3.7, 5.95), arrowstyle='->', 
                           mutation_scale=20, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow_p3_1)

# PHASE 4: Visualization (with updated Dash App)
phase4_y = 3.8
phase4_box = Rectangle((0.2, phase4_y - 0.35), 13.6, 0.4, 
                       facecolor=color_phase_bg, edgecolor=color_phase, linewidth=2)
ax.add_patch(phase4_box)
ax.text(0.4, phase4_y, 'Phase 4: Visualization (Updated for Dash)', 
       fontsize=11, fontweight='bold', color=color_accent, va='center')

# Updated Dash component box (highlighted)
dash_box = FancyBboxPatch((5.8, 3.0), 2.2, 0.8, boxstyle="round,pad=0.05", 
                         edgecolor='#00ff00', facecolor='#1a3a1a', linewidth=3)
ax.add_patch(dash_box)
ax.text(6.9, 3.5, 'Dash App', fontsize=10, fontweight='bold', 
       ha='center', color='#00ff00')
ax.text(6.9, 3.15, '(Port 8050)', fontsize=8, ha='center', color='#7cb342')

# Phase 4 interactions
ax.text(4.0, 3.2, "Render Charts\n(Soil, Temp, Humidity)", fontsize=8, ha='center', color='#ccc')
ax.text(7.5, 2.5, "Display Modern Dashboard", fontsize=8, ha='center', color='#ccc', style='italic')

# Arrow for phase 4
arrow_p4_1 = FancyArrowPatch((3.7, 5.4), (6.0, 3.8), arrowstyle='->', 
                           mutation_scale=20, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow_p4_1)

# Features box
features_box = FancyBboxPatch((0.3, 1.0), 6.5, 1.8, boxstyle="round,pad=0.1", 
                             edgecolor=color_accent, facecolor=color_box, linewidth=2)
ax.add_patch(features_box)
ax.text(3.55, 2.5, '📊 Dash Dashboard Features', fontsize=10, fontweight='bold', 
       ha='center', color=color_accent)

features_text = """
✅ 5 Navigation Tabs (Home, Pipeline, Analytics, Advisory, Architecture)
✅ Interactive Plotly Charts (Soil, Temperature, Humidity)
✅ Intelligent Crop Advisory System (AI-powered recommendations)
✅ Real-time MongoDB Integration (Responsive analytics)
✅ Farm-Themed Design (Green colors, Bootstrap layout)
✅ One-Click Pipeline Automation (Run all 5 steps in ~1 minute)
"""

ax.text(3.55, 1.85, features_text, fontsize=7.5, ha='center', va='top', 
       color='#ccc', family='monospace')

# Technology Stack box
tech_box = FancyBboxPatch((7.2, 1.0), 6.5, 1.8, boxstyle="round,pad=0.1", 
                         edgecolor=color_accent, facecolor=color_box, linewidth=2)
ax.add_patch(tech_box)
ax.text(10.45, 2.5, '⚙️ Technology Stack', fontsize=10, fontweight='bold', 
       ha='center', color=color_accent)

tech_text = """
🐘 Hadoop 3.2.1 (Distributed Storage - HDFS)
⚡ Apache Spark 3.4.1 (Batch Processing)
🍃 MongoDB (Analytics Database on Port 27017)
📊 Dash/Plotly (Modern Interactive Dashboard)
🐳 Docker (Containerization & Orchestration)
🐍 Python 3.12 (Core Language)
"""

ax.text(10.45, 1.85, tech_text, fontsize=7.5, ha='center', va='top', 
       color='#ccc', family='monospace')

# Pipeline flow summary
summary_box = FancyBboxPatch((0.3, 0.05), 13.4, 0.7, boxstyle="round,pad=0.05", 
                            edgecolor=color_accent, facecolor='#0d2608', linewidth=2)
ax.add_patch(summary_box)
ax.text(7, 0.6, '🔄 Complete Pipeline Flow:', fontsize=9, fontweight='bold', 
       ha='center', color=color_accent)
ax.text(7, 0.25, 'IoT Sensors → Hadoop HDFS → Apache Spark → MongoDB → Dash Dashboard (Port 8050) → Farm Analytics', 
       fontsize=8, ha='center', color='#ccc', style='italic')

# Save figure
output_dir = os.path.join(os.path.dirname(__file__), 'app', 'images')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'pipeline_flowchart.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.3, 
           facecolor='#1a1a1a', edgecolor='none')
print(f"✓ Pipeline flowchart saved to: {output_path}")
plt.close()
