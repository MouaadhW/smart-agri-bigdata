#!/usr/bin/env python3
"""
Generate system architecture diagram for Smart Agri BigData Platform
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Set up figure
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Define colors
color_data = '#E8F5E9'
color_compute = '#BBDEFB'
color_storage = '#FFF9C4'
color_ui = '#F8BBD0'
color_arrow = '#424242'

# Title
ax.text(5, 9.5, 'Smart Agriculture Big Data Platform Architecture', 
        fontsize=20, fontweight='bold', ha='center')

# Layer 1: Data Generation (Top)
data_box = FancyBboxPatch((0.5, 7.5), 2, 1.2, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_box)
ax.text(1.5, 8.3, '📱 IoT Sensors', fontsize=11, fontweight='bold', ha='center')
ax.text(1.5, 7.95, '• Soil sensors', fontsize=9, ha='center')
ax.text(1.5, 7.7, '• Weather stations', fontsize=9, ha='center')

# Sensor simulator
data_sim_box = FancyBboxPatch((3, 7.5), 2, 1.2, boxstyle="round,pad=0.1", 
                             edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_sim_box)
ax.text(4, 8.3, '🔧 Data Generator', fontsize=11, fontweight='bold', ha='center')
ax.text(4, 7.95, 'simulate_sensors', fontsize=8, ha='center')
ax.text(4, 7.7, 'gateway.py', fontsize=8, ha='center')

# Disease metadata
disease_box = FancyBboxPatch((5.5, 7.5), 2, 1.2, boxstyle="round,pad=0.1", 
                            edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(disease_box)
ax.text(6.5, 8.3, '🏥 Disease Data', fontsize=11, fontweight='bold', ha='center')
ax.text(6.5, 7.95, 'prepare_disease', fontsize=8, ha='center')
ax.text(6.5, 7.7, 'metadata.py', fontsize=8, ha='center')

# Layer 2: Data Ingestion (Middle-Top)
hdfs_box = FancyBboxPatch((0.5, 5.5), 3, 1.5, boxstyle="round,pad=0.1", 
                         edgecolor='black', facecolor=color_storage, linewidth=2)
ax.add_patch(hdfs_box)
ax.text(2, 6.7, '🗄️ HDFS / Hadoop', fontsize=11, fontweight='bold', ha='center')
ax.text(2, 6.35, 'NameNode: 9870', fontsize=9, ha='center')
ax.text(2, 6, '/data/agri/sensors/', fontsize=8, ha='center')
ax.text(2, 5.7, '/data/agri/disease/', fontsize=8, ha='center')

# Layer 2: Processing (Middle)
spark_box = FancyBboxPatch((4, 5.5), 3, 1.5, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color_compute, linewidth=2)
ax.add_patch(spark_box)
ax.text(5.5, 6.7, '⚡ Apache Spark', fontsize=11, fontweight='bold', ha='center')
ax.text(5.5, 6.35, 'Batch Pipeline', fontsize=9, ha='center')
ax.text(5.5, 6, 'spark_batch', fontsize=8, ha='center')
ax.text(5.5, 5.7, 'pipeline.py', fontsize=8, ha='center')

# Layer 3: Analytics Storage (Bottom-Top)
mongo_box = FancyBboxPatch((0.5, 3.5), 3, 1.5, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color_storage, linewidth=2)
ax.add_patch(mongo_box)
ax.text(2, 4.7, '🍃 MongoDB', fontsize=11, fontweight='bold', ha='center')
ax.text(2, 4.35, 'Port: 27017', fontsize=9, ha='center')
ax.text(2, 4, 'Collections:', fontsize=8, ha='center')
ax.text(2, 3.7, 'analyticsdaily', fontsize=8, ha='center')

# Layer 3: Processing output
output_box = FancyBboxPatch((4, 3.5), 3, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='black', facecolor=color_storage, linewidth=2)
ax.add_patch(output_box)
ax.text(5.5, 4.7, '📊 Analytics Output', fontsize=11, fontweight='bold', ha='center')
ax.text(5.5, 4.35, 'Parquet Format', fontsize=9, ha='center')
ax.text(5.5, 4, '/aggdaily/', fontsize=8, ha='center')
ax.text(5.5, 3.7, '/diseasestats/', fontsize=8, ha='center')

# Layer 4: UI (Bottom)
ui_box = FancyBboxPatch((2.5, 1.2), 5, 1.5, boxstyle="round,pad=0.1", 
                       edgecolor='black', facecolor=color_ui, linewidth=2)
ax.add_patch(ui_box)
ax.text(5, 2.4, '🌐 Streamlit Dashboard', fontsize=12, fontweight='bold', ha='center')
ax.text(5, 2, 'Port: 8501', fontsize=9, ha='center')
ax.text(5, 1.6, 'Home | Runbook | Data | Analytics | Architecture', fontsize=8, ha='center')

# Docker Container label
docker_box = FancyBboxPatch((7.5, 3), 2.2, 4.5, boxstyle="round,pad=0.15", 
                           edgecolor='#2196F3', facecolor='none', linewidth=2, linestyle='--')
ax.add_patch(docker_box)
ax.text(8.6, 7.3, '🐳 Docker', fontsize=10, fontweight='bold', ha='center', color='#2196F3')
ax.text(8.6, 6.95, 'Containers', fontsize=9, ha='center', color='#2196F3')

# Arrows: Data generation → HDFS
arrow1 = FancyArrowPatch((2.5, 7.5), (2, 7), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow1)

arrow2 = FancyArrowPatch((4, 7.5), (2.8, 7), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow2)

arrow3 = FancyArrowPatch((6.5, 7.5), (3, 6.5), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow3)

# Arrow: HDFS → Spark
arrow4 = FancyArrowPatch((3.5, 6.2), (4, 6.2), arrowstyle='<->', 
                        mutation_scale=25, linewidth=2.5, color=color_arrow)
ax.add_patch(arrow4)
ax.text(3.75, 6.5, 'Process', fontsize=8, ha='center', style='italic')

# Arrow: Spark → MongoDB
arrow5 = FancyArrowPatch((4.8, 5.5), (2.5, 5), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow5)
ax.text(3.5, 5.3, 'Load', fontsize=8, ha='center', style='italic')

# Arrow: Spark → Output
arrow6 = FancyArrowPatch((5.5, 5.5), (5.5, 5), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow6)

# Arrow: MongoDB → Dashboard
arrow7 = FancyArrowPatch((2, 3.5), (3.5, 2.7), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow7)
ax.text(2.3, 3, 'Query', fontsize=8, ha='center', style='italic')

# Arrow: Output → Dashboard
arrow8 = FancyArrowPatch((5.5, 3.5), (5, 2.7), arrowstyle='->', 
                        mutation_scale=25, linewidth=2, color=color_arrow)
ax.add_patch(arrow8)
ax.text(5.7, 3, 'Display', fontsize=8, ha='center', style='italic')

# Data flow label
ax.text(5, 0.7, 'Data Flow: IoT → HDFS → Spark Processing → MongoDB → Streamlit Dashboard', 
        fontsize=9, ha='center', style='italic', color='#666')

# Save figure
output_dir = os.path.join(os.path.dirname(__file__), 'app', 'images')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'sys_arch.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Architecture diagram saved to: {output_path}")
plt.close()
