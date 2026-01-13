"""
Create a visual flowchart of the Smart Agri Big Data Pipeline
Shows the data flow from generation through visualization using Dash
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines
import os

def create_pipeline_flowchart():
    """Create and save the pipeline flowchart diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors for different phases
    color_data_gen = "#FFE5B4"      # Peach
    color_storage = "#B4D7FF"       # Light Blue
    color_processing = "#D7FFB4"    # Light Green
    color_analytics = "#FFB4D7"     # Light Pink
    color_visualization = "#FFD700" # Gold
    
    # Title
    ax.text(5, 9.5, "Smart Agri Big Data Pipeline Architecture", 
            fontsize=20, fontweight='bold', ha='center')
    
    # =============== PHASE 1: Data Generation & Ingestion (Top Row) ===============
    ax.text(5, 8.8, "PHASE 1: Data Generation & Ingestion", 
            fontsize=13, fontweight='bold', ha='center', color='#333')
    
    # Generator Script
    generator_box = FancyBboxPatch((0.3, 7.6), 2.2, 0.8, 
                                   boxstyle="round,pad=0.1", 
                                   edgecolor='#333', facecolor=color_data_gen, 
                                   linewidth=2)
    ax.add_patch(generator_box)
    ax.text(1.4, 8.0, "Sensor Data\nGenerator Script", fontsize=10, 
            ha='center', va='center', fontweight='bold')
    
    # HDFS Storage
    hdfs_box = FancyBboxPatch((3.5, 7.6), 2.2, 0.8, 
                              boxstyle="round,pad=0.1", 
                              edgecolor='#333', facecolor=color_storage, 
                              linewidth=2)
    ax.add_patch(hdfs_box)
    ax.text(4.6, 8.0, "Hadoop HDFS\nFile Storage", fontsize=10, 
            ha='center', va='center', fontweight='bold')
    
    # MongoDB Raw
    mongo_raw_box = FancyBboxPatch((6.8, 7.6), 2.2, 0.8, 
                                   boxstyle="round,pad=0.1", 
                                   edgecolor='#333', facecolor=color_storage, 
                                   linewidth=2)
    ax.add_patch(mongo_raw_box)
    ax.text(7.9, 8.0, "MongoDB\nRaw Data", fontsize=10, 
            ha='center', va='center', fontweight='bold')
    
    # Arrows for Phase 1
    arrow1 = FancyArrowPatch((2.5, 8.0), (3.5, 8.0), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666', linewidth=2.5)
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((5.7, 8.0), (6.8, 8.0), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666', linewidth=2.5)
    ax.add_patch(arrow2)
    
    # =============== PHASE 2: Batch Processing (Middle-Top Row) ===============
    ax.text(5, 6.8, "PHASE 2: Batch Processing", 
            fontsize=13, fontweight='bold', ha='center', color='#333')
    
    # Spark Job
    spark_box = FancyBboxPatch((2.2, 5.6), 2.8, 0.8, 
                               boxstyle="round,pad=0.1", 
                               edgecolor='#333', facecolor=color_processing, 
                               linewidth=2.5)
    ax.add_patch(spark_box)
    ax.text(3.6, 6.0, "Apache Spark\nBatch Job", fontsize=11, 
            ha='center', va='center', fontweight='bold')
    
    # Data Processing Details
    ax.text(3.6, 5.3, "• Aggregate sensor data\n• Detect anomalies\n• Compute statistics", 
            fontsize=8, ha='center', va='top', style='italic', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Processed Data Output
    processed_box = FancyBboxPatch((5.8, 5.6), 2.8, 0.8, 
                                   boxstyle="round,pad=0.1", 
                                   edgecolor='#333', facecolor=color_analytics, 
                                   linewidth=2.5)
    ax.add_patch(processed_box)
    ax.text(7.2, 6.0, "Processed Data\nResults", fontsize=11, 
            ha='center', va='center', fontweight='bold')
    
    # Arrows into Spark Job
    arrow3 = FancyArrowPatch((4.6, 7.6), (3.6, 6.4), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666', linewidth=2.5, linestyle='--')
    ax.add_patch(arrow3)
    
    arrow4 = FancyArrowPatch((7.9, 7.6), (7.2, 6.4), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666', linewidth=2.5, linestyle='--')
    ax.add_patch(arrow4)
    
    # Arrow from Spark to Output
    arrow5 = FancyArrowPatch((5.0, 6.0), (5.8, 6.0), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666', linewidth=2.5)
    ax.add_patch(arrow5)
    
    # =============== PHASE 3: Analytics Loading (Middle-Bottom Row) ===============
    ax.text(5, 4.6, "PHASE 3: Analytics Loading", 
            fontsize=13, fontweight='bold', ha='center', color='#333')
    
    # MongoDB Analytics Collections
    mongo_analytics_box = FancyBboxPatch((2.5, 3.2), 5, 0.8, 
                                         boxstyle="round,pad=0.1", 
                                         edgecolor='#333', facecolor=color_analytics, 
                                         linewidth=2.5)
    ax.add_patch(mongo_analytics_box)
    ax.text(5, 3.6, "MongoDB Analytics Collections\n(aggDaily, diseaseStats, warnings)", 
            fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Arrow from Processed Data to MongoDB
    arrow6 = FancyArrowPatch((7.2, 5.6), (5, 4.0), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666', linewidth=2.5)
    ax.add_patch(arrow6)
    
    # =============== PHASE 4: Visualization (Bottom Row) ===============
    ax.text(5, 2.4, "PHASE 4: Real-Time Dashboard Visualization", 
            fontsize=13, fontweight='bold', ha='center', color='#333')
    
    # Dash Web Application
    dash_box = FancyBboxPatch((2.0, 0.6), 6, 1.2, 
                              boxstyle="round,pad=0.1", 
                              edgecolor='#333', facecolor=color_visualization, 
                              linewidth=3)
    ax.add_patch(dash_box)
    ax.text(5, 1.3, "🌐 Dash Web Application (Port 8050)", fontsize=12, 
            ha='center', va='center', fontweight='bold', color='#000')
    ax.text(5, 0.9, "Real-time Analytics Dashboard | Disease Metrics | Sensor Data Visualization", 
            fontsize=9, ha='center', va='center', style='italic')
    
    # Arrow from MongoDB to Dash
    arrow7 = FancyArrowPatch((5, 3.2), (5, 1.8), 
                            arrowstyle='->', mutation_scale=25, 
                            color='#333', linewidth=3)
    ax.add_patch(arrow7)
    
    # =============== Add Legend ===============
    legend_y = 0.2
    ax.text(0.2, legend_y, "Data Flow →", fontsize=9, style='italic', color='#666')
    
    # Add technology stack notes
    tech_box = FancyBboxPatch((0.1, -0.8), 9.8, 0.6, 
                              boxstyle="round,pad=0.05", 
                              edgecolor='#999', facecolor='#f9f9f9', 
                              linewidth=1, linestyle='--', alpha=0.7)
    ax.add_patch(tech_box)
    ax.text(5, -0.5, "🔧 Tech Stack: Python | Apache Spark | Hadoop HDFS | MongoDB | Dash | Docker | Docker Compose", 
            fontsize=8, ha='center', va='center', style='italic', color='#555')
    
    plt.tight_layout()
    
    # Save the figure
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "pipeline_flowchart.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Pipeline flowchart saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    create_pipeline_flowchart()
