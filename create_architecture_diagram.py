#!/usr/bin/env python3
"""
Generate system architecture diagram for Smart Agri BigData Platform
Updated for modern Dash/Plotly UI
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Set up figure
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Define colors - Farm themed
color_data = '#E8F5E9'        # Light green
color_compute = '#BBDEFB'     # Light blue
color_storage = '#FFF9C4'     # Light yellow
color_ui = '#F0E5CC'          # Light cream/tan
color_arrow = '#2d5016'       # Dark farm green
color_accent = '#7cb342'      # Bright farm green

# Title
title_box = FancyBboxPatch((0.3, 9), 9.4, 0.8, boxstyle="round,pad=0.1", 
                           edgecolor=color_accent, facecolor='#f0f7f4', linewidth=3)
ax.add_patch(title_box)
ax.text(5, 9.55, '🌾 Smart Agriculture Big Data Platform Architecture', 
        fontsize=18, fontweight='bold', ha='center', color='#2d5016')
ax.text(5, 9.15, 'Modern Dash/Plotly Dashboard with Intelligent Crop Advisory', 
        fontsize=9, ha='center', color='#558b2f', style='italic')

# Layer 1: Data Generation (Top)
data_box = FancyBboxPatch((0.5, 7.6), 1.8, 1.0, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_box)
ax.text(1.4, 8.35, '📱 IoT Sensors', fontsize=9, fontweight='bold', ha='center')
ax.text(1.4, 8.05, 'Soil Moisture', fontsize=7, ha='center')
ax.text(1.4, 7.8, 'Temperature', fontsize=7, ha='center')

# Sensor simulator
data_sim_box = FancyBboxPatch((2.6, 7.6), 1.8, 1.0, boxstyle="round,pad=0.1", 
                             edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_sim_box)
ax.text(3.5, 8.35, '🔧 Data Generator', fontsize=9, fontweight='bold', ha='center')
ax.text(3.5, 8.05, 'simulate_', fontsize=7, ha='center')
ax.text(3.5, 7.8, 'sensors.py', fontsize=7, ha='center')

# Disease metadata
disease_box = FancyBboxPatch((4.7, 7.6), 1.8, 1.0, boxstyle="round,pad=0.1", 
                            edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(disease_box)
ax.text(5.6, 8.35, '🏥 Disease Data', fontsize=9, fontweight='bold', ha='center')
ax.text(5.6, 8.05, 'prepare_', fontsize=7, ha='center')
ax.text(5.6, 7.8, 'metadata.py', fontsize=7, ha='center')

# Pipeline Orchestrator
pipeline_box = FancyBboxPatch((6.8, 7.6), 1.8, 1.0, boxstyle="round,pad=0.1", 
                             edgecolor='black', facecolor='#FFE0B2', linewidth=2)
ax.add_patch(pipeline_box)
ax.text(7.7, 8.35, '⚙️ Orchestrator', fontsize=9, fontweight='bold', ha='center')
ax.text(7.7, 8.05, 'run_full_', fontsize=7, ha='center')
ax.text(7.7, 7.8, 'pipeline.py', fontsize=7, ha='center')

# Layer 2: Distributed Storage (Middle-Top)
hdfs_box = FancyBboxPatch((0.5, 5.8), 2.8, 1.2, boxstyle="round,pad=0.1", 
                         edgecolor='black', facecolor=color_storage, linewidth=2)
ax.add_patch(hdfs_box)
ax.text(1.9, 6.7, '🗄️ HDFS / Hadoop', fontsize=10, fontweight='bold', ha='center')
ax.text(1.9, 6.3, 'Distributed Storage', fontsize=7, ha='center')
ax.text(1.9, 6, '/data/agri/sensors/', fontsize=6, ha='center')

# Layer 2: Processing (Middle)
spark_box = FancyBboxPatch((3.7, 5.8), 2.8, 1.2, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color_compute, linewidth=2)
ax.add_patch(spark_box)
ax.text(5.1, 6.7, '⚡ Apache Spark', fontsize=10, fontweight='bold', ha='center')
ax.text(5.1, 6.3, 'Batch Processing', fontsize=7, ha='center')
ax.text(5.1, 6, 'Daily Aggregation', fontsize=6, ha='center')

# MongoDB Analytics
mongo_box = FancyBboxPatch((6.9, 5.8), 2.8, 1.2, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color_storage, linewidth=2)
ax.add_patch(mongo_box)
ax.text(8.3, 6.7, '🍃 MongoDB', fontsize=10, fontweight='bold', ha='center')
ax.text(8.3, 6.3, 'Analytics DB', fontsize=7, ha='center')
ax.text(8.3, 6, 'Collections', fontsize=6, ha='center')

# Layer 3: Dashboard Components (Middle-Bottom)
# Home Tab
home_tab = FancyBboxPatch((0.3, 4.3), 1.4, 1.0, boxstyle="round,pad=0.08", 
                         edgecolor='black', facecolor='#E3F2FD', linewidth=1.5)
ax.add_patch(home_tab)
ax.text(1.0, 5.05, '🏠 Home', fontsize=8, fontweight='bold', ha='center')
ax.text(1.0, 4.7, 'Overview', fontsize=6, ha='center')
ax.text(1.0, 4.45, 'Tech Stack', fontsize=6, ha='center')

# Pipeline Tab
pipeline_tab = FancyBboxPatch((1.9, 4.3), 1.4, 1.0, boxstyle="round,pad=0.08", 
                             edgecolor='black', facecolor='#FFF3E0', linewidth=1.5)
ax.add_patch(pipeline_tab)
ax.text(2.6, 5.05, '🚀 Pipeline', fontsize=8, fontweight='bold', ha='center')
ax.text(2.6, 4.7, 'Run Steps', fontsize=6, ha='center')
ax.text(2.6, 4.45, 'Status', fontsize=6, ha='center')

# Analytics Tab
analytics_tab = FancyBboxPatch((3.5, 4.3), 1.4, 1.0, boxstyle="round,pad=0.08", 
                              edgecolor='black', facecolor='#F3E5F5', linewidth=1.5)
ax.add_patch(analytics_tab)
ax.text(4.2, 5.05, '📈 Analytics', fontsize=8, fontweight='bold', ha='center')
ax.text(4.2, 4.7, 'Charts', fontsize=6, ha='center')
ax.text(4.2, 4.45, 'Metrics', fontsize=6, ha='center')

# Advisory Tab (NEW)
advisory_tab = FancyBboxPatch((5.1, 4.3), 1.4, 1.0, boxstyle="round,pad=0.08", 
                             edgecolor=color_accent, facecolor='#E8F5E9', linewidth=2)
ax.add_patch(advisory_tab)
ax.text(5.8, 5.05, '🌾 Advisory', fontsize=8, fontweight='bold', ha='center', color=color_accent)
ax.text(5.8, 4.7, 'AI Crop', fontsize=6, ha='center')
ax.text(5.8, 4.45, 'Predictions', fontsize=6, ha='center')

# Architecture Tab
arch_tab = FancyBboxPatch((6.7, 4.3), 1.4, 1.0, boxstyle="round,pad=0.08", 
                         edgecolor='black', facecolor='#F1F8E9', linewidth=1.5)
ax.add_patch(arch_tab)
ax.text(7.4, 5.05, '🏗️ Architecture', fontsize=8, fontweight='bold', ha='center')
ax.text(7.4, 4.7, 'Diagram', fontsize=6, ha='center')
ax.text(7.4, 4.45, 'Tech Docs', fontsize=6, ha='center')

# Dash Framework Container
dash_container = FancyBboxPatch((0.2, 2.9), 8.6, 1.3, boxstyle="round,pad=0.1", 
                               edgecolor=color_accent, facecolor=color_ui, linewidth=2.5)
ax.add_patch(dash_container)
ax.text(4.5, 3.95, '📊 Dash/Plotly Dashboard Framework', fontsize=11, fontweight='bold', ha='center', color='#2d5016')
ax.text(4.5, 3.6, 'Modern Interactive UI | Farm-Themed Colors | Responsive Bootstrap Layout', fontsize=7, ha='center', color='#558b2f')
ax.text(4.5, 3.25, 'Port: 8050 | Real-time MongoDB Integration | Intelligent Crop Advisory System', fontsize=7, ha='center', color='#558b2f')

# Docker Container label (Left side)
docker_box = FancyBboxPatch((0.15, 0.8), 4, 1.7, boxstyle="round,pad=0.15", 
                           edgecolor='#2196F3', facecolor='none', linewidth=2.5, linestyle='--')
ax.add_patch(docker_box)
ax.text(2.15, 2.35, '🐳 Docker Containers', fontsize=9, fontweight='bold', ha='center', color='#2196F3')

# Docker services
services_text = 'Hadoop NameNode • Spark • MongoDB • App Container'
ax.text(2.15, 2.0, services_text, fontsize=6.5, ha='center', color='#2196F3')

# Host label (Right side)
host_box = FancyBboxPatch((5.85, 0.8), 4, 1.7, boxstyle="round,pad=0.15", 
                         edgecolor='#FF6F00', facecolor='none', linewidth=2.5, linestyle='--')
ax.add_patch(host_box)
ax.text(7.85, 2.35, '💻 Host Machine', fontsize=9, fontweight='bold', ha='center', color='#FF6F00')
services_text2 = 'Python Environment • Dash Server • Data Scripts'
ax.text(7.85, 2.0, services_text2, fontsize=6.5, ha='center', color='#FF6F00')

# Arrows: Data generation → HDFS
arrow1 = FancyArrowPatch((1.4, 7.6), (1.5, 7.0), arrowstyle='->', 
                        mutation_scale=18, linewidth=2, color=color_arrow)
ax.add_patch(arrow1)

arrow2 = FancyArrowPatch((3.5, 7.6), (2.8, 7.0), arrowstyle='->', 
                        mutation_scale=18, linewidth=2, color=color_arrow)
ax.add_patch(arrow2)

arrow3 = FancyArrowPatch((5.6, 7.6), (5.1, 7.0), arrowstyle='->', 
                        mutation_scale=18, linewidth=2, color=color_arrow)
ax.add_patch(arrow3)

# Arrow: HDFS ↔ Spark (bidirectional)
arrow4 = FancyArrowPatch((3.3, 6.4), (3.7, 6.4), arrowstyle='<->', 
                        mutation_scale=18, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow4)
ax.text(3.5, 6.65, 'Read/Write', fontsize=6, ha='center', style='italic')

# Arrow: Spark → MongoDB
arrow5 = FancyArrowPatch((6.5, 6.4), (6.9, 6.4), arrowstyle='->', 
                        mutation_scale=18, linewidth=2, color=color_arrow)
ax.add_patch(arrow5)
ax.text(6.7, 6.65, 'Load', fontsize=6, ha='center', style='italic', color=color_arrow)

# Arrow: Dashboard ← MongoDB
arrow6 = FancyArrowPatch((8.3, 5.8), (5, 4.2), arrowstyle='->', 
                        mutation_scale=18, linewidth=2.5, color=color_accent)
ax.add_patch(arrow6)
ax.text(6.8, 4.9, 'Query', fontsize=6, ha='center', style='italic', color=color_accent, fontweight='bold')

# Arrow: Orchestrator → Pipeline
arrow7 = FancyArrowPatch((7.7, 7.6), (5, 2.9), arrowstyle='->', 
                        mutation_scale=18, linewidth=2, color='#FF6F00')
ax.add_patch(arrow7)
ax.text(6.5, 5.0, 'Execute', fontsize=6, ha='center', style='italic', color='#FF6F00')

# Data flow label
ax.text(5, 0.45, 'Data Flow: IoT → HDFS → Spark Processing → MongoDB → Dash Dashboard', 
        fontsize=8, ha='center', style='italic', color='#666', fontweight='bold')
ax.text(5, 0.1, 'Features: One-Click Pipeline • Real-Time Charts • Intelligent Crop Advisory • Responsive UI', 
        fontsize=7, ha='center', style='italic', color='#888')

# Save figure
output_dir = os.path.join(os.path.dirname(__file__), 'app', 'images')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'sys_arch.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Architecture diagram saved to: {output_path}")
plt.close()

# Arrows: Data generation → HDFS
arrow1 = FancyArrowPatch((1.4, 8.3), (1.5, 7.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow1)

arrow2 = FancyArrowPatch((3.5, 8.3), (2.8, 7.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow2)

arrow3 = FancyArrowPatch((5.6, 8.3), (5.1, 7.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow3)

# Arrow: HDFS ↔ Spark (bidirectional)
arrow4 = FancyArrowPatch((3.3, 7.1), (3.7, 7.1), arrowstyle='<->', 
                        mutation_scale=20, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow4)
ax.text(3.5, 7.35, 'Read/Write', fontsize=7, ha='center', style='italic')

# Arrow: Spark → MongoDB
arrow5 = FancyArrowPatch((6.5, 7.1), (6.9, 7.1), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color=color_arrow)
ax.add_patch(arrow5)
ax.text(6.7, 7.35, 'Load', fontsize=7, ha='center', style='italic', color=color_arrow)

# Arrow: Dashboard ← MongoDB
arrow6 = FancyArrowPatch((8.3, 6.5), (5, 5), arrowstyle='->', 
                        mutation_scale=20, linewidth=2.5, color=color_accent)
ax.add_patch(arrow6)
ax.text(7, 5.8, 'Query Analytics', fontsize=7, ha='center', style='italic', color=color_accent, fontweight='bold')

# Arrow: Orchestrator → Pipeline
arrow7 = FancyArrowPatch((7.7, 8.3), (5, 3.5), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='#FF6F00')
ax.add_patch(arrow7)
ax.text(6.5, 5.8, 'Execute', fontsize=7, ha='center', style='italic', color='#FF6F00')

# Data flow label
ax.text(5, 1.1, 'Data Flow: IoT Sensors → HDFS → Spark Processing → MongoDB → Dash Dashboard', 
        fontsize=9, ha='center', style='italic', color='#666', fontweight='bold')
ax.text(5, 0.7, 'Features: One-Click Pipeline • Real-Time Charts • Intelligent Crop Advisory • Responsive UI', 
        fontsize=8, ha='center', style='italic', color='#888')

# Save figure
output_dir = os.path.join(os.path.dirname(__file__), 'app', 'images')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'sys_arch.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.3, facecolor='white')
print(f"✅ Architecture diagram saved to: {output_path}")
plt.close()
