"""
Create a visual architecture diagram of the Smart Agri Big Data System
Shows all components and their interactions
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import os

def create_architecture_diagram():
    """Create and save the architecture diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 11))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    ax.text(8, 10.5, "Smart Agri Big Data System Architecture", 
            fontsize=22, fontweight='bold', ha='center')
    ax.text(8, 10.0, "Comprehensive Data Pipeline from Sensors to Analytics Dashboard", 
            fontsize=11, ha='center', style='italic', color='#666')
    
    # Define colors
    color_sensors = "#FFE5B4"      # Peach
    color_ingestion = "#B4D7FF"    # Light Blue
    color_storage = "#B4E5FF"      # Lighter Blue
    color_processing = "#D7FFB4"   # Light Green
    color_analytics = "#FFB4D7"    # Light Pink
    color_app = "#FFD700"          # Gold
    color_container = "#E8E8E8"    # Light Gray
    
    # =============== CONTAINER LAYER (Top) ===============
    container_y = 9.2
    ax.text(8, 9.7, "🐳 Docker Containers", fontsize=12, fontweight='bold', 
            ha='center', color='#333')
    
    # Docker Compose container box
    docker_box = FancyBboxPatch((0.5, container_y - 0.35), 15, 0.4, 
                                boxstyle="round,pad=0.02", 
                                edgecolor='#888', facecolor='#f0f0f0', 
                                linewidth=2, linestyle='--', alpha=0.6)
    ax.add_patch(docker_box)
    ax.text(0.7, container_y - 0.15, "docker-compose orchestrates all services", 
            fontsize=8, style='italic', color='#666')
    
    # =============== LAYER 1: Data Sources & Generation ===============
    layer1_y = 7.8
    ax.text(8, layer1_y + 0.7, "LAYER 1: Data Generation & Sources", 
            fontsize=12, fontweight='bold', ha='center', color='#333')
    
    # Sensors
    sensor_box = FancyBboxPatch((1, layer1_y - 0.3), 3, 0.6, 
                                boxstyle="round,pad=0.05", 
                                edgecolor='#333', facecolor=color_sensors, 
                                linewidth=2)
    ax.add_patch(sensor_box)
    ax.text(2.5, layer1_y, "IoT Sensors\nTemperature\nMoisture\nHumidity", 
            fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Generator Script
    gen_box = FancyBboxPatch((5.5, layer1_y - 0.3), 3, 0.6, 
                             boxstyle="round,pad=0.05", 
                             edgecolor='#333', facecolor=color_sensors, 
                             linewidth=2)
    ax.add_patch(gen_box)
    ax.text(7, layer1_y, "Sensor Data\nGenerator Script\n(Python)", 
            fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Disease Metadata
    disease_box = FancyBboxPatch((10, layer1_y - 0.3), 3, 0.6, 
                                 boxstyle="round,pad=0.05", 
                                 edgecolor='#333', facecolor=color_sensors, 
                                 linewidth=2)
    ax.add_patch(disease_box)
    ax.text(11.5, layer1_y, "Disease\nMetadata\nReference Data", 
            fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Arrow from sensors to generator
    arrow1 = FancyArrowPatch((4, layer1_y), (5.5, layer1_y), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2)
    ax.add_patch(arrow1)
    
    # =============== LAYER 2: Data Ingestion & Storage ===============
    layer2_y = 6.0
    ax.text(8, layer2_y + 0.8, "LAYER 2: Data Ingestion & Storage", 
            fontsize=12, fontweight='bold', ha='center', color='#333')
    
    # Hadoop HDFS
    hdfs_box = FancyBboxPatch((1.5, layer2_y - 0.35), 3.5, 0.7, 
                              boxstyle="round,pad=0.05", 
                              edgecolor='#333', facecolor=color_ingestion, 
                              linewidth=2.5)
    ax.add_patch(hdfs_box)
    ax.text(3.25, layer2_y, "🐘 Hadoop HDFS\nDistributed\nFile Storage", 
            fontsize=9, ha='center', va='center', fontweight='bold')
    
    # MongoDB (Raw)
    mongo_raw_box = FancyBboxPatch((6, layer2_y - 0.35), 3.5, 0.7, 
                                   boxstyle="round,pad=0.05", 
                                   edgecolor='#333', facecolor=color_storage, 
                                   linewidth=2.5)
    ax.add_patch(mongo_raw_box)
    ax.text(7.75, layer2_y, "MongoDB\n(Raw Collections)\ngateway_data\ndisease_meta", 
            fontsize=8.5, ha='center', va='center', fontweight='bold')
    
    # Message Queue / Buffer (conceptual)
    queue_box = FancyBboxPatch((10.5, layer2_y - 0.35), 3.5, 0.7, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='#333', facecolor=color_ingestion, 
                               linewidth=2.5)
    ax.add_patch(queue_box)
    ax.text(12.25, layer2_y, "Data Pipeline\nGateway\nBatch Collection", 
            fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Arrows from generator to storage
    arrow2 = FancyArrowPatch((7, layer1_y - 0.3), (3.25, layer2_y + 0.35), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2)
    ax.add_patch(arrow2)
    
    arrow3 = FancyArrowPatch((7, layer1_y - 0.3), (7.75, layer2_y + 0.35), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2)
    ax.add_patch(arrow3)
    
    arrow4 = FancyArrowPatch((11.5, layer1_y - 0.3), (12.25, layer2_y + 0.35), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2)
    ax.add_patch(arrow4)
    
    # =============== LAYER 3: Batch Processing ===============
    layer3_y = 4.2
    ax.text(8, layer3_y + 0.8, "LAYER 3: Batch Processing & Transformation", 
            fontsize=12, fontweight='bold', ha='center', color='#333')
    
    # Spark Job
    spark_box = FancyBboxPatch((2, layer3_y - 0.4), 5, 0.8, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='#333', facecolor=color_processing, 
                               linewidth=2.5)
    ax.add_patch(spark_box)
    ax.text(4.5, layer3_y + 0.15, "Apache Spark Batch Job", fontsize=10, 
            ha='center', va='center', fontweight='bold')
    ax.text(4.5, layer3_y - 0.15, "Aggregation | Disease Detection | Statistics", 
            fontsize=8, ha='center', va='center', style='italic')
    
    # Processed Data Storage
    processed_box = FancyBboxPatch((9, layer3_y - 0.4), 5, 0.8, 
                                   boxstyle="round,pad=0.05", 
                                   edgecolor='#333', facecolor=color_analytics, 
                                   linewidth=2.5)
    ax.add_patch(processed_box)
    ax.text(11.5, layer3_y + 0.15, "MongoDB Analytics DB", fontsize=10, 
            ha='center', va='center', fontweight='bold')
    ax.text(11.5, layer3_y - 0.15, "aggDaily | diseaseStats | warnings", 
            fontsize=8, ha='center', va='center', style='italic')
    
    # Arrows from storage to Spark
    arrow5 = FancyArrowPatch((3.25, layer2_y - 0.35), (3.8, layer3_y + 0.4), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2, linestyle='--')
    ax.add_patch(arrow5)
    
    arrow6 = FancyArrowPatch((7.75, layer2_y - 0.35), (4.5, layer3_y + 0.4), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2, linestyle='--')
    ax.add_patch(arrow6)
    
    arrow7 = FancyArrowPatch((12.25, layer2_y - 0.35), (5.2, layer3_y + 0.4), 
                            arrowstyle='->', mutation_scale=15, 
                            color='#666', linewidth=2, linestyle='--')
    ax.add_patch(arrow7)
    
    # Arrow from Spark to Analytics DB
    arrow8 = FancyArrowPatch((7, layer3_y), (9, layer3_y), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#333', linewidth=3)
    ax.add_patch(arrow8)
    
    # =============== LAYER 4: Visualization & User Interface ===============
    layer4_y = 2.0
    ax.text(8, layer4_y + 1.0, "LAYER 4: Real-Time Analytics & Visualization", 
            fontsize=12, fontweight='bold', ha='center', color='#333')
    
    # Dash Application
    dash_box = FancyBboxPatch((2.5, layer4_y - 0.5), 11, 1.0, 
                              boxstyle="round,pad=0.05", 
                              edgecolor='#333', facecolor=color_app, 
                              linewidth=3)
    ax.add_patch(dash_box)
    ax.text(8, layer4_y + 0.3, "Dash Web Application (Port 8050) - Modern Analytics Dashboard", 
            fontsize=11, ha='center', va='center', fontweight='bold')
    ax.text(8, layer4_y - 0.15, "Real-time Charts | Disease Metrics | Sensor Data | System Architecture | System Status", 
            fontsize=9, ha='center', va='center', style='italic')
    
    # Arrow from MongoDB to Dash
    arrow9 = FancyArrowPatch((11.5, layer3_y - 0.4), (8, layer4_y + 0.5), 
                            arrowstyle='->', mutation_scale=25, 
                            color='#333', linewidth=3)
    ax.add_patch(arrow9)
    
    # =============== LEGEND & NOTES ===============
    legend_y = 0.6
    
    # Data Flow Types
    ax.text(1, legend_y + 0.3, "Data Flow Types:", fontsize=9, fontweight='bold')
    ax.plot([1.5, 2], [legend_y + 0.2, legend_y + 0.2], 'o-', color='#666', linewidth=2, markersize=4)
    ax.text(2.2, legend_y + 0.2, "Synchronous", fontsize=8, va='center')
    
    ax.plot([4.5, 5], [legend_y + 0.2, legend_y + 0.2], 'o--', color='#666', linewidth=2, markersize=4)
    ax.text(5.2, legend_y + 0.2, "Batch Processing", fontsize=8, va='center')
    
    # Technology Stack Summary
    tech_y = -0.2
    tech_text = "Tech Stack: Python 3.12 | Hadoop HDFS | Apache Spark | MongoDB | Plotly/Dash | Docker & Docker Compose"
    ax.text(8, tech_y, tech_text, fontsize=9, ha='center', style='italic', 
            color='#555', bbox=dict(boxstyle='round', facecolor='#f9f9f9', alpha=0.8, pad=0.5))
    
    plt.tight_layout()
    
    # Save the figure
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "architecture_diagram.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Architecture diagram saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    create_architecture_diagram()
